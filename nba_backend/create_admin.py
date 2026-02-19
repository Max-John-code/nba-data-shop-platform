#!/usr/bin/env python
"""快速创建管理员用户的脚本"""
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nba_backend.settings')
django.setup()

from accounts.models import User

def create_admin(phone):
    """创建管理员用户"""
    # 检查用户是否已存在
    if User.objects.filter(phone=phone).exists():
        user = User.objects.get(phone=phone)
        user.role = 'admin'
        user.save()
        print(f"✓ 用户 {phone} 已升级为管理员")
    else:
        # 创建新管理员
        user = User.objects.create(
            username=phone,
            phone=phone,
            role='admin'
        )
        print(f"✓ 管理员用户创建成功: {phone}")
    
    print(f"  登录验证码: 9999 (管理员专用)")
    return user

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("使用方法: python create_admin.py <手机号>")
        print("示例: python create_admin.py 13900139000")
        sys.exit(1)
    
    phone = sys.argv[1]
    
    # 验证手机号格式
    if not phone.isdigit() or len(phone) != 11:
        print("错误: 请输入正确的11位手机号")
        sys.exit(1)
    
    create_admin(phone)
