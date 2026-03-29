<template>
  <view class="container">
    <view class="header">
      <view class="title">现役球星管理</view>
      <view class="actions">
        <view class="add-btn" @click="showAddStar">添加球星</view>
        <view class="back-btn" @click="goBack">返回</view>
      </view>
    </view>

    <view class="player-list">
      <view v-for="player in players" :key="player.id" class="player-item">
        <view class="player-avatar">
          <image v-if="player.avatar" :src="player.avatar" mode="aspectFill" />
          <view v-else class="avatar-placeholder">{{ player.name.charAt(0) }}</view>
        </view>
        <view class="player-info">
          <view class="player-name">{{ player.name }}</view>
          <view class="player-team">{{ player.team }} | {{ player.position }}</view>
        </view>
        <view class="player-stats">
          <view class="stat-item">得分: {{ player.points_per_game }}</view>
          <view class="stat-item">篮板: {{ player.rebounds_per_game }}</view>
          <view class="stat-item">助攻: {{ player.assists_per_game }}</view>
        </view>
        <view class="player-actions">
          <view class="action-btn edit" @click="editPlayer(player)">编辑</view>
          <view class="action-btn delete" @click="deletePlayerConfirm(player)">删除</view>
        </view>
      </view>
    </view>

    <view v-if="players.length === 0" class="empty">暂无球星数据</view>
  </view>
</template>

<script>
import { getPlayerList, deletePlayer } from '@/api/player'

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
        console.error('加载球星列表失败', err)
      }).finally(() => {
        uni.hideLoading()
      })
    },
    showAddStar() {
      uni.navigateTo({ url: '/pages/admin/star-form' })
    },
    editPlayer(player) {
      uni.navigateTo({ url: `/pages/admin/star-form?id=${player.id}` })
    },
    deletePlayerConfirm(player) {
      uni.showModal({
        title: '确认删除',
        content: `确定要删除球星 ${player.name} 吗？`,
        confirmColor: '#e74c3c',
        success: (res) => {
          if (res.confirm) {
            this.deletePlayerAction(player.id)
          }
        }
      })
    },
    deletePlayerAction(playerId) {
      uni.showLoading({ title: '删除中...' })
      
      deletePlayer(playerId).then(res => {
        if (res.code === 200) {
          uni.showToast({ title: '删除成功', icon: 'success' })
          this.loadPlayers()
        }
      }).catch(err => {
        console.error('删除失败', err)
      }).finally(() => {
        uni.hideLoading()
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

.player-list {
  padding: 20rpx;
}

.player-item {
  background-color: #fff;
  border-radius: 12rpx;
  padding: 25rpx;
  margin-bottom: 20rpx;
  display: flex;
  align-items: center;
  gap: 20rpx;
}

.player-avatar {
  width: 100rpx;
  height: 100rpx;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
}

.player-avatar image {
  width: 100%;
  height: 100%;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  background-color: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40rpx;
  color: #999;
}

.player-info {
  flex: 1;
}

.player-name {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 8rpx;
}

.player-team {
  font-size: 24rpx;
  color: #999;
}

.player-stats {
  display: flex;
  flex-direction: column;
  gap: 5rpx;
  margin-right: 20rpx;
}

.stat-item {
  font-size: 22rpx;
  color: #666;
}

.player-actions {
  display: flex;
  flex-direction: column;
  gap: 10rpx;
}

.action-btn {
  padding: 8rpx 20rpx;
  border-radius: 6rpx;
  font-size: 24rpx;
  color: #fff;
  text-align: center;
  min-width: 80rpx;
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
