<template>
  <view class="container">
    <view class="form">
      <view class="form-item">
        <view class="label">标题 *</view>
        <input v-model="formData.title" placeholder="请输入标题" class="input" />
      </view>

      <view class="form-item">
        <view class="label">对阵球队 *</view>
        <input v-model="formData.teams" placeholder="例如：湖人vs勇士" class="input" />
      </view>

      <view class="form-item">
        <view class="label">比赛日期 *</view>
        <picker mode="date" :value="formData.match_date" @change="onDateChange">
          <view class="picker-input">{{ formData.match_date || '请选择日期' }}</view>
        </picker>
      </view>

      <view class="form-item">
        <view class="label">视频文件 *</view>
        <view class="video-upload" @click="chooseVideo">
          <view v-if="formData.videoFile" class="video-info">
            <text class="video-icon">🎬</text>
            <view class="video-details">
              <text class="video-name">{{ formData.videoFile.name }}</text>
              <text class="video-duration">时长：{{ formatDuration(formData.duration) }}</text>
            </view>
            <text class="change-text">重新选择</text>
          </view>
          <view v-else class="upload-placeholder">
            <text class="upload-icon">📹</text>
            <text class="upload-text">点击选择视频</text>
            <text v-if="isEdit && formData.duration" class="current-duration">当前时长：{{ formatDuration(formData.duration) }}</text>
          </view>
        </view>
      </view>

      <view class="form-item" v-if="formData.duration > 0">
        <view class="label">视频时长</view>
        <view class="duration-display">
          <text class="duration-value">{{ formatDuration(formData.duration) }}</text>
          <text class="duration-seconds">({{ formData.duration }} 秒)</text>
        </view>
      </view>

      <view class="form-item">
        <view class="label">封面图片</view>
        <view class="image-upload" @click="chooseCover">
          <image v-if="formData.coverPreview" :src="formData.coverPreview" mode="aspectFill" class="upload-image" />
          <view v-else class="upload-placeholder">
            <text class="upload-icon">🖼️</text>
            <text class="upload-text">点击上传封面</text>
          </view>
        </view>
      </view>

      <view class="form-item">
        <view class="label">描述</view>
        <textarea v-model="formData.description" placeholder="请输入精彩回放描述" class="textarea" />
      </view>

      <view class="form-item">
        <view class="label">状态 *</view>
        <picker :value="statusIndex" :range="statusOptions" range-key="label" @change="onStatusChange">
          <view class="picker-input">{{ statusOptions[statusIndex].label }}</view>
        </picker>
      </view>
    </view>

    <view class="footer-btns">
      <view class="btn cancel-btn" @click="goBack">取消</view>
      <view class="btn submit-btn" @click="submitForm">{{ isEdit ? '保存' : '添加' }}</view>
    </view>
  </view>
</template>

<script>
import { getHighlightDetail } from '@/api/highlight'

export default {
  data() {
    return {
      isEdit: false,
      highlightId: null,
      formData: {
        title: '',
        teams: '',
        match_date: '',
        videoFile: null,
        coverFile: null,
        coverPreview: '',
        duration: 0,
        description: '',
        is_active: true
      },
      statusOptions: [
        { value: true, label: '显示' },
        { value: false, label: '隐藏' }
      ],
      statusIndex: 0
    }
  },

  onLoad(options) {
    if (options.id) {
      this.isEdit = true
      this.highlightId = options.id
      this.loadHighlight()
    }
  },

  methods: {
    async loadHighlight() {
      uni.showLoading({ title: '加载中...' })
      
      try {
        const res = await getHighlightDetail(this.highlightId)
        const data = res.data || res
        this.formData = {
          title: data.title,
          teams: data.teams,
          match_date: data.match_date,
          videoFile: null,
          coverFile: null,
          coverPreview: data.cover_full_url || '',
          duration: data.duration,
          description: data.description,
          is_active: data.is_active
        }
        this.statusIndex = data.is_active ? 0 : 1
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

    chooseVideo() {
      uni.chooseVideo({
        sourceType: ['album'],
        success: (res) => {
          this.formData.videoFile = {
            path: res.tempFilePath,
            name: res.tempFilePath.split('/').pop()
          }
          this.formData.duration = Math.floor(res.duration)
        }
      })
    },

    chooseCover() {
      uni.chooseImage({
        count: 1,
        sourceType: ['album'],
        success: (res) => {
          this.formData.coverFile = {
            path: res.tempFilePaths[0],
            name: res.tempFilePaths[0].split('/').pop()
          }
          this.formData.coverPreview = res.tempFilePaths[0]
        }
      })
    },

    onDateChange(e) {
      this.formData.match_date = e.detail.value
    },

    onStatusChange(e) {
      this.statusIndex = e.detail.value
      this.formData.is_active = this.statusOptions[e.detail.value].value
    },

    async submitForm() {
      if (!this.formData.title || !this.formData.teams || !this.formData.match_date) {
        uni.showToast({
          title: '请填写必填项',
          icon: 'none'
        })
        return
      }

      if (!this.isEdit && !this.formData.videoFile) {
        uni.showToast({
          title: '请选择视频文件',
          icon: 'none'
        })
        return
      }

      uni.showLoading({ title: '上传中...' })

      try {
        const token = uni.getStorageSync('token')
        
        if (this.formData.videoFile) {
          // 有视频文件，使用 uploadFile 上传
          const url = this.isEdit 
            ? `http://127.0.0.1:8000/api/highlights/${this.highlightId}/`
            : 'http://127.0.0.1:8000/api/highlights/'

          const formData = {
            title: this.formData.title,
            teams: this.formData.teams,
            match_date: this.formData.match_date,
            duration: this.formData.duration,
            description: this.formData.description || '',
            is_active: this.formData.is_active ? '1' : '0'
          }

          // 先上传视频
          uni.uploadFile({
            url: url,
            filePath: this.formData.videoFile.path,
            name: 'video',
            formData: formData,
            header: {
              'Authorization': `Token ${token}`
            },
            success: async (uploadRes) => {
              if (uploadRes.statusCode === 200 || uploadRes.statusCode === 201) {
                const data = JSON.parse(uploadRes.data)
                
                // 如果有封面，再上传封面
                if (this.formData.coverFile) {
                  await this.uploadCoverSeparately(data.id, token)
                } else {
                  this.handleSuccess()
                }
              } else {
                this.handleError()
              }
            },
            fail: () => {
              this.handleError()
            }
          })
        } else {
          // 没有视频文件，只更新其他信息（编辑模式）
          const url = `http://127.0.0.1:8000/api/highlights/${this.highlightId}/`
          const data = {
            title: this.formData.title,
            teams: this.formData.teams,
            match_date: this.formData.match_date,
            duration: this.formData.duration,
            description: this.formData.description || '',
            is_active: this.formData.is_active
          }

          uni.request({
            url: url,
            method: 'PUT',
            data: data,
            header: {
              'Authorization': `Token ${token}`,
              'Content-Type': 'application/json'
            },
            success: async (res) => {
              if (res.statusCode === 200) {
                // 如果有封面，上传封面
                if (this.formData.coverFile) {
                  await this.uploadCoverSeparately(this.highlightId, token)
                } else {
                  this.handleSuccess()
                }
              } else {
                this.handleError()
              }
            },
            fail: () => {
              this.handleError()
            }
          })
        }
      } catch (error) {
        this.handleError()
      }
    },

    uploadCoverSeparately(highlightId, token) {
      return new Promise((resolve, reject) => {
        uni.uploadFile({
          url: `http://127.0.0.1:8000/api/highlights/${highlightId}/upload_cover/`,
          filePath: this.formData.coverFile.path,
          name: 'cover_image',
          header: {
            'Authorization': `Token ${token}`
          },
          success: (res) => {
            if (res.statusCode === 200) {
              this.handleSuccess()
              resolve()
            } else {
              uni.hideLoading()
              uni.showToast({
                title: '封面上传失败',
                icon: 'none'
              })
              reject()
            }
          },
          fail: () => {
            uni.hideLoading()
            uni.showToast({
              title: '封面上传失败',
              icon: 'none'
            })
            reject()
          }
        })
      })
    },

    handleSuccess() {
      uni.hideLoading()
      uni.showToast({
        title: this.isEdit ? '更新成功' : '添加成功',
        icon: 'success'
      })
      setTimeout(() => {
        uni.navigateBack()
      }, 1500)
    },

    handleError() {
      uni.hideLoading()
      uni.showToast({
        title: '提交失败',
        icon: 'none'
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
.container {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 20rpx;
  padding-bottom: 120rpx;
}

.form {
  background-color: #fff;
  border-radius: 12rpx;
  padding: 30rpx;
}

.form-item {
  margin-bottom: 30rpx;
}

.label {
  font-size: 28rpx;
  color: #333;
  margin-bottom: 15rpx;
  font-weight: 500;
}

.input, .textarea, .picker-input {
  width: 100%;
  padding: 25rpx 20rpx;
  border: 1rpx solid #ddd;
  border-radius: 8rpx;
  font-size: 28rpx;
  box-sizing: border-box;
  min-height: 80rpx;
}

.textarea {
  min-height: 200rpx;
  line-height: 1.6;
}

.picker-input {
  background-color: #fff;
  display: flex;
  align-items: center;
  color: #333;
}

.video-upload {
  width: 100%;
  min-height: 150rpx;
  border-radius: 12rpx;
  border: 2rpx dashed #ddd;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #fafafa;
  padding: 20rpx;
}

.video-info {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 20rpx;
}

.video-icon {
  font-size: 60rpx;
}

.video-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8rpx;
}

.video-name {
  font-size: 26rpx;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.video-duration {
  font-size: 24rpx;
  color: #667eea;
  font-weight: bold;
}

.change-text {
  font-size: 24rpx;
  color: #667eea;
}

.image-upload {
  width: 100%;
  height: 400rpx;
  border-radius: 12rpx;
  border: 2rpx dashed #ddd;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background-color: #fafafa;
}

.upload-image {
  width: 100%;
  height: 100%;
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15rpx;
}

.upload-icon {
  font-size: 80rpx;
}

.upload-text {
  font-size: 26rpx;
  color: #999;
}

.current-duration {
  font-size: 24rpx;
  color: #667eea;
  margin-top: 8rpx;
}

.duration-display {
  width: 100%;
  padding: 25rpx 20rpx;
  border: 1rpx solid #ddd;
  border-radius: 8rpx;
  background-color: #f8f9fa;
  display: flex;
  align-items: center;
  gap: 12rpx;
}

.duration-value {
  font-size: 32rpx;
  font-weight: bold;
  color: #667eea;
}

.duration-seconds {
  font-size: 24rpx;
  color: #999;
}

.footer-btns {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  background-color: #fff;
  padding: 20rpx;
  border-top: 1rpx solid #eee;
  gap: 20rpx;
  z-index: 100;
}

.btn {
  flex: 1;
  padding: 25rpx 0;
  text-align: center;
  border-radius: 8rpx;
  font-size: 30rpx;
  font-weight: bold;
}

.cancel-btn {
  background-color: #f0f0f0;
  color: #666;
}

.submit-btn {
  background-color: #667eea;
  color: #fff;
}
</style>
