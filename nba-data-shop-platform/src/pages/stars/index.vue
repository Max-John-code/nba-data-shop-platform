<template>
  <view class="container">
    <view class="header">
      <view class="title">现役球星</view>
      <view class="subtitle">Active Stars</view>
    </view>

    <view class="stars-list">
      <view v-for="player in players" :key="player.id" class="star-item">
        <view class="player-avatar">
          <image v-if="player.avatar" :src="player.avatar" mode="aspectFill" />
          <view v-else class="avatar-placeholder">{{ player.name.charAt(0) }}</view>
        </view>
        
        <view class="player-info">
          <view class="player-name">{{ player.name }}</view>
          <view class="player-team">{{ player.team }} · {{ player.position }}</view>
        </view>
        
        <view class="player-stats">
          <view class="stat-row">
            <view class="stat-item">
              <text class="stat-value">{{ player.points_per_game }}</text>
              <text class="stat-label">得分</text>
            </view>
            <view class="stat-item">
              <text class="stat-value">{{ player.rebounds_per_game }}</text>
              <text class="stat-label">篮板</text>
            </view>
            <view class="stat-item">
              <text class="stat-value">{{ player.assists_per_game }}</text>
              <text class="stat-label">助攻</text>
            </view>
          </view>
        </view>
      </view>
    </view>

    <view v-if="players.length === 0" class="empty">
      <text class="empty-icon">⭐</text>
      <text class="empty-text">暂无球星数据</text>
    </view>
  </view>
</template>

<script>
import { getPlayerList } from '@/api/player'

export default {
  data() {
    return {
      players: []
    }
  },
  onLoad() {
    this.loadPlayers()
  },
  methods: {
    loadPlayers() {
      uni.showLoading({ title: '加载中...' })
      
      getPlayerList('star').then(res => {
        if (res.code === 200) {
          this.players = res.data.players
        }
      }).catch(err => {
        console.error('加载球星失败', err)
        uni.showToast({ title: '加载失败', icon: 'none' })
      }).finally(() => {
        uni.hideLoading()
      })
    }
  }
}
</script>

<style scoped>
.container {
  min-height: 100vh;
  background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
  padding-bottom: 20rpx;
}

.header {
  padding: 60rpx 30rpx 40rpx;
  text-align: center;
  background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
}

.title {
  font-size: 48rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 10rpx;
}

.subtitle {
  font-size: 24rpx;
  color: rgba(0, 0, 0, 0.6);
  letter-spacing: 2rpx;
}

.stars-list {
  padding: 20rpx;
}

.star-item {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0.08) 100%);
  backdrop-filter: blur(10px);
  border-radius: 16rpx;
  padding: 25rpx;
  margin-bottom: 20rpx;
  display: flex;
  align-items: center;
  gap: 20rpx;
  border: 1rpx solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.3);
}

.player-avatar {
  width: 100rpx;
  height: 100rpx;
  border-radius: 50%;
  overflow: hidden;
  border: 3rpx solid rgba(255, 215, 0, 0.5);
  flex-shrink: 0;
}

.player-avatar image {
  width: 100%;
  height: 100%;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #ffd700 0%, #ffb347 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40rpx;
  font-weight: bold;
  color: #333;
}

.player-info {
  flex: 1;
  min-width: 0;
}

.player-name {
  font-size: 32rpx;
  font-weight: bold;
  color: #fff;
  margin-bottom: 8rpx;
}

.player-team {
  font-size: 24rpx;
  color: rgba(255, 255, 255, 0.7);
}

.player-stats {
  flex-shrink: 0;
}

.stat-row {
  display: flex;
  gap: 25rpx;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5rpx;
}

.stat-value {
  font-size: 28rpx;
  font-weight: bold;
  color: #ffd700;
}

.stat-label {
  font-size: 20rpx;
  color: rgba(255, 255, 255, 0.6);
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
  color: rgba(255, 255, 255, 0.5);
}
</style>
