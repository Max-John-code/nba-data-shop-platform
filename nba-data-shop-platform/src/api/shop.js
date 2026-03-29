import { request } from '@/utils/request'

// 商品列表
export const getProductList = (category) => {
  return request({
    url: '/shop/products/',
    method: 'GET',
    params: category ? { category } : {}
  })
}

// 商品详情
export const getProductDetail = (productId) => {
  return request({
    url: `/shop/products/${productId}/`,
    method: 'GET'
  })
}

// 购物车列表
export const getCartList = () => {
  return request({
    url: '/shop/cart/',
    method: 'GET'
  })
}

// 添加到购物车
export const addToCart = (data) => {
  return request({
    url: '/shop/cart/',
    method: 'POST',
    data
  })
}

// 更新购物车
export const updateCart = (cartId, data) => {
  return request({
    url: `/shop/cart/${cartId}/`,
    method: 'PUT',
    data
  })
}

// 删除购物车
export const deleteCart = (cartId) => {
  return request({
    url: `/shop/cart/${cartId}/`,
    method: 'DELETE'
  })
}

// 订单列表
export const getOrderList = () => {
  return request({
    url: '/shop/orders/',
    method: 'GET'
  })
}

// 创建订单
export const createOrder = (data) => {
  return request({
    url: '/shop/orders/',
    method: 'POST',
    data
  })
}

// 订单详情
export const getOrderDetail = (orderId) => {
  return request({
    url: `/shop/orders/${orderId}/`,
    method: 'GET'
  })
}

// 管理员 - 商品列表
export const getAdminProductList = () => {
  return request({
    url: '/shop/admin/products/',
    method: 'GET'
  })
}

// 管理员 - 添加商品
export const addProduct = (data) => {
  return request({
    url: '/shop/admin/products/',
    method: 'POST',
    data
  })
}

// 管理员 - 更新商品
export const updateProduct = (productId, data) => {
  return request({
    url: `/shop/admin/products/${productId}/`,
    method: 'PUT',
    data
  })
}

// 管理员 - 删除商品
export const deleteProduct = (productId) => {
  return request({
    url: `/shop/admin/products/${productId}/`,
    method: 'DELETE'
  })
}

// 支付订单
export const payOrder = (orderId) => {
  return request({
    url: `/shop/orders/${orderId}/pay/`,
    method: 'POST'
  })
}

// 管理员 - 订单列表
export const getAdminOrderList = () => {
  return request({
    url: '/shop/admin/orders/',
    method: 'GET'
  })
}

// 管理员 - 更新订单状态
export const updateOrderStatus = (orderId, status) => {
  return request({
    url: `/shop/admin/orders/${orderId}/`,
    method: 'PUT',
    data: { status }
  })
}
