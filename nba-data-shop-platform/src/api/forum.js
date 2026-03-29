import { request } from '@/utils/request'

// 获取文章列表
export const getArticleList = () => {
  return request({
    url: '/forum/articles/',
    method: 'GET',
    params: { _t: Date.now() }
  })
}

// 发表文章（管理员）
export const publishArticle = (data) => {
  return request({
    url: '/forum/articles/manage/',
    method: 'POST',
    data
  })
}

// 获取文章详情
export const getArticleDetail = (articleId) => {
  return request({
    url: `/forum/articles/${articleId}/`,
    method: 'GET',
    params: { _t: Date.now() }
  })
}

// 更新文章（管理员）
export const updateArticle = (articleId, data) => {
  return request({
    url: `/forum/articles/${articleId}/`,
    method: 'PUT',
    data
  })
}

// 删除文章（管理员）
export const deleteArticle = (articleId) => {
  return request({
    url: `/forum/articles/${articleId}/`,
    method: 'DELETE'
  })
}

// 发表评论
export const postComment = (data) => {
  return request({
    url: '/forum/comments/',
    method: 'POST',
    data
  })
}

// 删除评论
export const deleteComment = (commentId) => {
  return request({
    url: `/forum/comments/${commentId}/`,
    method: 'DELETE'
  })
}
