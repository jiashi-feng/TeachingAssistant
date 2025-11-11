<template>
  <div class="position-manage">
    <el-card>
      <template #header>
        <span>岗位管理</span>
        <div style="float:right;">
          <el-input v-model="filters.course_code" placeholder="课程代码" size="small" style="width:140px;margin-right:8px;" />
          <el-select v-model="filters.status" placeholder="状态" size="small" style="width:120px;margin-right:8px;">
            <el-option label="全部" :value="''" />
            <el-option label="开放中" value="open" />
            <el-option label="已关闭" value="closed" />
            <el-option label="已招满" value="filled" />
          </el-select>
          <el-button size="small" type="primary" @click="loadData">查询</el-button>
          <el-button size="small" @click="resetFilters">重置</el-button>
          <el-button size="small" type="success" @click="openCreate">发布岗位</el-button>
        </div>
      </template>

      <el-table :data="list" v-loading="loading" stripe>
        <el-table-column prop="title" label="岗位" min-width="200" />
        <el-table-column prop="course_name" label="课程" min-width="160" />
        <el-table-column prop="course_code" label="代码" width="120" />
        <el-table-column prop="num_filled" label="已录/需求" width="120">
          <template #default="{ row }">{{ row.num_filled }} / {{ row.num_positions }}</template>
        </el-table-column>
        <el-table-column prop="application_deadline" label="截止时间" min-width="160" />
        <el-table-column prop="status" label="状态" width="100" />
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button size="small" :disabled="row.status!=='open'" @click="openEdit(row)">编辑</el-button>
            <el-button size="small" type="danger" :disabled="row.status!=='open'" @click="closePosition(row)">关闭</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div style="margin-top:12px; text-align:right;">
        <el-pagination
          background
          layout="prev, pager, next"
          :page-size="pageSize"
          :total="total"
          :current-page="page"
          @current-change="onPageChange"
        />
      </div>
    </el-card>

    <el-dialog v-model="dialog.visible" :title="dialog.mode==='create'?'发布岗位':'编辑岗位'" width="680px">
      <el-form :model="form" label-width="110px">
        <el-form-item label="岗位标题"><el-input v-model="form.title" /></el-form-item>
        <el-form-item label="课程名称"><el-input v-model="form.course_name" /></el-form-item>
        <el-form-item label="课程代码"><el-input v-model="form.course_code" :disabled="dialog.mode==='edit'" /></el-form-item>
        <el-form-item label="岗位描述"><el-input type="textarea" :rows="4" v-model="form.description" /></el-form-item>
        <el-form-item label="任职要求"><el-input type="textarea" :rows="4" v-model="form.requirements" /></el-form-item>
        <el-form-item label="招聘人数"><el-input type="number" v-model.number="form.num_positions" /></el-form-item>
        <el-form-item label="每周工时"><el-input type="number" v-model.number="form.work_hours_per_week" /></el-form-item>
        <el-form-item label="时薪"><el-input type="number" v-model.number="form.hourly_rate" /></el-form-item>
        <el-form-item label="开始日期"><el-date-picker v-model="form.start_date" type="date" value-format="YYYY-MM-DD" /></el-form-item>
        <el-form-item label="结束日期"><el-date-picker v-model="form.end_date" type="date" value-format="YYYY-MM-DD" /></el-form-item>
        <el-form-item label="截止时间"><el-date-picker v-model="form.application_deadline" type="datetime" value-format="YYYY-MM-DD HH:mm:ss" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialog.visible=false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submitForm">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import api from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'

const loading = ref(false)
const list = ref([])
const page = ref(1)
const pageSize = 20
const total = ref(0)
const filters = reactive({ status: '', course_code: '' })

const dialog = reactive({ visible: false, mode: 'create', currentId: null })
const submitting = ref(false)
const form = reactive({
  title: '', course_name: '', course_code: '', description: '', requirements: '',
  num_positions: 1, work_hours_per_week: 4, hourly_rate: 50,
  start_date: '', end_date: '', application_deadline: '',
})

const resetForm = () => {
  Object.assign(form, {
    title: '', course_name: '', course_code: '', description: '', requirements: '',
    num_positions: 1, work_hours_per_week: 4, hourly_rate: 50,
    start_date: '', end_date: '', application_deadline: '',
  })
}

const loadData = async () => {
  try {
    loading.value = true
    const data = await api.positions.getMyPositions({
      page: page.value,
      status: filters.status || undefined,
      course_code: filters.course_code || undefined,
      ordering: '-created_at',
    })
    list.value = data.results || data
    total.value = data.count || (data.results ? data.results.length : list.value.length)
  } catch (e) {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

const onPageChange = (p) => {
  page.value = p
  loadData()
}

const resetFilters = () => {
  filters.status = ''
  filters.course_code = ''
  page.value = 1
  loadData()
}

const openCreate = () => {
  dialog.mode = 'create'
  dialog.currentId = null
  resetForm()
  dialog.visible = true
}

const openEdit = (row) => {
  dialog.mode = 'edit'
  dialog.currentId = row.position_id
  Object.assign(form, {
    title: row.title, course_name: row.course_name, course_code: row.course_code,
    description: row.description, requirements: row.requirements,
    num_positions: row.num_positions, work_hours_per_week: row.work_hours_per_week,
    hourly_rate: row.hourly_rate, start_date: row.start_date, end_date: row.end_date,
    application_deadline: row.application_deadline,
  })
  dialog.visible = true
}

const submitForm = async () => {
  try {
    submitting.value = true
    if (dialog.mode === 'create') {
      await api.positions.createPosition({ ...form })
      ElMessage.success('发布成功')
    } else {
      await api.positions.updatePosition(dialog.currentId, { ...form })
      ElMessage.success('保存成功')
    }
    dialog.visible = false
    loadData()
  } catch (e) {
    ElMessage.error('提交失败，请检查表单')
  } finally {
    submitting.value = false
  }
}

const closePosition = async (row) => {
  try {
    await ElMessageBox.confirm(`确认关闭岗位「${row.title}」吗？`, '提示', { type: 'warning' })
    await api.positions.closePosition(row.position_id)
    ElMessage.success('已关闭')
    loadData()
  } catch (e) {
    if (e !== 'cancel') {
      ElMessage.error('操作失败')
    }
  }
}

onMounted(loadData)
</script>

<style scoped>
.position-manage :deep(.el-card__header) { font-weight: 600; }
</style>

