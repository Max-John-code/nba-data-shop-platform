# nba_api/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('django_backend.urls_auth')),
    path('api/matches/', include('django_backend.urls_matches')),
    path('api/news/', include('django_backend.urls_news')),
    path('api/rankings/', include('django_backend.urls_rankings')),
    path('api/search/', include('django_backend.urls_search')),
    path('api/user/', include('django_backend.urls_user')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
