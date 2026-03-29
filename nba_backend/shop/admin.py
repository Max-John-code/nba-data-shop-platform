from django.contrib import admin
from .models import Product, Cart, Order, OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'stock', 'category', 'player_name', 'sales', 'status']
    list_filter = ['category', 'status']
    search_fields = ['name', 'player_name']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_no', 'user', 'total_amount', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['order_no', 'user__username']
