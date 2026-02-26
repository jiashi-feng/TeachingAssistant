## 学生助教管理平台 · 后端 API 文档（权威版本）

> 说明：本文件是后端接口的**唯一权威定义**，其他 README 中仅保留概览与链接。
>
> - 基础 URL：`http://localhost:8000`
> - 所有业务接口前缀：`/api/...`
> - 统一返回格式约定：
>   - 成功：`{"code": 200, "data": {...}, "message": "success"}` 或等价结构
>   - 失败：`{"code": 4xx/5xx, "message": "错误提示", "errors": {...}}`

---

## 1. 认证与用户模块 `/api/auth/`

### 1.1 获取 JWT Token

- **URL**：`POST /api/auth/token/`
- **说明**：使用用户名+密码获取访问/刷新 Token（SimpleJWT 标准接口）。

#### 请求体

```json
{
  "username": "student1",
  "password": "password123"
}
```

#### 响应体（示例）

```json
{
  "access": "ACCESS_TOKEN",
  "refresh": "REFRESH_TOKEN"
}
```

---

### 1.2 刷新 Token

- **URL**：`POST /api/auth/token/refresh/`
- **说明**：使用 `refresh` 获取新的 `access`。

#### 请求体

```json
{
  "refresh": "REFRESH_TOKEN"
}
```

#### 响应体（示例）

```json
{
  "access": "NEW_ACCESS_TOKEN"
}
```

---

### 1.3 用户注册

- **URL**：`POST /api/auth/register/`
- **权限**：允许匿名
- **说明**：注册学生 / 教师 / 管理员账号（根据传入角色）。

#### 请求体（示例）

```json
{
  "username": "student1",
  "password": "password123",
  "email": "s1@example.com",
  "role": "student"
}
```

#### 响应体（示例）

```json
{
  "message": "注册成功",
  "user": {
    "user_id": "U0001",
    "username": "student1",
    "email": "s1@example.com",
    "roles": ["student"]
  },
  "tokens": {
    "access": "ACCESS_TOKEN",
    "refresh": "REFRESH_TOKEN"
  }
}
```

---

### 1.4 用户登录

- **URL**：`POST /api/auth/login/`
- **权限**：允许匿名
- **说明**：使用用户名+密码登录，返回用户信息和 JWT。

#### 请求体

```json
{
  "username": "student1",
  "password": "password123"
}
```

#### 响应体（示例）

```json
{
  "message": "登录成功",
  "user": {
    "user_id": "U0001",
    "username": "student1",
    "real_name": "学生一",
    "roles": ["student"],
    "permissions": ["view_position", "apply_position"]
  },
  "tokens": {
    "access": "ACCESS_TOKEN",
    "refresh": "REFRESH_TOKEN"
  }
}
```

---

### 1.5 用户登出

- **URL**：`POST /api/auth/logout/`
- **权限**：登录用户
- **说明**：将 `refresh_token` 加入黑名单（SimpleJWT Blacklist）。

#### 请求体

```json
{
  "refresh_token": "REFRESH_TOKEN"
}
```

#### 响应体

```json
{
  "message": "登出成功"
}
```

---

### 1.6 获取当前用户信息

- **URL**：`GET /api/auth/profile/`
- **权限**：登录用户

#### 响应体（示例）

```json
{
  "message": "获取用户信息成功",
  "user": {
    "user_id": "U0001",
    "username": "student1",
    "real_name": "学生一",
    "email": "s1@example.com",
    "roles": ["student"],
    "permissions": ["view_position", "apply_position"]
  }
}
```

---

### 1.7 更新当前用户信息

- **URL**：`PUT /api/auth/profile/`
- **权限**：登录用户
- **说明**：支持更新姓名、手机、邮箱、头像等。

#### 请求体（示例，JSON 或 multipart）

```json
{
  "real_name": "新名字",
  "phone": "13800000000",
  "email": "new@example.com"
}
```

---

### 1.8 修改密码

- **URL**：`PUT /api/auth/change-password/`
- **权限**：登录用户

---

### 1.9 用户列表与详情（管理员）

- **URL**：
  - `GET /api/auth/users/` 用户列表（分页、筛选）
  - `GET /api/auth/users/{user_id}/` 用户详情
- **权限**：管理员 / 具备相应权限的 staff

---

### 1.10 辅助检查接口

- `GET /api/auth/check-username/?username=...`
- `GET /api/auth/check-email/?email=...`
- `GET /api/auth/check-user-id/?user_id=...`

用于前端注册/编辑时的唯一性检查。

---

## 2. 学生端模块 `/api/student/`

### 2.1 学生看板

- **URL**：`GET /api/student/dashboard/`
- **说明**：统计可申请岗位数、我的申请数、待审核数、已通过数等。

---

### 2.2 岗位列表与详情

- `GET /api/student/positions/`
  - 支持查询参数：`search`、`status`、`page` 等。
- `GET /api/student/positions/{position_id}/`

---

### 2.3 投递申请与申请列表

- `POST /api/student/applications/submit/`
  - 表单字段：岗位 ID、简历（在线文本或附件文件）、附加说明等。
- `GET /api/student/applications/`
- `GET /api/student/applications/{application_id}/`

---

## 3. 教师端模块 `/api/faculty/`

### 3.1 教师看板

- `GET /api/faculty/dashboard/`

---

### 3.2 岗位管理

- `GET /api/faculty/positions/` 我的岗位列表（含筛选/排序）。
- `POST /api/faculty/positions/` 创建岗位。
- `PUT /api/faculty/positions/{position_id}/` 编辑岗位。
- `PATCH /api/faculty/positions/{position_id}/close/` 关闭岗位。

---

### 3.3 申请审核

- `GET /api/faculty/positions/{position_id}/applications/` 查看某岗位的所有申请。
- `GET /api/faculty/applications/` 教师端申请列表。
- `GET /api/faculty/applications/{application_id}/` 单条申请详情。
- `POST /api/faculty/applications/{application_id}/review/` 审核（`accept` / `reject`）。
- `POST /api/faculty/applications/{application_id}/revoke/` 撤销审核，恢复为 `reviewing`。

---

### 3.4 工时审核

- `GET /api/faculty/timesheets/` 助教工时列表。
- `GET /api/faculty/timesheets/{timesheet_id}/` 工时详情（仅限自己岗位）。
- `POST /api/faculty/timesheets/{timesheet_id}/review/` 审核工时（通过/驳回）。

---

## 4. 助教端模块 `/api/ta/`

### 4.1 工时管理

- `POST /api/ta/timesheets/` 提交工时。
- `GET /api/ta/timesheets/` 我的工时列表（筛选/分页）。
- `GET /api/ta/timesheets/{timesheet_id}/` 工时详情。
- `PUT /api/ta/timesheets/{timesheet_id}/update/` 编辑工时（仅待审核状态）。

---

### 4.2 薪酬查询

- `GET /api/ta/salaries/` 薪酬记录列表。
- `GET /api/ta/salaries/{salary_id}/` 薪酬详情。

---

### 4.3 助教看板

- `GET /api/ta/dashboard/`

---

## 5. 通知模块 `/api/notifications/`

- `GET /api/notifications/` 通知列表。
- `GET /api/notifications/{notification_id}/` 通知详情（查看即标记为已读）。
- `POST /api/notifications/{notification_id}/read/` 标记单条已读。
- `POST /api/notifications/read-all/` 全部标记为已读。
- `GET /api/notifications/unread-count/` 未读数量统计。

---

## 6. 师生聊天模块 `/api/chat/`

- `GET /api/chat/conversations/` 会话列表。
- `POST /api/chat/start/` 发起会话（如从岗位详情 / 申请 / 工时场景中发起）。
- `GET /api/chat/conversations/{conversation_id}/messages/` 消息列表。
- `POST /api/chat/conversations/{conversation_id}/send/` 发送消息。

---

## 7. 管理端统计与报表 `/api/admin/`

> 管理端主要依赖 Django Admin，可通过下列接口获取统计与报表数据。

### 7.1 月度报表

- `GET /api/admin/reports/monthly/`
  - 查询参数：`year`、`month`（可选；默认当年当月）。

### 7.2 月度报表导出

- `GET /api/admin/reports/export/`
  - 查询参数：`year`、`month`、`format=csv`
  - 响应：CSV 文件下载。

### 7.3 历史趋势

- `GET /api/admin/reports/trends/`
  - 查询参数：
    - `metric`：`positions` / `applications` / `timesheets` / `salaries`
    - `group_by`：`year` / `month`
    - `start_year`、`end_year`

---

## 8. 版本与变更说明

- 本文档对应代码分支：`main`
- 如接口有新增/调整，应**优先在本文件中更新**，再根据需要在 README 中同步示例或说明。

