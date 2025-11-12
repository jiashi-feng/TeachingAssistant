<template>
  <div class="position-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>浏览岗位</span>
          <div style="float:right;">
            <el-input v-model="keyword" placeholder="搜索岗位/课程" size="small" style="width:220px;margin-right:8px;" @keyup.enter="loadData" />
            <el-button size="small" type="primary" @click="loadData">搜索</el-button>
          </div>
        </div>
      </template>

      <!-- 筛选和排序 -->
      <div class="filter-bar" style="margin-bottom: 16px;">
        <el-row :gutter="16">
          <el-col :span="6">
            <el-select
              v-model="filters.course_code"
              placeholder="筛选课程"
              clearable
              style="width: 100%"
              @change="loadData"
            >
              <el-option
                v-for="course in courseOptions"
                :key="course.code"
                :label="course.name"
                :value="course.code"
              />
            </el-select>
          </el-col>
          <el-col :span="6">
            <el-select
              v-model="filters.posted_by"
              placeholder="筛选发布教师"
              clearable
              style="width: 100%"
              @change="loadData"
            >
              <el-option
                v-for="teacher in teacherOptions"
                :key="teacher.id"
                :label="teacher.name"
                :value="teacher.id"
              />
            </el-select>
          </el-col>
          <el-col :span="6">
            <el-select
              v-model="ordering"
              placeholder="排序方式"
              style="width: 100%"
              @change="loadData"
            >
              <el-option label="最新发布" value="-created_at" />
              <el-option label="最早发布" value="created_at" />
              <el-option label="截止时间（早→晚）" value="application_deadline" />
              <el-option label="截止时间（晚→早）" value="-application_deadline" />
            </el-select>
          </el-col>
          <el-col :span="6">
            <el-button @click="resetFilters">重置筛选</el-button>
          </el-col>
        </el-row>
      </div>

      <el-table :data="list" v-loading="loading" stripe>
        <el-table-column prop="title" label="岗位" min-width="200" />
        <el-table-column prop="course_name" label="课程" min-width="160" />
        <el-table-column prop="application_deadline" label="截止时间" min-width="160" />
        <el-table-column prop="posted_by_name" label="发布者" min-width="120" />
        <el-table-column label="操作" width="120">
          <template #default="{ row }">
            <el-button type="primary" link @click="toDetail(row.position_id)">查看</el-button>
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const loading = ref(false)
const list = ref([])
const page = ref(1)
const pageSize = 20
const total = ref(0)
const keyword = ref('')
const ordering = ref('-created_at')

// 筛选条件
const filters = ref({
  course_code: '',
  posted_by: '',
})

// 筛选选项（从数据中提取）
const courseOptions = ref([])
const teacherOptions = ref([])

// 加载所有数据以获取筛选选项
const loadFilterOptions = async () => {
  try {
    const data = await api.positions.getStudentPositions({
      page_size: 1000, // 获取足够多的数据来提取选项
    })
    const allPositions = data.results || data
    
    // 提取唯一的课程
    const coursesMap = new Map()
    allPositions.forEach(pos => {
      if (pos.course_code && pos.course_name) {
        coursesMap.set(pos.course_code, {
          code: pos.course_code,
          name: `${pos.course_name} (${pos.course_code})`
        })
      }
    })
    courseOptions.value = Array.from(coursesMap.values())
    
    // 提取唯一的发布教师
    const teachersMap = new Map()
    allPositions.forEach(pos => {
      if (pos.posted_by && pos.posted_by_name) {
        teachersMap.set(pos.posted_by, {
          id: pos.posted_by,
          name: pos.posted_by_name
        })
      }
    })
    teacherOptions.value = Array.from(teachersMap.values())
  } catch (e) {
    console.error('加载筛选选项失败:', e)
  }
}

const loadData = async () => {
  try {
    loading.value = true
    const params = {
      page: page.value,
      search: keyword.value || undefined,
      ordering: ordering.value,
    }
    
    // 添加筛选参数
    if (filters.value.course_code) {
      params.course_code = filters.value.course_code
    }
    if (filters.value.posted_by) {
      params.posted_by = filters.value.posted_by
    }
    
    const data = await api.positions.getStudentPositions(params)
    // 兼容后端分页/非分页返回
    list.value = data.results || data
    total.value = data.count || (data.results ? data.results.length : list.value.length)
  } catch (e) {
    ElMessage.error('加载岗位失败')
  } finally {
    loading.value = false
  }
}

// 重置筛选
const resetFilters = () => {
  filters.value = {
    course_code: '',
    posted_by: '',
  }
  keyword.value = ''
  ordering.value = '-created_at'
  page.value = 1
  loadData()
}

const toDetail = (id) => {
  router.push({ name: 'PositionDetail', params: { id } })
}

const onPageChange = (p) => {
  page.value = p
  loadData()
}

onMounted(async () => {
  await loadFilterOptions()
  loadData()
})
</script>

<style scoped>
.card-header {
  font-weight: 600;
}

.filter-bar {
  padding: 12px;
  background-color: #f5f7fa;
  border-radius: 4px;
}
</style>

