<template>
  <div class="salary-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>薪酬记录</span>
          <el-button :icon="Refresh" @click="loadData">刷新</el-button>
        </div>
      </template>

      <!-- 统计信息 -->
      <div class="statistics-bar" v-if="statistics.total > 0">
        <el-statistic title="总薪酬" :value="statistics.total" :precision="2">
          <template #prefix>¥</template>
        </el-statistic>
        <el-statistic title="已支付" :value="statistics.paid" :precision="2">
          <template #prefix>¥</template>
        </el-statistic>
        <el-statistic title="待支付" :value="statistics.pending" :precision="2">
          <template #prefix>¥</template>
        </el-statistic>
      </div>

      <!-- 薪酬列表 -->
      <el-table :data="list" v-loading="loading" stripe style="margin-top: 16px">
        <el-table-column prop="timesheet_month" label="工作月份" width="120" />
        <el-table-column prop="position_title" label="岗位" min-width="200" />
        <el-table-column prop="position_course_name" label="课程" min-width="150" />
        <el-table-column prop="amount" label="薪酬金额" width="120" align="right">
          <template #default="{ row }">
            <span class="amount-text">¥{{ formatAmount(row.amount) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="payment_status_display" label="支付状态" width="100">
          <template #default="{ row }">
            <el-tag :type="paymentStatusMap[row.payment_status]?.type || 'info'">
              {{ paymentStatusMap[row.payment_status]?.label || row.payment_status_display }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="generated_at" label="生成时间" width="180" />
        <el-table-column prop="paid_at" label="支付时间" width="180">
          <template #default="{ row }">
            {{ row.paid_at || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" link @click="viewDetail(row)">
              详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-empty v-if="!loading && list.length === 0" description="暂无薪酬记录" />
    </el-card>

    <!-- 详情对话框 -->
    <el-dialog v-model="detailDialogVisible" title="薪酬详情" width="800px">
      <el-descriptions :column="2" border v-if="currentDetail">
        <el-descriptions-item label="薪酬ID">{{ currentDetail.salary_id }}</el-descriptions-item>
        <el-descriptions-item label="工作月份">{{ currentDetail.timesheet_month }}</el-descriptions-item>
        <el-descriptions-item label="岗位">{{ currentDetail.position_title }}</el-descriptions-item>
        <el-descriptions-item label="课程">
          {{ currentDetail.position_course_name }} ({{ currentDetail.position_course_code }})
        </el-descriptions-item>
        <el-descriptions-item label="工作小时数">{{ currentDetail.timesheet_hours }} 小时</el-descriptions-item>
        <el-descriptions-item label="时薪">¥{{ formatAmount(currentDetail.position_hourly_rate) }}/小时</el-descriptions-item>
        <el-descriptions-item label="薪酬金额" :span="2">
          <span class="amount-text-large">¥{{ formatAmount(currentDetail.amount) }}</span>
        </el-descriptions-item>
        <el-descriptions-item label="支付状态">
          <el-tag :type="paymentStatusMap[currentDetail.payment_status]?.type || 'info'">
            {{ paymentStatusMap[currentDetail.payment_status]?.label || currentDetail.payment_status_display }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="生成时间">{{ currentDetail.generated_at }}</el-descriptions-item>
        <el-descriptions-item label="生成人">{{ currentDetail.generated_by_name }}</el-descriptions-item>
        <el-descriptions-item label="支付时间">{{ currentDetail.paid_at || '-' }}</el-descriptions-item>
        <el-descriptions-item label="支付方式">{{ currentDetail.payment_method || '-' }}</el-descriptions-item>
        <el-descriptions-item label="交易流水号">{{ currentDetail.transaction_id || '-' }}</el-descriptions-item>
        
        <!-- 计算明细 -->
        <el-descriptions-item label="计算明细" :span="2" v-if="currentDetail.calculation_details">
          <el-card style="margin-top: 8px;">
            <div class="calculation-details">
              <div class="detail-item">
                <span class="label">工作小时数：</span>
                <span class="value">{{ currentDetail.calculation_details.hours }} 小时</span>
              </div>
              <div class="detail-item">
                <span class="label">时薪：</span>
                <span class="value">¥{{ formatAmount(currentDetail.calculation_details.rate) }}/小时</span>
              </div>
              <div class="detail-item formula">
                <span class="label">计算公式：</span>
                <span class="value">{{ currentDetail.calculation_details.formula }}</span>
              </div>
              <div class="detail-item result">
                <span class="label">计算结果：</span>
                <span class="value">¥{{ formatAmount(currentDetail.amount) }}</span>
              </div>
            </div>
          </el-card>
        </el-descriptions-item>
        
        <!-- 工作描述 -->
        <el-descriptions-item label="工作描述" :span="2">
          <div class="work-description">{{ currentDetail.timesheet_description }}</div>
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import api from '@/api'

const loading = ref(false)
const list = ref([])

const paymentStatusMap = {
  pending: { label: '待支付', type: 'warning' },
  paid: { label: '已支付', type: 'success' },
}

// 统计信息
const statistics = computed(() => {
  const total = list.value.reduce((sum, item) => sum + parseFloat(item.amount || 0), 0)
  const paid = list.value
    .filter(item => item.payment_status === 'paid')
    .reduce((sum, item) => sum + parseFloat(item.amount || 0), 0)
  const pending = total - paid
  
  return {
    total: total.toFixed(2),
    paid: paid.toFixed(2),
    pending: pending.toFixed(2),
  }
})

// 详情对话框
const detailDialogVisible = ref(false)
const currentDetail = ref(null)

// 格式化金额
const formatAmount = (amount) => {
  if (!amount) return '0.00'
  return parseFloat(amount).toFixed(2)
}

// 加载数据
const loadData = async () => {
  try {
    loading.value = true
    const response = await api.timesheets.getMySalaries()
    // 修复：axios拦截器已经返回了response.data，所以response本身就是数据
    list.value = response.results || response || []
  } catch (error) {
    console.error('加载失败:', error)
    ElMessage.error('加载薪酬记录失败：' + (error.response?.data?.detail || error.message || '未知错误'))
  } finally {
    loading.value = false
  }
}

// 查看详情
const viewDetail = async (row) => {
  try {
    const response = await api.timesheets.getSalaryDetail(row.salary_id)
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
})
</script>

<style scoped>
.salary-list {
  padding: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.statistics-bar {
  display: flex;
  gap: 40px;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
  margin-bottom: 16px;
}

.amount-text {
  font-weight: 600;
  color: #409eff;
  font-size: 14px;
}

.amount-text-large {
  font-weight: 700;
  color: #409eff;
  font-size: 20px;
}

.calculation-details {
  padding: 12px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.detail-item:last-child {
  border-bottom: none;
}

.detail-item.formula {
  background: #f5f7fa;
  padding: 12px;
  border-radius: 4px;
  margin: 8px 0;
}

.detail-item.result {
  font-size: 16px;
  font-weight: 600;
  color: #409eff;
  margin-top: 8px;
}

.detail-item .label {
  color: #666;
}

.detail-item .value {
  color: #333;
  font-weight: 500;
}

.work-description {
  white-space: pre-wrap;
  line-height: 1.6;
  color: #666;
  padding: 8px;
  background: #f9f9f9;
  border-radius: 4px;
}
</style>
