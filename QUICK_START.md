# Django后端快速开始指南

## 本地开发快速开始

### 1. 克隆项目
```bash
git clone your_repo_url
cd nba_api
```

### 2. 创建虚拟环境
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 配置环境变量
```bash
# 创建 .env 文件
cat > .env << EOF
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
EOF
```

### 5. 数据库迁移
```bash
python manage.py migrate
```

### 6. 创建超级用户
```bash
python manage.py createsuperuser
```

### 7. 启动开发服务器
```bash
python manage.py runserver
```

访问：http://localhost:8000

## 项目结构说明

```
nba_api/
├── manage.py                 # Django管理脚本
├── requirements.txt          # 项目依赖
├── .env                      # 环境变量配置
├── nba_api/                  # 项目配置目录
│   ├── settings.py          # 项目设置
│   ├── urls.py              # 主URL配置
│   ├── wsgi.py              # WSGI配置
│   └── asgi.py              # ASGI配置
├── apps/                     # 应用目录
│   ├── auth/                # 认证应用
│   │   ├── models.py        # 数据模型
│   │   ├── views.py         # 视图函数
│   │   ├── urls.py          # URL路由
│   │   ├── serializers.py   # 序列化器
│   │   └── admin.py         # 管理后台
│   ├── matches/             # 比赛应用
│   ├── news/                # 新闻应用
│   ├── rankings/            # 排行榜应用
│   └── search/              # 搜索应用
├── utils/                    # 工具函数
│   ├── response.py          # 响应格式
│   ├── sms.py               # 短信服务
│   └── jwt_auth.py          # JWT认证
├── templates/               # HTML模板
├── static/                  # 静态文件
├── media/                   # 媒体文件
└── logs/                    # 日志文件
```

## 常用命令

### 数据库操作
```bash
# 创建迁移文件
python manage.py makemigrations

# 应用迁移
python manage.py migrate

# 查看迁移状态
python manage.py showmigrations

# 回滚迁移
python manage.py migrate app_name 0001
```

### 用户管理
```bash
# 创建超级用户
python manage.py createsuperuser

# 修改用户密码
python manage.py changepassword username
```

### 静态文件
```bash
# 收集静态文件
python manage.py collectstatic

# 清理静态文件
python manage.py collectstatic --clear
```

### 测试
```bash
# 运行所有测试
python manage.py test

# 运行特定应用的测试
python manage.py test apps.auth

# 运行特定测试类
python manage.py test apps.auth.tests.UserTestCase

# 运行特定测试方法
python manage.py test apps.auth.tests.UserTestCase.test_login
```

### 调试
```bash
# 进入Django shell
python manage.py shell

# 在shell中可以执行Python代码
>>> from apps.auth.models import User
>>> User.objects.all()
```

## API测试

### 使用curl测试
```bash
# 发送短信验证码
curl -X POST http://localhost:8000/api/auth/sendSmsCode \
  -H "Content-Type: application/json" \
  -d '{"phone":"13800138000"}'

# 用户登录
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phone":"13800138000","smsCode":"1234"}'

# 获取用户信息（需要token）
curl -X GET http://localhost:8000/api/user/profile \
  -H "Authorization: Bearer your_token"
```

### 使用Postman测试
1. 导入API文档
2. 设置环境变量（base_url, token等）
3. 逐个测试API端点

## 常见问题

### Q: 如何修改数据库？
A: 修改settings.py中的DATABASES配置，或在.env文件中设置数据库参数。

### Q: 如何添加新的应用？
A: 
```bash
python manage.py startapp app_name
# 然后在settings.py的INSTALLED_APPS中添加应用
```

### Q: 如何处理CORS错误？
A: 在settings.py中配置CORS_ALLOWED_ORIGINS，添加前端地址。

### Q: 如何上传文件？
A: 使用MultiPartParser，在views.py中处理request.FILES。

### Q: 如何实现分页？
A: 使用DRF的PageNumberPagination，在settings.py中配置PAGE_SIZE。

## 下一步

1. 根据API文档实现各个应用的views和serializers
2. 编写单元测试
3. 配置短信服务（阿里云、腾讯云等）
4. 部署到云服务器
5. 配置HTTPS和域名
6. 监控和优化性能

## 相关文档

- [API文档](API_DOCUMENTATION.md)
- [部署指南](DEPLOYMENT_GUIDE.md)
- [Django官方文档](https://docs.djangoproject.com/)
- [DRF官方文档](https://www.django-rest-framework.org/)
