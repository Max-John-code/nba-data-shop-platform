from rest_framework import serializers
from .models import Product, Cart, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    product_image = serializers.CharField(source='product.image', read_only=True)
    product_stock = serializers.IntegerField(source='product.stock', read_only=True)
    subtotal = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id', 'product', 'product_name', 'product_price', 'product_image', 
                  'product_stock', 'quantity', 'subtotal', 'created_at']
        read_only_fields = ['created_at']
    
    def get_subtotal(self, obj):
        return obj.product.price * obj.quantity


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'order_no', 'user', 'username', 'total_amount', 'status',
                  'receiver_name', 'receiver_phone', 'receiver_address', 
                  'items', 'created_at', 'updated_at']
        read_only_fields = ['order_no', 'user', 'created_at', 'updated_at']
