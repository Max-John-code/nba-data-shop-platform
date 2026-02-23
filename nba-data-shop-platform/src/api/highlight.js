import { request } from '@/utils/request'

// 获取精彩回放列表
export function getHighlightList(params) {
  return request({
    url: '/highlights/',
    method: 'get',
    params
  })
}

// 获取精彩回放详情
export function getHighlightDetail(id) {
  return request({
    url: `/highlights/${id}/`,
    method: 'get'
  })
}

// 增加观看次数
export function incrementViews(id) {
  return request({
    url: `/highlights/${id}/increment_views/`,
    method: 'post'
  })
}

// 创建精彩回放（管理员）
export function createHighlight(data) {
  return request({
    url: '/highlights/',
    method: 'post',
    data
  })
}

// 更新精彩回放（管理员）
export function updateHighlight(id, data) {
  return request({
    url: `/highlights/${id}/`,
    method: 'put',
    data
  })
}

// 删除精彩回放（管理员）
export function deleteHighlight(id) {
  return request({
    url: `/highlights/${id}/`,
    method: 'delete'
  })
}
