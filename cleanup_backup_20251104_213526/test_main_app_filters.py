#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار الفلاتر في البرنامج الرئيسي main_with_auth.py
"""

import tkinter as tk
import sys
import os

# إضافة مسار المشروع
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import MainWindow
from config.settings import load_config
from enhanced_sheets_manager import EnhancedSheetsManager
from new_filter_window import NewFilterSearchWindow

def test_main_app_filters():
    """اختبار الفلاتر في التطبيق الرئيسي"""
    print("🧪 اختبار الفلاتر في البرنامج الرئيسي...")
    print("=" * 50)
    
    try:
        # تحميل الإعدادات
        print("1️⃣ تحميل الإعدادات...")
        config = load_config()
        if not config:
            print("❌ فشل في تحميل الإعدادات")
            return False
        print("   ✅ تم تحميل الإعدادات بنجاح")
        
        # إنشاء النافذة الرئيسية (بدون عرض)
        print("\n2️⃣ إنشاء النافذة الرئيسية...")
        root = tk.Tk()
        root.withdraw()  # إخفاء النافذة
        root.title("اختبار نظام إدارة المخزون")
        
        main_window = MainWindow(root, config)
        main_window.current_user = {"username": "admin", "role": "admin"}
        print("   ✅ تم إنشاء النافذة الرئيسية")
        
        # اختبار الاتصال
        print("\n3️⃣ اختبار الاتصال بـ Google Sheets...")
        if not main_window.sheets_manager:
            print("❌ لا يوجد اتصال بـ Google Sheets")
            return False
        print("   ✅ تم الاتصال بـ Google Sheets")
        
        # اختبار إنشاء المدير المحسن
        print("\n4️⃣ اختبار المدير المحسن...")
        enhanced_manager = EnhancedSheetsManager(
            main_window.sheets_manager.credentials_file,
            main_window.sheets_manager.spreadsheet_name,
            main_window.sheets_manager.worksheet_name
        )
        
        if not enhanced_manager.connect():
            print("❌ فشل في الاتصال بالمدير المحسن")
            return False
        print("   ✅ تم إنشاء المدير المحسن بنجاح")
        
        # اختبار تحميل البيانات
        print("\n5️⃣ اختبار تحميل البيانات...")
        data = enhanced_manager.get_activity_log_new_format()
        if not data:
            print("❌ لا توجد بيانات في الشيت الجديد")
            return False
        print(f"   ✅ تم تحميل {len(data)} سجل من الشيت الجديد")
        
        # اختبار الفلاتر
        print("\n6️⃣ اختبار وظائف الفلترة...")
        
        # فلتر بالعناصر
        if data:
            test_item = data[0][3] if len(data[0]) > 3 else None
            if test_item:
                filtered = enhanced_manager.filter_activity_log_new(item_name=test_item)
                print(f"   📦 فلتر العناصر: {len(filtered)} نتيجة للعنصر: {test_item[:20]}...")
            
        # فلتر بالعمليات
        add_filtered = enhanced_manager.filter_activity_log_new(operation_type="إضافة")
        print(f"   ➕ فلتر العمليات: {len(add_filtered)} نتيجة لعمليات الإضافة")
        
        # فلتر بالتاريخ
        date_filtered = enhanced_manager.filter_activity_log_new(
            date_from="2025-11-01", date_to="2025-11-30"
        )
        print(f"   📅 فلتر التاريخ: {len(date_filtered)} نتيجة في نوفمبر 2025")
        
        # اختبار نافذة الفلاتر
        print("\n7️⃣ اختبار نافذة الفلاتر...")
        try:
            # محاكاة فتح نافذة الفلاتر
            main_window.open_filter_search_window()
            print("   ✅ تم اختبار فتح نافذة الفلاتر بنجاح")
        except Exception as e:
            print(f"   ❌ خطأ في فتح نافذة الفلاتر: {e}")
            return False
        
        print("\n" + "=" * 50)
        print("🎉 جميع الاختبارات نجحت!")
        print("📋 النظام جاهز مع الفلاتر المحسنة")
        print("🔍 يمكنك الآن استخدام زر 'بحث بفلاتر' في البرنامج الرئيسي")
        print("=" * 50)
        
        # عرض النافذة للاختبار اليدوي
        print("\n📱 عرض النافذة للاختبار اليدوي...")
        print("   - سجل دخول بـ admin/admin")
        print("   - انقر على زر 'بحث بفلاتر'")
        print("   - اختبر جميع أنواع الفلاتر")
        
        root.deiconify()  # إظهار النافذة
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 بدء اختبار الفلاتر في البرنامج الرئيسي...")
    print()
    
    success = test_main_app_filters()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ الاختبار مكتمل!")
    else:
        print("❌ فشل في الاختبار")
    print("=" * 50)