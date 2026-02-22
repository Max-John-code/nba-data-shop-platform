from django.db import models
from accounts.models import User


class Article(models.Model):
    """文章模型"""
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    image = models.TextField(blank=True, null=True, verbose_name='图片(base64)')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    view_count = models.IntegerField(default=0, verbose_name='浏览次数')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'article'
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    """评论模型"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', verbose_name='文章')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='评论用户')
    content = models.TextField(verbose_name='评论内容')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'comment'
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['created_at']
    
    def __str__(self):
        return f'{self.user.username} 评论了 {self.article.title}'
