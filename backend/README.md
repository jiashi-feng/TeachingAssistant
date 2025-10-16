# Django后端 - 学生助教管理平台

> Django + Django REST Framework 后端API服务

## 📋 技术栈

- **Django 3.2+** - Python Web框架
- **Django REST Framework** - RESTful API框架
- **Simple JWT** - JWT认证
- **MySQL 8.0** - 关系型数据库
- **django-cors-headers** - CORS跨域支持
- **django-filter** - API过滤

---

## 📂 项目结构

```
backend/
├── accounts/                # 用户认证模块 ✅已完成
│   ├── migrations/          # 数据库迁移文件 ✅8个模型
│   ├── management/          # 自定义管理命令
│   │   └── commands/
│   │       └── init_basic_data.py  # 初始化角色权限 ✅
│   ├── models.py           # RBAC用户模型（8个模型，561行）✅
│   ├── admin.py            # Admin后台配置（8个Admin类）✅
│   ├── views.py            # 认证API视图（12个接口，324行）✅
│   ├── serializers.py      # 序列化器（10个，430行）✅
│   ├── permissions.py      # 权限控制（9个权限类，200行）✅
│   ├── urls.py             # 路由配置（12个路由）✅
│   ├── apps.py             # 应用配置
│   └── tests.py            # 单元测试
│
├── recruitment/            # 招募管理模块 ✅模型完成
│   ├── migrations/         # ✅已迁移
│   ├── models.py           # Position岗位模型 ✅
│   ├── admin.py            # Admin后台配置 ✅
│   ├── views.py            # 岗位管理API
│   ├── serializers.py
│   ├── urls.py
│   └── tests.py
│
├── application/            # 申请流程模块 ✅模型完成
│   ├── migrations/         # ✅已迁移
│   ├── models.py           # Application申请模型 ✅
│   ├── admin.py            # Admin后台配置 ✅
│   ├── views.py            # 申请管理API
│   ├── serializers.py
│   ├── urls.py
│   └── tests.py
│
├── timesheet/              # 工时管理模块 ✅模型完成
│   ├── migrations/         # ✅已迁移
│   ├── models.py           # Timesheet/Salary模型 ✅
│   ├── admin.py            # Admin后台配置 ✅
│   ├── views.py            # 工时管理API
│   ├── serializers.py
│   ├── urls.py
│   └── tests.py
│
├── notifications/          # 通知模块 ✅模型完成
│   ├── migrations/         # ✅已迁移
│   ├── models.py           # Notification通知模型 ✅
│   ├── admin.py            # Admin后台配置 ✅
│   ├── views.py            # 通知API
│   ├── serializers.py
│   ├── signals.py          # 信号处理（自动通知）
│   ├── urls.py
│   └── tests.py
│
├── dashboard/              # 数据看板模块（管理员端）✅部分完成
│   ├── migrations/
│   ├── models.py
│   ├── admin.py            # 自定义Admin站点 ✅
│   ├── admin_views.py      # Admin统计数据视图 ✅
│   ├── context_processors.py
│   ├── views.py            # 统计数据API
│   ├── serializers.py
│   ├── urls.py
│   └── tests.py
│
├── TeachingAssistant/      # Django项目配置
│   ├── settings.py         # 核心配置文件 ✅已完成配置
│   │                       # - DRF + JWT + CORS
│   │                       # - MySQL数据库配置
│   │                       # - 静态文件和媒体文件
│   │                       # - 中文简体 + 上海时区
│   ├── urls.py             # 主路由配置
│   ├── wsgi.py             # WSGI配置
│   └── __init__.py
│
├── media/                  # 用户上传文件（不提交到Git）
│   ├── avatars/            # 用户头像
│   └── resumes/            # 简历文件
│
├── static/                 # 开发环境静态文件
├── staticfiles/            # 生产环境静态文件收集目录
├── templates/              # 模板文件
│   └── admin/              # Django Admin自定义模板 ✅
│       └── index.html      # 优化的Admin首页 ✅
├── manage.py               # Django管理脚本
└── requirements.txt        # Python依赖 ✅已完成
```

### ✅ 开发进度

- [x] **第一阶段：环境搭建** (2025-10-14完成)
  - 环境配置完成
  - 虚拟环境已创建
  - 所有依赖已安装
  - MySQL数据库已配置
  - Django settings.py核心配置已完成

- [x] **第二阶段：数据模型设计** (2025-10-15完成)
  - RBAC权限架构（8个模型）
  - 5个业务模块（13个数据表）
  - Admin后台配置（13个Admin类）
  - 数据库迁移完成
  - 初始化数据导入完成

- [x] **第三阶段：认证与权限系统** (2025-10-15完成)
  - JWT Token认证配置（user_id主键支持）
  - 用户认证API（12个接口）
  - 权限控制系统（9个权限类）
  - 序列化器系统（10个序列化器）
  - URL路由配置（12个路由）
  - 测试通过（注册、登录、Token验证）

- [x] **第四阶段（部分）：管理员端开发** (2025-10-16完成)
  - Django Admin后台优化（统计看板、UI/UX优化）
  - 自定义AdminSite（实时数据统计）
  - 优化Admin首页模板（5个统计卡片）
  - 快捷操作按钮优化（创建用户、岗位、审核申请）
  - 用户管理功能（13个模型的Admin配置）

**当前进度：46.4% (26/56任务完成) | 里程碑M3已达成 + 管理后台完成**

---

## 🚀 快速开始

### 1. 安装依赖

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate       # Windows
# source venv/bin/activate  # Linux/Mac

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置数据库

```bash
# 创建MySQL数据库
mysql -u root -p
CREATE DATABASE teaching_assistant_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit;
```

编辑 `TeachingAssistant/settings.py`：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'teaching_assistant_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 3. 执行迁移

```bash
# 生成迁移文件
python manage.py makemigrations

# 执行迁移
python manage.py migrate

# 初始化基础数据（角色、权限）
python manage.py init_basic_data

# 创建超级用户
python manage.py createsuperuser
```

### 4. 启动服务

```bash
python manage.py runserver
```

访问：
- **API接口**: http://localhost:8000/api/ ✅可用
- **管理后台**: http://localhost:8000/admin/ ✅可用（已优化）

---

## 📡 API路由

### 认证相关 (`/api/auth/`) ✅ 已实现

```
# JWT Token
POST   /api/auth/token/              # 获取JWT Token（登录）
POST   /api/auth/token/refresh/      # 刷新Token

# 用户认证
POST   /api/auth/register/           # 用户注册（学生/教师/管理员）
POST   /api/auth/login/              # 用户登录
POST   /api/auth/logout/             # 用户登出（Token黑名单）
GET    /api/auth/profile/            # 获取当前用户信息
PUT    /api/auth/profile/            # 更新用户信息
PUT    /api/auth/change-password/    # 修改密码

# 用户管理
GET    /api/auth/users/              # 用户列表（支持搜索、筛选、分页）
GET    /api/auth/users/{user_id}/    # 用户详情

# 辅助接口
GET    /api/auth/check-username/     # 检查用户名可用性
GET    /api/auth/check-email/        # 检查邮箱可用性
```

### 学生端 (`/api/student/`)

```
GET    /api/student/positions/              # 浏览岗位列表
GET    /api/student/positions/{id}/         # 岗位详情
POST   /api/student/applications/submit/    # 投递申请
GET    /api/student/applications/           # 我的申请
GET    /api/student/dashboard/              # 学生看板
```

### 教师端 (`/api/faculty/`)

```
POST   /api/faculty/positions/              # 创建岗位
GET    /api/faculty/positions/              # 我的岗位
PUT    /api/faculty/positions/{id}/         # 编辑岗位
PATCH  /api/faculty/positions/{id}/close/   # 关闭岗位
GET    /api/faculty/applications/           # 查看申请
POST   /api/faculty/applications/{id}/review/  # 审核申请
GET    /api/faculty/timesheets/             # 查看工时
GET    /api/faculty/dashboard/              # 教师看板
```

### 助教端 (`/api/ta/`)

```
POST   /api/ta/timesheets/          # 提交工时
GET    /api/ta/timesheets/          # 我的工时
PUT    /api/ta/timesheets/{id}/     # 编辑工时
GET    /api/ta/salaries/            # 薪酬记录
GET    /api/ta/dashboard/           # 助教看板
```

### 管理员端

#### Django Admin后台 ✅ 已完成优化
```
http://localhost:8000/admin/           # Django Admin管理后台

功能：
- 优化的统计看板（用户、岗位、申请、薪酬统计）
- 用户管理（创建、编辑、删除）
- 13个模型的完整CRUD操作
- 快捷操作按钮
- 实时数据统计
```

#### RESTful API (`/api/admin/`)
```
GET    /api/admin/users/                # 用户列表
POST   /api/admin/users/                # 创建用户
PUT    /api/admin/users/{id}/           # 编辑用户
DELETE /api/admin/users/{id}/           # 删除用户
GET    /api/admin/dashboard/            # 全局数据看板
GET    /api/admin/reports/monthly/      # 月度报表
```

### 通知 (`/api/notifications/`)

```
GET    /api/notifications/               # 通知列表
POST   /api/notifications/{id}/read/    # 标记已读
POST   /api/notifications/read-all/     # 全部标记已读
GET    /api/notifications/unread-count/ # 未读数量
```

---

## 🔐 权限控制

### 权限类（`accounts/permissions.py`）

```python
IsStudent      # 学生权限（包含助教）
IsTA           # 助教权限
IsFaculty      # 教师权限
IsAdmin        # 管理员权限
IsOwnerOrReadOnly  # 对象级权限
```

### 使用方式

```python
from accounts.permissions import IsFaculty

class PositionListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsFaculty]
    # ...
```

---

## 🗃️ 数据模型（RBAC架构）

### ✅ 用户认证模块（8个模型）

#### User（核心用户表）
```python
# accounts/models.py
class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=20, unique=True)  # 通用ID
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

#### Role（角色表）
```python
class Role(models.Model):
    role_name = models.CharField(max_length=50, unique=True)
    role_code = models.CharField(max_length=20, unique=True)  # STUDENT/FACULTY/ADMIN
    description = models.TextField(blank=True)
```

#### Permission（权限表）
```python
class Permission(models.Model):
    permission_name = models.CharField(max_length=100, unique=True)
    permission_code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
```

#### UserRole + RolePermission（关联表）
- UserRole: 用户-角色多对多关联
- RolePermission: 角色-权限多对多关联

#### Student / Faculty / Administrator（扩展信息表）
- 一对一扩展User，存储角色特定信息

### ✅ 业务功能模块（5个模型）

#### Position（岗位模型）
```python
# recruitment/models.py
class Position(models.Model):
    title = models.CharField(max_length=200)
    course_name = models.CharField(max_length=200)
    posted_by = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.CharField(max_length=20)  # open/closed/filled
    max_hires = models.IntegerField()
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2)
    # ...
```

#### Application（申请模型）
```python
# application/models.py
class Application(models.Model):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)  # submitted/reviewing/accepted/rejected
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    # ...
    
    class Meta:
        unique_together = ('position', 'applicant')  # 同一岗位不可重复申请
```

#### Timesheet（工时模型）
```python
# timesheet/models.py
class Timesheet(models.Model):
    ta_user = models.ForeignKey(User, on_delete=models.PROTECT)
    position = models.ForeignKey(Position, on_delete=models.PROTECT)
    month = models.DateField()
    work_hours = models.DecimalField(max_digits=5, decimal_places=1)
    status = models.CharField(max_length=20)  # pending/approved/rejected
    # ...
```

#### Salary（薪酬模型）
```python
class Salary(models.Model):
    timesheet = models.OneToOneField(Timesheet, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    generated_by = models.ForeignKey(User, on_delete=models.PROTECT)  # 管理员
    generated_at = models.DateTimeField(auto_now_add=True)
    # ...
```

#### Notification（通知模型）
```python
# notifications/models.py
class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=50)  # 25种类型
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    # ...
```

详细设计请参考：[DATABASE_DESIGN.md](../DATABASE_DESIGN.md)

---

## 🔧 常用命令

```bash
# 创建新的Django应用
python manage.py startapp app_name

# 生成迁移文件
python manage.py makemigrations

# 执行迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 启动开发服务器
python manage.py runserver

# 进入Django shell
python manage.py shell

# 运行测试
python manage.py test

# 收集静态文件
python manage.py collectstatic

# 初始化基础数据（角色、权限）
python manage.py init_basic_data

# 创建测试数据（可选）
python manage.py create_test_data
```

---

## 🧪 测试

### 运行测试

```bash
# 运行所有测试
python manage.py test

# 运行特定应用的测试
python manage.py test accounts

# 运行特定测试类
python manage.py test accounts.tests.UserModelTest
```

### 使用Postman测试API

```bash
# 1. 登录获取token
POST http://localhost:8000/api/auth/login/
Body: {"username":"admin","password":"password"}

# 2. 使用token访问API
GET http://localhost:8000/api/student/positions/
Headers: Authorization: Bearer <your_token>
```

---

## 📝 开发规范

### 代码规范

- 遵循 PEP 8 规范
- 类名使用 PascalCase
- 函数和变量使用 snake_case
- 添加必要的注释和文档字符串

### Git提交规范

```bash
feat: 添加用户登录功能
fix: 修复工时计算错误
docs: 更新API文档
refactor: 重构权限检查逻辑
test: 添加用户模型测试
```

---

## 🔒 安全配置

### 生产环境配置

```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']

# 使用环境变量
SECRET_KEY = os.environ.get('SECRET_KEY')
```

### CORS配置

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",  # 开发环境
    "https://yourdomain.com",  # 生产环境
]
```

---

## 📚 相关文档

- [项目主文档](../README.md)
- [数据库设计文档](../DATABASE_DESIGN.md) ✅
- [系统设计文档](../Design.md) ✅
- [开发任务清单](../TODO.md) ✅
- [项目结构说明](../PROJECT_STRUCTURE.md)

---

## 🐛 常见问题

### 1. 数据库连接失败

检查MySQL服务是否启动，settings.py配置是否正确。

### 2. CORS错误

确保settings.py中配置了CORS_ALLOWED_ORIGINS。

### 3. 迁移错误

删除migrations文件夹中除__init__.py外的所有文件，重新生成迁移。

---

**最后更新**: 2025-10-16

---

## 📝 配置说明

### 环境变量配置（.env文件）

项目使用 `.env` 文件管理敏感配置，位于项目根目录：

```env
# Django配置
SECRET_KEY=your_secret_key_here
DEBUG=True

# 数据库配置
DB_ENGINE=django.db.backends.mysql
DB_NAME=teaching_assistant_db
DB_USER=ta_admin
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306

# 允许的主机
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 已完成的配置

✅ **REST Framework**
- JWT Token认证（Access: 2小时，Refresh: 7天）
- 默认权限：需要登录
- 分页：每页10条
- 支持过滤、搜索、排序

✅ **CORS跨域**
- 开发环境：允许localhost:5173（Vue前端）
- 允许携带Cookie
- 配置所有必需的HTTP方法和请求头

✅ **静态文件和媒体文件**
- STATIC_ROOT: `backend/staticfiles/`
- MEDIA_ROOT: `backend/media/`
- 文件上传限制：10MB

✅ **国际化**
- 语言：中文简体（zh-hans）
- 时区：Asia/Shanghai（东八区）

---

## 🎉 第三阶段完成总结

### ✅ 已实现功能

#### 1. JWT认证系统
- ✅ 配置SIMPLE_JWT，支持user_id作为主键
- ✅ Access Token有效期2小时，Refresh Token有效期7天
- ✅ Token刷新机制和黑名单功能
- ✅ 自定义Token序列化器，嵌入用户角色和权限

#### 2. 用户认证API（12个接口）
- ✅ **注册接口**：支持学生/教师/管理员注册，自动创建扩展信息
- ✅ **登录接口**：返回JWT Token + 用户完整信息 + 角色 + 权限列表
- ✅ **登出接口**：Token黑名单机制，确保安全登出
- ✅ **用户信息接口**：获取和更新当前用户资料
- ✅ **修改密码接口**：旧密码验证 + 新密码强度检查
- ✅ **用户列表接口**：支持搜索、筛选、分页
- ✅ **辅助接口**：检查用户名和邮箱可用性

#### 3. RBAC权限控制（9个权限类）
- ✅ **IsStudent** - 学生权限
- ✅ **IsTA** - 助教权限（检查Student.is_ta字段）
- ✅ **IsFaculty** - 教师权限
- ✅ **IsAdministrator** - 管理员权限
- ✅ **IsStudentOrTA** - 学生或助教
- ✅ **IsFacultyOrAdmin** - 教师或管理员
- ✅ **IsOwner** - 对象所有者
- ✅ **IsOwnerOrReadOnly** - 所有者可写，他人只读
- ✅ **HasPermission** - 基于RBAC的动态权限检查

#### 4. 序列化器系统（10个）
- ✅ **UserSerializer** - 用户完整信息（含角色、权限、扩展信息）
- ✅ **UserSimpleSerializer** - 用户简化信息（列表展示）
- ✅ **RegisterSerializer** - 注册序列化器（支持三种角色）
- ✅ **LoginSerializer** - 登录序列化器
- ✅ **ChangePasswordSerializer** - 修改密码序列化器
- ✅ **RoleSerializer** - 角色序列化器
- ✅ **PermissionSerializer** - 权限序列化器
- ✅ **StudentSerializer** - 学生信息序列化器
- ✅ **FacultySerializer** - 教师信息序列化器
- ✅ **AdministratorSerializer** - 管理员信息序列化器

### 🔧 技术突破

1. **CharField主键问题解决**
   - 修改UserManager的create_user方法
   - 支持user_id在创建时传入，避免主键为空错误
   - 实现：`user = self.model(user_id=user_id, username=username, ...)`

2. **密码安全标准**
   - 使用PBKDF2-SHA256哈希算法
   - 60万次迭代，符合OWASP标准
   - 每个密码使用唯一随机盐值
   - 单向加密，不可逆向解密

3. **JWT无状态认证**
   - 支持分布式部署和水平扩展
   - Token中嵌入用户信息，减少数据库查询
   - 黑名单机制确保登出安全

4. **RBAC动态权限**
   - 通过数据库查询实现权限检查
   - 支持多角色和权限继承
   - 灵活的权限分配和回收

### 📊 代码统计

| 文件                    | 行数      | 说明                         |
| ----------------------- | --------- | ---------------------------- |
| accounts/views.py       | 324       | 12个API视图                  |
| accounts/serializers.py | 430       | 10个序列化器                 |
| accounts/permissions.py | 200       | 9个权限类                    |
| accounts/urls.py        | 58        | 12个路由                     |
| accounts/models.py      | 561       | 8个模型（含UserManager优化） |
| **总计**                | **1,573** | **第三阶段新增/修改代码**    |

### 🎯 下一步计划

继续 **第四阶段：核心业务API开发**
- 实现岗位管理（recruitment/views.py）
- 实现申请流程（application/views.py）
- 实现工时管理（timesheet/views.py）
- 实现通知系统（notifications/views.py）

---

## 📝 管理后台优化总结 (2025-10-16)

### ✅ 已完成的优化

#### 1. Django Admin首页自定义
**文件**: `backend/templates/admin/index.html`
- ✅ 5个统计卡片：用户总数、岗位总数、申请总数、待审核申请、本月薪酬
- ✅ 优化布局：Grid网格布局，响应式设计
- ✅ 修复嵌套标签问题：移除多余的stat-icon嵌套
- ✅ 配色方案：蓝色（用户）、绿色（岗位）、橙色（申请）、红色（待审核）、紫色（薪酬）
- ✅ 快捷操作按钮：创建用户、创建岗位、审核申请
- ✅ 按钮样式优化：字体加粗、增大字号、阴影效果、悬停动画

#### 2. 自定义Admin站点
**文件**: `backend/dashboard/admin_views.py`
- ✅ 创建CustomAdminSite类，重写index方法
- ✅ 实时统计数据注入context
- ✅ 统计逻辑：
  - 用户总数（User.objects.count()）
  - 岗位总数（Position.objects.count()）
  - 申请总数（Application.objects.count()）
  - 待审核申请（status='pending'）
  - 本月薪酬（当月Salary汇总）

#### 3. UI/UX优化
- ✅ 统计卡片：悬停效果（上移+阴影加深）
- ✅ 快捷按钮：增强文字可见度（font-weight: 600, font-size: 15px）
- ✅ 布局间距：卡片间距20px，按钮间距15px
- ✅ 响应式设计：自动适应不同屏幕尺寸


**优化前**：
- ❌ 统计卡片布局混乱（嵌套标签错误）
- ❌ 按钮文字不清晰（字体小、无阴影）
- ❌ 缺少视觉反馈（无悬停效果）

**优化后**：
- ✅ 清晰的网格布局（响应式）
- ✅ 醒目的按钮文字（加粗、增大、阴影）
- ✅ 流畅的交互体验（悬停动画）
- ✅ 实时数据统计（自动更新）

