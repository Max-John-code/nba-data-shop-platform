import { request } from '@/utils/request'

// 获取统计概览
export function getStatsOverview() {
  return request({
    url: '/stats/overview/',
    method: 'get'
  })
}

// 获取订单状态统计
export function getOrderStats() {
  return request({
    url: '/stats/orders/',
    method: 'get'
  })
}

// 获取商品销售统计
export function getProductSales() {
  return request({
    url: '/stats/products/',
    method: 'get'
  })
}

// 获取分类销售统计
export function getCategorySales() {
  return request({
    url: '/stats/categories/',
    method: 'get'
  })
}

// 获取精彩回放观看统计
export function getHighlightStats() {
  return request({
    url: '/stats/highlights/',
    method: 'get'
  })
}

// 获取文章浏览量统计
export function getArticleStats() {
  return request({
    url: '/stats/articles/',
    method: 'get'
  })
}
