<template>
  <view class="container">
    <image 
      v-if="product.image" 
      :src="product.image" 
      class="product-image" 
      mode="aspectFill" />
    <view v-else class="product-image-placeholder">📦</view>

    <view class="product-info">
      <view class="product-name">{{ product.name }}</view>
      <view class="product-player" v-if="product.player_name">
        球星：{{ product.player_name }}
      </view>
      <view class="product-price">¥{{ product.price }}</view>
      <view class="product-meta">
        <text>库存：{{ product.stock }}</text>
        <text class="dot">·</text>
        <text>已售：{{ product.sales }}</text>
      </view>
    </view>

    <view class="product-desc">
      <view class="desc-title">商品描述</view>
      <view class="desc-content">{{ product.description || '暂无描述' }}</view>
    </view>

    <view class="footer">
      <view class="quantity-control">
        <view class="btn-minus" @click="decreaseQuantity">-</view>
        <view class="quantity">{{ quantity }}</view>
        <view class="btn-plus" @click="increaseQuantity">+</view>
      </view>
      <view class="btn-add-cart" @click="addToCart">加入购物车</view>
      <view class="btn-buy-now" @click="buyNow">立即购买</view>
    </view>
  </view>
</template>

<script>
import { getProductDetail, addToCart as addToCartApi } from '@/api/shop'

export default {
  data() {
    return {
      productId: null,
      product: {},
      quantity: 1
    }
  },
  onLoad(options) {
    this.productId = options.id
    this.loadProduct()
  },
  methods: {
    loadProduct() {
      uni.showLoading({ title: '加载中...' })
      
      getProductDetail(this.productId).then(res => {
        if (res.code === 200) {
          this.product = res.data
        }
      }).catch(err => {
        console.error('加载商品失败', err)
        uni.showToast({ title: '加载失败', icon: 'none' })
      }).finally(() => {
        uni.hideLoading()
      })
    },
    decreaseQuantity() {
      if (this.quantity > 1) {
        this.quantity--
      }
    },
    increaseQuantity() {
      if (this.quantity < this.product.stock) {
        this.quantity++
      } else {
        uni.showToast({ title: '库存不足', icon: 'none' })
      }
    },
    addToCart() {
      const token = uni.getStorageSync('token')
      if (!token) {
        uni.showToast({ title: '请先登录', icon: 'none' })
        uni.navigateTo({ url: '/pages/login/login' })
        return
      }

      if (this.product.stock < this.quantity) {
        uni.showToast({ title: '库存不足', icon: 'none' })
        return
      }

      uni.showLoading({ title: '添加中...' })
      
      addToCartApi({
        product_id: this.productId,
        quantity: this.quantity
      }).then(res => {
        if (res.code === 200) {
          uni.showToast({ title: '已加入购物车', icon: 'success' })
          this.quantity = 1
        }
      }).catch(err => {
        console.error('添加失败', err)
        uni.showToast({ title: '添加失败', icon: 'none' })
      }).finally(() => {
        uni.hideLoading()
      })
    },
    buyNow() {
      this.addToCart()
      setTimeout(() => {
        uni.navigateTo({ url: '/pages/shop/cart' })
      }, 1500)
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

.product-image, .product-image-placeholder {
  width: 100%;
  height: 600rpx;
}

.product-image-placeholder {
  background-color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 150rpx;
}

.product-info {
  background-color: #fff;
  padding: 30rpx;
  margin-bottom: 20rpx;
}

.product-name {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 15rpx;
}

.product-player {
  font-size: 28rpx;
  color: #666;
  margin-bottom: 20rpx;
}

.product-price {
  font-size: 48rpx;
  color: #e74c3c;
  font-weight: bold;
  margin-bottom: 15rpx;
}

.product-meta {
  font-size: 24rpx;
  color: #999;
}

.dot {
  margin: 0 10rpx;
}

.product-desc {
  background-color: #fff;
  padding: 30rpx;
}

.desc-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.desc-content {
  font-size: 28rpx;
  color: #666;
  line-height: 1.6;
}

.footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: #fff;
  padding: 20rpx;
  display: flex;
  gap: 15rpx;
  border-top: 1rpx solid #eee;
}

.quantity-control {
  display: flex;
  align-items: center;
  border: 1rpx solid #ddd;
  border-radius: 8rpx;
  overflow: hidden;
}

.btn-minus, .btn-plus {
  width: 60rpx;
  height: 60rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32rpx;
  color: #666;
  background-color: #f5f5f5;
}

.quantity {
  width: 80rpx;
  text-align: center;
  font-size: 28rpx;
}

.btn-add-cart, .btn-buy-now {
  flex: 1;
  padding: 20rpx 0;
  text-align: center;
  border-radius: 8rpx;
  font-size: 28rpx;
  font-weight: bold;
}

.btn-add-cart {
  background-color: #ffa500;
  color: #fff;
}

.btn-buy-now {
  background-color: #e74c3c;
  color: #fff;
}
</style>
