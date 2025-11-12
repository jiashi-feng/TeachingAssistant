import request from '@/utils/request'

export default {
  // 通知列表
  getNotifications(params) {
    return request({
      url: '/notifications/',
      method: 'get',
      params,
    })
  },

  // 通知详情（查看时自动标记为已读）
  getNotificationDetail(notificationId) {
    return request({
      url: `/notifications/${notificationId}/`,
      method: 'get',
    })
  },

  // 标记已读
  markAsRead(notificationId) {
    return request({
      url: `/notifications/${notificationId}/read/`,
      method: 'post',
    })
  },

  // 全部标记为已读
  markAllAsRead() {
    return request({
      url: '/notifications/read-all/',
      method: 'post',
    })
  },

  // 未读数量
  getUnreadCount() {
    return request({
      url: '/notifications/unread-count/',
      method: 'get',
    })
  },
}

