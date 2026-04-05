@echo off
chcp 65001
echo ========================================
echo 快速修复点赞收藏数据库
echo ========================================
echo.
echo 正在执行SQL脚本...
echo.

mysql -u root -p123456 nba_platform < 修复点赞收藏字段.sql

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo 数据库修复成功！
    echo ========================================
    echo.
    echo 请重启Django服务器：
    echo   python manage.py runserver
) else (
    echo.
    echo ========================================
    echo 执行失败！请检查MySQL密码
    echo ========================================
)

echo.
pause
