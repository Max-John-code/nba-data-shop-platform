# apps/rankings/serializers.py
from rest_framework import serializers
from .models import TeamRanking, PlayerRanking


class TeamRankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamRanking
        fields = ['rank', 'team_id', 'team_name', 'wins', 'losses', 'win_rate', 'points_for', 'points_against', 'season']
        read_only_fields = ['rank', 'season']


class PlayerRankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerRanking
        fields = ['rank', 'player_id', 'player_name', 'team_name', 'value', 'games', 'stat_type', 'season']
        read_only_fields = ['rank', 'season']
