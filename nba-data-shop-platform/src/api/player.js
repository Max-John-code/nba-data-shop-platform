import { request } from '@/utils/request'

// 获取球员列表
export const getPlayerList = (type = null) => {
  const params = type ? { type } : {}
  return request({
    url: '/players/',
    method: 'GET',
    params
  })
}

// 添加球员
export const addPlayer = (data) => {
  return request({
    url: '/players/manage/',
    method: 'POST',
    data
  })
}

// 获取球员详情
export const getPlayerDetail = (playerId) => {
  return request({
    url: `/players/${playerId}/`,
    method: 'GET'
  })
}

// 更新球员信息
export const updatePlayer = (playerId, data) => {
  return request({
    url: `/players/${playerId}/`,
    method: 'PUT',
    data
  })
}

// 删除球员
export const deletePlayer = (playerId) => {
  return request({
    url: `/players/${playerId}/`,
    method: 'DELETE'
  })
}
