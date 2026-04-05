from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from highlights.models import Highlight, HighlightLike, HighlightFavorite
from highlights.serializers import HighlightSerializer
from forum.models import Article, ArticleLike, ArticleFavorite
from forum.serializers import ArticleSerializer


class UserFavoriteView(viewsets.ViewSet):
    """用户收藏和点赞列表视图"""
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def liked_highlights(self, request):
        """我点赞的视频列表"""
        liked_ids = HighlightLike.objects.filter(user=request.user).values_list('highlight_id', flat=True)
        highlights = Highlight.objects.filter(id__in=liked_ids, is_active=True)
        serializer = HighlightSerializer(highlights, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def favorited_highlights(self, request):
        """我收藏的视频列表"""
        favorited_ids = HighlightFavorite.objects.filter(user=request.user).values_list('highlight_id', flat=True)
        highlights = Highlight.objects.filter(id__in=favorited_ids, is_active=True)
        serializer = HighlightSerializer(highlights, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def liked_articles(self, request):
        """我点赞的文章列表"""
        liked_ids = ArticleLike.objects.filter(user=request.user).values_list('article_id', flat=True)
        articles = Article.objects.filter(id__in=liked_ids)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def favorited_articles(self, request):
        """我收藏的文章列表"""
        favorited_ids = ArticleFavorite.objects.filter(user=request.user).values_list('article_id', flat=True)
        articles = Article.objects.filter(id__in=favorited_ids)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
