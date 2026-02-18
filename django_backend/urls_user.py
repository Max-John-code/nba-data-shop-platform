# apps/user/urls.py
from django.urls import path
from . import apps_auth_views as views

urlpatterns = [
    path('profile', views.get_profile, name='get_profile'),
    path('profile', views.update_profile, name='update_profile'),
    path('changePassword', views.change_password, name='change_password'),
]
