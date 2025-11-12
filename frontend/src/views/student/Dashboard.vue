<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <!-- 欢迎卡片 -->
      <el-col :span="24">
        <el-card class="welcome-card">
          <h2>欢迎回来，{{ userStore.userInfo?.real_name }}！</h2>
          <p v-if="userStore.isTA" class="ta-badge">
            <el-tag type="success" size="large">
              <el-icon><Star /></el-icon> 助教
            </el-tag>
          </p>
        </el-card>
      </el-col>
    </el-row>

    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card" @click="goToPositions">
          <div class="stat-icon" style="background-color: #409eff20">
            <el-icon :size="40" color="#409eff"><Briefcase /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ dashboardData.statistics?.available_positions || 0 }}</div>
            <div class="stat-label">可申请岗位</div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card" @click="goToApplications">
          <div class="stat-icon" style="background-color: #67c23a20">
            <el-icon :size="40" color="#67c23a"><Document /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ dashboardData.statistics?.total_applications || 0 }}</div>
            <div class="stat-label">我的申请</div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card" @click="goToApplications">
          <div class="stat-icon" style="background-color: #e6a23c20">
            <el-icon :size="40" color="#e6a23c"><Clock /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ dashboardData.statistics?.pending_applications || 0 }}</div>
            <div class="stat-label">待审核</div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card" @click="goToApplications">
          <div class="stat-icon" style="background-color: #f56c6c20">
            <el-icon :size="40" color="#f56c6c"><CircleCheck /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ dashboardData.statistics?.accepted_applications || 0 }}</div>
            <div class="stat-label">已通过</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 快捷操作 -->
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>快捷操作</span>
            </div>
          </template>
          <div class="quick-actions">
            <el-button type="primary" :icon="Search" @click="goToPositions">
              浏览岗位
            </el-button>
            <el-button type="success" :icon="Document" @click="goToApplications">
              我的申请
            </el-button>
            <el-button v-if="userStore.isTA" type="warning" :icon="Clock" @click="goToTimesheets">
              提交工时
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 最新岗位 -->
    <el-row :gutter="20" class="mt-20">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>最新岗位</span>
              <el-link type="primary" @click="goToPositions">查看全部 →</el-link>
            </div>
          </template>
          <el-table :data="dashboardData.recent_positions" style="width: 100%" v-if="dashboardData.recent_positions?.length">
            <el-table-column prop="title" label="岗位标题" min-width="200" />
            <el-table-column prop="course_name" label="课程" min-width="150" />
            <el-table-column prop="posted_by_name" label="发布教师" width="120" />
            <el-table-column label="截止时间" width="180">
              <template #default="scope">
                {{ formatDate(scope.row.application_deadline) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="100">
              <template #default="scope">
                <el-link type="primary" @click="goToPositionDetail(scope.row.position_id)">查看</el-link>
              </template>
            </el-table-column>
          </el-table>
          <el-empty v-else description="暂无岗位" />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/store/user'
import api from '@/api'
import {
  Briefcase,
  Document,
  Clock,
  CircleCheck,
  Search,
  Star,
} from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

const dashboardData = ref({
  statistics: {},
  recent_positions: [],
  recent_applications: [],
})

const loading = ref(false)

// 格式化日期（使用原生JavaScript）
const formatDate = (dateString) => {
  if (!dateString) return '-'
  try {
    const date = new Date(dateString)
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    return `${year}-${month}-${day}`
  } catch (error) {
    return dateString
  }
}

// 获取看板数据
const fetchDashboardData = async () => {
  loading.value = true
  try {
    const response = await api.positions.getStudentDashboard()
    console.log('看板数据:', response) // 调试用
    dashboardData.value = response
  } catch (error) {
    console.error('获取看板数据失败:', error)
    ElMessage.error('获取看板数据失败')
  } finally {
    loading.value = false
  }
}

const goToPositions = () => {
  router.push('/student/positions')
}

const goToApplications = () => {
  router.push('/student/applications')
}

const goToPositionDetail = (positionId) => {
  router.push(`/student/positions/${positionId}`)
}

const goToTimesheets = () => {
  router.push('/ta/timesheets')
}

onMounted(async () => {
  // 刷新用户信息，确保is_ta状态是最新的
  try {
    await userStore.refreshUserInfo()
  } catch (error) {
    console.error('刷新用户信息失败:', error)
  }
  fetchDashboardData()
})
</script>

<style scoped>
.dashboard {
  padding: 0;
}

.welcome-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  margin-bottom: 20px;
}

.welcome-card h2 {
  margin: 0 0 10px 0;
  font-size: 24px;
}

.ta-badge {
  margin: 10px 0 0 0;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.stat-card :deep(.el-card__body) {
  display: flex;
  align-items: center;
  gap: 20px;
}

.stat-icon {
  width: 70px;
  height: 70px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #999;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.quick-actions {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.mt-20 {
  margin-top: 20px;
}
</style>

