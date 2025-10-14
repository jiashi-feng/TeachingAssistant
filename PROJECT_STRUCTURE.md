# 项目结构说明

## 📁 整体架构

本项目采用**前后端分离**架构：

```
TeachingAssistant/
├── 后端 (Django REST Framework)
│   ├── accounts/              # 用户认证模块
│   ├── recruitment/           # 招募管理模块
│   ├── application/           # 申请流程模块
│   ├── timesheet/             # 工时管理模块
│   ├── notifications/         # 通知模块
│   ├── dashboard/             # 数据看板模块
│   ├── TeachingAssistant/     # Django配置
│   └── manage.py              # Django管理脚本
│
├── 前端 (Vue 3 + Vite)
│   └── frontend/              # Vue前端项目
│
├── 文档
│   ├── docs/                  # 技术文档
│   ├── README.md              # 项目主说明
│   ├── TODO.md                # 开发任务清单
│   └── PROJECT_STRUCTURE.md   # 本文件
│
└── 配置文件
    ├── requirements.txt       # Python依赖
    └── .gitignore            # Git忽略配置
```

---

## 🔙 后端结构详解

### Django应用模块

#### 1️⃣ accounts - 用户认证模块
**路径**: `accounts/`  
**功能**: 用户注册、登录、权限管理  
**API路由**: `/api/auth/`

```
accounts/
├── models.py          # 自定义用户模型（User）
├── views.py           # 认证API视图
├── serializers.py     # 数据序列化器
├── permissions.py     # 权限控制类
└── urls.py           # 路由配置
```

**核心模型**:
- `User`: 自定义用户模型，包含角色字段（student/ta/faculty/admin）

**核心API**:
- POST `/api/auth/register/` - 用户注册
- POST `/api/auth/login/` - 用户登录
- GET `/api/auth/profile/` - 获取用户信息
- PUT `/api/auth/change-password/` - 修改密码

---

#### 2️⃣ recruitment - 招募管理模块
**路径**: `recruitment/`  
**功能**: 岗位发布与管理（教师端）  
**API路由**: `/api/faculty/`

```
recruitment/
├── models.py          # 岗位模型
├── views.py           # 岗位管理API
├── serializers.py     # 序列化器
└── urls.py           # 路由配置
```

**核心模型**:
- `Position`: 助教岗位信息

**核心API**:
- POST `/api/faculty/positions/` - 创建岗位
- GET `/api/faculty/positions/` - 我的岗位列表
- PUT `/api/faculty/positions/{id}/` - 编辑岗位
- PATCH `/api/faculty/positions/{id}/close/` - 关闭岗位

---

#### 3️⃣ application - 申请流程模块
**路径**: `application/`  
**功能**: 学生申请管理  
**API路由**: `/api/student/`

```
application/
├── models.py          # 申请模型
├── views.py           # 申请管理API
├── serializers.py     # 序列化器
└── urls.py           # 路由配置
```

**核心模型**:
- `Application`: 助教申请记录

**核心API**:
- GET `/api/student/positions/` - 浏览岗位
- POST `/api/student/applications/submit/` - 投递申请
- GET `/api/student/applications/` - 我的申请

---

#### 4️⃣ timesheet - 工时管理模块
**路径**: `timesheet/`  
**功能**: 工时提交与薪酬管理  
**API路由**: `/api/ta/`

```
timesheet/
├── models.py          # 工时、薪酬模型
├── views.py           # 工时管理API
├── serializers.py     # 序列化器
└── urls.py           # 路由配置
```

**核心模型**:
- `Timesheet`: 工时记录
- `Salary`: 薪酬记录

**核心API**:
- POST `/api/ta/timesheets/` - 提交工时
- GET `/api/ta/timesheets/` - 我的工时列表
- GET `/api/ta/salaries/` - 薪酬记录

---

#### 5️⃣ notifications - 通知模块
**路径**: `notifications/`  
**功能**: 消息通知管理  
**API路由**: `/api/notifications/`

```
notifications/
├── models.py          # 通知模型
├── views.py           # 通知API
├── signals.py         # 自动通知触发
├── serializers.py     # 序列化器
└── urls.py           # 路由配置
```

**核心模型**:
- `Notification`: 通知消息

**核心API**:
- GET `/api/notifications/` - 通知列表
- POST `/api/notifications/{id}/read/` - 标记已读
- GET `/api/notifications/unread-count/` - 未读数量

---

#### 6️⃣ dashboard - 数据看板模块
**路径**: `dashboard/`  
**功能**: 数据统计与报表（管理员端）  
**API路由**: `/api/admin/`

```
dashboard/
├── views.py           # 统计API
├── serializers.py     # 序列化器
└── urls.py           # 路由配置
```

**核心API**:
- GET `/api/admin/dashboard/` - 全局数据看板
- GET `/api/admin/users/` - 用户管理
- GET `/api/admin/reports/monthly/` - 月度报表

---

### Django配置

#### TeachingAssistant/ - 项目配置目录

```
TeachingAssistant/
├── settings.py        # Django设置（重要配置）
├── urls.py           # 主路由配置
├── wsgi.py           # WSGI配置
└── asgi.py           # ASGI配置（可选）
```

**settings.py 关键配置**:
- `INSTALLED_APPS`: 包含所有Django应用 + DRF + CORS
- `REST_FRAMEWORK`: DRF配置（认证、权限、分页）
- `SIMPLE_JWT`: JWT认证配置
- `CORS_ALLOWED_ORIGINS`: 跨域配置
- `DATABASES`: MySQL数据库配置
- `AUTH_USER_MODEL`: 自定义用户模型

---

## 🎨 前端结构详解

### frontend/ - Vue 3前端项目

详细说明请参考：[frontend/README.md](frontend/README.md)

**推荐结构**:
```
frontend/
├── src/
│   ├── api/              # API请求封装
│   ├── assets/           # 静态资源
│   ├── components/       # 公共组件
│   ├── layouts/          # 布局组件（按角色分）
│   ├── views/            # 页面组件（按角色分）
│   ├── router/           # 路由配置
│   ├── store/            # 状态管理（Pinia）
│   ├── utils/            # 工具函数
│   ├── App.vue          # 根组件
│   └── main.js          # 入口文件
├── package.json
└── vite.config.js
```

---

## 🗂️ 其他目录说明

### media/ - 用户上传文件
存储用户上传的文件（简历、头像等）

### static/ - 静态文件
Django静态文件（CSS、JS、图片等）

### templates/ - 模板文件
Django模板文件（前后端分离项目中可能用不到）

### scripts/ - 脚本文件
存放自动化脚本、数据导入脚本等

### docs/ - 文档目录
- `api.md`: API接口文档
- `database.md`: 数据库设计文档
- `deployment.md`: 部署文档

---

## 🔗 前后端通信

### API请求流程

```
前端 (Vue)                    后端 (Django)
   │                              │
   │  1. 登录请求                 │
   ├──────────────────────────────>│
   │     POST /api/auth/login/    │
   │                               │
   │  2. 返回 JWT Token + 角色    │
   │<──────────────────────────────┤
   │                               │
   │  3. 后续请求携带Token         │
   ├──────────────────────────────>│
   │     Header: Authorization:    │
   │            Bearer <token>     │
   │                               │
   │  4. 验证Token并返回数据       │
   │<──────────────────────────────┤
```

### 跨域配置

**后端 (settings.py)**:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",  # Vue开发服务器
]
```

**前端 (vite.config.js)**:
```javascript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    },
  },
}
```

---

## 🚀 启动流程

### 开发环境

#### 1. 启动后端
```bash
# 激活虚拟环境
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 运行迁移
python manage.py migrate

# 启动服务
python manage.py runserver
```

后端运行在: http://localhost:8000

#### 2. 启动前端
```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端运行在: http://localhost:8080

---

## 📝 开发规范

### 后端规范

1. **模型命名**: PascalCase (如 `Position`, `Application`)
2. **视图命名**: 使用类视图，继承DRF的通用视图
3. **URL命名**: 使用RESTful风格
4. **权限控制**: 每个视图必须指定 `permission_classes`
5. **代码风格**: 遵循 PEP 8

### 前端规范

1. **组件命名**: PascalCase (如 `UserProfile.vue`)
2. **API调用**: 统一通过 `src/api/` 模块
3. **路由守卫**: 检查用户角色和权限
4. **状态管理**: 全局状态用Pinia，局部状态用组件state
5. **代码风格**: 遵循 ESLint 规则

---

## 🔐 安全要点

1. **密码存储**: Django自动哈希加密
2. **Token安全**: JWT存储在localStorage，请求时携带
3. **CORS控制**: 严格限制允许的源
4. **文件上传**: 限制文件类型和大小
5. **SQL注入**: 使用Django ORM避免注入
6. **XSS防护**: Vue自动转义，后端设置安全头

---

## 📚 参考文档

- [Django官方文档](https://docs.djangoproject.com/)
- [DRF官方文档](https://www.django-rest-framework.org/)
- [Vue 3官方文档](https://v3.vuejs.org/)
- [开发任务清单](TODO.md)
- [项目README](README.md)

---

**最后更新**: 2025-10-13

