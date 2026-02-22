import { request } from '@/utils/request'

// 综合搜索
export const search = (keyword) => {
  return request({
    url: '/search/',
    method: 'GET',
    params: { keyword }
  })
}
