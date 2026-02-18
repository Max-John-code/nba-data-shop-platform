# 故障排除指南

## 🔍 常见问题和解决方案

---

## 数据库相关问题

### 问题1：无法连接到MySQL数据库
**错误信息：**
```
django.db.utils.OperationalError: (2003, "Can't connect to MySQL server on 'localhost' (10061)")
```

**解决方案：**
1. 检查MySQL服务是否运行
   ```bash
   # Windows
   net start MySQL80
   
   # Linux
   sudo systemctl start mysql
   
   # Mac
   brew services start mysql
   ```

2. 检查数据库连接信息
   ```bash
   # 测试连接
   mysql -u root -p -h localhost
   ```

3. 检查.env文件中的数据库配置
   ```env
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=your-password
   ```

---

### 问题2：数据库不存在
**错误信息：**
```
django.db.utils.ProgrammingError: (1049, "Unknown database 'nba_api'")
```

**解决方案：**
```bash
# 创建数据库
mysql -u root -p
CREATE DATABASE nba_api CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

---

### 问题3：迁移失败
**错误信息：**
```
django.db.migrations.exceptions.MigrationSchemaMissing
```

**解决方案：**
```bash
# 重新执行迁移
python manage.py migrate --run-syncdb

# 或者删除迁移文件重新创建
python manage.py makemigrations
python manage.py migrate
```

---

## 认证相关问题

### 问题4：Token过期
**错误信息：**
```json
{
  "code": 1,
  "message": "Token已过期"
}
```

**解决方案：**
1. 重新登录获取新的token
2. 检查settings.py中的token过期时间
   ```python
   SIMPLE_JWT = {
       'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
   }
   ```

---

### 问题5：短信验证码发送失败
**错误信息：**
```
SMSException: Failed to send SMS
```

**解决方案：**
1. 检查短信服务配置
   ```env
   SMS_API_KEY=your-api-key
   SMS_API_SECRET=your-api-secret
   ```

2. 检查短信服务是否可用
   ```bash
   # 测试短信服务连接
   python manage.py shell
   >>> from utils.sms import send_sms
   >>> send_sms('13800138000', '测试验证码：1234')
   ```

3. 检查手机号格式
   - 必须是11位数字
   - 必须是有效的中国手机号

---

### 问题6：验证码频率限制
**错误信息：**
```json
{
  "code": 1,
  "message": "请求过于频繁，请60秒后再试"
}
```

**解决方案：**
- 这是正常的频率限制，防止滥用
- 等待60秒后重试
- 如需修改限制，编辑apps_auth_views.py中的send_sms_code函数

---

## API相关问题

### 问题7：401 Unauthorized
**错误信息：**
```json
{
  "code": 1,
  "message": "未授权"
}
```

**解决方案：**
1. 检查请求头中是否包含Authorization
   ```
   Authorization: Bearer YOUR_TOKEN
   ```

2. 检查token是否有效
   ```bash
   # 在Django shell中验证token
   python manage.py shell
   >>> from rest_framework_simplejwt.tokens import AccessToken
   >>> token = AccessToken('YOUR_TOKEN')
   >>> token.payload
   ```

3. 重新登录获取新的token

---

### 问题8：400 Bad Request
**错误信息：**
```json
{
  "code": 1,
  "message": "请输入正确的11位手机号"
}
```

**解决方案：**
1. 检查请求参数
   - 手机号必须是11位数字
   - 验证码必须是4位数字
   - 密码必须是6-16位字母数字

2. 检查请求格式
   ```json
   {
     "phone": "13800138000",
     "smsCode": "1234"
   }
   ```

3. 检查Content-Type
   ```
   Content-Type: application/json
   ```

---

### 问题9：404 Not Found
**错误信息：**
```json
{
  "code": 1,
  "message": "资源不存在"
}
```

**解决方案：**
1. 检查资源ID是否正确
2. 检查资源是否存在于数据库
3. 检查URL路径是否正确

---

### 问题10：500 Internal Server Error
**错误信息：**
```
Internal Server Error
```

**解决方案：**
1. 查看服务器日志
   ```bash
   tail -100 logs/debug.log
   ```

2. 检查错误堆栈跟踪
3. 在Django shell中测试代码
4. 检查数据库连接

---

## CORS相关问题

### 问题11：CORS错误
**错误信息：**
```
Access to XMLHttpRequest at 'http://localhost:8000/api/...' from origin 'http://localhost:5173' 
has been blocked by CORS policy
```

**解决方案：**
1. 检查settings.py中的CORS配置
   ```python
   CORS_ALLOWED_ORIGINS = [
       'http://localhost:5173',
       'http://localhost:8080',
   ]
   ```

2. 添加前端地址到CORS_ALLOWED_ORIGINS
3. 重启Django服务器

---

## 性能相关问题

### 问题12：API响应缓慢
**症状：**
- API响应时间超过1秒
- 数据库查询缓慢

**解决方案：**
1. 检查数据库索引
   ```sql
   SHOW INDEX FROM users;
   SHOW INDEX FROM news;
   ```

2. 优化查询语句
   ```python
   # 使用select_related和prefetch_related
   matches = Match.objects.select_related('team1', 'team2')
   ```

3. 添加缓存
   ```python
   from django.views.decorators.cache import cache_page
   
   @cache_page(60 * 5)  # 缓存5分钟
   def get_news_list(request):
       ...
   ```

4. 使用分页
   ```python
   paginator = NewsPagination()
   page = paginator.paginate_queryset(news_list, request)
   ```

---

### 问题13：内存占用过高
**症状：**
- 服务器内存占用不断增加
- 服务器变得缓慢

**解决方案：**
1. 检查是否有内存泄漏
2. 限制查询结果数量
3. 使用分页
4. 定期重启服务器

---

## 部署相关问题

### 问题14：Gunicorn启动失败
**错误信息：**
```
Error: Failed to find application object
```

**解决方案：**
1. 检查WSGI配置
   ```bash
   gunicorn nba_api.wsgi:application --bind 0.0.0.0:8000
   ```

2. 检查项目结构
3. 检查Python路径

---

### 问题15：Nginx配置错误
**错误信息：**
```
502 Bad Gateway
```

**解决方案：**
1. 检查Nginx配置
   ```bash
   sudo nginx -t
   ```

2. 检查Gunicorn是否运行
   ```bash
   ps aux | grep gunicorn
   ```

3. 检查Nginx日志
   ```bash
   tail -100 /var/log/nginx/error.log
   ```

4. 检查Gunicorn日志
   ```bash
   tail -100 /var/log/gunicorn/error.log
   ```

---

### 问题16：SSL证书错误
**错误信息：**
```
SSL_ERROR_RX_RECORD_TOO_LONG
```

**解决方案：**
1. 检查SSL证书配置
2. 检查Nginx SSL配置
3. 重新生成SSL证书

---

## 日志相关问题

### 问题17：日志文件过大
**症状：**
- 日志文件占用大量磁盘空间
- 服务器磁盘空间不足

**解决方案：**
1. 配置日志轮转
   ```python
   'handlers': {
       'file': {
           'level': 'INFO',
           'class': 'logging.handlers.RotatingFileHandler',
           'filename': BASE_DIR / 'logs' / 'debug.log',
           'maxBytes': 1024 * 1024 * 10,  # 10MB
           'backupCount': 5,
       },
   }
   ```

2. 定期清理旧日志
   ```bash
   find logs/ -name "*.log" -mtime +30 -delete
   ```

---

## 数据相关问题

### 问题18：数据不一致
**症状：**
- 数据库中的数据与预期不符
- 点赞数不正确

**解决方案：**
1. 检查数据库事务
2. 检查并发问题
3. 使用数据库锁
4. 定期数据验证

---

### 问题19：数据丢失
**症状：**
- 数据库中的数据消失
- 用户信息丢失

**解决方案：**
1. 检查备份
2. 恢复备份
3. 检查删除操作
4. 实现软删除

---

## 调试技巧

### 启用Django调试模式
```python
# settings.py
DEBUG = True
```

### 使用Django Shell
```bash
python manage.py shell

# 测试模型
>>> from apps.auth.models import User
>>> User.objects.all()

# 测试序列化器
>>> from apps.auth.serializers import UserSerializer
>>> user = User.objects.first()
>>> serializer = UserSerializer(user)
>>> serializer.data
```

### 查看SQL查询
```python
from django.db import connection
from django.test.utils import CaptureQueriesContext

with CaptureQueriesContext(connection) as context:
    # 执行查询
    users = User.objects.all()
    
# 查看SQL
for query in context.captured_queries:
    print(query['sql'])
```

### 使用Django Debug Toolbar
```bash
pip install django-debug-toolbar
```

---

## 获取帮助

### 查看日志
```bash
# 查看最后100行
tail -100 logs/debug.log

# 实时查看
tail -f logs/debug.log

# 搜索错误
grep ERROR logs/debug.log
```

### 查看数据库
```bash
# 连接数据库
mysql -u root -p nba_api

# 查看表
SHOW TABLES;

# 查看表结构
DESCRIBE users;

# 查看数据
SELECT * FROM users;
```

### 查看进程
```bash
# 查看Python进程
ps aux | grep python

# 查看端口占用
lsof -i :8000
```

---

## 联系方式

如需进一步帮助，请参考：
- `BACKEND_IMPLEMENTATION_GUIDE.md` - 详细实现指南
- `DEVELOPER_QUICK_REFERENCE.md` - 快速参考
- `API_DOCUMENTATION_BASKETBALL_ONLY.md` - API文档
- `DEPLOYMENT_GUIDE.md` - 部署指南
