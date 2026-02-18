# apps/search/views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

from apps.news.models import News
from apps.matches.models import Team
from apps.news.serializers import NewsSerializer
from apps.matches.serializers import TeamSerializer
from utils.response import success_response, error_response


class SearchPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'pageSize'
    max_page_size = 100


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_news(request):
    """搜索新闻"""
    keyword = request.query_params.get('keyword')
    
    if not keyword:
        return Response(error_response('keyword参数必填'), status=status.HTTP_400_BAD_REQUEST)
    
    news_list = News.objects.filter(
        Q(title__icontains=keyword) | Q(content__icontains=keyword)
    ).order_by('-created_at')
    
    paginator = SearchPagination()
    page = paginator.paginate_queryset(news_list, request)
    
    if page is not None:
        serializer = NewsSerializer(page, many=True)
        return Response(success_response({
            'total': paginator.page.paginator.count,
            'page': paginator.page.number,
            'pageSize': paginator.page_size,
            'results': serializer.data
        }), status=status.HTTP_200_OK)
    
    serializer = NewsSerializer(news_list, many=True)
    return Response(success_response({
        'total': news_list.count(),
        'page': 1,
        'pageSize': 10,
        'results': serializer.data
    }), status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_teams(request):
    """搜索球队"""
    keyword = request.query_params.get('keyword')
    
    if not keyword:
        return Response(error_response('keyword参数必填'), status=status.HTTP_400_BAD_REQUEST)
    
    teams = Team.objects.filter(
        Q(name__icontains=keyword) | Q(city__icontains=keyword)
    )
    
    serializer = TeamSerializer(teams, many=True)
    return Response(success_response({
        'results': serializer.data
    }), status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_players(request):
    """搜索球员"""
    keyword = request.query_params.get('keyword')
    
    if not keyword:
        return Response(error_response('keyword参数必填'), status=status.HTTP_400_BAD_REQUEST)
    
    # 这里需要从Player模型搜索，但当前还没有创建Player模型
    # 暂时返回空结果，后续可以扩展
    return Response(success_response({
        'results': []
    }), status=status.HTTP_200_OK)
