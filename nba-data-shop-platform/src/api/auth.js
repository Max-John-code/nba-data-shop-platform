import { request } from '@/utils/request'

// 发送短信验证码
export const sendSms = (phone) => {
  return request({
    url: '/accounts/send-sms/',
    method: 'POST',
    data: { phone }
  })
}

// 登录
export const login = (phone, sms_code) => {
  return request({
    url: '/accounts/login/',
    method: 'POST',
    data: { phone, sms_code }
  })
}

// 注册
export const register = (phone, sms_code) => {
  return request({
    url: '/accounts/register/',
    method: 'POST',
    data: { phone, sms_code }
  })
}


// 获取个人信息
export const getProfile = () => {
  return request({
    url: '/accounts/profile/',
    method: 'GET'
  })
}

// 更新个人信息
export const updateProfile = (data) => {
  return request({
    url: '/accounts/profile/',
    method: 'PUT',
    data
  })
}

// 上传头像
export const uploadAvatar = (avatar) => {
  return request({
    url: '/accounts/upload-avatar/',
    method: 'POST',
    data: { avatar }
  })
}
