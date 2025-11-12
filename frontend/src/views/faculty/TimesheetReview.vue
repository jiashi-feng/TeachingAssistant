<template>
  <div class="timesheet-review">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>工时审核</span>
          <div class="header-actions">
            <el-select
              v-model="filters.position"
              filterable
              placeholder="岗位筛选"
              clearable
              size="small"
              style="width: 200px; margin-right: 8px"
              @change="loadData"
            >
              <el-option
                v-for="p in positionOptions"
                :key="p.position_id"
                :label="p.title"
                :value="p.position_id"
              />
            </el-select>
            <el-select
              v-model="filters.status"
              placeholder="状态筛选"
              clearable
              size="small"
              style="width: 120px; margin-right: 8px"
              @change="loadData"
            >
              <el-option label="待审核" value="pending" />
              <el-option label="已批准" value="approved" />
              <el-option label="已驳回" value="rejected" />
            </el-select>
            <el-button size="small" type="primary" :icon="Refresh" @click="loadData">刷新</el-button>
          </div>
        </div>
      </template>

      <!-- 工时列表 -->
      <el-table :data="list" v-loading="loading" stripe>
        <el-table-column prop="position_title" label="岗位" min-width="200" />
        <el-table-column prop="ta_name" label="助教" width="120" />
        <el-table-column prop="month_display" label="工作月份" width="120" />
        <el-table-column prop="hours_worked" label="工时（小时）" width="120" align="right" />
        <el-table-column prop="status_display" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="statusMap[row.status]?.type || 'info'">
              {{ statusMap[row.status]?.label || row.status_display }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="submitted_at" label="提交时间" width="180" />
        <el-table-column prop="reviewed_by_name" label="审核人" width="100" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button
              v-if="row.status === 'pending'"
              size="small"
              type="success"
              @click="showReviewDialog(row, 'approve')"
            >
              批准
            </el-button>
            <el-button
              v-if="row.status === 'pending'"
              size="small"
              type="danger"
              @click="showReviewDialog(row, 'reject')"
            >
              驳回
            </el-button>
            <el-button size="small" type="primary" link @click="viewDetail(row)">
              详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-empty v-if="!loading && list.length === 0" description="暂无工时记录" />
    </el-card>

    <!-- 审核对话框 -->
    <el-dialog
      v-model="reviewDialogVisible"
      :title="reviewAction === 'approve' ? '批准工时表' : '驳回工时表'"
      width="600px"
    >
      <el-form :model="reviewForm" :rules="reviewRules" ref="reviewFormRef" label-width="100px">
        <el-form-item label="岗位">
          <el-input :value="reviewForm.position_title" disabled />
        </el-form-item>
        <el-form-item label="助教">
          <el-input :value="reviewForm.ta_name" disabled />
        </el-form-item>
        <el-form-item label="工作月份">
          <el-input :value="reviewForm.month_display" disabled />
        </el-form-item>
        <el-form-item label="工作小时数">
          <el-input :value="reviewForm.hours_worked + ' 小时'" disabled />
        </el-form-item>
        <el-form-item label="工作描述">
          <el-input :value="reviewForm.work_description" type="textarea" :rows="4" disabled />
        </el-form-item>
        <el-form-item label="审核备注" prop="review_notes">
          <el-input
            v-model="reviewForm.review_notes"
            type="textarea"
            :rows="4"
            :placeholder="reviewAction === 'approve' ? '请输入批准备注（可选）' : '请输入驳回原因（建议填写）'"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="reviewDialogVisible = false">取消</el-button>
        <el-button
          :type="reviewAction === 'approve' ? 'success' : 'danger'"
          :loading="reviewing"
          @click="handleReview"
        >
          {{ reviewAction === 'approve' ? '确认批准' : '确认驳回' }}
        </el-button>
      </template>
    </el-dialog>

    <!-- 详情对话框 -->
    <el-dialog v-model="detailDialogVisible" title="工时表详情" width="700px">
      <el-descriptions :column="2" border v-if="currentDetail">
        <el-descriptions-item label="岗位">{{ currentDetail.position_title }}</el-descriptions-item>
        <el-descriptions-item label="助教">{{ currentDetail.ta_name }}</el-descriptions-item>
        <el-descriptions-item label="工作月份">{{ currentDetail.month_display }}</el-descriptions-item>
        <el-descriptions-item label="工作小时数">{{ currentDetail.hours_worked }} 小时</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="statusMap[currentDetail.status]?.type || 'info'">
            {{ statusMap[currentDetail.status]?.label || currentDetail.status_display }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="提交时间">{{ currentDetail.submitted_at }}</el-descriptions-item>
        <el-descriptions-item label="审核人">{{ currentDetail.reviewed_by_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="审核时间">{{ currentDetail.reviewed_at || '-' }}</el-descriptions-item>
        <el-descriptions-item label="审核备注" :span="2">{{ currentDetail.review_notes || '-' }}</el-descriptions-item>
        <el-descriptions-item label="工作描述" :span="2">
          <div style="white-space: pre-wrap;">{{ currentDetail.work_description }}</div>
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import api from '@/api'

const loading = ref(false)
const list = ref([])
const positionOptions = ref([])

const filters = reactive({
  status: '',
  position: '',
})

const statusMap = {
  pending: { label: '待审核', type: 'warning' },
  approved: { label: '已批准', type: 'success' },
  rejected: { label: '已驳回', type: 'danger' },
}

// 审核对话框
const reviewDialogVisible = ref(false)
const reviewFormRef = ref(null)
const reviewing = ref(false)
const reviewAction = ref('approve') // 'approve' 或 'reject'
const reviewForm = reactive({
  timesheet_id: null,
  position_title: '',
  ta_name: '',
  month_display: '',
  hours_worked: null,
  work_description: '',
  review_notes: '',
})

const reviewRules = {
  review_notes: [
    {
      validator: (rule, value, callback) => {
        if (reviewAction.value === 'reject' && !value?.trim()) {
          callback(new Error('驳回时必须填写驳回原因'))
        } else {
          callback()
        }
      },
      trigger: 'blur',
    },
  ],
}

// 详情对话框
const detailDialogVisible = ref(false)
const currentDetail = ref(null)

// 加载数据
const loadData = async () => {
  try {
    loading.value = true
    const params = {}
    if (filters.status) params.status = filters.status
    if (filters.position) params.position = filters.position
    
    const response = await api.timesheets.getFacultyTimesheets(params)
    // axios 拦截器已返回 data，这里直接使用 response
    list.value = response.results || response || []
    
    // 提取岗位选项（用于筛选）
    const positions = new Map()
    list.value.forEach(item => {
      if (item.position && !positions.has(item.position)) {
        positions.set(item.position, {
          position_id: item.position,
          title: item.position_title,
        })
      }
    })
    positionOptions.value = Array.from(positions.values())
  } catch (error) {
    console.error('加载失败:', error)
    ElMessage.error('加载工时列表失败')
  } finally {
    loading.value = false
  }
}

// 加载岗位列表（用于筛选）
const loadPositions = async () => {
  try {
    const response = await api.positions.getMyPositions()
    const positions = response.results || response || []
    positionOptions.value = positions.map(p => ({
      position_id: p.position_id,
      title: p.title,
    }))
  } catch (error) {
    console.error('加载岗位列表失败:', error)
  }
}

// 显示审核对话框
const showReviewDialog = (row, action) => {
  reviewAction.value = action
  reviewForm.timesheet_id = row.timesheet_id
  reviewForm.position_title = row.position_title
  reviewForm.ta_name = row.ta_name
  reviewForm.month_display = row.month_display
  reviewForm.hours_worked = parseFloat(row.hours_worked)
  reviewForm.work_description = row.work_description
  reviewForm.review_notes = ''
  reviewDialogVisible.value = true
}

// 执行审核
const handleReview = async () => {
  if (!reviewFormRef.value) return
  
  try {
    await reviewFormRef.value.validate()
    
    const actionText = reviewAction.value === 'approve' ? '批准' : '驳回'
    await ElMessageBox.confirm(
      `确认要${actionText}该工时表吗？`,
      '提示',
      { type: 'warning' }
    )
    
    reviewing.value = true
    
    // 调用审核API，参数：action (approve/reject), review_notes (可选)
    const data = {
      action: reviewAction.value, // 'approve' 或 'reject'
      review_notes: reviewForm.review_notes || '', // 可选，但驳回时建议填写
    }
    
    await api.timesheets.reviewTimesheet(reviewForm.timesheet_id, data)
    ElMessage.success(`${actionText}成功`)
    reviewDialogVisible.value = false
    loadData()
  } catch (error) {
    if (error === 'cancel') {
      return
    }
    
    if (error.response?.data) {
      const errorData = error.response.data
      if (typeof errorData === 'string') {
        ElMessage.error(errorData)
      } else if (errorData.detail) {
        ElMessage.error(errorData.detail)
      } else {
        const errorMessages = Object.values(errorData).flat()
        ElMessage.error(errorMessages[0] || '审核失败')
      }
    } else {
      ElMessage.error('审核失败')
    }
  } finally {
    reviewing.value = false
  }
}

// 查看详情
const viewDetail = async (row) => {
  try {
    // 教师端详情接口
    const response = await api.timesheets.getFacultyTimesheetDetail(row.timesheet_id)
    currentDetail.value = response
    detailDialogVisible.value = true
  } catch (error) {
    ElMessage.error('获取详情失败')
  }
}

onMounted(() => {
  loadData()
  loadPositions()
})
</script>

<style scoped>
.timesheet-review {
  padding: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  align-items: center;
}
</style>
