<template>
  <view class="container">
    <view class="header">
      <view class="title">联盟榜单管理</view>
      <view class="actions">
        <view class="add-btn" @click="showAddPlayer">添加球员</view>
        <view class="back-btn" @click="goBack">返回</view>
      </view>
    </view>

    <view class="player-list">
      <view v-for="player in players" :key="player.id" class="player-item">
        <view v-if="player.ranking >= 1 && player.ranking <= 3" class="player-rank">{{ player.ranking }}</view>
        <view v-else class="player-rank-placeholder"></view>
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

    <view v-if="players.length === 0" class="empty">暂无球员数据</view>
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
      
      getPlayerList('ranking').then(res => {
        if (res.code === 200) {
          const allPlayers = res.data.players
          
          // 分离前三名和其他球员
          const topThree = allPlayers.filter(p => p.ranking >= 1 && p.ranking <= 3)
            .sort((a, b) => a.ranking - b.ranking)
          
          const others = allPlayers.filter(p => p.ranking === 0 || p.ranking > 3)
            .sort((a, b) => b.id - a.id)
          
          // 合并显示
          this.players = [...topThree, ...others]
        }
      }).catch(err => {
        console.error('加载球员列表失败', err)
      }).finally(() => {
        uni.hideLoading()
      })
    },
    showAddPlayer() {
      uni.navigateTo({ url: '/pages/admin/player-form' })
    },
    editPlayer(player) {
      uni.navigateTo({ url: `/pages/admin/player-form?id=${player.id}` })
    },
    deletePlayerConfirm(player) {
      uni.showModal({
        title: '确认删除',
        content: `确定要删除球员 ${player.name} 吗？`,
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

.player-rank {
  font-size: 48rpx;
  font-weight: bold;
  color: #e74c3c;
  min-width: 80rpx;
  text-align: center;
}

.player-rank-placeholder {
  min-width: 80rpx;
}

.player-avatar {
  width: 100rpx;
  height: 100rpx;
  border-radius: 50%;
  overflow: hidden;
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
  margin-bottom: 8rpx;
}

.player-rating {
  display: flex;
  gap: 5rpx;
}

.star {
  font-size: 28rpx;
  color: #ddd;
}

.star-filled {
  color: #ffd700;
}

.player-rating {
  display: flex;
  gap: 5rpx;
}

.star {
  font-size: 28rpx;
  color: #ddd;
}

.star-filled {
  color: #ffd700;
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

/* 弹窗样式 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.modal-content {
  width: 90%;
  max-width: 700rpx;
  max-height: 85vh;
  background-color: #fff;
  border-radius: 12rpx;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 30rpx;
  border-bottom: 1rpx solid #eee;
  flex-shrink: 0;
}

.modal-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.modal-close {
  font-size: 48rpx;
  color: #999;
  line-height: 1;
}

.modal-body {
  flex: 1;
  padding: 30rpx;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}

.form-section {
  margin-bottom: 30rpx;
}

.section-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
  padding-bottom: 10rpx;
  border-bottom: 2rpx solid #e74c3c;
}

.form-row {
  display: flex;
  gap: 20rpx;
}

.form-item {
  margin-bottom: 25rpx;
}

.form-item.half {
  flex: 1;
  margin-bottom: 0;
}

.form-label {
  font-size: 26rpx;
  color: #666;
  margin-bottom: 10rpx;
}

.form-input {
  width: 100%;
  padding: 18rpx;
  border: 1rpx solid #ddd;
  border-radius: 6rpx;
  font-size: 28rpx;
  box-sizing: border-box;
  background-color: #fff;
  color: #333;
}

.form-input:focus {
  border-color: #e74c3c;
  outline: none;
}

.avatar-upload {
  width: 150rpx;
  height: 150rpx;
  border-radius: 12rpx;
  border: 2rpx dashed #ddd;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background-color: #fafafa;
}

.upload-avatar {
  width: 100%;
  height: 100%;
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8rpx;
}

.upload-icon {
  font-size: 48rpx;
}

.upload-text {
  font-size: 22rpx;
  color: #999;
}

.modal-footer {
  display: flex;
  border-top: 1rpx solid #eee;
  flex-shrink: 0;
}

.modal-btn {
  flex: 1;
  padding: 30rpx 0;
  text-align: center;
  font-size: 30rpx;
}

.cancel {
  color: #666;
  border-right: 1rpx solid #eee;
}

.confirm {
  color: #fff;
  background-color: #e74c3c;
  font-weight: bold;
}
</style>
