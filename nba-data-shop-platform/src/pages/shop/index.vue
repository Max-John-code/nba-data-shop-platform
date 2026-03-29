<template>
  <view class="container">
    <view class="header">
      <view class="title">球星商城</view>
      <view class="cart-icon" @click="goToCart">
        🛒
        <view class="cart-badge" v-if="cartCount > 0">{{ cartCount }}</view>
      </view>
    </view>

    <view class="category-tabs">
      <view 
        class="tab" 
        :class="{ active: currentCategory === '' }"
        @click="changeCategory('')">
        全部
      </view>
      <view 
        class="tab" 
        :class="{ active: currentCategory === 'jersey' }"
        @click="changeCategory('jersey')">
        球衣
      </view>
      <view 
        class="tab" 
        :class="{ active: currentCategory === 'shoes' }"
        @click="changeCategory('shoes')">
        球鞋
      </view>
      <view 
        class="tab" 
        :class="{ active: currentCategory === 'cap' }"
        @click="changeCategory('cap')">
        帽子
      </view>
      <view 
        class="tab" 
        :class="{ active: currentCategory === 'other' }"
        @click="changeCategory('other')">
        其他
      </view>
    </view>

    <view class="product-list">
      <view 
        class="product-item" 
        v-for="product in products" 
        :key="product.id"
        @click="goToDetail(product.id)">
        <image 
          v-if="product.image" 
          :src="product.image" 
          class="product-image" 
          mode="aspectFill" />
        <view v-else class="product-image-placeholder">📦</view>
        <view class="product-info">
          <view class="product-name">{{ product.name }}</view>
          <view class="product-player" v-if="product.player_name">{{ product.player_name }}</view>
          <view class="product-footer">
            <view class="product-price">¥{{ product.price }}</view>
            <view class="product-sales">已售{{ product.sales }}</view>
          </view>
        </view>
      </view>
    </view>

    <view class="empty" v-if="products.length === 0">
      <text class="empty-icon">🛍️</text>
      <text class="empty-text">暂无商品</text>
    </view>
  </view>
</template>

<script>
import { getProductList, getCartList } from '@/api/shop'

export default {
  data() {
    return {
      currentCategory: '',
      products: [],
      cartCount: 0
    }
  },
  onLoad() {
    this.loadProducts()
    this.loadCartCount()
  },
  onShow() {
    this.loadCartCount()
  },
  methods: {
    loadProducts() {
      uni.showLoading({ title: '加载中...' })
      
      getProductList(this.currentCategory).then(res => {
        if (res.code === 200) {
          this.products = res.data.products
        }
      }).catch(err => {
        console.error('加载商品失败', err)
      }).finally(() => {
        uni.hideLoading()
      })
    },
    loadCartCount() {
      const token = uni.getStorageSync('token')
      if (!token) return
      
      getCartList().then(res => {
        if (res.code === 200) {
          this.cartCount = res.data.items.length
        }
      }).catch(err => {
        console.error('加载购物车失败', err)
      })
    },
    changeCategory(category) {
      this.currentCategory = category
      this.loadProducts()
    },
    goToDetail(productId) {
      uni.navigateTo({ url: `/pages/shop/detail?id=${productId}` })
    },
    goToCart() {
      const token = uni.getStorageSync('token')
      if (!token) {
        uni.showToast({ title: '请先登录', icon: 'none' })
        uni.navigateTo({ url: '/pages/login/login' })
        return
      }
      uni.navigateTo({ url: '/pages/shop/cart' })
    }
  }
}
</script>

<style scoped>
.container {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding-bottom: 20rpx;
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

.cart-icon {
  font-size: 48rpx;
  position: relative;
}

.cart-badge {
  position: absolute;
  top: -10rpx;
  right: -10rpx;
  background-color: #e74c3c;
  color: #fff;
  font-size: 20rpx;
  padding: 2rpx 8rpx;
  border-radius: 20rpx;
  min-width: 30rpx;
  text-align: center;
}

.category-tabs {
  display: flex;
  background-color: #fff;
  padding: 20rpx;
  gap: 15rpx;
  overflow-x: auto;
}

.tab {
  padding: 12rpx 25rpx;
  border-radius: 20rpx;
  font-size: 26rpx;
  color: #666;
  background-color: #f5f5f5;
  white-space: nowrap;
}

.tab.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.product-list {
  padding: 20rpx;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20rpx;
}

.product-item {
  background-color: #fff;
  border-radius: 12rpx;
  overflow: hidden;
}

.product-image, .product-image-placeholder {
  width: 100%;
  height: 300rpx;
}

.product-image-placeholder {
  background-color: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 80rpx;
}

.product-info {
  padding: 20rpx;
}

.product-name {
  font-size: 28rpx;
  color: #333;
  font-weight: 500;
  margin-bottom: 8rpx;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-player {
  font-size: 24rpx;
  color: #999;
  margin-bottom: 12rpx;
}

.product-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.product-price {
  font-size: 32rpx;
  color: #e74c3c;
  font-weight: bold;
}

.product-sales {
  font-size: 22rpx;
  color: #999;
}

.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 100rpx 0;
  background-color: #fff;
  border-radius: 12rpx;
  margin: 20rpx;
}

.empty-icon {
  font-size: 100rpx;
  margin-bottom: 20rpx;
}

.empty-text {
  font-size: 28rpx;
  color: #999;
}
</style>
