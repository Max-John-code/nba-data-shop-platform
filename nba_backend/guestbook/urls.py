from django.urls import path
from .views import MessageListView, MessageManageView

urlpatterns = [
    path('', MessageListView.as_view(), name='message-list'),
    path('<int:message_id>/', MessageManageView.as_view(), name='message-delete'),
]
