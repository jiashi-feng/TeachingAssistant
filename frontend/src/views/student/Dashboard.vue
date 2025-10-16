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
        <el-card class="stat-card">
          <div class="stat-icon" style="background-color: #409eff20">
            <el-icon :size="40" color="#409eff"><Briefcase /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">12</div>
            <div class="stat-label">可申请岗位</div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card">
          <div class="stat-icon" style="background-color: #67c23a20">
            <el-icon :size="40" color="#67c23a"><Document /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">5</div>
            <div class="stat-label">我的申请</div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card">
          <div class="stat-icon" style="background-color: #e6a23c20">
            <el-icon :size="40" color="#e6a23c"><Clock /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">3</div>
            <div class="stat-label">待审核</div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card">
          <div class="stat-icon" style="background-color: #f56c6c20">
            <el-icon :size="40" color="#f56c6c"><CircleCheck /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">2</div>
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
            <el-button v-if="userStore.isTA" type="warning" :icon="Clock">
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
          <el-empty description="正在开发中..."></el-empty>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
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

const goToPositions = () => {
  router.push('/student/positions')
}

const goToApplications = () => {
  router.push('/student/applications')
}
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

