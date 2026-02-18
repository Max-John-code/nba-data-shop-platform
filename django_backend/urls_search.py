# apps/search/urls.py
from django.urls import path
from . import apps_search_views as views

urlpatterns = [
    path('news', views.search_news, name='search_news'),
    path('teams', views.search_teams, name='search_teams'),
    path('players', views.search_players, name='search_players'),
]
