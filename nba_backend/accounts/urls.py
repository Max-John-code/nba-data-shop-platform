from django.urls import path
from .views import (
    SendSmsView, LoginView, RegisterView, 
    UserListView, UserDetailView,
    ProfileView, UploadAvatarView
)

urlpatterns = [
    path('send-sms/', SendSmsView.as_view(), name='send_sms'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<int:user_id>/', UserDetailView.as_view(), name='user_detail'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('upload-avatar/', UploadAvatarView.as_view(), name='upload_avatar'),
]
