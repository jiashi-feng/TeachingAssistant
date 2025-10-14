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
├── accounts/                # 用户认证模块
│   ├── migrations/          # 数据库迁移文件
│   ├── models.py           # 自定义用户模型
│   ├── views.py            # 认证API视图
│   ├── serializers.py      # 序列化器
│   ├── permissions.py      # 权限控制
│   ├── urls.py             # 路由配置
│   ├── admin.py            # Admin后台配置
│   ├── apps.py             # 应用配置
│   └── tests.py            # 单元测试
│
├── recruitment/            # 招募管理模块（教师端）
│   ├── migrations/
│   ├── models.py           # Position岗位模型
│   ├── views.py            # 岗位管理API
│   ├── serializers.py
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
│
├── application/            # 申请流程模块（学生端）
│   ├── migrations/
│   ├── models.py           # Application申请模型
│   ├── views.py            # 申请管理API
│   ├── serializers.py
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
│
├── timesheet/              # 工时管理模块（助教端）
│   ├── migrations/
│   ├── models.py           # Timesheet/Salary模型
│   ├── views.py            # 工时管理API
│   ├── serializers.py
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
│
├── notifications/          # 通知模块
│   ├── migrations/
│   ├── models.py           # Notification通知模型
│   ├── views.py            # 通知API
│   ├── serializers.py
│   ├── signals.py          # 信号处理（自动通知）
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
│
├── dashboard/              # 数据看板模块（管理员端）
│   ├── migrations/
│   ├── models.py
│   ├── views.py            # 统计数据API
│   ├── serializers.py
│   ├── urls.py
│   ├── admin.py
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
├── templates/              # 模板文件（如果需要）
├── manage.py               # Django管理脚本
└── requirements.txt        # Python依赖 ✅已完成
```

### ✅ 第一阶段完成状态

- [x] 环境配置完成
- [x] 虚拟环境已创建
- [x] 所有依赖已安装
- [x] MySQL数据库已配置
- [x] Django settings.py核心配置已完成
- [ ] 数据模型设计（进行中）

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

# 创建超级用户
python manage.py createsuperuser
```

### 4. 启动服务

```bash
python manage.py runserver
```

访问：
- **API接口**: http://localhost:8000/api/
- **管理后台**: http://localhost:8000/admin/

---

## 📡 API路由

### 认证相关 (`/api/auth/`)

```
POST   /api/auth/register/          # 用户注册
POST   /api/auth/login/             # 用户登录
POST   /api/auth/logout/            # 用户登出
GET    /api/auth/profile/           # 获取用户信息
PUT    /api/auth/change-password/   # 修改密码
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

### 管理员端 (`/api/admin/`)

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

## 🗃️ 数据模型

### User (自定义用户模型)

```python
# accounts/models.py
class User(AbstractUser):
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    student_id = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=20)
    department = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars/')
```

### Position (岗位模型)

```python
# recruitment/models.py
class Position(models.Model):
    title = models.CharField(max_length=200)
    course_name = models.CharField(max_length=200)
    faculty = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)  # open/closed/filled
    # ...
```

### Application (申请模型)

```python
# application/models.py
class Application(models.Model):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)  # submitted/reviewing/accepted/rejected
    resume = models.FileField(upload_to='resumes/')
    # ...
```

### Timesheet (工时模型)

```python
# timesheet/models.py
class Timesheet(models.Model):
    ta = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    month = models.DateField()
    work_hours = models.DecimalField(max_digits=5, decimal_places=1)
    status = models.CharField(max_length=20)  # pending/approved/rejected
    # ...
```

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
- [开发任务清单](../TODO.md)
- [项目结构说明](../PROJECT_STRUCTURE.md)
- [开发指南](../DEVELOPMENT.md)
- [API文档](../docs/api.md)

---

## 🐛 常见问题

### 1. 数据库连接失败

检查MySQL服务是否启动，settings.py配置是否正确。

### 2. CORS错误

确保settings.py中配置了CORS_ALLOWED_ORIGINS。

### 3. 迁移错误

删除migrations文件夹中除__init__.py外的所有文件，重新生成迁移。

---

**最后更新**: 2025-10-14

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

