from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import Article, ArticleLike, ArticleFavorite


class ArticleLikeView(viewsets.ViewSet):
    """文章点赞视图"""
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """点赞文章"""
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response({'error': '文章不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        with transaction.atomic():
            like, created = ArticleLike.objects.get_or_create(
                user=request.user,
                article=article
            )
            
            if created:
                # 增加点赞数
                article.likes += 1
                article.save()
                return Response({'message': '点赞成功', 'is_liked': True}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': '已经点赞过了', 'is_liked': True}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['delete'])
    def unlike(self, request, pk=None):
        """取消点赞"""
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response({'error': '文章不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        with transaction.atomic():
            try:
                like = ArticleLike.objects.get(user=request.user, article=article)
                like.delete()
                # 减少点赞数
                if article.likes > 0:
                    article.likes -= 1
                    article.save()
                return Response({'message': '取消点赞成功', 'is_liked': False}, status=status.HTTP_200_OK)
            except ArticleLike.DoesNotExist:
                return Response({'message': '未点赞过', 'is_liked': False}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        """获取点赞状态"""
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response({'error': '文章不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        is_liked = ArticleLike.objects.filter(user=request.user, article=article).exists()
        is_favorited = ArticleFavorite.objects.filter(user=request.user, article=article).exists()
        
        return Response({
            'is_liked': is_liked,
            'is_favorited': is_favorited,
            'likes': article.likes,
            'favorites': article.favorites
        })


class ArticleFavoriteView(viewsets.ViewSet):
    """文章收藏视图"""
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        """收藏文章"""
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response({'error': '文章不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        with transaction.atomic():
            favorite, created = ArticleFavorite.objects.get_or_create(
                user=request.user,
                article=article
            )
            
            if created:
                # 增加收藏数
                article.favorites += 1
                article.save()
                return Response({'message': '收藏成功', 'is_favorited': True}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': '已经收藏过了', 'is_favorited': True}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['delete'])
    def unfavorite(self, request, pk=None):
        """取消收藏"""
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response({'error': '文章不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        with transaction.atomic():
            try:
                favorite = ArticleFavorite.objects.get(user=request.user, article=article)
                favorite.delete()
                # 减少收藏数
                if article.favorites > 0:
                    article.favorites -= 1
                    article.save()
                return Response({'message': '取消收藏成功', 'is_favorited': False}, status=status.HTTP_200_OK)
            except ArticleFavorite.DoesNotExist:
                return Response({'message': '未收藏过', 'is_favorited': False}, status=status.HTTP_200_OK)
