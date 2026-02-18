# apps/matches/models.py
from django.db import models
import uuid

class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='team_logos/')
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'teams'
        verbose_name = '球队'
        verbose_name_plural = '球队'

    def __str__(self):
        return self.name


class Match(models.Model):
    STATUS_CHOICES = [
        ('未开始', '未开始'),
        ('进行中', '进行中'),
        ('已结束', '已结束'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    team1_score = models.IntegerField(default=0)
    team2_score = models.IntegerField(default=0)
    match_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='未开始')
    viewers = models.CharField(max_length=20, default='0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'matches'
        verbose_name = '比赛'
        verbose_name_plural = '比赛'
        indexes = [
            models.Index(fields=['match_date']),
        ]

    def __str__(self):
        return f'{self.team1.name} vs {self.team2.name}'


class Player(models.Model):
    POSITION_CHOICES = [
        ('PG', '控卫'),
        ('SG', '得分后卫'),
        ('SF', '小前锋'),
        ('PF', '大前锋'),
        ('C', '中锋'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    position = models.CharField(max_length=2, choices=POSITION_CHOICES)
    height = models.CharField(max_length=10, null=True, blank=True)
    weight = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'players'
        verbose_name = '球员'
        verbose_name_plural = '球员'
        unique_together = ('team', 'number')

    def __str__(self):
        return self.name


class MatchStats(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='stats')
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    rebounds = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    steals = models.IntegerField(default=0)
    blocks = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'match_stats'
        verbose_name = '比赛统计'
        verbose_name_plural = '比赛统计'
        unique_together = ('match', 'player')

    def __str__(self):
        return f'{self.player.name} - {self.match}'
