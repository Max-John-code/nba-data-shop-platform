<template>
  <view class="container">
    <view class="header">
      <view class="logo">NBA球星数据咨询</view>
      <view class="search-box" @click="goToSearch">
        <text class="search-icon">搜</text>
        <view class="search-placeholder">搜我想看</view>
      </view>
      <view v-if="!isLogin" class="login-btn" @click="goLogin">登录</view>
      <view v-else class="user-info" @click="goUserCenter">
        <text v-if="userRole === 'admin'" class="admin-badge">管理员</text>
        <text v-else>个人中心</text>
      </view>
    </view>

    <view class="nav-menu">
      <view class="nav-item active">首页</view>
      <view class="nav-item" @click="goToRanking">联盟榜单</view>
      <view class="nav-item" @click="goToStars">现役球星</view>
      <view class="nav-item" @click="goToForum">交流论坛</view>
      <view class="nav-item" @click="goToMessages">留言板</view>
      <view class="nav-item" @click="goToShop">球星商城</view>
    </view>

    <view class="league-tabs">
      <view class="league-tab active">NBA</view>
    </view>

    <!-- 球星商城横幅 -->
    <view class="shop-banner" @click="goToShop">
      <view class="banner-left">
        <view class="banner-icon">🛍️</view>
        <view class="banner-content">
          <view class="banner-title">球星周边商城</view>
          <view class="banner-subtitle">正品球衣·限量球鞋·潮流配饰</view>
        </view>
      </view>
      <view class="banner-right">
        <text class="banner-btn">立即选购</text>
        <text class="banner-arrow">›</text>
      </view>
      <view class="banner-badge">HOT</view>
    </view>

    <view class="matches-container">
      <view v-for="match in matches" :key="match.id" class="match-card">
        <view class="match-date">{{ match.date }}</view>
        <view class="match-content">
          <view class="team team-left">
            <view class="team-logo">{{ match.team1.logo }}</view>
            <view class="team-name">{{ match.team1.name }}</view>
          </view>
          <view class="score">
            <view class="score-main">{{ match.team1.score }} - {{ match.team2.score }}</view>
            <view class="match-status">{{ getStatusLabel(match.status) }}</view>
          </view>
          <view class="team team-right">
            <view class="team-name">{{ match.team2.name }}</view>
            <view class="team-logo">{{ match.team2.logo }}</view>
          </view>
        </view>
      </view>
    </view>

    <view class="more-matches" @click="showAllMatches">
      <text>{{ getTodayDate() }} 今日全部比赛</text>
      <text class="arrow">{{ totalMatches }}场 ></text>
    </view>

    <!-- 热门新闻 -->
    <view class="hot-news" v-if="hotArticle" @click="goToArticle(hotArticle.id)">
      <view class="news-header">
        <view class="news-title-text">热门新闻</view>
      </view>
      <image v-if="hotArticle.image" :src="hotArticle.image" class="news-cover" mode="aspectFill" />
      <view class="news-info">
        <view class="news-title">{{ hotArticle.title }}</view>
        <view class="news-meta">
          <text class="author">{{ hotArticle.author_name }}</text>
          <text class="dot">·</text>
          <text class="views">{{ hotArticle.view_count }}浏览</text>
          <text class="dot">·</text>
          <text class="comments">{{ hotArticle.comment_count }}评论</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import { getMatchList } from '@/api/match'
import { getArticleList } from '@/api/forum'

export default {
  data() {
    return {
      isLogin: false,
      userRole: '',
      matches: [],
      totalMatches: 0,
      hotArticle: null,
      statusMap: {
        'upcoming': '未开始',
        'live': '进行中',
        'finished': '已结束'
      }
    }
  },
  onLoad() {
    this.checkLogin()
    this.loadTodayMatches()
    this.loadArticles()
  },
  onShow() {
    this.checkLogin()
    this.loadTodayMatches()
    this.loadArticles()
  },
  methods: {
    loadTodayMatches() {
      getMatchList().then(res => {
        if (res.code === 200) {
          this.totalMatches = res.data.total
          // 只显示前3场比赛
          const allMatches = res.data.matches.map(match => ({
            id: match.id,
            date: match.match_date,
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
          this.matches = allMatches.slice(0, 3)
        }
      }).catch(err => {
        console.error('加载比赛失败', err)
      })
    },
    loadArticles() {
      getArticleList().then(res => {
        if (res.code === 200) {
          // 只显示第一篇文章作为热门新闻
          this.hotArticle = res.data.articles[0] || null
        }
      }).catch(err => {
        console.error('加载文章失败', err)
      })
    },
    checkLogin() {
      const userInfo = uni.getStorageSync('userInfo')
      if (userInfo) {
        this.isLogin = true
        this.userRole = userInfo.role || 'user'
      } else {
        this.isLogin = false
        this.userRole = ''
      }
    },
    goLogin() {
      uni.navigateTo({
        url: '/pages/login/login'
      })
    },
    goUserCenter() {
      const itemList = this.userRole === 'admin' 
        ? ['个人信息', '管理后台', '退出登录']
        : ['个人信息', '退出登录']
      
      uni.showActionSheet({
        itemList: itemList,
        success: (res) => {
          if (this.userRole === 'admin') {
            if (res.tapIndex === 0) {
              uni.navigateTo({ url: '/pages/profile/index' })
            } else if (res.tapIndex === 1) {
              uni.navigateTo({ url: '/pages/admin/index' })
            } else if (res.tapIndex === 2) {
              this.logout()
            }
          } else {
            if (res.tapIndex === 0) {
              uni.navigateTo({ url: '/pages/profile/index' })
            } else if (res.tapIndex === 1) {
              this.logout()
            }
          }
        }
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
            this.isLogin = false
            this.userRole = ''
            uni.showToast({
              title: '已退出登录',
              icon: 'success'
            })
          }
        }
      })
    },
    goToRanking() {
      uni.navigateTo({
        url: '/pages/ranking/index'
      })
    },
    goToStars() {
      uni.navigateTo({
        url: '/pages/stars/index'
      })
    },
    goToForum() {
      uni.navigateTo({
        url: '/pages/forum/index'
      })
    },
    goToMessages() {
      uni.navigateTo({
        url: '/pages/messages/index'
      })
    },
    goToArticle(articleId) {
      uni.navigateTo({
        url: `/pages/forum/detail?id=${articleId}`
      })
    },
    showAllMatches() {
      uni.navigateTo({
        url: '/pages/matches/today'
      })
    },
    getTodayDate() {
      const today = new Date()
      const month = today.getMonth() + 1
      const day = today.getDate()
      return `${month}月${day}日`
    },
    showComingSoon(feature) {
      uni.showToast({
        title: `${feature}功能开发中`,
        icon: 'none'
      })
    },
    getStatusLabel(status) {
      return this.statusMap[status] || status
    },
    goToSearch() {
      uni.navigateTo({ url: '/pages/search/index' })
    },
    goToShop() {
      uni.navigateTo({ url: '/pages/shop/index' })
    }
  }
}
</script>

<style scoped>
.container {
  background-color: #f5f5f5;
  min-height: 100vh;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15rpx 20rpx;
  background-color: #fff;
  border-bottom: 1rpx solid #eee;
}

.logo {
  font-size: 24rpx;
  font-weight: bold;
  color: #e74c3c;
  white-space: nowrap;
}

.search-box {
  flex: 1;
  display: flex;
  align-items: center;
  margin: 0 20rpx;
  background-color: #f0f0f0;
  border-radius: 20rpx;
  padding: 8rpx 15rpx;
}

.search-icon {
  margin-right: 10rpx;
  color: #999;
}

.search-input {
  flex: 1;
  background: transparent;
  border: none;
  font-size: 28rpx;
  color: #333;
}

.search-placeholder {
  flex: 1;
  font-size: 28rpx;
  color: #999;
}

.app-btn {
  background-color: #e74c3c;
  color: white;
  padding: 8rpx 20rpx;
  border-radius: 4rpx;
  font-size: 24rpx;
  font-weight: bold;
  display: none;
}

.login-btn {
  background-color: #e74c3c;
  color: white;
  padding: 10rpx 25rpx;
  border-radius: 4rpx;
  font-size: 26rpx;
  font-weight: bold;
  white-space: nowrap;
}

.user-info {
  color: #e74c3c;
  font-size: 26rpx;
  font-weight: bold;
  white-space: nowrap;
  display: flex;
  align-items: center;
}

.admin-badge {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 8rpx 15rpx;
  border-radius: 4rpx;
  font-size: 24rpx;
}

.nav-menu {
  display: flex;
  background-color: #fff;
  border-bottom: 1rpx solid #eee;
  overflow-x: auto;
}

.nav-item {
  flex-shrink: 0;
  padding: 20rpx 25rpx;
  font-size: 28rpx;
  color: #666;
  border-bottom: 3rpx solid transparent;
}

.nav-item.active {
  color: #e74c3c;
  border-bottom-color: #e74c3c;
}

.league-tabs {
  display: flex;
  background-color: #fff;
  padding: 15rpx 20rpx;
  border-bottom: 1rpx solid #eee;
}

.league-tab {
  padding: 8rpx 20rpx;
  margin-right: 15rpx;
  border-radius: 4rpx;
  font-size: 26rpx;
  color: #999;
  background-color: #f5f5f5;
}

.league-tab.active {
  background-color: #e74c3c;
  color: white;
}

.shop-banner {
  margin: 15rpx 20rpx;
  padding: 30rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16rpx;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 8rpx 20rpx rgba(102, 126, 234, 0.3);
  position: relative;
  overflow: hidden;
  transition: transform 0.3s ease;
}

.shop-banner:active {
  transform: scale(0.98);
}

.banner-badge {
  position: absolute;
  top: 15rpx;
  right: 15rpx;
  padding: 8rpx 20rpx;
  background-color: #ff4757;
  color: #fff;
  font-size: 22rpx;
  font-weight: bold;
  border-radius: 20rpx;
  box-shadow: 0 4rpx 8rpx rgba(255, 71, 87, 0.4);
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

.banner-left {
  display: flex;
  align-items: center;
  gap: 20rpx;
}

.banner-icon {
  font-size: 70rpx;
  filter: drop-shadow(0 4rpx 8rpx rgba(0, 0, 0, 0.2));
}

.banner-content {
  display: flex;
  flex-direction: column;
  gap: 8rpx;
}

.banner-title {
  font-size: 36rpx;
  font-weight: bold;
  color: #fff;
  text-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.2);
}

.banner-subtitle {
  font-size: 24rpx;
  color: rgba(255, 255, 255, 0.9);
}

.banner-right {
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.banner-btn {
  padding: 15rpx 30rpx;
  background-color: rgba(255, 255, 255, 0.95);
  color: #667eea;
  border-radius: 30rpx;
  font-size: 28rpx;
  font-weight: bold;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.15);
}

.banner-arrow {
  font-size: 50rpx;
  color: #fff;
  font-weight: bold;
}

.matches-container {
  background-color: #fff;
  margin: 15rpx 0;
}

.match-card {
  padding: 20rpx;
  border-bottom: 1rpx solid #eee;
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
  font-size: 28rpx;
  margin-bottom: 8rpx;
  font-weight: bold;
  color: #e74c3c;
}

.team-name {
  font-size: 26rpx;
  color: #333;
}

.score {
  flex: 1;
  text-align: center;
  margin: 0 30rpx;
}

.score-main {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
}

.match-status {
  font-size: 22rpx;
  color: #999;
  margin-top: 8rpx;
  padding: 4rpx 12rpx;
  background-color: #f5f5f5;
  border-radius: 10rpx;
  display: inline-block;
}

.more-matches {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #fff;
  padding: 20rpx;
  margin: 15rpx 0;
  font-size: 26rpx;
  color: #333;
  cursor: pointer;
}

.arrow {
  color: #e74c3c;
  font-weight: bold;
}

.hot-news {
  background-color: #fff;
  margin: 15rpx 0;
  overflow: hidden;
}

.news-header {
  padding: 20rpx 20rpx 15rpx;
  border-bottom: 1rpx solid #eee;
}

.news-title-text {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.news-cover {
  width: 100%;
  height: 400rpx;
}

.news-info {
  padding: 25rpx 20rpx;
}

.news-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  line-height: 1.5;
  margin-bottom: 15rpx;
}

.news-meta {
  display: flex;
  align-items: center;
  font-size: 24rpx;
  color: #999;
  gap: 8rpx;
}

.author {
  color: #666;
}

.dot {
  color: #ddd;
}
</style>