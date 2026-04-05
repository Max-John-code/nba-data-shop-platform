from django.urls import path
from .views import ArticleListView, ArticleManageView, ArticleDetailView, CommentView, RecommendedArticlesView
from .like_views import ArticleLikeView, ArticleFavoriteView

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='article-list'),
    path('articles/recommended/', RecommendedArticlesView.as_view(), name='article-recommended'),
    path('articles/manage/', ArticleManageView.as_view(), name='article-manage'),
    path('articles/<int:article_id>/', ArticleDetailView.as_view(), name='article-detail'),
    path('articles/<int:pk>/like/', ArticleLikeView.as_view({'post': 'like', 'delete': 'unlike'}), name='article-like'),
    path('articles/<int:pk>/favorite/', ArticleFavoriteView.as_view({'post': 'favorite', 'delete': 'unfavorite'}), name='article-favorite'),
    path('articles/<int:pk>/status/', ArticleLikeView.as_view({'get': 'status'}), name='article-status'),
    path('comments/', CommentView.as_view(), name='comment-create'),
    path('comments/<int:comment_id>/', CommentView.as_view(), name='comment-delete'),
]
