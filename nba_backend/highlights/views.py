from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, BasePermission
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from .models import Highlight
from .serializers import HighlightSerializer


class IsAdminRole(BasePermission):
    """检查用户是否为管理员角色"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'


class HighlightViewSet(viewsets.ModelViewSet):
    queryset = Highlight.objects.all()
    serializer_class = HighlightSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'increment_views']:
            return [AllowAny()]
        return [IsAdminRole()]

    def get_queryset(self):
        queryset = Highlight.objects.all()
        if self.action in ['list', 'retrieve'] and not (self.request.user and self.request.user.is_authenticated and self.request.user.role == 'admin'):
            queryset = queryset.filter(is_active=True)
        return queryset
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def create(self, request, *args, **kwargs):
        """创建精彩回放，处理文件上传"""
        data = request.data.copy()
        
        # 处理布尔值字段（从字符串转换）
        if 'is_active' in data:
            data['is_active'] = data['is_active'] in ['1', 'true', 'True', True]
        
        # 处理视频文件上传
        if 'video' in request.FILES:
            video_file = request.FILES['video']
            video_path = f'highlights/videos/{video_file.name}'
            saved_path = default_storage.save(video_path, ContentFile(video_file.read()))
            data['video_url'] = saved_path
        
        # 处理封面图片上传
        if 'cover_image' in request.FILES:
            cover_file = request.FILES['cover_image']
            cover_path = f'highlights/covers/{cover_file.name}'
            saved_path = default_storage.save(cover_path, ContentFile(cover_file.read()))
            data['cover_image'] = saved_path
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        """更新精彩回放，处理文件上传"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy()
        
        # 处理布尔值字段（从字符串转换）
        if 'is_active' in data:
            data['is_active'] = data['is_active'] in ['1', 'true', 'True', True]
        
        # 处理视频文件上传
        if 'video' in request.FILES:
            # 删除旧文件
            if instance.video_url and default_storage.exists(instance.video_url):
                default_storage.delete(instance.video_url)
            
            video_file = request.FILES['video']
            video_path = f'highlights/videos/{video_file.name}'
            saved_path = default_storage.save(video_path, ContentFile(video_file.read()))
            data['video_url'] = saved_path
        
        # 处理封面图片上传
        if 'cover_image' in request.FILES:
            # 删除旧文件
            if instance.cover_image and default_storage.exists(instance.cover_image):
                default_storage.delete(instance.cover_image)
            
            cover_file = request.FILES['cover_image']
            cover_path = f'highlights/covers/{cover_file.name}'
            saved_path = default_storage.save(cover_path, ContentFile(cover_file.read()))
            data['cover_image'] = saved_path
        
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def increment_views(self, request, pk=None):
        """增加观看次数"""
        highlight = self.get_object()
        highlight.views += 1
        highlight.save()
        return Response({'views': highlight.views})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminRole])
    def upload_cover(self, request, pk=None):
        """单独上传封面图片"""
        highlight = self.get_object()
        
        if 'cover_image' in request.FILES:
            # 删除旧封面
            if highlight.cover_image and default_storage.exists(highlight.cover_image):
                default_storage.delete(highlight.cover_image)
            
            cover_file = request.FILES['cover_image']
            cover_path = f'highlights/covers/{cover_file.name}'
            saved_path = default_storage.save(cover_path, ContentFile(cover_file.read()))
            highlight.cover_image = saved_path
            highlight.save()
            
            serializer = self.get_serializer(highlight)
            return Response(serializer.data)
        
        return Response({'error': '没有上传文件'}, status=status.HTTP_400_BAD_REQUEST)


from django.db import transaction
from .models import HighlightLike, HighlightFavorite


class HighlightLikeView(viewsets.ViewSet):
    """视频点赞视图"""
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """点赞视频"""
        try:
            highlight = Highlight.objects.get(pk=pk)
        except Highlight.DoesNotExist:
            return Response({'error': '视频不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        with transaction.atomic():
            like, created = HighlightLike.objects.get_or_create(
                user=request.user,
                highlight=highlight
            )
            
            if created:
                # 增加点赞数
                highlight.likes += 1
                highlight.save()
                return Response({'message': '点赞成功', 'is_liked': True}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': '已经点赞过了', 'is_liked': True}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['delete'])
    def unlike(self, request, pk=None):
        """取消点赞"""
        try:
            highlight = Highlight.objects.get(pk=pk)
        except Highlight.DoesNotExist:
            return Response({'error': '视频不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        with transaction.atomic():
            try:
                like = HighlightLike.objects.get(user=request.user, highlight=highlight)
                like.delete()
                # 减少点赞数
                if highlight.likes > 0:
                    highlight.likes -= 1
                    highlight.save()
                return Response({'message': '取消点赞成功', 'is_liked': False}, status=status.HTTP_200_OK)
            except HighlightLike.DoesNotExist:
                return Response({'message': '未点赞过', 'is_liked': False}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        """获取点赞状态"""
        try:
            highlight = Highlight.objects.get(pk=pk)
        except Highlight.DoesNotExist:
            return Response({'error': '视频不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        is_liked = HighlightLike.objects.filter(user=request.user, highlight=highlight).exists()
        is_favorited = HighlightFavorite.objects.filter(user=request.user, highlight=highlight).exists()
        
        return Response({
            'is_liked': is_liked,
            'is_favorited': is_favorited,
            'likes': highlight.likes,
            'favorites': highlight.favorites
        })


class HighlightFavoriteView(viewsets.ViewSet):
    """视频收藏视图"""
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        """收藏视频"""
        try:
            highlight = Highlight.objects.get(pk=pk)
        except Highlight.DoesNotExist:
            return Response({'error': '视频不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        with transaction.atomic():
            favorite, created = HighlightFavorite.objects.get_or_create(
                user=request.user,
                highlight=highlight
            )
            
            if created:
                # 增加收藏数
                highlight.favorites += 1
                highlight.save()
                return Response({'message': '收藏成功', 'is_favorited': True}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': '已经收藏过了', 'is_favorited': True}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['delete'])
    def unfavorite(self, request, pk=None):
        """取消收藏"""
        try:
            highlight = Highlight.objects.get(pk=pk)
        except Highlight.DoesNotExist:
            return Response({'error': '视频不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        with transaction.atomic():
            try:
                favorite = HighlightFavorite.objects.get(user=request.user, highlight=highlight)
                favorite.delete()
                # 减少收藏数
                if highlight.favorites > 0:
                    highlight.favorites -= 1
                    highlight.save()
                return Response({'message': '取消收藏成功', 'is_favorited': False}, status=status.HTTP_200_OK)
            except HighlightFavorite.DoesNotExist:
                return Response({'message': '未收藏过', 'is_favorited': False}, status=status.HTTP_200_OK)
