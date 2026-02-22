from django.urls import path
from .views import MatchListView, MatchManageView, MatchDetailView

urlpatterns = [
    path('', MatchListView.as_view(), name='match-list'),
    path('manage/', MatchManageView.as_view(), name='match-manage'),
    path('<int:match_id>/', MatchDetailView.as_view(), name='match-detail'),
]
