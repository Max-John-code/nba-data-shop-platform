# apps/rankings/views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from datetime import datetime

from .models import TeamRanking, PlayerRanking
from .serializers import TeamRankingSerializer, PlayerRankingSerializer
from utils.response import success_response, error_response


class PlayerRankingPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'pageSize'
    max_page_size = 100


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_team_rankings(request):
    """获取球队排行榜"""
    season = request.query_params.get('season')
    
    if not season:
        current_year = datetime.now().year
        season = f'{current_year}-{current_year + 1}'
    
    rankings = TeamRanking.objects.filter(season=season).order_by('rank')
    
    serializer = TeamRankingSerializer(rankings, many=True)
    return Response(success_response({
        'season': season,
        'teams': serializer.data
    }), status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_player_rankings(request):
    """获取球员排行榜"""
    stat = request.query_params.get('stat')
    season = request.query_params.get('season')
    
    if not stat:
        return Response(error_response('stat参数必填'), status=status.HTTP_400_BAD_REQUEST)
    
    valid_stats = ['points', 'rebounds', 'assists', 'steals', 'blocks']
    if stat not in valid_stats:
        return Response(error_response(f'stat必须是以下之一: {", ".join(valid_stats)}'), status=status.HTTP_400_BAD_REQUEST)
    
    if not season:
        current_year = datetime.now().year
        season = f'{current_year}-{current_year + 1}'
    
    rankings = PlayerRanking.objects.filter(
        season=season,
        stat_type=stat
    ).order_by('rank')
    
    paginator = PlayerRankingPagination()
    page = paginator.paginate_queryset(rankings, request)
    
    if page is not None:
        serializer = PlayerRankingSerializer(page, many=True)
        return Response(success_response({
            'season': season,
            'stat': stat,
            'players': serializer.data
        }), status=status.HTTP_200_OK)
    
    serializer = PlayerRankingSerializer(rankings, many=True)
    return Response(success_response({
        'season': season,
        'stat': stat,
        'players': serializer.data
    }), status=status.HTTP_200_OK)
