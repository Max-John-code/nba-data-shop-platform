from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Player
from .serializers import PlayerSerializer


class PlayerListView(APIView):
    """球员列表（所有用户可访问）"""
    
    def get(self, request):
        """获取球员列表"""
        player_type = request.GET.get('type', None)
        
        if player_type:
            players = Player.objects.filter(player_type=player_type).order_by('ranking')
        else:
            players = Player.objects.all().order_by('ranking')
            
        serializer = PlayerSerializer(players, many=True)
        
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'players': serializer.data,
                'total': players.count()
            }
        })


class PlayerManageView(APIView):
    """球员管理（仅管理员）"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """添加球员"""
        if request.user.role != 'admin':
            return Response({'code': 403, 'message': '无权限访问'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        serializer = PlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'code': 200,
                'message': '添加成功',
                'data': serializer.data
            })
        
        return Response({'code': 400, 'message': '参数错误', 'data': serializer.errors}, 
                      status=status.HTTP_400_BAD_REQUEST)


class PlayerDetailView(APIView):
    """球员详情/更新/删除（仅管理员）"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, player_id):
        """获取球员详情"""
        try:
            player = Player.objects.get(id=player_id)
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': PlayerSerializer(player).data
            })
        except Player.DoesNotExist:
            return Response({'code': 404, 'message': '球员不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, player_id):
        """更新球员信息"""
        if request.user.role != 'admin':
            return Response({'code': 403, 'message': '无权限访问'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        try:
            player = Player.objects.get(id=player_id)
            serializer = PlayerSerializer(player, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'code': 200,
                    'message': '更新成功',
                    'data': serializer.data
                })
            
            return Response({'code': 400, 'message': '参数错误', 'data': serializer.errors}, 
                          status=status.HTTP_400_BAD_REQUEST)
        except Player.DoesNotExist:
            return Response({'code': 404, 'message': '球员不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, player_id):
        """删除球员"""
        if request.user.role != 'admin':
            return Response({'code': 403, 'message': '无权限访问'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        try:
            player = Player.objects.get(id=player_id)
            player.delete()
            return Response({
                'code': 200,
                'message': '删除成功'
            })
        except Player.DoesNotExist:
            return Response({'code': 404, 'message': '球员不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)
