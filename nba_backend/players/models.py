from django.db import models


class Player(models.Model):
    """球员模型"""
    TYPE_CHOICES = (
        ('ranking', '联盟榜单'),
        ('star', '现役球星'),
    )
    
    name = models.CharField(max_length=100, verbose_name='球员姓名')
    team = models.CharField(max_length=100, verbose_name='所属球队')
    position = models.CharField(max_length=50, verbose_name='位置')
    avatar = models.TextField(blank=True, null=True, verbose_name='头像')
    player_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='ranking', verbose_name='类型')
    ranking = models.IntegerField(default=0, verbose_name='排名')
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, verbose_name='评分(星级)')
    
    # 数据统计
    points_per_game = models.DecimalField(max_digits=5, decimal_places=1, default=0.0, verbose_name='场均得分')
    rebounds_per_game = models.DecimalField(max_digits=5, decimal_places=1, default=0.0, verbose_name='场均篮板')
    assists_per_game = models.DecimalField(max_digits=5, decimal_places=1, default=0.0, verbose_name='场均助攻')
    steals_per_game = models.DecimalField(max_digits=5, decimal_places=1, default=0.0, verbose_name='场均抢断')
    blocks_per_game = models.DecimalField(max_digits=5, decimal_places=1, default=0.0, verbose_name='场均盖帽')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'player'
        verbose_name = '球员'
        verbose_name_plural = verbose_name
        ordering = ['ranking']
    
    def __str__(self):
        return f'{self.name} - {self.team}'
