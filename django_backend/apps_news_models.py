# apps/news/models.py
from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class News(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/')
    source = models.CharField(max_length=100, default='虎扑篮球资讯')
    author = models.CharField(max_length=100, null=True, blank=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'news'
        verbose_name = '新闻'
        verbose_name_plural = '新闻'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.title


class NewsLike(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news_likes')
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='user_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'news_likes'
        verbose_name = '新闻点赞'
        verbose_name_plural = '新闻点赞'
        unique_together = ('user', 'news')

    def __str__(self):
        return f'{self.user.phone} liked {self.news.title}'


class NewsComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'news_comments'
        verbose_name = '新闻评论'
        verbose_name_plural = '新闻评论'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.phone} commented on {self.news.title}'
