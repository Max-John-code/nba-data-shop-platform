from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
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
        
        # 查找用户
        user = User.objects.filter(phone=phone).first()
        if not user:
            return Response({'code': 400, 'message': '用户不存在，请先注册'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
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
