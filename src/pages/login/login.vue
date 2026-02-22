<template>
  <view class="login-page">
    <view class="logo-container">
      <view class="logo-text">虎扑</view>
    </view>

    <view class="form-container">
      <view class="input-group">
        <input 
          class="input-field" 
          type="number" 
          v-model="phone" 
          placeholder="请输入大陆地区的手机号"
          maxlength="11"
        />
      </view>

      <view class="verify-group" @click="startVerify">
        <text class="verify-icon">✈️</text>
        <text class="verify-text">点击开始验证</text>
      </view>

      <view class="code-group">
        <input 
          class="code-input" 
          type="number" 
          v-model="code" 
          placeholder="请输入短信验证码"
          maxlength="6"
        />
        <view class="get-code-btn" @click="getCode">
          <text v-if="countdown === 0">获取短信验证码</text>
          <text v-else>{{ countdown }}s</text>
        </view>
      </view>

      <view class="register-link" @click="goToRegister">
        <text>没有账号，立即注册 ></text>
      </view>

      <button class="login-btn" @click="handleLogin">登录</button>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      phone: '',
      code: '',
      countdown: 0,
      timer: null
    }
  },
  methods: {
    startVerify() {
      if (!this.phone || this.phone.length !== 11) {
        uni.showToast({
          title: '请输入正确的手机号',
          icon: 'none'
        })
        return
      }
      uni.showToast({
        title: '验证已开始',
        icon: 'success'
      })
    },
    
    getCode() {
      if (!this.phone || this.phone.length !== 11) {
        uni.showToast({
          title: '请输入正确的手机号',
          icon: 'none'
        })
        return
      }
      
      if (this.countdown > 0) return
      
      uni.showToast({
        title: '验证码已发送',
        icon: 'success'
      })
      
      this.countdown = 60
      this.timer = setInterval(() => {
        this.countdown--
        if (this.countdown === 0) {
          clearInterval(this.timer)
        }
      }, 1000)
    },
    
    handleLogin() {
      if (!this.phone || this.phone.length !== 11) {
        uni.showToast({
          title: '请输入正确的手机号',
          icon: 'none'
        })
        return
      }
      
      if (!this.code) {
        uni.showToast({
          title: '请输入验证码',
          icon: 'none'
        })
        return
      }
      
      uni.showToast({
        title: '登录成功',
        icon: 'success'
      })
      
      setTimeout(() => {
        uni.switchTab({
          url: '/pages/index/index'
        })
      }, 1500)
    },
    
    goToRegister() {
      uni.navigateTo({
        url: '/pages/register/register'
      })
    }
  },
  
  onUnload() {
    if (this.timer) {
      clearInterval(this.timer)
    }
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background-color: #fff;
  padding: 0 60rpx;
}

.logo-container {
  display: flex;
  justify-content: center;
  padding: 120rpx 0 80rpx;
}

.logo-text {
  font-size: 80rpx;
  font-weight: bold;
  color: #e74c3c;
}

.form-container {
  width: 100%;
}

.input-group {
  margin-bottom: 40rpx;
}

.input-field {
  width: 100%;
  height: 100rpx;
  border: 1rpx solid #e0e0e0;
  border-radius: 10rpx;
  padding: 0 30rpx;
  font-size: 28rpx;
  box-sizing: border-box;
}

.verify-group {
  display: flex;
  align-items: center;
  background-color: #f5f5f5;
  padding: 30rpx;
  border-radius: 10rpx;
  margin-bottom: 40rpx;
  cursor: pointer;
}

.verify-icon {
  font-size: 40rpx;
  margin-right: 20rpx;
}

.verify-text {
  font-size: 28rpx;
  color: #666;
}

.code-group {
  display: flex;
  align-items: center;
  margin-bottom: 30rpx;
  gap: 20rpx;
}

.code-input {
  flex: 1;
  height: 100rpx;
  border: 1rpx solid #e0e0e0;
  border-radius: 10rpx;
  padding: 0 30rpx;
  font-size: 28rpx;
  box-sizing: border-box;
}

.get-code-btn {
  width: 280rpx;
  height: 100rpx;
  background-color: #e74c3c;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10rpx;
  font-size: 26rpx;
  flex-shrink: 0;
}

.register-link {
  text-align: right;
  margin-bottom: 60rpx;
}

.register-link text {
  color: #3b9ff3;
  font-size: 28rpx;
}

.login-btn {
  width: 100%;
  height: 100rpx;
  background-color: #e74c3c;
  color: #fff;
  border: none;
  border-radius: 10rpx;
  font-size: 32rpx;
  line-height: 100rpx;
}
</style>
