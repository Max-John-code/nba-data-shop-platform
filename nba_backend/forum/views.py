from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Article, Comment, ArticleLike, ArticleFavorite
from highlights.models import HighlightLike, HighlightFavorite
from .serializers import ArticleSerializer, ArticleDetailSerializer, CommentSerializer
from django.db.models import Count, Q
from collections import Counter


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



class RecommendedArticlesView(APIView):
    """基于协同过滤的文章推荐"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        """
        获取推荐文章（2篇）
        - 如果用户已登录：基于用户点赞/收藏的球队进行推荐
        - 如果用户未登录：返回最热门的文章
        """
        limit = int(request.GET.get('limit', 2))
        
        if request.user.is_authenticated:
            # 已登录用户：基于协同过滤推荐
            recommended_articles = self._get_personalized_recommendations(request.user, limit)
        else:
            # 未登录用户：返回热门文章
            recommended_articles = self._get_popular_articles(limit)
        
        serializer = ArticleSerializer(recommended_articles, many=True)
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'articles': serializer.data,
                'total': len(serializer.data)
            }
        })
    
    def _get_personalized_recommendations(self, user, limit):
        """基于用户行为的个性化推荐"""
        # 1. 获取用户点赞和收藏的文章球队
        liked_articles = ArticleLike.objects.filter(user=user).select_related('article')
        favorited_articles = ArticleFavorite.objects.filter(user=user).select_related('article')
        
        article_teams = []
        for like in liked_articles:
            if like.article.team:
                article_teams.append(like.article.team)
        for favorite in favorited_articles:
            if favorite.article.team:
                article_teams.append(favorite.article.team)
        
        print(f"用户 {user.username} 点赞/收藏的文章球队: {article_teams}")
        
        # 2. 获取用户点赞和收藏的视频球队
        liked_highlights = HighlightLike.objects.filter(user=user).select_related('highlight')
        favorited_highlights = HighlightFavorite.objects.filter(user=user).select_related('highlight')
        
        highlight_teams = []
        for like in liked_highlights:
            if like.highlight.teams:
                # 视频的teams格式是 "湖人 vs 勇士"，提取两个球队
                teams = like.highlight.teams.replace(' vs ', ' ').replace('vs', ' ').split()
                highlight_teams.extend(teams)
        for favorite in favorited_highlights:
            if favorite.highlight.teams:
                teams = favorite.highlight.teams.replace(' vs ', ' ').replace('vs', ' ').split()
                highlight_teams.extend(teams)
        
        print(f"用户 {user.username} 点赞/收藏的视频球队: {highlight_teams}")
        
        # 3. 合并所有球队，统计频率
        all_teams = article_teams + highlight_teams
        
        if not all_teams:
            # 如果用户没有任何点赞/收藏记录，返回热门文章
            print(f"用户 {user.username} 没有点赞/收藏记录，返回热门文章")
            return self._get_popular_articles(limit)
        
        # 统计球队出现频率
        team_counter = Counter(all_teams)
        # 获取最喜欢的球队（按频率排序）
        favorite_teams = [team for team, count in team_counter.most_common()]
        
        print(f"用户 {user.username} 最喜欢的球队排序: {favorite_teams}")
        
        # 4. 获取用户已经点赞/收藏过的文章ID（用于排除，避免重复推荐）
        interacted_article_ids = set()
        interacted_article_ids.update(liked_articles.values_list('article_id', flat=True))
        interacted_article_ids.update(favorited_articles.values_list('article_id', flat=True))
        
        print(f"用户 {user.username} 已互动的文章ID: {interacted_article_ids}")
        
        # 5. 根据喜欢的球队推荐文章（推荐同球队的其他文章）
        recommended_articles = []
        
        # 优先推荐最喜欢球队的文章
        for team in favorite_teams:
            if len(recommended_articles) >= limit:
                break
            
            # 推荐该球队的文章，排除已经互动过的
            team_articles = Article.objects.filter(
                team=team
            ).exclude(
                id__in=interacted_article_ids
            ).order_by('-created_at', '-view_count')[:limit - len(recommended_articles)]
            
            print(f"为球队 {team} 找到 {team_articles.count()} 篇文章")
            
            recommended_articles.extend(team_articles)
        
        # 6. 如果推荐的文章不够，用热门文章补充
        if len(recommended_articles) < limit:
            additional_articles = Article.objects.exclude(
                Q(id__in=interacted_article_ids) | 
                Q(id__in=[a.id for a in recommended_articles])
            ).order_by('-view_count', '-likes', '-created_at')[:limit - len(recommended_articles)]
            
            recommended_articles.extend(additional_articles)
        
        return recommended_articles[:limit]
    
    def _get_popular_articles(self, limit):
        """获取热门文章（未登录用户或无历史记录用户）"""
        return Article.objects.all().order_by('-view_count', '-likes', '-created_at')[:limit]
