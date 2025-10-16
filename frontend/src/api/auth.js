/**
 * 认证相关API
 */

import request from '@/utils/request'

export default {
  // 用户登录
  login(data) {
    return request({
      url: '/auth/login/',
      method: 'post',
      data,
    })
  },

  // 用户注册
  register(data) {
    return request({
      url: '/auth/register/',
      method: 'post',
      data,
    })
  },

  // 用户登出
  logout(data) {
    return request({
      url: '/auth/logout/',
      method: 'post',
      data,
    })
  },

  // 获取当前用户信息
  getProfile() {
    return request({
      url: '/auth/profile/',
      method: 'get',
    })
  },

  // 更新用户信息
  updateProfile(data) {
    return request({
      url: '/auth/profile/',
      method: 'put',
      data,
    })
  },

  // 修改密码
  changePassword(data) {
    return request({
      url: '/auth/change-password/',
      method: 'put',
      data,
    })
  },

  // 检查用户名是否可用
  checkUsername(username) {
    return request({
      url: '/auth/check-username/',
      method: 'get',
      params: { username },
    })
  },

  // 检查邮箱是否可用
  checkEmail(email) {
    return request({
      url: '/auth/check-email/',
      method: 'get',
      params: { email },
    })
  },

  // 刷新Token
  refreshToken(refresh) {
    return request({
      url: '/auth/token/refresh/',
      method: 'post',
      data: { refresh },
    })
  },
}

