from django.db import models
from accounts.models import User


class Product(models.Model):
    """商品模型"""
    CATEGORY_CHOICES = [
        ('jersey', '球衣'),
        ('shoes', '球鞋'),
        ('cap', '帽子'),
        ('other', '其他')
    ]
    
    STATUS_CHOICES = [
        ('active', '上架'),
        ('inactive', '下架')
    ]
    
    name = models.CharField(max_length=200, verbose_name='商品名称')
    description = models.TextField(blank=True, null=True, verbose_name='商品描述')
    image = models.TextField(blank=True, null=True, verbose_name='商品图片')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    stock = models.IntegerField(default=0, verbose_name='库存')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name='分类')
    player_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='关联球星')
    sales = models.IntegerField(default=0, verbose_name='销量')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='状态')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'product'
        verbose_name = '商品'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class Cart(models.Model):
    """购物车模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='商品')
    quantity = models.IntegerField(default=1, verbose_name='数量')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'cart'
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return f'{self.user.username} - {self.product.name}'


class Order(models.Model):
    """订单模型"""
    STATUS_CHOICES = [
        ('pending', '待支付'),
        ('paid', '已支付'),
        ('shipped', '已发货'),
        ('completed', '已完成'),
        ('cancelled', '已取消')
    ]
    
    order_no = models.CharField(max_length=50, unique=True, verbose_name='订单号')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='总金额')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    receiver_name = models.CharField(max_length=100, verbose_name='收货人')
    receiver_phone = models.CharField(max_length=20, verbose_name='收货电话')
    receiver_address = models.TextField(verbose_name='收货地址')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'order'
        verbose_name = '订单'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
    
    def __str__(self):
        return self.order_no


class OrderItem(models.Model):
    """订单明细模型"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='订单')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='商品')
    product_name = models.CharField(max_length=200, verbose_name='商品名称')
    product_image = models.TextField(blank=True, null=True, verbose_name='商品图片')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    quantity = models.IntegerField(verbose_name='数量')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='小计')
    
    class Meta:
        db_table = 'order_item'
        verbose_name = '订单明细'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return f'{self.order.order_no} - {self.product_name}'
