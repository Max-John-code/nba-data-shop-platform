@echo off
chcp 65001
echo ========================================
echo 正在执行点赞收藏功能SQL脚本...
echo ========================================
echo.

echo 请输入MySQL root密码:
set /p password=

echo.
echo 正在连接数据库并执行SQL...
mysql -u root -p%password% nba_platform < 修复点赞收藏字段.sql

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo SQL脚本执行成功！
    echo ========================================
    echo.
    echo 数据库表已创建：
    echo   - highlight_like ^(视频点赞表^)
    echo   - highlight_favorite ^(视频收藏表^)
    echo   - article_like ^(文章点赞表^)
    echo   - article_favorite ^(文章收藏表^)
    echo.
    echo 字段已添加：
    echo   - highlight.likes ^(点赞数^)
    echo   - highlight.favorites ^(收藏数^)
    echo   - article.likes ^(点赞数^)
    echo   - article.favorites ^(收藏数^)
    echo.
    echo 下一步：重启Django服务器
    echo   python manage.py runserver
) else (
    echo.
    echo ========================================
    echo SQL脚本执行失败！
    echo ========================================
    echo.
    echo 可能的原因：
    echo   1. MySQL密码错误
    echo   2. 数据库不存在
    echo   3. 表或字段已存在
    echo.
    echo 请检查错误信息并重试
)

echo.
pause
