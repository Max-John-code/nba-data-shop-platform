from django.urls import path
from .views import (
    StatsOverviewView,
    OrderStatusView,
    ProductSalesView,
    CategorySalesView,
    HighlightStatsView,
    ArticleStatsView
)

urlpatterns = [
    path('overview/', StatsOverviewView.as_view(), name='stats-overview'),
    path('orders/', OrderStatusView.as_view(), name='order-status'),
    path('products/', ProductSalesView.as_view(), name='product-sales'),
    path('categories/', CategorySalesView.as_view(), name='category-sales'),
    path('highlights/', HighlightStatsView.as_view(), name='highlight-stats'),
    path('articles/', ArticleStatsView.as_view(), name='article-stats'),
]
