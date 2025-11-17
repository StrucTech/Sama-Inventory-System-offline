#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار عرض العناصر للمستخدمين العاديين
"""

from sheets.manager import SheetsManager

def test_user_items():
    # تحميل البيانات
    sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')

    if sheets_manager.connect():
        print('✅ تم الاتصال بـ Google Sheets')
        
        # جلب جميع العناصر
        all_items = sheets_manager.get_all_items()
        print(f'\n📦 إجمالي العناصر: {len(all_items)}')
        
        # عرض كل عنصر مع تفاصيله
        for item in all_items:
            print(f'\n🔍 العنصر: {item["item_name"]}')
            print(f'  التصنيف: {item["category"]}')
            print(f'  المشروع: {item["project_id"]}')
            print(f'  الكمية: {item["quantity"]}')
            print(f'  آخر تحديث: {item["last_updated"]}')
        
        # اختبار فلترة المشروع
        print('\n🔍 اختبار فلترة المشروع PRJ_002...')
        project_items = sheets_manager.get_items_by_project('PRJ_002')
        print(f'عناصر PRJ_002: {len(project_items)}')
        
        for item in project_items:
            print(f'  - {item["item_name"]} (الكمية: {item["quantity"]})')
            
        # اختبار المشروع التجريبي
        print('\n🧪 اختبار فلترة المشروع PRJ_TEST_001...')
        test_project_items = sheets_manager.get_items_by_project('PRJ_TEST_001')
        print(f'عناصر PRJ_TEST_001: {len(test_project_items)}')
        
        for item in test_project_items:
            print(f'  - {item["item_name"]} (الكمية: {item["quantity"]})')
            
    else:
        print('❌ فشل في الاتصال')

if __name__ == "__main__":
    test_user_items()