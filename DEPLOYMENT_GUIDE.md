# Django后端云服务器部署指南

## 1. 云服务器环境准备

### 1.1 连接到云服务器
```bash
ssh root@your_server_ip
```

### 1.2 安装系统依赖
```bash
# Ubuntu/Debian
apt-get update
apt-get install -y python3 python3-pip python3-venv mysql-server nginx supervisor git

# CentOS/RHEL
yum install -y python3 python3-pip mysql-server nginx supervisor git
```

### 1.3 创建项目目录
```bash
mkdir -p /home/nba_api
cd /home/nba_api
git clone your_repo_url .
```

## 2. Python环境配置

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 3. 数据库配置

### 3.1 MySQL配置
```bash
# 登录MySQL
mysql -u root -p

# 创建数据库
CREATE DATABASE nba_api CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'nba_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON nba_api.* TO 'nba_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3.2 创建.env文件
```bash
cat > /home/nba_api/.env << EOF
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your_domain.com,www.your_domain.com,your_server_ip
DB_ENGINE=django.db.backends.mysql
DB_NAME=nba_api
DB_USER=nba_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
SMS_API_KEY=your_sms_api_key
SMS_API_SECRET=your_sms_api_secret
EOF
```

## 4. Django配置

```bash
cd /home/nba_api

# 数据库迁移
python manage.py migrate

# 收集静态文件
python manage.py collectstatic --noinput

# 创建超级用户
python manage.py createsuperuser
```

## 5. Gunicorn配置

### 5.1 创建gunicorn配置文件
```bash
cat > /home/nba_api/gunicorn_config.py << EOF
import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2
EOF
```

### 5.2 启动Gunicorn
```bash
cd /home/nba_api
source venv/bin/activate
gunicorn -c gunicorn_config.py nba_api.wsgi:application
```

## 6. Nginx配置

### 6.1 创建Nginx配置文件
```bash
cat > /etc/nginx/sites-available/nba_api << 'EOF'
upstream nba_api {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name your_domain.com www.your_domain.com;
    
    client_max_body_size 100M;
    
    location / {
        proxy_pass http://nba_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static/ {
        alias /home/nba_api/staticfiles/;
    }
    
    location /media/ {
        alias /home/nba_api/media/;
    }
}
EOF
```

### 6.2 启用Nginx配置
```bash
ln -s /etc/nginx/sites-available/nba_api /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

## 7. Supervisor配置

### 7.1 创建Supervisor配置文件
```bash
cat > /etc/supervisor/conf.d/nba_api.conf << 'EOF'
[program:nba_api]
command=/home/nba_api/venv/bin/gunicorn -c /home/nba_api/gunicorn_config.py nba_api.wsgi:application
directory=/home/nba_api
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/nba_api/logs/gunicorn.log
EOF
```

### 7.2 启动Supervisor
```bash
supervisorctl reread
supervisorctl update
supervisorctl start nba_api
```

## 8. SSL证书配置（HTTPS）

### 8.1 使用Let's Encrypt
```bash
apt-get install -y certbot python3-certbot-nginx
certbot certonly --nginx -d your_domain.com -d www.your_domain.com
```

### 8.2 更新Nginx配置
```bash
# 编辑 /etc/nginx/sites-available/nba_api
# 添加SSL配置
listen 443 ssl;
ssl_certificate /etc/letsencrypt/live/your_domain.com/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/your_domain.com/privkey.pem;
```

## 9. 日志管理

```bash
# 创建日志目录
mkdir -p /home/nba_api/logs

# 配置日志轮转
cat > /etc/logrotate.d/nba_api << 'EOF'
/home/nba_api/logs/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
}
EOF
```

## 10. 监控和维护

### 10.1 查看日志
```bash
# Gunicorn日志
tail -f /home/nba_api/logs/gunicorn.log

# Nginx日志
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# Django日志
tail -f /home/nba_api/logs/debug.log
```

### 10.2 重启服务
```bash
# 重启Gunicorn
supervisorctl restart nba_api

# 重启Nginx
systemctl restart nginx

# 重启MySQL
systemctl restart mysql
```

## 11. 备份策略

### 11.1 数据库备份
```bash
# 创建备份脚本
cat > /home/nba_api/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/home/nba_api/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mysqldump -u nba_user -p'your_password' nba_api > $BACKUP_DIR/nba_api_$DATE.sql
gzip $BACKUP_DIR/nba_api_$DATE.sql
EOF

chmod +x /home/nba_api/backup.sh

# 添加到crontab（每天凌晨2点备份）
crontab -e
# 添加: 0 2 * * * /home/nba_api/backup.sh
```

## 12. 常见问题

### 问题1：502 Bad Gateway
- 检查Gunicorn是否运行：`supervisorctl status nba_api`
- 查看Gunicorn日志：`tail -f /home/nba_api/logs/gunicorn.log`

### 问题2：数据库连接失败
- 检查MySQL是否运行：`systemctl status mysql`
- 检查.env文件中的数据库配置

### 问题3：静态文件404
- 重新收集静态文件：`python manage.py collectstatic --noinput`
- 检查Nginx配置中的静态文件路径

## 13. 性能优化

### 13.1 数据库优化
```bash
# 在MySQL中创建索引
mysql -u nba_user -p'your_password' nba_api < indexes.sql
```

### 13.2 缓存配置
```python
# 在settings.py中添加Redis缓存
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### 13.3 CDN配置
- 将静态文件和媒体文件上传到CDN
- 更新settings.py中的STATIC_URL和MEDIA_URL

## 14. 安全建议

1. 定期更新系统和依赖包
2. 配置防火墙规则
3. 使用HTTPS
4. 定期备份数据库
5. 监控服务器资源使用情况
6. 设置强密码
7. 禁用root远程登录
