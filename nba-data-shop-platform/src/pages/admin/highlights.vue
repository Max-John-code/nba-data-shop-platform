<template>
  <view class="admin-highlights">
    <view class="header">
      <view class="back-btn" @click="goBack">
        <text class="back-icon">←</text>
      </view>
      <text class="title">精彩回放管理</text>
    </view>

    <!-- 统计卡片 -->
    <view class="stats-container">
      <view class="stat-card">
        <text class="stat-number">{{ totalVideos }}</text>
        <text class="stat-label">总视频</text>
      </view>
      <view class="stat-card">
        <text class="stat-number">{{ activeVideos }}</text>
        <text class="stat-label">已显示</text>
      </view>
      <view class="stat-card">
        <text class="stat-number">{{ totalViews }}</text>
        <text class="stat-label">总观看</text>
      </view>
    </view>

    <!-- 添加视频按钮 -->
    <view class="add-btn-container">
      <button class="add-btn" @click="goToForm">
        <text class="add-icon">+</text>
        <text>添加视频</text>
      </button>
    </view>

    <!-- 视频列表 -->
    <view class="video-list">
      <view v-for="item in highlights" :key="item.id" class="video-item">
        <image 
          :src="item.cover_full_url || '/static/logo.png'" 
          class="video-thumbnail"
          mode="aspectFill"
        />
        
        <view class="video-info">
          <text class="video-title">{{ item.title }}</text>
          <text class="video-meta">{{ item.teams }} · {{ formatDuration(item.duration) }}</text>
          <view class="video-stats">
            <text class="views-icon">👁</text>
            <text class="views-count">{{ item.views }}</text>
          </view>
        </view>

        <view class="video-status">
          <view :class="['status-badge', item.is_active ? 'active' : 'inactive']">
            {{ item.is_active ? '已显示' : '已隐藏' }}
          </view>
        </view>

        <view class="video-actions">
          <button class="action-btn edit-btn" @click="goToEdit(item.id)">编辑</button>
          <button class="action-btn delete-btn" @click="deleteItem(item)">删除</button>
        </view>
      </view>
    </view>

    <view v-if="highlights.length === 0" class="empty">
      <text>暂无视频</text>
    </view>
  </view>
</template>

<script>
import { getHighlightList, deleteHighlight } from '@/api/highlight'

export default {
  data() {
    return {
      highlights: [],
      totalVideos: 0,
      activeVideos: 0,
      totalViews: 0
    }
  },

  onLoad() {
    this.loadData()
  },

  methods: {
    async loadData() {
      try {
        const res = await getHighlightList()
        // Django REST framework 直接返回数组，不是 {data: []} 格式
        this.highlights = Array.isArray(res) ? res : (res.data || [])
        this.calculateStats()
      } catch (error) {
        console.error('加载失败', error)
        uni.showToast({
          title: '加载失败',
          icon: 'none'
        })
      }
    },

    calculateStats() {
      this.totalVideos = this.highlights.length
      this.activeVideos = this.highlights.filter(h => h.is_active).length
      this.totalViews = this.highlights.reduce((sum, h) => sum + h.views, 0)
    },

    goToForm() {
      uni.navigateTo({
        url: '/pages/admin/highlight-form'
      })
    },

    goToEdit(id) {
      uni.navigateTo({
        url: `/pages/admin/highlight-form?id=${id}`
      })
    },

    deleteItem(item) {
      uni.showModal({
        title: '确认删除',
        content: `确定要删除"${item.title}"吗？`,
        success: async (res) => {
          if (res.confirm) {
            try {
              await deleteHighlight(item.id)
              uni.showToast({
                title: '删除成功',
                icon: 'success'
              })
              this.loadData()
            } catch (error) {
              uni.showToast({
                title: '删除失败',
                icon: 'none'
              })
            }
          }
        }
      })
    },

    formatDuration(seconds) {
      if (!seconds) return '00:00'
      const mins = Math.floor(seconds / 60)
      const secs = seconds % 60
      return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`
    },

    goBack() {
      uni.navigateBack()
    }
  }
}
</script>

<style scoped>
.admin-highlights {
  min-height: 100vh;
  background: #f5f5f5;
  padding-bottom: 30rpx;
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

.stats-container {
  display: flex;
  padding: 30rpx 20rpx;
  gap: 20rpx;
}

.stat-card {
  flex: 1;
  background: #fff;
  border-radius: 16rpx;
  padding: 30rpx 20rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.08);
}

.stat-number {
  font-size: 48rpx;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 8rpx;
}

.stat-label {
  font-size: 24rpx;
  color: #999;
}

.add-btn-container {
  padding: 0 20rpx 20rpx;
}

.add-btn {
  width: 100%;
  background: #667eea;
  color: #fff;
  border: none;
  border-radius: 16rpx;
  padding: 30rpx;
  font-size: 32rpx;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12rpx;
  box-shadow: 0 8rpx 20rpx rgba(102, 126, 234, 0.3);
}

.add-icon {
  font-size: 40rpx;
}

.video-list {
  padding: 0 20rpx;
}

.video-item {
  background: #fff;
  border-radius: 16rpx;
  margin-bottom: 20rpx;
  padding: 20rpx;
  display: flex;
  align-items: center;
  gap: 20rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.08);
}

.video-thumbnail {
  width: 160rpx;
  height: 120rpx;
  border-radius: 12rpx;
  background: #f0f0f0;
}

.video-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8rpx;
}

.video-title {
  font-size: 30rpx;
  font-weight: bold;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.video-meta {
  font-size: 24rpx;
  color: #999;
}

.video-stats {
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.views-icon {
  font-size: 24rpx;
}

.views-count {
  font-size: 24rpx;
  color: #666;
}

.video-status {
  margin-right: 12rpx;
}

.status-badge {
  padding: 8rpx 20rpx;
  border-radius: 20rpx;
  font-size: 24rpx;
}

.status-badge.active {
  background: #d4edda;
  color: #155724;
}

.status-badge.inactive {
  background: #f8d7da;
  color: #721c24;
}

.video-actions {
  display: flex;
  flex-direction: column;
  gap: 12rpx;
}

.action-btn {
  padding: 12rpx 24rpx;
  border-radius: 8rpx;
  font-size: 24rpx;
  border: none;
  min-width: 100rpx;
}

.edit-btn {
  background: #667eea;
  color: #fff;
}

.delete-btn {
  background: #ff6b6b;
  color: #fff;
}

.empty {
  text-align: center;
  padding: 100rpx 0;
  color: #999;
  font-size: 28rpx;
}
</style>
