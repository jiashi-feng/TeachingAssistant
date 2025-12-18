<template>
  <div class="settings-container">
    <el-card class="settings-card">
      <template #header>
        <div class="card-header">
          <span>设置</span>
        </div>
      </template>

      <!-- 修改密码 -->
      <el-card shadow="never" class="section-card">
        <template #header>
          <div class="section-header">
            <el-icon><Lock /></el-icon>
            <span>修改密码</span>
          </div>
        </template>

        <el-form
          ref="passwordFormRef"
          :model="passwordForm"
          :rules="passwordRules"
          label-width="120px"
          class="password-form"
        >
          <el-form-item label="当前密码" prop="old_password">
            <el-input
              v-model="passwordForm.old_password"
              type="password"
              placeholder="请输入当前密码"
              show-password
              clearable
            />
          </el-form-item>

          <el-form-item label="新密码" prop="new_password">
            <el-input
              v-model="passwordForm.new_password"
              type="password"
              placeholder="请输入新密码（至少8位，包含大小写字母和数字）"
              show-password
              clearable
            />
            <!-- 密码强度指示器 -->
            <div v-if="passwordForm.new_password" class="password-strength">
              <div
                class="strength-bar"
                :class="passwordStrengthClass"
                :style="{ width: passwordStrengthWidth }"
              ></div>
              <span class="strength-text">{{ passwordStrengthText }}</span>
            </div>
          </el-form-item>

          <el-form-item label="确认新密码" prop="new_password_confirm">
            <el-input
              v-model="passwordForm.new_password_confirm"
              type="password"
              placeholder="请再次输入新密码"
              show-password
              clearable
            />
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              :loading="changingPassword"
              @click="handleChangePassword"
            >
              修改密码
            </el-button>
            <el-button @click="resetPasswordForm">重置</el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <!-- 其他设置（可选扩展） -->
      <el-card shadow="never" class="section-card" style="margin-top: 20px">
        <template #header>
          <div class="section-header">
            <el-icon><Setting /></el-icon>
            <span>其他设置</span>
          </div>
        </template>
        <p style="color: #909399; margin: 0">更多设置功能即将上线...</p>
      </el-card>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Lock, Setting } from '@element-plus/icons-vue'
import api from '@/api'

const router = useRouter()
const userStore = useUserStore()

const passwordFormRef = ref(null)
const changingPassword = ref(false)

// 密码表单
const passwordForm = reactive({
  old_password: '',
  new_password: '',
  new_password_confirm: '',
})

// 密码强度计算
const passwordStrength = computed(() => {
  const pwd = passwordForm.new_password
  if (!pwd) return 0

  let strength = 0
  if (pwd.length >= 8) strength++
  if (pwd.length >= 12) strength++
  if (/[a-z]/.test(pwd)) strength++
  if (/[A-Z]/.test(pwd)) strength++
  if (/[0-9]/.test(pwd)) strength++
  if (/[^a-zA-Z0-9]/.test(pwd)) strength++

  return strength
})

const passwordStrengthClass = computed(() => {
  const strength = passwordStrength.value
  if (strength <= 2) return 'weak'
  if (strength <= 4) return 'medium'
  return 'strong'
})

const passwordStrengthWidth = computed(() => {
  const strength = passwordStrength.value
  return `${(strength / 6) * 100}%`
})

const passwordStrengthText = computed(() => {
  const strength = passwordStrength.value
  if (strength <= 2) return '弱'
  if (strength <= 4) return '中等'
  return '强'
})

// 表单验证规则
const passwordRules = {
  old_password: [
    { required: true, message: '请输入当前密码', trigger: 'blur' },
  ],
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 8, message: '密码长度不能少于8位', trigger: 'blur' },
    {
      pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$/,
      message: '密码必须包含大小写字母和数字',
      trigger: 'blur',
    },
  ],
  new_password_confirm: [
    { required: true, message: '请再次输入新密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== passwordForm.new_password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur',
    },
  ],
}

// 修改密码
const handleChangePassword = async () => {
  if (!passwordFormRef.value) return

  await passwordFormRef.value.validate(async (valid) => {
    if (!valid) return

    changingPassword.value = true
    try {
      await api.auth.changePassword({
        old_password: passwordForm.old_password,
        new_password: passwordForm.new_password,
        new_password_confirm: passwordForm.new_password_confirm,
      })

      ElMessageBox.confirm('密码修改成功，请重新登录', '提示', {
        confirmButtonText: '确定',
        showCancelButton: false,
        type: 'success',
      }).then(() => {
        // 登出并跳转到登录页
        userStore.logout()
      })
    } catch (error) {
      console.error('修改密码失败:', error)
    } finally {
      changingPassword.value = false
    }
  })
}

// 重置表单
const resetPasswordForm = () => {
  passwordForm.old_password = ''
  passwordForm.new_password = ''
  passwordForm.new_password_confirm = ''
  if (passwordFormRef.value) {
    passwordFormRef.value.clearValidate()
  }
}
</script>

<style scoped>
.settings-container {
  padding: 20px;
}

.settings-card {
  max-width: 800px;
  margin: 0 auto;
}

.card-header {
  font-size: 18px;
  font-weight: 600;
}

.section-card {
  border: 1px solid #ebeef5;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
}

.password-form {
  margin-top: 20px;
}

.password-strength {
  margin-top: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.strength-bar {
  height: 4px;
  border-radius: 2px;
  transition: all 0.3s;
}

.strength-bar.weak {
  background-color: #f56c6c;
}

.strength-bar.medium {
  background-color: #e6a23c;
}

.strength-bar.strong {
  background-color: #67c23a;
}

.strength-text {
  font-size: 12px;
  color: #666;
}

:deep(.el-form-item__label) {
  font-weight: 500;
}
</style>

