from django.db import models
from accounts.models import User


class Message(models.Model):
    """留言模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='留言用户')
    content = models.TextField(verbose_name='留言内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'message'
        verbose_name = '留言'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.username} 的留言'
