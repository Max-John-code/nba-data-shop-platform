from rest_framework import serializers
from .models import Article, Comment


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    avatar = serializers.CharField(source='user.avatar', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'article', 'user', 'username', 'avatar', 'content', 'created_at']
        read_only_fields = ['user', 'created_at']


class ArticleSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    comment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'image', 'author', 'author_name', 
                  'view_count', 'comment_count', 'created_at', 'updated_at']
        read_only_fields = ['author', 'view_count', 'created_at', 'updated_at']
    
    def get_comment_count(self, obj):
        return obj.comments.count()


class ArticleDetailSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'image', 'author', 'author_name', 
                  'view_count', 'comment_count', 'comments', 'created_at', 'updated_at']
        read_only_fields = ['author', 'view_count', 'created_at', 'updated_at']
    
    def get_comment_count(self, obj):
        return obj.comments.count()
