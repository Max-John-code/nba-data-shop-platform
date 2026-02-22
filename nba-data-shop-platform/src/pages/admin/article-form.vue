<template>
  <view class="container">
    <view class="header">
      <view class="title">{{ isEdit ? '编辑文章' : '发表文章' }}</view>
    </view>

    <view class="form-container">
      <view class="form-item">
        <view class="form-label">文章标题 *</view>
        <input v-model="formData.title" placeholder="请输入文章标题" class="form-input" />
      </view>

      <view class="form-item">
        <view class="form-label">文章内容 *</view>
        <textarea 
          v-model="formData.content" 
          placeholder="请输入文章内容" 
          class="form-textarea"
          :maxlength="-1" />
      </view>

      <view class="form-item">
        <view class="form-label">文章图片（可选）</view>
        <view class="image-upload" @click="chooseImage">
          <image v-if="formData.image" :src="formData.image" mode="aspectFill" class="upload-image" />
          <view v-else class="upload-placeholder">
            <text class="upload-icon">📷</text>
            <text class="upload-text">点击上传图片</text>
          </view>
        </view>
      </view>
    </view>

    <view class="footer-btns">
      <view class="btn cancel-btn" @click="goBack">取消</view>
      <view class="btn submit-btn" @click="submitArticle">{{ isEdit ? '保存' : '发表' }}</view>
    </view>
  </view>
</template>

<script>
import { publishArticle, updateArticle, getArticleDetail } from '@/api/forum'

export default {
  data() {
    return {
      isEdit: false,
      articleId: null,
      formData: {
        title: '',
        content: '',
        image: ''
      }
    }
  },
  onLoad(options) {
    if (options.id) {
      this.isEdit = true
      this.articleId = options.id
      this.loadArticleDetail()
    }
  },
  methods: {
    loadArticleDetail() {
      uni.showLoading({ title: '加载中...' })
      
      getArticleDetail(this.articleId).then(res => {
        if (res.code === 200) {
          this.formData = {
            title: res.data.title,
            content: res.data.content,
            image: res.data.image || ''
          }
        }
      }).catch(err => {
        console.error('加载文章详情失败', err)
      }).finally(() => {
        uni.hideLoading()
      })
    },
    chooseImage() {
      uni.chooseImage({
        count: 1,
        sizeType: ['compressed'],
        success: (res) => {
          const tempFilePath = res.tempFilePaths[0]
          
          // 检查文件大小（如果可用）
          if (res.tempFiles && res.tempFiles[0]) {
            const fileSize = res.tempFiles[0].size
            // 限制为5MB
            if (fileSize > 5 * 1024 * 1024) {
              uni.showToast({
                title: '图片过大，请选择小于5MB的图片',
                icon: 'none',
                duration: 2000
              })
              return
            }
          }
          
          // #ifdef H5
          this.convertToBase64H5(tempFilePath)
          // #endif
          
          // #ifndef H5
          this.convertToBase64(tempFilePath)
          // #endif
        }
      })
    },
    convertToBase64H5(blobUrl) {
      const xhr = new XMLHttpRequest()
      xhr.open('GET', blobUrl, true)
      xhr.responseType = 'blob'
      
      xhr.onload = () => {
        if (xhr.status === 200) {
          const blob = xhr.response
          const reader = new FileReader()
          
          reader.onloadend = () => {
            this.formData.image = reader.result
          }
          
          reader.readAsDataURL(blob)
        }
      }
      
      xhr.send()
    },
    convertToBase64(filePath) {
      uni.getFileSystemManager().readFile({
        filePath: filePath,
        encoding: 'base64',
        success: (fileRes) => {
          this.formData.image = 'data:image/jpeg;base64,' + fileRes.data
        }
      })
    },
    submitArticle() {
      if (!this.formData.title) {
        uni.showToast({ title: '请输入文章标题', icon: 'none' })
        return
      }
      
      if (!this.formData.content) {
        uni.showToast({ title: '请输入文章内容', icon: 'none' })
        return
      }
      
      console.log('提交数据:', {
        title: this.formData.title,
        content: this.formData.content.substring(0, 50) + '...',
        imageLength: this.formData.image ? this.formData.image.length : 0,
        imagePrefix: this.formData.image ? this.formData.image.substring(0, 50) : 'no image'
      })
      
      uni.showLoading({ title: '提交中...' })
      
      const apiCall = this.isEdit 
        ? updateArticle(this.articleId, this.formData)
        : publishArticle(this.formData)
      
      apiCall.then(res => {
        console.log('提交成功响应:', res)
        if (res.code === 200) {
          uni.showToast({ 
            title: this.isEdit ? '更新成功' : '发表成功', 
            icon: 'success' 
          })
          setTimeout(() => {
            uni.navigateBack()
          }, 1500)
        } else {
          console.error('提交失败，返回码不是200:', res)
          uni.showToast({ 
            title: res.message || '提交失败', 
            icon: 'none',
            duration: 3000
          })
        }
      }).catch(err => {
        console.error('提交失败详细错误:', err)
        console.error('错误响应:', err.response)
        console.error('错误数据:', err.data)
        
        let errorMsg = '提交失败'
        if (err.data && err.data.message) {
          errorMsg = err.data.message
        } else if (err.message) {
          errorMsg = err.message
        }
        
        uni.showToast({ 
          title: errorMsg, 
          icon: 'none',
          duration: 3000
        })
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
  padding-bottom: 120rpx;
}

.header {
  background-color: #fff;
  padding: 30rpx;
  border-bottom: 1rpx solid #eee;
}

.title {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
}

.form-container {
  padding: 20rpx;
}

.form-item {
  background-color: #fff;
  border-radius: 12rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
}

.form-label {
  font-size: 30rpx;
  color: #333;
  margin-bottom: 18rpx;
  font-weight: 500;
}

.form-input {
  width: 100%;
  padding: 25rpx 20rpx;
  border: 1rpx solid #ddd;
  border-radius: 8rpx;
  font-size: 30rpx;
  background-color: #fff;
  box-sizing: border-box;
  min-height: 80rpx;
}

.form-textarea {
  width: 100%;
  min-height: 400rpx;
  padding: 25rpx 20rpx;
  border: 1rpx solid #ddd;
  border-radius: 8rpx;
  font-size: 30rpx;
  background-color: #fff;
  box-sizing: border-box;
  line-height: 1.6;
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
  background-color: #e74c3c;
  color: #fff;
}
</style>
