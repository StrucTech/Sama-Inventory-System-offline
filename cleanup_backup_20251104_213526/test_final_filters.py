#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار شامل ونهائي لنظام الفلاتر المحسن
"""

import tkinter as tk
from enhanced_sheets_manager import EnhancedSheetsManager
from new_filter_window import NewFilterSearchWindow
from config.settings import load_config

def test_final_system():
    """اختبار النظام النهائي"""
    print("🎯 اختبار النظام النهائي...")
    print("=" * 50)
    
    try:
        # تحميل الإعدادات
        print("0️⃣ تحميل الإعدادات...")
        config = load_config()
        if not config:
            print("❌ فشل في تحميل الإعدادات")
            return False
        print("   ✅ تم تحميل الإعدادات بنجاح")
        
        # اختبار 1: إنشاء المدير المحسن
        print("\n1️⃣ اختبار المدير المحسن...")
        enhanced_manager = EnhancedSheetsManager(
            credentials_file=config['credentials_file'],
            spreadsheet_name=config['spreadsheet_name'],
            worksheet_name=config['worksheet_name']
        )
        
        if not enhanced_manager.connect():
            print("❌ فشل في الاتصال بـ Google Sheets")
            return False
        print("   ✅ تم إنشاء المدير والاتصال بنجاح")
        
        # اختبار 2: تحميل البيانات
        print("\n2️⃣ اختبار تحميل البيانات...")
        data = enhanced_manager.get_activity_log_new_format()
        print(f"   ✅ تم تحميل {len(data)} سجل من الشيت الجديد")
        
        # اختبار 3: الفلترة
        print("\n3️⃣ اختبار وظائف الفلترة...")
        
        # فلتر بالتاريخ
        date_filtered = enhanced_manager.filter_activity_log_new(
            date_from="2025-11-01", date_to="2025-11-30"
        )
        print(f"   📅 فلتر التاريخ: {len(date_filtered)} نتيجة")
        
        # فلتر بنوع العملية
        operation_filtered = enhanced_manager.filter_activity_log_new(operation_type="إضافة")
        print(f"   🔄 فلتر العمليات: {len(operation_filtered)} نتيجة للإضافة")
        
        # فلتر بالعنصر
        if data:
            first_item = data[0][3] if len(data[0]) > 3 else None
            if first_item:
                item_filtered = enhanced_manager.filter_activity_log_new(item_name=first_item)
                print(f"   📦 فلتر العناصر: {len(item_filtered)} نتيجة للعنصر: {first_item[:20]}...")
        
        # اختبار 4: الإحصائيات
        print("\n4️⃣ اختبار الإحصائيات...")
        stats = enhanced_manager.get_statistics_new()
        print(f"   📊 إجمالي السجلات: {stats['total_records']}")
        print(f"   ➕ إجمالي المضاف: {stats['total_added']}")
        print(f"   ➖ إجمالي المخرج: {stats['total_removed']}")
        print(f"   🏗️ عدد المشاريع: {len(stats['projects_count'])}")
        
        # اختبار 5: واجهة الفلترة
        print("\n5️⃣ اختبار واجهة المستخدم...")
        root = tk.Tk()
        root.withdraw()  # إخفاء النافذة الرئيسية
        
        # إنشاء نافذة الفلترة
        filter_window = NewFilterSearchWindow(root, enhanced_manager)
        print("   ✅ تم إنشاء نافذة الفلترة بنجاح")
        
        # عرض تعليمات للمستخدم
        print("\n" + "=" * 50)
        print("🎉 النظام جاهز للاستخدام!")
        print("=" * 50)
        print("📋 اختبر الميزات التالية:")
        print("   1. 📅 اختيار التاريخ من التقويم")
        print("   2. 📝 اختيار العناصر من القائمة المنسدلة")
        print("   3. 🔍 البحث بنوع العملية")
        print("   4. 👤 البحث بالمستلم")
        print("   5. 🏗️ البحث بالمشروع")
        print("   6. 🗑️ مسح جميع الفلاتر")
        print("   7. 📊 مراجعة الإحصائيات التلقائية")
        print("=" * 50)
        
        # تشغيل الواجهة
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 بدء اختبار النظام المحسن...")
    print()
    
    success = test_final_system()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 جميع الاختبارات نجحت! النظام يعمل بشكل مثالي!")
    else:
        print("⚠️ فشل في بعض الاختبارات")
    print("=" * 50)