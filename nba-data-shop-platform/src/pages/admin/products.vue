<template>
  <view class="container">
    <view class="header">
      <view class="title">商品管理</view>
      <view class="actions">
        <view class="add-btn" @click="addProduct">添加商品</view>
      </view>
    </view>

    <view class="stats">
      <view class="stat-item">
        <view class="stat-value">{{ total }}</view>
        <view class="stat-label">总商品数</view>
      </view>
      <view class="stat-item">
        <view class="stat-value">{{ activeCount }}</view>
        <view class="stat-label">上架中</view>
      </view>
    </view>

    <view class="product-list">
      <view class="product-item" v-for="product in products" :key="product.id">
        <image 
          v-if="product.image" 
          :src="product.image" 
          class="product-image" 
          mode="aspectFill" />
        <view v-else class="product-image-placeholder">📦</view>
        
        <view class="product-info">
          <view class="product-name">{{ product.name }}</view>
          <view class="product-meta">
            <text>¥{{ product.price }}</text>
            <text class="dot">·</text>
            <text>库存{{ product.stock }}</text>
            <text class="dot">·</text>
            <text>销量{{ product.sales }}</text>
          </view>
          <view class="product-status" :class="product.status">
            {{ product.status === 'active' ? '已上架' : '已下架' }}
          </view>
        </view>
        
        <view class="product-actions">
          <view class="btn-edit" @click="editProduct(product)">编辑</view>
          <view class="btn-delete" @click="deleteProduct(product)">删除</view>
        </view>
      </view>
    </view>

    <view class="empty" v-if="products.length === 0">暂无商品</view>
  </view>
</template>

<script>
import { getAdminProductList, deleteProduct } from '@/api/shop'

export default {
  data() {
    return {
      products: [],
      total: 0
    }
  },
  computed: {
    activeCount() {
      return this.products.filter(p => p.status === 'active').length
    }
  },
  onLoad() {
    this.loadProducts()
  },
  onShow() {
    this.loadProducts()
  },
  methods: {
    loadProducts() {
      uni.showLoading({ title: '加载中...' })
      
      getAdminProductList().then(res => {
        if (res.code === 200) {
          this.products = res.data.products
          this.total = res.data.total
        }
      }).catch(err => {
        console.error('加载商品失败', err)
      }).finally(() => {
        uni.hideLoading()
      })
    },
    addProduct() {
      uni.navigateTo({ url: '/pages/admin/product-form' })
    },
    editProduct(product) {
      uni.navigateTo({ url: `/pages/admin/product-form?id=${product.id}` })
    },
    deleteProduct(product) {
      uni.showModal({
        title: '确认删除',
        content: `确定要删除商品"${product.name}"吗？`,
        success: (res) => {
          if (res.confirm) {
            deleteProduct(product.id).then(res => {
              if (res.code === 200) {
                uni.showToast({ title: '删除成功', icon: 'success' })
                this.loadProducts()
              }
            }).catch(err => {
              console.error('删除失败', err)
              uni.showToast({ title: '删除失败', icon: 'none' })
            })
          }
        }
      })
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 30rpx;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #fff;
}

.title {
  font-size: 36rpx;
  font-weight: bold;
}

.add-btn {
  padding: 12rpx 25rpx;
  background-color: rgba(255, 255, 255, 0.3);
  border-radius: 20rpx;
  font-size: 26rpx;
}

.stats {
  display: flex;
  gap: 20rpx;
  padding: 20rpx;
}

.stat-item {
  flex: 1;
  background-color: #fff;
  padding: 25rpx;
  border-radius: 12rpx;
  text-align: center;
}

.stat-value {
  font-size: 40rpx;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 8rpx;
}

.stat-label {
  font-size: 24rpx;
  color: #999;
}

.product-list {
  padding: 0 20rpx 20rpx;
}

.product-item {
  background-color: #fff;
  border-radius: 12rpx;
  padding: 20rpx;
  margin-bottom: 15rpx;
  display: flex;
  gap: 20rpx;
}

.product-image, .product-image-placeholder {
  width: 150rpx;
  height: 150rpx;
  border-radius: 8rpx;
  flex-shrink: 0;
}

.product-image-placeholder {
  background-color: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 60rpx;
}

.product-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.product-name {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
}

.product-meta {
  font-size: 24rpx;
  color: #999;
}

.dot {
  margin: 0 8rpx;
}

.product-status {
  font-size: 22rpx;
  padding: 4rpx 12rpx;
  border-radius: 10rpx;
  display: inline-block;
  width: fit-content;
}

.product-status.active {
  background-color: #d4edda;
  color: #155724;
}

.product-status.inactive {
  background-color: #f8d7da;
  color: #721c24;
}

.product-actions {
  display: flex;
  flex-direction: column;
  gap: 10rpx;
  justify-content: center;
}

.btn-edit, .btn-delete {
  padding: 10rpx 20rpx;
  border-radius: 6rpx;
  font-size: 24rpx;
  text-align: center;
  color: #fff;
}

.btn-edit {
  background-color: #3498db;
}

.btn-delete {
  background-color: #e74c3c;
}

.empty {
  text-align: center;
  padding: 100rpx 0;
  color: #999;
  font-size: 28rpx;
}
</style>
