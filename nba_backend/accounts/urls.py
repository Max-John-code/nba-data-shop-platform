from django.urls import path
from .views import (
    SendSmsView, LoginView, RegisterView, 
    UserListView, UserDetailView,
    ProfileView, UploadAvatarView
)
from .favorite_views import UserFavoriteView

urlpatterns = [
    path('send-sms/', SendSmsView.as_view(), name='send_sms'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<int:user_id>/', UserDetailView.as_view(), name='user_detail'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('upload-avatar/', UploadAvatarView.as_view(), name='upload_avatar'),
    # 用户收藏和点赞列表
    path('favorites/highlights/', UserFavoriteView.as_view({'get': 'favorited_highlights'}), name='user-favorited-highlights'),
    path('favorites/articles/', UserFavoriteView.as_view({'get': 'favorited_articles'}), name='user-favorited-articles'),
    path('likes/highlights/', UserFavoriteView.as_view({'get': 'liked_highlights'}), name='user-liked-highlights'),
    path('likes/articles/', UserFavoriteView.as_view({'get': 'liked_articles'}), name='user-liked-articles'),
]
