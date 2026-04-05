@echo off
chcp 65001
echo ========================================
echo 创建点赞收藏表（无外键版本）
echo ========================================
echo.

mysql -u root -p123456 nba_platform < 创建点赞收藏表-无外键.sql

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo 表创建成功！
    echo ========================================
    echo.
    echo 正在验证表结构...
    mysql -u root -p123456 nba_platform -e "SHOW TABLES LIKE '%%like%%'; SHOW TABLES LIKE '%%favorite%%';"
    echo.
    echo 请重启Django服务器
) else (
    echo.
    echo ========================================
    echo 创建失败！
    echo ========================================
)

echo.
pause
