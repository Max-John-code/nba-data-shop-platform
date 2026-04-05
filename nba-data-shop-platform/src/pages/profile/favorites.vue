<template>
  <view class="favorites-page">
    <view class="header">
      <view class="back-btn" @click="goBack">
        <text class="back-icon">←</text>
      </view>
      <text class="title">我的收藏</text>
    </view>

    <!-- Tab切换 -->
    <view class="tabs">
      <view 
        v-for="tab in tabs" 
        :key="tab.key" 
        class="tab-item" 
        :class="{ active: currentTab === tab.key }"
        @click="switchTab(tab.key)"
      >
        <text class="tab-text">{{ tab.label }}</text>
      </view>
    </view>

    <!-- 视频列表 -->
    <view v-if="currentTab === 'liked-videos' || currentTab === 'favorited-videos'" class="video-list">
      <view 
        v-for="item in currentList" 
        :key="item.id" 
        class="video-item"
        @click="playVideo(item)"
      >
        <view class="video-cover">
          <image 
            v-if="item.cover_full_url" 
            :src="item.cover_full_url" 
            mode="aspectFill"
            class="cover-image"
          />
          <view v-else class="cover-placeholder">
            <text class="icon">▶</text>
          </view>
          <view class="play-icon">▶</view>
        </view>
        <view class="video-info">
          <text class="video-title">{{ item.title }}</text>
          <text class="video-teams">{{ item.teams }}</text>
          <view class="video-meta">
            <text class="views">👁️ {{ item.views }}</text>
            <text class="likes">❤️ {{ item.likes }}</text>
          </view>
        </view>
      </view>
      
      <view v-if="currentList.length === 0" class="empty">
        <text class="empty-icon">📭</text>
        <text class="empty-text">暂无内容</text>
      </view>
    </view>

    <!-- 文章列表 -->
    <view v-if="currentTab === 'liked-articles' || currentTab === 'favorited-articles'" class="article-list">
      <view 
        v-for="item in currentList" 
        :key="item.id" 
        class="article-item"
        @click="goToArticle(item.id)"
      >
        <view class="article-content">
          <text class="article-title">{{ item.title }}</text>
          <view class="article-meta">
            <text class="author">{{ item.author_name || '匿名' }}</text>
            <text class="views">👁️ {{ item.view_count }}</text>
            <text class="likes">❤️ {{ item.likes }}</text>
          </view>
        </view>
        <image 
          v-if="item.image" 
          :src="item.image" 
          mode="aspectFill"
          class="article-image"
        />
      </view>
      
      <view v-if="currentList.length === 0" class="empty">
        <text class="empty-icon">📭</text>
        <text class="empty-text">暂无内容</text>
      </view>
    </view>

    <!-- 视频播放弹窗 -->
    <view v-if="showPlayer" class="video-modal" @click="closePlayer">
      <view class="modal-content" @click.stop>
        <view class="modal-header">
          <text class="modal-title">{{ currentVideo.title }}</text>
          <text class="close-btn" @click="closePlayer">✕</text>
        </view>
        <video 
          :src="currentVideo.video_full_url"
          controls
          autoplay
          class="video-player"
        />
      </view>
    </view>
  </view>
</template>

<script>
import { getUserLikedHighlights, getUserFavoritedHighlights, getUserLikedArticles, getUserFavoritedArticles } from '@/api/like'

export default {
  data() {
    return {
      currentTab: 'favorited-videos',
      tabs: [
        { key: 'favorited-videos', label: '收藏的视频' },
        { key: 'liked-videos', label: '点赞的视频' },
        { key: 'favorited-articles', label: '收藏的文章' },
        { key: 'liked-articles', label: '点赞的文章' }
      ],
      likedVideos: [],
      favoritedVideos: [],
      likedArticles: [],
      favoritedArticles: [],
      showPlayer: false,
      currentVideo: {}
    }
  },
  
  computed: {
    currentList() {
      switch (this.currentTab) {
        case 'liked-videos':
          return this.likedVideos
        case 'favorited-videos':
          return this.favoritedVideos
        case 'liked-articles':
          return this.likedArticles
        case 'favorited-articles':
          return this.favoritedArticles
        default:
          return []
      }
    }
  },
  
  onLoad() {
    this.loadData()
  },
  
  methods: {
    async loadData() {
      uni.showLoading({ title: '加载中...' })
      
      try {
        const [likedVideos, favoritedVideos, likedArticles, favoritedArticles] = await Promise.all([
          getUserLikedHighlights(),
          getUserFavoritedHighlights(),
          getUserLikedArticles(),
          getUserFavoritedArticles()
        ])
        
        this.likedVideos = Array.isArray(likedVideos) ? likedVideos : []
        this.favoritedVideos = Array.isArray(favoritedVideos) ? favoritedVideos : []
        this.likedArticles = Array.isArray(likedArticles) ? likedArticles : []
        this.favoritedArticles = Array.isArray(favoritedArticles) ? favoritedArticles : []
      } catch (error) {
        console.error('加载失败', error)
        uni.showToast({
          title: '加载失败',
          icon: 'none'
        })
      } finally {
        uni.hideLoading()
      }
    },
    
    switchTab(key) {
      this.currentTab = key
    },
    
    playVideo(item) {
      this.currentVideo = item
      this.showPlayer = true
    },
    
    closePlayer() {
      this.showPlayer = false
      this.currentVideo = {}
    },
    
    goToArticle(id) {
      uni.navigateTo({
        url: `/pages/forum/detail?id=${id}`
      })
    },
    
    goBack() {
      uni.navigateBack()
    }
  }
}
</script>

<style scoped>
.favorites-page {
  min-height: 100vh;
  background: #f5f5f5;
}

.header {
  position: relative;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 30rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.back-btn {
  position: absolute;
  left: 30rpx;
  width: 60rpx;
  height: 60rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.back-icon {
  font-size: 40rpx;
  color: #fff;
}

.title {
  font-size: 36rpx;
  font-weight: bold;
  color: #fff;
}

.tabs {
  display: flex;
  background: #fff;
  border-bottom: 1px solid #eee;
}

.tab-item {
  flex: 1;
  padding: 24rpx;
  text-align: center;
  position: relative;
}

.tab-item.active {
  color: #667eea;
}

.tab-item.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 60rpx;
  height: 4rpx;
  background: #667eea;
  border-radius: 2rpx;
}

.tab-text {
  font-size: 28rpx;
}

.video-list {
  padding: 20rpx;
}

.video-item {
  display: flex;
  background: #fff;
  border-radius: 12rpx;
  margin-bottom: 20rpx;
  overflow: hidden;
}

.video-cover {
  position: relative;
  width: 240rpx;
  height: 180rpx;
  flex-shrink: 0;
  background: #000;
}

.cover-image {
  width: 100%;
  height: 100%;
}

.cover-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.cover-placeholder .icon {
  font-size: 48rpx;
  color: rgba(255, 255, 255, 0.8);
}

.play-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 60rpx;
  height: 60rpx;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24rpx;
  color: #667eea;
}

.video-info {
  flex: 1;
  padding: 20rpx;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.video-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.video-teams {
  font-size: 24rpx;
  color: #667eea;
  margin-top: 8rpx;
}

.video-meta {
  display: flex;
  gap: 24rpx;
  font-size: 22rpx;
  color: #999;
  margin-top: 8rpx;
}

.article-list {
  padding: 20rpx;
}

.article-item {
  display: flex;
  background: #fff;
  border-radius: 12rpx;
  padding: 24rpx;
  margin-bottom: 20rpx;
}

.article-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.article-title {
  font-size: 30rpx;
  font-weight: bold;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  margin-bottom: 16rpx;
}

.article-meta {
  display: flex;
  gap: 24rpx;
  font-size: 22rpx;
  color: #999;
}

.article-image {
  width: 180rpx;
  height: 120rpx;
  border-radius: 8rpx;
  margin-left: 20rpx;
  flex-shrink: 0;
}

.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 120rpx 0;
}

.empty-icon {
  font-size: 120rpx;
  margin-bottom: 24rpx;
}

.empty-text {
  font-size: 28rpx;
  color: #999;
}

.video-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  width: 90%;
  max-width: 800rpx;
  background: #fff;
  border-radius: 16rpx;
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24rpx;
  border-bottom: 1px solid #eee;
}

.modal-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  flex: 1;
}

.close-btn {
  font-size: 40rpx;
  color: #999;
  padding: 0 12rpx;
}

.video-player {
  width: 100%;
  height: 400rpx;
  background: #000;
}
</style>
