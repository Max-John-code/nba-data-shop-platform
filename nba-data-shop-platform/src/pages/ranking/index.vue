<template>
  <view class="container">
    <view class="header">
      <view class="title">NBA联盟榜单</view>
      <view class="subtitle">League Rankings</view>
    </view>

    <view class="ranking-list">
      <view v-for="player in players" :key="player.id" class="ranking-item">
        <view class="rank-badge" :class="getRankClass(player.ranking)">
          <text class="rank-number">{{ player.ranking }}</text>
        </view>
        
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
      <text class="empty-icon">🏀</text>
      <text class="empty-text">暂无榜单数据</text>
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
      
      getPlayerList('ranking').then(res => {
        if (res.code === 200) {
          this.players = res.data.players
        }
      }).catch(err => {
        console.error('加载榜单失败', err)
        uni.showToast({ title: '加载失败', icon: 'none' })
      }).finally(() => {
        uni.hideLoading()
      })
    },
    getRankClass(rank) {
      if (rank === 1) return 'rank-gold'
      if (rank === 2) return 'rank-silver'
      if (rank === 3) return 'rank-bronze'
      return 'rank-normal'
    }
  }
}
</script>

<style scoped>
.container {
  min-height: 100vh;
  background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
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

.ranking-list {
  padding: 20rpx;
}

.ranking-item {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
  backdrop-filter: blur(10px);
  border-radius: 16rpx;
  padding: 25rpx;
  margin-bottom: 20rpx;
  display: flex;
  align-items: center;
  gap: 20rpx;
  border: 1rpx solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.3);
}

.rank-badge {
  width: 80rpx;
  height: 80rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  flex-shrink: 0;
}

.rank-gold {
  background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
  box-shadow: 0 4rpx 12rpx rgba(255, 215, 0, 0.5);
}

.rank-silver {
  background: linear-gradient(135deg, #c0c0c0 0%, #e8e8e8 100%);
  box-shadow: 0 4rpx 12rpx rgba(192, 192, 192, 0.5);
}

.rank-bronze {
  background: linear-gradient(135deg, #cd7f32 0%, #e8a87c 100%);
  box-shadow: 0 4rpx 12rpx rgba(205, 127, 50, 0.5);
}

.rank-normal {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.rank-number {
  font-size: 36rpx;
  color: #fff;
  text-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.3);
}

.player-avatar {
  width: 100rpx;
  height: 100rpx;
  border-radius: 50%;
  overflow: hidden;
  border: 3rpx solid rgba(255, 255, 255, 0.3);
  flex-shrink: 0;
}

.player-avatar image {
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
  font-size: 40rpx;
  font-weight: bold;
  color: #fff;
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
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
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
