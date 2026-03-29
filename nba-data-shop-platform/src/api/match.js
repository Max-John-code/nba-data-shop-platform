import { request } from '@/utils/request'

// 获取比赛列表（今天的比赛）
export const getMatchList = (date = null) => {
  const params = date ? { date, _t: Date.now() } : { _t: Date.now() }
  return request({
    url: '/matches/',
    method: 'GET',
    params
  })
}

// 获取所有比赛（管理用）
export const getAllMatches = () => {
  return request({
    url: '/matches/manage/',
    method: 'GET',
    params: { _t: Date.now() }
  })
}

// 添加比赛
export const addMatch = (data) => {
  return request({
    url: '/matches/manage/',
    method: 'POST',
    data
  })
}

// 获取比赛详情
export const getMatchDetail = (matchId) => {
  return request({
    url: `/matches/${matchId}/`,
    method: 'GET'
  })
}

// 更新比赛信息
export const updateMatch = (matchId, data) => {
  return request({
    url: `/matches/${matchId}/`,
    method: 'PUT',
    data
  })
}

// 删除比赛
export const deleteMatch = (matchId) => {
  return request({
    url: `/matches/${matchId}/`,
    method: 'DELETE'
  })
}
