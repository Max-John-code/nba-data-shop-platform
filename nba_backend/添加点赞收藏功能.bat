@echo off
chcp 65001
echo ========================================
echo 添加点赞和收藏功能
echo ========================================
echo.

echo 步骤1: 创建数据库迁移文件...
python manage.py makemigrations highlights forum
echo.

echo 步骤2: 执行数据库迁移...
python manage.py migrate
echo.

echo ========================================
echo 迁移完成！
echo ========================================
pause
