import { request } from '@/utils/request'

// 获取留言列表
export const getMessageList = () => {
  return request({
    url: '/messages/',
    method: 'GET',
    params: { _t: Date.now() }
  })
}

// 发表留言
export const postMessage = (data) => {
  return request({
    url: '/messages/',
    method: 'POST',
    data
  })
}

// 删除留言（管理员）
export const deleteMessage = (messageId) => {
  return request({
    url: `/messages/${messageId}/`,
    method: 'DELETE'
  })
}
