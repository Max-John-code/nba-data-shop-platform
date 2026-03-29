<template>
  <view class="container">
    <view class="header">
      <view class="avatar-section" @click="chooseAvatar">
        <image v-if="userInfo.avatar" :src="userInfo.avatar" class="avatar" mode="aspectFill" />
        <view v-else class="avatar-placeholder">
          <text class="avatar-text">{{ userInfo.username ? userInfo.username.charAt(0) : '?' }}</text>
        </view>
        <view class="avatar-tip">点击更换头像</view>
      </view>
    </view>

    <view class="info-section">
      <view class="info-item">
        <view class="info-label">用户名</view>
        <view class="info-value" @click="showEditUsername">
          <text>{{ userInfo.username || '未设置' }}</text>
          <text class="edit-icon">></text>
        </view>
      </view>

      <view class="info-item">
        <view class="info-label">手机号</view>
        <view class="info-value">
          <text>{{ userInfo.phone }}</text>
        </view>
      </view>

      <view class="info-item">
        <view class="info-label">角色</view>
        <view class="info-value">
          <view :class="['role-badge', userInfo.role === 'admin' ? 'role-admin' : 'role-user']">
            {{ userInfo.role === 'admin' ? '管理员' : '普通用户' }}
          </view>
        </view>
      </view>

      <view class="info-item">
        <view class="info-label">注册时间</view>
        <view class="info-value">
          <text>{{ formatTime(userInfo.created_at) }}</text>
        </view>
      </view>
    </view>

    <view class="menu-section">
      <view class="menu-item" @click="goToOrders">
        <text class="menu-icon">📦</text>
        <text class="menu-label">我的订单</text>
        <text class="menu-arrow">></text>
      </view>
    </view>

    <view class="logout-btn" @click="logout">退出登录</view>
  </view>
</template>

<script>
import { getProfile, updateProfile, uploadAvatar } from '@/api/auth'

export default {
  data() {
    return {
      userInfo: {
        username: '',
        phone: '',
        role: 'user',
        avatar: '',
        created_at: ''
      }
    }
  },
  onLoad() {
    this.loadProfile()
  },
  methods: {
    loadProfile() {
      uni.showLoading({ title: '加载中...' })
      
      getProfile().then(res => {
        console.log('获取个人信息响应:', res)
        if (res.code === 200) {
          console.log('用户头像:', res.data.avatar)
          this.userInfo = res.data
        }
      }).catch(err => {
        console.error('加载个人信息失败', err)
        uni.showToast({ title: '加载失败', icon: 'none' })
      }).finally(() => {
        uni.hideLoading()
      })
    },
    chooseAvatar() {
      uni.chooseImage({
        count: 1,
        sizeType: ['compressed'],
        sourceType: ['album', 'camera'],
        success: (res) => {
          console.log('选择图片成功', res)
          const tempFilePath = res.tempFilePaths[0]
          
          // H5环境需要转换为base64
          // #ifdef H5
          this.convertImageToBase64H5(tempFilePath)
          // #endif
          
          // 非H5环境
          // #ifndef H5
          uni.compressImage({
            src: tempFilePath,
            quality: 60,
            success: (compressRes) => {
              this.convertToBase64(compressRes.tempFilePath)
            },
            fail: () => {
              this.convertToBase64(tempFilePath)
            }
          })
          // #endif
        },
        fail: (err) => {
          console.error('选择图片失败', err)
          uni.showToast({ title: '选择图片失败', icon: 'none' })
        }
      })
    },
    convertImageToBase64H5(blobUrl) {
      console.log('H5环境转换base64', blobUrl)
      uni.showLoading({ title: '处理中...' })
      
      // 创建XMLHttpRequest获取blob数据
      const xhr = new XMLHttpRequest()
      xhr.open('GET', blobUrl, true)
      xhr.responseType = 'blob'
      
      xhr.onload = () => {
        if (xhr.status === 200) {
          const blob = xhr.response
          const reader = new FileReader()
          
          reader.onloadend = () => {
            const base64 = reader.result
            console.log('base64转换成功，长度:', base64.length)
            
            if (base64.length > 2 * 1024 * 1024) {
              uni.hideLoading()
              uni.showToast({ 
                title: '图片过大，请选择小一点的图片', 
                icon: 'none',
                duration: 2000
              })
              return
            }
            
            this.uploadAvatarToServer(base64)
          }
          
          reader.onerror = () => {
            uni.hideLoading()
            console.error('读取blob失败')
            uni.showToast({ title: '读取图片失败', icon: 'none' })
          }
          
          reader.readAsDataURL(blob)
        }
      }
      
      xhr.onerror = () => {
        uni.hideLoading()
        console.error('获取blob失败')
        uni.showToast({ title: '获取图片失败', icon: 'none' })
      }
      
      xhr.send()
    },
    convertToBase64(filePath) {
      console.log('开始转换base64', filePath)
      uni.showLoading({ title: '处理中...' })
      
      uni.getFileSystemManager().readFile({
        filePath: filePath,
        encoding: 'base64',
        success: (fileRes) => {
          console.log('base64转换成功，长度:', fileRes.data.length)
          const base64 = 'data:image/jpeg;base64,' + fileRes.data
          
          if (base64.length > 2 * 1024 * 1024) {
            uni.hideLoading()
            uni.showToast({ 
              title: '图片过大，请选择小一点的图片', 
              icon: 'none',
              duration: 2000
            })
            return
          }
          
          this.uploadAvatarToServer(base64)
        },
        fail: (err) => {
          uni.hideLoading()
          console.error('读取文件失败', err)
          uni.showToast({ title: '读取图片失败', icon: 'none' })
        }
      })
    },
    uploadAvatarToServer(avatarData) {
      console.log('开始上传头像，数据长度:', avatarData.length)
      uni.showLoading({ title: '上传中...' })
      
      uploadAvatar(avatarData).then(res => {
        console.log('上传响应:', res)
        uni.hideLoading()
        if (res.code === 200) {
          this.userInfo.avatar = res.data.avatar
          // 更新本地存储
          const userInfo = uni.getStorageSync('userInfo')
          userInfo.avatar = res.data.avatar
          uni.setStorageSync('userInfo', userInfo)
          
          uni.showToast({ title: '上传成功', icon: 'success' })
        } else {
          uni.showToast({ 
            title: res.message || '上传失败', 
            icon: 'none',
            duration: 2000
          })
        }
      }).catch(err => {
        uni.hideLoading()
        console.error('上传头像失败', err)
        uni.showToast({ 
          title: '上传失败，请重试', 
          icon: 'none',
          duration: 2000
        })
      })
    },
    showEditUsername() {
      uni.showModal({
        title: '修改用户名',
        editable: true,
        placeholderText: '请输入新用户名',
        content: this.userInfo.username,
        success: (res) => {
          if (res.confirm && res.content) {
            const newUsername = res.content.trim()
            if (newUsername) {
              this.updateUsername(newUsername)
            }
          }
        }
      })
    },
    updateUsername(username) {
      uni.showLoading({ title: '更新中...' })
      
      updateProfile({ username }).then(res => {
        if (res.code === 200) {
          this.userInfo.username = res.data.username
          // 更新本地存储
          const userInfo = uni.getStorageSync('userInfo')
          userInfo.username = res.data.username
          uni.setStorageSync('userInfo', userInfo)
          
          uni.showToast({ title: '更新成功', icon: 'success' })
        }
      }).catch(err => {
        console.error('更新用户名失败', err)
      }).finally(() => {
        uni.hideLoading()
      })
    },
    logout() {
      uni.showModal({
        title: '提示',
        content: '确定要退出登录吗？',
        success: (res) => {
          if (res.confirm) {
            uni.removeStorageSync('token')
            uni.removeStorageSync('userInfo')
            uni.showToast({ title: '已退出登录', icon: 'success' })
            setTimeout(() => {
              uni.reLaunch({ url: '/pages/index/index' })
            }, 1500)
          }
        }
      })
    },
    goToOrders() {
      uni.navigateTo({ url: '/pages/shop/orders' })
    },
    formatTime(timeStr) {
      if (!timeStr) return ''
      const date = new Date(timeStr)
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      return `${year}-${month}-${day}`
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 60rpx 0 80rpx;
  display: flex;
  justify-content: center;
  align-items: center;
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.avatar,
.avatar-placeholder {
  width: 160rpx;
  height: 160rpx;
  border-radius: 50%;
  border: 6rpx solid rgba(255, 255, 255, 0.3);
  overflow: hidden;
}

.avatar-placeholder {
  background-color: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-text {
  font-size: 60rpx;
  font-weight: bold;
  color: #fff;
}

.avatar-tip {
  margin-top: 20rpx;
  font-size: 24rpx;
  color: rgba(255, 255, 255, 0.8);
}

.info-section {
  background-color: #fff;
  margin: -40rpx 20rpx 20rpx;
  border-radius: 12rpx;
  padding: 0 30rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.08);
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 35rpx 0;
  border-bottom: 1rpx solid #f0f0f0;
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  font-size: 28rpx;
  color: #666;
}

.info-value {
  display: flex;
  align-items: center;
  font-size: 28rpx;
  color: #333;
}

.edit-icon {
  margin-left: 10rpx;
  color: #999;
  font-size: 24rpx;
}

.role-badge {
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

.logout-btn {
  margin: 20rpx;
  padding: 25rpx 0;
  background-color: #fff;
  border-radius: 12rpx;
  text-align: center;
  font-size: 30rpx;
  color: #e74c3c;
  font-weight: bold;
}
</style>


.menu-section {
  background-color: #fff;
  margin: 20rpx;
  border-radius: 12rpx;
  overflow: hidden;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 30rpx;
  border-bottom: 1rpx solid #f5f5f5;
}

.menu-item:last-child {
  border-bottom: none;
}

.menu-icon {
  font-size: 40rpx;
  margin-right: 20rpx;
}

.menu-label {
  flex: 1;
  font-size: 30rpx;
  color: #333;
}

.menu-arrow {
  font-size: 28rpx;
  color: #999;
}
