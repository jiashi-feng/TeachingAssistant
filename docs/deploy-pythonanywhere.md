# 学生助教管理平台 · PythonAnywhere 部署清单

从注册账号到在浏览器中打开站点，按顺序完成以下步骤即可。文中 `yourusername` 请替换为你在 PythonAnywhere 的登录用户名。

---

## 部署前：在本地准备好配置（必读）

在**拉取/上传代码到 PythonAnywhere 之前**，建议在本地先做好下面两件事，这样部署时不会缺配置、也不会被数据库卡住。

### 1. 用环境变量控制“生产配置”（项目已支持）

本项目已通过 **环境变量** 控制敏感和与环境相关的配置，**无需改代码**，只要在部署环境里设置变量即可。

- **本地**：在项目根目录（与 `backend` 同级）放一个 `.env` 文件，用于本地开发；**不要**把 `.env` 提交到 Git（已在 `.gitignore` 中）。
- **PythonAnywhere**：在 PA 的 Web 里填环境变量，或在服务器上放 `/home/yourusername/TeachingAssistant/.env`（与 `backend` 同级）。

**生产环境建议配置示例**（部署时在 PA 使用，不要写进代码仓库；**推荐使用 SQLite**）：

```bash
DEBUG=False
SECRET_KEY=请用随机长字符串
ALLOWED_HOSTS=yourusername.pythonanywhere.com
CSRF_TRUSTED_ORIGINS=https://yourusername.pythonanywhere.com
USE_SQLITE=True
```

- **SECRET_KEY**：可在本地用 `python -c "import secrets; print(secrets.token_urlsafe(50))"` 生成，复制到 PA。
- **ALLOWED_HOSTS / CSRF_TRUSTED_ORIGINS**：换成你的 PA 域名（如 `https://yourusername.pythonanywhere.com`）。
- **USE_SQLITE=True**：使用 SQLite 时必设；无需任何 DB_* 变量。若改用 MySQL，则去掉 USE_SQLITE 并增加下面的 DB_*。



## 一、注册与准备

### 1.1 注册 PythonAnywhere

1. 打开 https://www.pythonanywhere.com/
2. 点击 **Pricing & signup** → 选择 **Create a Beginner account**（免费）
3. 填写用户名、邮箱、密码，完成注册并验证邮箱

### 1.2 登录后进入面板

- 登录后默认进入 **Dashboard**
- 顶部有 **Consoles**、**Web**、**Databases**、**Files** 等标签，后续会用到

---

## 二、上传或拉取项目代码

### 方式 A：用 Git 克隆（推荐，项目已在 Git 仓库时）

1. 打开 **Consoles** → 点击 **$ Bash**
2. 在终端中执行（替换为你的仓库地址）：

   ```bash
   cd ~
   git clone https://github.com/你的用户名/TeachingAssistant.git
   ```

3. 克隆完成后，项目路径为：`/home/yourusername/TeachingAssistant/`
   - 后端代码在：`/home/yourusername/TeachingAssistant/backend/`

### 方式 B：本地上传压缩包

1. 在本地将项目（除 `venv`、`node_modules`、`__pycache__`、`.git` 等）打成 zip
2. 在 PA 的 **Files** 中进入 `/home/yourusername/`
3. 点击 **Upload a file** 上传 zip，再在 **Bash** 里解压：

   ```bash
   cd ~
   unzip TeachingAssistant.zip -d TeachingAssistant
   ```

---

## 三、数据库：SQLite（推荐）或 MySQL（二选一）

### 方案 A：使用 SQLite（推荐，默认）

- **无需**在 **Databases** 里做任何操作。
- 在“五、配置环境变量”中设置 **USE_SQLITE=True**，不要填任何 DB_*。
- 在“四、虚拟环境”中使用 **requirements-sqlite.txt** 安装依赖。
- 首次执行 `python manage.py migrate` 时会在 `backend` 目录下自动生成 `db.sqlite3` 文件。


1. 打开 **Databases**
2. 设置 MySQL 密码（首次使用会提示），记住该密码
3. 点击 **Create** 创建新数据库，例如：
   - Database name: `yourusername$teaching_assistant_db`（免费账户格式为 `用户名$库名`）
   - 创建后记下 **Host name**（一般为 `yourusername.mysql.pythonanywhere-services.com`）
4. 若创建时已自动绑定当前用户，无需再建用户；否则在 Databases 页为该库创建用户并授权
5. 在“五、配置环境变量”中填写 `DB_NAME`、`DB_USER`、`DB_PASSWORD`、`DB_HOST`、`DB_PORT`，**不要**设置 `USE_SQLITE`；在“四、虚拟环境”中使用 **requirements.txt** 安装依赖。

---

## 四、创建 Web 应用与虚拟环境

### 4.1 创建 Web 应用

1. 打开 **Web**
2. 点击 **Add a new web app** → 选 **Manual configuration**（不要选 Django 自动配置）
3. 选择 **Python 3.10**（或 PA 提供的 3.8+ 版本）
4. 创建完成后会得到一个域名：`https://yourusername.pythonanywhere.com`

### 4.2 配置虚拟环境

1. 在 **Web** 页找到 **Virtualenv** 区域
2. 点击 **Enter path to a virtualenv**，输入（注意替换 yourusername）：

   ```
   /home/yourusername/TeachingAssistant/backend/venv
   ```

3. 若该路径还不存在，先到 **Bash** 里创建并安装依赖：

   - **使用 SQLite 时**（推荐，无需 MySQL）：
     ```bash
     cd ~/TeachingAssistant/backend
     python3.10 -m venv venv
     source venv/bin/activate
     pip install --upgrade pip
     pip install -r requirements-sqlite.txt
     ```


   若 PA 上 Python 命令是 `python3`，则用 `python3 -m venv venv`。安装完成后，再在 Web 的 Virtualenv 中填写上述路径。

---

## 五、配置环境变量

项目通过 `.env` 或系统环境变量读取配置。推荐在 PA 的 Web 里配置，避免把敏感信息写进代码。

### 5.1 在 Web 页配置环境变量

1. 在 **Web** 页找到 **Code** 区域
2. 找到 **Environment variables**（或 **WSGI configuration file** 下方的环境变量入口）
3. 按你选的数据库，填写下面其中一组（把 `yourusername` 和密码等换成你的）：

   **使用 SQLite 时**（推荐）：

   ```
   DEBUG=False
   SECRET_KEY=你的随机长字符串
   ALLOWED_HOSTS=yourusername.pythonanywhere.com
   CSRF_TRUSTED_ORIGINS=https://yourusername.pythonanywhere.com
   USE_SQLITE=True
   ```

   
   - `SECRET_KEY` 建议用随机字符串（如 `python -c "import secrets; print(secrets.token_urlsafe(50))"` 生成）


### 5.2 或用项目根目录的 .env 文件

- 项目会从「backend 的上一级目录」加载 `.env`，即 `/home/yourusername/TeachingAssistant/.env`
- 在 **Files** 中进入 `/home/yourusername/TeachingAssistant/`，新建 `.env`，内容与上面 5.1 中“MySQL”或“SQLite”任选一组一致（每行 `KEY=value`，不要引号）
- 若 PA 的 Web 不支持在界面填环境变量，用此方式即可

---

## 六、配置 WSGI

1. 在 **Web** 页 **Code** 区域找到 **WSGI configuration file** 的链接（如 `/var/www/yourusername_pythonanywhere_com_wsgi.py`），点击编辑
2. **删除** 文件内全部内容，改为下面内容（注意把 `yourusername` 换成你的用户名）：

   ```python
   import os
   import sys

   path = '/home/yourusername/TeachingAssistant/backend'
   if path not in sys.path:
       sys.path.insert(0, path)

   os.environ['DJANGO_SETTINGS_MODULE'] = 'TeachingAssistant.settings'

   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```

3. 保存文件

---

## 七、静态文件与媒体文件映射

1. 在 **Web** 页找到 **Static files**
2. 添加两条映射（URL 与目录）：

   | URL        | 目录                                                       |
   | ---------- | ---------------------------------------------------------- |
   | `/static/` | `/home/yourusername/TeachingAssistant/backend/staticfiles` |
   | `/media/`  | `/home/yourusername/TeachingAssistant/backend/media`       |

3. 若尚未执行过 collectstatic，先在 **Bash** 中执行：

   ```bash
   cd ~/TeachingAssistant/backend
   source venv/bin/activate
   python manage.py collectstatic --noinput
   ```

   这样 `/static/` 会指向 `staticfiles` 目录。

---

## 八、数据库迁移与初始数据

在 **Bash** 中执行（虚拟环境需已激活）：

```bash
cd ~/TeachingAssistant/backend
source venv/bin/activate
python manage.py migrate
python manage.py init_basic_data
python manage.py createsuperuser
```

- **SQLite（推荐）**：无需先建库；首次 `migrate` 会在 `backend` 目录生成 `db.sqlite3`。
- **MySQL**：需先在“三、数据库”里建好库并填好 DB_* 环境变量后再执行上述命令。
- `init_basic_data`：初始化角色、权限。
- `createsuperuser`：按提示设置管理员账号密码，用于登录 Admin。

---

## 九、重载 Web 应用并访问

1. 回到 **Web** 页，点击绿色的 **Reload** 按钮
2. 在浏览器中访问：
   - 管理后台：`https://yourusername.pythonanywhere.com/admin/`
   - API 示例：`https://yourusername.pythonanywhere.com/api/auth/login/`
3. 用 `createsuperuser` 创建的账号登录 Admin，确认能正常打开

---

## 十、常见问题排查

| 现象           | 可能原因                                                           | 处理                                                                                                                                    |
| -------------- | ------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| 500 错误       | 环境变量未生效、路径错误、依赖缺失                                 | 在 **Web** 页查看 **Error log**；确认 Virtualenv 路径、WSGI 中 path 和 DJANGO_SETTINGS_MODULE 正确；Bash 中 `pip list` 核对依赖         |
| 静态文件 404   | 未 collectstatic 或 Static files 映射错误                          | 执行 `collectstatic`；核对 URL `/static/` 与目录 `.../backend/staticfiles`                                                              |
| 数据库连接失败 | SQLite 未设 USE_SQLITE 或用了 requirements.txt；MySQL 时 DB_* 填错 | 用 SQLite：设 `USE_SQLITE=True` 且用 `requirements-sqlite.txt`；用 MySQL：在 Databases 页核对库名、Host、用户（库名格式 `用户名$库名`） |
| Admin 样式错乱 | 静态文件未正确提供                                                 | 确认 Static files 映射为 `/static/` → `staticfiles` 并已 collectstatic                                                                  |

---

## 十一、前端部署说明（可选）

当前后端已可在 `https://yourusername.pythonanywhere.com` 提供 API 和 Admin。若要把 Vue 前端也部署上去：

1. 本地在 `frontend` 目录执行 `npm run build`，得到 `dist/`
2. 将 **新的** `dist/` 内所有文件上传到 PA，覆盖原有前端静态文件。**若只更新了后端（如 git pull）而未重新构建并上传前端，浏览器仍会加载旧版 JS，登录可能一直报「CSRF token missing」。**
3. 在 PA 的 **Static files** 中把 `/` 映射到该静态目录；**或**
4. 将前端部署到 Vercel/Netlify 等，把前端访问的 API 地址改为 `https://yourusername.pythonanywhere.com/api`，并在后端 `ALLOWED_HOSTS`、`CSRF_TRUSTED_ORIGINS`、CORS 中加上前端域名

完成以上步骤后，即可在浏览器中通过 `https://yourusername.pythonanywhere.com` 访问你的站点（至少 Admin 与 API 可用）。
