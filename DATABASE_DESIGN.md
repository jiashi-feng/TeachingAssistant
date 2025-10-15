# 学生助教管理平台 - 数据库设计文档

> **版本**: v1.0  
> **创建日期**: 2025-10-15  
> **设计架构**: RBAC（基于角色的访问控制）

---

## 📋 目录

- [1. 设计概述](#1-设计概述)
- [2. 用户认证模块](#2-用户认证模块-accounts)
- [3. 招募管理模块](#3-招募管理模块-recruitment)
- [4. 申请流程模块](#4-申请流程模块-application)
- [5. 工时管理模块](#5-工时管理模块-timesheet)
- [6. 通知系统模块](#6-通知系统模块-notifications)
- [7. 数据库关系图](#7-数据库关系图)
- [8. 索引设计](#8-索引设计)
- [9. 数据字典](#9-数据字典)

---

## 1. 设计概述

### 1.1 设计原则

本系统采用**标准RBAC（基于角色的访问控制）架构**，具有以下特点：

- ✅ **多表分离设计**：核心用户表 + 角色扩展表（学生/教师/管理员）
- ✅ **灵活的权限系统**：角色表 + 权限表 + 关联表，支持动态权限分配
- ✅ **完善的审计追踪**：所有关键操作记录操作人和操作时间
- ✅ **统一用户标识**：使用 `user_id` 作为全局唯一标识
- ✅ **支持多角色**：用户可同时拥有多个角色（如：学生 + 助教）

### 1.2 命名规范

- **表名**：使用单数形式，PascalCase（如 `User`, `Position`）
- **字段名**：使用 snake_case（如 `user_id`, `created_at`）
- **主键**：统一使用 `表名_id` 或 `id`
- **外键**：使用关联表名（如 `user`, `position`）
- **时间字段**：创建时间 `created_at`，更新时间 `updated_at`

### 1.3 通用字段约定

所有表都包含以下通用字段（除非特殊说明）：

| 字段名       | 类型     | 说明     | 默认值               |
| ------------ | -------- | -------- | -------------------- |
| `created_at` | DateTime | 创建时间 | 当前时间             |
| `updated_at` | DateTime | 更新时间 | 当前时间（自动更新） |

---

## 2. 用户认证模块 (accounts)

### 2.1 User（核心用户表）

所有用户的基础信息，不区分角色。

| 字段名        | 类型         | 约束                 | 说明             | 举例                                                         |
| ------------- | ------------ | -------------------- | ---------------- | ------------------------------------------------------------ |
| `user_id`     | VARCHAR(20)  | PK, UNIQUE, NOT NULL | 统一用户ID       | S2021001234（学生）<br>F20210001（教师）<br>A00001（管理员） |
| `username`    | VARCHAR(150) | UNIQUE, NOT NULL     | 用户名（登录用） | zhangsan                                                     |
| `email`       | VARCHAR(254) | UNIQUE, NOT NULL     | 邮箱             | zhangsan@university.edu.cn                                   |
| `password`    | VARCHAR(128) | NOT NULL             | 密码（哈希加密） | pbkdf2_sha256$...                                            |
| `real_name`   | VARCHAR(50)  | NOT NULL             | 真实姓名         | 张三                                                         |
| `phone`       | VARCHAR(11)  | NULL                 | 手机号           | 13800138000                                                  |
| `avatar`      | VARCHAR(100) | NULL                 | 头像路径         | avatars/zhangsan.jpg                                         |
| `is_active`   | BOOLEAN      | NOT NULL             | 账号是否激活     | TRUE                                                         |
| `date_joined` | DateTime     | NOT NULL             | 注册时间         | 2025-10-15 10:30:00                                          |
| `last_login`  | DateTime     | NULL                 | 最后登录时间     | 2025-10-15 14:20:00                                          |
| `created_at`  | DateTime     | NOT NULL             | 创建时间         | 自动生成                                                     |
| `updated_at`  | DateTime     | NOT NULL             | 更新时间         | 自动更新                                                     |

**索引**：
- PRIMARY KEY (`user_id`)
- UNIQUE KEY (`username`)
- UNIQUE KEY (`email`)
- INDEX (`is_active`)

**说明**：
- `user_id` 格式规则：
  - 学生：`S` + 学号（如 S2021001234）
  - 教师：`F` + 工号（如 F20210001）
  - 管理员：`A` + 编号（如 A00001）
- 继承 Django 的 `AbstractBaseUser`，提供密码加密和认证功能

---

### 2.2 Role（角色表）

定义系统中的所有角色类型。

| 字段名        | 类型        | 约束               | 说明     | 举例                           |
| ------------- | ----------- | ------------------ | -------- | ------------------------------ |
| `role_id`     | INT         | PK, AUTO_INCREMENT | 角色ID   | 1                              |
| `role_code`   | VARCHAR(20) | UNIQUE, NOT NULL   | 角色代码 | student, faculty, admin        |
| `role_name`   | VARCHAR(50) | NOT NULL           | 角色名称 | 学生, 教师, 管理员             |
| `description` | TEXT        | NULL               | 角色描述 | 普通学生用户，可浏览和申请岗位 |
| `created_at`  | DateTime    | NOT NULL           | 创建时间 | 自动生成                       |

**索引**：
- PRIMARY KEY (`role_id`)
- UNIQUE KEY (`role_code`)

**预设数据**：
```sql
INSERT INTO Role (role_code, role_name, description) VALUES
('student', '学生', '普通学生用户，可浏览和申请岗位'),
('faculty', '教师', '教师用户，可发布岗位和审核申请'),
('admin', '管理员', '系统管理员，拥有最高权限');
```

---

### 2.3 Permission（权限表）

定义系统中的所有权限项。

| 字段名            | 类型         | 约束               | 说明     | 举例                     |
| ----------------- | ------------ | ------------------ | -------- | ------------------------ |
| `permission_id`   | INT          | PK, AUTO_INCREMENT | 权限ID   | 1                        |
| `permission_code` | VARCHAR(50)  | UNIQUE, NOT NULL   | 权限代码 | view_position            |
| `permission_name` | VARCHAR(100) | NOT NULL           | 权限名称 | 浏览岗位                 |
| `module`          | VARCHAR(50)  | NOT NULL           | 所属模块 | recruitment              |
| `description`     | TEXT         | NULL               | 权限描述 | 允许用户浏览所有开放岗位 |
| `created_at`      | DateTime     | NOT NULL           | 创建时间 | 自动生成                 |

**索引**：
- PRIMARY KEY (`permission_id`)
- UNIQUE KEY (`permission_code`)
- INDEX (`module`)

**权限分类**：

| 模块         | 权限代码                 | 权限名称       | 说明                    |
| ------------ | ------------------------ | -------------- | ----------------------- |
| **用户管理** | `manage_user`            | 管理用户       | 增删改查用户            |
|              | `manage_role`            | 管理角色       | 分配和撤销角色          |
| **岗位管理** | `view_position`          | 浏览岗位       | 查看开放岗位            |
|              | `create_position`        | 创建岗位       | 发布新岗位              |
|              | `manage_own_position`    | 管理自己的岗位 | 编辑/关闭自己发布的岗位 |
|              | `manage_all_position`    | 管理所有岗位   | 管理员权限              |
| **申请管理** | `apply_position`         | 申请岗位       | 提交岗位申请            |
|              | `view_own_application`   | 查看自己的申请 | 查看申请状态            |
|              | `review_application`     | 审核申请       | 审核学生申请            |
| **工时管理** | `submit_timesheet`       | 提交工时       | 提交工时表              |
|              | `view_own_timesheet`     | 查看自己的工时 | 查看工时记录            |
|              | `review_timesheet`       | 审核工时       | 审核助教工时            |
| **薪酬管理** | `view_own_salary`        | 查看自己的薪酬 | 查看薪酬记录            |
|              | `generate_salary_report` | 生成薪酬报表   | 管理员生成月度报表      |
|              | `manage_payment`         | 管理支付       | 标记支付状态            |
| **数据统计** | `view_own_dashboard`     | 查看个人看板   | 查看个人数据统计        |
|              | `view_all_dashboard`     | 查看全局看板   | 查看全平台数据          |
|              | `export_report`          | 导出报表       | 导出Excel报表           |

---

### 2.4 UserRole（用户角色关联表）

支持一个用户拥有多个角色。

| 字段名        | 类型        | 约束               | 说明         | 举例                |
| ------------- | ----------- | ------------------ | ------------ | ------------------- |
| `id`          | INT         | PK, AUTO_INCREMENT | 主键         | 1                   |
| `user_id`     | VARCHAR(20) | FK, NOT NULL       | 用户ID       | S2021001234         |
| `role_id`     | INT         | FK, NOT NULL       | 角色ID       | 1                   |
| `is_primary`  | BOOLEAN     | NOT NULL           | 是否为主角色 | TRUE                |
| `assigned_at` | DateTime    | NOT NULL           | 分配时间     | 2025-10-15 10:00:00 |
| `assigned_by` | VARCHAR(20) | FK, NULL           | 分配人       | A00001（管理员）    |
| `created_at`  | DateTime    | NOT NULL           | 创建时间     | 自动生成            |

**索引**：
- PRIMARY KEY (`id`)
- UNIQUE KEY (`user_id`, `role_id`)
- INDEX (`user_id`)
- INDEX (`role_id`)

**外键约束**：
- FOREIGN KEY (`user_id`) REFERENCES `User`(`user_id`) ON DELETE CASCADE
- FOREIGN KEY (`role_id`) REFERENCES `Role`(`role_id`) ON DELETE CASCADE
- FOREIGN KEY (`assigned_by`) REFERENCES `User`(`user_id`) ON DELETE SET NULL

**业务规则**：
- 每个用户必须有且只有一个主角色（`is_primary=TRUE`）
- 学生申请通过后，自动添加助教角色（`role_code='ta'`，需先创建TA角色）

---

### 2.5 RolePermission（角色权限关联表）

定义每个角色拥有的权限。

| 字段名          | 类型     | 约束               | 说明     | 举例                |
| --------------- | -------- | ------------------ | -------- | ------------------- |
| `id`            | INT      | PK, AUTO_INCREMENT | 主键     | 1                   |
| `role_id`       | INT      | FK, NOT NULL       | 角色ID   | 1                   |
| `permission_id` | INT      | FK, NOT NULL       | 权限ID   | 1                   |
| `granted_at`    | DateTime | NOT NULL           | 授权时间 | 2025-10-15 10:00:00 |
| `created_at`    | DateTime | NOT NULL           | 创建时间 | 自动生成            |

**索引**：
- PRIMARY KEY (`id`)
- UNIQUE KEY (`role_id`, `permission_id`)
- INDEX (`role_id`)
- INDEX (`permission_id`)

**外键约束**：
- FOREIGN KEY (`role_id`) REFERENCES `Role`(`role_id`) ON DELETE CASCADE
- FOREIGN KEY (`permission_id`) REFERENCES `Permission`(`permission_id`) ON DELETE CASCADE

---

### 2.6 Student（学生信息表）

存储学生特有的信息。

| 字段名       | 类型         | 约束                 | 说明         | 举例                 |
| ------------ | ------------ | -------------------- | ------------ | -------------------- |
| `id`         | INT          | PK, AUTO_INCREMENT   | 主键         | 1                    |
| `user_id`    | VARCHAR(20)  | FK, UNIQUE, NOT NULL | 关联用户     | S2021001234          |
| `student_id` | VARCHAR(20)  | UNIQUE, NOT NULL     | 学号         | 2021001234           |
| `department` | VARCHAR(100) | NOT NULL             | 院系         | 计算机科学与技术学院 |
| `major`      | VARCHAR(100) | NOT NULL             | 专业         | 软件工程             |
| `grade`      | INT          | NOT NULL             | 年级         | 2021                 |
| `class_name` | VARCHAR(50)  | NULL                 | 班级         | 软件2101             |
| `is_ta`      | BOOLEAN      | NOT NULL             | 是否为助教   | FALSE（默认）        |
| `ta_since`   | DATE         | NULL                 | 成为助教时间 | 2025-03-01           |
| `created_at` | DateTime     | NOT NULL             | 创建时间     | 自动生成             |
| `updated_at` | DateTime     | NOT NULL             | 更新时间     | 自动更新             |

**索引**：
- PRIMARY KEY (`id`)
- UNIQUE KEY (`user_id`)
- UNIQUE KEY (`student_id`)
- INDEX (`department`)
- INDEX (`is_ta`)

**外键约束**：
- FOREIGN KEY (`user_id`) REFERENCES `User`(`user_id`) ON DELETE CASCADE

**业务规则**：
- 当学生申请通过后，`is_ta` 自动设为 `TRUE`，`ta_since` 设为当前日期

---

### 2.7 Faculty（教师信息表）

存储教师特有的信息。

| 字段名            | 类型         | 约束                 | 说明     | 举例                 |
| ----------------- | ------------ | -------------------- | -------- | -------------------- |
| `id`              | INT          | PK, AUTO_INCREMENT   | 主键     | 1                    |
| `user_id`         | VARCHAR(20)  | FK, UNIQUE, NOT NULL | 关联用户 | F20210001            |
| `faculty_id`      | VARCHAR(20)  | UNIQUE, NOT NULL     | 工号     | 20210001             |
| `department`      | VARCHAR(100) | NOT NULL             | 院系     | 计算机科学与技术学院 |
| `title`           | VARCHAR(50)  | NOT NULL             | 职称     | 副教授               |
| `office_location` | VARCHAR(100) | NULL                 | 办公室   | 科技楼A508           |
| `research_area`   | TEXT         | NULL                 | 研究方向 | 数据库系统、云计算   |
| `created_at`      | DateTime     | NOT NULL             | 创建时间 | 自动生成             |
| `updated_at`      | DateTime     | NOT NULL             | 更新时间 | 自动更新             |

**索引**：
- PRIMARY KEY (`id`)
- UNIQUE KEY (`user_id`)
- UNIQUE KEY (`faculty_id`)
- INDEX (`department`)

**外键约束**：
- FOREIGN KEY (`user_id`) REFERENCES `User`(`user_id`) ON DELETE CASCADE

---

### 2.8 Administrator（管理员信息表）

存储管理员特有的信息。

| 字段名       | 类型         | 约束                 | 说明       | 举例       |
| ------------ | ------------ | -------------------- | ---------- | ---------- |
| `id`         | INT          | PK, AUTO_INCREMENT   | 主键       | 1          |
| `user_id`    | VARCHAR(20)  | FK, UNIQUE, NOT NULL | 关联用户   | A00001     |
| `admin_id`   | VARCHAR(20)  | UNIQUE, NOT NULL     | 管理员编号 | A00001     |
| `department` | VARCHAR(100) | NOT NULL             | 部门       | 教务处     |
| `position`   | VARCHAR(50)  | NOT NULL             | 职位       | 系统管理员 |
| `created_at` | DateTime     | NOT NULL             | 创建时间   | 自动生成   |
| `updated_at` | DateTime     | NOT NULL             | 更新时间   | 自动更新   |

**索引**：
- PRIMARY KEY (`id`)
- UNIQUE KEY (`user_id`)
- UNIQUE KEY (`admin_id`)
- INDEX (`department`)

**外键约束**：
- FOREIGN KEY (`user_id`) REFERENCES `User`(`user_id`) ON DELETE CASCADE

**说明**：
- 管理员拥有系统最高权限，无需设置级别区分

---

## 3. 招募管理模块 (recruitment)

### 3.1 Position（岗位表）

存储教师发布的助教岗位信息。

| 字段名                 | 类型          | 约束               | 说明            | 举例                  |
| ---------------------- | ------------- | ------------------ | --------------- | --------------------- |
| `position_id`          | INT           | PK, AUTO_INCREMENT | 岗位ID          | 1                     |
| `title`                | VARCHAR(200)  | NOT NULL           | 岗位标题        | 数据结构课程助教      |
| `course_name`          | VARCHAR(100)  | NOT NULL           | 课程名称        | 数据结构与算法        |
| `course_code`          | VARCHAR(20)   | NOT NULL           | 课程代码        | CS101                 |
| `description`          | TEXT          | NOT NULL           | 岗位描述        | 协助批改作业、答疑... |
| `requirements`         | TEXT          | NOT NULL           | 任职要求        | 熟悉Python，绩点3.5+  |
| `num_positions`        | INT           | NOT NULL           | 招聘人数        | 2                     |
| `num_filled`           | INT           | NOT NULL           | 已录用人数      | 0（默认）             |
| `work_hours_per_week`  | INT           | NOT NULL           | 每周工时        | 10                    |
| `hourly_rate`          | DECIMAL(10,2) | NOT NULL           | 时薪（元/小时） | 50.00                 |
| `start_date`           | DATE          | NOT NULL           | 开始日期        | 2025-03-01            |
| `end_date`             | DATE          | NOT NULL           | 结束日期        | 2025-06-30            |
| `application_deadline` | DateTime      | NOT NULL           | 申请截止时间    | 2025-02-20 23:59:59   |
| `status`               | VARCHAR(20)   | NOT NULL           | 岗位状态        | open, closed, filled  |
| `posted_by`            | VARCHAR(20)   | FK, NOT NULL       | 发布教师        | F20210001             |
| `created_at`           | DateTime      | NOT NULL           | 创建时间        | 自动生成              |
| `updated_at`           | DateTime      | NOT NULL           | 更新时间        | 自动更新              |

**索引**：
- PRIMARY KEY (`position_id`)
- INDEX (`status`)
- INDEX (`posted_by`)
- INDEX (`course_code`)
- INDEX (`application_deadline`)

**外键约束**：
- FOREIGN KEY (`posted_by`) REFERENCES `User`(`user_id`) ON DELETE PROTECT

**状态枚举**：
```python
STATUS_CHOICES = [
    ('open', '开放中'),
    ('closed', '已关闭'),
    ('filled', '已招满'),
]
```

**业务规则**：
- 当 `num_filled` 达到 `num_positions` 时，状态自动变为 `filled`
- 当超过 `application_deadline` 时，状态自动变为 `closed`
- 时薪必须 > 0
- 结束日期必须 > 开始日期

---

## 4. 申请流程模块 (application)

### 4.1 Application（申请表）

记录学生申请岗位的过程。

| 字段名           | 类型         | 约束               | 说明         | 举例                                     |
| ---------------- | ------------ | ------------------ | ------------ | ---------------------------------------- |
| `application_id` | INT          | PK, AUTO_INCREMENT | 申请ID       | 1                                        |
| `position_id`    | INT          | FK, NOT NULL       | 申请的岗位   | 1                                        |
| `applicant_id`   | VARCHAR(20)  | FK, NOT NULL       | 申请人       | S2021001234                              |
| `status`         | VARCHAR(20)  | NOT NULL           | 申请状态     | submitted, reviewing, accepted, rejected |
| `resume`         | VARCHAR(100) | NOT NULL           | 简历文件路径 | resumes/2025/10/张三_简历.pdf            |
| `applied_at`     | DateTime     | NOT NULL           | 申请时间     | 2025-10-15 14:30:00                      |
| `reviewed_at`    | DateTime     | NULL               | 审核时间     | 2025-10-16 10:20:00                      |
| `reviewed_by`    | VARCHAR(20)  | FK, NULL           | 审核人       | F20210001                                |
| `review_notes`   | TEXT         | NULL               | 审核备注     | 专业能力强，同意录用                     |
| `created_at`     | DateTime     | NOT NULL           | 创建时间     | 自动生成                                 |
| `updated_at`     | DateTime     | NOT NULL           | 更新时间     | 自动更新                                 |

**索引**：
- PRIMARY KEY (`application_id`)
- UNIQUE KEY (`position_id`, `applicant_id`)
- INDEX (`applicant_id`)
- INDEX (`status`)
- INDEX (`applied_at`)

**外键约束**：
- FOREIGN KEY (`position_id`) REFERENCES `Position`(`position_id`) ON DELETE CASCADE
- FOREIGN KEY (`applicant_id`) REFERENCES `User`(`user_id`) ON DELETE CASCADE
- FOREIGN KEY (`reviewed_by`) REFERENCES `User`(`user_id`) ON DELETE SET NULL

**状态枚举**：
```python
STATUS_CHOICES = [
    ('submitted', '已提交'),
    ('reviewing', '审核中'),
    ('accepted', '已录用'),
    ('rejected', '已拒绝'),
]
```

**业务规则**：
- 唯一约束：同一个学生不能重复申请同一个岗位
- 申请状态变为 `accepted` 时，自动更新 `Student.is_ta=TRUE`
- 申请状态变为 `accepted` 时，对应岗位的 `num_filled` 加1

---

## 5. 工时管理模块 (timesheet)

### 5.1 Timesheet（工时表）

记录助教的工作时间。

| 字段名             | 类型         | 约束               | 说明                 | 举例                        |
| ------------------ | ------------ | ------------------ | -------------------- | --------------------------- |
| `timesheet_id`     | INT          | PK, AUTO_INCREMENT | 工时表ID             | 1                           |
| `ta_id`            | VARCHAR(20)  | FK, NOT NULL       | 助教                 | S2021001234                 |
| `position_id`      | INT          | FK, NOT NULL       | 岗位                 | 1                           |
| `month`            | DATE         | NOT NULL           | 工作月份（月初日期） | 2025-03-01                  |
| `hours_worked`     | DECIMAL(5,2) | NOT NULL           | 工作小时数           | 40.5                        |
| `work_description` | TEXT         | NOT NULL           | 工作描述             | 批改作业30份，答疑5次...    |
| `status`           | VARCHAR(20)  | NOT NULL           | 审核状态             | pending, approved, rejected |
| `submitted_at`     | DateTime     | NOT NULL           | 提交时间             | 2025-03-25 18:00:00         |
| `reviewed_by`      | VARCHAR(20)  | FK, NULL           | 审核教师             | F20210001                   |
| `reviewed_at`      | DateTime     | NULL               | 审核时间             | 2025-03-26 10:00:00         |
| `review_notes`     | TEXT         | NULL               | 审核备注             | 工作认真，同意              |
| `created_at`       | DateTime     | NOT NULL           | 创建时间             | 自动生成                    |
| `updated_at`       | DateTime     | NOT NULL           | 更新时间             | 自动更新                    |

**索引**：
- PRIMARY KEY (`timesheet_id`)
- UNIQUE KEY (`ta_id`, `position_id`, `month`)
- INDEX (`ta_id`)
- INDEX (`position_id`)
- INDEX (`status`)
- INDEX (`month`)

**外键约束**：
- FOREIGN KEY (`ta_id`) REFERENCES `User`(`user_id`) ON DELETE CASCADE
- FOREIGN KEY (`position_id`) REFERENCES `Position`(`position_id`) ON DELETE CASCADE
- FOREIGN KEY (`reviewed_by`) REFERENCES `User`(`user_id`) ON DELETE SET NULL

**状态枚举**：
```python
STATUS_CHOICES = [
    ('pending', '待审核'),
    ('approved', '已批准'),
    ('rejected', '已驳回'),
]
```

**业务规则**：
- 唯一约束：同一助教同一岗位同一月份只能提交一次工时表
- 工作小时数必须在 0 到 744 之间（一个月最多31天×24小时）
- 工时表审核通过后，自动生成对应的薪酬记录

---

### 5.2 Salary（薪酬记录表）

记录助教的薪酬信息，由管理员根据已批准的工时生成。

| 字段名                | 类型          | 约束                 | 说明                 | 举例                                           |
| --------------------- | ------------- | -------------------- | -------------------- | ---------------------------------------------- |
| `salary_id`           | INT           | PK, AUTO_INCREMENT   | 薪酬ID               | 1                                              |
| `timesheet_id`        | INT           | FK, UNIQUE, NOT NULL | 关联工时表           | 1                                              |
| `amount`              | DECIMAL(10,2) | NOT NULL             | 薪酬金额（元）       | 2025.00                                        |
| `calculation_details` | JSON          | NULL                 | 计算明细             | {"hours":40.5, "rate":50, "formula":"40.5×50"} |
| `payment_status`      | VARCHAR(20)   | NOT NULL             | 支付状态             | pending, paid                                  |
| `generated_by`        | VARCHAR(20)   | FK, NOT NULL         | 报表生成人（管理员） | A00001                                         |
| `generated_at`        | DateTime      | NOT NULL             | 报表生成时间         | 2025-03-28 09:00:00                            |
| `paid_at`             | DateTime      | NULL                 | 支付时间             | 2025-04-01 14:30:00                            |
| `payment_method`      | VARCHAR(50)   | NULL                 | 支付方式             | 银行转账, 支付宝                               |
| `transaction_id`      | VARCHAR(100)  | NULL                 | 交易流水号           | TX20250401001                                  |
| `created_at`          | DateTime      | NOT NULL             | 创建时间             | 自动生成                                       |
| `updated_at`          | DateTime      | NOT NULL             | 更新时间             | 自动更新                                       |

**索引**：
- PRIMARY KEY (`salary_id`)
- UNIQUE KEY (`timesheet_id`)
- INDEX (`payment_status`)
- INDEX (`generated_by`)
- INDEX (`generated_at`)

**外键约束**：
- FOREIGN KEY (`timesheet_id`) REFERENCES `Timesheet`(`timesheet_id`) ON DELETE CASCADE
- FOREIGN KEY (`generated_by`) REFERENCES `User`(`user_id`) ON DELETE PROTECT

**状态枚举**：
```python
STATUS_CHOICES = [
    ('pending', '待支付'),
    ('paid', '已支付'),
]
```

**业务规则**：
- 一个工时表对应一条薪酬记录（一对一关系）
- 薪酬金额 = 工作小时数 × 岗位时薪
- 只有管理员可以生成薪酬报表
- `calculation_details` 以JSON格式存储计算过程，便于审计

---

## 6. 通知系统模块 (notifications)

### 6.1 Notification（通知表）

系统消息和通知记录。

| 字段名              | 类型         | 约束               | 说明                     | 举例                                   |
| ------------------- | ------------ | ------------------ | ------------------------ | -------------------------------------- |
| `notification_id`   | INT          | PK, AUTO_INCREMENT | 通知ID                   | 1                                      |
| `recipient_id`      | VARCHAR(20)  | FK, NOT NULL       | 接收人                   | S2021001234                            |
| `sender_id`         | VARCHAR(20)  | FK, NULL           | 发送人（系统通知为NULL） | F20210001                              |
| `notification_type` | VARCHAR(50)  | NOT NULL           | 通知类型                 | application_accepted                   |
| `category`          | VARCHAR(20)  | NOT NULL           | 通知分类                 | system, application, timesheet, salary |
| `title`             | VARCHAR(200) | NOT NULL           | 标题                     | 申请审核结果通知                       |
| `message`           | TEXT         | NOT NULL           | 消息内容                 | 您申请的数据结构助教岗位已通过审核     |
| `priority`          | VARCHAR(10)  | NOT NULL           | 优先级                   | low, medium, high, urgent              |
| `is_read`           | BOOLEAN      | NOT NULL           | 是否已读                 | FALSE（默认）                          |
| `read_at`           | DateTime     | NULL               | 阅读时间                 | 2025-10-15 16:00:00                    |
| `related_model`     | VARCHAR(50)  | NULL               | 关联模型                 | Application, Timesheet                 |
| `related_object_id` | INT          | NULL               | 关联对象ID               | 123                                    |
| `expires_at`        | DateTime     | NULL               | 过期时间                 | NULL（重要通知不过期）                 |
| `created_at`        | DateTime     | NOT NULL           | 创建时间                 | 自动生成                               |

**索引**：
- PRIMARY KEY (`notification_id`)
- INDEX (`recipient_id`, `is_read`)
- INDEX (`notification_type`)
- INDEX (`category`)
- INDEX (`created_at`)

**外键约束**：
- FOREIGN KEY (`recipient_id`) REFERENCES `User`(`user_id`) ON DELETE CASCADE
- FOREIGN KEY (`sender_id`) REFERENCES `User`(`user_id`) ON DELETE SET NULL

**分类枚举**：
```python
CATEGORY_CHOICES = [
    ('system', '系统通知'),
    ('application', '申请相关'),
    ('timesheet', '工时相关'),
    ('salary', '薪酬相关'),
]
```

**优先级枚举**：
```python
PRIORITY_CHOICES = [
    ('low', '低'),
    ('medium', '中'),
    ('high', '高'),
    ('urgent', '紧急'),
]
```

---

### 6.2 通知类型详细说明

| 分类         | 类型代码                 | 类型名称     | 触发场景         | 接收人               | 优先级 |
| ------------ | ------------------------ | ------------ | ---------------- | -------------------- | ------ |
| **系统通知** | `system_announcement`    | 系统公告     | 管理员发布公告   | 所有用户             | medium |
|              | `system_maintenance`     | 系统维护通知 | 系统维护前       | 所有用户             | high   |
|              | `account_activated`      | 账号激活     | 用户注册成功     | 新用户               | low    |
|              | `password_changed`       | 密码修改     | 用户修改密码     | 当前用户             | medium |
| **岗位相关** | `position_published`     | 新岗位发布   | 教师发布新岗位   | 所有学生             | low    |
|              | `position_updated`       | 岗位信息更新 | 教师修改岗位     | 已申请的学生         | medium |
|              | `position_closed`        | 岗位关闭     | 教师关闭岗位     | 已申请的学生         | medium |
|              | `position_deadline_soon` | 申请截止提醒 | 截止前24小时     | 浏览过但未申请的学生 | high   |
| **申请相关** | `application_submitted`  | 收到新申请   | 学生提交申请     | 岗位发布教师         | medium |
|              | `application_reviewing`  | 申请审核中   | 教师开始审核     | 申请人               | low    |
|              | `application_accepted`   | 申请通过     | 教师接受申请     | 申请人               | high   |
|              | `application_rejected`   | 申请被拒     | 教师拒绝申请     | 申请人               | medium |
|              | `application_withdrawn`  | 申请已撤回   | 学生撤回申请     | 岗位发布教师         | low    |
| **工时相关** | `timesheet_submitted`    | 收到工时表   | 助教提交工时     | 岗位教师             | medium |
|              | `timesheet_approved`     | 工时已批准   | 教师批准工时     | 助教                 | medium |
|              | `timesheet_rejected`     | 工时被驳回   | 教师驳回工时     | 助教                 | high   |
|              | `timesheet_reminder`     | 工时提交提醒 | 每月25日         | 所有助教             | high   |
| **薪酬相关** | `salary_generated`       | 薪酬已生成   | 管理员生成报表   | 助教                 | medium |
|              | `salary_paid`            | 薪酬已发放   | 财务支付完成     | 助教                 | high   |
|              | `salary_delayed`         | 薪酬延迟通知 | 超过预计支付日期 | 助教                 | urgent |
| **角色相关** | `role_granted`           | 角色授予     | 管理员分配角色   | 用户                 | medium |
|              | `role_revoked`           | 角色撤销     | 管理员撤销角色   | 用户                 | high   |
|              | `became_ta`              | 成为助教     | 申请通过后       | 学生                 | high   |
| **评价相关** | `evaluation_received`    | 收到工作评价 | 教师评价助教     | 助教                 | low    |
|              | `evaluation_reminder`    | 评价提醒     | 学期结束前       | 教师                 | medium |

---

## 7. 数据库关系图

### 7.1 实体关系总览

```
┌─────────────────────────────────────────────────────────────────┐
│                        用户认证模块                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  User (核心用户表)                                               │
│    │                                                            │
│    ├──┬──→ UserRole ←→ Role ←→ RolePermission ←→ Permission    │
│    │  │                                                         │
│    │  ├──→ Student (一对一)                                     │
│    │  ├──→ Faculty (一对一)                                     │
│    │  └──→ Administrator (一对一)                               │
│    │                                                            │
└────┼────────────────────────────────────────────────────────────┘
     │
┌────┼────────────────────────────────────────────────────────────┐
│    │                   业务功能模块                              │
├────┼────────────────────────────────────────────────────────────┤
│    │                                                            │
│    ├──→ Position (岗位)                                         │
│    │      │                                                     │
│    │      └──→ Application (申请)                               │
│    │             │                                              │
│    │             └──→ applicant: User(Student)                 │
│    │             └──→ reviewed_by: User(Faculty)               │
│    │                                                            │
│    ├──→ Timesheet (工时表)                                      │
│    │      │                                                     │
│    │      ├──→ ta: User(Student, is_ta=True)                   │
│    │      ├──→ position: Position                              │
│    │      ├──→ reviewed_by: User(Faculty)                      │
│    │      │                                                     │
│    │      └──→ Salary (薪酬，一对一)                            │
│    │             │                                              │
│    │             └──→ generated_by: User(Administrator)        │
│    │                                                            │
│    └──→ Notification (通知)                                     │
│           │                                                     │
│           ├──→ recipient: User                                 │
│           └──→ sender: User (可选)                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2 关系类型说明

| 关系                                 | 类型   | 说明                       |
| ------------------------------------ | ------ | -------------------------- |
| User → Student/Faculty/Administrator | 一对一 | 根据 user_id 前缀区分      |
| User → UserRole                      | 一对多 | 一个用户可以有多个角色     |
| Role → Permission                    | 多对多 | 通过 RolePermission 关联   |
| Faculty → Position                   | 一对多 | 一个教师可以发布多个岗位   |
| Position → Application               | 一对多 | 一个岗位可以有多个申请     |
| Student → Application                | 一对多 | 一个学生可以申请多个岗位   |
| Student → Timesheet                  | 一对多 | 一个助教可以提交多个工时表 |
| Timesheet → Salary                   | 一对一 | 一个工时表对应一条薪酬记录 |
| User → Notification                  | 一对多 | 一个用户可以收到多条通知   |

---

## 8. 索引设计

### 8.1 索引策略

为提高查询性能，为以下场景建立索引：

#### 高频查询字段
- 用户认证：`User.username`, `User.email`
- 角色权限：`UserRole.user_id`, `RolePermission.role_id`
- 岗位浏览：`Position.status`, `Position.application_deadline`
- 申请管理：`Application.applicant_id`, `Application.status`
- 工时管理：`Timesheet.ta_id`, `Timesheet.month`, `Timesheet.status`

#### 外键字段
所有外键字段都建立索引，加速JOIN操作。

#### 复合索引
- `Application(position_id, applicant_id)`：唯一性约束 + 快速查询
- `Timesheet(ta_id, position_id, month)`：唯一性约束 + 快速查询
- `Notification(recipient_id, is_read)`：未读消息查询

---

## 9. 数据字典

### 9.1 表清单

| 序号 | 表名           | 中文名         | 模块          | 说明           |
| ---- | -------------- | -------------- | ------------- | -------------- |
| 1    | User           | 用户表         | accounts      | 核心用户信息   |
| 2    | Role           | 角色表         | accounts      | 角色定义       |
| 3    | Permission     | 权限表         | accounts      | 权限定义       |
| 4    | UserRole       | 用户角色关联表 | accounts      | 多对多关系     |
| 5    | RolePermission | 角色权限关联表 | accounts      | 多对多关系     |
| 6    | Student        | 学生信息表     | accounts      | 学生扩展信息   |
| 7    | Faculty        | 教师信息表     | accounts      | 教师扩展信息   |
| 8    | Administrator  | 管理员信息表   | accounts      | 管理员扩展信息 |
| 9    | Position       | 岗位表         | recruitment   | 助教岗位       |
| 10   | Application    | 申请表         | application   | 岗位申请       |
| 11   | Timesheet      | 工时表         | timesheet     | 工时记录       |
| 12   | Salary         | 薪酬表         | timesheet     | 薪酬记录       |
| 13   | Notification   | 通知表         | notifications | 系统通知       |

### 9.2 表统计信息

| 表名           | 预计记录数 | 增长速度 | 备注                             |
| -------------- | ---------- | -------- | -------------------------------- |
| User           | 10,000     | 慢       | 每年增加约1000名用户             |
| Role           | 10         | 极慢     | 基本固定                         |
| Permission     | 50         | 慢       | 随功能扩展缓慢增加               |
| UserRole       | 12,000     | 慢       | 略多于用户数（一些用户有多角色） |
| RolePermission | 100        | 慢       | 角色×权限数量                    |
| Student        | 8,000      | 慢       | 学生用户数                       |
| Faculty        | 500        | 极慢     | 教师用户数                       |
| Administrator  | 10         | 极慢     | 管理员数量                       |
| Position       | 500/学期   | 快       | 每学期500个岗位                  |
| Application    | 5,000/学期 | 快       | 平均每个岗位10个申请             |
| Timesheet      | 2,000/月   | 快       | 每月约2000个助教提交工时         |
| Salary         | 2,000/月   | 快       | 与工时表一致                     |
| Notification   | 50,000/年  | 非常快   | 最活跃的表                       |

---

## 10. 附录

### 10.1 数据类型说明

| Django类型        | MySQL类型    | 说明           |
| ----------------- | ------------ | -------------- |
| CharField(n)      | VARCHAR(n)   | 可变长度字符串 |
| TextField         | TEXT         | 长文本         |
| IntegerField      | INT          | 整数           |
| DecimalField(m,n) | DECIMAL(m,n) | 定点小数       |
| BooleanField      | TINYINT(1)   | 布尔值         |
| DateField         | DATE         | 日期           |
| DateTimeField     | DATETIME     | 日期时间       |
| ImageField        | VARCHAR(100) | 图片路径       |
| FileField         | VARCHAR(100) | 文件路径       |
| JSONField         | JSON         | JSON数据       |

### 10.2 删除策略说明

| 策略        | 说明       | 使用场景                 |
| ----------- | ---------- | ------------------------ |
| CASCADE     | 级联删除   | 删除用户时删除其所有数据 |
| PROTECT     | 保护模式   | 有关联数据时禁止删除     |
| SET NULL    | 设为NULL   | 删除后保留记录但清空关联 |
| SET DEFAULT | 设为默认值 | 删除后设为预设值         |

### 10.3 设计变更记录

| 版本 | 日期       | 变更内容               | 变更人 |
| ---- | ---------- | ---------------------- | ------ |
| v1.0 | 2025-10-15 | 初始版本，采用RBAC架构 | -      |

---

## 📝 备注

1. **字符集**：所有表使用 `utf8mb4` 字符集，支持中文和emoji
2. **时区**：所有时间字段使用服务器时区（Asia/Shanghai）
3. **事务**：使用 InnoDB 引擎，支持事务和外键
4. **备份策略**：建议每日全量备份，每小时增量备份
5. **性能优化**：定期清理过期通知，建议保留近6个月数据

---

**文档维护者**：开发团队  
**最后更新**：2025-10-15  
**审核状态**：待审核

---

