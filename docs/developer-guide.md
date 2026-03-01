# 学生助教管理平台 · 开发者指南

面向二次开发与协作开发，说明本地环境、代码规范与常用命令。

---

## 1. 本地开发环境

### 1.1 依赖

- Python 3.8+（推荐 3.10）
- Node.js 16+
- MySQL 8.0+ 或 SQLite（本地可用 SQLite 简化环境）

### 1.2 后端

```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
# 配置 .env（或环境变量）后：
python manage.py migrate
python manage.py init_basic_data
python manage.py createsuperuser
python manage.py runserver
```

- 默认：http://localhost:8000  
- API 前缀：`/api/`  
- Admin：http://localhost:8000/admin/

### 1.3 前端

```bash
cd frontend
npm install
npm run dev
```

- 默认：http://localhost:5173  
- 开发时代理：`/api` → `http://localhost:8000`（见 `vite.config.js`）

---

## 2. 代码与仓库规范

- **Python**：遵循 PEP 8；Django 应用按功能划分（accounts、recruitment、application、timesheet、notifications、messaging 等）。
- **前端**：Vue 3 + Composition API；接口请求统一走 `src/api/`，路由与权限见 `src/router/index.js`。
- **Git**：建议 `main` 保持可部署；功能在 `feature/*` 或 `develop` 开发，合并前做基本自测。

---

## 3. 文档与接口

- **API 定义**：以 [docs/api.md](api.md) 为唯一权威，前后端对接以该文档为准。
- **数据库**：表结构概览见 [docs/database.md](database.md)；细节见各应用 `models.py`。
- **部署**：见 [docs/deployment.md](deployment.md) 与 [docs/deploy-pythonanywhere.md](deploy-pythonanywhere.md)。

---

## 4. 常用命令速查

| 用途 | 命令（均在 backend 下） |
|------|-------------------------|
| 迁移 | `python manage.py migrate` |
| 初始化角色/权限 | `python manage.py init_basic_data` |
| 收集静态文件 | `python manage.py collectstatic --noinput` |
| 安全冒烟测试 | `python manage.py security_smoke_test` |
| API 冒烟测试 | 项目根目录 `python scripts/api_smoke_test.py`（需先启动后端） |

---

## 5. 测试

- 测试方案与用例说明：[docs/testing-plan.md](testing-plan.md)。
- 自动化：可运行 `scripts/api_smoke_test.py` 做接口冒烟；无额外 TestCase 要求，见 `backend/README.md`。
