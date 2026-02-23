from rest_framework import serializers
from .models import Highlight


class HighlightSerializer(serializers.ModelSerializer):
    video_full_url = serializers.SerializerMethodField()
    cover_full_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Highlight
        fields = ['id', 'title', 'description', 'video_url', 'cover_image', 
                  'video_full_url', 'cover_full_url', 'match_date', 'teams', 
                  'views', 'duration', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['views', 'created_at', 'updated_at']
    
    def get_video_full_url(self, obj):
        """返回视频的完整URL"""
        request = self.context.get('request')
        video_url = obj.get_video_url()
        if video_url and request and not video_url.startswith('http'):
            return request.build_absolute_uri(video_url)
        return video_url
    
    def get_cover_full_url(self, obj):
        """返回封面的完整URL"""
        request = self.context.get('request')
        cover_url = obj.get_cover_url()
        if cover_url and request and not cover_url.startswith('http'):
            return request.build_absolute_uri(cover_url)
        return cover_url
