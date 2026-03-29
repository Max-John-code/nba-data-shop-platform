<template>
  <view class="container">
    <view class="form">
      <view class="form-item">
        <view class="label">商品名称 *</view>
        <input v-model="formData.name" placeholder="请输入商品名称" class="input" />
      </view>

      <view class="form-item">
        <view class="label">商品描述</view>
        <textarea v-model="formData.description" placeholder="请输入商品描述" class="textarea" />
      </view>

      <view class="form-item">
        <view class="label">商品图片</view>
        <view class="image-upload" @click="chooseImage">
          <image v-if="formData.image" :src="formData.image" mode="aspectFill" class="upload-image" />
          <view v-else class="upload-placeholder">
            <text class="upload-icon">📷</text>
            <text class="upload-text">点击上传图片</text>
          </view>
        </view>
      </view>

      <view class="form-item">
        <view class="label">价格 *</view>
        <input v-model.number="formData.price" type="digit" placeholder="请输入价格" class="input" />
      </view>

      <view class="form-item">
        <view class="label">库存 *</view>
        <input v-model.number="formData.stock" type="number" placeholder="请输入库存" class="input" />
      </view>

      <view class="form-item">
        <view class="label">分类 *</view>
        <picker :value="categoryIndex" :range="categoryOptions" range-key="label" @change="onCategoryChange">
          <view class="picker-input">{{ categoryOptions[categoryIndex].label }}</view>
        </picker>
      </view>

      <view class="form-item">
        <view class="label">关联球星</view>
        <input v-model="formData.player_name" placeholder="请输入球星名字（可选）" class="input" />
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
      <view class="btn submit-btn" @click="submitProduct">{{ isEdit ? '保存' : '添加' }}</view>
    </view>
  </view>
</template>

<script>
import { getProductDetail, addProduct, updateProduct } from '@/api/shop'

export default {
  data() {
    return {
      isEdit: false,
      productId: null,
      formData: {
        name: '',
        description: '',
        image: '',
        price: '',
        stock: 0,
        category: 'jersey',
        player_name: '',
        status: 'active'
      },
      categoryOptions: [
        { value: 'jersey', label: '球衣' },
        { value: 'shoes', label: '球鞋' },
        { value: 'cap', label: '帽子' },
        { value: 'other', label: '其他' }
      ],
      categoryIndex: 0,
      statusOptions: [
        { value: 'active', label: '上架' },
        { value: 'inactive', label: '下架' }
      ],
      statusIndex: 0
    }
  },
  onLoad(options) {
    if (options.id) {
      this.isEdit = true
      this.productId = options.id
      this.loadProduct()
    }
  },
  methods: {
    loadProduct() {
      uni.showLoading({ title: '加载中...' })
      
      getProductDetail(this.productId).then(res => {
        if (res.code === 200) {
          this.formData = res.data
          this.categoryIndex = this.categoryOptions.findIndex(item => item.value === res.data.category)
          this.statusIndex = this.statusOptions.findIndex(item => item.value === res.data.status)
        }
      }).catch(err => {
        console.error('加载商品失败', err)
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
    onCategoryChange(e) {
      this.categoryIndex = e.detail.value
      this.formData.category = this.categoryOptions[e.detail.value].value
    },
    onStatusChange(e) {
      this.statusIndex = e.detail.value
      this.formData.status = this.statusOptions[e.detail.value].value
    },
    submitProduct() {
      if (!this.formData.name) {
        uni.showToast({ title: '请输入商品名称', icon: 'none' })
        return
      }
      if (!this.formData.price) {
        uni.showToast({ title: '请输入价格', icon: 'none' })
        return
      }

      uni.showLoading({ title: '提交中...' })
      
      const apiCall = this.isEdit 
        ? updateProduct(this.productId, this.formData)
        : addProduct(this.formData)
      
      apiCall.then(res => {
        if (res.code === 200) {
          uni.showToast({ 
            title: this.isEdit ? '更新成功' : '添加成功', 
            icon: 'success' 
          })
          setTimeout(() => {
            uni.navigateBack()
          }, 1500)
        }
      }).catch(err => {
        console.error('提交失败', err)
        uni.showToast({ title: '提交失败', icon: 'none' })
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
  background-color: #667eea;
  color: #fff;
}
</style>
