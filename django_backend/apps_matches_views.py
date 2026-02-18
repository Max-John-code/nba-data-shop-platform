# apps/matches/views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from datetime import datetime, timedelta

from .models import Match, Team
from .serializers import MatchSerializer, MatchDetailSerializer
from utils.response import success_response, error_response


class MatchPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'pageSize'
    max_page_size = 100


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_matches_list(request):
    """获取比赛列表"""
    date_str = request.query_params.get('date')
    
    try:
        if date_str:
            match_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            match_date = datetime.now().date()
        
        matches = Match.objects.filter(date=match_date).order_by('-created_at')
        
        paginator = MatchPagination()
        page = paginator.paginate_queryset(matches, request)
        
        if page is not None:
            serializer = MatchSerializer(page, many=True)
            return Response(success_response({
                'total': paginator.page.paginator.count,
                'page': paginator.page.number,
                'pageSize': paginator.page_size,
                'matches': serializer.data
            }), status=status.HTTP_200_OK)
        
        serializer = MatchSerializer(matches, many=True)
        return Response(success_response({
            'total': matches.count(),
            'page': 1,
            'pageSize': 10,
            'matches': serializer.data
        }), status=status.HTTP_200_OK)
        
    except ValueError:
        return Response(error_response('日期格式错误，请使用YYYY-MM-DD'), status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_match_detail(request, match_id):
    """获取比赛详情"""
    try:
        match = Match.objects.get(id=match_id)
        serializer = MatchDetailSerializer(match)
        return Response(success_response(serializer.data), status=status.HTTP_200_OK)
    except Match.DoesNotExist:
        return Response(error_response('比赛不存在'), status=status.HTTP_404_NOT_FOUND)
