<template>
  <view class="container">
    <view class="header">
      <view class="title">管理后台</view>
      <view class="back-btn" @click="goBack">返回</view>
    </view>

    <view class="admin-info">
      <view class="admin-avatar">管</view>
      <view class="admin-details">
        <view class="admin-name">管理员</view>
        <view class="admin-phone">{{ userPhone }}</view>
      </view>
    </view>

    <view class="menu-grid">
      <view class="menu-item" @click="goToPage('/pages/admin/users')">
        <view class="menu-icon user-icon">👤</view>
        <view class="menu-name">用户管理</view>
        <view class="menu-desc">管理系统用户</view>
      </view>

      <view class="menu-item" @click="goToPage('/pages/admin/players')">
        <view class="menu-icon rank-icon">🏆</view>
        <view class="menu-name">联盟榜单管理</view>
        <view class="menu-desc">管理联盟排名</view>
      </view>

      <view class="menu-item" @click="goToPage('/pages/admin/stars')">
        <view class="menu-icon star-icon">⭐</view>
        <view class="menu-name">现役球星管理</view>
        <view class="menu-desc">球星数据管理</view>
      </view>

      <view class="menu-item" @click="goToPage('/pages/admin/matches')">
        <view class="menu-icon match-icon">📅</view>
        <view class="menu-name">今日赛事管理</view>
        <view class="menu-desc">管理比赛信息</view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      userPhone: ''
    }
  },
  onLoad() {
    const userInfo = uni.getStorageSync('userInfo')
    if (userInfo) {
      this.userPhone = userInfo.phone
    }
  },
  methods: {
    goToPage(url) {
      uni.navigateTo({ url })
    },
    showComingSoon(moduleName) {
      uni.showToast({
        title: `${moduleName}功能开发中`,
        icon: 'none',
        duration: 2000
      })
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 30rpx;
  color: #fff;
}

.title {
  font-size: 36rpx;
  font-weight: bold;
}

.back-btn {
  font-size: 28rpx;
  opacity: 0.9;
}

.admin-info {
  display: flex;
  align-items: center;
  padding: 40rpx 30rpx;
  margin: 0 30rpx 30rpx;
  background-color: rgba(255, 255, 255, 0.15);
  border-radius: 12rpx;
  backdrop-filter: blur(10px);
}

.admin-avatar {
  width: 100rpx;
  height: 100rpx;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48rpx;
  font-weight: bold;
  color: #fff;
  margin-right: 25rpx;
}

.admin-details {
  flex: 1;
}

.admin-name {
  font-size: 32rpx;
  font-weight: bold;
  color: #fff;
  margin-bottom: 8rpx;
}

.admin-phone {
  font-size: 26rpx;
  color: rgba(255, 255, 255, 0.8);
}

.menu-grid {
  padding: 0 30rpx 30rpx;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20rpx;
}

.menu-item {
  background-color: #fff;
  border-radius: 12rpx;
  padding: 40rpx 30rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.menu-item:active {
  transform: scale(0.95);
}

.menu-icon {
  font-size: 80rpx;
  margin-bottom: 20rpx;
  width: 100rpx;
  height: 100rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.player-icon {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.player-icon {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.match-icon {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.rank-icon {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.menu-name {
  font-size: 30rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 10rpx;
}

.menu-desc {
  font-size: 24rpx;
  color: #999;
  text-align: center;
}
</style>


.rank-icon {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.star-icon {
  background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
}
