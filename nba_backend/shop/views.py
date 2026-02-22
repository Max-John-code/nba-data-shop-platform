from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from datetime import datetime
from .models import Product, Cart, Order, OrderItem
from .serializers import ProductSerializer, CartItemSerializer, OrderSerializer


class ProductListView(APIView):
    """商品列表"""
    
    def get(self, request):
        """获取商品列表"""
        category = request.query_params.get('category')
        
        products = Product.objects.filter(status='active')
        if category:
            products = products.filter(category=category)
        
        serializer = ProductSerializer(products, many=True)
        
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'products': serializer.data,
                'total': products.count()
            }
        })


class ProductDetailView(APIView):
    """商品详情"""
    
    def get(self, request, product_id):
        """获取商品详情"""
        try:
            product = Product.objects.get(id=product_id)
            serializer = ProductSerializer(product)
            
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': serializer.data
            })
        except Product.DoesNotExist:
            return Response({'code': 404, 'message': '商品不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)


class CartView(APIView):
    """购物车"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取购物车列表"""
        carts = Cart.objects.filter(user=request.user)
        serializer = CartItemSerializer(carts, many=True)
        
        total = sum(item.product.price * item.quantity for item in carts)
        
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'items': serializer.data,
                'total': float(total)
            }
        })
    
    def post(self, request):
        """添加到购物车"""
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        
        try:
            product = Product.objects.get(id=product_id, status='active')
            
            # 检查库存
            if product.stock < quantity:
                return Response({'code': 400, 'message': '库存不足'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            # 检查是否已在购物车
            cart_item, created = Cart.objects.get_or_create(
                user=request.user,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            
            return Response({
                'code': 200,
                'message': '添加成功'
            })
        except Product.DoesNotExist:
            return Response({'code': 404, 'message': '商品不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, cart_id):
        """更新购物车商品数量"""
        quantity = request.data.get('quantity')
        
        try:
            cart_item = Cart.objects.get(id=cart_id, user=request.user)
            
            if quantity <= 0:
                cart_item.delete()
                return Response({'code': 200, 'message': '已删除'})
            
            if cart_item.product.stock < quantity:
                return Response({'code': 400, 'message': '库存不足'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            cart_item.quantity = quantity
            cart_item.save()
            
            return Response({'code': 200, 'message': '更新成功'})
        except Cart.DoesNotExist:
            return Response({'code': 404, 'message': '购物车项不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, cart_id):
        """删除购物车商品"""
        try:
            cart_item = Cart.objects.get(id=cart_id, user=request.user)
            cart_item.delete()
            
            return Response({'code': 200, 'message': '删除成功'})
        except Cart.DoesNotExist:
            return Response({'code': 404, 'message': '购物车项不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)


class OrderView(APIView):
    """订单"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取订单列表"""
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'orders': serializer.data,
                'total': orders.count()
            }
        })
    
    @transaction.atomic
    def post(self, request):
        """创建订单"""
        receiver_name = request.data.get('receiver_name')
        receiver_phone = request.data.get('receiver_phone')
        receiver_address = request.data.get('receiver_address')
        
        if not all([receiver_name, receiver_phone, receiver_address]):
            return Response({'code': 400, 'message': '收货信息不完整'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # 获取购物车商品
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response({'code': 400, 'message': '购物车为空'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # 检查库存
        for item in cart_items:
            if item.product.stock < item.quantity:
                return Response({'code': 400, 'message': f'{item.product.name}库存不足'}, 
                              status=status.HTTP_400_BAD_REQUEST)
        
        # 计算总金额
        total_amount = sum(item.product.price * item.quantity for item in cart_items)
        
        # 生成订单号
        order_no = f'ORD{datetime.now().strftime("%Y%m%d%H%M%S")}{request.user.id}'
        
        # 创建订单
        order = Order.objects.create(
            order_no=order_no,
            user=request.user,
            total_amount=total_amount,
            receiver_name=receiver_name,
            receiver_phone=receiver_phone,
            receiver_address=receiver_address
        )
        
        # 创建订单明细并扣减库存
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                product_image=item.product.image,
                price=item.product.price,
                quantity=item.quantity,
                subtotal=item.product.price * item.quantity
            )
            
            # 扣减库存，增加销量
            item.product.stock -= item.quantity
            item.product.sales += item.quantity
            item.product.save()
        
        # 清空购物车
        cart_items.delete()
        
        serializer = OrderSerializer(order)
        
        return Response({
            'code': 200,
            'message': '下单成功',
            'data': serializer.data
        })


class OrderDetailView(APIView):
    """订单详情"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, order_id):
        """获取订单详情"""
        try:
            order = Order.objects.get(id=order_id, user=request.user)
            serializer = OrderSerializer(order)
            
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': serializer.data
            })
        except Order.DoesNotExist:
            return Response({'code': 404, 'message': '订单不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)


class OrderPayView(APIView):
    """订单支付"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, order_id):
        """支付订单（模拟支付）"""
        try:
            order = Order.objects.get(id=order_id, user=request.user)
            
            if order.status != 'pending':
                return Response({'code': 400, 'message': '订单状态不正确'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            # 模拟支付成功，更新订单状态
            order.status = 'paid'
            order.save()
            
            return Response({
                'code': 200,
                'message': '支付成功'
            })
        except Order.DoesNotExist:
            return Response({'code': 404, 'message': '订单不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)


class OrderConfirmView(APIView):
    """确认收货"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, order_id):
        """确认收货"""
        try:
            order = Order.objects.get(id=order_id, user=request.user)
            
            if order.status != 'shipped':
                return Response({'code': 400, 'message': '订单状态不正确'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            # 确认收货，更新订单状态为已完成
            order.status = 'completed'
            order.save()
            
            return Response({
                'code': 200,
                'message': '确认收货成功'
            })
        except Order.DoesNotExist:
            return Response({'code': 404, 'message': '订单不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)


# 管理员API
class ProductManageView(APIView):
    """商品管理（管理员）"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取所有商品"""
        if request.user.role != 'admin':
            return Response({'code': 403, 'message': '无权限访问'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'products': serializer.data,
                'total': products.count()
            }
        })
    
    def post(self, request):
        """添加商品"""
        if request.user.role != 'admin':
            return Response({'code': 403, 'message': '无权限访问'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'code': 200,
                'message': '添加成功',
                'data': serializer.data
            })
        
        return Response({'code': 400, 'message': '参数错误', 'data': serializer.errors}, 
                      status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, product_id):
        """更新商品"""
        if request.user.role != 'admin':
            return Response({'code': 403, 'message': '无权限访问'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        try:
            product = Product.objects.get(id=product_id)
            serializer = ProductSerializer(product, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'code': 200,
                    'message': '更新成功',
                    'data': serializer.data
                })
            
            return Response({'code': 400, 'message': '参数错误', 'data': serializer.errors}, 
                          status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({'code': 404, 'message': '商品不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, product_id):
        """删除商品"""
        if request.user.role != 'admin':
            return Response({'code': 403, 'message': '无权限访问'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            
            return Response({'code': 200, 'message': '删除成功'})
        except Product.DoesNotExist:
            return Response({'code': 404, 'message': '商品不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)



class OrderManageView(APIView):
    """订单管理（管理员）"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取所有订单"""
        if request.user.role != 'admin':
            return Response({'code': 403, 'message': '无权限访问'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        orders = Order.objects.all().order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        
        # 统计数据
        stats = {
            'total': orders.count(),
            'pending': orders.filter(status='pending').count(),
            'paid': orders.filter(status='paid').count(),
            'shipped': orders.filter(status='shipped').count(),
            'completed': orders.filter(status='completed').count(),
            'cancelled': orders.filter(status='cancelled').count(),
        }
        
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'orders': serializer.data,
                'stats': stats
            }
        })
    
    def put(self, request, order_id):
        """更新订单状态"""
        if request.user.role != 'admin':
            return Response({'code': 403, 'message': '无权限访问'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        new_status = request.data.get('status')
        if new_status not in ['pending', 'paid', 'shipped', 'completed', 'cancelled']:
            return Response({'code': 400, 'message': '状态值不正确'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            order = Order.objects.get(id=order_id)
            order.status = new_status
            order.save()
            
            return Response({
                'code': 200,
                'message': '更新成功'
            })
        except Order.DoesNotExist:
            return Response({'code': 404, 'message': '订单不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)
