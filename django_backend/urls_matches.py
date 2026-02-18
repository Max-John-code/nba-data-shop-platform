# apps/matches/urls.py
from django.urls import path
from . import apps_matches_views as views

urlpatterns = [
    path('list', views.get_matches_list, name='matches_list'),
    path('<str:match_id>', views.get_match_detail, name='match_detail'),
]
