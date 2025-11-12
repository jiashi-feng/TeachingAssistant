<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <!-- 欢迎卡片 -->
      <el-col :span="24">
        <el-card class="welcome-card">
          <h2>教师工作台</h2>
          <p>欢迎，{{ userStore.userInfo?.real_name }} 老师</p>
        </el-card>
      </el-col>
    </el-row>

    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card">
          <div class="stat-icon" style="background-color: #409eff20">
            <el-icon :size="40" color="#409eff"><Briefcase /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ dashboardData.statistics?.total_positions || 0 }}</div>
            <div class="stat-label">已发布岗位</div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card" @click="goToApplications">
          <div class="stat-icon" style="background-color: #e6a23c20">
            <el-icon :size="40" color="#e6a23c"><DocumentChecked /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ dashboardData.statistics?.pending_applications || 0 }}</div>
            <div class="stat-label">待审核申请</div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card">
          <div class="stat-icon" style="background-color: #67c23a20">
            <el-icon :size="40" color="#67c23a"><User /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ dashboardData.statistics?.active_tas || 0 }}</div>
            <div class="stat-label">在岗助教</div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card" @click="goToTimesheetReview">
          <div class="stat-icon" style="background-color: #f56c6c20">
            <el-icon :size="40" color="#f56c6c"><Clock /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ dashboardData.statistics?.pending_timesheets || 0 }}</div>
            <div class="stat-label">待审核工时</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 快捷操作 -->
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card>
          <template #header>
            <span class="card-title">快捷操作</span>
          </template>
          <div class="quick-actions">
            <el-button type="primary" :icon="Plus" @click="goToPositionManage">发布新岗位</el-button>
            <el-button type="warning" :icon="DocumentChecked" @click="goToApplications">审核申请</el-button>
            <el-button type="success" :icon="Clock" @click="goToTimesheetReview">审核工时</el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 待办事项 -->
    <el-row :gutter="20" class="mt-20">
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span class="card-title">待审核申请</span>
              <el-link type="primary" @click="goToApplications">查看全部 →</el-link>
            </div>
          </template>
          <el-table :data="dashboardData.recent_applications" style="width: 100%" v-if="dashboardData.recent_applications?.length">
            <el-table-column prop="position_title" label="岗位" />
            <el-table-column prop="applicant_name" label="申请人" />
            <el-table-column prop="status_display" label="状态" />
            <el-table-column label="操作" width="100">
              <template #default="scope">
                <el-link type="primary" @click="goToApplicationReview(scope.row.application_id)">查看</el-link>
              </template>
            </el-table-column>
          </el-table>
          <el-empty v-else description="暂无待审核申请" />
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span class="card-title">待审核工时</span>
              <el-link type="primary" @click="goToTimesheetReview">查看全部 →</el-link>
            </div>
          </template>
          <el-table :data="dashboardData.recent_timesheets" style="width: 100%" v-if="dashboardData.recent_timesheets?.length">
            <el-table-column prop="position_title" label="岗位" />
            <el-table-column prop="ta_name" label="助教" />
            <el-table-column prop="month_display" label="月份" />
            <el-table-column label="操作" width="100">
              <template #default="scope">
                <el-link type="primary" @click="goToTimesheetReview(scope.row.timesheet_id)">审核</el-link>
              </template>
            </el-table-column>
          </el-table>
          <el-empty v-else description="暂无待审核工时" />
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
  DocumentChecked,
  User,
  Clock,
  Plus,
} from '@element-plus/icons-vue'

const userStore = useUserStore()
const router = useRouter()

const dashboardData = ref({
  statistics: {},
  recent_positions: [],
  recent_applications: [],
  recent_timesheets: [],
})

const loading = ref(false)

// 获取看板数据
const fetchDashboardData = async () => {
  loading.value = true
  try {
    const response = await api.positions.getFacultyDashboard()
    dashboardData.value = response
  } catch (error) {
    console.error('获取看板数据失败:', error)
    ElMessage.error('获取看板数据失败')
  } finally {
    loading.value = false
  }
}

// 路由跳转
const goToPositionManage = () => {
  router.push('/faculty/positions')
}

const goToApplications = () => {
  router.push('/faculty/applications')
}

const goToTimesheetReview = (timesheetId) => {
  if (timesheetId) {
    router.push(`/faculty/timesheets?timesheet_id=${timesheetId}`)
  } else {
    router.push('/faculty/timesheets')
  }
}

const goToApplicationReview = (applicationId) => {
  router.push(`/faculty/applications?application_id=${applicationId}`)
}

onMounted(() => {
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

.welcome-card p {
  margin: 0;
  font-size: 14px;
  opacity: 0.9;
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

.card-title {
  font-weight: 600;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
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

