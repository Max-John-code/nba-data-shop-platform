<template>
  <view class="container">
    <view class="stats">
      <view class="stat-item">
        <view class="stat-value">{{ stats.total }}</view>
        <view class="stat-label">总订单</view>
      </view>
      <view class="stat-item">
        <view class="stat-value">{{ stats.pending }}</view>
        <view class="stat-label">待支付</view>
      </view>
      <view class="stat-item">
        <view class="stat-value">{{ stats.paid }}</view>
        <view class="stat-label">已支付</view>
      </view>
      <view class="stat-item">
        <view class="stat-value">{{ stats.shipped }}</view>
        <view class="stat-label">已发货</view>
      </view>
    </view>

    <view class="order-list" v-if="orders.length > 0">
      <view class="order-item" v-for="order in orders" :key="order.id">
        <view class="order-header">
          <view class="order-no">订单号：{{ order.order_no }}</view>
          <view class="order-status" :class="'status-' + order.status">
            {{ getStatusLabel(order.status) }}
          </view>
        </view>
        
        <view class="order-user">
          <text>用户：{{ order.user_name }}</text>
        </view>

        <view class="order-receiver">
          <view class="receiver-item">
            <text class="label">收货人：</text>
            <text>{{ order.receiver_name }}</text>
          </view>
          <view class="receiver-item">
            <text class="label">电话：</text>
            <text>{{ order.receiver_phone }}</text>
          </view>
          <view class="receiver-item">
            <text class="label">地址：</text>
            <text>{{ order.receiver_address }}</text>
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
            <picker 
              mode="selector" 
              :range="statusOptions" 
              :range-key="'label'"
              :value="getStatusIndex(order.status)"
              @change="changeStatus($event, order.id)">
              <view class="btn-status">修改状态</view>
            </picker>
          </view>
        </view>
      </view>
    </view>

    <view class="empty" v-else>
      <text class="empty-icon">📦</text>
      <text class="empty-text">暂无订单</text>
    </view>
  </view>
</template>

<script>
import { getAdminOrderList, updateOrderStatus } from '@/api/shop'

export default {
  data() {
    return {
      orders: [],
      stats: {
        total: 0,
        pending: 0,
        paid: 0,
        shipped: 0,
        completed: 0,
        cancelled: 0
      },
      statusMap: {
        'pending': '待支付',
        'paid': '已支付',
        'shipped': '已发货',
        'completed': '已完成',
        'cancelled': '已取消'
      },
      statusOptions: [
        { value: 'pending', label: '待支付' },
        { value: 'paid', label: '已支付' },
        { value: 'shipped', label: '已发货' },
        { value: 'completed', label: '已完成' },
        { value: 'cancelled', label: '已取消' }
      ]
    }
  },
  onLoad() {
    this.loadOrders()
  },
  methods: {
    loadOrders() {
      uni.showLoading({ title: '加载中...' })
      
      getAdminOrderList().then(res => {
        if (res.code === 200) {
          this.orders = res.data.orders
          this.stats = res.data.stats
        }
      }).catch(err => {
        console.error('加载订单失败', err)
        uni.showToast({ title: '加载失败', icon: 'none' })
      }).finally(() => {
        uni.hideLoading()
      })
    },
    getStatusLabel(status) {
      return this.statusMap[status] || status
    },
    getStatusIndex(status) {
      return this.statusOptions.findIndex(item => item.value === status)
    },
    changeStatus(e, orderId) {
      const index = e.detail.value
      const newStatus = this.statusOptions[index].value
      
      uni.showModal({
        title: '确认修改',
        content: `确认将订单状态修改为"${this.statusOptions[index].label}"吗？`,
        success: (res) => {
          if (res.confirm) {
            uni.showLoading({ title: '修改中...' })
            
            updateOrderStatus(orderId, newStatus).then(res => {
              if (res.code === 200) {
                uni.showToast({ title: '修改成功', icon: 'success' })
                this.loadOrders()
              }
            }).catch(err => {
              console.error('修改失败', err)
              uni.showToast({ title: '修改失败', icon: 'none' })
            }).finally(() => {
              uni.hideLoading()
            })
          }
        }
      })
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

.stats {
  display: flex;
  background-color: #fff;
  border-radius: 12rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  gap: 20rpx;
}

.stat-item {
  flex: 1;
  text-align: center;
}

.stat-value {
  font-size: 40rpx;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 10rpx;
}

.stat-label {
  font-size: 24rpx;
  color: #999;
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

.order-user {
  padding: 15rpx 20rpx;
  font-size: 26rpx;
  color: #333;
  border-bottom: 1rpx solid #f5f5f5;
}

.order-receiver {
  padding: 15rpx 20rpx;
  border-bottom: 1rpx solid #f5f5f5;
}

.receiver-item {
  font-size: 24rpx;
  color: #666;
  margin-bottom: 8rpx;
}

.receiver-item:last-child {
  margin-bottom: 0;
}

.receiver-item .label {
  color: #999;
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

.btn-status {
  padding: 15rpx 30rpx;
  background-color: #667eea;
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
</style>
