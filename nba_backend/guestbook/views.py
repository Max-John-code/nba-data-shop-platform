from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Message
from .serializers import MessageSerializer


class MessageListView(APIView):
    """留言列表（所有用户可访问）"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        """获取留言列表"""
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'messages': serializer.data,
                'total': messages.count()
            }
        })
    
    def post(self, request):
        """发表留言（需要登录）"""
        if not request.user.is_authenticated:
            return Response({'code': 401, 'message': '请先登录'}, 
                          status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                'code': 200,
                'message': '留言成功',
                'data': serializer.data
            })
        
        return Response({'code': 400, 'message': '参数错误', 'data': serializer.errors}, 
                      status=status.HTTP_400_BAD_REQUEST)


class MessageManageView(APIView):
    """留言管理（仅管理员）"""
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, message_id):
        """删除留言（仅管理员）"""
        if request.user.role != 'admin':
            return Response({'code': 403, 'message': '无权限访问'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        try:
            message = Message.objects.get(id=message_id)
            message.delete()
            return Response({
                'code': 200,
                'message': '删除成功'
            })
        except Message.DoesNotExist:
            return Response({'code': 404, 'message': '留言不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)
