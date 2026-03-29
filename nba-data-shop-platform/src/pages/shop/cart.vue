<template>
  <view class="container">
    <view class="cart-list" v-if="cartItems.length > 0">
      <view class="cart-item" v-for="item in cartItems" :key="item.id">
        <image 
          v-if="item.product_image" 
          :src="item.product_image" 
          class="product-image" 
          mode="aspectFill" />
        <view v-else class="product-image-placeholder">📦</view>
        
        <view class="item-info">
          <view class="product-name">{{ item.product_name }}</view>
          <view class="product-price">¥{{ item.product_price }}</view>
          <view class="quantity-control">
            <view class="btn-minus" @click="updateQuantity(item, item.quantity - 1)">-</view>
            <view class="quantity">{{ item.quantity }}</view>
            <view class="btn-plus" @click="updateQuantity(item, item.quantity + 1)">+</view>
          </view>
        </view>
        
        <view class="item-actions">
          <view class="btn-delete" @click="deleteItem(item)">删除</view>
        </view>
      </view>
    </view>

    <view class="empty" v-else>
      <text class="empty-icon">🛒</text>
      <text class="empty-text">购物车是空的</text>
      <view class="btn-go-shop" @click="goToShop">去逛逛</view>
    </view>

    <view class="footer" v-if="cartItems.length > 0">
      <view class="total">
        <text class="total-label">合计：</text>
        <text class="total-price">¥{{ totalPrice }}</text>
      </view>
      <view class="btn-checkout" @click="checkout">去结算</view>
    </view>
  </view>
</template>

<script>
import { getCartList, updateCart, deleteCart } from '@/api/shop'

export default {
  data() {
    return {
      cartItems: []
    }
  },
  computed: {
    totalPrice() {
      return this.cartItems.reduce((sum, item) => {
        return sum + (item.product_price * item.quantity)
      }, 0).toFixed(2)
    }
  },
  onLoad() {
    this.loadCart()
  },
  methods: {
    loadCart() {
      uni.showLoading({ title: '加载中...' })
      
      getCartList().then(res => {
        if (res.code === 200) {
          this.cartItems = res.data.items
        }
      }).catch(err => {
        console.error('加载购物车失败', err)
      }).finally(() => {
        uni.hideLoading()
      })
    },
    updateQuantity(item, newQuantity) {
      if (newQuantity < 1) {
        this.deleteItem(item)
        return
      }

      if (newQuantity > item.product_stock) {
        uni.showToast({ title: '库存不足', icon: 'none' })
        return
      }

      updateCart(item.id, { quantity: newQuantity }).then(res => {
        if (res.code === 200) {
          this.loadCart()
        }
      }).catch(err => {
        console.error('更新失败', err)
        uni.showToast({ title: '更新失败', icon: 'none' })
      })
    },
    deleteItem(item) {
      uni.showModal({
        title: '确认删除',
        content: '确定要删除这件商品吗？',
        success: (res) => {
          if (res.confirm) {
            deleteCart(item.id).then(res => {
              if (res.code === 200) {
                uni.showToast({ title: '已删除', icon: 'success' })
                this.loadCart()
              }
            }).catch(err => {
              console.error('删除失败', err)
              uni.showToast({ title: '删除失败', icon: 'none' })
            })
          }
        }
      })
    },
    checkout() {
      uni.navigateTo({ url: '/pages/shop/checkout' })
    },
    goToShop() {
      uni.navigateTo({ url: '/pages/shop/index' })
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

.cart-list {
  padding: 20rpx;
}

.cart-item {
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

.item-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.product-name {
  font-size: 28rpx;
  color: #333;
  font-weight: 500;
}

.product-price {
  font-size: 32rpx;
  color: #e74c3c;
  font-weight: bold;
}

.quantity-control {
  display: flex;
  align-items: center;
  border: 1rpx solid #ddd;
  border-radius: 8rpx;
  overflow: hidden;
  width: fit-content;
}

.btn-minus, .btn-plus {
  width: 50rpx;
  height: 50rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28rpx;
  color: #666;
  background-color: #f5f5f5;
}

.quantity {
  width: 60rpx;
  text-align: center;
  font-size: 26rpx;
}

.item-actions {
  display: flex;
  align-items: flex-end;
}

.btn-delete {
  font-size: 24rpx;
  color: #e74c3c;
  padding: 10rpx 20rpx;
}

.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 150rpx 0;
}

.empty-icon {
  font-size: 120rpx;
  margin-bottom: 20rpx;
}

.empty-text {
  font-size: 28rpx;
  color: #999;
  margin-bottom: 40rpx;
}

.btn-go-shop {
  padding: 20rpx 60rpx;
  background-color: #667eea;
  color: #fff;
  border-radius: 30rpx;
  font-size: 28rpx;
}

.footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: #fff;
  padding: 20rpx;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1rpx solid #eee;
}

.total {
  flex: 1;
}

.total-label {
  font-size: 28rpx;
  color: #666;
}

.total-price {
  font-size: 40rpx;
  color: #e74c3c;
  font-weight: bold;
}

.btn-checkout {
  padding: 20rpx 60rpx;
  background-color: #e74c3c;
  color: #fff;
  border-radius: 30rpx;
  font-size: 28rpx;
  font-weight: bold;
}
</style>
