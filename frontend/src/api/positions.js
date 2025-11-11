import request from '@/utils/request'

export default {
  // 学生端：岗位列表
  getStudentPositions(params) {
    return request({
      url: '/student/positions/',
      method: 'get',
      params,
    })
  },

  // 学生端：岗位详情
  getPositionDetail(positionId) {
    return request({
      url: `/student/positions/${positionId}/`,
      method: 'get',
    })
  },

  // 教师端：我的岗位列表
  getMyPositions(params) {
    return request({
      url: '/faculty/positions/',
      method: 'get',
      params,
    })
  },

  // 教师端：创建岗位
  createPosition(data) {
    return request({
      url: '/faculty/positions/',
      method: 'post',
      data,
    })
  },

  // 教师端：编辑岗位
  updatePosition(positionId, data) {
    return request({
      url: `/faculty/positions/${positionId}/`,
      method: 'put',
      data,
    })
  },

  // 教师端：关闭岗位
  closePosition(positionId) {
    return request({
      url: `/faculty/positions/${positionId}/close/`,
      method: 'patch',
    })
  },
}


