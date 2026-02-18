# apps/matches/serializers.py
from rest_framework import serializers
from .models import Team, Match


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'logo', 'city']


class MatchSerializer(serializers.ModelSerializer):
    team1 = TeamSerializer(read_only=True)
    team2 = TeamSerializer(read_only=True)
    
    class Meta:
        model = Match
        fields = ['id', 'date', 'team1', 'team2', 'team1_score', 'team2_score', 'status', 'viewers', 'created_at']
        read_only_fields = ['id', 'created_at']


class MatchDetailSerializer(serializers.ModelSerializer):
    team1 = TeamSerializer(read_only=True)
    team2 = TeamSerializer(read_only=True)
    
    class Meta:
        model = Match
        fields = ['id', 'date', 'team1', 'team2', 'team1_score', 'team2_score', 'status', 'viewers', 'created_at']
