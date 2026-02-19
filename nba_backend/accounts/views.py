from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
import random
from .models import User, SmsCode
from .serializers import SendSmsSerializer, LoginSerializer, RegisterSerializer, UserSerializer


class SendSmsView(APIView):
    """发送短信验证码"""
    
    def post(self, request):
        serializer = SendSmsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'code': 400, 'message': '参数错误', 'data': serializer.errors}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        phone = serializer.validated_data['phone']
        
        # 检查60秒内是否已发送
        one_minute_ago = timezone.now() - timedelta(seconds=60)
        recent_code = SmsCode.objects.filter(phone=phone, created_at__gte=one_minute_ago).first()
        if recent_code:
            return Response({'code': 400, 'message': '请60秒后再试'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # 生成4位验证码
        code = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        
        # 保存验证码
        SmsCode.objects.create(phone=phone, code=code)
        
        # 实际项目中这里应该调用短信服务商API发送短信
        # 开发环境直接返回验证码
        print(f'验证码: {code}')
        
        return Response({'code': 200, 'message': '验证码已发送', 'data': {'code': code}})


class LoginView(APIView):
    """登录"""
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'code': 400, 'message': '参数错误', 'data': serializer.errors}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        phone = serializer.validated_data['phone']
        sms_code = serializer.validated_data['sms_code']
        
        # 查找用户
        user = User.objects.filter(phone=phone).first()
        if not user:
            return Response({'code': 400, 'message': '用户不存在，请先注册'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # 管理员可以使用特殊验证码 9999
        if user.role == 'admin' and sms_code == '9999':
            # 生成token
            token, _ = Token.objects.get_or_create(user=user)
            
            return Response({
                'code': 200, 
                'message': '登录成功',
                'data': {
                    'token': token.key,
                    'user': UserSerializer(user).data
                }
            })
        
        # 验证验证码
        five_minutes_ago = timezone.now() - timedelta(minutes=5)
        code_obj = SmsCode.objects.filter(
            phone=phone, 
            code=sms_code, 
            is_used=False,
            created_at__gte=five_minutes_ago
        ).first()
        
        if not code_obj:
            return Response({'code': 400, 'message': '验证码错误或已过期'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # 标记验证码已使用
        code_obj.is_used = True
        code_obj.save()
        
        # 生成token
        token, _ = Token.objects.get_or_create(user=user)
        
        return Response({
            'code': 200, 
            'message': '登录成功',
            'data': {
                'token': token.key,
                'user': UserSerializer(user).data
            }
        })


class RegisterView(APIView):
    """注册"""
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'code': 400, 'message': '参数错误', 'data': serializer.errors}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        phone = serializer.validated_data['phone']
        sms_code = serializer.validated_data['sms_code']
        
        # 验证验证码
        five_minutes_ago = timezone.now() - timedelta(minutes=5)
        code_obj = SmsCode.objects.filter(
            phone=phone, 
            code=sms_code, 
            is_used=False,
            created_at__gte=five_minutes_ago
        ).first()
        
        if not code_obj:
            return Response({'code': 400, 'message': '验证码错误或已过期'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # 标记验证码已使用
        code_obj.is_used = True
        code_obj.save()
        
        # 创建用户
        user = User.objects.create(
            username=phone,
            phone=phone
        )
        
        # 生成token
        token = Token.objects.create(user=user)
        
        return Response({
            'code': 200, 
            'message': '注册成功',
            'data': {
                'token': token.key,
                'user': UserSerializer(user).data
            }
        })



class UserListView(APIView):
    """用户列表（仅管理员）"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # 验证是否为管理员
        if request.user.role != 'admin':
            return Response({'code': 403, 'message': '无权限访问'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        # 获取所有用户
        users = User.objects.all().order_by('-created_at')
        serializer = UserSerializer(users, many=True)
        
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'users': serializer.data,
                'total': users.count()
            }
        })


class UserDetailView(APIView):
    """用户详情/更新/删除（仅管理员）"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, user_id):
        # 验证是否为管理员
        if request.user.role != 'admin':
            return Response({'code': 403, 'message': '无权限访问'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        try:
            user = User.objects.get(id=user_id)
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': UserSerializer(user).data
            })
        except User.DoesNotExist:
            return Response({'code': 404, 'message': '用户不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, user_id):
        # 验证是否为管理员
        if request.user.role != 'admin':
            return Response({'code': 403, 'message': '无权限访问'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        try:
            user = User.objects.get(id=user_id)
            
            # 更新角色
            if 'role' in request.data:
                user.role = request.data['role']
                user.save()
            
            return Response({
                'code': 200,
                'message': '更新成功',
                'data': UserSerializer(user).data
            })
        except User.DoesNotExist:
            return Response({'code': 404, 'message': '用户不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, user_id):
        # 验证是否为管理员
        if request.user.role != 'admin':
            return Response({'code': 403, 'message': '无权限访问'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        try:
            user = User.objects.get(id=user_id)
            
            # 不能删除自己
            if user.id == request.user.id:
                return Response({'code': 400, 'message': '不能删除自己'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            user.delete()
            return Response({
                'code': 200,
                'message': '删除成功'
            })
        except User.DoesNotExist:
            return Response({'code': 404, 'message': '用户不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)



class ProfileView(APIView):
    """个人信息查看和更新"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取当前用户信息"""
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': UserSerializer(request.user).data
        })
    
    def put(self, request):
        """更新当前用户信息"""
        user = request.user
        
        # 更新用户名
        if 'username' in request.data:
            username = request.data['username'].strip()
            if username:
                # 检查用户名是否已被使用（排除自己）
                if User.objects.filter(username=username).exclude(id=user.id).exists():
                    return Response({'code': 400, 'message': '用户名已被使用'}, 
                                  status=status.HTTP_400_BAD_REQUEST)
                user.username = username
        
        # 更新头像
        if 'avatar' in request.data:
            user.avatar = request.data['avatar']
        
        user.save()
        
        return Response({
            'code': 200,
            'message': '更新成功',
            'data': UserSerializer(user).data
        })


class UploadAvatarView(APIView):
    """上传头像"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """上传头像（base64格式）"""
        avatar_data = request.data.get('avatar')
        
        if not avatar_data:
            return Response({'code': 400, 'message': '请上传头像'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # 检查base64数据大小（限制5MB）
            if len(avatar_data) > 5 * 1024 * 1024:
                return Response({'code': 400, 'message': '图片过大，请选择小于5MB的图片'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            # 保存base64字符串到数据库
            user = request.user
            user.avatar = avatar_data
            user.save()
            
            return Response({
                'code': 200,
                'message': '上传成功',
                'data': {
                    'avatar': user.avatar
                }
            })
        except Exception as e:
            return Response({'code': 500, 'message': f'上传失败: {str(e)}'}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)
