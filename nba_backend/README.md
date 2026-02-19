# NBA数据商城后端

## 安装依赖

```bash
pip install -r requirements.txt
```

## 数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

## 创建超级管理员（可选）

```bash
python manage.py createsuperuser
```

## 启动开发服务器

```bash
python manage.py runserver
```

服务器将在 http://127.0.0.1:8000 启动

## API接口

### 发送短信验证码
- URL: `/api/accounts/send-sms/`
- 方法: POST
- 参数: `{"phone": "13800138000"}`

### 登录
- URL: `/api/accounts/login/`
- 方法: POST
- 参数: `{"phone": "13800138000", "sms_code": "1234"}`

### 注册
- URL: `/api/accounts/register/`
- 方法: POST
- 参数: `{"phone": "13800138000", "sms_code": "1234"}`

## 注意事项

- 开发环境下，验证码会在响应中返回，方便测试
- 生产环境需要接入真实的短信服务商
- 验证码有效期为5分钟
- 同一手机号60秒内只能发送一次验证码
