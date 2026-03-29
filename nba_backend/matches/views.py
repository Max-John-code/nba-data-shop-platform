from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from datetime import date
from .models import Match
from .serializers import MatchSerializer


class MatchListView(APIView):
    """比赛列表（所有用户可访问）"""
    
    def get(self, request):
        """获取比赛列表"""
        match_date = request.GET.get('date', None)
        
        if match_date:
            # 获取指定日期的比赛
            matches = Match.objects.filter(match_date=match_date)
        else:
            # 获取今天的比赛
            today = date.today()
            matches = Match.objects.filter(match_date=today)
        
        serializer = MatchSerializer(matches, many=True)
        
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'matches': serializer.data,
                'total': matches.count()
            }
        })


class MatchManageView(APIView):
    """比赛管理（仅管理员）"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取所有比赛（管理用）"""
        if request.user.role != 'admin':
            return Response({'code': 403, 'message': '无权限访问'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        matches = Match.objects.all()
        serializer = MatchSerializer(matches, many=True)
        
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'matches': serializer.data,
                'total': matches.count()
            }
        })
    
    def post(self, request):
        """添加比赛"""
        if request.user.role != 'admin':
            return Response({'code': 403, 'message': '无权限访问'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        serializer = MatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'code': 200,
                'message': '添加成功',
                'data': serializer.data
            })
        
        return Response({'code': 400, 'message': '参数错误', 'data': serializer.errors}, 
                      status=status.HTTP_400_BAD_REQUEST)


class MatchDetailView(APIView):
    """比赛详情/更新/删除（仅管理员）"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, match_id):
        """获取比赛详情"""
        try:
            match = Match.objects.get(id=match_id)
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': MatchSerializer(match).data
            })
        except Match.DoesNotExist:
            return Response({'code': 404, 'message': '比赛不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, match_id):
        """更新比赛信息"""
        if request.user.role != 'admin':
            return Response({'code': 403, 'message': '无权限访问'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        try:
            match = Match.objects.get(id=match_id)
            serializer = MatchSerializer(match, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'code': 200,
                    'message': '更新成功',
                    'data': serializer.data
                })
            
            return Response({'code': 400, 'message': '参数错误', 'data': serializer.errors}, 
                          status=status.HTTP_400_BAD_REQUEST)
        except Match.DoesNotExist:
            return Response({'code': 404, 'message': '比赛不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, match_id):
        """删除比赛"""
        if request.user.role != 'admin':
            return Response({'code': 403, 'message': '无权限访问'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        try:
            match = Match.objects.get(id=match_id)
            match.delete()
            return Response({
                'code': 200,
                'message': '删除成功'
            })
        except Match.DoesNotExist:
            return Response({'code': 404, 'message': '比赛不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)
