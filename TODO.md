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

## 🗃️ 第二阶段：数据模型设计（核心基础）✅

**优先级：🔴 最高 | 预计时间：3-5天 | 实际完成：2025-10-15**  
**依赖：第一阶段完成**

### 任务列表

- [x] **2.1 用户模型（accounts）** ✅
  - [x] 创建自定义User模型（基于RBAC架构，8个模型）
  - [x] 添加角色系统（Role、Permission、UserRole、RolePermission）
  - [x] 添加扩展表（Student、Faculty、Administrator）
  - [x] 配置 `AUTH_USER_MODEL` 和 `DEFAULT_AUTO_FIELD`
  - [x] 执行迁移 `python manage.py makemigrations accounts`

- [x] **2.2 招募岗位模型（recruitment）** ✅
  - [x] 创建Position模型
  - [x] 关联发布教师（ForeignKey to User）
  - [x] 添加岗位状态（open/closed/filled）
  - [x] 执行迁移

- [x] **2.3 申请流程模型（application）** ✅
  - [x] 创建Application模型
  - [x] 关联岗位和申请人
  - [x] 添加申请状态（submitted/reviewing/accepted/rejected）
  - [x] 设置唯一约束（同一岗位同一人只能申请一次）
  - [x] 执行迁移

- [x] **2.4 工时管理模型（timesheet）** ✅
  - [x] 创建Timesheet模型
  - [x] 创建Salary模型（含管理员生成信息）
  - [x] 关联助教和岗位
  - [x] 添加审核状态
  - [x] 执行迁移

- [x] **2.5 通知模型（notifications）** ✅
  - [x] 创建Notification模型
  - [x] 添加25种通知类型和已读状态
  - [x] 执行迁移

- [x] **2.6 数据库初始化** ✅
  - [x] 运行所有迁移 `python manage.py migrate`
  - [x] 配置所有模块的Admin后台（13个Admin类）
  - [x] 创建初始化数据命令（角色、权限）
  - [x] 创建测试数据命令（用户、岗位、申请）
  - [x] 验证admin后台可访问
  - [x] 解决MySQL时区问题（USE_TZ=False）

---

## 🔐 第三阶段：认证与权限系统（关键功能）✅

**优先级：🔴 最高 | 预计时间：2-3天 | 实际完成：2025-10-15**  
**依赖：第二阶段完成**

### 任务列表

- [x] **3.1 JWT认证配置** ✅
  - [x] 配置 `SIMPLE_JWT` 设置（设置user_id作为用户标识）
  - [x] 创建token获取/刷新接口（CustomTokenObtainPairView）
  - [x] 测试token认证流程

- [x] **3.2 用户认证API（accounts/views.py）** ✅
  - [x] 注册接口 `POST /api/auth/register/`（支持学生/教师/管理员）
  - [x] 登录接口 `POST /api/auth/login/`（返回token+用户完整信息+角色+权限）
  - [x] 登出接口 `POST /api/auth/logout/`（Token黑名单机制）
  - [x] 获取当前用户信息 `GET /api/auth/profile/`
  - [x] 更新用户信息接口 `PUT /api/auth/profile/`（支持修改姓名、手机、邮箱、头像上传）
  - [x] 修改密码接口 `PUT /api/auth/change-password/`
  - [x] 用户列表接口 `GET /api/auth/users/`
  - [x] 辅助接口（检查用户名、邮箱可用性）

- [x] **3.3 权限控制** ✅
  - [x] 创建9个权限类（IsStudent/IsTA/IsFaculty/IsAdministrator等）
  - [x] 对象级权限控制（IsOwner/IsOwnerOrReadOnly）
  - [x] 基于RBAC的动态权限检查（HasPermission）

- [x] **3.4 URL配置** ✅
  - [x] 配置 `accounts/urls.py`（12个API路由）
  - [x] 在主URL中引入 `api/auth/` 路由
  - [x] 配置静态文件和媒体文件路由

---

## 🏗️ 第四阶段：核心业务API开发（可部分并行）

**优先级：🟠 高 | 预计时间：7-10天**  
**依赖：第三阶段完成**

### 4A组：学生端API（可并行开发）

- [x] **4A.1 岗位浏览（recruitment/views.py）** ✅
  - [x] 岗位列表接口 `GET /api/student/positions/`
  - [x] 支持搜索、筛选、排序
  - [x] 岗位详情接口 `GET /api/student/positions/{id}/`

- [x] **4A.2 申请管理** ✅
  - [x] 投递申请 `POST /api/student/applications/submit/`（在线填写 或 上传文件，二选一）
  - [x] 我的申请列表 `GET /api/student/applications/`
  - [x] 申请详情 `GET /api/student/applications/{id}/`
  - [x] 文件上传处理（简历，10MB，pdf/doc/docx白名单）

- [x] **4A.3 学生看板** ✅
  - [x] 学生数据看板 `GET /api/student/dashboard/`
  - [x] 统计可申请岗位数、我的申请数、待审核数、已通过数

### 4B组：教师端API（可并行开发）

- [x] **4B.1 岗位管理（recruitment/views.py）** ✅
  - [x] 创建岗位 `POST /api/faculty/positions/`
  - [x] 我的岗位列表 `GET /api/faculty/positions/`
  - [x] 编辑岗位 `PUT /api/faculty/positions/{id}/`
  - [x] 关闭岗位 `PATCH /api/faculty/positions/{id}/close/`

- [x] **4B.2 申请审核** ✅
  - [x] 岗位申请列表 `GET /api/faculty/positions/{id}/applications/`
  - [x] 审核申请 `POST /api/faculty/applications/{id}/review/`
  - [x] 撤销审核 `POST /api/faculty/applications/{id}/revoke/`（恢复为reviewing，已通过将回退名额）
  - [ ] 批量审核（可选）

- [x] **4B.3 工时审核** ✅
  - [x] 工时列表 `GET /api/faculty/timesheets/`
  - [x] 工时详情 `GET /api/faculty/timesheets/{id}/`（教师可查看自己岗位的助工时表）
  - [x] 审核工时 `POST /api/faculty/timesheets/{id}/review/`

- [x] **4B.4 教师看板** ✅
  - [x] 教师数据看板 `GET /api/faculty/dashboard/`
  - [x] 统计岗位数、申请数、在岗助教数、待审核工时

### 4C组：助教端API（可并行开发）

- [x] **4C.1 工时管理（timesheet/views.py）** ✅
  - [x] 提交工时表 `POST /api/ta/timesheets/`
  - [x] 我的工时列表 `GET /api/ta/timesheets/`
  - [x] 编辑工时 `PUT /api/ta/timesheets/{id}/update/`

- [x] **4C.2 薪酬查询** ✅
  - [x] 薪酬记录列表 `GET /api/ta/salaries/`
  - [x] 薪酬详情 `GET /api/ta/salaries/{id}/`

- [x] **4C.3 助教看板** ✅
  - [x] 助教数据看板 `GET /api/ta/dashboard/`

### 4D组：管理员端API（可并行开发）

- [x] **4D.1 用户管理（dashboard/admin_views.py）** ✅
  - [x] 用户列表（Django Admin后台）
  - [x] 创建用户（Django Admin后台）
  - [x] 编辑用户（Django Admin后台）
  - [x] 删除用户（Django Admin后台）

- [x] **4D.2 数据统计** ✅
  - [x] 全局数据看板（Django Admin首页）
  - [x] 统计用户总数、岗位总数、申请总数
  - [x] 本月薪酬统计（修复为按工时月份统计）
  - [x] 生成月度报表 `GET /api/admin/reports/monthly/`
  - [ ] 导出Excel（可选）
  - [x] 待审核申请统计修复（`submitted/reviewing` 双状态）

- [x] **4D.3 薪酬管理优化（timesheet/admin.py）** ✅
  - [x] Admin表单自动计算薪酬金额与计算明细（选择工时时自动填充）
  - [x] 教师端新增工时详情API，支持管理员/教师查看详情
  - [x] 支付方式下拉选择（银行转账/支付宝/微信/现金等）
  - [x] 交易流水号自动生成（UUID）

### 4E组：通知系统（可并行开发）

- [x] **4E.1 通知API（notifications/views.py）** ✅
  - [x] 通知列表 `GET /api/notifications/`
  - [x] 通知详情 `GET /api/notifications/{id}/`（查看时自动标记为已读）
  - [x] 标记已读 `POST /api/notifications/{id}/read/`
  - [x] 全部标记已读 `POST /api/notifications/read-all/`
  - [x] 未读数量 `GET /api/notifications/unread-count/`

- [x] **4E.2 自动通知触发** ✅
  - [x] 使用Django信号（signals）
  - [x] 申请提交/状态变更通知（application_submitted / application_accepted / application_rejected）
  - [x] 工时提交通知（timesheet_submitted）
  - [x] 工时审核通知（timesheet_approved / timesheet_rejected）
  - [x] 岗位发布通知（position_published - 通知所有学生用户）

---

## 🎨 第五阶段：前端开发（✅ 已完成）

**优先级：🟠 高 | 预计时间：7-10天**  
**依赖：第四阶段对应API完成**

### 任务列表

- [x] **5.1 前端项目初始化** ✅
  - [x] 创建Vue 3项目 `npm create vite@latest frontend -- --template vue`
  - [x] 安装依赖（Vue Router、Pinia、Axios、Element Plus）
  - [x] 配置代理解决开发环境跨域

- [x] **5.2 路由与布局** ✅
  - [x] 配置Vue Router（基于角色的路由）
  - [x] 创建布局组件（StudentLayout、FacultyLayout）
  - [x] 实现路由守卫（角色权限控制）

- [x] **5.3 公共组件** ✅
  - [x] 登录/注册页面（完整的表单验证和错误处理）
  - [x] 导航栏组件
  - [x] 侧边栏组件
  - [x] 通知中心组件（下拉菜单、未读徽章、分类筛选、标记已读）
  - [x] 个人信息页面（Profile.vue - 用户信息展示、编辑、头像上传）
  - [x] 设置页面（Settings.vue - 修改密码、密码强度提示）

- [x] **5.4 学生端页面** ✅
  - [x] 学生看板（统计卡片和快捷操作）
  - [x] 岗位浏览页（接入API）
  - [x] 岗位详情页（接入API，投递在线/文件）
  - [x] 我的申请页（接入API）

- [x] **5.5 助教端页面** ✅
  - [x] 助教看板（工时和薪酬入口）
  - [x] 工时管理页（列表、提交、编辑功能）
  - [x] 薪酬记录页（列表、详情、统计信息）

- [x] **5.6 教师端页面** ✅
  - [x] 教师看板（接入API数据，显示统计和待办事项）
  - [x] 岗位管理页
  - [x] 申请审核页（接入API）
  - [x] 工时审核页（列表、筛选、审核功能）

- [x] **5.7 管理员端页面** ✅
  - [x] 管理员看板（Django Admin后台优化）
  - [x] 用户管理页（Django Admin）
  - [ ] 数据报表入口（与Django Admin集成，可导出任务迁移至第六阶段）

- [x] **5.8 API集成** ✅
  - [x] 封装Axios请求
  - [x] 配置请求拦截器（自动添加token）
  - [x] 配置响应拦截器（统一错误处理）
  - [x] Pinia状态管理（用户认证状态）
  - [x] 工时管理API封装（timesheets.js）
  - [x] 通知系统API封装（notifications.js）
  - [x] 认证API扩展（头像上传 uploadAvatar 方法）

---

## 🔧 第六阶段：功能优化与安全加固

**优先级：🟡 中 | 预计时间：2-3天**  
**依赖：第四、五阶段基本完成**

### 任务列表

- [ ] **6.1 安全加固**
  - [ ] 配置CSRF保护
  - [x] 文件上传安全检查（文件类型、大小限制）✅（头像上传已实现类型和大小验证）
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

- 阶段一：✅ 100% (4/4) - **已完成** (2025-10-14)
- 阶段二：✅ 100% (6/6) - **已完成** (2025-10-15)
- 阶段三：✅ 100% (4/4) - **已完成** (2025-10-15)
- 阶段四：✅ 100% (21/21) - **已完成**
- 阶段五：✅ 100% (8/8) - **已完成** (2025-11-12)
- 阶段六：🟦 33% (1/3) - **进行中**
- 阶段七：⬜ 0% (0/4)
- 阶段八：⬜ 0% (0/7)
- 阶段九：⬜ 0% (0/2)

**总进度：45/58 任务完成 (77.6%)**

---

## 🎯 里程碑

- [x] **M1：环境搭建完成** ✅ (阶段一完成 - 2025-10-14)
- [x] **M2：数据模型完成** ✅ (阶段二完成 - 2025-10-15)
- [x] **M3：认证系统完成** ✅ (阶段三完成 - 2025-10-15)
- [x] **M4：后端API完成** ✅ (阶段四完成)
- [x] **M5：前端开发完成** ✅ (阶段五完成 - 2025-11-12)
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

**最后更新时间：** 2025-11-12
