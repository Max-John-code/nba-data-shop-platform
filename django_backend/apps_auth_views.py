# apps/auth/views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta
import random
import string

from .models import User, SmsCode
from .serializers import UserSerializer
from utils.response import success_response, error_response
from utils.sms import send_sms

@api_view(['POST'])
@permission_classes([AllowAny])
def send_sms_code(request):
    """发送短信验证码"""
    phone = request.data.get('phone')
    
    if not phone or len(phone) != 11:
        return Response(error_response('请输入正确的11位手机号'), status=status.HTTP_400_BAD_REQUEST)
    
    # 检查频率限制
    recent_code = SmsCode.objects.filter(
        phone=phone,
        created_at__gte=timezone.now() - timedelta(minutes=1)
    ).first()
    
    if recent_code:
        return Response(error_response('请求过于频繁，请60秒后再试'), status=status.HTTP_400_BAD_REQUEST)
    
    # 生成4位验证码
    code = ''.join(random.choices(string.digits, k=4))
    
    # 保存验证码
    expires_at = timezone.now() + timedelta(minutes=5)
    SmsCode.objects.create(
        phone=phone,
        code=code,
        expires_at=expires_at
    )
    
    # 发送短信
    send_sms(phone, f'您的验证码是：{code}，5分钟内有效')
    
    return Response(success_response({
        'expiresIn': 300
    }), status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """用户登录"""
    phone = request.data.get('phone')
    sms_code = request.data.get('smsCode')
    
    if not phone or not sms_code:
        return Response(error_response('手机号和验证码不能为空'), status=status.HTTP_400_BAD_REQUEST)
    
    # 验证短信验证码
    sms = SmsCode.objects.filter(
        phone=phone,
        code=sms_code,
        is_used=False,
        expires_at__gte=timezone.now()
    ).first()
    
    if not sms:
        return Response(error_response('验证码错误或已过期'), status=status.HTTP_401_UNAUTHORIZED)
    
    # 标记验证码已使用
    sms.is_used = True
    sms.save()
    
    # 获取或创建用户
    user, created = User.objects.get_or_create(
        phone=phone,
        defaults={'username': phone}
    )
    
    # 生成token
    refresh = RefreshToken.for_user(user)
    
    return Response(success_response({
        'userId': str(user.id),
        'phone': user.phone,
        'token': str(refresh.access_token),
        'userName': user.username
    }), status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """用户注册"""
    phone = request.data.get('phone')
    sms_code = request.data.get('smsCode')
    password = request.data.get('password')
    confirm_password = request.data.get('confirmPassword')
    
    # 验证参数
    if not all([phone, sms_code, password, confirm_password]):
        return Response(error_response('参数不完整'), status=status.HTTP_400_BAD_REQUEST)
    
    if password != confirm_password:
        return Response(error_response('两次密码不一致'), status=status.HTTP_400_BAD_REQUEST)
    
    if len(password) < 6 or len(password) > 16:
        return Response(error_response('密码需要6-16位'), status=status.HTTP_400_BAD_REQUEST)
    
    # 验证短信验证码
    sms = SmsCode.objects.filter(
        phone=phone,
        code=sms_code,
        is_used=False,
        expires_at__gte=timezone.now()
    ).first()
    
    if not sms:
        return Response(error_response('验证码错误或已过期'), status=status.HTTP_401_UNAUTHORIZED)
    
    # 检查手机号是否已注册
    if User.objects.filter(phone=phone).exists():
        return Response(error_response('手机号已被注册'), status=status.HTTP_400_BAD_REQUEST)
    
    # 标记验证码已使用
    sms.is_used = True
    sms.save()
    
    # 创建用户
    user = User.objects.create_user(
        username=phone,
        phone=phone,
        password=password
    )
    
    # 生成token
    refresh = RefreshToken.for_user(user)
    
    return Response(success_response({
        'userId': str(user.id),
        'phone': user.phone,
        'token': str(refresh.access_token),
        'userName': user.username
    }), status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    """获取用户信息"""
    user = request.user
    serializer = UserSerializer(user)
    return Response(success_response(serializer.data), status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """更新用户信息"""
    user = request.user
    
    if 'userName' in request.data:
        user.username = request.data['userName']
    
    if 'avatar' in request.FILES:
        user.avatar = request.FILES['avatar']
    
    user.save()
    
    serializer = UserSerializer(user)
    return Response(success_response(serializer.data), status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """修改密码"""
    user = request.user
    old_password = request.data.get('oldPassword')
    new_password = request.data.get('newPassword')
    
    if not user.check_password(old_password):
        return Response(error_response('旧密码错误'), status=status.HTTP_400_BAD_REQUEST)
    
    if len(new_password) < 6 or len(new_password) > 16:
        return Response(error_response('密码需要6-16位'), status=status.HTTP_400_BAD_REQUEST)
    
    user.set_password(new_password)
    user.save()
    
    return Response(success_response({}), status=status.HTTP_200_OK)
