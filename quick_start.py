"""
سكريبت البدء السريع
فحص النظام وتشغيله بأمان
"""

import os
import sys
import json
from datetime import datetime

def quick_system_check():
    """فحص سريع للنظام"""
    print("🚀 فحص سريع للنظام...")
    
    issues = []
    
    # فحص الملفات الأساسية
    required_files = [
        'main_with_auth.py',
        'config/config.json', 
        'gui/main_window.py',
        'sheets/manager.py'
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            issues.append(f"ملف مفقود: {file}")
    
    # فحص الإعدادات
    try:
        with open('config/config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        if 'spreadsheet_name' not in config:
            issues.append("اسم الجدول غير محدد في الإعدادات")
    except:
        issues.append("خطأ في قراءة ملف الإعدادات")
    
    # فحص الأمان
    if not os.path.exists('.gitignore'):
        issues.append("ملف .gitignore مفقود")
    
    return issues

def start_system_safely():
    """تشغيل النظام بأمان"""
    print("🎯 نظام إدارة المخزون Sama - البدء السريع")
    print("=" * 50)
    
    # فحص سريع
    issues = quick_system_check()
    
    if issues:
        print("⚠️ مشاكل مكتشفة:")
        for issue in issues:
            print(f"   • {issue}")
        
        print("\n🔧 يُنصح بحل هذه المشاكل أولاً")
        
        choice = input("\nهل تريد المتابعة على أي حال؟ (y/n): ")
        if choice.lower() != 'y':
            print("تم إيقاف التشغيل")
            return False
    else:
        print("✅ جميع الفحوصات نجحت")
    
    print("\n🚀 بدء تشغيل النظام...")
    
    try:
        # محاولة تشغيل النظام
        os.system('python main_with_auth.py')
        return True
    except Exception as e:
        print(f"❌ خطأ في التشغيل: {e}")
        return False

if __name__ == "__main__":
    start_system_safely()
