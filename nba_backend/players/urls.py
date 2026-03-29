from django.urls import path
from .views import PlayerListView, PlayerManageView, PlayerDetailView

urlpatterns = [
    path('', PlayerListView.as_view(), name='player_list'),
    path('manage/', PlayerManageView.as_view(), name='player_manage'),
    path('<int:player_id>/', PlayerDetailView.as_view(), name='player_detail'),
]
