<template>
  <div class="position-detail">
    <el-card v-loading="loading">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-button 
              type="text" 
              :icon="ArrowLeft" 
              @click="goBack"
              style="margin-right: 12px;"
            >
              返回
            </el-button>
            <span>{{ detail?.title || '岗位详情' }}</span>
          </div>
        </div>
      </template>

      <div v-if="detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="课程">{{ detail.course_name }} ({{ detail.course_code }})</el-descriptions-item>
          <el-descriptions-item label="发布者">{{ detail.posted_by_name }}</el-descriptions-item>
          <el-descriptions-item label="截止时间">{{ detail.application_deadline }}</el-descriptions-item>
          <el-descriptions-item label="每周工时">{{ detail.work_hours_per_week }}</el-descriptions-item>
          <el-descriptions-item label="时薪">{{ detail.hourly_rate }}</el-descriptions-item>
          <el-descriptions-item label="人数">{{ detail.num_filled }} / {{ detail.num_positions }}</el-descriptions-item>
        </el-descriptions>

        <el-card style="margin-top:16px;">
          <template #header>职责描述</template>
          <div class="mono">{{ detail.description }}</div>
        </el-card>

        <el-card style="margin-top:16px;">
          <template #header>任职要求</template>
          <div class="mono">{{ detail.requirements }}</div>
        </el-card>

        <el-divider />

        <div class="apply-area">
          <!-- 检查岗位是否过期或已关闭 -->
          <div v-if="isExpired || isClosed" style="margin-bottom: 16px;">
            <el-alert
              :title="isExpired ? '该岗位申请已过期' : '该岗位已关闭'"
              type="warning"
              :closable="false"
              show-icon
            />
          </div>
          
          <template v-else>
            <el-segmented v-model="applyMode" :options="[{label:'在线填写',value:'text'},{label:'上传文件',value:'file'}]" />

            <div v-if="applyMode==='text'" style="margin-top:12px;">
              <el-input
                type="textarea"
                v-model="resumeText"
                :rows="8"
                placeholder="请输入简历文本（教育经历、项目、技能等）"
              />
            </div>
            <div v-else style="margin-top:12px;">
              <el-upload
                :auto-upload="false"
                :limit="1"
                :on-change="onFileChange"
                :before-upload="() => false"
              >
                <el-button type="primary">选择简历文件</el-button>
                <template #tip>
                  <div class="el-upload__tip">支持 PDF/DOC/DOCX，最大 10MB</div>
                </template>
              </el-upload>
              <div v-if="fileName" style="margin-top:6px;color:#666;">已选择：{{ fileName }}</div>
            </div>

            <div style="margin-top:12px;">
              <el-button type="primary" :loading="submitting" @click="submit">投递申请</el-button>
            </div>
          </template>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'
import api from '@/api'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const id = Number(route.params.id)
const loading = ref(false)
const detail = ref(null)

// 计算属性：检查岗位是否过期
const isExpired = computed(() => {
  if (!detail.value || !detail.value.application_deadline) return false
  return new Date(detail.value.application_deadline) < new Date()
})

// 计算属性：检查岗位是否已关闭
const isClosed = computed(() => {
  if (!detail.value) return false
  return detail.value.status !== 'open'
})

// 返回岗位列表页
const goBack = () => {
  router.push('/student/positions')
}

const applyMode = ref('text')
const resumeText = ref('')
const selectedFile = ref(null)
const fileName = ref('')
const submitting = ref(false)

const loadDetail = async () => {
  loading.value = true
  try {
    const data = await api.positions.getPositionDetail(id)
    detail.value = data
  } catch (e) {
    ElMessage.error('加载详情失败')
  } finally {
    loading.value = false
  }
}

const onFileChange = (file) => {
  selectedFile.value = file.raw
  fileName.value = file.name
}

const submit = async () => {
  try {
    submitting.value = true
    const payload = {
      position: id,
      resumeText: applyMode.value === 'text' ? resumeText.value : undefined,
      file: applyMode.value === 'file' ? selectedFile.value : undefined,
    }
    await api.applications.submitApplication(payload)
    ElMessage.success('申请已提交')
    resumeText.value = ''
    selectedFile.value = null
    fileName.value = ''
    // 跳转到申请列表页面
    router.push('/student/applications')
  } catch (e) {
    const errorMsg = e?.response?.data?.detail || e?.response?.data?.message || '提交失败，请检查输入'
    ElMessage.error(errorMsg)
  } finally {
    submitting.value = false
  }
}

onMounted(loadDetail)
</script>

<style scoped>
.card-header {
  font-weight: 600;
  display: flex;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
}

.mono {
  white-space: pre-wrap;
  line-height: 1.6;
}
.apply-area {
  margin-top: 12px;
}
</style>

