from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', '普通用户'),
        ('admin', '管理员'),
    )
    
    phone = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user', verbose_name='角色')
    avatar = models.TextField(blank=True, null=True, verbose_name='头像')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.phone


class SmsCode(models.Model):
    phone = models.CharField(max_length=11, verbose_name='手机号')
    code = models.CharField(max_length=6, verbose_name='验证码')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    is_used = models.BooleanField(default=False, verbose_name='是否已使用')
    
    class Meta:
        db_table = 'sms_code'
        verbose_name = '短信验证码'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return f'{self.phone} - {self.code}'
