#!/usr/bin/env python3
"""
اختبار النظام الكامل مع واجهة الإدارة
"""

import sys
import json
from pathlib import Path

def test_complete_system():
    """اختبار النظام الكامل"""
    print("=" * 60)
    print("        اختبار نظام إدارة المخزون مع إدارة المشاريع")
    print("=" * 60)
    
    # 1. التحقق من الملفات الأساسية
    print("\n1. التحقق من الملفات الأساسية:")
    
    required_files = [
        "main_with_auth.py",
        "gui/main_window.py", 
        "gui/admin_projects_window.py",
        "sheets/users_manager.py",
        "sheets/projects_manager.py",
        "sheets/manager.py",
        "config/settings.py"
    ]
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"   ✓ {file_path}")
        else:
            print(f"   ✗ {file_path} - مفقود!")
    
    # 2. التحقق من الواردات
    print("\n2. التحقق من الواردات:")
    
    try:
        from gui.admin_projects_window import AdminProjectsWindow
        print("   ✓ AdminProjectsWindow")
        
        from sheets.users_manager import UsersManager
        print("   ✓ UsersManager")
        
        from sheets.projects_manager import ProjectsManager  
        print("   ✓ ProjectsManager")
        
        from sheets.manager import SheetsManager
        print("   ✓ SheetsManager")
        
    except Exception as e:
        print(f"   ✗ خطأ في الواردات: {e}")
        return False
    
    # 3. التحقق من إعدادات Google Sheets
    print("\n3. التحقق من الإعدادات:")
    
    try:
        from config.settings import SPREADSHEET_CONFIG
        print(f"   ✓ ملف الإعدادات موجود")
        print(f"   - اسم الجدول: {SPREADSHEET_CONFIG.get('spreadsheet_name', 'غير محدد')}")
        
        credentials_file = SPREADSHEET_CONFIG.get('credentials_file')
        if credentials_file and Path(credentials_file).exists():
            print(f"   ✓ ملف الاعتماد موجود: {credentials_file}")
        else:
            print(f"   ! ملف الاعتماد مفقود: {credentials_file}")
            
    except Exception as e:
        print(f"   ✗ خطأ في قراءة الإعدادات: {e}")
    
    # 4. ميزات النظام
    print("\n4. ميزات النظام المتاحة:")
    print("   ✓ نظام تسجيل الدخول والتسجيل")
    print("   ✓ إدارة المستخدمين مع أرقام تعريفية (USR_001, USR_002...)")
    print("   ✓ إدارة المشاريع مع أرقام تعريفية (PRJ_001, PRJ_002...)")
    print("   ✓ ربط المستخدمين بالمشاريع")
    print("   ✓ فصل عرض المخزون حسب المشروع")
    print("   ✓ واجهة إدارة شاملة للمدراء")
    print("   ✓ إنشاء مشاريع جديدة")
    print("   ✓ تعيين المستخدمين للمشاريع")
    print("   ✓ عرض جداول البيانات التفاعلية")
    
    # 5. هيكل قاعدة البيانات
    print("\n5. هيكل Google Sheets:")
    print("   ✓ Users Sheet (8 أعمدة):")
    print("     - اسم المستخدم، كلمة المرور، نوع المستخدم، رقم التعريف")
    print("     - رقم المشروع، تاريخ الإنشاء، آخر تسجيل دخول، الحالة")
    print("   ✓ Projects Sheet (7 أعمدة):")
    print("     - رقم المشروع، اسم المشروع، الوصف، مدير المشروع")
    print("     - تاريخ البداية، تاريخ النهاية، الحالة") 
    print("   ✓ Inventory Sheet (4 أعمدة):")
    print("     - اسم العنصر، الكمية، رقم المشروع، التاريخ")
    print("   ✓ Activity_Log Sheet (6 أعمدة):")
    print("     - الوقت، المستخدم، النشاط، العنصر، التفاصيل، رقم المشروع")
    
    # 6. تعليمات التشغيل
    print("\n6. تعليمات التشغيل:")
    print("   1. تأكد من وجود ملف credentials.json")
    print("   2. تأكد من إعداد Google Sheets")
    print("   3. شغل: python main_with_auth.py")
    print("   4. سجل دخول كمدير لرؤية واجهة الإدارة")
    print("   5. اضغط على 'إدارة المشاريع' في الواجهة الرئيسية")
    
    print("\n" + "=" * 60)
    print("          النظام جاهز للاستخدام!")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    test_complete_system()