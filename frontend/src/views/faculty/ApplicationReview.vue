<template>
  <div class="application-review">
    <el-card>
      <template #header>
        <span>申请审核</span>
        <div style="float:right;">
          <el-select v-model="selectedPositionId" filterable placeholder="选择我的岗位" size="small" style="width:260px;margin-right:8px;" @change="loadData">
            <el-option v-for="p in positions" :key="p.position_id" :label="p.title" :value="p.position_id" />
          </el-select>
          <el-button size="small" type="primary" :disabled="!selectedPositionId" @click="loadData">加载申请</el-button>
        </div>
      </template>

      <el-table :data="list" v-loading="loading" stripe>
        <el-table-column prop="position_title" label="岗位" min-width="180" />
        <el-table-column prop="application_id" label="申请ID" width="100" />
        <el-table-column prop="status" label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="row.status==='accepted' ? 'success' : (row.status==='rejected' ? 'danger' : (row.status==='reviewing' ? 'warning' : 'info'))">
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="applied_at" label="申请时间" min-width="180" />
        <el-table-column label="操作" width="280">
          <template #default="{ row }">
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'

const loading = ref(false)
const list = ref([])
const positions = ref([])
const selectedPositionId = ref(null)

const isActionable = (row) => {
  return row.status === 'submitted' || row.status === 'reviewing'
}

const isRevokeEnabled = (row) => {
  return row.status === 'accepted' || row.status === 'rejected'
}

const loadData = async () => {
  if (!selectedPositionId.value) {
    ElMessage.warning('请先选择岗位')
    return
  }
  try {
    loading.value = true
    const data = await api.applications.getPositionApplications(selectedPositionId.value)
    list.value = data.results || data
  } catch (e) {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
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
    if (positions.value.length && !selectedPositionId.value) {
      selectedPositionId.value = positions.value[0].position_id
      loadData()
    }
  } catch (e) {
    // 忽略错误，用户可手动重试
  }
}

const revoke = async (applicationId) => {
  try {
    await ElMessageBox.confirm('确认撤销该申请的审核结果吗？撤销后状态将回到“审核中”。', '提示', { type: 'warning' })
    await api.applications.revokeApplication(applicationId)
    ElMessage.success('已撤销')
    loadData()
  } catch (e) {
    if (e !== 'cancel') {
      ElMessage.error('撤销失败')
    }
  }
}

onMounted(loadMyPositions)
</script>

