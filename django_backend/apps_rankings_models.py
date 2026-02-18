# apps/rankings/models.py
from django.db import models
import uuid

class TeamRanking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team_id = models.CharField(max_length=100)
    team_name = models.CharField(max_length=100)
    league = models.CharField(max_length=10)
    season = models.CharField(max_length=20)
    rank = models.IntegerField()
    wins = models.IntegerField()
    losses = models.IntegerField()
    win_rate = models.CharField(max_length=10)
    points_for = models.FloatField()
    points_against = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'team_rankings'
        verbose_name = '球队排名'
        verbose_name_plural = '球队排名'
        unique_together = ('team_id', 'league', 'season')
        indexes = [
            models.Index(fields=['league', 'season', 'rank']),
        ]

    def __str__(self):
        return f'{self.team_name} - {self.rank}'


class PlayerRanking(models.Model):
    STAT_CHOICES = [
        ('points', '得分'),
        ('rebounds', '篮板'),
        ('assists', '助攻'),
        ('steals', '抢断'),
        ('blocks', '盖帽'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    player_id = models.CharField(max_length=100)
    player_name = models.CharField(max_length=100)
    team_name = models.CharField(max_length=100)
    league = models.CharField(max_length=10)
    season = models.CharField(max_length=20)
    stat_type = models.CharField(max_length=20, choices=STAT_CHOICES)
    rank = models.IntegerField()
    value = models.FloatField()
    games = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'player_rankings'
        verbose_name = '球员排名'
        verbose_name_plural = '球员排名'
        unique_together = ('player_id', 'league', 'season', 'stat_type')
        indexes = [
            models.Index(fields=['league', 'season', 'stat_type', 'rank']),
        ]

    def __str__(self):
        return f'{self.player_name} - {self.stat_type}'
