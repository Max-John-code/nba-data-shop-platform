# Django后端项目搭建指南

## 1. 环境准备

### 1.1 本地开发环境
```bash
# 安装Python 3.9+
python --version

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 1.2 云服务器部署
```bash
# SSH连接到云服务器
ssh root@your_server_ip

# 安装Python和依赖
apt-get update
apt-get install python3 python3-pip python3-venv

# 创建项目目录
mkdir /home/nba_api
cd /home/nba_api

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate
```

## 2. 项目结构
```
nba_api/
├── manage.py
├── requirements.txt
├── nba_api/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── auth/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── serializers.py
│   ├── matches/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── serializers.py
│   ├── news/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── serializers.py
│   ├── rankings/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── serializers.py
│   └── search/
│       ├── models.py
│       ├── views.py
│       ├── urls.py
│       └── serializers.py
└── utils/
    ├── sms.py (短信服务)
    ├── jwt_auth.py (JWT认证)
    └── response.py (统一响应格式)
```

## 3. 依赖安装
见 requirements.txt 文件

## 4. 数据库配置
- 本地开发：SQLite
- 云服务器：MySQL 8.0+

## 5. 启动项目
```bash
# 数据库迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 启动开发服务器
python manage.py runserver 0.0.0.0:8000
```

## 6. 云服务器部署
见 DEPLOYMENT_GUIDE.md
