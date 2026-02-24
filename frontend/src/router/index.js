/**
 * Vue Router 路由配置
 * 包含路由定义、路由守卫、权限控制
 */

import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/store/user'
import { ElMessage } from 'element-plus'

// 路由配置
const routes = [
  // ==================== 公共路由 ====================
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/Login.vue'),
    meta: {
      title: '登录',
      requiresAuth: false,
    },
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/auth/Register.vue'),
    meta: {
      title: '注册',
      requiresAuth: false,
    },
  },

  // ==================== 学生路由 ====================
  {
    path: '/student',
    component: () => import('@/layouts/StudentLayout.vue'),
    meta: {
      requiresAuth: true,
      roles: ['student'],
    },
    children: [
      {
        path: 'dashboard',
        name: 'StudentDashboard',
        component: () => import('@/views/student/Dashboard.vue'),
        meta: {
          title: '学生看板',
          requiresAuth: true,
          roles: ['student'],
        },
      },
      {
        path: 'positions',
        name: 'StudentPositions',
        component: () => import('@/views/student/PositionList.vue'),
        meta: {
          title: '浏览岗位',
          requiresAuth: true,
          roles: ['student'],
        },
      },
      {
        path: 'positions/:id',
        name: 'PositionDetail',
        component: () => import('@/views/student/PositionDetail.vue'),
        meta: {
          title: '岗位详情',
          requiresAuth: true,
          roles: ['student'],
        },
      },
      {
        path: 'applications',
        name: 'StudentApplications',
        component: () => import('@/views/student/ApplicationList.vue'),
        meta: {
          title: '我的申请',
          requiresAuth: true,
          roles: ['student'],
        },
      },
      {
        path: 'profile',
        name: 'StudentProfile',
        component: () => import('@/views/user/Profile.vue'),
        meta: {
          title: '个人信息',
          requiresAuth: true,
          roles: ['student'],
        },
      },
      {
        path: 'settings',
        name: 'StudentSettings',
        component: () => import('@/views/user/Settings.vue'),
        meta: {
          title: '设置',
          requiresAuth: true,
          roles: ['student'],
        },
      },
      {
        path: 'notifications',
        name: 'StudentNotifications',
        component: () => import('@/views/user/NotificationList.vue'),
        meta: {
          title: '通知列表',
          requiresAuth: true,
          roles: ['student'],
        },
      },
      {
        path: 'chat',
        name: 'StudentChat',
        component: () => import('@/views/user/Chat.vue'),
        meta: {
          title: '联系教师',
          requiresAuth: true,
          roles: ['student'],
        },
      },
    ],
  },

  // ==================== 助教路由（扩展学生路由）====================
  {
    path: '/ta',
    component: () => import('@/layouts/StudentLayout.vue'),
    meta: {
      requiresAuth: true,
      roles: ['student'],
      requiresTA: true,
    },
    children: [
      {
        path: 'timesheets',
        name: 'TATimesheets',
        component: () => import('@/views/student/TimesheetList.vue'),
        meta: {
          title: '工时管理',
          requiresAuth: true,
          roles: ['student'],
          requiresTA: true,
        },
      },
      {
        path: 'salaries',
        name: 'TASalaries',
        component: () => import('@/views/student/SalaryList.vue'),
        meta: {
          title: '薪酬记录',
          requiresAuth: true,
          roles: ['student'],
          requiresTA: true,
        },
      },
    ],
  },

  // ==================== 教师路由 ====================
  {
    path: '/faculty',
    component: () => import('@/layouts/FacultyLayout.vue'),
    meta: {
      requiresAuth: true,
      roles: ['faculty'],
    },
    children: [
      {
        path: 'dashboard',
        name: 'FacultyDashboard',
        component: () => import('@/views/faculty/Dashboard.vue'),
        meta: {
          title: '教师看板',
          requiresAuth: true,
          roles: ['faculty'],
        },
      },
      {
        path: 'positions',
        name: 'FacultyPositions',
        component: () => import('@/views/faculty/PositionManage.vue'),
        meta: {
          title: '岗位管理',
          requiresAuth: true,
          roles: ['faculty'],
        },
      },
      {
        path: 'applications',
        name: 'FacultyApplications',
        component: () => import('@/views/faculty/ApplicationReview.vue'),
        meta: {
          title: '申请审核',
          requiresAuth: true,
          roles: ['faculty'],
        },
      },
      {
        path: 'timesheets',
        name: 'FacultyTimesheets',
        component: () => import('@/views/faculty/TimesheetReview.vue'),
        meta: {
          title: '工时审核',
          requiresAuth: true,
          roles: ['faculty'],
        },
      },
      {
        path: 'profile',
        name: 'FacultyProfile',
        component: () => import('@/views/user/Profile.vue'),
        meta: {
          title: '个人信息',
          requiresAuth: true,
          roles: ['faculty'],
        },
      },
      {
        path: 'settings',
        name: 'FacultySettings',
        component: () => import('@/views/user/Settings.vue'),
        meta: {
          title: '设置',
          requiresAuth: true,
          roles: ['faculty'],
        },
      },
      {
        path: 'notifications',
        name: 'FacultyNotifications',
        component: () => import('@/views/user/NotificationList.vue'),
        meta: {
          title: '通知列表',
          requiresAuth: true,
          roles: ['faculty'],
        },
      },
      {
        path: 'chat',
        name: 'FacultyChat',
        component: () => import('@/views/user/Chat.vue'),
        meta: {
          title: '联系学生/助教',
          requiresAuth: true,
          roles: ['faculty'],
        },
      },
    ],
  },

  // ==================== 根路径重定向 ====================
  {
    path: '/',
    redirect: () => {
      const userStore = useUserStore()

      // 如果未登录，跳转到登录页
      if (!userStore.isAuthenticated) {
        return '/login'
      }

      // 根据角色跳转
      const roleCodes = userStore.roleCodes
      if (roleCodes.includes('faculty')) {
        return '/faculty/dashboard'
      } else if (roleCodes.includes('student')) {
        return '/student/dashboard'
      }

      return '/login'
    },
  },

  // ==================== 404页面 ====================
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: {
      title: '页面不存在',
    },
  },
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes,
})

// ==================== 全局前置守卫 ====================
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - 学生助教管理平台`
  }

  // 1. 检查是否需要认证
  if (to.meta.requiresAuth === false) {
    // 不需要认证，直接放行
    next()
    return
  }

  // 2. 检查用户是否已登录
  if (!userStore.isAuthenticated) {
    // 未登录，重定向到登录页
    ElMessage.warning('请先登录')
    next({
      path: '/login',
      query: { redirect: to.fullPath }, // 保存目标路径，登录后跳转
    })
    return
  }

  // 3. 检查角色权限
  if (to.meta.roles && to.meta.roles.length > 0) {
    const hasRole = userStore.hasAnyRole(to.meta.roles)

    if (!hasRole) {
      ElMessage.error('您没有权限访问该页面')
      // 跳转到用户对应的首页
      if (userStore.hasRole('faculty')) {
        next('/faculty/dashboard')
      } else if (userStore.hasRole('student')) {
        next('/student/dashboard')
      } else {
        next('/login')
      }
      return
    }
  }

  // 4. 检查是否需要助教身份
  if (to.meta.requiresTA && !userStore.isTA) {
    ElMessage.error('该功能仅助教可用')
    next('/student/dashboard')
    return
  }

  // 5. 检查细粒度权限（如果配置了）
  if (to.meta.permissions && to.meta.permissions.length > 0) {
    const hasPermission = to.meta.permissions.some(permission =>
      userStore.hasPermission(permission)
    )

    if (!hasPermission) {
      ElMessage.error('您没有权限执行此操作')
      next(from.fullPath || '/')
      return
    }
  }

  // 所有检查通过，放行
  next()
})

// ==================== 全局后置钩子 ====================
router.afterEach((to, from) => {
  // 可以在这里添加页面访问日志、统计等
  console.log(`导航: ${from.path} -> ${to.path}`)
})

export default router

