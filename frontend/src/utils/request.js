/**
 * Axios请求封装
 * 统一处理请求和响应，自动添加token，处理错误
 */

import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

// 创建axios实例
const service = axios.create({
  baseURL: '/api', // 部署时与后端同域，通过 /api 访问
  timeout: 10000, // 请求超时时间
  headers: {
    'Content-Type': 'application/json',
  },
  // CSRF 配置：从 csrftoken Cookie 读取并自动添加到 X-CSRFToken 请求头
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
})

// 请求拦截器
service.interceptors.request.use(
  (config) => {
    // 从localStorage获取token
    const token = localStorage.getItem('access_token')

    // 如果存在token，自动添加到请求头
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }

    return config
  },
  (error) => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  (response) => {
    // 直接返回响应数据
    return response.data
  },
  async (error) => {
    console.error('响应错误:', error)

    if (error.response) {
      const { status, data } = error.response

      switch (status) {
        case 401:
          // 未认证或token过期
          ElMessage.error(data.detail || '登录已过期，请重新登录')

          // 清除本地存储
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          localStorage.removeItem('user_info')

          // 跳转到登录页
          router.push('/login')
          break

        case 403:
          // 权限不足
          ElMessage.error(data.detail || '您没有权限执行此操作')
          break

        case 404:
          // 资源未找到
          ElMessage.error(data.detail || '请求的资源不存在')
          break

        case 400:
          // 请求参数错误
          if (typeof data === 'object') {
            // 优先显示后端返回的通用 message
            if (data.message && typeof data.message === 'string') {
              ElMessage.error(data.message)
              break
            }
            // 显示第一个字段的错误信息
            const firstError = Object.values(data)[0]
            ElMessage.error(Array.isArray(firstError) ? firstError[0] : firstError)
          } else {
            ElMessage.error(data.detail || '请求参数错误')
          }
          break

        case 500:
          // 服务器错误
          ElMessage.error('服务器错误，请稍后重试')
          break

        default:
          ElMessage.error(data.detail || '请求失败，请稍后重试')
      }
    } else if (error.request) {
      // 请求发送成功但未收到响应
      ElMessage.error('网络连接失败，请检查网络')
    } else {
      // 其他错误
      ElMessage.error('请求失败：' + error.message)
    }

    return Promise.reject(error)
  }
)

export default service

