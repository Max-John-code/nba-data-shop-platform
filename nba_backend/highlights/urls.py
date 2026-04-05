from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HighlightViewSet, HighlightLikeView, HighlightFavoriteView

router = DefaultRouter()
router.register(r'', HighlightViewSet, basename='highlight')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/like/', HighlightLikeView.as_view({'post': 'like', 'delete': 'unlike'}), name='highlight-like'),
    path('<int:pk>/favorite/', HighlightFavoriteView.as_view({'post': 'favorite', 'delete': 'unfavorite'}), name='highlight-favorite'),
    path('<int:pk>/status/', HighlightLikeView.as_view({'get': 'status'}), name='highlight-status'),
]
