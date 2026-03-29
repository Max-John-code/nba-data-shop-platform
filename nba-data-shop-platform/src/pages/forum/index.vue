<template>
  <view class="container">
    <view class="header">
      <view class="title">交流论坛</view>
      <view class="subtitle">NBA Community Forum</view>
    </view>

    <view class="article-list">
      <view v-for="article in articles" :key="article.id" class="article-card" @click="goToDetail(article.id)">
        <view class="article-header">
          <view class="article-title">{{ article.title }}</view>
          <view class="article-meta">
            <text class="author">{{ article.author_name }}</text>
            <text class="date">{{ formatDate(article.created_at) }}</text>
          </view>
        </view>
        
        <view class="article-content">{{ article.content.substring(0, 120) }}...</view>
        
        <image v-if="article.image" :src="article.image" mode="aspectFill" class="article-image" />
        
        <view class="article-footer">
          <view class="stat-item">
            <text class="icon">👁</text>
            <text>{{ article.view_count }}</text>
          </view>
          <view class="stat-item">
            <text class="icon">💬</text>
            <text>{{ article.comment_count }}</text>
          </view>
        </view>
      </view>
    </view>

    <view v-if="articles.length === 0" class="empty">
      <text class="empty-icon">📝</text>
      <text class="empty-text">暂无文章</text>
    </view>
  </view>
</template>

<script>
import { getArticleList } from '@/api/forum'

export default {
  data() {
    return {
      articles: []
    }
  },
  onLoad() {
    this.loadArticles()
  },
  onShow() {
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
        uni.showToast({ title: '加载失败', icon: 'none' })
      }).finally(() => {
        uni.hideLoading()
      })
    },
    goToDetail(articleId) {
      uni.navigateTo({
        url: `/pages/forum/detail?id=${articleId}`
      })
    },
    formatDate(dateStr) {
      const date = new Date(dateStr)
      const now = new Date()
      const diff = now - date
      const minutes = Math.floor(diff / 60000)
      const hours = Math.floor(diff / 3600000)
      const days = Math.floor(diff / 86400000)
      
      if (minutes < 1) return '刚刚'
      if (minutes < 60) return `${minutes}分钟前`
      if (hours < 24) return `${hours}小时前`
      if (days < 7) return `${days}天前`
      
      const month = date.getMonth() + 1
      const day = date.getDate()
      return `${month}月${day}日`
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
  padding: 60rpx 30rpx 40rpx;
  text-align: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.title {
  font-size: 48rpx;
  font-weight: bold;
  color: #fff;
  margin-bottom: 10rpx;
}

.subtitle {
  font-size: 24rpx;
  color: rgba(255, 255, 255, 0.8);
  letter-spacing: 2rpx;
}

.article-list {
  padding: 20rpx;
}

.article-card {
  background-color: #fff;
  border-radius: 12rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.1);
}

.article-header {
  margin-bottom: 20rpx;
}

.article-title {
  font-size: 34rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 15rpx;
  line-height: 1.4;
}

.article-meta {
  display: flex;
  gap: 20rpx;
  font-size: 24rpx;
  color: #999;
}

.author {
  color: #667eea;
  font-weight: 500;
}

.article-content {
  font-size: 28rpx;
  color: #666;
  line-height: 1.6;
  margin-bottom: 20rpx;
}

.article-image {
  width: 100%;
  height: 300rpx;
  border-radius: 8rpx;
  margin-bottom: 20rpx;
}

.article-footer {
  display: flex;
  gap: 30rpx;
  padding-top: 20rpx;
  border-top: 1rpx solid #f0f0f0;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 8rpx;
  font-size: 24rpx;
  color: #999;
}

.icon {
  font-size: 28rpx;
}

.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 150rpx 0;
  gap: 20rpx;
}

.empty-icon {
  font-size: 120rpx;
  opacity: 0.3;
}

.empty-text {
  font-size: 28rpx;
  color: #999;
}
</style>
