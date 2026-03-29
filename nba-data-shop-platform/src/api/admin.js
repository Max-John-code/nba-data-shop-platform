import { request } from '@/utils/request'

// 获取用户列表
export const getUserList = () => {
  return request({
    url: '/accounts/users/',
    method: 'GET'
  })
}

// 更新用户信息
export const updateUser = (userId, data) => {
  return request({
    url: `/accounts/users/${userId}/`,
    method: 'PUT',
    data
  })
}

// 删除用户
export const deleteUser = (userId) => {
  return request({
    url: `/accounts/users/${userId}/`,
    method: 'DELETE'
  })
}
