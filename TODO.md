# 学生助教管理平台 - 开发任务清单

> 本文档记录项目开发的所有任务，包括优先级、依赖关系和进度跟踪

## 📊 任务状态说明

- ⬜ 未开始
- 🟦 进行中
- ✅ 已完成
- 🔄 需要优化
- ⏸️ 暂停

---

## 🎯 第一阶段：环境搭建与基础配置（✅ 已完成）

**优先级：🔴 最高 | 预计时间：1-2天 | 实际完成：2025-10-14**

### 任务列表

- [x] **1.1 开发环境配置** ✅
  - [x] 安装Python 3.8+ (已安装 3.8.10)
  - [x] 安装MySQL 8.0+ (已安装 8.0.43)
  - [x] 安装Node.js 16+ (已安装 v22.14.0)
  - [x] 配置虚拟环境 `python -m venv venv`
  - [x] 配置Cursor自动激活虚拟环境

- [x] **1.2 后端依赖安装** ✅
  ```bash
  pip install -r requirements.txt
  ```
  - [x] 更新 `requirements.txt`（添加DRF、JWT、CORS等）
  - [x] 验证所有依赖安装成功
  - [x] 添加python-dotenv环境变量管理

- [x] **1.3 数据库配置** ✅
  - [x] 创建MySQL数据库 `teaching_assistant_db`
  - [x] 创建专用数据库用户 `ta_admin`
  - [x] 配置 `settings.py` 数据库连接
  - [x] 创建 `.env` 环境变量文件
  - [x] 测试数据库连接

- [x] **1.4 Django核心配置** ✅
  - [x] 添加第三方库到INSTALLED_APPS（DRF、JWT、CORS等）
  - [x] 配置REST Framework认证和权限
  - [x] 配置JWT Token（2小时有效期）
  - [x] 配置CORS跨域支持
  - [x] 配置静态文件和媒体文件路径
  - [x] 设置语言和时区（中文、上海时区）
  - [x] 配置 `ALLOWED_HOSTS`（从环境变量读取）
  - [x] 添加文件上传配置

---

## 🗃️ 第二阶段：数据模型设计（核心基础）

**优先级：🔴 最高 | 预计时间：3-5天**  
**依赖：第一阶段完成**

### 任务列表

- [ ] **2.1 用户模型（accounts）**
  - [ ] 创建自定义User模型（扩展AbstractUser）
  - [ ] 添加角色字段（student/ta/faculty/admin）
  - [ ] 添加学号、电话、院系、头像等字段
  - [ ] 配置 `AUTH_USER_MODEL`
  - [ ] 执行迁移 `python manage.py makemigrations accounts`

- [ ] **2.2 招募岗位模型（recruitment）**
  - [ ] 创建Position模型
  - [ ] 关联发布教师（ForeignKey to User）
  - [ ] 添加岗位状态（open/closed/filled）
  - [ ] 执行迁移

- [ ] **2.3 申请流程模型（application）**
  - [ ] 创建Application模型
  - [ ] 关联岗位和申请人
  - [ ] 添加申请状态（submitted/reviewing/accepted/rejected）
  - [ ] 设置唯一约束（同一岗位同一人只能申请一次）
  - [ ] 执行迁移

- [ ] **2.4 工时管理模型（timesheet）**
  - [ ] 创建Timesheet模型
  - [ ] 创建Salary模型
  - [ ] 关联助教和岗位
  - [ ] 添加审核状态
  - [ ] 执行迁移

- [ ] **2.5 通知模型（notifications）**
  - [ ] 创建Notification模型
  - [ ] 添加通知类型和已读状态
  - [ ] 执行迁移

- [ ] **2.6 数据库初始化**
  - [ ] 运行所有迁移 `python manage.py migrate`
  - [ ] 创建超级用户 `python manage.py createsuperuser`
  - [ ] 验证admin后台可访问

---

## 🔐 第三阶段：认证与权限系统（关键功能）

**优先级：🔴 最高 | 预计时间：2-3天**  
**依赖：第二阶段完成**

### 任务列表

- [ ] **3.1 JWT认证配置**
  - [ ] 配置 `SIMPLE_JWT` 设置
  - [ ] 创建token获取/刷新接口
  - [ ] 测试token认证流程

- [ ] **3.2 用户认证API（accounts/views.py）**
  - [ ] 注册接口 `POST /api/auth/register/`
  - [ ] 登录接口 `POST /api/auth/login/`（返回token+角色）
  - [ ] 登出接口 `POST /api/auth/logout/`
  - [ ] 获取当前用户信息 `GET /api/auth/profile/`
  - [ ] 修改密码接口 `PUT /api/auth/change-password/`

- [ ] **3.3 权限控制**
  - [ ] 创建权限类（IsStudent/IsTA/IsFaculty/IsAdmin）
  - [ ] 在视图中应用权限装饰器
  - [ ] 测试不同角色的访问控制

- [ ] **3.4 URL配置**
  - [ ] 配置 `accounts/urls.py`
  - [ ] 在主URL中引入 `api/auth/` 路由

---

## 🏗️ 第四阶段：核心业务API开发（可部分并行）

**优先级：🟠 高 | 预计时间：7-10天**  
**依赖：第三阶段完成**

### 4A组：学生端API（可并行开发）

- [ ] **4A.1 岗位浏览（application/views.py）**
  - [ ] 岗位列表接口 `GET /api/student/positions/`
  - [ ] 支持搜索、筛选、排序
  - [ ] 岗位详情接口 `GET /api/student/positions/{id}/`

- [ ] **4A.2 申请管理**
  - [ ] 投递申请 `POST /api/student/applications/submit/`
  - [ ] 我的申请列表 `GET /api/student/applications/`
  - [ ] 申请详情 `GET /api/student/applications/{id}/`
  - [ ] 文件上传处理（简历）

- [ ] **4A.3 学生看板**
  - [ ] 学生数据看板 `GET /api/student/dashboard/`
  - [ ] 统计已申请岗位数、待审核数等

### 4B组：教师端API（可并行开发）

- [ ] **4B.1 岗位管理（recruitment/views.py）**
  - [ ] 创建岗位 `POST /api/faculty/positions/`
  - [ ] 我的岗位列表 `GET /api/faculty/positions/`
  - [ ] 编辑岗位 `PUT /api/faculty/positions/{id}/`
  - [ ] 关闭岗位 `PATCH /api/faculty/positions/{id}/close/`

- [ ] **4B.2 申请审核**
  - [ ] 岗位申请列表 `GET /api/faculty/positions/{id}/applications/`
  - [ ] 审核申请 `POST /api/faculty/applications/{id}/review/`
  - [ ] 批量审核（可选）

- [ ] **4B.3 工时审核**
  - [ ] 工时列表 `GET /api/faculty/timesheets/`
  - [ ] 审核工时 `POST /api/faculty/timesheets/{id}/review/`

- [ ] **4B.4 教师看板**
  - [ ] 教师数据看板 `GET /api/faculty/dashboard/`
  - [ ] 统计岗位数、申请数、在岗助教数

### 4C组：助教端API（可并行开发）

- [ ] **4C.1 工时管理（timesheet/views.py）**
  - [ ] 提交工时表 `POST /api/ta/timesheets/`
  - [ ] 我的工时列表 `GET /api/ta/timesheets/`
  - [ ] 编辑工时 `PUT /api/ta/timesheets/{id}/`

- [ ] **4C.2 薪酬查询**
  - [ ] 薪酬记录列表 `GET /api/ta/salaries/`
  - [ ] 薪酬详情 `GET /api/ta/salaries/{id}/`

- [ ] **4C.3 助教看板**
  - [ ] 助教数据看板 `GET /api/ta/dashboard/`

### 4D组：管理员端API（可并行开发）

- [ ] **4D.1 用户管理（dashboard/views.py）**
  - [ ] 用户列表 `GET /api/admin/users/`
  - [ ] 创建用户 `POST /api/admin/users/`
  - [ ] 编辑用户 `PUT /api/admin/users/{id}/`
  - [ ] 删除用户 `DELETE /api/admin/users/{id}/`

- [ ] **4D.2 数据统计**
  - [ ] 全局数据看板 `GET /api/admin/dashboard/`
  - [ ] 生成月度报表 `GET /api/admin/reports/monthly/`
  - [ ] 导出Excel（可选）

### 4E组：通知系统（可并行开发）

- [ ] **4E.1 通知API（notifications/views.py）**
  - [ ] 通知列表 `GET /api/notifications/`
  - [ ] 标记已读 `POST /api/notifications/{id}/read/`
  - [ ] 全部标记已读 `POST /api/notifications/read-all/`
  - [ ] 未读数量 `GET /api/notifications/unread-count/`

- [ ] **4E.2 自动通知触发**
  - [ ] 使用Django信号（signals）
  - [ ] 申请状态变更通知
  - [ ] 工时审核通知
  - [ ] 岗位发布通知

---

## 🎨 第五阶段：前端开发（可部分并行）

**优先级：🟠 高 | 预计时间：7-10天**  
**依赖：第四阶段对应API完成**

### 任务列表

- [ ] **5.1 前端项目初始化**
  - [ ] 创建Vue 3项目 `npm create vite@latest frontend -- --template vue`
  - [ ] 安装依赖（Vue Router、Pinia、Axios、Element Plus）
  - [ ] 配置代理解决开发环境跨域

- [ ] **5.2 路由与布局**
  - [ ] 配置Vue Router（基于角色的路由）
  - [ ] 创建布局组件（StudentLayout、TALayout、FacultyLayout、AdminLayout）
  - [ ] 实现路由守卫（角色权限控制）

- [ ] **5.3 公共组件**
  - [ ] 登录/注册页面
  - [ ] 导航栏组件
  - [ ] 侧边栏组件
  - [ ] 通知中心组件

- [ ] **5.4 学生端页面**
  - [ ] 学生看板
  - [ ] 岗位浏览页
  - [ ] 岗位详情页
  - [ ] 我的申请页

- [ ] **5.5 助教端页面**
  - [ ] 助教看板
  - [ ] 工时管理页
  - [ ] 薪酬记录页

- [ ] **5.6 教师端页面**
  - [ ] 教师看板
  - [ ] 岗位管理页
  - [ ] 申请审核页
  - [ ] 工时审核页

- [ ] **5.7 管理员端页面**
  - [ ] 管理员看板
  - [ ] 用户管理页
  - [ ] 数据报表页

- [ ] **5.8 API集成**
  - [ ] 封装Axios请求
  - [ ] 配置请求拦截器（自动添加token）
  - [ ] 配置响应拦截器（统一错误处理）

---

## 🔧 第六阶段：功能优化与安全加固

**优先级：🟡 中 | 预计时间：2-3天**  
**依赖：第四、五阶段基本完成**

### 任务列表

- [ ] **6.1 安全加固**
  - [ ] 配置CSRF保护
  - [ ] 文件上传安全检查（文件类型、大小限制）
  - [ ] SQL注入防护测试
  - [ ] XSS防护测试

- [ ] **6.2 性能优化**
  - [ ] 数据库查询优化（select_related、prefetch_related）
  - [ ] API响应缓存（可选）
  - [ ] 前端代码分割与懒加载

- [ ] **6.3 用户体验优化**
  - [ ] 表单验证优化
  - [ ] 加载状态提示
  - [ ] 错误提示优化
  - [ ] 响应式设计调整

---

## 🧪 第七阶段：测试与调试

**优先级：🔴 高 | 预计时间：3-5天**  
**依赖：第四、五阶段完成**

### 任务列表

- [ ] **7.1 后端测试**
  - [ ] 模型单元测试
  - [ ] API接口测试
  - [ ] 权限控制测试
  - [ ] 边界情况测试

- [ ] **7.2 前端测试**
  - [ ] 组件单元测试（可选）
  - [ ] E2E测试（可选）
  - [ ] 浏览器兼容性测试

- [ ] **7.3 集成测试**
  - [ ] 完整业务流程测试
  - [ ] 多角色协作测试
  - [ ] 并发测试

- [ ] **7.4 用户验收测试**
  - [ ] 邀请真实用户测试
  - [ ] 收集反馈并优化

---

## 🚀 第八阶段：部署上线

**优先级：🔴 高 | 预计时间：2-3天**  
**依赖：第七阶段完成**

### 任务列表

- [ ] **8.1 生产环境配置**
  - [ ] 配置环境变量
  - [ ] 关闭DEBUG模式
  - [ ] 配置ALLOWED_HOSTS
  - [ ] 配置HTTPS

- [ ] **8.2 数据库迁移**
  - [ ] 备份本地数据
  - [ ] 在生产环境执行迁移
  - [ ] 创建初始数据

- [ ] **8.3 静态文件处理**
  - [ ] 收集静态文件 `python manage.py collectstatic`
  - [ ] 配置静态文件服务

- [ ] **8.4 文件存储配置**
  - [ ] 配置云存储（AWS S3 / 阿里云OSS）
  - [ ] 迁移媒体文件

- [ ] **8.5 PythonAnywhere部署**
  - [ ] 上传代码到服务器
  - [ ] 配置虚拟环境
  - [ ] 配置WSGI文件
  - [ ] 配置静态文件映射
  - [ ] 测试访问

- [ ] **8.6 前端部署**
  - [ ] 构建生产版本 `npm run build`
  - [ ] 部署到Nginx/CDN
  - [ ] 配置域名

- [ ] **8.7 监控与日志**
  - [ ] 配置错误日志
  - [ ] 配置访问日志
  - [ ] 设置性能监控（可选）

---

## 📚 第九阶段：文档完善

**优先级：🟡 中 | 预计时间：1-2天**  
**可与其他阶段并行**

### 任务列表

- [ ] **9.1 项目文档**
  - [ ] 完善README.md
  - [ ] 编写API文档（docs/api.md）
  - [ ] 编写数据库文档（docs/database.md）
  - [ ] 编写部署文档（docs/deployment.md）

- [ ] **9.2 代码文档**
  - [ ] 添加代码注释
  - [ ] 编写开发者指南
  - [ ] 生成API文档（Swagger/Redoc）

---

## 📊 进度追踪

### 总体进度

- 阶段一：✅ 100% (4/4) - **已完成**
- 阶段二：⬜ 0% (0/6)
- 阶段三：⬜ 0% (0/4)
- 阶段四：⬜ 0% (0/18)
- 阶段五：⬜ 0% (0/8)
- 阶段六：⬜ 0% (0/3)
- 阶段七：⬜ 0% (0/4)
- 阶段八：⬜ 0% (0/7)
- 阶段九：⬜ 0% (0/2)

**总进度：4/56 任务完成 (7.1%)**

---

## 🎯 里程碑

- [x] **M1：环境搭建完成** ✅ (阶段一完成 - 2025-10-14)
- [ ] **M2：数据模型完成** (阶段二完成)
- [ ] **M3：认证系统完成** (阶段三完成)
- [ ] **M4：后端API完成** (阶段四完成)
- [ ] **M5：前端开发完成** (阶段五完成)
- [ ] **M6：测试通过** (阶段七完成)
- [ ] **M7：成功部署** (阶段八完成)
- [ ] **M8：项目交付** (所有阶段完成)

---

## 🔄 并行开发建议

可以同时进行的任务组：

1. **后端API开发**：4A、4B、4C、4D、4E 可以由不同开发者并行开发
2. **前端+后端**：某个API完成后，对应的前端页面可以立即开始开发
3. **文档编写**：可在开发过程中同步进行

---

## 📝 注意事项

1. **版本控制**：每完成一个任务，提交一次Git
2. **分支管理**：主分支保持稳定，功能开发使用feature分支
3. **代码审查**：重要功能合并前进行代码审查
4. **定期备份**：数据库和代码定期备份
5. **问题记录**：遇到的问题记录在Issues中

---

**最后更新时间：** 2025-10-14

---

## 📝 第一阶段完成总结

### ✅ 已配置项

1. **开发环境**
   - Python 3.8.10 + 虚拟环境
   - MySQL 8.0.43 + 专用数据库用户
   - Node.js v22.14.0 + Yarn
   - Cursor IDE配置

2. **Django配置**
   - Django 4.2.7 (LTS版本)
   - REST Framework + JWT认证
   - CORS跨域支持
   - 中文简体 + 上海时区
   - 静态文件和媒体文件路径

3. **安全配置**
   - `.env` 环境变量管理
   - 数据库密码隔离
   - SECRET_KEY保护
   - 文件上传限制（10MB）

4. **项目结构**
   - 6个功能模块已创建
   - `.gitignore` 配置完善
   - `.vscode` 自动激活配置

### 🎯 下一步

开始 **第二阶段：数据模型设计**，创建核心数据模型（User、Position、Application等）。

