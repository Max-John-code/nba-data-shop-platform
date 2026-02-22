# apps/auth/urls.py
from django.urls import path
from . import apps_auth_views as views

urlpatterns = [
    path('sendSmsCode', views.send_sms_code, name='send_sms_code'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
]
