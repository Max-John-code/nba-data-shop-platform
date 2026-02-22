<template>
  <view class="container">
    <view class="header">
      <view class="title">今日赛事管理</view>
      <view class="actions">
        <view class="add-btn" @click="showAddMatch">添加比赛</view>
        <view class="back-btn" @click="goBack">返回</view>
      </view>
    </view>

    <view class="match-list">
      <view v-for="match in matches" :key="match.id" class="match-item">
        <view class="match-date">{{ match.match_date }}</view>
        <view class="match-content">
          <view class="team">
            <view class="team-logo">{{ match.home_team_logo }}</view>
            <view class="team-name">{{ match.home_team_name }}</view>
            <view class="team-score">{{ match.home_team_score }}</view>
          </view>
          <view class="vs">VS</view>
          <view class="team">
            <view class="team-logo">{{ match.away_team_logo }}</view>
            <view class="team-name">{{ match.away_team_name }}</view>
            <view class="team-score">{{ match.away_team_score }}</view>
          </view>
        </view>
        <view class="match-status">{{ getStatusLabel(match.status) }}</view>
        <view class="match-actions">
          <view class="action-btn edit" @click="editMatch(match)">编辑</view>
          <view class="action-btn delete" @click="deleteMatchConfirm(match)">删除</view>
        </view>
      </view>
    </view>

    <view v-if="matches.length === 0" class="empty">暂无比赛数据</view>
  </view>
</template>

<script>
import { getAllMatches, deleteMatch } from '@/api/match'

export default {
  data() {
    return {
      matches: [],
      statusMap: {
        'upcoming': '未开始',
        'live': '进行中',
        'finished': '已结束'
      }
    }
  },
  onLoad() {
    this.loadMatches()
  },
  methods: {
    loadMatches() {
      uni.showLoading({ title: '加载中...' })
      
      getAllMatches().then(res => {
        if (res.code === 200) {
          this.matches = res.data.matches
        }
      }).catch(err => {
        console.error('加载比赛列表失败', err)
      }).finally(() => {
        uni.hideLoading()
      })
    },
    showAddMatch() {
      uni.navigateTo({ url: '/pages/admin/match-form' })
    },
    editMatch(match) {
      uni.navigateTo({ url: `/pages/admin/match-form?id=${match.id}` })
    },
    deleteMatchConfirm(match) {
      uni.showModal({
        title: '确认删除',
        content: `确定要删除比赛 ${match.home_team_name} vs ${match.away_team_name} 吗？`,
        confirmColor: '#e74c3c',
        success: (res) => {
          if (res.confirm) {
            this.deleteMatchAction(match.id)
          }
        }
      })
    },
    deleteMatchAction(matchId) {
      uni.showLoading({ title: '删除中...' })
      
      deleteMatch(matchId).then(res => {
        if (res.code === 200) {
          uni.showToast({ title: '删除成功', icon: 'success' })
          this.loadMatches()
        }
      }).catch(err => {
        console.error('删除失败', err)
      }).finally(() => {
        uni.hideLoading()
      })
    },
    goBack() {
      uni.navigateBack()
    },
    getStatusLabel(status) {
      return this.statusMap[status] || status
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

.match-list {
  padding: 20rpx;
}

.match-item {
  background-color: #fff;
  border-radius: 12rpx;
  padding: 25rpx;
  margin-bottom: 20rpx;
}

.match-date {
  font-size: 24rpx;
  color: #999;
  margin-bottom: 15rpx;
}

.match-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 15rpx;
}

.team {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8rpx;
}

.team-logo {
  font-size: 32rpx;
  font-weight: bold;
  color: #e74c3c;
}

.team-name {
  font-size: 26rpx;
  color: #333;
}

.team-score {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
}

.vs {
  font-size: 24rpx;
  color: #999;
  padding: 0 20rpx;
}

.match-status {
  text-align: center;
  font-size: 24rpx;
  color: #666;
  margin-bottom: 10rpx;
  padding: 5rpx 15rpx;
  background-color: #f0f0f0;
  border-radius: 10rpx;
  display: inline-block;
}

.match-actions {
  display: flex;
  justify-content: center;
  gap: 15rpx;
}

.action-btn {
  padding: 8rpx 25rpx;
  border-radius: 6rpx;
  font-size: 24rpx;
  color: #fff;
  text-align: center;
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
