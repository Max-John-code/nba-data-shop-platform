from django.urls import path
from .views import (
    ProductListView, ProductDetailView,
    CartView, OrderView, OrderDetailView, OrderPayView, OrderConfirmView,
    ProductManageView, OrderManageView
)

urlpatterns = [
    # 商品
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:product_id>/', ProductDetailView.as_view(), name='product-detail'),
    
    # 购物车
    path('cart/', CartView.as_view(), name='cart-list'),
    path('cart/<int:cart_id>/', CartView.as_view(), name='cart-update'),
    
    # 订单
    path('orders/', OrderView.as_view(), name='order-list'),
    path('orders/<int:order_id>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:order_id>/pay/', OrderPayView.as_view(), name='order-pay'),
    path('orders/<int:order_id>/confirm/', OrderConfirmView.as_view(), name='order-confirm'),
    
    # 管理员
    path('admin/products/', ProductManageView.as_view(), name='product-manage'),
    path('admin/products/<int:product_id>/', ProductManageView.as_view(), name='product-manage-detail'),
    path('admin/orders/', OrderManageView.as_view(), name='order-manage'),
    path('admin/orders/<int:order_id>/', OrderManageView.as_view(), name='order-manage-detail'),
]
