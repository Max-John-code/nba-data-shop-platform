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
      >
        <view class="video-cover" @click="playVideo(item)">
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
            <text class="views">👁️ {{ item.views }}</text>
          </view>
          
          <!-- 点赞和收藏按钮 -->
          <view class="actions">
            <button 
              class="action-btn like-btn" 
              :class="{ active: item.is_liked }" 
              @click="toggleLike(item)"
            >
              <text class="icon">{{ item.is_liked ? '❤️' : '🤍' }}</text>
              <text class="count">{{ item.likes || 0 }}</text>
            </button>
            <button 
              class="action-btn favorite-btn" 
              :class="{ active: item.is_favorited }" 
              @click="toggleFavorite(item)"
            >
              <text class="icon">{{ item.is_favorited ? '⭐' : '☆' }}</text>
              <text class="count">{{ item.favorites || 0 }}</text>
            </button>
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
          
          <!-- 弹窗内的点赞收藏 -->
          <view class="modal-actions">
            <button 
              class="modal-action-btn like-btn" 
              :class="{ active: currentVideo.is_liked }" 
              @click="toggleLike(currentVideo)"
            >
              <text class="icon">{{ currentVideo.is_liked ? '❤️' : '🤍' }}</text>
              <text class="text">{{ currentVideo.is_liked ? '已点赞' : '点赞' }}</text>
              <text class="count">({{ currentVideo.likes || 0 }})</text>
            </button>
            <button 
              class="modal-action-btn favorite-btn" 
              :class="{ active: currentVideo.is_favorited }" 
              @click="toggleFavorite(currentVideo)"
            >
              <text class="icon">{{ currentVideo.is_favorited ? '⭐' : '☆' }}</text>
              <text class="text">{{ currentVideo.is_favorited ? '已收藏' : '收藏' }}</text>
              <text class="count">({{ currentVideo.favorites || 0 }})</text>
            </button>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import { getHighlightList, incrementViews } from '@/api/highlight'
import { likeHighlight, unlikeHighlight, favoriteHighlight, unfavoriteHighlight, getHighlightStatus } from '@/api/like'

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
        this.highlights = Array.isArray(res) ? res : (res.data || [])
        
        // 如果用户已登录,加载点赞收藏状态
        const token = uni.getStorageSync('token')
        if (token && this.highlights.length > 0) {
          await this.loadLikeStatus()
        }
      } catch (error) {
        console.error('加载失败', error)
        uni.showToast({
          title: '加载失败',
          icon: 'none'
        })
      }
    },
    
    async loadLikeStatus() {
      // 批量加载每个视频的点赞收藏状态
      for (let item of this.highlights) {
        try {
          const status = await getHighlightStatus(item.id)
          item.is_liked = status.is_liked
          item.is_favorited = status.is_favorited
          item.likes = status.likes
          item.favorites = status.favorites
        } catch (error) {
          console.error('加载状态失败', error)
        }
      }
      this.$forceUpdate()
    },
    
    async toggleLike(item) {
      const token = uni.getStorageSync('token')
      if (!token) {
        uni.showToast({
          title: '请先登录',
          icon: 'none'
        })
        return
      }
      
      try {
        if (item.is_liked) {
          await unlikeHighlight(item.id)
          item.is_liked = false
          item.likes = Math.max(0, (item.likes || 0) - 1)
          uni.showToast({
            title: '取消点赞',
            icon: 'none'
          })
        } else {
          await likeHighlight(item.id)
          item.is_liked = true
          item.likes = (item.likes || 0) + 1
          uni.showToast({
            title: '点赞成功',
            icon: 'success'
          })
        }
        this.$forceUpdate()
      } catch (error) {
        console.error('点赞操作失败', error)
        uni.showToast({
          title: '操作失败，请重试',
          icon: 'none'
        })
      }
    },
    
    async toggleFavorite(item) {
      const token = uni.getStorageSync('token')
      if (!token) {
        uni.showToast({
          title: '请先登录',
          icon: 'none'
        })
        return
      }
      
      try {
        if (item.is_favorited) {
          await unfavoriteHighlight(item.id)
          item.is_favorited = false
          item.favorites = Math.max(0, (item.favorites || 0) - 1)
          uni.showToast({
            title: '取消收藏',
            icon: 'none'
          })
        } else {
          await favoriteHighlight(item.id)
          item.is_favorited = true
          item.favorites = (item.favorites || 0) + 1
          uni.showToast({
            title: '收藏成功',
            icon: 'success'
          })
        }
        this.$forceUpdate()
      } catch (error) {
        console.error('收藏操作失败', error)
        uni.showToast({
          title: '操作失败，请重试',
          icon: 'none'
        })
      }
    },
    
    playVideo(item) {
      this.currentVideo = { ...item }
      this.showPlayer = true
    },
    
    closePlayer() {
      // 同步当前视频的状态回列表
      const index = this.highlights.findIndex(h => h.id === this.currentVideo.id)
      if (index !== -1) {
        this.highlights[index].is_liked = this.currentVideo.is_liked
        this.highlights[index].is_favorited = this.currentVideo.is_favorited
        this.highlights[index].likes = this.currentVideo.likes
        this.highlights[index].favorites = this.currentVideo.favorites
      }
      
      this.showPlayer = false
      this.currentVideo = {}
    },
    
    async onVideoPlay() {
      try {
        await incrementViews(this.currentVideo.id)
        this.currentVideo.views++
        const index = this.highlights.findIndex(h => h.id === this.currentVideo.id)
        if (index !== -1) {
          this.highlights[index].views = this.currentVideo.views
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
  margin-bottom: 16rpx;
}

.actions {
  display: flex;
  gap: 16rpx;
  margin-top: 16rpx;
}

.action-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8rpx;
  padding: 16rpx;
  background: #f5f5f5;
  border: none;
  border-radius: 8rpx;
  font-size: 26rpx;
  color: #666;
  transition: all 0.3s;
}

.action-btn.active {
  background: linear-gradient(135deg, #fff5f5 0%, #ffe5e5 100%);
}

.action-btn.like-btn.active {
  color: #ff4d4f;
}

.action-btn.favorite-btn.active {
  color: #faad14;
  background: linear-gradient(135deg, #fffbf0 0%, #fff7e6 100%);
}

.action-btn .icon {
  font-size: 32rpx;
}

.action-btn .count {
  font-size: 24rpx;
  font-weight: bold;
}

.modal-actions {
  display: flex;
  gap: 16rpx;
  margin-top: 24rpx;
  padding-top: 24rpx;
  border-top: 1px solid #eee;
}

.modal-action-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8rpx;
  padding: 20rpx;
  background: #f5f5f5;
  border: none;
  border-radius: 12rpx;
  font-size: 28rpx;
  color: #666;
  transition: all 0.3s;
}

.modal-action-btn.active {
  background: linear-gradient(135deg, #fff5f5 0%, #ffe5e5 100%);
}

.modal-action-btn.like-btn.active {
  color: #ff4d4f;
}

.modal-action-btn.favorite-btn.active {
  color: #faad14;
  background: linear-gradient(135deg, #fffbf0 0%, #fff7e6 100%);
}

.modal-action-btn .icon {
  font-size: 36rpx;
}

.modal-action-btn .text {
  font-weight: 500;
}

.modal-action-btn .count {
  font-size: 24rpx;
  opacity: 0.8;
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
