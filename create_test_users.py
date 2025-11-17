#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
👥 إنشاء مستخدمين تجريبيين مع مشاريع
=====================================

هذا الملف سينشئ مستخدمين تجريبيين لاختبار النظام
"""

import sys
import os

# إضافة مسار المشروع
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sheets.users_manager import UsersManager

def create_test_users():
    """إنشاء مستخدمين تجريبيين"""
    
    print("👥 إنشاء مستخدمين تجريبيين...")
    print("="*50)
    
    # إنشاء مدير المستخدمين
    users_manager = UsersManager('config/credentials.json', 'Inventory Management')
    
    if not users_manager.connect():
        print("❌ فشل في الاتصال بـ Google Sheets!")
        return False
    
    # قائمة المستخدمين التجريبيين
    test_users = [
        {
            "username": "admin",
            "password": "admin123",
            "user_type": "admin",
            "project_id": "",  # المدير يرى جميع المشاريع
            "name": "أحمد المدير العام"
        },
        {
            "username": "mohammed_prj1",
            "password": "mohammed123",
            "user_type": "user", 
            "project_id": "PRJ_2024_001",
            "name": "محمد مدير المشروع الأول"
        },
        {
            "username": "fatma_prj2",
            "password": "fatma123",
            "user_type": "user",
            "project_id": "PRJ_2024_002", 
            "name": "فاطمة مديرة المشروع الثاني"
        },
        {
            "username": "ali_prj3",
            "password": "ali123",
            "user_type": "user",
            "project_id": "PRJ_2024_003",
            "name": "علي مدير المشروع الثالث"
        },
        {
            "username": "sara_prj4",
            "password": "sara123", 
            "user_type": "user",
            "project_id": "PRJ_2024_004",
            "name": "سارة مديرة المشروع الرابع"
        }
    ]
    
    # إنشاء المستخدمين
    successful_users = []
    failed_users = []
    
    for user_data in test_users:
        try:
            print(f"📝 إنشاء المستخدم: {user_data['username']} - {user_data['name']}")
            
            # محاولة إنشاء المستخدم
            result = users_manager.create_user_with_project(
                username=user_data['username'],
                password=user_data['password'],
                user_type=user_data['user_type'],
                project_id=user_data['project_id']
            )
            
            if result:
                successful_users.append(user_data)
                project_text = f"المشروع: {user_data['project_id']}" if user_data['project_id'] else "جميع المشاريع"
                print(f"   ✅ تم الإنشاء بنجاح - {project_text}")
            else:
                failed_users.append(user_data)
                print(f"   ❌ فشل في الإنشاء")
                
        except Exception as e:
            failed_users.append(user_data)
            print(f"   ❌ خطأ: {e}")
    
    # تقرير النتائج
    print("\n" + "="*50)
    print("📊 تقرير إنشاء المستخدمين")
    print("="*50)
    
    print(f"✅ المستخدمون الناجحون: {len(successful_users)}")
    for user in successful_users:
        project_info = f" - {user['project_id']}" if user['project_id'] else " - مدير عام"
        print(f"   👤 {user['username']} ({user['user_type']}){project_info}")
    
    if failed_users:
        print(f"\n❌ المستخدمون الفاشلون: {len(failed_users)}")
        for user in failed_users:
            print(f"   👤 {user['username']}")
    
    print("\n🎮 يمكنك الآن اختبار تسجيل الدخول بالمستخدمين التاليين:")
    print("="*50)
    print("🔐 بيانات تسجيل الدخول:")
    
    for user in successful_users:
        project_desc = ""
        if user['user_type'] == 'admin':
            project_desc = " (يرى جميع العمليات)"
        else:
            project_desc = f" (يرى عمليات {user['project_id']} فقط)"
            
        print(f"   👤 المستخدم: {user['username']}")
        print(f"   🔑 كلمة المرور: {user['password']}")
        print(f"   🏷️ النوع: {user['user_type']}{project_desc}")
        print("   " + "-"*30)
    
    print("\n💡 لاختبار النظام:")
    print("1. شغل python main_with_auth.py")
    print("2. سجل دخول بأحد المستخدمين أعلاه") 
    print("3. اضغط على 'بحث في سجل العمليات'")
    print("4. لاحظ الفرق في البيانات المعروضة حسب نوع المستخدم")
    print("="*50)
    
    return len(successful_users) > 0

def main():
    """الدالة الرئيسية"""
    
    try:
        success = create_test_users()
        
        if success:
            print("\n🎉 تم إنشاء المستخدمين التجريبيين بنجاح!")
        else:
            print("\n❌ فشل في إنشاء المستخدمين!")
            
    except KeyboardInterrupt:
        print("\n⏹️ تم إيقاف العملية")
    except Exception as e:
        print(f"\n❌ خطأ غير متوقع: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()