<template>
  <view class="container">
    <view class="header">
      <view class="title">留言板管理</view>
      <view class="stats">
        <view class="stat-item">
          <view class="stat-value">{{ total }}</view>
          <view class="stat-label">总留言数</view>
        </view>
      </view>
    </view>

    <view class="message-list">
      <view class="message-item" v-for="msg in messages" :key="msg.id">
        <view class="message-header">
          <view class="user-info">
            <image v-if="msg.avatar" :src="msg.avatar" class="avatar" mode="aspectFill" />
            <view v-else class="avatar-placeholder">{{ msg.username.charAt(0) }}</view>
            <view class="user-details">
              <view class="username">{{ msg.username }}</view>
              <view class="time">{{ formatTime(msg.created_at) }}</view>
            </view>
          </view>
          <view class="delete-btn" @click="deleteMessage(msg.id)">删除</view>
        </view>
        <view class="message-content">{{ msg.content }}</view>
      </view>

      <view class="empty" v-if="messages.length === 0">
        <text class="empty-icon">💬</text>
        <text class="empty-text">暂无留言</text>
      </view>
    </view>
  </view>
</template>

<script>
import { getMessageList, deleteMessage } from '@/api/message'

export default {
  data() {
    return {
      messages: [],
      total: 0
    }
  },
  onLoad() {
    this.loadMessages()
  },
  methods: {
    loadMessages() {
      uni.showLoading({ title: '加载中...' })
      
      getMessageList().then(res => {
        if (res.code === 200) {
          this.messages = res.data.messages
          this.total = res.data.total
        }
      }).catch(err => {
        console.error('加载留言失败', err)
      }).finally(() => {
        uni.hideLoading()
      })
    },
    deleteMessage(id) {
      uni.showModal({
        title: '确认删除',
        content: '确定要删除这条留言吗？',
        success: (res) => {
          if (res.confirm) {
            uni.showLoading({ title: '删除中...' })
            
            deleteMessage(id).then(res => {
              if (res.code === 200) {
                uni.showToast({ title: '删除成功', icon: 'success' })
                this.loadMessages()
              }
            }).catch(err => {
              console.error('删除失败', err)
              uni.showToast({ title: '删除失败', icon: 'none' })
            }).finally(() => {
              uni.hideLoading()
            })
          }
        }
      })
    },
    formatTime(timeStr) {
      const time = new Date(timeStr)
      const year = time.getFullYear()
      const month = String(time.getMonth() + 1).padStart(2, '0')
      const day = String(time.getDate()).padStart(2, '0')
      const hour = String(time.getHours()).padStart(2, '0')
      const minute = String(time.getMinutes()).padStart(2, '0')
      
      return `${year}-${month}-${day} ${hour}:${minute}`
    }
  }
}
</script>

<style scoped>
.container {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.header {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
  padding: 30rpx;
  color: #fff;
}

.title {
  font-size: 36rpx;
  font-weight: bold;
  margin-bottom: 30rpx;
}

.stats {
  display: flex;
  gap: 30rpx;
}

.stat-item {
  background-color: rgba(255, 255, 255, 0.2);
  padding: 20rpx 30rpx;
  border-radius: 8rpx;
  text-align: center;
}

.stat-value {
  font-size: 36rpx;
  font-weight: bold;
  margin-bottom: 5rpx;
}

.stat-label {
  font-size: 24rpx;
  opacity: 0.9;
}

.message-list {
  padding: 20rpx;
}

.message-item {
  background-color: #fff;
  border-radius: 12rpx;
  padding: 30rpx;
  margin-bottom: 15rpx;
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
}

.user-info {
  display: flex;
  align-items: center;
  flex: 1;
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

.user-details {
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

.delete-btn {
  padding: 10rpx 25rpx;
  background-color: #e74c3c;
  color: #fff;
  border-radius: 20rpx;
  font-size: 24rpx;
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
