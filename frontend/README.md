# 前端项目 (Vue 3 + Vite)

## 📋 项目说明

这是学生助教管理平台的前端项目，采用 Vue 3 + Vite 构建。

## 🚀 快速开始

### 安装依赖

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install
```

### 开发服务器

```bash
npm run dev
```

访问：http://localhost:5173

### 生产构建

```bash
npm run build
```

## 📦 技术栈

- **Vue 3** - 渐进式JavaScript框架
- **Vite** - 下一代前端构建工具
- **Vue Router 4** - 官方路由管理器
- **Pinia** - 新一代状态管理库
- **Axios** - HTTP客户端
- **Element Plus** - Vue 3 UI组件库

## 📂 项目结构

当前代码已按以下方式组织：

```
frontend/
├── public/                    # 静态资源
├── src/
│   ├── api/                   # API请求封装
│   │   ├── index.js
│   │   ├── request.js         # Axios实例，自动注入Token与错误处理
│   │   ├── auth.js            # 认证接口
│   │   ├── positions.js       # 岗位/看板接口（学生&教师）
│   │   ├── applications.js    # 申请管理接口
│   │   ├── timesheets.js      # 工时/薪酬接口（助教、教师）
│   │   └── notifications.js   # 通知接口
│   │
│   ├── assets/                # 静态资源（样式、图片等）
│   │
│   ├── components/
│   │   └── NotificationCenter.vue  # 通知中心组件（未读角标、Popover）
│   │
│   ├── layouts/
│   │   ├── StudentLayout.vue
│   │   ├── FacultyLayout.vue
│   │   └── AdminLayout.vue
│   │
│   ├── router/
│   │   └── index.js           # 路由守卫（基于角色）
│   │
│   ├── store/
│   │   └── user.js            # Pinia用户信息&角色状态
│   │
│   ├── utils/
│   │   ├── request.js         # 请求封装（与api/request.js共享底层逻辑）
│   │   └── storage.js         # 本地存储工具
│   │
│   ├── views/
│   │   ├── auth/              # 登录、注册
│   │   ├── student/           # 学生端：Dashboard、PositionList、PositionDetail、ApplicationList、TimesheetList、SalaryList
│   │   ├── faculty/           # 教师端：Dashboard、PositionManage、ApplicationReview、TimesheetReview
│   │   └── NotFound.vue
│   │
│   ├── App.vue
│   └── main.js
│
├── .env.development          # 开发环境配置
├── .env.production           # 生产环境配置
├── .gitignore
├── index.html
├── package.json
├── vite.config.js            # Vite配置
└── README.md
```

## ⚙️ 配置说明

### Vite配置（vite.config.js）

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
```

### 环境变量

创建 `.env.development`:
```
VITE_API_BASE_URL=http://localhost:8000/api
```

创建 `.env.production`:
```
VITE_API_BASE_URL=https://yourdomain.com/api
```

## 🔧 开发规范

1. **组件命名**：使用 PascalCase（如 `UserProfile.vue`）
2. **文件组织**：按功能模块分组
3. **API调用**：统一通过 `src/api/` 下的模块
4. **状态管理**：全局状态使用 Pinia
5. **样式**：使用 scoped 样式或 CSS Modules

## 📝 近期更新与待办事项

- [x] 学生端：岗位筛选/排序、详情页过期校验、申请后跳转
- [x] 学生/助教：看板数据校准、工时与薪酬列表、提交校验
- [x] 教师端：工时审核列表 + 详情弹窗 + 审核API适配
- [x] 通知中心：未读计数、自动刷新、刷新用户角色状态
- [x] 管理后台配合：薪酬自动生成、支付方式下拉、流水号自动填充
- [ ] 管理员前端可视化页面

## 🔗 相关链接

- [Vue 3 文档](https://v3.vuejs.org/)
- [Vite 文档](https://vitejs.dev/)
- [Vue Router 文档](https://router.vuejs.org/)
- [Pinia 文档](https://pinia.vuejs.org/)
- [Element Plus 文档](https://element-plus.org/)

