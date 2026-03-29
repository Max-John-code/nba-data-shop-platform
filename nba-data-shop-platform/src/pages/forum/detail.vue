<template>
  <view class="container">
    <view class="article-detail">
      <view class="article-title">{{ article.title }}</view>
      
      <view class="article-meta">
        <text class="author">{{ article.author_name }}</text>
        <text class="date">{{ formatDate(article.created_at) }}</text>
        <text class="views">👁 {{ article.view_count }}</text>
      </view>
      
      <view class="article-content">{{ article.content }}</view>
      
      <image v-if="article.image" :src="article.image" mode="widthFix" class="article-image" />
    </view>

    <view class="comment-section">
      <view class="section-title">
        <text>评论 ({{ comments.length }})</text>
      </view>

      <view class="comment-input-box">
        <textarea 
          v-model="commentContent" 
          placeholder="写下你的评论..." 
          class="comment-input"
          :maxlength="500" />
        <view class="comment-btn" @click="submitComment">发表</view>
      </view>

      <view class="comment-list">
        <view v-for="comment in comments" :key="comment.id" class="comment-item">
          <view class="comment-avatar">
            <image v-if="comment.avatar" :src="comment.avatar" mode="aspectFill" />
            <view v-else class="avatar-placeholder">{{ comment.username.charAt(0) }}</view>
          </view>
          
          <view class="comment-content">
            <view class="comment-header">
              <text class="comment-username">{{ comment.username }}</text>
              <text class="comment-time">{{ formatCommentTime(comment.created_at) }}</text>
            </view>
            <view class="comment-text">{{ comment.content }}</view>
          </view>
        </view>
      </view>

      <view v-if="comments.length === 0" class="empty-comments">
        <text class="empty-icon">💬</text>
        <text class="empty-text">暂无评论，快来抢沙发吧~</text>
      </view>
    </view>
  </view>
</template>

<script>
import { getArticleDetail, postComment } from '@/api/forum'

export default {
  data() {
    return {
      articleId: null,
      article: {
        title: '',
        content: '',
        image: '',
        author_name: '',
        view_count: 0,
        created_at: ''
      },
      comments: [],
      commentContent: ''
    }
  },
  onLoad(options) {
    if (options.id) {
      this.articleId = options.id
      this.loadArticleDetail()
    }
  },
  methods: {
    loadArticleDetail() {
      uni.showLoading({ title: '加载中...' })
      
      getArticleDetail(this.articleId).then(res => {
        if (res.code === 200) {
          this.article = res.data
          this.comments = res.data.comments || []
        }
      }).catch(err => {
        console.error('加载文章详情失败', err)
        uni.showToast({ title: '加载失败', icon: 'none' })
      }).finally(() => {
        uni.hideLoading()
      })
    },
    submitComment() {
      // 检查是否登录
      const token = uni.getStorageSync('token')
      if (!token) {
        uni.showToast({ title: '请先登录', icon: 'none' })
        setTimeout(() => {
          uni.navigateTo({ url: '/pages/login/login' })
        }, 1500)
        return
      }

      if (!this.commentContent.trim()) {
        uni.showToast({ title: '请输入评论内容', icon: 'none' })
        return
      }

      uni.showLoading({ title: '发表中...' })
      
      postComment({
        article: this.articleId,
        content: this.commentContent
      }).then(res => {
        if (res.code === 200) {
          uni.showToast({ title: '评论成功', icon: 'success' })
          this.commentContent = ''
          // 重新加载文章详情以获取最新评论
          this.loadArticleDetail()
        }
      }).catch(err => {
        console.error('评论失败', err)
        uni.showToast({ title: '评论失败', icon: 'none' })
      }).finally(() => {
        uni.hideLoading()
      })
    },
    formatDate(dateStr) {
      const date = new Date(dateStr)
      const year = date.getFullYear()
      const month = date.getMonth() + 1
      const day = date.getDate()
      const hour = String(date.getHours()).padStart(2, '0')
      const minute = String(date.getMinutes()).padStart(2, '0')
      return `${year}-${month}-${day} ${hour}:${minute}`
    },
    formatCommentTime(dateStr) {
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

.article-detail {
  background-color: #fff;
  padding: 30rpx;
  margin-bottom: 20rpx;
}

.article-title {
  font-size: 38rpx;
  font-weight: bold;
  color: #333;
  line-height: 1.4;
  margin-bottom: 20rpx;
}

.article-meta {
  display: flex;
  gap: 20rpx;
  font-size: 24rpx;
  color: #999;
  margin-bottom: 30rpx;
  padding-bottom: 20rpx;
  border-bottom: 1rpx solid #f0f0f0;
}

.author {
  color: #667eea;
  font-weight: 500;
}

.article-content {
  font-size: 30rpx;
  color: #333;
  line-height: 1.8;
  margin-bottom: 30rpx;
  white-space: pre-wrap;
}

.article-image {
  width: 100%;
  border-radius: 8rpx;
}

.comment-section {
  background-color: #fff;
  padding: 30rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 25rpx;
}

.comment-input-box {
  display: flex;
  gap: 15rpx;
  margin-bottom: 30rpx;
}

.comment-input {
  flex: 1;
  min-height: 120rpx;
  padding: 20rpx;
  border: 1rpx solid #ddd;
  border-radius: 8rpx;
  font-size: 28rpx;
  background-color: #fafafa;
}

.comment-btn {
  width: 120rpx;
  height: 120rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border-radius: 8rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28rpx;
  font-weight: bold;
}

.comment-list {
  display: flex;
  flex-direction: column;
  gap: 25rpx;
}

.comment-item {
  display: flex;
  gap: 20rpx;
}

.comment-avatar {
  width: 80rpx;
  height: 80rpx;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
}

.comment-avatar image {
  width: 100%;
  height: 100%;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 36rpx;
  font-weight: bold;
  color: #fff;
}

.comment-content {
  flex: 1;
  min-width: 0;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10rpx;
}

.comment-username {
  font-size: 28rpx;
  font-weight: 500;
  color: #333;
}

.comment-time {
  font-size: 24rpx;
  color: #999;
}

.comment-text {
  font-size: 28rpx;
  color: #666;
  line-height: 1.6;
  word-wrap: break-word;
}

.empty-comments {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80rpx 0;
  gap: 15rpx;
}

.empty-icon {
  font-size: 100rpx;
  opacity: 0.3;
}

.empty-text {
  font-size: 26rpx;
  color: #999;
}
</style>
