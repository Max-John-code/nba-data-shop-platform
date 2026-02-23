from django.db import models
from django.conf import settings


class Highlight(models.Model):
    """精彩回放模型 - 使用本地文件存储"""
    title = models.CharField(max_length=200, verbose_name='标题')
    description = models.TextField(blank=True, default='', verbose_name='描述')
    video_url = models.CharField(max_length=500, verbose_name='视频文件路径')
    cover_image = models.CharField(max_length=500, blank=True, default='', verbose_name='封面图片路径')
    match_date = models.DateField(verbose_name='比赛日期')
    teams = models.CharField(max_length=100, verbose_name='对阵球队')
    views = models.IntegerField(default=0, verbose_name='观看次数')
    duration = models.IntegerField(default=0, verbose_name='时长(秒)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')

    class Meta:
        db_table = 'highlight'
        verbose_name = '精彩回放'
        verbose_name_plural = '精彩回放'
        ordering = ['-match_date', '-created_at']

    def __str__(self):
        return self.title
    
    def get_video_url(self):
        """返回视频的完整URL"""
        if self.video_url:
            # 如果是相对路径，添加 MEDIA_URL 前缀
            if not self.video_url.startswith('http'):
                return f"{settings.MEDIA_URL}{self.video_url}"
            return self.video_url
        return ''
    
    def get_cover_url(self):
        """返回封面的完整URL"""
        if self.cover_image:
            # 如果是相对路径，添加 MEDIA_URL 前缀
            if not self.cover_image.startswith('http'):
                return f"{settings.MEDIA_URL}{self.cover_image}"
            return self.cover_image
        return ''
