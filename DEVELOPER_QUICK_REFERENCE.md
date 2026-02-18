# 开发者快速参考

## 项目结构

```
nba_api/
├── django_backend/          # Django应用目录
│   ├── apps_auth_*         # 认证模块
│   ├── apps_matches_*      # 比赛模块
│   ├── apps_news_*         # 新闻模块
│   ├── apps_rankings_*     # 排行榜模块
│   ├── apps_search_*       # 搜索模块
│   ├── settings.py         # Django配置
│   ├── urls.py             # 主URL配置
│   └── utils_*             # 工具函数
├── src/                     # Vue3前端
├── requirements.txt         # Python依赖
└── .env                     # 环境变量
```

---

## 常用命令

### 数据库操作
```bash
# 创建迁移文件
python manage.py makemigrations

# 执行迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 进入Django shell
python manage.py shell
```

### 服务器
```bash
# 开发服务器
python manage.py runserver 0.0.0.0:8000

# 收集静态文件
python manage.py collectstatic

# 运行测试
python manage.py test
```

---

## API调用示例

### 1. 发送短信验证码
```bash
curl -X POST http://localhost:8000/api/auth/sendSmsCode \
  -H "Content-Type: application/json" \
  -d '{"phone": "13800138000"}'
```

**响应：**
```json
{
  "code": 0,
  "message": "验证码已发送",
  "data": {
    "expiresIn": 300
  }
}
```

### 2. 用户登录
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phone": "13800138000", "smsCode": "1234"}'
```

**响应：**
```json
{
  "code": 0,
  "message": "登录成功",
  "data": {
    "userId": "1",
    "phone": "13800138000",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "userName": "13800138000"
  }
}
```

### 3. 获取比赛列表
```bash
curl -X GET "http://localhost:8000/api/matches/list?date=2025-02-18&page=1&pageSize=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 4. 获取新闻列表
```bash
curl -X GET "http://localhost:8000/api/news/list?sort=hot&page=1&pageSize=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 5. 点赞新闻
```bash
curl -X POST http://localhost:8000/api/news/1/like \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 6. 搜索新闻
```bash
curl -X GET "http://localhost:8000/api/search/news?keyword=篮球&page=1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 7. 获取球队排行榜
```bash
curl -X GET "http://localhost:8000/api/rankings/teams?season=2025-26" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 8. 获取球员排行榜
```bash
curl -X GET "http://localhost:8000/api/rankings/players?stat=points&season=2025-26" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 响应格式

### 成功响应
```json
{
  "code": 0,
  "message": "成功消息",
  "data": {
    // 具体数据
  }
}
```

### 失败响应
```json
{
  "code": 1,
  "message": "错误消息"
}
```

---

## 认证

所有需要认证的接口都需要在请求头中添加：
```
Authorization: Bearer {token}
```

Token有效期：7天

---

## 分页参数

所有列表接口都支持分页：
- `page` - 页码（从1开始）
- `pageSize` - 每页数量（默认10，最大100）

---

## 数据库连接

### 本地开发（SQLite）
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### 生产环境（MySQL）
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nba_api',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

---

## 常见错误处理

### 401 Unauthorized
- Token过期或无效
- 需要重新登录获取新token

### 400 Bad Request
- 请求参数错误
- 检查参数格式和必填项

### 404 Not Found
- 资源不存在
- 检查资源ID是否正确

### 500 Internal Server Error
- 服务器错误
- 查看服务器日志

---

## 环境变量配置

```env
# Django配置
SECRET_KEY=your-secret-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# 数据库配置
DB_ENGINE=django.db.backends.mysql
DB_NAME=nba_api
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=3306

# 短信服务配置
SMS_API_KEY=your-api-key
SMS_API_SECRET=your-api-secret

# JWT配置
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=168
```

---

## 文件上传

### 更新用户头像
```bash
curl -X PUT http://localhost:8000/api/user/profile \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "avatar=@/path/to/image.jpg"
```

---

## 日志查看

日志文件位置：`logs/debug.log`

```bash
# 查看最后100行日志
tail -100 logs/debug.log

# 实时查看日志
tail -f logs/debug.log
```

---

## 性能优化建议

1. **缓存热门数据**
   - 排行榜数据
   - 热门新闻
   - 球队信息

2. **数据库索引**
   - 在phone字段添加索引
   - 在date字段添加索引
   - 在created_at字段添加索引

3. **异步任务**
   - 使用Celery处理短信发送
   - 使用Celery处理数据更新

4. **API限流**
   - 实现请求频率限制
   - 防止API滥用

---

## 部署检查清单

- [ ] 更改SECRET_KEY
- [ ] 设置DEBUG=False
- [ ] 配置ALLOWED_HOSTS
- [ ] 配置数据库（MySQL）
- [ ] 配置短信服务
- [ ] 配置CORS
- [ ] 收集静态文件
- [ ] 配置Nginx
- [ ] 配置SSL证书
- [ ] 配置日志
- [ ] 配置监控

---

## 有用的链接

- [Django官方文档](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [JWT认证](https://django-rest-framework-simplejwt.readthedocs.io/)
- [MySQL文档](https://dev.mysql.com/doc/)

---

## 联系方式

如有问题，请查看：
- `BACKEND_IMPLEMENTATION_GUIDE.md` - 详细实现指南
- `DEPLOYMENT_GUIDE.md` - 部署指南
- `API_DOCUMENTATION_BASKETBALL_ONLY.md` - API文档
