<template>
  <div class="profile-container">
    <el-card class="profile-card">
      <template #header>
        <div class="card-header">
          <span>个人信息</span>
        </div>
      </template>

      <!-- 头像区域 -->
      <div class="avatar-section">
        <el-upload
          class="avatar-uploader"
          :action="''"
          :show-file-list="false"
          :before-upload="beforeAvatarUpload"
          :http-request="handleAvatarUpload"
          :disabled="uploading"
        >
          <el-avatar
            v-if="userInfo?.avatar"
            :size="120"
            :src="avatarUrl"
            class="avatar"
          />
          <el-avatar
            v-else
            :size="120"
            class="avatar"
          >
            {{ userInfo?.real_name?.charAt(0) || 'U' }}
          </el-avatar>
          <div class="avatar-overlay">
            <el-icon v-if="!uploading"><Camera /></el-icon>
            <el-icon v-else class="is-loading"><Loading /></el-icon>
          </div>
        </el-upload>
        <p class="avatar-tip">点击头像上传新头像（支持 JPG、PNG、GIF，最大 10MB）</p>
      </div>

      <!-- 基本信息表单 -->
      <el-form
        ref="profileFormRef"
        :model="profileForm"
        :rules="profileRules"
        label-width="100px"
        class="profile-form"
      >
        <el-form-item label="用户ID" prop="user_id">
          <el-input v-model="profileForm.user_id" disabled />
        </el-form-item>

        <el-form-item label="用户名" prop="username">
          <el-input v-model="profileForm.username" disabled />
        </el-form-item>

        <el-form-item label="真实姓名" prop="real_name">
          <el-input
            v-model="profileForm.real_name"
            placeholder="请输入真实姓名"
            :disabled="!isEditing"
          />
        </el-form-item>

        <el-form-item label="邮箱" prop="email">
          <el-input
            v-model="profileForm.email"
            placeholder="请输入邮箱"
            :disabled="!isEditing"
          />
        </el-form-item>

        <el-form-item label="手机号" prop="phone">
          <el-input
            v-model="profileForm.phone"
            placeholder="请输入手机号"
            :disabled="!isEditing"
            maxlength="11"
          />
        </el-form-item>

        <!-- 角色信息（只读） -->
        <el-form-item label="角色">
          <el-tag
            v-for="role in userInfo?.roles"
            :key="role.role_id"
            :type="role.is_primary ? 'primary' : 'info'"
            style="margin-right: 8px"
          >
            {{ role.role_name }}
            <span v-if="role.is_primary" style="margin-left: 4px">(主角色)</span>
          </el-tag>
        </el-form-item>

        <!-- 学生信息（只读） -->
        <template v-if="userInfo?.student_info">
          <el-divider>学生信息</el-divider>
          <el-form-item label="学号">
            <el-input :value="userInfo.student_info.student_id" disabled />
          </el-form-item>
          <el-form-item label="院系">
            <el-input :value="userInfo.student_info.department" disabled />
          </el-form-item>
          <el-form-item label="专业">
            <el-input :value="userInfo.student_info.major" disabled />
          </el-form-item>
          <el-form-item label="年级">
            <el-input :value="`${userInfo.student_info.grade}级`" disabled />
          </el-form-item>
          <el-form-item v-if="userInfo.student_info.class_name" label="班级">
            <el-input :value="userInfo.student_info.class_name" disabled />
          </el-form-item>
          <el-form-item label="助教状态">
            <el-tag :type="userInfo.student_info.is_ta ? 'success' : 'info'">
              {{ userInfo.student_info.is_ta ? '是' : '否' }}
            </el-tag>
          </el-form-item>
        </template>

        <!-- 教师信息（只读） -->
        <template v-if="userInfo?.faculty_info">
          <el-divider>教师信息</el-divider>
          <el-form-item label="工号">
            <el-input :value="userInfo.faculty_info.faculty_id" disabled />
          </el-form-item>
          <el-form-item label="院系">
            <el-input :value="userInfo.faculty_info.department" disabled />
          </el-form-item>
          <el-form-item label="职称">
            <el-input :value="userInfo.faculty_info.title" disabled />
          </el-form-item>
          <el-form-item v-if="userInfo.faculty_info.office_location" label="办公室">
            <el-input :value="userInfo.faculty_info.office_location" disabled />
          </el-form-item>
          <el-form-item v-if="userInfo.faculty_info.research_area" label="研究方向">
            <el-input
              :value="userInfo.faculty_info.research_area"
              type="textarea"
              :rows="2"
              disabled
            />
          </el-form-item>
        </template>

        <!-- 管理员信息（只读） -->
        <template v-if="userInfo?.admin_info">
          <el-divider>管理员信息</el-divider>
          <el-form-item label="管理员编号">
            <el-input :value="userInfo.admin_info.admin_id" disabled />
          </el-form-item>
          <el-form-item label="部门">
            <el-input :value="userInfo.admin_info.department" disabled />
          </el-form-item>
          <el-form-item label="职位">
            <el-input :value="userInfo.admin_info.position" disabled />
          </el-form-item>
        </template>

        <!-- 操作按钮 -->
        <el-form-item>
          <el-button
            v-if="!isEditing"
            type="primary"
            @click="startEdit"
          >
            编辑信息
          </el-button>
          <template v-else>
            <el-button @click="cancelEdit">取消</el-button>
            <el-button
              type="primary"
              :loading="saving"
              @click="saveProfile"
            >
              保存
            </el-button>
          </template>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useUserStore } from '@/store/user'
import { ElMessage } from 'element-plus'
import { Camera, Loading } from '@element-plus/icons-vue'
import api from '@/api'

const userStore = useUserStore()

const profileFormRef = ref(null)
const isEditing = ref(false)
const saving = ref(false)
const uploading = ref(false)

const userInfo = computed(() => userStore.userInfo)

// 头像URL（处理相对路径）
const avatarUrl = computed(() => {
  if (!userInfo.value?.avatar) return null
  const avatar = userInfo.value.avatar
  // 如果已经是完整URL，直接返回
  if (avatar.startsWith('http://') || avatar.startsWith('https://')) {
    return avatar
  }
  // 如果是相对路径（以 / 开头），拼接后端地址
  if (avatar.startsWith('/')) {
    return `http://localhost:8000${avatar}`
  }
  // 否则拼接 /media/ 前缀
  return `http://localhost:8000/media/${avatar}`
})

// 表单数据
const profileForm = reactive({
  user_id: '',
  username: '',
  real_name: '',
  email: '',
  phone: '',
})

// 表单验证规则
const profileRules = {
  real_name: [
    { required: true, message: '请输入真实姓名', trigger: 'blur' },
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    {
      type: 'email',
      message: '请输入正确的邮箱格式',
      trigger: 'blur',
    },
  ],
  phone: [
    {
      pattern: /^1[3-9]\d{9}$/,
      message: '请输入正确的手机号',
      trigger: 'blur',
    },
  ],
}

// 初始化表单数据
const initForm = () => {
  if (userInfo.value) {
    profileForm.user_id = userInfo.value.user_id || ''
    profileForm.username = userInfo.value.username || ''
    profileForm.real_name = userInfo.value.real_name || ''
    profileForm.email = userInfo.value.email || ''
    profileForm.phone = userInfo.value.phone || ''
  }
}

// 开始编辑
const startEdit = () => {
  isEditing.value = true
}

// 取消编辑
const cancelEdit = () => {
  initForm()
  isEditing.value = false
  if (profileFormRef.value) {
    profileFormRef.value.clearValidate()
  }
}

// 保存个人信息
const saveProfile = async () => {
  if (!profileFormRef.value) return

  await profileFormRef.value.validate(async (valid) => {
    if (!valid) return

    saving.value = true
    try {
      const response = await api.auth.updateProfile({
        real_name: profileForm.real_name,
        email: profileForm.email,
        phone: profileForm.phone,
      })

      // 更新用户信息
      userStore.setUserInfo(response.user)
      ElMessage.success('个人信息更新成功')
      isEditing.value = false
    } catch (error) {
      console.error('更新失败:', error)
    } finally {
      saving.value = false
    }
  })
}

// 头像上传前验证
const beforeAvatarUpload = (file) => {
  const isImage = ['image/jpeg', 'image/png', 'image/gif'].includes(file.type)
  const isLt10M = file.size / 1024 / 1024 < 10

  if (!isImage) {
    ElMessage.error('头像只能是 JPG、PNG 或 GIF 格式!')
    return false
  }
  if (!isLt10M) {
    ElMessage.error('头像大小不能超过 10MB!')
    return false
  }
  return true
}

// 处理头像上传
const handleAvatarUpload = async (options) => {
  uploading.value = true
  try {
    const response = await api.auth.uploadAvatar(options.file)
    
    // 更新用户信息
    userStore.setUserInfo(response.user)
    ElMessage.success('头像上传成功')
  } catch (error) {
    console.error('头像上传失败:', error)
  } finally {
    uploading.value = false
  }
}

// 组件挂载时初始化
onMounted(() => {
  // 如果用户信息不存在，先获取
  if (!userInfo.value) {
    userStore.refreshUserInfo().then(() => {
      initForm()
    })
  } else {
    initForm()
  }
})
</script>

<style scoped>
.profile-container {
  padding: 20px;
}

.profile-card {
  max-width: 800px;
  margin: 0 auto;
}

.card-header {
  font-size: 18px;
  font-weight: 600;
}

.avatar-section {
  text-align: center;
  margin-bottom: 30px;
}

.avatar-uploader {
  position: relative;
  display: inline-block;
  cursor: pointer;
}

.avatar {
  border: 2px solid #dcdfe6;
  transition: border-color 0.3s;
}

.avatar-uploader:hover .avatar {
  border-color: #409eff;
}

.avatar-overlay {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 40px;
  height: 40px;
  background-color: rgba(0, 0, 0, 0.6);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  transition: background-color 0.3s;
}

.avatar-uploader:hover .avatar-overlay {
  background-color: rgba(64, 158, 255, 0.8);
}

.avatar-tip {
  margin-top: 10px;
  font-size: 12px;
  color: #909399;
}

.profile-form {
  margin-top: 20px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
}

:deep(.el-input.is-disabled .el-input__inner) {
  background-color: #f5f7fa;
  color: #606266;
}
</style>

