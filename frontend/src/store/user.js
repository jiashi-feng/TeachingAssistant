/**
 * 用户状态管理 (Pinia Store)
 * 管理用户认证状态、个人信息、角色权限
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api'
import storage from '@/utils/storage'
import router from '@/router'
import { ElMessage } from 'element-plus'

export const useUserStore = defineStore('user', () => {
  // ==================== 状态 ====================

  // 访问令牌
  const token = ref(null)

  // 刷新令牌
  const refreshToken = ref(null)

  // 用户信息
  const userInfo = ref(null)

  // ==================== 计算属性 ====================

  // 是否已登录
  const isAuthenticated = computed(() => !!token.value)

  // 用户角色列表（完整对象数组）
  const roles = computed(() => userInfo.value?.roles || [])

  // 用户角色代码列表（提取role_code，方便判断）
  const roleCodes = computed(() => {
    return roles.value.map(role => role.role_code)
  })

  // 用户权限列表
  const permissions = computed(() => userInfo.value?.permissions || [])

  // 是否为助教
  const isTA = computed(() => {
    return userInfo.value?.student_info?.is_ta || false
  })

  // ==================== 方法 ====================

  /**
   * 登录
   * @param {Object} credentials - { username, password }
   * @returns {Promise}
   */
  async function login(credentials) {
    try {
      const response = await api.auth.login(credentials)

      // 保存token（后端返回的是 tokens 对象）
      token.value = response.tokens.access
      refreshToken.value = response.tokens.refresh
      storage.setToken(response.tokens.access, response.tokens.refresh)

      // 保存用户信息
      userInfo.value = response.user
      storage.setUserInfo(response.user)

      ElMessage.success('登录成功，欢迎回来！')

      return response
    } catch (error) {
      console.error('登录失败:', error)
      throw error
    }
  }

  /**
   * 登出
   */
  async function logout() {
    try {
      // 调用后端登出接口（将refresh token加入黑名单）
      if (refreshToken.value) {
        await api.auth.logout({ refresh_token: refreshToken.value })
      }
    } catch (error) {
      console.error('登出接口调用失败:', error)
    } finally {
      // 无论接口是否成功，都清除本地数据
      clearAuth()
      ElMessage.success('已退出登录')
      router.push('/login')
    }
  }

  /**
   * 设置Token
   * @param {string} accessToken 
   * @param {string} refresh 
   */
  function setToken(accessToken, refresh) {
    token.value = accessToken
    refreshToken.value = refresh
    storage.setToken(accessToken, refresh)
  }

  /**
   * 设置用户信息
   * @param {Object} info 
   */
  function setUserInfo(info) {
    userInfo.value = info
    storage.setUserInfo(info)
  }

  /**
   * 清除认证信息
   */
  function clearAuth() {
    token.value = null
    refreshToken.value = null
    userInfo.value = null
    storage.clearAuth()
  }

  /**
   * 检查用户是否拥有指定角色
   * @param {string} roleCode - 角色代码（如 'student', 'faculty'）
   * @returns {boolean}
   */
  function hasRole(roleCode) {
    return roleCodes.value.includes(roleCode)
  }

  /**
   * 检查用户是否拥有指定权限
   * @param {string} permission - 权限名称
   * @returns {boolean}
   */
  function hasPermission(permission) {
    return permissions.value.includes(permission)
  }

  /**
   * 检查用户是否拥有任一指定角色
   * @param {Array<string>} roleList - 角色代码列表
   * @returns {boolean}
   */
  function hasAnyRole(roleList) {
    return roleList.some(role => roleCodes.value.includes(role))
  }

  /**
   * 检查用户是否拥有所有指定角色
   * @param {Array<string>} roleList - 角色代码列表
   * @returns {boolean}
   */
  function hasAllRoles(roleList) {
    return roleList.every(role => roleCodes.value.includes(role))
  }

  /**
   * 应用启动时恢复登录状态
   * 从localStorage读取token和用户信息
   */
  function initAuth() {
    const savedToken = storage.getAccessToken()
    const savedRefreshToken = storage.getRefreshToken()
    const savedUserInfo = storage.getUserInfo()

    if (savedToken && savedUserInfo) {
      token.value = savedToken
      refreshToken.value = savedRefreshToken
      userInfo.value = savedUserInfo

      console.log('已恢复登录状态:', savedUserInfo.username)
    }
  }

  /**
   * 刷新用户信息
   * 从后端重新获取最新的用户信息
   */
  async function refreshUserInfo() {
    try {
      const response = await api.auth.getProfile()
      // 修复：从响应中提取 user 字段，与登录时的处理保持一致
      // 后端返回格式：{message: "...", user: {...}}
      const userData = response.user || response
      setUserInfo(userData)
      return userData
    } catch (error) {
      console.error('刷新用户信息失败:', error)
      throw error
    }
  }

  /**
   * 根据用户角色跳转到对应的首页
   */
  function navigateToHome() {
    const userRoleCodes = roleCodes.value

    if (userRoleCodes.includes('admin')) {
      // 管理员跳转到Django Admin后台
      window.location.href = 'http://localhost:8000/admin/'
    } else if (userRoleCodes.includes('faculty')) {
      // 教师跳转到教师看板
      router.push('/faculty/dashboard')
    } else if (userRoleCodes.includes('student')) {
      // 学生/助教跳转到学生看板
      router.push('/student/dashboard')
    } else {
      // 默认跳转到登录页
      router.push('/login')
    }
  }

  // 返回状态和方法
  return {
    // 状态
    token,
    refreshToken,
    userInfo,

    // 计算属性
    isAuthenticated,
    roles,        // 完整角色对象数组
    roleCodes,    // 角色代码字符串数组
    permissions,
    isTA,

    // 方法
    login,
    logout,
    setToken,
    setUserInfo,
    clearAuth,
    hasRole,
    hasPermission,
    hasAnyRole,
    hasAllRoles,
    initAuth,
    refreshUserInfo,
    navigateToHome,
  }
})

export default useUserStore

