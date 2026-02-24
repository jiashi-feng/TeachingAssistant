<template>
  <div class="application-review">
    <el-card>
      <template #header>
        <span>申请审核</span>
        <div style="float:right;">
          <el-select v-model="selectedPositionId" filterable placeholder="选择我的岗位" size="small" style="width:260px;margin-right:8px;" @change="handlePositionChange">
            <el-option label="全部申请" value="all" />
            <el-option v-for="p in positions" :key="p.position_id" :label="p.title" :value="p.position_id" />
          </el-select>
          <el-button size="small" @click="resetFilters">重置筛选</el-button>
        </div>
      </template>

      <el-table :data="list" v-loading="loading" stripe>
        <el-table-column prop="position_title" label="岗位" min-width="180" />
        <el-table-column prop="application_id" label="申请ID" width="100" />
        <el-table-column prop="applicant_name" label="申请人" min-width="120" />
        <el-table-column prop="status" label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="row.status==='accepted' ? 'success' : (row.status==='rejected' ? 'danger' : (row.status==='reviewing' ? 'warning' : 'info'))">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="applied_at" label="申请时间" min-width="180" />
        <el-table-column label="操作" width="440">
          <template #default="{ row }">
            <el-button
              size="small"
              type="primary"
              @click="viewResume(row.application_id)"
            >查看简历</el-button>
            <el-button
              size="small"
              type="info"
              @click="goChatByApplication(row.application_id)"
            >联系学生</el-button>
            <el-button
              size="small"
              type="success"
              :disabled="!isActionable(row)"
              @click="review(row.application_id, 'accept')"
            >通过</el-button>
            <el-button
              size="small"
              type="danger"
              :disabled="!isActionable(row)"
              @click="review(row.application_id, 'reject')"
            >拒绝</el-button>
            <el-button
              size="small"
              type="warning"
              :disabled="!isRevokeEnabled(row)"
              @click="revoke(row.application_id)"
            >撤销</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div style="margin-top:12px; text-align:right;">
        <el-button size="small" @click="loadData">刷新</el-button>
      </div>
    </el-card>

    <!-- 简历查看对话框 -->
    <el-dialog
      v-model="resumeDialogVisible"
      title="查看简历"
      width="70%"
      :close-on-click-modal="false"
    >
      <div v-loading="resumeLoading">
        <div v-if="currentApplication">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="申请人">{{ currentApplication.applicant_name }}</el-descriptions-item>
            <el-descriptions-item label="申请岗位">{{ currentApplication.position_title }}</el-descriptions-item>
            <el-descriptions-item label="申请时间">{{ currentApplication.applied_at }}</el-descriptions-item>
            <el-descriptions-item label="申请状态">
              <el-tag :type="currentApplication.status==='accepted' ? 'success' : (currentApplication.status==='rejected' ? 'danger' : (currentApplication.status==='reviewing' ? 'warning' : 'info'))">
                {{ getStatusText(currentApplication.status) }}
              </el-tag>
            </el-descriptions-item>
          </el-descriptions>

          <el-divider>简历内容</el-divider>

          <!-- 文件简历 -->
          <div v-if="currentApplication.resume_url" style="margin-bottom: 20px;">
            <el-alert
              title="该申请包含简历文件"
              type="info"
              :closable="false"
              style="margin-bottom: 10px;"
            />
            <div>
              <el-button type="primary" @click="downloadResume(currentApplication.resume_url)">
                <el-icon><Download /></el-icon>
                下载简历文件
              </el-button>
              <el-button type="success" @click="previewResume(currentApplication.resume_url)">
                <el-icon><View /></el-icon>
                在线预览
              </el-button>
            </div>
          </div>

          <!-- 在线填写简历 -->
          <div v-if="currentApplication.resume_text">
            <el-alert
              title="在线填写简历"
              type="success"
              :closable="false"
              style="margin-bottom: 10px;"
            />
            <el-card>
              <div style="white-space: pre-wrap; line-height: 1.8; font-size: 14px;">
                {{ currentApplication.resume_text }}
              </div>
            </el-card>
          </div>

          <!-- 无简历提示 -->
          <el-empty v-if="!currentApplication.resume_url && !currentApplication.resume_text" description="该申请未包含简历信息" />
        </div>
      </div>
      <template #footer>
        <el-button @click="resumeDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Download, View } from '@element-plus/icons-vue'

const router = useRouter()

const goChatByApplication = async (applicationId) => {
  try {
    const res = await api.chat.startConversationByApplication(applicationId)
    router.push({ path: '/faculty/chat', query: { conversation_id: res.conversation_id } })
  } catch (e) {
    ElMessage.error(e?.response?.data?.detail || '发起会话失败')
  }
}

const loading = ref(false)
const list = ref([])
const positions = ref([])
const selectedPositionId = ref('all') // 默认显示全部申请
const resumeDialogVisible = ref(false)
const resumeLoading = ref(false)
const currentApplication = ref(null)

const getStatusText = (status) => {
  const statusMap = {
    'submitted': '已提交',
    'reviewing': '审核中',
    'accepted': '已录用',
    'rejected': '已拒绝'
  }
  return statusMap[status] || status
}

const isActionable = (row) => {
  return row.status === 'submitted' || row.status === 'reviewing'
}

const isRevokeEnabled = (row) => {
  return row.status === 'accepted' || row.status === 'rejected'
}

const handlePositionChange = () => {
  // 当选择岗位时立即加载数据
  loadData()
}

const loadData = async () => {
  try {
    loading.value = true
    
    if (selectedPositionId.value === 'all') {
      // 加载所有申请
      const data = await api.applications.getAllApplications()
      list.value = data.results || data
    } else if (selectedPositionId.value) {
      // 加载特定岗位的申请
      const data = await api.applications.getPositionApplications(selectedPositionId.value)
      list.value = data.results || data
    } else {
      list.value = []
    }
  } catch (e) {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

const resetFilters = () => {
  selectedPositionId.value = 'all'
  loadData()
}

const review = async (applicationId, action) => {
  try {
    await ElMessageBox.confirm(`确认要${action === 'accept' ? '通过' : '拒绝'}该申请吗？`, '提示', { type: 'warning' })
    await api.applications.reviewApplication(applicationId, action)
    ElMessage.success('操作成功')
    loadData()
  } catch (e) {
    if (e !== 'cancel') {
      ElMessage.error('操作失败')
    }
  }
}

const loadMyPositions = async () => {
  try {
    const data = await api.positions.getMyPositions({ ordering: '-created_at' })
    positions.value = data.results || data
    // 页面加载时默认显示全部申请
    loadData()
  } catch (e) {
    // 忽略错误，用户可手动重试
  }
}

const revoke = async (applicationId) => {
  try {
    await ElMessageBox.confirm('确认撤销该申请的审核结果吗？撤销后状态将回到"审核中"。', '提示', { type: 'warning' })
    await api.applications.revokeApplication(applicationId)
    ElMessage.success('已撤销')
    loadData()
  } catch (e) {
    if (e !== 'cancel') {
      ElMessage.error('撤销失败')
    }
  }
}

// 查看简历
const viewResume = async (applicationId) => {
  try {
    resumeLoading.value = true
    resumeDialogVisible.value = true
    const data = await api.applications.getApplicationDetail(applicationId)
    currentApplication.value = data
  } catch (e) {
    ElMessage.error('加载简历失败')
    resumeDialogVisible.value = false
  } finally {
    resumeLoading.value = false
  }
}

// 下载简历文件
const downloadResume = (url) => {
  if (!url) {
    ElMessage.warning('简历文件不存在')
    return
  }
  // 创建临时链接下载
  const link = document.createElement('a')
  link.href = url
  link.download = ''
  link.target = '_blank'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  ElMessage.success('开始下载简历文件')
}

// 预览简历文件
const previewResume = (url) => {
  if (!url) {
    ElMessage.warning('简历文件不存在')
    return
  }
  // 在新窗口打开文件
  window.open(url, '_blank')
}

onMounted(loadMyPositions)
</script>