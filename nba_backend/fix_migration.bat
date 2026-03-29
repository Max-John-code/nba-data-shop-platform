@echo off
echo 激活虚拟环境并修复迁移...
call D:\development_environment\anaconda3\Scripts\activate.bat nba_env
python manage.py migrate highlights --fake
echo.
echo 迁移已标记为完成！
echo 现在可以启动服务器了：python manage.py runserver
pause
