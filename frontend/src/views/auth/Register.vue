<template>
  <div class="register-container">
    <div class="register-box">
      <!-- Logo和标题 -->
      <div class="register-header">
        <h1 class="register-title">用户注册</h1>
        <p class="register-subtitle">创建您的账号</p>
      </div>

      <!-- 步骤指示器 -->
      <el-steps :active="currentStep" align-center class="steps">
        <el-step title="基本信息" icon="User" />
        <el-step title="角色信息" icon="Stamp" />
      </el-steps>

      <!-- 注册表单 -->
      <el-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="registerRules"
        class="register-form"
        label-width="80px"
        label-position="top"
      >
        <!-- 步骤1：基本信息 -->
        <div v-show="currentStep === 0" class="form-step">

        <el-form-item label="用户ID" prop="user_id">
          <el-input
            v-model="registerForm.user_id"
            placeholder="学生: STU001, 教师: FAC001"
            clearable
          >
            <template #prepend>
              <el-icon><User /></el-icon>
            </template>
          </el-input>
          <span class="form-tip">
            学生请输入STU开头，教师请输入FAC开头
          </span>
        </el-form-item>

        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="registerForm.username"
            placeholder="4-20个字符，字母、数字、下划线"
            clearable
            @blur="checkUsernameAvailable"
          >
            <template #prepend>
              <el-icon><User /></el-icon>
            </template>
            <template #suffix>
              <el-icon v-if="usernameChecking" class="is-loading">
                <Loading />
              </el-icon>
              <el-icon v-else-if="usernameAvailable === true" color="#67c23a">
                <CircleCheck />
              </el-icon>
              <el-icon v-else-if="usernameAvailable === false" color="#f56c6c">
                <CircleClose />
              </el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item label="真实姓名" prop="real_name">
          <el-input
            v-model="registerForm.real_name"
            placeholder="请输入真实姓名"
            clearable
          />
        </el-form-item>

        <el-form-item label="邮箱" prop="email">
          <el-input
            v-model="registerForm.email"
            placeholder="请输入邮箱地址"
            clearable
            @blur="checkEmailAvailable"
          >
            <template #prepend>
              <el-icon><Message /></el-icon>
            </template>
            <template #suffix>
              <el-icon v-if="emailChecking" class="is-loading">
                <Loading />
              </el-icon>
              <el-icon v-else-if="emailAvailable === true" color="#67c23a">
                <CircleCheck />
              </el-icon>
              <el-icon v-else-if="emailAvailable === false" color="#f56c6c">
                <CircleClose />
              </el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input
            v-model="registerForm.password"
            type="password"
            placeholder="至少8位，包含大小写字母和数字"
            show-password
            clearable
          >
            <template #prepend>
              <el-icon><Lock /></el-icon>
            </template>
          </el-input>
          <!-- 密码强度指示器 -->
          <div v-if="registerForm.password" class="password-strength">
            <div
              class="strength-bar"
              :class="passwordStrengthClass"
              :style="{ width: passwordStrengthWidth }"
            ></div>
            <span class="strength-text">{{ passwordStrengthText }}</span>
          </div>
        </el-form-item>

        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            v-model="registerForm.confirmPassword"
            type="password"
            placeholder="请再次输入密码"
            show-password
            clearable
          >
            <template #prepend>
              <el-icon><Lock /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <!-- 步骤1的按钮 -->
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            class="step-button"
            @click="nextStep"
          >
            下一步
          </el-button>
        </el-form-item>
        </div>

        <!-- 步骤2：角色信息 -->
        <div v-show="currentStep === 1" class="form-step">

        <el-form-item label="注册角色" prop="role">
          <el-select
            v-model="registerForm.role"
            placeholder="请选择角色"
            size="large"
            style="width: 100%"
          >
            <el-option label="学生" value="student" />
            <el-option label="教师" value="faculty" />
          </el-select>
          <span class="form-tip">
            管理员账号需由系统管理员在后台创建
          </span>
        </el-form-item>

        <!-- 学生专属字段 -->
        <template v-if="registerForm.role === 'student'">
          <el-form-item label="学号" prop="student_id">
            <el-input
              v-model="registerForm.student_id"
              placeholder="请输入学号"
              clearable
            />
          </el-form-item>

          <el-form-item label="院系" prop="department">
            <el-input
              v-model="registerForm.department"
              placeholder="如：计算机学院"
              clearable
            />
          </el-form-item>

          <el-form-item label="专业" prop="major">
            <el-input
              v-model="registerForm.major"
              placeholder="如：软件工程"
              clearable
            />
          </el-form-item>

          <el-form-item label="年级" prop="grade">
            <el-select
              v-model="registerForm.grade"
              placeholder="请选择年级"
              style="width: 100%"
            >
              <el-option
                v-for="year in gradeOptions"
                :key="year"
                :label="`${year}级`"
                :value="year"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="班级">
            <el-input
              v-model="registerForm.class_name"
              placeholder="如：软工1班（可选）"
              clearable
            />
          </el-form-item>
        </template>

        <!-- 教师专属字段 -->
        <template v-if="registerForm.role === 'faculty'">
          <el-form-item label="工号" prop="faculty_id">
            <el-input
              v-model="registerForm.faculty_id"
              placeholder="请输入工号"
              clearable
            />
          </el-form-item>

          <el-form-item label="职称" prop="title">
            <el-select
              v-model="registerForm.title"
              placeholder="请选择职称"
              style="width: 100%"
            >
              <el-option label="助教" value="助教" />
              <el-option label="讲师" value="讲师" />
              <el-option label="副教授" value="副教授" />
              <el-option label="教授" value="教授" />
            </el-select>
          </el-form-item>

          <el-form-item label="院系" prop="department">
            <el-input
              v-model="registerForm.department"
              placeholder="如：计算机学院"
              clearable
            />
          </el-form-item>

          <el-form-item label="办公室">
            <el-input
              v-model="registerForm.office_location"
              placeholder="如：教学楼A301（可选）"
              clearable
            />
          </el-form-item>

          <el-form-item label="联系电话">
            <el-input
              v-model="registerForm.phone"
              placeholder="联系电话（可选）"
              clearable
            />
          </el-form-item>
        </template>

        <!-- 步骤2的按钮 -->
        <el-form-item>
          <div class="button-group">
            <el-button
              size="large"
              class="step-button"
              @click="prevStep"
            >
              上一步
            </el-button>
            <el-button
              type="primary"
              size="large"
              class="step-button"
              :loading="loading"
              @click="handleRegister"
            >
              {{ loading ? '注册中...' : '完成注册' }}
            </el-button>
          </div>
        </el-form-item>
        </div>

        <div class="register-footer">
          <span>已有账号？</span>
          <el-link type="primary" @click="goToLogin">立即登录</el-link>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  User,
  Lock,
  Message,
  Loading,
  CircleCheck,
  CircleClose,
  Stamp,
} from '@element-plus/icons-vue'
import api from '@/api'

const router = useRouter()

// 表单引用
const registerFormRef = ref(null)

// 加载状态
const loading = ref(false)

// 当前步骤（0: 基本信息, 1: 角色信息）
const currentStep = ref(0)

// 用户名检查状态
const usernameChecking = ref(false)
const usernameAvailable = ref(null)

// 邮箱检查状态
const emailChecking = ref(false)
const emailAvailable = ref(null)

// 年级选项（最近5年）
const currentYear = new Date().getFullYear()
const gradeOptions = Array.from({ length: 5 }, (_, i) => currentYear - i)

// 注册表单数据
const registerForm = reactive({
  user_id: '',
  username: '',
  real_name: '',
  email: '',
  password: '',
  confirmPassword: '',
  role: 'student',
  
  // 学生字段
  student_id: '',
  department: '',
  major: '',
  grade: currentYear,
  class_name: '',
  
  // 教师字段
  faculty_id: '',
  title: '',
  office_location: '',
  phone: '',
})

// 密码强度计算
const passwordStrength = computed(() => {
  const pwd = registerForm.password
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
const registerRules = computed(() => {
  const baseRules = {
    user_id: [
      { required: true, message: '请输入用户ID', trigger: 'blur' },
      { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' },
    ],
    username: [
      { required: true, message: '请输入用户名', trigger: 'blur' },
      { min: 4, max: 20, message: '长度在 4 到 20 个字符', trigger: 'blur' },
      {
        pattern: /^[a-zA-Z0-9_]+$/,
        message: '只能包含字母、数字和下划线',
        trigger: 'blur',
      },
    ],
    real_name: [
      { required: true, message: '请输入真实姓名', trigger: 'blur' },
    ],
    email: [
      { required: true, message: '请输入邮箱', trigger: 'blur' },
      { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' },
    ],
    password: [
      { required: true, message: '请输入密码', trigger: 'blur' },
      { min: 8, message: '密码长度不能少于8位', trigger: 'blur' },
      {
        pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$/,
        message: '密码必须包含大小写字母和数字',
        trigger: 'blur',
      },
    ],
    confirmPassword: [
      { required: true, message: '请再次输入密码', trigger: 'blur' },
      {
        validator: (rule, value, callback) => {
          if (value !== registerForm.password) {
            callback(new Error('两次输入的密码不一致'))
          } else {
            callback()
          }
        },
        trigger: 'blur',
      },
    ],
    role: [
      { required: true, message: '请选择角色', trigger: 'change' },
    ],
  }
  
  // 根据角色添加额外验证
  if (registerForm.role === 'student') {
    baseRules.student_id = [
      { required: true, message: '请输入学号', trigger: 'blur' },
    ]
    baseRules.department = [
      { required: true, message: '请输入院系', trigger: 'blur' },
    ]
    baseRules.major = [
      { required: true, message: '请输入专业', trigger: 'blur' },
    ]
    baseRules.grade = [
      { required: true, message: '请选择年级', trigger: 'change' },
    ]
  } else if (registerForm.role === 'faculty') {
    baseRules.faculty_id = [
      { required: true, message: '请输入工号', trigger: 'blur' },
    ]
    baseRules.title = [
      { required: true, message: '请选择职称', trigger: 'change' },
    ]
    baseRules.department = [
      { required: true, message: '请输入院系', trigger: 'blur' },
    ]
  }
  
  return baseRules
})

/**
 * 检查用户名是否可用
 */
let usernameCheckTimer = null
const checkUsernameAvailable = async () => {
  const username = registerForm.username
  if (!username || username.length < 4) {
    usernameAvailable.value = null
    return
  }
  
  // 防抖：延迟500ms后检查
  clearTimeout(usernameCheckTimer)
  usernameCheckTimer = setTimeout(async () => {
    usernameChecking.value = true
    try {
      const response = await api.auth.checkUsername(username)
      usernameAvailable.value = response.available
    } catch (error) {
      usernameAvailable.value = false
    } finally {
      usernameChecking.value = false
    }
  }, 500)
}

/**
 * 检查邮箱是否可用
 */
let emailCheckTimer = null
const checkEmailAvailable = async () => {
  const email = registerForm.email
  if (!email || !email.includes('@')) {
    emailAvailable.value = null
    return
  }
  
  clearTimeout(emailCheckTimer)
  emailCheckTimer = setTimeout(async () => {
    emailChecking.value = true
    try {
      const response = await api.auth.checkEmail(email)
      emailAvailable.value = response.available
    } catch (error) {
      emailAvailable.value = false
    } finally {
      emailChecking.value = false
    }
  }, 500)
}

/**
 * 下一步
 */
const nextStep = async () => {
  if (!registerFormRef.value) return
  
  // 验证第一步的字段
  const fieldsToValidate = [
    'user_id',
    'username',
    'real_name',
    'email',
    'password',
    'confirmPassword'
  ]
  
  try {
    await registerFormRef.value.validateField(fieldsToValidate)
    currentStep.value = 1
  } catch (error) {
    ElMessage.warning('请完善基本信息')
  }
}

/**
 * 上一步
 */
const prevStep = () => {
  currentStep.value = 0
}

/**
 * 处理注册
 */
const handleRegister = async () => {
  if (!registerFormRef.value) return
  
  await registerFormRef.value.validate(async (valid) => {
    if (!valid) {
      ElMessage.warning('请完善表单信息')
      return
    }
    
    loading.value = true
    
    try {
      // 组装提交数据 - 后端期望扁平结构
      const submitData = {
        user_id: registerForm.user_id,
        username: registerForm.username,
        real_name: registerForm.real_name,
        email: registerForm.email,
        password: registerForm.password,
        password_confirm: registerForm.confirmPassword,  // 后端需要这个字段
        role_code: registerForm.role,  // 改为 role_code
        phone: registerForm.phone || '',
      }
      
      // 添加角色专属数据 - 扁平结构
      if (registerForm.role === 'student') {
        Object.assign(submitData, {
          student_id: registerForm.student_id,
          department: registerForm.department,
          major: registerForm.major,
          grade: registerForm.grade,
          class_name: registerForm.class_name || '',
        })
      } else if (registerForm.role === 'faculty') {
        Object.assign(submitData, {
          faculty_id: registerForm.faculty_id,
          title: registerForm.title,
          department: registerForm.department,
          office_location: registerForm.office_location || '',
        })
      }
      
      // 调用注册接口
      await api.auth.register(submitData)
      
      ElMessage.success('注册成功！3秒后跳转到登录页...')
      
      // 3秒后跳转到登录页
      setTimeout(() => {
        router.push({
          path: '/login',
          query: { username: registerForm.username },
        })
      }, 3000)
    } catch (error) {
      console.error('注册失败:', error)
      // 错误信息已在axios拦截器中处理
    } finally {
      loading.value = false
    }
  })
}

/**
 * 跳转到登录页面
 */
const goToLogin = () => {
  router.push('/login')
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  position: relative;
  padding: 40px 20px;
  
  /* 背景图片 */
  background-image: url('@/assets/styles/login-bg.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: fixed;
}

/* 半透明遮罩层，让注册框更清晰 */
.register-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(102, 126, 234, 0.3);
  z-index: 0;
}

.register-box {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 600px;
  background: white;
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.5s ease-out;
  max-height: 90vh;
  overflow-y: auto;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.register-header {
  text-align: center;
  margin-bottom: 20px;
}

.steps {
  margin-bottom: 30px;
}

.register-title {
  font-size: 28px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

.register-subtitle {
  font-size: 14px;
  color: #999;
  margin: 0;
}

.register-form {
  margin-top: 20px;
}

.form-tip {
  display: block;
  font-size: 12px;
  color: #999;
  margin-top: 4px;
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

.form-step {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateX(10px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.step-button {
  width: 100%;
  height: 45px;
  font-size: 16px;
  font-weight: 500;
  border-radius: 6px;
  margin-top: 10px;
}

.button-group {
  display: flex;
  gap: 15px;
}

.button-group .step-button {
  flex: 1;
}

.register-footer {
  text-align: center;
  margin-top: 20px;
  color: #666;
  font-size: 14px;
}

.register-footer span {
  margin-right: 8px;
}

:deep(.el-divider__text) {
  font-weight: 600;
  color: #409eff;
}

/* 响应式设计 */
@media (max-width: 640px) {
  .register-box {
    padding: 30px 20px;
  }
  
  .register-title {
    font-size: 24px;
  }
  
  :deep(.el-form-item) {
    margin-bottom: 18px;
  }
}
</style>

