<template>
  <div class="application-list">
    <el-card>
      <template #header>
        <span>我的申请</span>
      </template>

      <el-table :data="list" v-loading="loading" stripe>
        <el-table-column prop="position_title" label="岗位" min-width="220" />
        <el-table-column prop="status" label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="statusMap[row.status]?.type || 'info'">
              {{ statusMap[row.status]?.label || row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="applied_at" label="申请时间" min-width="180" />
      </el-table>

      <div style="margin-top:12px; text-align:right;">
        <el-button size="small" type="primary" @click="loadData">刷新</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const list = ref([])

const statusMap = {
  submitted: { label: '已提交', type: 'info' },
  reviewing: { label: '审核中', type: 'warning' },
  accepted: { label: '已录用', type: 'success' },
  rejected: { label: '已拒绝', type: 'danger' },
}

const loadData = async () => {
  try {
    loading.value = true
    const data = await api.applications.getMyApplications()
    list.value = data.results || data
  } catch (e) {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

onMounted(loadData)
</script>

