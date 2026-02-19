from django.urls import path
from .views import SendSmsView, LoginView, RegisterView

urlpatterns = [
    path('send-sms/', SendSmsView.as_view(), name='send_sms'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
]
