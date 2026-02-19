<template>
  <view class="container">
    <view class="header">
      <view class="title">用户管理</view>
      <view class="back-btn" @click="goBack">返回</view>
    </view>

    <view class="stats">
      <view class="stat-item">
        <view class="stat-value">{{ totalUsers }}</view>
        <view class="stat-label">总用户数</view>
      </view>
      <view class="stat-item">
        <view class="stat-value">{{ adminCount }}</view>
        <view class="stat-label">管理员</view>
      </view>
      <view class="stat-item">
        <view class="stat-value">{{ userCount }}</view>
        <view class="stat-label">普通用户</view>
      </view>
    </view>

    <view class="user-list">
      <view v-for="user in users" :key="user.id" class="user-item">
        <view class="user-info">
          <view class="user-header">
            <view class="user-phone">{{ user.phone }}</view>
            <view :class="['user-role', user.role === 'admin' ? 'role-admin' : 'role-user']">
              {{ user.role === 'admin' ? '管理员' : '普通用户' }}
            </view>
          </view>
          <view class="user-meta">
            <text class="user-id">ID: {{ user.id }}</text>
            <text class="user-time">注册时间: {{ formatTime(user.created_at) }}</text>
          </view>
        </view>
        <view class="user-actions">
          <view 
            v-if="user.role === 'user'" 
            class="action-btn promote" 
            @click="changeRole(user, 'admin')"
          >
            设为管理员
          </view>
          <view 
            v-if="user.role === 'admin' && user.id !== currentUserId" 
            class="action-btn demote" 
            @click="changeRole(user, 'user')"
          >
            取消管理员
          </view>
          <view 
            v-if="user.id !== currentUserId" 
            class="action-btn delete" 
            @click="deleteUser(user)"
          >
            删除
          </view>
        </view>
      </view>
    </view>

    <view v-if="users.length === 0" class="empty">
      <text>暂无用户数据</text>
    </view>
  </view>
</template>

<script>
import { getUserList, updateUser, deleteUser } from '@/api/admin'

export default {
  data() {
    return {
      users: [],
      totalUsers: 0,
      adminCount: 0,
      userCount: 0,
      currentUserId: 0
    }
  },
  onLoad() {
    const userInfo = uni.getStorageSync('userInfo')
    if (userInfo) {
      this.currentUserId = userInfo.id
    }
    this.loadUsers()
  },
  methods: {
    loadUsers() {
      uni.showLoading({ title: '加载中...' })
      
      getUserList().then(res => {
        if (res.code === 200) {
          this.users = res.data.users
          this.totalUsers = res.data.total
          this.adminCount = this.users.filter(u => u.role === 'admin').length
          this.userCount = this.users.filter(u => u.role === 'user').length
        }
      }).catch(err => {
        console.error('加载用户列表失败', err)
      }).finally(() => {
        uni.hideLoading()
      })
    },
    changeRole(user, newRole) {
      const action = newRole === 'admin' ? '设为管理员' : '取消管理员'
      
      uni.showModal({
        title: '确认操作',
        content: `确定要将 ${user.phone} ${action}吗？`,
        success: (res) => {
          if (res.confirm) {
            updateUser(user.id, { role: newRole }).then(res => {
              if (res.code === 200) {
                uni.showToast({ title: '操作成功', icon: 'success' })
                this.loadUsers()
              }
            }).catch(err => {
              console.error('更新用户失败', err)
            })
          }
        }
      })
    },
    deleteUser(user) {
      uni.showModal({
        title: '确认删除',
        content: `确定要删除用户 ${user.phone} 吗？此操作不可恢复！`,
        confirmColor: '#e74c3c',
        success: (res) => {
          if (res.confirm) {
            deleteUser(user.id).then(res => {
              if (res.code === 200) {
                uni.showToast({ title: '删除成功', icon: 'success' })
                this.loadUsers()
              }
            }).catch(err => {
              console.error('删除用户失败', err)
            })
          }
        }
      })
    },
    formatTime(timeStr) {
      const date = new Date(timeStr)
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      const hour = String(date.getHours()).padStart(2, '0')
      const minute = String(date.getMinutes()).padStart(2, '0')
      return `${year}-${month}-${day} ${hour}:${minute}`
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

.back-btn {
  color: #e74c3c;
  font-size: 28rpx;
}

.stats {
  display: flex;
  background-color: #fff;
  margin: 20rpx;
  border-radius: 8rpx;
  padding: 30rpx 0;
}

.stat-item {
  flex: 1;
  text-align: center;
  border-right: 1rpx solid #eee;
}

.stat-item:last-child {
  border-right: none;
}

.stat-value {
  font-size: 48rpx;
  font-weight: bold;
  color: #e74c3c;
  margin-bottom: 10rpx;
}

.stat-label {
  font-size: 24rpx;
  color: #999;
}

.user-list {
  padding: 0 20rpx;
}

.user-item {
  background-color: #fff;
  border-radius: 8rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
}

.user-info {
  margin-bottom: 20rpx;
}

.user-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15rpx;
}

.user-phone {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.user-role {
  padding: 6rpx 15rpx;
  border-radius: 4rpx;
  font-size: 22rpx;
  color: #fff;
}

.role-admin {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.role-user {
  background-color: #95a5a6;
}

.user-meta {
  display: flex;
  flex-direction: column;
  gap: 8rpx;
  font-size: 24rpx;
  color: #999;
}

.user-actions {
  display: flex;
  gap: 15rpx;
}

.action-btn {
  flex: 1;
  text-align: center;
  padding: 15rpx 0;
  border-radius: 6rpx;
  font-size: 26rpx;
  color: #fff;
}

.promote {
  background-color: #3498db;
}

.demote {
  background-color: #95a5a6;
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
