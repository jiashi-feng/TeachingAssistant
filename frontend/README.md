# 前端项目 (Vue 3 + Vite)

## 📋 项目说明

这是学生助教管理平台的前端项目，采用 Vue 3 + Vite 构建。

## 🚀 快速开始

### 初始化项目

```bash
# 进入前端目录
cd frontend

# 创建 Vue 3 项目（使用 Vite）
npm create vite@latest . -- --template vue

# 安装依赖
npm install

# 安装项目所需的其他依赖
npm install vue-router@4 pinia axios element-plus @element-plus/icons-vue
```

### 开发服务器

```bash
npm run dev
```

访问：http://localhost:8080

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

## 📂 推荐的项目结构

创建项目后，建议按以下结构组织代码：

```
frontend/
├── public/                    # 静态资源
├── src/
│   ├── api/                   # API请求封装
│   │   ├── index.js          # axios配置
│   │   ├── auth.js           # 认证相关API
│   │   ├── student.js        # 学生端API
│   │   ├── faculty.js        # 教师端API
│   │   ├── ta.js             # 助教端API
│   │   └── admin.js          # 管理员端API
│   │
│   ├── assets/               # 静态资源（图片、样式等）
│   │   ├── images/
│   │   └── styles/
│   │       └── main.css
│   │
│   ├── components/           # 公共组件
│   │   ├── common/
│   │   │   ├── Navbar.vue
│   │   │   ├── Sidebar.vue
│   │   │   └── Footer.vue
│   │   ├── notification/
│   │   │   └── NotificationCenter.vue
│   │   └── ...
│   │
│   ├── layouts/              # 布局组件
│   │   ├── StudentLayout.vue    # 学生端布局
│   │   ├── TALayout.vue         # 助教端布局
│   │   ├── FacultyLayout.vue    # 教师端布局
│   │   └── AdminLayout.vue      # 管理员端布局
│   │
│   ├── views/                # 页面组件
│   │   ├── auth/
│   │   │   ├── Login.vue
│   │   │   └── Register.vue
│   │   ├── student/
│   │   │   ├── Dashboard.vue
│   │   │   ├── Positions.vue
│   │   │   └── Applications.vue
│   │   ├── ta/
│   │   │   ├── Dashboard.vue
│   │   │   ├── Timesheets.vue
│   │   │   └── Salaries.vue
│   │   ├── faculty/
│   │   │   ├── Dashboard.vue
│   │   │   ├── Positions.vue
│   │   │   ├── Applications.vue
│   │   │   └── Timesheets.vue
│   │   └── admin/
│   │       ├── Dashboard.vue
│   │       ├── Users.vue
│   │       └── Reports.vue
│   │
│   ├── router/               # 路由配置
│   │   └── index.js
│   │
│   ├── store/                # Pinia状态管理
│   │   ├── index.js
│   │   ├── auth.js           # 认证状态
│   │   └── user.js           # 用户信息
│   │
│   ├── utils/                # 工具函数
│   │   ├── request.js        # axios拦截器
│   │   ├── auth.js           # 认证工具
│   │   └── storage.js        # 本地存储
│   │
│   ├── App.vue               # 根组件
│   └── main.js               # 入口文件
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
    port: 8080,
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

## 📝 待办事项

- [ ] 初始化 Vue 3 项目
- [ ] 安装必要依赖
- [ ] 配置路由和状态管理
- [ ] 创建基础布局组件
- [ ] 实现登录注册页面
- [ ] 开发各角色功能页面

## 🔗 相关链接

- [Vue 3 文档](https://v3.vuejs.org/)
- [Vite 文档](https://vitejs.dev/)
- [Vue Router 文档](https://router.vuejs.org/)
- [Pinia 文档](https://pinia.vuejs.org/)
- [Element Plus 文档](https://element-plus.org/)

