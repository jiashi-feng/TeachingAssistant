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

const loadData = async () => {
  try {
    loading.value = true
    const data = await api.positions.getStudentPositions({
      page: page.value,
      search: keyword.value || undefined,
      ordering: '-created_at',
    })
    // 兼容后端分页/非分页返回
    list.value = data.results || data
    total.value = data.count || (data.results ? data.results.length : list.value.length)
  } catch (e) {
    ElMessage.error('加载岗位失败')
  } finally {
    loading.value = false
  }
}

const toDetail = (id) => {
  router.push({ name: 'PositionDetail', params: { id } })
}

const onPageChange = (p) => {
  page.value = p
  loadData()
}

onMounted(loadData)
</script>

<style scoped>
.card-header {
  font-weight: 600;
}
</style>

