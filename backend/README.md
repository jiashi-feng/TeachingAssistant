# Django 后端 - 学生助教管理平台

> Django + Django REST Framework 后端 API 服务；支持 MySQL / SQLite（通过环境变量切换）。

## 📋 技术栈

- **Django 3.2+** - Python Web 框架
- **Django REST Framework** - RESTful API
- **Simple JWT** - JWT 认证
- **MySQL 8.0 / SQLite** - 数据库（生产可用 SQLite，见 [部署文档](../docs/deployment.md)）
- **django-cors-headers** - CORS
- **django-filter** - 过滤与搜索

## 📚 文档索引

| 文档                                                  | 说明                     |
| ----------------------------------------------------- | ------------------------ |
| [docs/api.md](../docs/api.md)                         | **API 接口定义（权威）** |
| [docs/database.md](../docs/database.md)               | 数据库表结构概览         |
| [docs/deployment.md](../docs/deployment.md)           | 部署总览与 PA 清单       |
| [docs/developer-guide.md](../docs/developer-guide.md) | 本地环境与常用命令       |

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
├── timesheet/              # 工时管理模块 ✅
│   ├── migrations/         # ✅已迁移
│   ├── models.py           # Timesheet/Salary模型（含支付信息、流水号）✅
│   ├── serializers.py      # 工时/薪酬序列化器（助教、教师、管理员）
│   ├── views.py            # 工时提交、列表、详情、审核、薪酬API
│   ├── admin.py            # Admin 后台（自动计算薪酬、支付信息）✅
│   ├── signals.py          # 工时提交/审核通知 ✅
│   ├── static/timesheet/js/salary_admin.js  # Admin 薪酬表单联动 ✅
│   ├── urls.py
│   └── tests.py
│
├── notifications/          # 通知模块 ✅
│   ├── migrations/         # ✅已迁移
│   ├── models.py           # Notification通知模型 ✅
│   ├── serializers.py      # 通知序列化器
│   ├── views.py            # 通知列表、已读、详情API
│   ├── signals.py          # 信号处理（自动通知：岗位/申请/工时/薪酬）
│   ├── admin.py            # Admin后台配置 ✅
│   ├── urls.py
│   └── tests.py
│
├── dashboard/              # 数据看板与报表（管理员端）✅
│   ├── admin.py            # 自定义 Admin 站点 ✅
│   ├── admin_views.py      # Admin 统计与趋势视图 ✅
│   ├── admin_trends.py     # Admin 趋势分析页（图表+表格）✅
│   ├── views.py            # 月度报表导出、趋势 API ✅
│   ├── urls.py
│   └── ...
│
├── messaging/              # 师生聊天模块 ✅
│   ├── models.py           # Conversation / Message ✅
│   ├── views.py            # 会话与消息 API ✅
│   ├── serializers.py
│   ├── urls.py
│   └── admin.py
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
├── media/                  # 用户上传文件（不提交到Git，已在根 .gitignore 中忽略）
│   ├── avatars/            # 用户头像
│   └── resumes/            # 简历文件
│
├── static/                 # 开发环境静态文件
├── templates/              # 模板文件
│   ├── admin/              # Django Admin 自定义模板 ✅
│   │   ├── index.html      # Admin 首页看板 ✅
│   │   └── trends.html     # Admin 趋势分析页 ✅
│   └── logout_cleanup.html # 登出后跳转前端登录页 ✅
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

**当前状态**：核心认证、岗位/申请/工时/薪酬/通知/聊天、管理端报表与趋势、Admin 优化与薪酬联动均已完成；测试与部署见 [docs/testing-plan.md](../docs/testing-plan.md)、[docs/deployment.md](../docs/deployment.md)。

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

- **本地开发**：可在项目根目录配置 `.env`（与 `backend` 同级），或直接改 `TeachingAssistant/settings.py`。使用 MySQL 时需先创建数据库并配置 `DB_NAME`、`DB_USER`、`DB_PASSWORD` 等。
- **生产 / PythonAnywhere**：通过环境变量控制；使用 SQLite 时设置 `USE_SQLITE=True`，无需 MySQL。详见 [docs/deployment.md](../docs/deployment.md) 与 [docs/deploy-pythonanywhere.md](../docs/deploy-pythonanywhere.md)。

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

## 🧰 自定义管理命令（全局工具）

以下管理命令虽然物理上定义在 `accounts.management.commands` 中，但**作用范围覆盖整个后端项目**，属于“全局运维/初始化工具”：

- `python manage.py init_basic_data`
  - 初始化角色、权限及角色-权限关联关系。
  - 可多次执行，具有幂等性（已存在的数据会被跳过或更新）。

- `python manage.py security_smoke_test`
  - 对部分核心接口（学生/教师/管理员端）做最小 SQL 注入 / XSS 冒烟测试。
  - 验证未登录访问是否被正确拒绝，以及常见恶意载荷不会导致 5xx 服务器错误。

> 当前各 app 下的 `tests.py` 文件主要作为后续单元测试的预留位置，**暂未系统性编写 `TestCase`**；现阶段主要依赖上述管理命令、`scripts/api_smoke_test.py` 以及手工端到端测试。

---

## 📡 API 路由与文档来源

> 说明：本文件仅给出模块级概览，**详细接口列表与字段说明以 `docs/api.md` 为唯一权威来源**。

- 认证与用户：`/api/auth/`（登录支持用户名或邮箱）
- 岗位/申请/工时：学生端、教师端、助教端路由见主路由挂载
- 通知：`/api/notifications/`
- 师生聊天：`/api/chat/`（会话、消息、发起会话等）
- 管理端：`/api/admin/`（报表导出、趋势分析等）

完整路径、请求/响应字段与示例以 **docs/api.md** 为准。

---

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
- 薪酬自动计算与支付信息录入（自动金额、计算明细、流水号、支付方式下拉）
```

#### RESTful API (`/api/admin/`)
- 报表导出：`GET /api/admin/reports/export/`（月度 CSV）
- 趋势分析：`GET /api/admin/reports/trends/?metric=...&group_by=...`
- 其他管理端接口见 [docs/api.md](../docs/api.md)

### 通知 (`/api/notifications/`)

```
GET    /api/notifications/               # 通知列表
POST   /api/notifications/{id}/read/    # 标记已读
POST   /api/notifications/read-all/     # 全部标记已读
GET    /api/notifications/unread-count/ # 未读数量
```

#### 自动通知（Signals）✅ 已接入
- 申请提交：通知岗位发布者（application_submitted）
- 申请审核：通知申请人（application_accepted / application_rejected）
- 审核撤销：通知申请人（application_reviewing）

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
# accounts/models.py（示意）
class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=20, unique=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    real_name = models.CharField(max_length=100, blank=True)
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

详细表结构概览与维护说明见：[docs/database.md](../docs/database.md)。

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

- **单元测试**：各 app 下 `tests.py` 为预留；当前未强制要求编写 TestCase，见上文「自定义管理命令」中的说明。
- **接口冒烟**：根目录 `python scripts/api_smoke_test.py`（需先启动后端）；安全冒烟：`python manage.py security_smoke_test`。
- **测试方案与用例**：[docs/testing-plan.md](../docs/testing-plan.md)。
- **手工/Postman**：登录 `POST /api/auth/login/` 取 Token，请求头 `Authorization: Bearer <token>` 访问需认证接口。

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
    "http://localhost:5173",  # 开发环境
    "https://yourdomain.com",  # 生产环境
]
```

---

## 📚 相关文档

- [项目主文档](../README.md) | [开发任务清单](../TODO.md) | [系统设计](../Design.md)
- **API**：[docs/api.md](../docs/api.md)（权威）  
- **数据库**：[docs/database.md](../docs/database.md)  
- **部署**：[docs/deployment.md](../docs/deployment.md) | [deploy-pythonanywhere.md](../docs/deploy-pythonanywhere.md)  
- **开发与测试**：[docs/developer-guide.md](../docs/developer-guide.md) | [docs/testing-plan.md](../docs/testing-plan.md)

---

## 🐛 常见问题

### 1. 数据库连接失败

检查MySQL服务是否启动，settings.py配置是否正确。

### 2. CORS错误

确保settings.py中配置了CORS_ALLOWED_ORIGINS。

### 3. 迁移错误

删除migrations文件夹中除__init__.py外的所有文件，重新生成迁移。

---

**最后更新**: 2026-03

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

## 📝 完成摘要

- **认证**：JWT（user_id 主键、Token 黑名单）、注册/登录/登出（支持用户名或邮箱）、RBAC 权限类与序列化器。
- **业务**：岗位、申请、工时、薪酬、通知、师生聊天（Conversation/Message）及对应 API。
- **管理端**：Admin 统计看板、趋势分析页（图表+表格）、月度报表导出、薪酬表单联动（salary_admin.js）；登出后跳转前端登录页（logout_cleanup.html）。
- 接口与字段以 **docs/api.md** 为准；数据库与部署见 **docs/database.md**、**docs/deployment.md**。

