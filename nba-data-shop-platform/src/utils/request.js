// API基础配置
const BASE_URL = 'http://127.0.0.1:8000/api'

// 请求封装
export const request = (options) => {
  return new Promise((resolve, reject) => {
    const token = uni.getStorageSync('token')
    
    // 处理GET请求的参数
    let url = BASE_URL + options.url
    if (options.method === 'GET' && options.params) {
      const queryString = Object.keys(options.params)
        .map(key => `${key}=${encodeURIComponent(options.params[key])}`)
        .join('&')
      url += (url.includes('?') ? '&' : '?') + queryString
    }
    
    uni.request({
      url: url,
      method: options.method || 'GET',
      data: options.data || {},
      header: {
        'Content-Type': 'application/json',
        'Authorization': token ? `Token ${token}` : ''
      },
      success: (res) => {
        if (res.statusCode === 200) {
          resolve(res.data)
        } else {
          uni.showToast({
            title: res.data.message || '请求失败',
            icon: 'none'
          })
          reject(res.data)
        }
      },
      fail: (err) => {
        uni.showToast({
          title: '网络请求失败',
          icon: 'none'
        })
        reject(err)
      }
    })
  })
}
