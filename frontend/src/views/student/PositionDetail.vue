<template>
  <div class="position-detail">
    <el-card v-loading="loading">
      <template #header>
        <div class="card-header">
          <span>{{ detail?.title || '岗位详情' }}</span>
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
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/api'
import { ElMessage } from 'element-plus'

const route = useRoute()
const id = Number(route.params.id)
const loading = ref(false)
const detail = ref(null)

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
  } catch (e) {
    ElMessage.error(e?.response?.data?.detail || '提交失败，请检查输入')
  } finally {
    submitting.value = false
  }
}

onMounted(loadDetail)
</script>

<style scoped>
.card-header {
  font-weight: 600;
}
.mono {
  white-space: pre-wrap;
  line-height: 1.6;
}
.apply-area {
  margin-top: 12px;
}
</style>

