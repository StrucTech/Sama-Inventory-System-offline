#!/usr/bin/env python3
"""
اختبار مبسط للبيانات والفلاتر
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sheets.manager import SheetsManager

print("📊 بدء اختبار البيانات الأساسية...")

# إعداد SheetsManager
sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')

if sheets_manager.connect():
    print("✅ تم الاتصال بـ Google Sheets")
    
    # تحميل البيانات
    try:
        inventory_data = sheets_manager.get_all_items_raw()
        print(f"\n📦 إجمالي عناصر المخزون: {len(inventory_data)}")
        
        if inventory_data:
            print("\n🔍 عينة من البيانات (أول 5 عناصر):")
            for i, item in enumerate(inventory_data[:5]):
                print(f"   {i+1}. {item}")
            
            # تحليل البيانات
            categories = set()
            items = set()
            projects = set()
            
            for item in inventory_data:
                if len(item) >= 4:
                    if item[0]:  # اسم العنصر
                        items.add(item[0])
                    if item[1]:  # التصنيف
                        categories.add(item[1])
                    if item[3]:  # المشروع
                        projects.add(item[3])
            
            print(f"\n📋 التصنيفات الموجودة ({len(categories)}):")
            for cat in sorted(categories):
                print(f"   • {cat}")
            
            print(f"\n📦 العناصر الموجودة ({len(items)}):")
            for item in sorted(list(items)[:10]):  # أول 10
                print(f"   • {item}")
            if len(items) > 10:
                print(f"   ... و {len(items) - 10} عنصر آخر")
                
            print(f"\n🏗️ المشاريع الموجودة ({len(projects)}):")
            for proj in sorted(projects):
                print(f"   • {proj}")
                
        else:
            print("⚠️ لا توجد بيانات في المخزون")
            
    except Exception as e:
        print(f"❌ خطأ في تحميل البيانات: {e}")
        import traceback
        traceback.print_exc()
        
    # اختبار سجل النشاط
    try:
        if hasattr(sheets_manager, 'get_activity_log'):
            activity_data = sheets_manager.get_activity_log()
            print(f"\n📊 إجمالي إدخالات سجل النشاط: {len(activity_data)}")
            
            if activity_data:
                print("\n🔍 عينة من سجل النشاط (أول 3 إدخالات):")
                for i, log in enumerate(activity_data[:3]):
                    print(f"   {i+1}. {log}")
        else:
            print("\n⚠️ سجل النشاط غير متاح")
            
    except Exception as e:
        print(f"⚠️ خطأ في تحميل سجل النشاط: {e}")
        
else:
    print("❌ فشل الاتصال بـ Google Sheets")
    
print("\n✅ انتهى اختبار البيانات")