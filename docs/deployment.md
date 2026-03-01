# 学生助教管理平台 · 部署文档

本文档为部署总览，具体环境请按需查阅对应子文档。

---

## 1. 部署方式概览

| 方式 | 说明 | 文档 |
|------|------|------|
| **PythonAnywhere（推荐毕设/演示）** | 免费账号、同域前后端、支持 SQLite | [PythonAnywhere 部署清单](deploy-pythonanywhere.md) |

其他环境（自建 VPS、Docker 等）可参考 PA 清单中的「环境变量、静态文件、数据库迁移、WSGI」等步骤自行适配。

---

## 2. 通用要点

- **环境变量**：生产环境务必设置 `DEBUG=False`、`SECRET_KEY`、`ALLOWED_HOSTS`、`CSRF_TRUSTED_ORIGINS`；使用 SQLite 时设置 `USE_SQLITE=True`。
- **数据库**：首次部署执行 `python manage.py migrate`；使用 MySQL 时需配置 `DB_NAME`、`DB_USER`、`DB_PASSWORD` 等（见 `backend/TeachingAssistant/settings.py`）。
- **静态文件**：生产环境执行 `python manage.py collectstatic`，并在 Web 服务器或 PA 中配置 `/static/` 映射到 `staticfiles` 目录。
- **前端**：Vue 使用 Hash 路由（`/#/login`）；构建产物 `frontend/dist/` 需上传到静态目录或同域提供，详见 [deploy-pythonanywhere.md](deploy-pythonanywhere.md)。

---

## 3. 相关文档

- [API 文档](api.md)
- [数据库文档](database.md)
- [测试方案](testing-plan.md)
