<template>
  <view class="container">
    <view class="form">
      <view class="form-item">
        <view class="label">收货人</view>
        <input v-model="formData.receiver_name" placeholder="请输入收货人姓名" class="input" />
      </view>
      
      <view class="form-item">
        <view class="label">联系电话</view>
        <input v-model="formData.receiver_phone" type="number" placeholder="请输入手机号" class="input" />
      </view>
      
      <view class="form-item">
        <view class="label">收货地址</view>
        <textarea v-model="formData.receiver_address" placeholder="请输入详细地址" class="textarea" />
      </view>
    </view>

    <view class="footer">
      <view class="total">合计：¥{{ totalAmount }}</view>
      <view class="btn-submit" @click="submitOrder">提交订单</view>
    </view>
  </view>
</template>

<script>
import { getCartList, createOrder } from '@/api/shop'

export default {
  data() {
    return {
      formData: {
        receiver_name: '',
        receiver_phone: '',
        receiver_address: ''
      },
      totalAmount: 0
    }
  },
  onLoad() {
    this.loadCartTotal()
  },
  methods: {
    loadCartTotal() {
      getCartList().then(res => {
        if (res.code === 200) {
          this.totalAmount = res.data.total
        }
      })
    },
    submitOrder() {
      if (!this.formData.receiver_name) {
        uni.showToast({ title: '请输入收货人', icon: 'none' })
        return
      }
      if (!this.formData.receiver_phone) {
        uni.showToast({ title: '请输入联系电话', icon: 'none' })
        return
      }
      if (!this.formData.receiver_address) {
        uni.showToast({ title: '请输入收货地址', icon: 'none' })
        return
      }

      uni.showLoading({ title: '提交中...' })
      
      createOrder(this.formData).then(res => {
        if (res.code === 200) {
          uni.showToast({ title: '下单成功', icon: 'success' })
          setTimeout(() => {
            uni.redirectTo({ url: '/pages/shop/orders' })
          }, 1500)
        }
      }).catch(err => {
        console.error('下单失败', err)
        uni.showToast({ title: '下单失败', icon: 'none' })
      }).finally(() => {
        uni.hideLoading()
      })
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
}

.input, .textarea {
  width: 100%;
  padding: 25rpx 20rpx;
  border: 1rpx solid #ddd;
  border-radius: 8rpx;
  font-size: 28rpx;
  box-sizing: border-box;
  min-height: 80rpx;
}

.textarea {
  min-height: 150rpx;
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
  font-size: 36rpx;
  color: #e74c3c;
  font-weight: bold;
}

.btn-submit {
  padding: 20rpx 60rpx;
  background-color: #e74c3c;
  color: #fff;
  border-radius: 30rpx;
  font-size: 28rpx;
  font-weight: bold;
}
</style>
