<template>
  <view class="container">
    <view class="header">
      <view class="title">留言板</view>
      <view class="subtitle">分享你的想法</view>
    </view>

    <!-- 发表留言区域 -->
    <view class="post-section" v-if="isLogin">
      <view class="post-header">
        <image v-if="userInfo.avatar" :src="userInfo.avatar" class="user-avatar" mode="aspectFill" />
        <view v-else class="user-avatar-placeholder">{{ userInfo.username?.charAt(0) || '?' }}</view>
        <view class="post-title">发表留言</view>
      </view>
      <textarea 
        v-model="newMessage" 
        placeholder="说点什么吧..." 
        class="message-input"
        :maxlength="500" />
      <view class="post-footer">
        <view class="char-count">{{ newMessage.length }}/500</view>
        <view class="post-btn" @click="submitMessage">发表</view>
      </view>
    </view>

    <view class="login-tip" v-else @click="goToLogin">
      <text>登录后即可发表留言</text>
    </view>

    <!-- 留言列表 -->
    <view class="message-list">
      <view class="list-header">
        <text class="list-title">全部留言</text>
        <text class="list-count">{{ total }}条</text>
      </view>

      <view class="message-item" v-for="msg in messages" :key="msg.id">
        <view class="message-user">
          <image v-if="msg.avatar" :src="msg.avatar" class="avatar" mode="aspectFill" />
          <view v-else class="avatar-placeholder">{{ msg.username.charAt(0) }}</view>
          <view class="user-info">
            <view class="username">{{ msg.username }}</view>
            <view class="time">{{ formatTime(msg.created_at) }}</view>
          </view>
        </view>
        <view class="message-content">{{ msg.content }}</view>
      </view>

      <view class="empty" v-if="messages.length === 0">
        <text class="empty-icon">💬</text>
        <text class="empty-text">还没有留言，快来抢沙发吧~</text>
      </view>
    </view>
  </view>
</template>

<script>
import { getMessageList, postMessage } from '@/api/message'

export default {
  data() {
    return {
      isLogin: false,
      userInfo: {},
      newMessage: '',
      messages: [],
      total: 0
    }
  },
  onLoad() {
    this.checkLogin()
    this.loadMessages()
  },
  onShow() {
    this.checkLogin()
  },
  methods: {
    checkLogin() {
      const token = uni.getStorageSync('token')
      const userInfo = uni.getStorageSync('userInfo')
      this.isLogin = !!token
      this.userInfo = userInfo || {}
    },
    loadMessages() {
      getMessageList().then(res => {
        if (res.code === 200) {
          this.messages = res.data.messages
          this.total = res.data.total
        }
      }).catch(err => {
        console.error('加载留言失败', err)
      })
    },
    submitMessage() {
      if (!this.newMessage.trim()) {
        uni.showToast({ title: '请输入留言内容', icon: 'none' })
        return
      }

      uni.showLoading({ title: '发表中...' })
      
      postMessage({ content: this.newMessage }).then(res => {
        if (res.code === 200) {
          uni.showToast({ title: '发表成功', icon: 'success' })
          this.newMessage = ''
          this.loadMessages()
        }
      }).catch(err => {
        console.error('发表留言失败', err)
        uni.showToast({ title: '发表失败', icon: 'none' })
      }).finally(() => {
        uni.hideLoading()
      })
    },
    formatTime(timeStr) {
      const time = new Date(timeStr)
      const now = new Date()
      const diff = Math.floor((now - time) / 1000)

      if (diff < 60) return '刚刚'
      if (diff < 3600) return `${Math.floor(diff / 60)}分钟前`
      if (diff < 86400) return `${Math.floor(diff / 3600)}小时前`
      if (diff < 604800) return `${Math.floor(diff / 86400)}天前`
      
      return `${time.getMonth() + 1}月${time.getDate()}日`
    },
    goToLogin() {
      uni.navigateTo({ url: '/pages/login/login' })
    }
  }
}
</script>

<style scoped>
.container {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding-bottom: 30rpx;
}

.header {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
  padding: 50rpx 30rpx 40rpx;
  color: #fff;
}

.title {
  font-size: 40rpx;
  font-weight: bold;
  margin-bottom: 10rpx;
}

.subtitle {
  font-size: 26rpx;
  opacity: 0.9;
}

.post-section {
  background-color: #fff;
  margin: 20rpx;
  border-radius: 12rpx;
  padding: 30rpx;
}

.post-header {
  display: flex;
  align-items: center;
  margin-bottom: 20rpx;
}

.user-avatar, .user-avatar-placeholder {
  width: 60rpx;
  height: 60rpx;
  border-radius: 50%;
  margin-right: 15rpx;
}

.user-avatar-placeholder {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 28rpx;
  font-weight: bold;
}

.post-title {
  font-size: 30rpx;
  font-weight: bold;
  color: #333;
}

.message-input {
  width: 100%;
  min-height: 200rpx;
  padding: 20rpx;
  border: 1rpx solid #ddd;
  border-radius: 8rpx;
  font-size: 28rpx;
  background-color: #fafafa;
  box-sizing: border-box;
  line-height: 1.6;
}

.post-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20rpx;
}

.char-count {
  font-size: 24rpx;
  color: #999;
}

.post-btn {
  padding: 15rpx 40rpx;
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
  color: #fff;
  border-radius: 20rpx;
  font-size: 28rpx;
  font-weight: bold;
}

.login-tip {
  background-color: #fff;
  margin: 20rpx;
  padding: 40rpx;
  border-radius: 12rpx;
  text-align: center;
  color: #fa709a;
  font-size: 28rpx;
}

.message-list {
  margin: 20rpx;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20rpx 10rpx;
}

.list-title {
  font-size: 30rpx;
  font-weight: bold;
  color: #333;
}

.list-count {
  font-size: 24rpx;
  color: #999;
}

.message-item {
  background-color: #fff;
  border-radius: 12rpx;
  padding: 30rpx;
  margin-bottom: 15rpx;
}

.message-user {
  display: flex;
  align-items: center;
  margin-bottom: 20rpx;
}

.avatar, .avatar-placeholder {
  width: 70rpx;
  height: 70rpx;
  border-radius: 50%;
  margin-right: 20rpx;
}

.avatar-placeholder {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 32rpx;
  font-weight: bold;
}

.user-info {
  flex: 1;
}

.username {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 5rpx;
}

.time {
  font-size: 24rpx;
  color: #999;
}

.message-content {
  font-size: 28rpx;
  color: #666;
  line-height: 1.6;
  word-break: break-all;
}

.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 100rpx 0;
  background-color: #fff;
  border-radius: 12rpx;
}

.empty-icon {
  font-size: 100rpx;
  margin-bottom: 20rpx;
}

.empty-text {
  font-size: 28rpx;
  color: #999;
}
</style>
