# Django后端实现指南

## 项目概述
本指南详细说明如何完成NBA篮球数据咨询应用的Django后端实现。

---

## 已完成的工作

### 1. 数据模型 (Models)
- ✅ `apps_auth_models.py` - 用户和短信验证码模型
- ✅ `apps_matches_models.py` - 比赛和球队模型
- ✅ `apps_news_models.py` - 新闻和新闻点赞模型
- ✅ `apps_rankings_models.py` - 球队排行榜和球员排行榜模型

### 2. 序列化器 (Serializers)
- ✅ `apps_auth_serializers.py` - 用户和短信验证码序列化器
- ✅ `apps_matches_serializers.py` - 比赛和球队序列化器
- ✅ `apps_news_serializers.py` - 新闻序列化器
- ✅ `apps_rankings_serializers.py` - 排行榜序列化器

### 3. 视图 (Views)
- ✅ `apps_auth_views.py` - 认证视图（登录、注册、发送短信、获取/更新用户信息、修改密码）
- ✅ `apps_matches_views.py` - 比赛视图（获取列表、获取详情）
- ✅ `apps_news_views.py` - 新闻视图（获取列表、获取详情、点赞、取消点赞）
- ✅ `apps_rankings_views.py` - 排行榜视图（获取球队排行榜、获取球员排行榜）
- ✅ `apps_search_views.py` - 搜索视图（搜索新闻、搜索球队、搜索球员）

### 4. URL路由 (URLs)
- ✅ `urls.py` - 主项目URL配置
- ✅ `urls_auth.py` - 认证模块URL
- ✅ `urls_matches.py` - 比赛模块URL
- ✅ `urls_news.py` - 新闻模块URL
- ✅ `urls_rankings.py` - 排行榜模块URL
- ✅ `urls_search.py` - 搜索模块URL
- ✅ `urls_user.py` - 用户模块URL

### 5. 工具函数 (Utils)
- ✅ `utils_response.py` - 统一响应格式
- ✅ `utils_sms.py` - 短信发送服务

### 6. 配置 (Settings)
- ✅ `settings.py` - Django配置（数据库、认证、CORS等）

---

## 后续实现步骤

### 第1步：安装依赖
```bash
pip install -r requirements.txt
```

**requirements.txt 应包含：**
```
Django==4.2.0
djangorestframework==3.14.0
djangorestframework-simplejwt==5.2.2
django-cors-headers==4.0.0
python-decouple==3.8
mysqlclient==2.1.1
Pillow==9.5.0
```

### 第2步：配置环境变量
创建 `.env` 文件在项目根目录：
```
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=nba_api
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=3306
SMS_API_KEY=your-sms-api-key
SMS_API_SECRET=your-sms-api-secret
```

### 第3步：创建数据库
```bash
# 创建MySQL数据库
mysql -u root -p
CREATE DATABASE nba_api CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### 第4步：执行数据库迁移
```bash
python manage.py makemigrations
python manage.py migrate
```

### 第5步：创建超级用户（可选）
```bash
python manage.py createsuperuser
```

### 第6步：配置SMS服务
编辑 `utils_sms.py`，集成实际的短信服务提供商（如阿里云、腾讯云等）：

```python
# 示例：使用阿里云短信服务
from aliyunsdkcore.client import AcsClient
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest

def send_sms(phone, message):
    client = AcsClient(
        settings.SMS_API_KEY,
        settings.SMS_API_SECRET,
        'cn-hangzhou'
    )
    
    request = SendSmsRequest()
    request.set_PhoneNumbers(phone)
    request.set_SignName('NBA篮球数据咨询')
    request.set_TemplateCode('SMS_TEMPLATE_CODE')
    request.set_TemplateParam(f'{{"code": "{message}"}}')
    
    response = client.do_action_with_exception(request)
    return response
```

### 第7步：运行开发服务器
```bash
python manage.py runserver 0.0.0.0:8000
```

---

## API端点总结

### 认证接口 (3个)
- `POST /api/auth/sendSmsCode` - 发送短信验证码
- `POST /api/auth/login` - 用户登录
- `POST /api/auth/register` - 用户注册

### 比赛接口 (2个)
- `GET /api/matches/list` - 获取比赛列表
- `GET /api/matches/<matchId>` - 获取比赛详情

### 新闻接口 (4个)
- `GET /api/news/list` - 获取新闻列表
- `GET /api/news/<newsId>` - 获取新闻详情
- `POST /api/news/<newsId>/like` - 点赞新闻
- `DELETE /api/news/<newsId>/like` - 取消点赞

### 排行榜接口 (2个)
- `GET /api/rankings/teams` - 获取球队排行榜
- `GET /api/rankings/players` - 获取球员排行榜

### 用户接口 (3个)
- `GET /api/user/profile` - 获取用户信息
- `PUT /api/user/profile` - 更新用户信息
- `POST /api/user/changePassword` - 修改密码

### 搜索接口 (3个)
- `GET /api/search/news` - 搜索新闻
- `GET /api/search/teams` - 搜索球队
- `GET /api/search/players` - 搜索球员

**总计：17个API端点**

---

## 数据库表结构

### users (用户表)
```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    phone VARCHAR(11) UNIQUE NOT NULL,
    username VARCHAR(100),
    password VARCHAR(255),
    avatar VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### sms_codes (短信验证码表)
```sql
CREATE TABLE sms_codes (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    phone VARCHAR(11) NOT NULL,
    code VARCHAR(4) NOT NULL,
    is_used BOOLEAN DEFAULT FALSE,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### teams (球队表)
```sql
CREATE TABLE teams (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(100),
    logo VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### matches (比赛表)
```sql
CREATE TABLE matches (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    date DATE NOT NULL,
    team1_id BIGINT NOT NULL,
    team2_id BIGINT NOT NULL,
    team1_score INT,
    team2_score INT,
    status VARCHAR(20),
    viewers VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (team1_id) REFERENCES teams(id),
    FOREIGN KEY (team2_id) REFERENCES teams(id)
);
```

### news (新闻表)
```sql
CREATE TABLE news (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    content LONGTEXT,
    image VARCHAR(255),
    source VARCHAR(100),
    author VARCHAR(100),
    comments INT DEFAULT 0,
    likes INT DEFAULT 0,
    shares INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### news_likes (新闻点赞表)
```sql
CREATE TABLE news_likes (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    news_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_user_news (user_id, news_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (news_id) REFERENCES news(id)
);
```

### team_rankings (球队排行榜表)
```sql
CREATE TABLE team_rankings (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    rank INT NOT NULL,
    team_id BIGINT NOT NULL,
    team_name VARCHAR(100),
    wins INT,
    losses INT,
    win_rate VARCHAR(10),
    points_for DECIMAL(5,1),
    points_against DECIMAL(5,1),
    season VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (team_id) REFERENCES teams(id)
);
```

### player_rankings (球员排行榜表)
```sql
CREATE TABLE player_rankings (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    rank INT NOT NULL,
    player_id BIGINT,
    player_name VARCHAR(100),
    team_name VARCHAR(100),
    value DECIMAL(5,1),
    games INT,
    stat_type VARCHAR(20),
    season VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 测试API

### 使用Postman或cURL测试

**1. 发送短信验证码**
```bash
curl -X POST http://localhost:8000/api/auth/sendSmsCode \
  -H "Content-Type: application/json" \
  -d '{"phone": "13800138000"}'
```

**2. 用户登录**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phone": "13800138000", "smsCode": "1234"}'
```

**3. 获取比赛列表**
```bash
curl -X GET http://localhost:8000/api/matches/list \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**4. 获取新闻列表**
```bash
curl -X GET http://localhost:8000/api/news/list \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 部署到云服务器

详见 `DEPLOYMENT_GUIDE.md`

---

## 常见问题

### Q: 如何修改数据库连接？
A: 编辑 `.env` 文件中的数据库配置参数

### Q: 如何集成真实的短信服务？
A: 编辑 `utils_sms.py`，使用相应的短信服务SDK

### Q: 如何处理CORS错误？
A: 在 `settings.py` 中配置 `CORS_ALLOWED_ORIGINS`

### Q: Token过期怎么办？
A: 前端需要重新登录获取新的token，或使用refresh token刷新

---

## 下一步

1. ✅ 完成所有API实现
2. ⏳ 编写单元测试
3. ⏳ 性能优化和缓存配置
4. ⏳ 部署到云服务器
5. ⏳ 监控和日志配置
