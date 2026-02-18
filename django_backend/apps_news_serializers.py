# apps/news/serializers.py
from rest_framework import serializers
from .models import News, NewsLike


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'image', 'source', 'comments', 'likes', 'shares', 'created_at']
        read_only_fields = ['id', 'created_at']


class NewsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'image', 'source', 'author', 'comments', 'likes', 'shares', 'created_at']
        read_only_fields = ['id', 'created_at']


class NewsLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsLike
        fields = ['id', 'user', 'news', 'created_at']
        read_only_fields = ['id', 'created_at']
