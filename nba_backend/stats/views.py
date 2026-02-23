from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, Q
from accounts.models import User
from players.models import Player
from shop.models import Product, Order, OrderItem
from highlights.models import Highlight
from forum.models import Article


class IsAdminRole(IsAuthenticated):
    """检查用户是否为管理员角色"""
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == 'admin'


class StatsOverviewView(APIView):
    """统计概览"""
    permission_classes = [IsAdminRole]
    
    def get(self, request):
        # 用户总数
        total_users = User.objects.count()
        
        # 球星总数
        total_players = Player.objects.count()
        
        # 商品总数
        total_products = Product.objects.count()
        
        # 订单统计
        total_orders = Order.objects.count()
        total_revenue = Order.objects.filter(status='paid').aggregate(
            total=Sum('total_amount')
        )['total'] or 0
        
        # 总销量（已支付订单的商品数量总和）
        total_sales = OrderItem.objects.filter(
            order__status='paid'
        ).aggregate(total=Sum('quantity'))['total'] or 0
        
        # 精彩回放统计
        total_highlights = Highlight.objects.count()
        total_views = Highlight.objects.aggregate(total=Sum('views'))['total'] or 0
        
        # 论坛统计
        total_articles = Article.objects.count()
        
        return Response({
            'users': {
                'total': total_users
            },
            'players': {
                'total': total_players,
                'active': Player.objects.filter(player_type='star').count()
            },
            'products': {
                'total': total_products,
                'active': Product.objects.filter(status='active').count()
            },
            'orders': {
                'total': total_orders,
                'revenue': float(total_revenue)
            },
            'sales': {
                'total': total_sales
            },
            'highlights': {
                'total': total_highlights,
                'views': total_views
            },
            'articles': {
                'total': total_articles
            }
        })


class OrderStatusView(APIView):
    """订单状态分布统计"""
    permission_classes = [IsAdminRole]
    
    def get(self, request):
        status_names = {
            'pending': '待支付',
            'paid': '已支付',
            'shipped': '已发货',
            'completed': '已完成',
            'cancelled': '已取消'
        }
        
        data = []
        for status, name in status_names.items():
            count = Order.objects.filter(status=status).count()
            # 只有当数量大于0时才添加到结果中
            if count > 0:
                data.append({
                    'status': status,
                    'name': name,
                    'count': count
                })
        
        return Response(data)


class ProductSalesView(APIView):
    """商品销售统计"""
    permission_classes = [IsAdminRole]
    
    def get(self, request):
        # 获取销量前10的商品
        products = Product.objects.annotate(
            sales_count=Count('orderitem', filter=Q(orderitem__order__status='paid')),
            sales_amount=Sum('orderitem__quantity', filter=Q(orderitem__order__status='paid'))
        ).order_by('-sales_amount')[:10]
        
        data = []
        for product in products:
            data.append({
                'id': product.id,
                'name': product.name,
                'category': product.get_category_display(),
                'price': float(product.price),
                'sales_count': product.sales_count or 0,
                'sales_amount': product.sales_amount or 0,
                'revenue': float(product.price) * (product.sales_amount or 0)
            })
        
        return Response(data)


class CategorySalesView(APIView):
    """分类销售统计"""
    permission_classes = [IsAdminRole]
    
    def get(self, request):
        categories = ['jersey', 'shoes', 'cap', 'other']
        category_names = {
            'jersey': '球衣',
            'shoes': '球鞋',
            'cap': '帽子',
            'other': '其他'
        }
        
        data = []
        for category in categories:
            # 统计该分类的订单项数量和销售数量
            sales = OrderItem.objects.filter(
                product__category=category,
                order__status='paid'
            ).aggregate(
                count=Count('id'),
                amount=Sum('quantity')
            )
            
            # 只有当销售数量大于0时才添加到结果中
            if sales['amount'] and sales['amount'] > 0:
                # 计算该分类的总收入
                revenue = OrderItem.objects.filter(
                    product__category=category,
                    order__status='paid'
                ).aggregate(total=Sum('subtotal'))['total'] or 0
                
                data.append({
                    'category': category,
                    'name': category_names[category],
                    'sales_count': sales['count'] or 0,
                    'sales_amount': sales['amount'] or 0,
                    'revenue': float(revenue)
                })
        
        return Response(data)


class HighlightStatsView(APIView):
    """精彩回放观看统计"""
    permission_classes = [IsAdminRole]
    
    def get(self, request):
        # 获取观看量前10的精彩回放
        highlights = Highlight.objects.order_by('-views')[:10]
        
        data = []
        for highlight in highlights:
            data.append({
                'id': highlight.id,
                'title': highlight.title,
                'teams': highlight.teams,
                'views': highlight.views,
                'duration': highlight.duration,
                'match_date': highlight.match_date.strftime('%Y-%m-%d')
            })
        
        return Response(data)


class ArticleStatsView(APIView):
    """文章浏览量统计"""
    permission_classes = [IsAdminRole]
    
    def get(self, request):
        # 获取浏览量前10的文章
        articles = Article.objects.order_by('-view_count')[:10]
        
        data = []
        for article in articles:
            data.append({
                'id': article.id,
                'title': article.title,
                'author': article.author.username,
                'view_count': article.view_count,
                'created_at': article.created_at.strftime('%Y-%m-%d')
            })
        
        return Response(data)
