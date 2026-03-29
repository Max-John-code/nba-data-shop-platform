from rest_framework.views import APIView
from rest_framework.response import Response
from players.models import Player
from players.serializers import PlayerSerializer
from forum.models import Article
from forum.serializers import ArticleSerializer
from shop.models import Product
from shop.serializers import ProductSerializer


class SearchView(APIView):
    """综合搜索API"""
    
    def get(self, request):
        """搜索球员、文章和商品"""
        keyword = request.query_params.get('keyword', '').strip()
        
        if not keyword:
            return Response({
                'code': 400,
                'message': '请输入搜索关键词'
            })
        
        # 搜索球员（名字包含关键词）
        players = Player.objects.filter(name__icontains=keyword)[:10]
        player_serializer = PlayerSerializer(players, many=True)
        
        # 搜索文章（标题或内容包含关键词）
        articles = Article.objects.filter(
            title__icontains=keyword
        ) | Article.objects.filter(
            content__icontains=keyword
        )
        articles = articles.distinct()[:10]
        article_serializer = ArticleSerializer(articles, many=True)
        
        # 搜索商品（名字、描述或关联球星包含关键词）
        products = Product.objects.filter(
            status='active'
        ).filter(
            name__icontains=keyword
        ) | Product.objects.filter(
            status='active'
        ).filter(
            description__icontains=keyword
        ) | Product.objects.filter(
            status='active'
        ).filter(
            player_name__icontains=keyword
        )
        products = products.distinct()[:10]
        product_serializer = ProductSerializer(products, many=True)
        
        return Response({
            'code': 200,
            'message': '搜索成功',
            'data': {
                'players': player_serializer.data,
                'articles': article_serializer.data,
                'products': product_serializer.data,
                'keyword': keyword
            }
        })
