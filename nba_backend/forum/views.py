from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Article, Comment
from .serializers import ArticleSerializer, ArticleDetailSerializer, CommentSerializer


class ArticleListView(APIView):
    """文章列表（所有用户可访问）"""
    
    def get(self, request):
        """获取文章列表"""
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'articles': serializer.data,
                'total': articles.count()
            }
        })


class ArticleManageView(APIView):
    """文章管理（仅管理员）"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """发表文章"""
        if request.user.role != 'admin':
            return Response({'code': 403, 'message': '无权限访问'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        print('收到发表文章请求')
        print('请求数据keys:', request.data.keys())
        print('标题:', request.data.get('title', 'N/A'))
        print('内容长度:', len(request.data.get('content', '')))
        print('图片长度:', len(request.data.get('image', '')))
        
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(author=request.user)
                print('文章保存成功')
                return Response({
                    'code': 200,
                    'message': '发表成功',
                    'data': serializer.data
                })
            except Exception as e:
                print('保存文章时出错:', str(e))
                return Response({
                    'code': 500, 
                    'message': f'保存失败: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        print('序列化验证失败:', serializer.errors)
        return Response({'code': 400, 'message': '参数错误', 'data': serializer.errors}, 
                      status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailView(APIView):
    """文章详情"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request, article_id):
        """获取文章详情（包含评论）"""
        try:
            article = Article.objects.get(id=article_id)
            # 增加浏览次数
            article.view_count += 1
            article.save()
            
            serializer = ArticleDetailSerializer(article)
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': serializer.data
            })
        except Article.DoesNotExist:
            return Response({'code': 404, 'message': '文章不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, article_id):
        """更新文章（仅管理员）"""
        if not request.user.is_authenticated or request.user.role != 'admin':
            return Response({'code': 403, 'message': '无权限访问'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        try:
            article = Article.objects.get(id=article_id)
            serializer = ArticleSerializer(article, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'code': 200,
                    'message': '更新成功',
                    'data': serializer.data
                })
            
            return Response({'code': 400, 'message': '参数错误', 'data': serializer.errors}, 
                          status=status.HTTP_400_BAD_REQUEST)
        except Article.DoesNotExist:
            return Response({'code': 404, 'message': '文章不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, article_id):
        """删除文章（仅管理员）"""
        if not request.user.is_authenticated or request.user.role != 'admin':
            return Response({'code': 403, 'message': '无权限访问'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        try:
            article = Article.objects.get(id=article_id)
            article.delete()
            return Response({
                'code': 200,
                'message': '删除成功'
            })
        except Article.DoesNotExist:
            return Response({'code': 404, 'message': '文章不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)


class CommentView(APIView):
    """评论管理"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """发表评论"""
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                'code': 200,
                'message': '评论成功',
                'data': serializer.data
            })
        
        return Response({'code': 400, 'message': '参数错误', 'data': serializer.errors}, 
                      status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, comment_id):
        """删除评论（仅本人或管理员）"""
        try:
            comment = Comment.objects.get(id=comment_id)
            
            # 只有评论作者或管理员可以删除
            if comment.user != request.user and request.user.role != 'admin':
                return Response({'code': 403, 'message': '无权限删除'}, 
                              status=status.HTTP_403_FORBIDDEN)
            
            comment.delete()
            return Response({
                'code': 200,
                'message': '删除成功'
            })
        except Comment.DoesNotExist:
            return Response({'code': 404, 'message': '评论不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)
