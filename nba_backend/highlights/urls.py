from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HighlightViewSet

router = DefaultRouter()
router.register(r'', HighlightViewSet, basename='highlight')

urlpatterns = [
    path('', include(router.urls)),
]
