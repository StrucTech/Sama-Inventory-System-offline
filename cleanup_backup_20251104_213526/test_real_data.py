#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار لجلب عينة من البيانات الفعلية من Google Sheets
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sheets.manager import SheetsManager
import json

def test_real_data():
    """اختبار البيانات الحقيقية من Google Sheets"""
    
    try:
        # تحميل الإعدادات
        with open('config/config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # إنشاء مدير الشيتس
        credentials_file = config.get('credentials_file', 'config/credentials.json')
        spreadsheet_name = config.get('spreadsheet_name', 'Inventory Management')
        
        sheets_manager = SheetsManager(credentials_file, spreadsheet_name)
        
        print("🔗 محاولة الاتصال بـ Google Sheets...")
        
        # جلب بيانات المخزون مباشرة للاختبار
        print("\n📦 جلب بيانات المخزون:")
        all_items = sheets_manager.get_all_items_raw()
        print(f"عدد العناصر: {len(all_items)}")
        
        # عرض أول 5 عناصر
        print("\n📋 أول 5 عناصر:")
        for i, item in enumerate(all_items[:5]):
            print(f"  {i+1}. {item}")
        
        # جلب سجل النشاط
        print("\n📊 جلب سجل النشاط:")
        activity_log = sheets_manager.get_activity_log()
        print(f"عدد الإدخالات: {len(activity_log)}")
        
        # عرض أول 5 إدخالات
        print("\n📋 أول 5 إدخالات من سجل النشاط:")
        for i, log in enumerate(activity_log[:5]):
            print(f"  {i+1}. {log}")
        
        # تحليل أسماء العناصر الفريدة
        print("\n🏷️ أسماء العناصر الفريدة:")
        unique_items = set()
        for item in all_items:
            if len(item) > 0 and item[0]:
                unique_items.add(item[0])
        
        for item_name in sorted(list(unique_items))[:10]:
            print(f"  - {item_name}")
        
        # تحليل التصنيفات الفريدة
        print("\n📂 التصنيفات الفريدة:")
        unique_categories = set()
        for item in all_items:
            if len(item) > 1 and item[1]:
                unique_categories.add(item[1])
        
        for category in sorted(list(unique_categories)):
            print(f"  - {category}")
        
        print(f"\n✅ إجمالي العناصر الفريدة: {len(unique_items)}")
        print(f"✅ إجمالي التصنيفات الفريدة: {len(unique_categories)}")
        
    except Exception as e:
        print(f"❌ خطأ: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_real_data()