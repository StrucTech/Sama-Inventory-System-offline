#!/usr/bin/env python3
"""
اختبار نظام التحديث الجديد
"""

import sys
import os
import json
from datetime import datetime

# إضافة مسار المشروع
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from auto_updater import AutoUpdater

def test_update_modes():
    """اختبار أوضاع فحص التحديثات المختلفة"""
    
    print("🧪 اختبار نظام التحديث الجديد")
    print("=" * 50)
    
    # إنشاء كائن التحديث
    updater = AutoUpdater("test_update_config.json")
    
    print("\n📋 اختبار الأوضاع المختلفة:")
    
    # اختبار الوضع الدائم
    print("\n1️⃣ اختبار الوضع الدائم (always):")
    updater.set_check_mode("always")
    print(f"   الوضع الحالي: {updater.get_check_mode_info()}")
    print(f"   هل يحتاج فحص؟ {updater.should_check_for_updates()}")
    
    # اختبار الوضع اليومي
    print("\n2️⃣ اختبار الوضع اليومي (daily):")
    updater.set_check_mode("daily")
    print(f"   الوضع الحالي: {updater.get_check_mode_info()}")
    print(f"   هل يحتاج فحص؟ {updater.should_check_for_updates()}")
    
    # اختبار الوضع الأسبوعي
    print("\n3️⃣ اختبار الوضع الأسبوعي (weekly):")
    updater.set_check_mode("weekly")
    print(f"   الوضع الحالي: {updater.get_check_mode_info()}")
    print(f"   هل يحتاج فحص؟ {updater.should_check_for_updates()}")
    
    # اختبار الوضع اليدوي
    print("\n4️⃣ اختبار الوضع اليدوي (manual):")
    updater.set_check_mode("manual")
    print(f"   الوضع الحالي: {updater.get_check_mode_info()}")
    print(f"   هل يحتاج فحص؟ {updater.should_check_for_updates()}")
    
    # العودة للوضع الافتراضي (دائماً)
    print("\n5️⃣ العودة للوضع الافتراضي (always):")
    updater.set_check_mode("always")
    print(f"   الوضع الحالي: {updater.get_check_mode_info()}")
    print(f"   هل يحتاج فحص؟ {updater.should_check_for_updates()}")
    
    print("\n" + "=" * 50)
    print("✅ انتهى اختبار أوضاع التحديث")

def test_config_file():
    """اختبار ملف الإعدادات"""
    
    print("\n📄 اختبار ملف الإعدادات:")
    
    config_file = "test_update_config.json"
    
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print("   محتويات الملف:")
        for key, value in config.items():
            if key == 'last_check' and value:
                try:
                    check_date = datetime.fromisoformat(value)
                    print(f"   {key}: {check_date.strftime('%Y-%m-%d %H:%M:%S')}")
                except:
                    print(f"   {key}: {value}")
            else:
                print(f"   {key}: {value}")
    else:
        print("   ❌ ملف الإعدادات غير موجود")

def simulate_program_startup():
    """محاكاة بدء تشغيل البرنامج"""
    
    print("\n🚀 محاكاة بدء تشغيل البرنامج:")
    print("-" * 30)
    
    # إنشاء كائن التحديث (كما يحدث في البرنامج الفعلي)
    updater = AutoUpdater("test_update_config.json")
    
    print(f"📊 معلومات النظام:")
    print(f"   الإصدار الحالي: {updater.current_version}")
    print(f"   وضع الفحص: {updater.get_check_mode_info()}")
    print(f"   التحديث التلقائي: {'مفعل' if updater.auto_update else 'معطل'}")
    
    # محاكاة فحص التحديثات
    if updater.should_check_for_updates():
        print("\n🔍 سيتم فحص التحديثات...")
        # هنا يمكن استدعاء updater.check_for_updates()
        
        # محاكاة تحديث تاريخ آخر فحص
        updater.update_last_check_date()
        print("✅ تم تحديث تاريخ آخر فحص")
    else:
        print("\n⏱️ لا حاجة لفحص التحديثات الآن")

def cleanup_test_files():
    """تنظيف ملفات الاختبار"""
    
    test_files = ["test_update_config.json"]
    
    for file_path in test_files:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"🧹 تم حذف ملف الاختبار: {file_path}")

def main():
    """الدالة الرئيسية"""
    
    try:
        # تشغيل الاختبارات
        test_update_modes()
        test_config_file()
        simulate_program_startup()
        
        print("\n" + "=" * 50)
        print("🎉 جميع الاختبارات تمت بنجاح!")
        
        # تنظيف الملفات
        print("\n🧹 تنظيف ملفات الاختبار...")
        cleanup_test_files()
        
    except Exception as e:
        print(f"\n❌ خطأ في الاختبار: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()