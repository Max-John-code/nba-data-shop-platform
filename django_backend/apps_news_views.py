# apps/news/views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import News, NewsLike
from .serializers import NewsSerializer, NewsDetailSerializer
from utils.response import success_response, error_response


class NewsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'pageSize'
    max_page_size = 100


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_news_list(request):
    """获取新闻列表"""
    sort = request.query_params.get('sort', 'hot')
    
    if sort == 'new':
        news_list = News.objects.all().order_by('-created_at')
    else:
        news_list = News.objects.all().order_by('-likes', '-created_at')
    
    paginator = NewsPagination()
    page = paginator.paginate_queryset(news_list, request)
    
    if page is not None:
        serializer = NewsSerializer(page, many=True)
        return Response(success_response({
            'total': paginator.page.paginator.count,
            'page': paginator.page.number,
            'pageSize': paginator.page_size,
            'newsList': serializer.data
        }), status=status.HTTP_200_OK)
    
    serializer = NewsSerializer(news_list, many=True)
    return Response(success_response({
        'total': news_list.count(),
        'page': 1,
        'pageSize': 10,
        'newsList': serializer.data
    }), status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_news_detail(request, news_id):
    """获取新闻详情"""
    try:
        news = News.objects.get(id=news_id)
        serializer = NewsDetailSerializer(news)
        return Response(success_response(serializer.data), status=status.HTTP_200_OK)
    except News.DoesNotExist:
        return Response(error_response('新闻不存在'), status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_news(request, news_id):
    """点赞新闻"""
    try:
        news = News.objects.get(id=news_id)
        
        like, created = NewsLike.objects.get_or_create(
            user=request.user,
            news=news
        )
        
        if created:
            news.likes += 1
            news.save()
        
        return Response(success_response({
            'likes': news.likes
        }), status=status.HTTP_200_OK)
    except News.DoesNotExist:
        return Response(error_response('新闻不存在'), status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unlike_news(request, news_id):
    """取消点赞新闻"""
    try:
        news = News.objects.get(id=news_id)
        
        like = NewsLike.objects.filter(
            user=request.user,
            news=news
        ).first()
        
        if like:
            like.delete()
            news.likes = max(0, news.likes - 1)
            news.save()
        
        return Response(success_response({
            'likes': news.likes
        }), status=status.HTTP_200_OK)
    except News.DoesNotExist:
        return Response(error_response('新闻不存在'), status=status.HTTP_404_NOT_FOUND)
