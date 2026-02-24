import request from '@/utils/request'

export default {
  getConversations(params) {
    return request({
      url: '/chat/conversations/',
      method: 'get',
      params,
    })
  },

  startConversationByPosition(positionId) {
    return request({
      url: '/chat/start/',
      method: 'post',
      data: { position_id: positionId },
    })
  },

  startConversationByApplication(applicationId) {
    return request({
      url: '/chat/start/',
      method: 'post',
      data: { application_id: applicationId },
    })
  },

  startConversationByTimesheet(timesheetId) {
    return request({
      url: '/chat/start/',
      method: 'post',
      data: { timesheet_id: timesheetId },
    })
  },

  getMessages(conversationId, params) {
    return request({
      url: `/chat/conversations/${conversationId}/messages/`,
      method: 'get',
      params,
    })
  },

  sendMessage(conversationId, content) {
    return request({
      url: `/chat/conversations/${conversationId}/send/`,
      method: 'post',
      data: { content },
    })
  },
}
