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

| 角色 | 主要功能 |
|------|---------|
| **学生** | 浏览岗位、投递申请、查看申请状态 |
| **助教** | 填写工时、查看薪酬记录 |
| **教师** | 发布岗位、审核申请、审批工时、评价助教 |
| **管理员** | 用户管理、数据统计、生成报表 |

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
├── backend/                           # Django后端
│   ├── accounts/                      # 用户认证模块
│   │   ├── models.py                  # 自定义用户模型
│   │   ├── views.py                   # 认证API
│   │   ├── serializers.py             # 序列化器
│   │   ├── permissions.py             # 权限控制
│   │   └── urls.py                    # 路由配置
│   │
│   ├── recruitment/                   # 招募管理模块
│   ├── application/                   # 申请流程模块
│   ├── timesheet/                     # 工时管理模块
│   ├── notifications/                 # 通知模块
│   ├── dashboard/                     # 数据看板模块
│   │
│   ├── TeachingAssistant/             # Django配置
│   │   ├── settings.py                # 核心配置文件
│   │   ├── urls.py                    # 主路由配置
│   │   └── wsgi.py                    # WSGI配置
│   │
│   ├── media/                         # 用户上传文件
│   ├── static/                        # 静态文件
│   ├── manage.py                      # Django管理脚本
│   ├── requirements.txt               # Python依赖
│   └── README.md                      # 后端说明
│
├── frontend/                          # Vue前端（待创建）
│   ├── src/
│   │   ├── api/                       # API请求封装
│   │   ├── components/                # 公共组件
│   │   ├── layouts/                   # 布局组件
│   │   ├── views/                     # 页面组件
│   │   ├── router/                    # 路由配置
│   │   ├── store/                     # 状态管理
│   │   └── main.js                    # 入口文件
│   ├── package.json
│   └── README.md                      # 前端说明
│
├── docs/                              # 项目文档
│   ├── api.md                         # API接口文档
│   ├── database.md                    # 数据库设计
│   └── deployment.md                  # 部署文档
│
├── README.md                          # 项目主说明
├── TODO.md                            # 开发任务清单
└── PROJECT_STRUCTURE.md               # 项目结构详解
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

# 6. 配置数据库（修改 TeachingAssistant/settings.py）
# 设置数据库用户名和密码

# 7. 执行迁移
python manage.py makemigrations
python manage.py migrate

# 8. 创建超级用户
python manage.py createsuperuser

# 9. 启动后端服务
python manage.py runserver
```

后端服务运行在：`http://localhost:8000`

### 前端启动（待创建）

```bash
# 1. 进入前端目录
cd frontend

# 2. 初始化Vue项目
npm create vite@latest . -- --template vue

# 3. 安装依赖
npm install
npm install vue-router@4 pinia axios element-plus

# 4. 启动开发服务器
npm run dev
```

前端服务运行在：`http://localhost:8080`

### 访问系统

- **前端页面**：http://localhost:8080
- **后端API**：http://localhost:8000/api/
- **管理后台**：http://localhost:8000/admin/

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

### 核心接口示例

#### 认证相关

```
POST   /api/auth/register/          # 用户注册
POST   /api/auth/login/             # 用户登录
GET    /api/auth/profile/           # 获取用户信息
```

#### 学生端

```
GET    /api/student/positions/      # 浏览岗位列表
POST   /api/student/applications/submit/  # 投递申请
```

#### 教师端

```
POST   /api/faculty/positions/      # 创建岗位
POST   /api/faculty/applications/{id}/review/  # 审核申请
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

## 👨‍💻 作者

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

---

## 🙏 致谢

- Django & Django REST Framework 社区
- Vue.js 社区
- Element Plus UI组件库

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给个Star支持一下！**

Made with ❤️ by [Your Name]

</div>
