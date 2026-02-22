<template>
  <view class="container">
    <view class="header">
      <view class="title">{{ getTodayDate() }} 今日全部比赛</view>
      <view class="count">共 {{ matches.length }} 场</view>
    </view>

    <view class="matches-list">
      <view class="match-card" v-for="match in matches" :key="match.id">
        <view class="match-time">{{ match.match_time }}</view>
        <view class="match-content">
          <view class="team team-left">
            <view class="team-logo">{{ match.team1.logo }}</view>
            <view class="team-name">{{ match.team1.name }}</view>
          </view>
          <view class="score">
            <view class="score-main">{{ match.team1.score }} - {{ match.team2.score }}</view>
            <view class="status">{{ getStatusLabel(match.status) }}</view>
          </view>
          <view class="team team-right">
            <view class="team-name">{{ match.team2.name }}</view>
            <view class="team-logo">{{ match.team2.logo }}</view>
          </view>
        </view>
      </view>

      <view class="empty" v-if="matches.length === 0">
        <text class="empty-icon">🏀</text>
        <text class="empty-text">今日暂无比赛</text>
      </view>
    </view>
  </view>
</template>

<script>
import { getMatchList } from '@/api/match'

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
      
      getMatchList().then(res => {
        if (res.code === 200) {
          this.matches = res.data.matches.map(match => ({
            id: match.id,
            match_time: match.match_time,
            status: match.status,
            team1: {
              name: match.home_team_name,
              logo: match.home_team_logo,
              score: match.home_team_score
            },
            team2: {
              name: match.away_team_name,
              logo: match.away_team_logo,
              score: match.away_team_score
            }
          }))
        }
      }).catch(err => {
        console.error('加载比赛失败', err)
        uni.showToast({ title: '加载失败', icon: 'none' })
      }).finally(() => {
        uni.hideLoading()
      })
    },
    getTodayDate() {
      const today = new Date()
      const month = today.getMonth() + 1
      const day = today.getDate()
      return `${month}月${day}日`
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
}

.header {
  background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
  padding: 40rpx 30rpx;
  color: #fff;
}

.title {
  font-size: 36rpx;
  font-weight: bold;
  margin-bottom: 10rpx;
}

.count {
  font-size: 26rpx;
  opacity: 0.9;
}

.matches-list {
  padding: 20rpx;
}

.match-card {
  background-color: #fff;
  border-radius: 12rpx;
  padding: 25rpx;
  margin-bottom: 15rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
}

.match-time {
  font-size: 24rpx;
  color: #999;
  margin-bottom: 20rpx;
  text-align: center;
}

.match-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.team {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
}

.team-left {
  align-items: flex-end;
}

.team-right {
  align-items: flex-start;
}

.team-logo {
  font-size: 32rpx;
  margin-bottom: 10rpx;
  font-weight: bold;
  color: #e74c3c;
}

.team-name {
  font-size: 28rpx;
  color: #333;
  font-weight: 500;
}

.score {
  flex: 1;
  text-align: center;
  margin: 0 30rpx;
}

.score-main {
  font-size: 40rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 8rpx;
}

.status {
  font-size: 22rpx;
  color: #999;
  padding: 4rpx 12rpx;
  background-color: #f5f5f5;
  border-radius: 10rpx;
  display: inline-block;
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
