from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone', 'created_at']
        read_only_fields = ['id', 'created_at']


class SendSmsSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11, min_length=11)
    
    def validate_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError('手机号格式不正确')
        return value


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11, min_length=11)
    sms_code = serializers.CharField(max_length=4, min_length=4)
    
    def validate_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError('手机号格式不正确')
        return value
    
    def validate_sms_code(self, value):
        if not value.isdigit():
            raise serializers.ValidationError('验证码格式不正确')
        return value


class RegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11, min_length=11)
    sms_code = serializers.CharField(max_length=4, min_length=4)
    
    def validate_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError('手机号格式不正确')
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError('该手机号已注册')
        return value
    
    def validate_sms_code(self, value):
        if not value.isdigit():
            raise serializers.ValidationError('验证码格式不正确')
        return value
