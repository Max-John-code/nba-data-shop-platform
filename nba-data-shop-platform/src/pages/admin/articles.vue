<template>
  <view class="container">
    <view class="header">
      <view class="title">交流论坛管理</view>
      <view class="actions">
        <view class="add-btn" @click="showAddArticle">发表文章</view>
        <view class="back-btn" @click="goBack">返回</view>
      </view>
    </view>

    <view class="article-list">
      <view v-for="article in articles" :key="article.id" class="article-item">
        <view class="article-title">{{ article.title }}</view>
        <view class="article-info">
          <text>作者: {{ article.author_name }}</text>
          <text>浏览: {{ article.view_count }}</text>
          <text>评论: {{ article.comment_count }}</text>
          <text>{{ formatDate(article.created_at) }}</text>
        </view>
        <view class="article-content">{{ article.content.substring(0, 100) }}...</view>
        <view class="article-actions">
          <view class="action-btn edit" @click="editArticle(article)">编辑</view>
          <view class="action-btn delete" @click="deleteArticleConfirm(article)">删除</view>
        </view>
      </view>
    </view>

    <view v-if="articles.length === 0" class="empty">暂无文章</view>
  </view>
</template>

<script>
import { getArticleList, deleteArticle } from '@/api/forum'

export default {
  data() {
    return {
      articles: []
    }
  },
  onLoad() {
    this.loadArticles()
  },
  methods: {
    loadArticles() {
      uni.showLoading({ title: '加载中...' })
      
      getArticleList().then(res => {
        if (res.code === 200) {
          this.articles = res.data.articles
        }
      }).catch(err => {
        console.error('加载文章列表失败', err)
      }).finally(() => {
        uni.hideLoading()
      })
    },
    showAddArticle() {
      uni.navigateTo({ url: '/pages/admin/article-form' })
    },
    editArticle(article) {
      uni.navigateTo({ url: `/pages/admin/article-form?id=${article.id}` })
    },
    deleteArticleConfirm(article) {
      uni.showModal({
        title: '确认删除',
        content: `确定要删除文章《${article.title}》吗？`,
        confirmColor: '#e74c3c',
        success: (res) => {
          if (res.confirm) {
            this.deleteArticleAction(article.id)
          }
        }
      })
    },
    deleteArticleAction(articleId) {
      uni.showLoading({ title: '删除中...' })
      
      deleteArticle(articleId).then(res => {
        if (res.code === 200) {
          uni.showToast({ title: '删除成功', icon: 'success' })
          this.loadArticles()
        }
      }).catch(err => {
        console.error('删除失败', err)
      }).finally(() => {
        uni.hideLoading()
      })
    },
    formatDate(dateStr) {
      const date = new Date(dateStr)
      const month = date.getMonth() + 1
      const day = date.getDate()
      return `${month}月${day}日`
    },
    goBack() {
      uni.navigateBack()
    }
  }
}
</script>

<style scoped>
.container {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding-bottom: 20rpx;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 30rpx;
  background-color: #fff;
  border-bottom: 1rpx solid #eee;
}

.title {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
}

.actions {
  display: flex;
  gap: 15rpx;
}

.add-btn {
  background-color: #e74c3c;
  color: #fff;
  padding: 10rpx 25rpx;
  border-radius: 6rpx;
  font-size: 26rpx;
}

.back-btn {
  color: #666;
  font-size: 28rpx;
}

.article-list {
  padding: 20rpx;
}

.article-item {
  background-color: #fff;
  border-radius: 12rpx;
  padding: 25rpx;
  margin-bottom: 20rpx;
}

.article-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 15rpx;
}

.article-info {
  display: flex;
  gap: 20rpx;
  font-size: 24rpx;
  color: #999;
  margin-bottom: 15rpx;
}

.article-content {
  font-size: 28rpx;
  color: #666;
  line-height: 1.6;
  margin-bottom: 15rpx;
}

.article-actions {
  display: flex;
  justify-content: flex-end;
  gap: 15rpx;
}

.action-btn {
  padding: 8rpx 25rpx;
  border-radius: 6rpx;
  font-size: 24rpx;
  color: #fff;
  text-align: center;
}

.edit {
  background-color: #3498db;
}

.delete {
  background-color: #e74c3c;
}

.empty {
  text-align: center;
  padding: 100rpx 0;
  color: #999;
  font-size: 28rpx;
}
</style>
