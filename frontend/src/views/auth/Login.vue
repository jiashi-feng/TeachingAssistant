<template>
  <div class="login-container">
    <div class="login-box">
      <!-- Logo和标题 -->
      <div class="login-header">
        <h1 class="login-title">学生助教管理平台</h1>
        <p class="login-subtitle">Teaching Assistant Management System</p>
      </div>

      <!-- 登录表单 -->
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        class="login-form"
        @keyup.enter="handleLogin"
      >
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名或邮箱"
            size="large"
            :prefix-icon="User"
            clearable
            autofocus
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            size="large"
            :prefix-icon="Lock"
            show-password
            clearable
          />
        </el-form-item>

        <el-form-item>
          <div class="login-options">
            <el-checkbox v-model="loginForm.remember">记住我</el-checkbox>
          </div>
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            size="large"
            class="login-button"
            :loading="loading"
            @click="handleLogin"
          >
            {{ loading ? '登录中...' : '登录' }}
          </el-button>
        </el-form-item>

        <div class="login-footer">
          <span>还没有账号？</span>
          <el-link type="primary" @click="goToRegister">立即注册</el-link>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/store/user'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import storage from '@/utils/storage'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

// 表单引用
const loginFormRef = ref(null)

// 加载状态
const loading = ref(false)

// 登录表单数据
const loginForm = reactive({
  username: '',
  password: '',
  remember: false,
})

// 表单验证规则
const loginRules = {
  username: [
    { required: true, message: '请输入用户名或邮箱', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' },
  ],
}

/**
 * 处理登录
 */
const handleLogin = async () => {
  // 表单验证
  if (!loginFormRef.value) return
  
  await loginFormRef.value.validate(async (valid) => {
    if (!valid) return
    
    loading.value = true
    
    try {
      // 调用登录接口
      const response = await userStore.login({
        username: loginForm.username,
        password: loginForm.password,
      })
      
      // 记住用户名
      if (loginForm.remember) {
        storage.setRememberUsername(loginForm.username)
      } else {
        storage.setRememberUsername('')
      }
      
      // 根据用户角色跳转
      const roles = response.user.roles
      const roleCodes = roles.map(role => role.role_code)
      
      
      if (roleCodes.includes('admin')) {
        // 管理员跳转到Django Admin后台
        ElMessage.success('正在跳转到管理后台...')
        setTimeout(() => {
          window.location.href = 'http://localhost:8000/admin/'
        }, 1000)
      } else if (roleCodes.includes('faculty')) {
        // 教师跳转到教师看板
        const redirect = route.query.redirect || '/faculty/dashboard'
        router.push(redirect)
      } else if (roleCodes.includes('student')) {
        // 学生/助教跳转到学生看板
        const redirect = route.query.redirect || '/student/dashboard'
        router.push(redirect)
      } else {
        // 未知角色
        ElMessage.warning('您的账号暂无可访问的功能')
      }
    } catch (error) {
      console.error('登录失败:', error)
      // 错误信息已在axios拦截器中处理
      // 清空密码框
      loginForm.password = ''
    } finally {
      loading.value = false
    }
  })
}

/**
 * 跳转到注册页面
 */
const goToRegister = () => {
  router.push('/register')
}

/**
 * 组件挂载时执行
 */
onMounted(() => {

  // 检查是否是从后台logout跳转过来的
  if (route.query.logout === 'true') {
    // 清除所有认证信息
    userStore.clearAuth()
    ElMessage.success('已退出登录')
    // 清除URL参数
    router.replace('/login')
    return
  }
  
  // 如果已经登录，直接跳转到首页
  if (userStore.isAuthenticated) {
    userStore.navigateToHome()
    return
  }
  
  // 恢复上次登录的用户名
  const rememberedUsername = storage.getRememberUsername()
  if (rememberedUsername) {
    loginForm.username = rememberedUsername
    loginForm.remember = true
  }
})
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  position: relative;
  padding: 20px;
  
  /* 背景图片 */
  background-image: url('@/assets/styles/login-bg.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: fixed;
}

/* 半透明遮罩层，让登录框更清晰 */
.login-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(102, 126, 234, 0.3);
  z-index: 0;
}

.login-box {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 420px;
  background: white;
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.5s ease-out;
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

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.login-title {
  font-size: 28px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

.login-subtitle {
  font-size: 14px;
  color: #999;
  margin: 0;
}

.login-form {
  margin-top: 20px;
}

.login-options {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.login-button {
  width: 100%;
  height: 45px;
  font-size: 16px;
  font-weight: 500;
  border-radius: 6px;
}

.login-footer {
  text-align: center;
  margin-top: 20px;
  color: #666;
  font-size: 14px;
}

.login-footer span {
  margin-right: 8px;
}

/* 响应式设计 */
@media (max-width: 480px) {
  .login-box {
    padding: 30px 20px;
  }
  
  .login-title {
    font-size: 24px;
  }
}
</style>

