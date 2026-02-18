# apps/auth/serializers.py
from rest_framework import serializers
from .models import User, SmsCode


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone', 'username', 'avatar', 'created_at']
        read_only_fields = ['id', 'created_at']


class SmsCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmsCode
        fields = ['phone', 'code', 'expires_at', 'is_used']
        read_only_fields = ['code', 'expires_at', 'is_used']
