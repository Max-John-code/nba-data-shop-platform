from django.db import models


class Match(models.Model):
    """比赛模型"""
    # 主队信息
    home_team_name = models.CharField(max_length=100, verbose_name='主队中文名')
    home_team_logo = models.CharField(max_length=50, verbose_name='主队英文缩写')
    home_team_score = models.IntegerField(default=0, verbose_name='主队得分')
    
    # 客队信息
    away_team_name = models.CharField(max_length=100, verbose_name='客队中文名')
    away_team_logo = models.CharField(max_length=50, verbose_name='客队英文缩写')
    away_team_score = models.IntegerField(default=0, verbose_name='客队得分')
    
    # 比赛信息
    match_date = models.DateField(verbose_name='比赛日期')
    match_time = models.TimeField(null=True, blank=True, verbose_name='比赛时间')
    status = models.CharField(
        max_length=20,
        choices=[
            ('upcoming', '未开始'),
            ('live', '进行中'),
            ('finished', '已结束')
        ],
        default='upcoming',
        verbose_name='比赛状态'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'match'
        verbose_name = '比赛'
        verbose_name_plural = verbose_name
        ordering = ['-match_date', '-match_time']
    
    def __str__(self):
        return f'{self.home_team_name} vs {self.away_team_name} ({self.match_date})'
