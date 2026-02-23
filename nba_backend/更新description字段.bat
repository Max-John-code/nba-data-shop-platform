@echo off
echo 更新 description 字段为可选...
call D:\development_environment\anaconda3\Scripts\activate.bat nba_env
python manage.py makemigrations highlights
python manage.py migrate highlights
echo.
echo 更新完成！
pause
