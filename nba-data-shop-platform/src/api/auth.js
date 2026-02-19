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
