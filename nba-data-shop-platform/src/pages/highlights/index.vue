<template>
  <view class="highlights-page">
    <!-- 顶部横幅 -->
    <view class="banner">
      <view class="banner-content">
        <text class="banner-icon">🎬</text>
        <view class="banner-text">
          <text class="banner-title">精彩回放</text>
          <text class="banner-subtitle">NBA经典瞬间</text>
        </view>
      </view>
    </view>

    <view class="highlights-list">
      <view 
        v-for="item in highlights" 
        :key="item.id" 
        class="highlight-item"
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
          <view class="duration">{{ formatDuration(item.duration) }}</view>
          <view class="play-icon">▶</view>
        </view>
        
        <view class="info">
          <text class="highlight-title">{{ item.title }}</text>
          <text class="teams">{{ item.teams }}</text>
          <view class="meta">
            <text class="date">{{ item.match_date }}</text>
            <text class="views">{{ item.views }} 次观看</text>
          </view>
        </view>
      </view>
    </view>

    <view v-if="highlights.length === 0" class="empty">
      <text>暂无精彩回放</text>
    </view>

    <!-- 视频播放弹窗 -->
    <view v-if="showPlayer" class="video-modal" @click="closePlayer" @touchmove.stop.prevent>
      <view class="modal-content" @click.stop @touchmove.stop>
        <view class="modal-header">
          <text class="modal-title">{{ currentVideo.title }}</text>
          <text class="close-btn" @click="closePlayer">✕</text>
        </view>
        <view class="video-container">
          <video 
            :src="currentVideo.video_full_url"
            controls
            autoplay
            class="video-player"
            @play="onVideoPlay"
            :enable-progress-gesture="true"
            :show-progress="true"
            :show-fullscreen-btn="true"
            :show-play-btn="true"
            :show-center-play-btn="true"
          />
        </view>
        <view class="video-info">
          <text class="video-teams">{{ currentVideo.teams }}</text>
          <text class="video-desc">{{ currentVideo.description }}</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import { getHighlightList, incrementViews } from '@/api/highlight'

export default {
  data() {
    return {
      highlights: [],
      showPlayer: false,
      currentVideo: {}
    }
  },
  
  onLoad() {
    this.loadHighlights()
  },
  
  methods: {
    async loadHighlights() {
      try {
        const res = await getHighlightList()
        // Django REST framework 直接返回数组
        this.highlights = Array.isArray(res) ? res : (res.data || [])
      } catch (error) {
        console.error('加载失败', error)
        uni.showToast({
          title: '加载失败',
          icon: 'none'
        })
      }
    },
    
    playVideo(item) {
      this.currentVideo = item
      this.showPlayer = true
    },
    
    closePlayer() {
      this.showPlayer = false
      this.currentVideo = {}
    },
    
    async onVideoPlay() {
      try {
        await incrementViews(this.currentVideo.id)
        const index = this.highlights.findIndex(h => h.id === this.currentVideo.id)
        if (index !== -1) {
          this.highlights[index].views++
        }
      } catch (error) {
        console.error('增加观看次数失败', error)
      }
    },
    
    formatDuration(seconds) {
      if (!seconds) return '00:00'
      const mins = Math.floor(seconds / 60)
      const secs = seconds % 60
      return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`
    }
  }
}
</script>

<style scoped>
.highlights-page {
  min-height: 100vh;
  background: #f5f5f5;
}

.banner {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 60rpx 40rpx;
}

.banner-content {
  display: flex;
  align-items: center;
  gap: 24rpx;
}

.banner-icon {
  font-size: 80rpx;
  filter: drop-shadow(0 4rpx 8rpx rgba(0, 0, 0, 0.2));
}

.banner-text {
  display: flex;
  flex-direction: column;
  gap: 8rpx;
}

.banner-title {
  font-size: 48rpx;
  font-weight: bold;
  color: #fff;
  text-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.2);
}

.banner-subtitle {
  font-size: 28rpx;
  color: rgba(255, 255, 255, 0.9);
}

.highlights-list {
  padding: 20rpx;
}

.highlight-item {
  background: #fff;
  border-radius: 12rpx;
  margin-bottom: 20rpx;
  overflow: hidden;
}

.video-cover {
  position: relative;
  width: 100%;
  height: 400rpx;
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
  font-size: 80rpx;
  color: rgba(255, 255, 255, 0.8);
}

.duration {
  position: absolute;
  bottom: 20rpx;
  right: 20rpx;
  background: rgba(0, 0, 0, 0.7);
  color: #fff;
  padding: 8rpx 16rpx;
  border-radius: 8rpx;
  font-size: 24rpx;
}

.play-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100rpx;
  height: 100rpx;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40rpx;
  color: #667eea;
}

.info {
  padding: 24rpx;
}

.highlight-title {
  display: block;
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 12rpx;
}

.teams {
  display: block;
  font-size: 28rpx;
  color: #667eea;
  font-weight: 500;
  margin-bottom: 16rpx;
}

.meta {
  display: flex;
  justify-content: space-between;
  font-size: 24rpx;
  color: #999;
}

.empty {
  text-align: center;
  padding: 100rpx 0;
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
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24rpx;
  border-bottom: 1px solid #eee;
  flex-shrink: 0;
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

.video-container {
  width: 100%;
  background: #000;
  position: relative;
  flex-shrink: 0;
}

.video-player {
  width: 100%;
  height: 400rpx;
  background: #000;
}

.video-info {
  padding: 24rpx;
  flex-shrink: 0;
  overflow-y: auto;
}

.video-teams {
  display: block;
  font-size: 28rpx;
  color: #667eea;
  margin-bottom: 12rpx;
}

.video-desc {
  display: block;
  font-size: 26rpx;
  color: #666;
  line-height: 1.6;
}
</style>
