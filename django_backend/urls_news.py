# apps/news/urls.py
from django.urls import path
from . import apps_news_views as views

urlpatterns = [
    path('list', views.get_news_list, name='news_list'),
    path('<str:news_id>', views.get_news_detail, name='news_detail'),
    path('<str:news_id>/like', views.like_news, name='like_news'),
]
