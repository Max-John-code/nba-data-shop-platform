from django.urls import path
from .views import ArticleListView, ArticleManageView, ArticleDetailView, CommentView

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='article-list'),
    path('articles/manage/', ArticleManageView.as_view(), name='article-manage'),
    path('articles/<int:article_id>/', ArticleDetailView.as_view(), name='article-detail'),
    path('comments/', CommentView.as_view(), name='comment-create'),
    path('comments/<int:comment_id>/', CommentView.as_view(), name='comment-delete'),
]
