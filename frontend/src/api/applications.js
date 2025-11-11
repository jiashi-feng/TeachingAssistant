import request from '@/utils/request'

export default {
  // 学生端：提交申请（在线填写 或 上传文件）
  submitApplication({ position, resumeText, file }) {
    if (file) {
      const form = new FormData()
      form.append('position', position)
      form.append('resume', file)
      return request({
        url: '/student/applications/submit/',
        method: 'post',
        data: form,
        headers: { 'Content-Type': 'multipart/form-data' },
      })
    }
    return request({
      url: '/student/applications/submit/',
      method: 'post',
      data: { position, resume_text: resumeText || '' },
    })
  },

  // 学生端：我的申请列表
  getMyApplications(params) {
    return request({
      url: '/student/applications/',
      method: 'get',
      params,
    })
  },

  // 学生端：申请详情
  getMyApplicationDetail(applicationId) {
    return request({
      url: `/student/applications/${applicationId}/`,
      method: 'get',
    })
  },

  // 教师端：岗位的申请列表
  getPositionApplications(positionId, params) {
    return request({
      url: `/faculty/positions/${positionId}/applications/`,
      method: 'get',
      params,
    })
  },

  // 教师端：审核申请
  reviewApplication(applicationId, action, notes) {
    return request({
      url: `/faculty/applications/${applicationId}/review/`,
      method: 'post',
      data: { action, notes },
    })
  },

  // 教师端：撤销审核
  revokeApplication(applicationId) {
    return request({
      url: `/faculty/applications/${applicationId}/revoke/`,
      method: 'post',
    })
  },
}


