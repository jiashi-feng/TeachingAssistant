import request from '@/utils/request'

export default {
  // 助教端：提交工时表
  submitTimesheet(data) {
    return request({
      url: '/ta/timesheets/',
      method: 'post',
      data,
    })
  },

  // 助教端：我的工时列表
  getMyTimesheets(params) {
    return request({
      url: '/ta/timesheets/',
      method: 'get',
      params,
    })
  },

  // 助教端：工时详情
  getTimesheetDetail(timesheetId) {
    return request({
      url: `/ta/timesheets/${timesheetId}/`,
      method: 'get',
    })
  },

  // 助教端：更新工时表
  updateTimesheet(timesheetId, data) {
    return request({
      url: `/ta/timesheets/${timesheetId}/update/`,
      method: 'put',
      data,
    })
  },

  // 助教端：我的薪酬列表
  getMySalaries(params) {
    return request({
      url: '/ta/salaries/',
      method: 'get',
      params,
    })
  },

  // 助教端：薪酬详情
  getSalaryDetail(salaryId) {
    return request({
      url: `/ta/salaries/${salaryId}/`,
      method: 'get',
    })
  },

  // 助教端：看板数据
  getTADashboard() {
    return request({
      url: '/ta/dashboard/',
      method: 'get',
    })
  },

  // 教师端：工时列表
  getFacultyTimesheets(params) {
    return request({
      url: '/faculty/timesheets/',
      method: 'get',
      params,
    })
  },

  // 教师端：工时详情
  getFacultyTimesheetDetail(timesheetId) {
    return request({
      url: `/faculty/timesheets/${timesheetId}/`,
      method: 'get',
    })
  },

  // 教师端：审核工时表
  reviewTimesheet(timesheetId, data) {
    return request({
      url: `/faculty/timesheets/${timesheetId}/review/`,
      method: 'post',
      data,
    })
  },
}

