<template>
  <view class="container">
    <view class="header">
      <view class="logo">NBA球星数据咨询</view>
      <view class="search-box">
        <text class="search-icon">搜</text>
        <input type="text" placeholder="搜我想看" class="search-input" />
      </view>
      <view v-if="!isLogin" class="login-btn" @click="goLogin">登录</view>
      <view v-else class="user-info" @click="goUserCenter">个人中心</view>
    </view>

    <view class="nav-menu">
      <view class="nav-item active">首页</view>
      <view class="nav-item">热榜</view>
      <view class="nav-item">评分</view>
      <view class="nav-item">篮球</view>
      <view class="nav-item">足球</view>
      <view class="nav-item">步行街</view>
      <view class="nav-item">电竞</view>
    </view>

    <view class="league-tabs">
      <view class="league-tab active">NBA</view>
      <view class="league-tab">CBA</view>
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
            <view class="score-sub">{{ match.viewers }}人评分</view>
          </view>
          <view class="team team-right">
            <view class="team-name">{{ match.team2.name }}</view>
            <view class="team-logo">{{ match.team2.logo }}</view>
          </view>
        </view>
      </view>
    </view>

    <view class="more-matches">
      <text>2月12日 今日全部比赛</text>
      <text class="arrow">14场 ></text>
    </view>

    <view class="features">
      <view class="feature-item">
        <view class="feature-icon">赛</view>
        <view class="feature-name">赛程</view>
      </view>
      <view class="feature-item">
        <view class="feature-icon">榜</view>
        <view class="feature-name">球队榜</view>
      </view>
      <view class="feature-item">
        <view class="feature-icon">员</view>
        <view class="feature-name">球员榜</view>
      </view>
    </view>

    <view class="news-container">
      <view v-for="news in newsList" :key="news.id" class="news-item" @click="goNewsDetail(news.id)">
        <view class="news-content">
          <view class="news-title">{{ news.title }}</view>
          <view class="news-meta">
            <text class="comment-count">{{ news.comments }}</text>
            <text class="like-count">{{ news.likes }}</text>
          </view>
        </view>
        <view class="news-image">图</view>
        <view class="news-tag">直播</view>
      </view>
    </view>

    <!-- 推荐新闻 -->
    <view class="recommend-section">
      <view class="recommend-title">推荐</view>
      <view class="recommend-item" @click="goNewsDetail(5)">
        <view class="recommend-label">资讯</view>
        <view class="recommend-content">
          <view class="recommend-text">流言板米切尔：作为老鹰球迷若能与他同队会很特别但那不取决于我</view>
          <view class="recommend-meta">
            <text>487</text>
            <text>548</text>
          </view>
        </view>
        <image src="https://via.placeholder.com/100x80?text=NBA" class="recommend-image" />
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      isLogin: false,
      matches: [
        {
          id: 1,
          date: '2月12日',
          team1: { name: '快船', logo: 'LAC', score: 105 },
          team2: { name: '火箭', logo: 'HOU', score: 102 },
          viewers: '17.6万'
        },
        {
          id: 2,
          date: '2月12日',
          team1: { name: '奇才', logo: 'WAS', score: 113 },
          team2: { name: '骑士', logo: 'CLE', score: 138 },
          viewers: '15.4万'
        },
        {
          id: 3,
          date: '2月12日',
          team1: { name: '马刺', logo: 'SAS', score: 126 },
          team2: { name: '勇士', logo: 'GSW', score: 113 },
          viewers: '12.7万'
        }
      ],
      newsList: [
        {
          id: 1,
          title: '美媒对比韦拉格与布泽尔赛季数据，布泽尔全面占优',
          comments: 0,
          likes: 0
        },
        {
          id: 2,
          title: '又打出来一个！14号秀卡特布莱恩特，马刺的争冠拼图？',
          comments: 11,
          likes: 5
        },
        {
          id: 3,
          title: '西亚卡姆：我不想被卷入摔跤的讨论范蜚，我几乎每场都上',
          comments: 15,
          likes: 3
        },
        {
          id: 4,
          title: 'SGA：我和保罗关系很亲密，他对我的职业生涯意义非凡',
          comments: 29,
          likes: 23
        }
      ]
    }
  },
  onLoad() {
    this.checkLogin()
  },
  methods: {
    checkLogin() {
      const userInfo = uni.getStorageSync('userInfo')
      if (userInfo) {
        this.isLogin = true
      }
    },
    goLogin() {
      uni.navigateTo({
        url: '/pages/login/login'
      })
    },
    goUserCenter() {
      uni.showActionSheet({
        itemList: ['个人信息', '退出登录'],
        success: (res) => {
          if (res.tapIndex === 0) {
            uni.showToast({
              title: '个人信息功能开发中',
              icon: 'none'
            })
          } else if (res.tapIndex === 1) {
            this.logout()
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
            uni.showToast({
              title: '已退出登录',
              icon: 'success'
            })
          }
        }
      })
    },
    goNewsDetail(id) {
      uni.navigateTo({
        url: `/pages/news/detail?id=${id}`
      })
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
  margin-bottom: 8rpx;
}

.score-sub {
  font-size: 22rpx;
  color: #999;
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
}

.arrow {
  color: #e74c3c;
  font-weight: bold;
}

.features {
  display: flex;
  justify-content: space-around;
  background-color: #fff;
  padding: 30rpx 0;
  margin: 15rpx 0;
}

.feature-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.feature-icon {
  font-size: 60rpx;
  margin-bottom: 10rpx;
  font-weight: bold;
  color: #e74c3c;
}

.feature-name {
  font-size: 24rpx;
  color: #333;
}

.news-container {
  background-color: #fff;
  margin: 15rpx 0;
}

.news-item {
  display: flex;
  padding: 20rpx;
  border-bottom: 1rpx solid #eee;
  position: relative;
}

.news-content {
  flex: 1;
  margin-right: 15rpx;
}

.news-title {
  font-size: 28rpx;
  color: #333;
  line-height: 1.4;
  margin-bottom: 10rpx;
}

.news-meta {
  display: flex;
  font-size: 22rpx;
  color: #999;
}

.comment-count::before {
  content: '评 ';
}

.like-count::before {
  content: '赞 ';
  margin-left: 15rpx;
}

.news-image {
  width: 100rpx;
  height: 80rpx;
  border-radius: 4rpx;
  background-color: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40rpx;
  color: #999;
}

.news-tag {
  position: absolute;
  top: 20rpx;
  right: 20rpx;
  background-color: #e74c3c;
  color: white;
  padding: 4rpx 10rpx;
  border-radius: 3rpx;
  font-size: 20rpx;
}

.recommend-section {
  background-color: #fff;
  margin: 15rpx 0;
  padding: 20rpx;
}

.recommend-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.recommend-item {
  display: flex;
  padding: 20rpx;
  background-color: #f9f9f9;
  border-radius: 6rpx;
  align-items: flex-start;
}

.recommend-label {
  background-color: #e74c3c;
  color: white;
  padding: 4rpx 10rpx;
  border-radius: 3rpx;
  font-size: 20rpx;
  margin-right: 15rpx;
  white-space: nowrap;
  margin-top: 5rpx;
}

.recommend-content {
  flex: 1;
  margin-right: 15rpx;
}

.recommend-text {
  font-size: 28rpx;
  color: #333;
  line-height: 1.4;
  margin-bottom: 10rpx;
}

.recommend-meta {
  display: flex;
  font-size: 22rpx;
  color: #999;
  gap: 20rpx;
}

.recommend-image {
  width: 100rpx;
  height: 80rpx;
  border-radius: 4rpx;
  object-fit: cover;
}
</style>