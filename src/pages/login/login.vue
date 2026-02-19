<template>
  <view class="container">
    <view class="logo-section">
      <view class="logo-text">NBA球星数据咨询</view>
    </view>

    <view v-if="!isRegister" class="form-section">
      <view class="form-title">登录</view>
      
      <view class="form-group">
        <input 
          v-model="loginForm.phone" 
          type="number" 
          placeholder="请输入手机号" 
          class="form-input"
          maxlength="11"
          @input="filterPhone('login')"
        />
      </view>

      <view class="form-group">
        <view class="code-input-group">
          <input 
            v-model="loginForm.smsCode" 
            type="number" 
            placeholder="请输入4位验证码" 
            class="form-input code-input"
            maxlength="4"
            @input="filterCode('login')"
          />
          <view class="get-code-btn" @click="getSmsCode">{{ codeText }}</view>
        </view>
      </view>

      <view class="agreement">
        <checkbox-group @change="handleAgreeChange">
          <label>
            <checkbox :checked="isAgree" />
            <text>我已阅读并同意用户协议及隐私条款</text>
          </label>
        </checkbox-group>
      </view>

      <view class="login-btn" @click="login">登录</view>

      <view class="register-link">
        没有账号，<text class="link-text" @click="toggleRegister">立即注册</text>
      </view>
    </view>

    <view v-else class="form-section">
      <view class="form-title">注册</view>
      
      <view class="form-group">
        <input 
          v-model="registerForm.phone" 
          type="number" 
          placeholder="请输入手机号" 
          class="form-input"
          maxlength="11"
          @input="filterPhone('register')"
        />
      </view>

      <view class="form-group">
        <view class="code-input-group">
          <input 
            v-model="registerForm.smsCode" 
            type="number" 
            placeholder="请输入4位验证码" 
            class="form-input code-input"
            maxlength="4"
            @input="filterCode('register')"
          />
          <view class="get-code-btn" @click="getSmsCode">{{ codeText }}</view>
        </view>
      </view>

      <view class="form-group">
        <input 
          v-model="registerForm.password" 
          type="password" 
          placeholder="设置密码(6-16位字母数字)" 
          class="form-input"
          maxlength="16"
          @input="filterPassword('register')"
        />
      </view>

      <view class="form-group">
        <input 
          v-model="registerForm.confirmPassword" 
          type="password" 
          placeholder="确认密码" 
          class="form-input"
          maxlength="16"
          @input="filterPassword('confirmPassword')"
        />
      </view>

      <view class="agreement">
        <checkbox-group @change="handleAgreeChange">
          <label>
            <checkbox :checked="isAgree" />
            <text>我已阅读并同意用户协议及隐私条款</text>
          </label>
        </checkbox-group>
      </view>

      <view class="register-btn" @click="register">注册</view>

      <view class="login-link">
        已有账号，<text class="link-text" @click="toggleRegister">立即登录</text>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      isRegister: false,
      isAgree: false,
      codeText: '获取验证码',
      codeCountdown: 0,
      loginForm: {
        phone: '',
        smsCode: ''
      },
      registerForm: {
        phone: '',
        smsCode: '',
        password: '',
        confirmPassword: ''
      }
    }
  },
  methods: {
    handleAgreeChange(e) {
      this.isAgree = e.detail.value.length > 0
    },
    toggleRegister() {
      this.isRegister = !this.isRegister
      this.resetForm()
    },
    resetForm() {
      this.loginForm = { phone: '', smsCode: '' }
      this.registerForm = { phone: '', smsCode: '', password: '', confirmPassword: '' }
      this.isAgree = false
      this.codeText = '获取验证码'
      this.codeCountdown = 0
    },
    getSmsCode() {
      if (this.codeCountdown > 0) return
      
      const form = this.isRegister ? this.registerForm : this.loginForm
      if (!form.phone) {
        uni.showToast({ title: '请输入手机号', icon: 'none' })
        return
      }
      if (!/^\d{11}$/.test(form.phone)) {
        uni.showToast({ title: '请输入正确的11位手机号', icon: 'none' })
        return
      }

      this.codeCountdown = 60
      this.codeText = '60秒后重试'
      
      const timer = setInterval(() => {
        this.codeCountdown--
        this.codeText = this.codeCountdown + '秒后重试'
        if (this.codeCountdown <= 0) {
          clearInterval(timer)
          this.codeText = '获取验证码'
        }
      }, 1000)

      uni.showToast({ title: '验证码已发送', icon: 'success' })
    },
    filterPhone(type) {
      const form = type === 'login' ? this.loginForm : this.registerForm
      form.phone = form.phone.replace(/[^\d]/g, '').slice(0, 11)
    },
    filterCode(type) {
      const form = type === 'login' ? this.loginForm : this.registerForm
      form.smsCode = form.smsCode.replace(/[^\d]/g, '').slice(0, 4)
    },
    filterPassword(type) {
      const form = this.registerForm
      const field = type === 'confirmPassword' ? 'confirmPassword' : 'password'
      form[field] = form[field].replace(/[^a-zA-Z0-9]/g, '')
    },
    login() {
      if (!this.loginForm.phone) {
        uni.showToast({ title: '请输入手机号', icon: 'none' })
        return
      }
      if (!/^\d{11}$/.test(this.loginForm.phone)) {
        uni.showToast({ title: '请输入正确的11位手机号', icon: 'none' })
        return
      }
      if (!this.loginForm.smsCode) {
        uni.showToast({ title: '请输入短信验证码', icon: 'none' })
        return
      }
      if (!/^\d{4}$/.test(this.loginForm.smsCode)) {
        uni.showToast({ title: '请输入正确的4位验证码', icon: 'none' })
        return
      }
      if (!this.isAgree) {
        uni.showToast({ title: '请同意用户协议', icon: 'none' })
        return
      }

      const userInfo = {
        name: this.loginForm.phone,
        phone: this.loginForm.phone
      }
      uni.setStorageSync('userInfo', userInfo)
      
      uni.showToast({ title: '登录成功', icon: 'success' })
      setTimeout(() => {
        uni.navigateBack()
      }, 1500)
    },
    register() {
      if (!this.registerForm.phone) {
        uni.showToast({ title: '请输入手机号', icon: 'none' })
        return
      }
      if (!/^\d{11}$/.test(this.registerForm.phone)) {
        uni.showToast({ title: '请输入正确的11位手机号', icon: 'none' })
        return
      }
      if (!this.registerForm.smsCode) {
        uni.showToast({ title: '请输入短信验证码', icon: 'none' })
        return
      }
      if (!/^\d{4}$/.test(this.registerForm.smsCode)) {
        uni.showToast({ title: '请输入正确的4位验证码', icon: 'none' })
        return
      }
      if (!this.registerForm.password) {
        uni.showToast({ title: '请设置密码', icon: 'none' })
        return
      }
      if (!/^[a-zA-Z0-9]{6,16}$/.test(this.registerForm.password)) {
        uni.showToast({ title: '密码需要6-16位字母数字组合', icon: 'none' })
        return
      }
      if (this.registerForm.password !== this.registerForm.confirmPassword) {
        uni.showToast({ title: '两次密码不一致', icon: 'none' })
        return
      }
      if (!this.isAgree) {
        uni.showToast({ title: '请同意用户协议', icon: 'none' })
        return
      }

      const userInfo = {
        name: this.registerForm.phone,
        phone: this.registerForm.phone
      }
      uni.setStorageSync('userInfo', userInfo)
      
      uni.showToast({ title: '注册成功', icon: 'success' })
      setTimeout(() => {
        uni.navigateBack()
      }, 1500)
    }
  }
}
</script>

<style scoped>
.container {
  background-color: #f5f5f5;
  min-height: 100vh;
  padding: 50rpx 25rpx;
}

.logo-section {
  text-align: center;
  margin-bottom: 60rpx;
  margin-top: 40rpx;
}

.logo-text {
  font-size: 48rpx;
  font-weight: bold;
  color: #e74c3c;
}

.form-section {
  background-color: #fff;
  border-radius: 8rpx;
  padding: 50rpx 40rpx;
}

.form-title {
  font-size: 40rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 50rpx;
  text-align: center;
}

.form-group {
  margin-bottom: 30rpx;
  position: relative;
}

.form-input {
  width: 100%;
  padding: 20rpx;
  border: 1rpx solid #ddd;
  border-radius: 6rpx;
  font-size: 30rpx;
  color: #333;
  box-sizing: border-box;
  height: 80rpx;
  line-height: 40rpx;
}

.form-input::placeholder {
  color: #bbb;
}

.code-input-group {
  display: flex;
  gap: 10rpx;
}

.code-input {
  flex: 1;
}

.get-code-btn {
  background-color: #e74c3c;
  color: white;
  padding: 20rpx;
  border-radius: 6rpx;
  font-size: 26rpx;
  white-space: nowrap;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 160rpx;
  height: 80rpx;
}

.agreement {
  margin-bottom: 40rpx;
  font-size: 26rpx;
  color: #666;
}

.agreement checkbox-group {
  display: flex;
  align-items: center;
}

.agreement label {
  display: flex;
  align-items: center;
}

.agreement checkbox {
  margin-right: 10rpx;
}

.agreement text {
  color: #666;
}

.login-btn,
.register-btn {
  width: 100%;
  padding: 22rpx 0;
  background-color: #e74c3c;
  color: white;
  border-radius: 6rpx;
  font-size: 34rpx;
  font-weight: bold;
  text-align: center;
  margin-bottom: 25rpx;
}

.register-link,
.login-link {
  text-align: center;
  font-size: 28rpx;
  color: #666;
}

.link-text {
  color: #0066cc;
  font-weight: bold;
}
</style>