@echo off
chcp 65001
echo ========================================
echo 点赞收藏功能 - 完整安装
echo ========================================
echo.

echo 步骤1: 创建数据表...
mysql -u root -p123456 nba_platform < 创建点赞收藏表-最终版.sql
if %errorlevel% neq 0 (
    echo 表创建失败或表已存在，继续...
)

echo.
echo 步骤2: 添加字段...
mysql -u root -p123456 nba_platform < 添加字段.sql
if %errorlevel% neq 0 (
    echo 字段添加失败或字段已存在，继续...
)

echo.
echo 步骤3: 验证安装...
mysql -u root -p123456 nba_platform -e "SHOW TABLES LIKE '%%like%%'; SHOW TABLES LIKE '%%favorite%%';"

echo.
echo ========================================
echo 安装完成！
echo ========================================
echo.
echo 请重启Django服务器：
echo   python manage.py runserver
echo.
pause
