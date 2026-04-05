import { request } from '@/utils/request'

// ==================== 视频点赞收藏 ====================

// 点赞视频
export function likeHighlight(id) {
  return request({
    url: `/highlights/${id}/like/`,
    method: 'post'
  })
}

// 取消点赞视频
export function unlikeHighlight(id) {
  return request({
    url: `/highlights/${id}/like/`,
    method: 'delete'
  })
}

// 收藏视频
export function favoriteHighlight(id) {
  return request({
    url: `/highlights/${id}/favorite/`,
    method: 'post'
  })
}

// 取消收藏视频
export function unfavoriteHighlight(id) {
  return request({
    url: `/highlights/${id}/favorite/`,
    method: 'delete'
  })
}

// 获取视频点赞收藏状态
export function getHighlightStatus(id) {
  return request({
    url: `/highlights/${id}/status/`,
    method: 'get'
  })
}

// ==================== 文章点赞收藏 ====================

// 点赞文章
export function likeArticle(id) {
  return request({
    url: `/forum/articles/${id}/like/`,
    method: 'post'
  })
}

// 取消点赞文章
export function unlikeArticle(id) {
  return request({
    url: `/forum/articles/${id}/like/`,
    method: 'delete'
  })
}

// 收藏文章
export function favoriteArticle(id) {
  return request({
    url: `/forum/articles/${id}/favorite/`,
    method: 'post'
  })
}

// 取消收藏文章
export function unfavoriteArticle(id) {
  return request({
    url: `/forum/articles/${id}/favorite/`,
    method: 'delete'
  })
}

// 获取文章点赞收藏状态
export function getArticleStatus(id) {
  return request({
    url: `/forum/articles/${id}/status/`,
    method: 'get'
  })
}

// ==================== 用户收藏列表 ====================

// 我收藏的视频
export function getUserFavoritedHighlights() {
  return request({
    url: '/accounts/favorites/highlights/',
    method: 'get'
  })
}

// 我收藏的文章
export function getUserFavoritedArticles() {
  return request({
    url: '/accounts/favorites/articles/',
    method: 'get'
  })
}

// 我点赞的视频
export function getUserLikedHighlights() {
  return request({
    url: '/accounts/likes/highlights/',
    method: 'get'
  })
}

// 我点赞的文章
export function getUserLikedArticles() {
  return request({
    url: '/accounts/likes/articles/',
    method: 'get'
  })
}
