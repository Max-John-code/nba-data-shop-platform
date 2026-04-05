<template>
  <view class="container">
    <view class="order-list" v-if="orders.length > 0">
      <view class="order-item" v-for="order in orders" :key="order.id">
        <view class="order-header">
          <view class="order-no">订单号：{{ order.order_no }}</view>
          <view class="order-status" :class="'status-' + order.status">
            {{ getStatusLabel(order.status) }}
          </view>
        </view>
        
        <view class="order-products">
          <view class="product-item" v-for="item in order.items" :key="item.id">
            <image 
              v-if="item.product_image" 
              :src="item.product_image" 
              class="product-image" 
              mode="aspectFill" />
            <view v-else class="product-image-placeholder">📦</view>
            <view class="product-info">
              <view class="product-name">{{ item.product_name }}</view>
              <view class="product-price">¥{{ item.price }} x {{ item.quantity }}</view>
            </view>
          </view>
        </view>
        
        <view class="order-footer">
          <view class="order-info">
            <view class="order-total">合计：¥{{ order.total_amount }}</view>
            <view class="order-time">{{ formatTime(order.created_at) }}</view>
          </view>
          <view class="order-actions">
            <view 
              v-if="order.status === 'pending'" 
              class="btn-pay" 
              @click="payOrder(order.id)">
              去支付
            </view>
            <view 
              v-if="order.status === 'shipped'" 
              class="btn-confirm" 
              @click="confirmOrder(order.id)">
              确认收货
            </view>
          </view>
        </view>
      </view>
    </view>

    <view class="empty" v-else>
      <text class="empty-icon">📦</text>
      <text class="empty-text">暂无订单</text>
    </view>
    
    <!-- 支付弹窗 -->
    <view v-if="showPaymentModal" class="payment-modal" @click="closePaymentModal">
      <view class="modal-content" @click.stop>
        <view class="modal-header">
          <text class="modal-title">扫码支付</text>
          <text class="close-btn" @click="closePaymentModal">✕</text>
        </view>
        
        <view class="qrcode-container">
          <image :src="paymentQRCode" class="qrcode-image" mode="aspectFit" />
          <text class="qrcode-tip">请使用微信/支付宝扫码支付</text>
        </view>
        
        <view class="modal-footer">
          <view class="btn-cancel" @click="closePaymentModal">取消</view>
          <view class="btn-confirm-pay" @click="confirmPayment">已完成支付</view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import { getOrderList, payOrder as payOrderApi } from '@/api/shop'

export default {
  data() {
    return {
      orders: [],
      statusMap: {
        'pending': '待支付',
        'paid': '已支付',
        'shipped': '已发货',
        'completed': '已完成',
        'cancelled': '已取消'
      },
      showPaymentModal: false,
      currentOrderId: null,
      paymentQRCode: '/static/payment-qrcode.jpg' // 收款码路径
    }
  },
  onLoad() {
    this.loadOrders()
  },
  methods: {
    loadOrders() {
      uni.showLoading({ title: '加载中...' })
      
      getOrderList().then(res => {
        if (res.code === 200) {
          this.orders = res.data.orders
        }
      }).catch(err => {
        console.error('加载订单失败', err)
      }).finally(() => {
        uni.hideLoading()
      })
    },
    payOrder(orderId) {
      this.currentOrderId = orderId
      this.showPaymentModal = true
    },
    
    confirmPayment() {
      uni.showLoading({ title: '确认支付中...' })
      
      payOrderApi(this.currentOrderId).then(res => {
        if (res.code === 200) {
          uni.showToast({ title: '支付成功', icon: 'success' })
          this.showPaymentModal = false
          this.currentOrderId = null
          this.loadOrders()
        }
      }).catch(err => {
        console.error('支付失败', err)
        uni.showToast({ title: '支付失败', icon: 'none' })
      }).finally(() => {
        uni.hideLoading()
      })
    },
    
    closePaymentModal() {
      this.showPaymentModal = false
      this.currentOrderId = null
    },
    confirmOrder(orderId) {
      uni.showModal({
        title: '确认收货',
        content: '确认已收到商品吗？',
        success: (res) => {
          if (res.confirm) {
            uni.showLoading({ title: '处理中...' })
            
            // 调用确认收货API，将状态改为completed
            const token = uni.getStorageSync('token')
            uni.request({
              url: 'http://127.0.0.1:8000/api/shop/orders/' + orderId + '/confirm/',
              method: 'POST',
              header: {
                'Authorization': 'Token ' + token
              },
              success: (res) => {
                if (res.data.code === 200) {
                  uni.showToast({ title: '确认成功', icon: 'success' })
                  this.loadOrders()
                } else {
                  uni.showToast({ title: res.data.message || '确认失败', icon: 'none' })
                }
              },
              fail: (err) => {
                console.error('确认收货失败', err)
                uni.showToast({ title: '确认失败', icon: 'none' })
              },
              complete: () => {
                uni.hideLoading()
              }
            })
          }
        }
      })
    },
    getStatusLabel(status) {
      return this.statusMap[status] || status
    },
    formatTime(timeStr) {
      const time = new Date(timeStr)
      const year = time.getFullYear()
      const month = String(time.getMonth() + 1).padStart(2, '0')
      const day = String(time.getDate()).padStart(2, '0')
      const hour = String(time.getHours()).padStart(2, '0')
      const minute = String(time.getMinutes()).padStart(2, '0')
      
      return `${year}-${month}-${day} ${hour}:${minute}`
    }
  }
}
</script>

<style scoped>
.container {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 20rpx;
}

.order-list {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.order-item {
  background-color: #fff;
  border-radius: 12rpx;
  overflow: hidden;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20rpx;
  border-bottom: 1rpx solid #f5f5f5;
}

.order-no {
  font-size: 24rpx;
  color: #666;
}

.order-status {
  font-size: 24rpx;
  padding: 5rpx 15rpx;
  border-radius: 10rpx;
}

.status-pending {
  background-color: #fff3cd;
  color: #856404;
}

.status-paid, .status-shipped {
  background-color: #d1ecf1;
  color: #0c5460;
}

.status-completed {
  background-color: #d4edda;
  color: #155724;
}

.status-cancelled {
  background-color: #f8d7da;
  color: #721c24;
}

.order-products {
  padding: 20rpx;
}

.product-item {
  display: flex;
  gap: 15rpx;
  margin-bottom: 15rpx;
}

.product-item:last-child {
  margin-bottom: 0;
}

.product-image, .product-image-placeholder {
  width: 120rpx;
  height: 120rpx;
  border-radius: 8rpx;
  flex-shrink: 0;
}

.product-image-placeholder {
  background-color: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 50rpx;
}

.product-info {
  flex: 1;
}

.product-name {
  font-size: 28rpx;
  color: #333;
  margin-bottom: 10rpx;
}

.product-price {
  font-size: 24rpx;
  color: #999;
}

.order-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20rpx;
  border-top: 1rpx solid #f5f5f5;
}

.order-info {
  flex: 1;
}

.order-total {
  font-size: 32rpx;
  color: #e74c3c;
  font-weight: bold;
  margin-bottom: 5rpx;
}

.order-time {
  font-size: 22rpx;
  color: #999;
}

.order-actions {
  display: flex;
  gap: 15rpx;
}

.btn-pay {
  padding: 15rpx 40rpx;
  background-color: #e74c3c;
  color: #fff;
  border-radius: 30rpx;
  font-size: 26rpx;
}

.btn-confirm {
  padding: 15rpx 40rpx;
  background-color: #27ae60;
  color: #fff;
  border-radius: 30rpx;
  font-size: 26rpx;
}

.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 150rpx 0;
  background-color: #fff;
  border-radius: 12rpx;
}

.empty-icon {
  font-size: 120rpx;
  margin-bottom: 20rpx;
}

.empty-text {
  font-size: 28rpx;
  color: #999;
}

.payment-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.modal-content {
  width: 600rpx;
  background-color: #fff;
  border-radius: 16rpx;
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 30rpx;
  border-bottom: 1rpx solid #f0f0f0;
}

.modal-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.close-btn {
  font-size: 40rpx;
  color: #999;
  line-height: 1;
}

.qrcode-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 50rpx 30rpx;
}

.qrcode-image {
  width: 400rpx;
  height: 400rpx;
  border: 2rpx solid #f0f0f0;
  border-radius: 8rpx;
  margin-bottom: 30rpx;
}

.qrcode-tip {
  font-size: 26rpx;
  color: #666;
  text-align: center;
}

.modal-footer {
  display: flex;
  border-top: 1rpx solid #f0f0f0;
}

.btn-cancel,
.btn-confirm-pay {
  flex: 1;
  padding: 30rpx 0;
  text-align: center;
  font-size: 30rpx;
}

.btn-cancel {
  color: #666;
  border-right: 1rpx solid #f0f0f0;
}

.btn-confirm-pay {
  color: #e74c3c;
  font-weight: bold;
}
</style>
