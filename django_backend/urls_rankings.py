# apps/rankings/urls.py
from django.urls import path
from . import apps_rankings_views as views

urlpatterns = [
    path('teams', views.get_team_rankings, name='team_rankings'),
    path('players', views.get_player_rankings, name='player_rankings'),
]
