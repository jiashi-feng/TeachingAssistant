# 学生助教管理平台 · 数据库文档

本文档描述项目所用数据库结构，便于部署、迁移与二次开发时查阅。实际表结构以各应用下 `migrations/` 及 `models.py` 为准。

---

## 1. 概述

- **开发/生产**：支持 MySQL 与 SQLite（通过环境变量 `USE_SQLITE` 切换，部署见 [部署文档](deployment.md)）。
- **ORM**：Django 模型，表名由 `Meta.db_table` 指定，默认小写+下划线。
- **迁移**：在 `backend` 目录执行 `python manage.py migrate` 应用迁移。

---

## 2. 表结构总览

### 2.1 用户与权限（accounts）

| 表名              | 说明                                                         |
| ----------------- | ------------------------------------------------------------ |
| `user`            | 用户主表（username、email、密码、is_staff、is_superuser 等） |
| `role`            | 角色（role_code：student / faculty / admin）                 |
| `permission`      | 权限（permission_code、模块）                                |
| `user_role`       | 用户-角色多对多（含 is_primary）                             |
| `role_permission` | 角色-权限多对多                                              |
| `student`         | 学生扩展（user_id、学号等）                                  |
| `faculty`         | 教师扩展（user_id、工号等）                                  |
| `administrator`   | 管理员扩展（user_id、admin_id、部门、岗位）                  |

### 2.2 业务模块

| 应用          | 表名           | 说明                                             |
| ------------- | -------------- | ------------------------------------------------ |
| recruitment   | `position`     | 招募岗位（课程、院系、时薪、状态等）             |
| application   | `application`  | 申请记录（岗位、申请人、状态、简历等）           |
| timesheet     | `timesheet`    | 工时表（月份、岗位、助教、工时、审批状态等）     |
| timesheet     | `salary`       | 薪酬记录（关联工时表、金额、支付方式、流水号等） |
| notifications | `notification` | 站内通知（接收人、类型、已读状态等）             |
| messaging     | `conversation` | 会话（师生聊天，参与人、关联岗位等）             |
| messaging     | `message`      | 消息（会话、发送人、内容、时间）                 |

### 2.3 Django 内置

- `auth_group` / `auth_permission` / `admin_log` 等由 Django 与 Admin 使用，迁移时会自动创建。

---

## 3. 关键关系

- **用户 → 角色**：`User` 与 `Role` 通过 `UserRole` 多对多；登录与权限判断依赖 `user_role` 与 `role_permission`。
- **岗位 → 申请 → 工时**：`Position` → `Application`（录用后）→ `Timesheet`（按岗位+助教+月份）；`Salary` 关联单条 `Timesheet`。
- **聊天**：`Conversation` 关联参与用户与可选岗位；`Message` 归属一条 `Conversation`。

---

## 4. 初始化与维护

- **初始化角色与权限**：`python manage.py init_basic_data`（在 `backend` 下执行）。
- **创建超级用户**：`python manage.py createsuperuser`。
- **备份**：MySQL 使用 `mysqldump`；SQLite 直接复制 `db.sqlite3` 文件。

更多实现细节见各应用下的 `models.py` 与 `backend/README.md`。**论文用表结构清单**（含每表字段、类型、约束与说明）见 [database-tables.md](database-tables.md)。
