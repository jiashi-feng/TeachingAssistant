/**
 * 本地存储工具函数
 * 统一管理localStorage操作
 */

const STORAGE_KEYS = {
  ACCESS_TOKEN: 'access_token',
  REFRESH_TOKEN: 'refresh_token',
  USER_INFO: 'user_info',
  REMEMBER_USERNAME: 'remember_username',
}

export const storage = {
  // 保存token
  setToken(accessToken, refreshToken) {
    localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, accessToken)
    localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, refreshToken)
  },

  // 获取access token
  getAccessToken() {
    return localStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN)
  },

  // 获取refresh token
  getRefreshToken() {
    return localStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN)
  },

  // 保存用户信息
  setUserInfo(userInfo) {
    localStorage.setItem(STORAGE_KEYS.USER_INFO, JSON.stringify(userInfo))
  },

  // 获取用户信息
  getUserInfo() {
    const userInfo = localStorage.getItem(STORAGE_KEYS.USER_INFO)
    return userInfo ? JSON.parse(userInfo) : null
  },

  // 清除所有认证信息
  clearAuth() {
    localStorage.removeItem(STORAGE_KEYS.ACCESS_TOKEN)
    localStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN)
    localStorage.removeItem(STORAGE_KEYS.USER_INFO)
  },

  // 保存记住的用户名
  setRememberUsername(username) {
    if (username) {
      localStorage.setItem(STORAGE_KEYS.REMEMBER_USERNAME, username)
    } else {
      localStorage.removeItem(STORAGE_KEYS.REMEMBER_USERNAME)
    }
  },

  // 获取记住的用户名
  getRememberUsername() {
    return localStorage.getItem(STORAGE_KEYS.REMEMBER_USERNAME)
  },
}

export default storage

