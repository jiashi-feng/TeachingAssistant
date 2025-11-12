<template>
  <div class="timesheet-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>工时管理</span>
          <el-button type="primary" :icon="Plus" @click="showSubmitDialog">提交工时表</el-button>
        </div>
      </template>

      <!-- 筛选条件 -->
      <div class="filter-bar">
        <el-select v-model="filters.status" placeholder="状态筛选" clearable style="width: 150px" @change="loadData">
          <el-option label="待审核" value="pending" />
          <el-option label="已批准" value="approved" />
          <el-option label="已驳回" value="rejected" />
        </el-select>
        <el-select v-model="filters.position" placeholder="岗位筛选" clearable style="width: 200px" @change="loadData">
          <el-option
            v-for="pos in positionOptions"
            :key="pos.position_id"
            :label="pos.title"
            :value="pos.position_id"
          />
        </el-select>
        <el-button :icon="Refresh" @click="loadData">刷新</el-button>
      </div>

      <!-- 工时列表 -->
      <el-table :data="list" v-loading="loading" stripe style="margin-top: 16px">
        <el-table-column prop="position_title" label="岗位" min-width="200" />
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
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button
              v-if="row.status === 'pending'"
              type="primary"
              size="small"
              link
              @click="showEditDialog(row)"
            >
              编辑
            </el-button>
            <el-button type="primary" size="small" link @click="viewDetail(row)">
              详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 提交工时表对话框 -->
    <el-dialog v-model="submitDialogVisible" title="提交工时表" width="600px">
      <el-form :model="submitForm" :rules="submitRules" ref="submitFormRef" label-width="100px">
        <el-form-item label="岗位" prop="position">
          <el-select v-model="submitForm.position" placeholder="请选择岗位" style="width: 100%">
            <el-option
              v-for="pos in acceptedPositions"
              :key="pos.position_id"
              :label="`${pos.title} (${pos.course_name})`"
              :value="pos.position_id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="工作月份" prop="month">
          <el-date-picker
            v-model="submitForm.month"
            type="month"
            placeholder="选择月份"
            format="YYYY-MM"
            value-format="YYYY-MM-01"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="工作小时数" prop="hours_worked">
          <el-input-number
            v-model="submitForm.hours_worked"
            :min="0"
            :max="744"
            :precision="2"
            style="width: 100%"
            placeholder="请输入工作小时数"
          />
        </el-form-item>
        <el-form-item label="工作描述" prop="work_description">
          <el-input
            v-model="submitForm.work_description"
            type="textarea"
            :rows="6"
            placeholder="请详细描述本月的工作内容"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="submitDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">提交</el-button>
      </template>
    </el-dialog>

    <!-- 编辑工时表对话框 -->
    <el-dialog v-model="editDialogVisible" title="编辑工时表" width="600px">
      <el-form :model="editForm" :rules="editRules" ref="editFormRef" label-width="100px">
        <el-form-item label="岗位">
          <el-input :value="editForm.position_title" disabled />
        </el-form-item>
        <el-form-item label="工作月份" prop="month">
          <el-date-picker
            v-model="editForm.month"
            type="month"
            placeholder="选择月份"
            format="YYYY-MM"
            value-format="YYYY-MM-01"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="工作小时数" prop="hours_worked">
          <el-input-number
            v-model="editForm.hours_worked"
            :min="0"
            :max="744"
            :precision="2"
            style="width: 100%"
            placeholder="请输入工作小时数"
          />
        </el-form-item>
        <el-form-item label="工作描述" prop="work_description">
          <el-input
            v-model="editForm.work_description"
            type="textarea"
            :rows="6"
            placeholder="请详细描述本月的工作内容"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="editing" @click="handleEdit">保存</el-button>
      </template>
    </el-dialog>

    <!-- 详情对话框 -->
    <el-dialog v-model="detailDialogVisible" title="工时表详情" width="700px">
      <el-descriptions :column="2" border v-if="currentDetail">
        <el-descriptions-item label="岗位">{{ currentDetail.position_title }}</el-descriptions-item>
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
import { Plus, Refresh } from '@element-plus/icons-vue'
import api from '@/api'

const loading = ref(false)
const list = ref([])
const positionOptions = ref([])
const acceptedPositions = ref([])

const filters = reactive({
  status: '',
  position: '',
})

const statusMap = {
  pending: { label: '待审核', type: 'warning' },
  approved: { label: '已批准', type: 'success' },
  rejected: { label: '已驳回', type: 'danger' },
}

// 提交对话框
const submitDialogVisible = ref(false)
const submitFormRef = ref(null)
const submitting = ref(false)
const submitForm = reactive({
  position: null,
  month: '',
  hours_worked: null,
  work_description: '',
})

const submitRules = {
  position: [{ required: true, message: '请选择岗位', trigger: 'change' }],
  month: [{ required: true, message: '请选择工作月份', trigger: 'change' }],
  hours_worked: [
    { required: true, message: '请输入工作小时数', trigger: 'blur' },
    { type: 'number', min: 0, max: 744, message: '小时数必须在0-744之间', trigger: 'blur' },
  ],
  work_description: [{ required: true, message: '请输入工作描述', trigger: 'blur' }],
}

// 编辑对话框
const editDialogVisible = ref(false)
const editFormRef = ref(null)
const editing = ref(false)
const editForm = reactive({
  timesheet_id: null,
  position_title: '',
  month: '',
  hours_worked: null,
  work_description: '',
})

const editRules = {
  month: [{ required: true, message: '请选择工作月份', trigger: 'change' }],
  hours_worked: [
    { required: true, message: '请输入工作小时数', trigger: 'blur' },
    { type: 'number', min: 0, max: 744, message: '小时数必须在0-744之间', trigger: 'blur' },
  ],
  work_description: [{ required: true, message: '请输入工作描述', trigger: 'blur' }],
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
    
    const response = await api.timesheets.getMyTimesheets(params)
    // 修复：axios拦截器已经返回了response.data，所以response本身就是数据
    list.value = response.results || response || []
    
    // 修复：从已通过的岗位和工时列表中合并岗位选项（用于筛选）
    const positions = new Map()
    
    // 先添加已通过的岗位（确保筛选选项包含所有可用岗位）
    acceptedPositions.value.forEach(pos => {
      positions.set(pos.position_id, {
        position_id: pos.position_id,
        title: pos.title,
      })
    })
    
    // 再从工时列表中提取岗位（补充可能遗漏的岗位）
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
    ElMessage.error('加载工时列表失败：' + (error.response?.data?.detail || error.message || '未知错误'))
  } finally {
    loading.value = false
  }
}

// 加载已通过的岗位（用于提交时选择和筛选）
const loadAcceptedPositions = async () => {
  try {
    const response = await api.applications.getMyApplications({ status: 'accepted' })
    // 修复：axios拦截器已经返回了response.data，所以response本身就是数据
    const applications = response.results || response || []
    
    if (applications.length === 0) {
      acceptedPositions.value = []
      positionOptions.value = [] // 同时清空筛选选项
      return
    }
    
    // 获取岗位详情
    const positionIds = applications.map(app => app.position || app.position_id).filter(Boolean)
    const positions = []
    for (const positionId of positionIds) {
      try {
        const posResponse = await api.positions.getPositionDetail(positionId)
        // 修复：axios拦截器已经返回了response.data，所以posResponse本身就是数据
        if (posResponse) {
          positions.push(posResponse)
        }
      } catch (error) {
        console.error('获取岗位详情失败:', error)
      }
    }
    acceptedPositions.value = positions
    
    // 修复：同时更新筛选选项，从已通过的岗位中提取
    positionOptions.value = positions.map(pos => ({
      position_id: pos.position_id,
      title: pos.title,
    }))
  } catch (error) {
    console.error('加载已通过岗位失败:', error)
    ElMessage.error('加载已通过岗位失败，请稍后重试')
  }
}

// 显示提交对话框
const showSubmitDialog = async () => {
  if (acceptedPositions.value.length === 0) {
    await loadAcceptedPositions()
  }
  if (acceptedPositions.value.length === 0) {
    ElMessage.warning('您还没有已通过的岗位，无法提交工时表')
    return
  }
  submitForm.position = null
  submitForm.month = ''
  submitForm.hours_worked = null
  submitForm.work_description = ''
  submitDialogVisible.value = true
}

// 提交工时表
const handleSubmit = async () => {
  if (!submitFormRef.value) return
  
  try {
    await submitFormRef.value.validate()
    submitting.value = true
    
    const data = {
      position: submitForm.position,
      month: submitForm.month, // 格式：YYYY-MM-01
      hours_worked: submitForm.hours_worked,
      work_description: submitForm.work_description,
    }
    
    await api.timesheets.submitTimesheet(data)
    ElMessage.success('提交成功')
    submitDialogVisible.value = false
    loadData()
  } catch (error) {
    if (error.response?.data) {
      const errorData = error.response.data
      if (typeof errorData === 'string') {
        ElMessage.error(errorData)
      } else if (errorData.detail) {
        ElMessage.error(errorData.detail)
      } else {
        // 处理字段错误
        const errorMessages = Object.values(errorData).flat()
        ElMessage.error(errorMessages[0] || '提交失败')
      }
    } else {
      ElMessage.error('提交失败')
    }
  } finally {
    submitting.value = false
  }
}

// 显示编辑对话框
const showEditDialog = (row) => {
  editForm.timesheet_id = row.timesheet_id
  editForm.position_title = row.position_title
  editForm.month = row.month // 格式：YYYY-MM-DD
  editForm.hours_worked = parseFloat(row.hours_worked)
  editForm.work_description = row.work_description
  editDialogVisible.value = true
}

// 编辑工时表
const handleEdit = async () => {
  if (!editFormRef.value) return
  
  try {
    await editFormRef.value.validate()
    editing.value = true
    
    const data = {
      month: editForm.month, // 格式：YYYY-MM-01
      hours_worked: editForm.hours_worked,
      work_description: editForm.work_description,
    }
    
    await api.timesheets.updateTimesheet(editForm.timesheet_id, data)
    ElMessage.success('更新成功')
    editDialogVisible.value = false
    loadData()
  } catch (error) {
    if (error.response?.data) {
      const errorData = error.response.data
      if (typeof errorData === 'string') {
        ElMessage.error(errorData)
      } else if (errorData.detail) {
        ElMessage.error(errorData.detail)
      } else {
        const errorMessages = Object.values(errorData).flat()
        ElMessage.error(errorMessages[0] || '更新失败')
      }
    } else {
      ElMessage.error('更新失败')
    }
  } finally {
    editing.value = false
  }
}

// 查看详情
const viewDetail = async (row) => {
  try {
    const response = await api.timesheets.getTimesheetDetail(row.timesheet_id)
    // 修复：axios拦截器已经返回了response.data，所以response本身就是数据
    currentDetail.value = response
    detailDialogVisible.value = true
  } catch (error) {
    console.error('获取详情失败:', error)
    ElMessage.error('获取详情失败：' + (error.response?.data?.detail || error.message || '未知错误'))
  }
}

onMounted(() => {
  loadData()
  loadAcceptedPositions()
})
</script>

<style scoped>
.timesheet-list {
  padding: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filter-bar {
  display: flex;
  gap: 12px;
  align-items: center;
}
</style>
