<template>
  <div class="notification-list-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>通知列表</span>
          <div class="header-actions">
            <el-button
              v-if="unreadCount > 0"
              type="primary"
              size="small"
              @click="markAllAsRead"
              :loading="markingAll"
            >
              全部已读
            </el-button>
            <el-button size="small" :icon="Refresh" @click="loadNotifications">刷新</el-button>
          </div>
        </div>
      </template>

      <el-tabs v-model="activeTab" @tab-change="handleTabChange">
        <el-tab-pane label="全部" name="all">
          <template #label>
            <span>全部 <el-badge :value="totalCount" :hidden="totalCount === 0" class="tab-badge" /></span>
          </template>
        </el-tab-pane>
        <el-tab-pane label="未读" name="unread">
          <template #label>
            <span>未读 <el-badge :value="unreadCount" :hidden="unreadCount === 0" type="danger" class="tab-badge" /></span>
          </template>
        </el-tab-pane>
        <el-tab-pane label="系统" name="system" />
        <el-tab-pane label="申请" name="application" />
        <el-tab-pane label="工时" name="timesheet" />
        <el-tab-pane label="薪酬" name="salary" />
      </el-tabs>

      <div class="notification-list" v-loading="loading">
        <div
          v-for="notification in filteredNotifications"
          :key="notification.notification_id"
          class="notification-item"
          :class="{ 'unread': !notification.is_read }"
          @click="handleNotificationClick(notification)"
        >
          <div class="notification-content">
            <div class="notification-title">
              <span class="title-text">{{ notification.title }}</span>
              <el-tag
                v-if="!notification.is_read"
                type="danger"
                size="small"
                effect="plain"
                class="unread-badge"
              >
                未读
              </el-tag>
            </div>
            <div class="notification-message">{{ notification.message }}</div>
            <div class="notification-meta">
              <span class="category-tag">{{ notification.category_display }}</span>
              <span class="sender" v-if="notification.sender_name">来自：{{ notification.sender_name }}</span>
              <span class="time">{{ formatTime(notification.created_at) }}</span>
            </div>
          </div>
          <div class="notification-actions">
            <el-button
              v-if="!notification.is_read"
              type="text"
              size="small"
              @click.stop="markAsRead(notification.notification_id)"
            >
              标记已读
            </el-button>
          </div>
        </div>
        <el-empty
          v-if="!loading && filteredNotifications.length === 0"
          description="暂无通知"
          :image-size="120"
        />
      </div>
    </el-card>

    <!-- 通知详情对话框 -->
    <el-dialog v-model="detailDialogVisible" title="通知详情" width="600px">
      <el-descriptions :column="1" border v-if="currentNotification">
        <el-descriptions-item label="标题">{{ currentNotification.title }}</el-descriptions-item>
        <el-descriptions-item label="发送人">{{ currentNotification.sender_name || '系统' }}</el-descriptions-item>
        <el-descriptions-item label="类型">{{ currentNotification.notification_type_display }}</el-descriptions-item>
        <el-descriptions-item label="分类">{{ currentNotification.category_display }}</el-descriptions-item>
        <el-descriptions-item label="优先级">
          <el-tag :type="getPriorityType(currentNotification.priority)">
            {{ currentNotification.priority_display }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="内容">
          <div style="white-space: pre-wrap;">{{ currentNotification.message }}</div>
        </el-descriptions-item>
        <el-descriptions-item label="时间">{{ formatTime(currentNotification.created_at) }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="currentNotification.is_read ? 'success' : 'warning'">
            {{ currentNotification.is_read ? '已读' : '未读' }}
          </el-tag>
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import api from '@/api'

const loading = ref(false)
const markingAll = ref(false)
const notifications = ref([])
const unreadCount = ref(0)
const activeTab = ref('all')
const detailDialogVisible = ref(false)
const currentNotification = ref(null)

// 筛选后的通知列表
const filteredNotifications = computed(() => {
  let filtered = notifications.value

  // 按标签筛选
  if (activeTab.value === 'unread') {
    filtered = filtered.filter(n => !n.is_read)
  } else if (activeTab.value !== 'all') {
    filtered = filtered.filter(n => n.category === activeTab.value)
  }

  // 未读优先，然后按时间倒序
  return filtered.sort((a, b) => {
    if (a.is_read !== b.is_read) {
      return a.is_read ? 1 : -1
    }
    return new Date(b.created_at) - new Date(a.created_at)
  })
})

// 总数量
const totalCount = computed(() => notifications.value.length)

// 加载通知列表
const loadNotifications = async () => {
  try {
    loading.value = true
    const response = await api.notifications.getNotifications({
      ordering: '-created_at',
    })
    notifications.value = response.results || response || []
  } catch (error) {
    console.error('加载通知失败:', error)
    ElMessage.error('加载通知失败')
  } finally {
    loading.value = false
  }
}

// 加载未读数量
const loadUnreadCount = async () => {
  try {
    const response = await api.notifications.getUnreadCount()
    unreadCount.value = response.total_unread || 0
  } catch (error) {
    console.error('加载未读数量失败:', error)
  }
}

// 标记为已读
const markAsRead = async (notificationId) => {
  try {
    await api.notifications.markAsRead(notificationId)
    const notification = notifications.value.find(n => n.notification_id === notificationId)
    if (notification) {
      notification.is_read = true
      notification.read_at = new Date().toISOString()
    }
    unreadCount.value = Math.max(0, unreadCount.value - 1)
    ElMessage.success('已标记为已读')
  } catch (error) {
    ElMessage.error('标记失败')
  }
}

// 全部标记为已读
const markAllAsRead = async () => {
  try {
    markingAll.value = true
    await api.notifications.markAllAsRead()
    notifications.value.forEach(n => {
      n.is_read = true
      n.read_at = new Date().toISOString()
    })
    unreadCount.value = 0
    ElMessage.success('已全部标记为已读')
  } catch (error) {
    ElMessage.error('操作失败')
  } finally {
    markingAll.value = false
  }
}

// 点击通知
const handleNotificationClick = async (notification) => {
  try {
    const response = await api.notifications.getNotificationDetail(notification.notification_id)
    currentNotification.value = response
    
    if (!notification.is_read) {
      notification.is_read = true
      notification.read_at = response.read_at
      unreadCount.value = Math.max(0, unreadCount.value - 1)
    }
    
    detailDialogVisible.value = true
  } catch (error) {
    ElMessage.error('获取详情失败')
  }
}

// 标签切换
const handleTabChange = () => {
  // 标签切换时不需要重新加载数据，computed会自动更新
}

// 格式化时间
const formatTime = (timeStr) => {
  if (!timeStr) return ''
  const time = new Date(timeStr)
  const now = new Date()
  const diff = now - time
  
  if (diff < 60000) {
    return '刚刚'
  } else if (diff < 3600000) {
    return `${Math.floor(diff / 60000)}分钟前`
  } else if (diff < 86400000) {
    return `${Math.floor(diff / 3600000)}小时前`
  } else if (diff < 604800000) {
    return `${Math.floor(diff / 86400000)}天前`
  } else {
    return time.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  }
}

// 获取优先级类型
const getPriorityType = (priority) => {
  const map = {
    low: 'info',
    medium: '',
    high: 'warning',
    urgent: 'danger',
  }
  return map[priority] || ''
}

onMounted(() => {
  loadNotifications()
  loadUnreadCount()
})
</script>

<style scoped>
.notification-list-page {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.tab-badge {
  margin-left: 4px;
}

.notification-list {
  margin-top: 20px;
  min-height: 400px;
}

.notification-item {
  display: flex;
  justify-content: space-between;
  padding: 16px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: background-color 0.2s;
}

.notification-item:hover {
  background-color: #f5f7fa;
}

.notification-item.unread {
  background-color: #ecf5ff;
}

.notification-item.unread:hover {
  background-color: #d9ecff;
}

.notification-content {
  flex: 1;
  min-width: 0;
}

.notification-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.title-text {
  font-weight: 600;
  font-size: 15px;
  color: #303133;
}

.unread-badge {
  flex-shrink: 0;
}

.notification-message {
  font-size: 14px;
  color: #606266;
  line-height: 1.6;
  margin-bottom: 10px;
}

.notification-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 12px;
  color: #909399;
}

.category-tag {
  padding: 2px 8px;
  background-color: #f0f0f0;
  border-radius: 3px;
}

.sender {
  color: #909399;
}

.time {
  margin-left: auto;
}

.notification-actions {
  flex-shrink: 0;
  margin-left: 16px;
}
</style>

