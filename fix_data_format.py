#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إصلاح تنسيق البيانات في Google Sheets لتتطابق مع توقعات البرنامج
"""

import os
import sys
from datetime import datetime, timedelta

# إضافة مسار المشروع
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sheets.manager import SheetsManager
from sheets.users_manager import UsersManager
from sheets.projects_manager import ProjectsManager

def fix_data_format():
    """إصلاح تنسيق البيانات لتتطابق مع توقعات البرنامج"""
    
    print("🔧 بدء إصلاح تنسيق البيانات...")
    
    # التأكد من وجود ملف الاعتماد
    if not os.path.exists('config/credentials.json'):
        print("❌ ملف credentials.json غير موجود")
        return False
    
    try:
        # إنشاء المديرين
        sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
        
        print("📡 الاتصال بـ Google Sheets...")
        
        if not sheets_manager.connect():
            print("❌ فشل في الاتصال بـ Google Sheets")
            return False
        
        print("✅ تم الاتصال بنجاح")
        
        # إصلاح رؤوس شيت المخزون
        print("🔧 إصلاح رؤوس شيت المخزون...")
        correct_headers = ["اسم العنصر", "التصنيف", "الكمية المتاحة", "رقم المشروع", "آخر تحديث"]
        sheets_manager.worksheet.update('A1:E1', [correct_headers])
        print("✅ تم تحديث رؤوس شيت المخزون")
        
        # إضافة بيانات اختبار منظمة
        print("📦 إضافة بيانات اختبار جديدة...")
        
        today = datetime.now()
        
        # بيانات منظمة للاختبار
        test_data = [
            # [اسم العنصر, التصنيف, الكمية المتاحة, رقم المشروع, آخر تحديث]
            ["أسمنت أبيض", "مواد البناء", "100", "PRJ_001", today.strftime('%Y-%m-%d %H:%M:%S')],
            ["طوب أحمر", "مواد البناء", "500", "PRJ_001", (today - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')],
            ["رمل خشن", "مواد البناء", "50", "PRJ_002", (today - timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S')],
            ["كابل كهرباء 2.5 مم", "أدوات كهربائية", "200", "PRJ_001", (today - timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S')],
            ["مفاتيح كهربائية", "أدوات كهربائية", "75", "PRJ_002", (today - timedelta(days=4)).strftime('%Y-%m-%d %H:%M:%S')],
            ["أنابيب PVC", "أدوات سباكة", "30", "PRJ_001", (today - timedelta(days=5)).strftime('%Y-%m-%d %H:%M:%S')],
            ["صنابير مياه", "أدوات سباكة", "15", "PRJ_002", (today - timedelta(days=6)).strftime('%Y-%m-%d %H:%M:%S')],
            ["مفك براغي", "أدوات عامة", "25", "", (today - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')],
            ["شريط قياس", "أدوات عامة", "10", "", (today - timedelta(days=8)).strftime('%Y-%m-%d %H:%M:%S')],
            ["مسامير حديد", "مواد البناء", "0", "PRJ_001", (today - timedelta(days=9)).strftime('%Y-%m-%d %H:%M:%S')],  # كمية صفر للاختبار
        ]
        
        # مسح البيانات القديمة (الاحتفاظ بالرؤوس)
        all_values = sheets_manager.worksheet.get_all_values()
        if len(all_values) > 1:
            range_to_clear = f"A2:E{len(all_values)}"
            sheets_manager.worksheet.batch_clear([range_to_clear])
            print("🧹 تم مسح البيانات القديمة")
        
        # إضافة البيانات الجديدة
        if test_data:
            start_row = 2
            end_row = start_row + len(test_data) - 1
            range_to_update = f"A{start_row}:E{end_row}"
            
            sheets_manager.worksheet.update(range_to_update, test_data)
            print(f"✅ تم إضافة {len(test_data)} عنصر جديد")
        
        # اختبار قراءة البيانات
        print("🧪 اختبار قراءة البيانات...")
        items = sheets_manager.get_all_items()
        print(f"📊 تم قراءة {len(items)} عنصر")
        
        if items:
            print("📋 أول 3 عناصر:")
            for i, item in enumerate(items[:3]):
                print(f"   {i+1}. {item['item_name']} - الكمية: {item['quantity']} - المشروع: {item['project_id']}")
        
        # اختبار البيانات الخام للفلاتر
        print("🧪 اختبار البيانات الخام...")
        raw_items = sheets_manager.get_all_items_raw()
        print(f"📊 تم قراءة {len(raw_items)} عنصر (خام)")
        
        if raw_items:
            print("📋 أول 3 عناصر (خام):")
            for i, item in enumerate(raw_items[:3]):
                if len(item) >= 3:
                    print(f"   {i+1}. {item[0]} - الكمية: {item[2]} - المشروع: {item[3] if len(item) > 3 else 'غير محدد'}")
        
        print("🎉 تم إصلاح تنسيق البيانات بنجاح!")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في إصلاح البيانات: {e}")
        import traceback
        traceback.print_exc()
        return False

def verify_filter_functionality():
    """التحقق من عمل الفلاتر مع البيانات المصححة"""
    
    print("\n" + "="*60)
    print("🔍 اختبار وظائف الفلاتر...")
    
    try:
        sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
        
        if not sheets_manager.connect():
            print("❌ فشل في الاتصال للاختبار")
            return False
        
        # اختبار البيانات المنظمة
        items = sheets_manager.get_all_items()
        raw_items = sheets_manager.get_all_items_raw()
        
        print(f"📊 البيانات المنظمة: {len(items)} عنصر")
        print(f"📊 البيانات الخام: {len(raw_items)} عنصر")
        
        # اختبار فلترة بالمشروع
        project_items = [item for item in items if item.get('project_id') == 'PRJ_001']
        print(f"🎯 عناصر مشروع PRJ_001: {len(project_items)}")
        
        # اختبار فلترة بالتصنيف
        building_items = [item for item in items if item.get('category') == 'مواد البناء']
        print(f"🏗️ عناصر مواد البناء: {len(building_items)}")
        
        # اختبار فلترة بالكمية
        zero_quantity_items = [item for item in items if item.get('quantity', 0) == 0]
        positive_quantity_items = [item for item in items if item.get('quantity', 0) > 0]
        print(f"📦 عناصر بكمية صفر: {len(zero_quantity_items)}")
        print(f"📦 عناصر بكمية موجبة: {len(positive_quantity_items)}")
        
        if zero_quantity_items:
            print(f"   🔍 مثال كمية صفر: {zero_quantity_items[0]['item_name']}")
        
        if positive_quantity_items:
            print(f"   🔍 مثال كمية موجبة: {positive_quantity_items[0]['item_name']} (الكمية: {positive_quantity_items[0]['quantity']})")
        
        print("✅ اختبار الفلاتر مكتمل")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار الفلاتر: {e}")
        return False

if __name__ == "__main__":
    print("🚀 بدء إصلاح تنسيق البيانات...")
    
    # إصلاح التنسيق
    if fix_data_format():
        # اختبار الفلاتر
        verify_filter_functionality()
        
        print("\n" + "="*60)
        print("🎯 النتيجة النهائية:")
        print("✅ تم إصلاح تنسيق البيانات")
        print("✅ تم اختبار وظائف الفلاتر")
        print("📱 يمكنك الآن تشغيل البرنامج واختبار الفلاتر")
        print("="*60)
    else:
        print("❌ فشل في إصلاح البيانات")