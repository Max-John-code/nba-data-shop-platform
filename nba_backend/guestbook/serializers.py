from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    avatar = serializers.CharField(source='user.avatar', read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'user', 'username', 'avatar', 'content', 'created_at']
        read_only_fields = ['user', 'created_at']
