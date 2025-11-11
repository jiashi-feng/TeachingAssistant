# 🎓 学生助教管理平台 (Teaching Assistant Management System)

<div align="center">

![Django](https://img.shields.io/badge/Django-3.2+-green.svg)
![Vue](https://img.shields.io/badge/Vue-3.0+-blue.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

一个面向高校的在线助教管理系统，实现助教招募、申请、工时跟踪与薪酬核算的全流程数字化管理。

[功能特性](#功能特性) • [技术架构](#技术架构) • [快速开始](#快速开始) • [API文档](#api文档) • [部署指南](#部署指南)

</div>

---

## 📋 目录

- [项目简介](#项目简介)
- [功能特性](#功能特性)
- [技术架构](#技术架构)
- [系统架构](#系统架构)
- [项目结构](#项目结构)
- [快速开始](#快速开始)
- [开发指南](#开发指南)
- [API文档](#api文档)
- [部署指南](#部署指南)
- [常见问题](#常见问题)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

---

## 📖 项目简介

学生助教管理平台是一个**前后端分离**的现代化Web应用，旨在解决高校助教管理流程繁琐、效率低下的问题。

### 🎯 核心目标

- ✅ **数字化招募流程**：在线发布岗位、投递简历、审核录用
- ✅ **透明化工时管理**：电子工时表、在线审批、自动核算薪酬
- ✅ **精细化权限控制**：基于角色的访问控制（RBAC），保障数据安全
- ✅ **自动化消息通知**：关键节点自动推送通知，提升协作效率

### 👥 用户角色

| 角色       | 主要功能                               |
| ---------- | -------------------------------------- |
| **学生**   | 浏览岗位、投递申请、查看申请状态       |
| **助教**   | 填写工时、查看薪酬记录                 |
| **教师**   | 发布岗位、审核申请、审批工时、评价助教 |
| **管理员** | 用户管理、数据统计、生成报表           |

---

## ✨ 功能特性

### 🔐 统一身份认证

- JWT Token认证
- 基于角色的权限控制（RBAC）
- 安全的密码存储（哈希加密）
- 自动角色路由（登录后跳转到对应角色页面）

### 📢 招募管理

- **教师端**：创建/编辑/关闭岗位，设置招募条件
- **学生端**：浏览/搜索/筛选岗位，查看详细信息
- 支持多条件筛选（院系、课程、薪资范围等）
- 岗位状态自动管理（开放/关闭/已满员）

### 📝 申请流程

- **学生端**：在线填写简历、一键投递、实时查看审核进度
- **教师端**：查看申请列表、预览简历、批量审核
- 申请状态追踪：已投递 → 审核中 → 已录用/已拒绝
- 自动去重（同一岗位不可重复申请）

### ⏰ 工时与薪酬

- **助教端**：按月填写工作日志、提交工时表
- **教师端**：在线审核工时、添加评价意见
- 薪酬自动核算（工时 × 时薪）
- 完整的薪酬记录查询

### 🔔 消息通知

- 关键节点自动通知（基于Django Signals）
- 支持站内消息
- 通知类型：岗位发布、申请状态变更、工时审核、薪酬发放等
- 未读消息提醒

### 📊 数据看板

- **学生/助教**：个人申请统计、工时汇总
- **教师**：岗位数据、申请人数、助教工作情况
- **管理员**：全校宏观数据、月度报表导出

---

## 🏗️ 技术架构

### 前端技术栈

```
Vue 3              # 渐进式JavaScript框架
├── Vue Router     # 路由管理
├── Pinia          # 状态管理
├── Axios          # HTTP客户端
├── Element Plus   # UI组件库
└── Vite           # 构建工具
```

### 后端技术栈

```
Django 3.2+                    # Web框架
├── Django REST Framework      # RESTful API
├── Simple JWT                 # JWT认证
├── django-cors-headers        # CORS支持
├── django-filter              # API过滤
├── MySQL 8.0                  # 关系型数据库
└── Pillow                     # 图片处理
```

### 开发工具

- **版本控制**：Git + GitHub
- **API测试**：Postman / Insomnia
- **数据库管理**：Navicat / MySQL Workbench
- **代码编辑器**：VSCode / PyCharm

---

## 🏛️ 系统架构

### 前后端分离架构

```
┌─────────────────┐          ┌─────────────────┐
│                 │          │                 │
│  Vue 3 Frontend │  ◄────►  │  Django Backend │
│   (Port 8080)   │   HTTP   │   (Port 8000)   │
│                 │  RESTful │                 │
└─────────────────┘   API    └─────────────────┘
                                      │
                                      ▼
                              ┌───────────────┐
                              │  MySQL 8.0    │
                              │   Database    │
                              └───────────────┘
```

### 认证流程

```
1. 用户登录 → 后端验证 → 返回JWT Token + 角色信息
2. 前端存储Token → 请求时自动携带Token → 后端验证权限
3. 前端根据角色路由到对应页面（student/ta/faculty/admin）
```

---

## 📂 项目结构

```
TeachingAssistant/
│
├── .env                               # 环境变量配置 ✅已配置
├── .gitignore                         # Git忽略配置 ✅已配置
├── .vscode/                           # VSCode/Cursor配置 ✅已配置
│   ├── settings.json                  # 自动激活虚拟环境
│   └── launch.json                    # 调试配置
│
├── venv/                              # Python虚拟环境 ✅已创建
│
├── backend/                           # Django后端
│   ├── accounts/                      # 用户认证模块 ✅已完成
│   │   ├── migrations/                # 数据库迁移文件 ✅8个模型
│   │   ├── management/                # 自定义管理命令
│   │   │   └── commands/
│   │   │       └── init_basic_data.py # 初始化角色权限 ✅
│   │   ├── models.py                  # RBAC用户模型（8个模型）✅
│   │   ├── admin.py                   # Admin后台配置 ✅
│   │   ├── views.py                   # 认证API
│   │   ├── serializers.py             # 序列化器
│   │   ├── permissions.py             # 权限控制
│   │   ├── urls.py                    # 路由配置
│   │   └── tests.py                   # 单元测试
│   │
│   ├── recruitment/                   # 招募管理模块（教师端）✅模型完成
│   │   ├── models.py                  # Position模型 ✅
│   │   └── admin.py                   # Admin后台配置 ✅
│   │
│   ├── application/                   # 申请流程模块（学生端）✅模型完成
│   │   ├── models.py                  # Application模型 ✅
│   │   └── admin.py                   # Admin后台配置 ✅
│   │
│   ├── timesheet/                     # 工时管理模块（助教端）✅模型完成
│   │   ├── models.py                  # Timesheet + Salary模型 ✅
│   │   └── admin.py                   # Admin后台配置 ✅
│   │
│   ├── notifications/                 # 通知模块 ✅模型完成
│   │   ├── models.py                  # Notification模型 ✅
│   │   └── admin.py                   # Admin后台配置 ✅
│   │
│   ├── dashboard/                     # 数据看板模块（管理员端）
│   │
│   ├── TeachingAssistant/             # Django项目配置
│   │   ├── settings.py                # 核心配置文件 ✅已完成配置
│   │   ├── urls.py                    # 主路由配置
│   │   └── wsgi.py                    # WSGI配置
│   │
│   ├── media/                         # 用户上传文件（头像、简历等）
│   ├── static/                        # 静态文件
│   ├── staticfiles/                   # 静态文件收集目录
│   ├── templates/                     # 模板文件
│   ├── manage.py                      # Django管理脚本
│   ├── requirements.txt               # Python依赖 ✅已完成
│   └── README.md                      # 后端说明
│
├── frontend/                          # Vue前端 ✅已完成基础架构
│   ├── src/
│   │   ├── api/                       # API请求封装 ✅
│   │   ├── components/                # 公共组件
│   │   ├── layouts/                   # 布局组件 ✅
│   │   │   ├── StudentLayout.vue      # 学生端布局 ✅
│   │   │   └── FacultyLayout.vue      # 教师端布局 ✅
│   │   ├── views/                     # 页面组件
│   │   │   ├── auth/                  # 认证页面 ✅
│   │   │   │   ├── Login.vue          # 登录页 ✅
│   │   │   │   └── Register.vue       # 注册页 ✅
│   │   │   ├── student/               # 学生端页面 ✅部分完成
│   │   │   │   └── Dashboard.vue      # 学生看板 ✅
│   │   │   └── faculty/               # 教师端页面 ✅部分完成
│   │   │       └── Dashboard.vue      # 教师看板 ✅
│   │   ├── router/                    # 路由配置 ✅
│   │   │   └── index.js               # 基于角色的路由 ✅
│   │   ├── store/                     # 状态管理（Pinia）✅
│   │   │   └── user.js                # 用户状态管理 ✅
│   │   ├── utils/                     # 工具函数 ✅
│   │   └── main.js                    # 入口文件 ✅
│   ├── public/                        # 公共资源
│   ├── package.json                   # NPM依赖配置 ✅
│   ├── vite.config.js                 # Vite构建配置 ✅
│   └── README.md                      # 前端说明
│
├── docs/                              # 项目文档（待完善）
│   ├── api.md                         # API接口文档
│   └── deployment.md                  # 部署文档
│
├── Design.md                          # 系统设计文档 ✅
├── DATABASE_DESIGN.md                 # 数据库设计文档 ✅
├── README.md                          # 项目主说明
├── TODO.md                            # 开发任务清单 ✅进度46.4%
└── PROJECT_STRUCTURE.md               # 项目结构详解
```

### 📝 开发进度

- ✅ **第一阶段：环境搭建与基础配置** (2025-10-14完成)
  - Python 3.8.10 + MySQL 8.0.43 + Node.js v22.14.0
  - Django 4.2.7 + REST Framework + JWT + CORS
  - 虚拟环境、数据库、核心配置已全部完成

- ✅ **第二阶段：数据模型设计** (2025-10-15完成)
  - 实现RBAC权限架构（8个认证模型）
  - 完成5个业务模块（13个数据表）
  - 配置Admin后台管理（13个Admin类）
  - 数据库迁移完成，初始数据已导入

- ✅ **第三阶段：认证与权限系统** (2025-10-15完成)
  - JWT Token认证（Access Token 2小时，Refresh Token 7天）
  - 12个用户认证API接口（注册、登录、登出、个人信息等）
  - 9个权限控制类（角色权限、对象权限、动态权限）
  - RBAC权限系统完全实现

- ✅ **第四阶段（部分）：管理员端开发** (2025-10-16完成)
  - Django Admin后台优化（统计看板、布局优化）
  - 用户管理功能（创建、编辑、删除）
  - 数据统计看板（用户、岗位、申请、薪酬统计）

- ✅ **第五阶段（部分）：前端开发** (2025-10-16完成)
  - Vue 3 + Vite 项目架构
  - 用户登录/注册页面（完整表单验证）
  - 基于角色的路由系统（学生/教师/助教）
  - Pinia状态管理（用户认证）
  - 学生/教师/助教看板页面
  - 响应式布局组件

- 🟦 **进行中**：核心业务API和页面开发（本次更新：学生端岗位/申请、教师端审核、通知信号已完成）
  - 岗位管理（教师端）
  - 申请流程（学生端）✅ 已完成基础闭环（浏览→投递→审核）
  - 工时管理（助教端）

---

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- MySQL 8.0+

### 后端启动

```bash
# 1. 克隆项目
git clone https://github.com/yourusername/TeachingAssistant.git
cd TeachingAssistant

# 2. 进入后端目录
cd backend

# 3. 创建虚拟环境
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac

# 4. 安装依赖
pip install -r requirements.txt

# 5. 创建数据库
mysql -u root -p
CREATE DATABASE teaching_assistant_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit;

# 6. 配置环境变量（.env文件）
# 设置数据库密码和SECRET_KEY

# 7. 执行迁移
python manage.py makemigrations
python manage.py migrate

# 8. 初始化基础数据（角色、权限）
python manage.py init_basic_data

# 9. 创建超级用户
python manage.py createsuperuser

# 10. 启动后端服务
python manage.py runserver
```

后端服务运行在：`http://localhost:8000`

### 前端启动

```bash
# 1. 进入前端目录
cd frontend

# 2. 安装依赖
npm install

# 3. 启动开发服务器
npm run dev
```

前端服务运行在：`http://localhost:5173`（Vite默认端口）

### 访问系统

- **前端页面**：http://localhost:5173 ✅可用（已接入学生端岗位/申请与教师端审核）
  - 登录页面：http://localhost:5173/login
  - 注册页面：http://localhost:5173/register
  
- **后端API**：http://localhost:8000/api/ ✅可用（已启用 recruitment/application 路由）
  - 认证API：http://localhost:8000/api/auth/
  - Swagger文档：http://localhost:8000/swagger/（待配置）

- **管理后台**：http://localhost:8000/admin/ ✅可用
  - 优化的统计看板
  - 用户管理功能

### 测试账号

通过命令创建测试数据：
```bash
python manage.py create_test_data
```

**学生账号**：
- 用户名：student1 / student2 / student3
- 密码：password123

**教师账号**：
- 用户名：teacher1 / teacher2
- 密码：password123

**管理员账号**：
- 用户名：admin
- 密码：password123（通过 `createsuperuser` 创建）

### 📊 数据库架构（已完成）

系统采用 **RBAC（基于角色的访问控制）** 架构，共13个核心数据表：

**用户认证模块（8表）**
- `User` - 核心用户表（支持自定义user_id）
- `Role` - 角色表（学生、教师、管理员）
- `Permission` - 权限表（18种权限）
- `UserRole` - 用户角色关联（支持多角色）
- `RolePermission` - 角色权限关联
- `Student` - 学生扩展信息
- `Faculty` - 教师扩展信息
- `Administrator` - 管理员扩展信息

**业务功能模块（5表）**
- `Position` - 岗位招募
- `Application` - 申请流程
- `Timesheet` - 工时记录
- `Salary` - 薪酬核算
- `Notification` - 消息通知（25种类型）

详细设计请参考：[DATABASE_DESIGN.md](DATABASE_DESIGN.md)

---

## 💻 开发指南

### API开发规范

- 遵循RESTful设计原则
- 统一返回格式：`{"code": 200, "data": {...}, "message": "success"}`
- 错误码标准化：200成功、400参数错误、401未认证、403无权限、404未找到、500服务器错误

### 代码规范

- **Python**：遵循PEP 8规范
- **JavaScript**：遵循ESLint规则
- **Git提交**：使用语义化提交信息（feat/fix/docs/refactor等）

### 分支管理

- `main`：主分支（稳定版本）
- `develop`：开发分支
- `feature/*`：功能分支
- `bugfix/*`：修复分支

### 开发流程

详细的开发任务清单请参考：[TODO.md](TODO.md)

---

## 📡 API文档

详细API文档请参考：
- [后端API说明](backend/README.md)
- [API接口文档](docs/api.md)

### 核心接口示例（本次新增 ✅）

#### 认证相关（已实现）✅

```
POST   /api/auth/register/          # 用户注册
POST   /api/auth/login/             # 用户登录
POST   /api/auth/logout/            # 用户登出
GET    /api/auth/profile/           # 获取用户信息
PUT    /api/auth/profile/           # 更新用户信息
PUT    /api/auth/change-password/   # 修改密码
GET    /api/auth/users/             # 用户列表（管理员）
POST   /api/auth/token/             # 获取Token
POST   /api/auth/token/refresh/     # 刷新Token
```

#### 学生端

```
GET    /api/student/positions/                 # 浏览岗位列表（支持搜索/筛选/排序）
GET    /api/student/positions/{id}/            # 岗位详情
POST   /api/student/applications/submit/       # 投递申请（在线填写 或 上传文件）
GET    /api/student/applications/              # 我的申请列表
GET    /api/student/applications/{id}/         # 申请详情
```

#### 教师端

```
GET    /api/faculty/positions/                      # 我的岗位列表（筛选/排序）
POST   /api/faculty/positions/                      # 创建岗位
PUT    /api/faculty/positions/{id}/                 # 编辑岗位
PATCH  /api/faculty/positions/{id}/close/           # 关闭岗位
GET    /api/faculty/positions/{id}/applications/    # 岗位申请列表
POST   /api/faculty/applications/{id}/review/       # 审核申请（accept/reject），录用将递增 num_filled（防超额）
POST   /api/faculty/applications/{id}/revoke/       # 撤销审核（恢复 reviewing，已录用会回退名额）
```

#### 助教端

```
POST   /api/ta/timesheets/          # 提交工时
GET    /api/ta/salaries/            # 查看薪酬
```

---

## 🌐 部署指南

详细部署文档请参考：[docs/deployment.md](docs/deployment.md)

### PythonAnywhere部署

1. 上传代码到服务器
2. 配置虚拟环境
3. 安装依赖：`pip install -r requirements.txt`
4. 配置MySQL数据库
5. 收集静态文件：`python manage.py collectstatic`
6. 配置WSGI文件

### 生产环境配置

```python
# backend/TeachingAssistant/settings.py
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']

# 使用环境变量
SECRET_KEY = os.environ.get('SECRET_KEY')
```

---

## ❓ 常见问题

### 1. CORS跨域问题

确保 `backend/TeachingAssistant/settings.py` 中配置了：
```python
CORS_ALLOWED_ORIGINS = ["http://localhost:8080"]
```

### 2. JWT Token过期

检查 `SIMPLE_JWT` 配置中的 `ACCESS_TOKEN_LIFETIME`

### 3. 文件上传失败

检查 `MEDIA_ROOT` 和 `MEDIA_URL` 配置

更多问题请查看 [Issues](https://github.com/yourusername/TeachingAssistant/issues)

---

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork本仓库
2. 创建特性分支：`git checkout -b feature/AmazingFeature`
3. 提交更改：`git commit -m 'feat: 添加XX功能'`
4. 推送到分支：`git push origin feature/AmazingFeature`
5. 提交Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 📈 项目统计

- **总进度**：46.4% (26/56 任务完成)
- **代码行数**：10,000+ 行
- **后端模型**：13个数据表
- **API接口**：12个认证接口 + 更多业务接口开发中
- **前端页面**：10+ 个组件
- **开发周期**：3天（2025-10-14 至 2025-10-16）

## ✨ 已完成功能亮点

### 🎯 用户认证系统
- ✅ 完整的用户注册/登录功能（支持学生和教师角色）
- ✅ JWT Token无状态认证（Access + Refresh Token）
- ✅ Token自动刷新机制
- ✅ 登录状态持久化（LocalStorage）
- ✅ 基于角色的自动路由跳转

### 🔐 权限控制系统
- ✅ RBAC权限架构（角色-权限完全解耦）
- ✅ 9种权限控制类（角色权限、对象权限、动态权限）
- ✅ 前后端权限验证（API权限 + 路由守卫）
- ✅ 细粒度权限检查（hasRole、hasPermission）

### 🎨 前端界面
- ✅ 现代化的登录/注册页面（表单验证、错误提示）
- ✅ 学生看板（统计卡片、快捷操作）
- ✅ 教师看板（岗位统计、审核入口）
- ✅ 助教功能入口（工时管理、薪酬查询）
- ✅ 响应式布局（侧边栏可折叠）
- ✅ 统一的导航栏和用户信息展示

### 🔧 管理后台
- ✅ Django Admin后台完全配置（13个模型管理）
- ✅ 优化的统计看板（5个统计卡片）
- ✅ 实时数据统计（用户、岗位、申请、薪酬）
- ✅ 快捷操作按钮（创建用户、创建岗位、审核申请）
- ✅ 优化的UI/UX设计（卡片布局、悬停效果）

### 🗃️ 数据库设计
- ✅ 13个核心数据表
- ✅ RBAC权限架构（8个认证模型）
- ✅ 完整的ER关系和外键约束
- ✅ 数据初始化命令（角色、权限、测试数据）

## 👨‍💻 作者

**Teaching Assistant Team**
- GitHub:(https://github.com/jiashi-feng)
---

## 🙏 致谢

- Django & Django REST Framework 社区
- Vue.js 社区
- Element Plus UI组件库

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给个Star支持一下！**
</div>
