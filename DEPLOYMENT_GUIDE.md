# 🚀 教学助手系统 - 部署指南

本文档详细说明如何在新电脑上部署和运行本项目。

---

## 📋 目录

1. [系统要求](#系统要求)
2. [依赖软件安装](#依赖软件安装)
3. [获取项目代码](#获取项目代码)
4. [后端环境配置](#后端环境配置)
5. [数据库配置](#数据库配置)
6. [前端环境配置](#前端环境配置)
7. [启动系统](#启动系统)
8. [验证部署](#验证部署)
9. [常见问题](#常见问题)

---

## 📦 系统要求

### 操作系统
- ✅ Windows 10/11
- ✅ macOS 10.15+
- ✅ Linux (Ubuntu 20.04+)

### 硬件要求
- CPU：双核及以上
- 内存：4GB及以上
- 硬盘：至少5GB可用空间

---

## 🛠️ 依赖软件安装

### 1. Python 3.8+ 安装

#### Windows
1. 访问 [Python官网](https://www.python.org/downloads/)
2. 下载 Python 3.8 或更高版本
3. **安装时勾选 "Add Python to PATH"**
4. 验证安装：
```bash
python --version
# 应该显示: Python 3.8.x 或更高
```

#### macOS
```bash
# 使用Homebrew安装
brew install python@3.8

# 验证安装
python3 --version
```

#### Linux (Ubuntu)
```bash
sudo apt update
sudo apt install python3.8 python3-pip python3-venv
python3 --version
```

---

### 2. MySQL 8.0+ 安装

#### Windows
1. 访问 [MySQL官网](https://dev.mysql.com/downloads/mysql/)
2. 下载 MySQL Community Server 8.0
3. 安装时设置root密码（请记住这个密码）
4. 验证安装：
```bash
mysql --version
# 应该显示: mysql  Ver 8.0.x
```

#### macOS
```bash
# 使用Homebrew安装
brew install mysql@8.0

# 启动MySQL服务
brew services start mysql@8.0

# 设置root密码
mysql_secure_installation
```

#### Linux (Ubuntu)
```bash
sudo apt update
sudo apt install mysql-server

# 启动MySQL服务
sudo systemctl start mysql
sudo systemctl enable mysql

# 设置root密码
sudo mysql_secure_installation
```

**重要配置：**
- 记住设置的root密码（后续配置需要使用）
- 确保MySQL服务已启动

---

### 3. Node.js 16+ 和 npm 安装

#### Windows
1. 访问 [Node.js官网](https://nodejs.org/)
2. 下载 LTS 版本（推荐）
3. 运行安装程序（npm会自动安装）
4. 验证安装：
```bash
node --version
# 应该显示: v16.x.x 或更高

npm --version
# 应该显示: 8.x.x 或更高
```

#### macOS
```bash
# 使用Homebrew安装
brew install node

# 验证安装
node --version
npm --version
```

#### Linux (Ubuntu)
```bash
# 安装Node.js 18.x LTS
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# 验证安装
node --version
npm --version
```

---

### 4. Git 安装（可选，用于克隆代码）

#### Windows
1. 访问 [Git官网](https://git-scm.com/)
2. 下载并安装 Git for Windows
3. 验证：`git --version`

#### macOS/Linux
```bash
# macOS
brew install git

# Ubuntu
sudo apt install git

# 验证
git --version
```

---

## 📥 获取项目代码

### 方式一：使用Git克隆（推荐）
```bash
# 克隆代码仓库
git clone https://github.com/your-username/TeachingAssistant.git

# 进入项目目录
cd TeachingAssistant
```

### 方式二：下载ZIP压缩包
1. 从GitHub仓库下载项目ZIP文件
2. 解压到本地目录
3. 打开命令行，进入解压后的项目目录

---

## 🐍 后端环境配置

### 步骤1：创建Python虚拟环境

```bash
# Windows
cd TeachingAssistant
python -m venv venv
venv\Scripts\activate

# macOS/Linux
cd TeachingAssistant
python3 -m venv venv
source venv/bin/activate

# 激活成功后，命令行前会显示 (venv)
```

**注意：** 每次打开新的命令行窗口都需要重新激活虚拟环境！

---

### 步骤2：安装Python依赖包

```bash
# 确保虚拟环境已激活（命令行前有 (venv) 标识）
cd backend
pip install -r requirements.txt

# 安装过程可能需要5-10分钟，请耐心等待
```

**可能遇到的问题：**

#### 问题1：mysqlclient安装失败（Windows）
**解决方案：**
```bash
# 下载预编译的mysqlclient wheel文件
# 访问: https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient
# 下载对应Python版本的.whl文件，例如：
# mysqlclient‑2.2.0‑cp38‑cp38‑win_amd64.whl (Python 3.8, 64位)

# 安装下载的wheel文件
pip install mysqlclient‑2.2.0‑cp38‑cp38‑win_amd64.whl

# 然后再运行
pip install -r requirements.txt
```

#### 问题2：Pillow安装失败
```bash
# 升级pip
pip install --upgrade pip

# 重新安装Pillow
pip install Pillow
```

---

### 步骤3：配置环境变量

在项目根目录（`TeachingAssistant/`）创建 `.env` 文件：

```bash
# Windows
cd ..
type nul > .env

# macOS/Linux
cd ..
touch .env
```

编辑 `.env` 文件，添加以下内容：

```env
# Django配置
SECRET_KEY=your-secret-key-here-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# 数据库配置（请修改为你的MySQL密码）
DB_NAME=teaching_assistant_db
DB_USER=root
DB_PASSWORD=your_mysql_root_password
DB_HOST=localhost
DB_PORT=3306
```

**重要提示：**
- 将 `your_mysql_root_password` 替换为你在安装MySQL时设置的root密码
- `SECRET_KEY` 可以保持不变（生产环境需要更改）

---

## 💾 数据库配置

### 步骤1：创建数据库

```bash
# 登录MySQL（输入root密码）
mysql -u root -p

# 进入MySQL后，执行以下SQL命令
CREATE DATABASE teaching_assistant_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 验证数据库已创建
SHOW DATABASES;

# 退出MySQL
exit;
```

---

### 步骤2：执行数据库迁移

```bash
# 确保在 backend 目录下，且虚拟环境已激活
cd backend

# 生成迁移文件
python manage.py makemigrations

# 执行迁移（创建数据表）
python manage.py migrate

# 成功后会看到 "Applying xxx... OK" 等提示
```

---

### 步骤3：初始化基础数据

```bash
# 初始化角色和权限数据
python manage.py init_basic_data

# 成功后会显示：
# ✅ 角色初始化完成
# ✅ 权限初始化完成
```

---

### 步骤4：创建超级管理员账号

```bash
python manage.py createsuperuser

# 按提示输入：
# 用户ID (user_id): admin
# 邮箱地址: admin@example.com
# 姓名: 管理员
# 密码: ******** (建议使用强密码)
# 确认密码: ********
```

**记住这个管理员账号，后续需要使用！**

---

## 🌐 前端环境配置

### 步骤1：安装前端依赖

打开**新的命令行窗口**（不要关闭后端窗口）：

```bash
# 进入前端目录
cd TeachingAssistant/frontend

# 安装npm依赖（需要5-10分钟）
npm install

# 如果安装很慢，可以使用国内镜像
npm config set registry https://registry.npmmirror.com
npm install
```

---

### 步骤2：配置API地址

前端默认已配置好API地址（`http://localhost:8000`），无需修改。

如果需要修改，编辑 `frontend/src/utils/request.js`：

```javascript
const service = axios.create({
  baseURL: 'http://localhost:8000',  // 后端API地址
  timeout: 5000
})
```

---

## 🚀 启动系统

### 启动后端服务

```bash
# 在第一个命令行窗口
# 确保在 backend 目录下，虚拟环境已激活

# Windows
cd backend
venv\Scripts\activate
python manage.py runserver

# macOS/Linux
cd backend
source venv/bin/activate
python manage.py runserver
```

**成功启动后会显示：**
```
Django version 4.2.7, using settings 'TeachingAssistant.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

**后端服务地址：** http://localhost:8000

---

### 启动前端服务

```bash
# 在第二个命令行窗口
cd TeachingAssistant/frontend
npm run dev
```

**成功启动后会显示：**
```
  VITE v5.0.11  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

**前端服务地址：** http://localhost:5173

---

## ✅ 验证部署

### 1. 访问前端页面

打开浏览器访问：**http://localhost:5173**

应该看到登录页面。

---

### 2. 访问管理后台

访问：**http://localhost:8000/admin/**

使用之前创建的超级管理员账号登录。

---

### 3. 测试用户注册

1. 在前端页面点击"注册"
2. 填写注册信息（选择"学生"或"教师"角色）
3. 提交注册
4. 使用注册的账号登录

---

### 4. 检查API接口

访问：**http://localhost:8000/api/auth/login/**

应该看到Django REST Framework的API页面。

---

## ❓ 常见问题

### 问题1：后端启动失败 - "mysqlclient连接错误"

**原因：** MySQL服务未启动或密码错误

**解决方案：**
```bash
# Windows - 启动MySQL服务
net start MySQL80

# macOS
brew services start mysql@8.0

# Linux
sudo systemctl start mysql

# 检查 .env 文件中的数据库密码是否正确
```

---

### 问题2：前端访问后端API时报CORS错误

**原因：** 跨域配置问题

**解决方案：**
检查 `backend/TeachingAssistant/settings.py` 中的CORS配置：
```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',     # 确保包含前端地址
    'http://127.0.0.1:5173',
]
```

重启后端服务。

---

### 问题3：npm install 安装失败

**解决方案1：切换npm镜像**
```bash
npm config set registry https://registry.npmmirror.com
npm install
```

**解决方案2：清除缓存**
```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

---

### 问题4：虚拟环境激活后仍提示找不到模块

**解决方案：**
```bash
# 确认虚拟环境已激活（命令行前有 (venv)）
# 重新安装依赖
pip install -r requirements.txt

# 验证Django是否安装成功
python -c "import django; print(django.get_version())"
# 应该显示: 4.2.7
```

---

### 问题5：端口被占用

**后端端口8000被占用：**
```bash
# 使用其他端口启动
python manage.py runserver 8001
```

**前端端口5173被占用：**
编辑 `frontend/vite.config.js`：
```javascript
export default defineConfig({
  server: {
    port: 5174  // 改为其他端口
  }
})
```

---

### 问题6：数据库迁移失败

**解决方案：**
```bash
# 删除所有迁移文件（保留 __init__.py）
# Windows
del /S backend\accounts\migrations\0*.py
del /S backend\recruitment\migrations\0*.py
# （其他模块同理）

# macOS/Linux
find backend -path "*/migrations/*.py" -not -name "__init__.py" -delete

# 重新生成迁移
python manage.py makemigrations
python manage.py migrate
```

---

## 📝 重要提示

### 开发环境注意事项

1. **每次打开新命令行都需要激活虚拟环境：**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

2. **同时运行前后端服务需要两个命令行窗口**

3. **修改代码后：**
   - 后端：会自动重启（无需手动操作）
   - 前端：会自动热更新（无需刷新浏览器）

4. **停止服务：**
   
   - 在命令行窗口按 `Ctrl + C`

---

### 生产环境部署

生产环境部署需要额外配置：

1. **修改 `.env` 文件：**
```env
DEBUG=False
SECRET_KEY=使用强随机密钥
ALLOWED_HOSTS=你的域名.com
```

2. **收集静态文件：**
```bash
python manage.py collectstatic
```

3. **使用生产级服务器：**
   - 后端：Gunicorn + Nginx
   - 前端：`npm run build` 后部署到Nginx

4. **数据库安全：**
   - 创建专用数据库用户（不使用root）
   - 设置强密码
   - 限制访问来源

---

## 🔧 开发工具推荐

### 代码编辑器
- **VSCode** / **Cursor**（推荐）
  - 安装Python插件
  - 安装Vetur/Volar插件（Vue支持）

### API测试工具
- **Postman** 或 **Insomnia**

### 数据库管理工具
- **Navicat** 或 **MySQL Workbench**

---

## ✅ 部署检查清单

部署完成后，请确认：

- [ ] Python 3.8+ 已安装
- [ ] MySQL 8.0+ 已安装并启动
- [ ] Node.js 16+ 已安装
- [ ] 虚拟环境已创建并激活
- [ ] Python依赖已安装
- [ ] `.env` 文件已配置
- [ ] 数据库已创建
- [ ] 数据库迁移已执行
- [ ] 基础数据已初始化
- [ ] 超级管理员已创建
- [ ] 前端依赖已安装
- [ ] 后端服务可正常启动（端口8000）
- [ ] 前端服务可正常启动（端口5173）
- [ ] 可以访问登录页面
- [ ] 可以访问管理后台
- [ ] 用户注册功能正常

---

## 🎉 部署成功！

现在你可以：

1. **访问前端页面：** http://localhost:5173
2. **访问管理后台：** http://localhost:8000/admin/
3. **查看API文档：** http://localhost:8000/api/

开始使用教学助手管理系统吧！

---

**最后更新：** 2025-10-21  
**文档版本：** 1.0

