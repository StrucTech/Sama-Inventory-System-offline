#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار سريع للفلاتر لحل المشكلة
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from enhanced_sheets_manager import EnhancedSheetsManager
from config.settings import load_config

def test_filters_debug():
    """اختبار تفصيلي للفلاتر"""
    print("🔍 اختبار تفصيلي للفلاتر...")
    
    try:
        # تحميل الإعدادات
        config = load_config()
        if not config:
            print("❌ فشل في تحميل الإعدادات")
            return
        
        # إنشاء المدير المحسن
        enhanced_manager = EnhancedSheetsManager(
            config['credentials_file'],
            config['spreadsheet_name'],
            config['worksheet_name']
        )
        
        if not enhanced_manager.connect():
            print("❌ فشل في الاتصال")
            return
        
        # تحميل جميع البيانات
        all_data = enhanced_manager.get_activity_log_new_format()
        print(f"📊 إجمالي البيانات: {len(all_data)} سجل")
        
        if not all_data:
            print("❌ لا توجد بيانات")
            return
        
        # عرض عينة من البيانات
        print("\n📋 عينة من البيانات:")
        for i, record in enumerate(all_data[:3]):
            print(f"   {i+1}. التاريخ: {record[0]}, العملية: {record[2]}, العنصر: {record[3]}, التصنيف: {record[4]}")
        
        # جمع القيم الفريدة
        operations = set()
        items = set()
        categories = set()
        
        for record in all_data:
            if len(record) >= 5:
                operations.add(record[2].strip())
                items.add(record[3].strip())
                categories.add(record[4].strip())
        
        print(f"\n📈 التحليل:")
        print(f"   🔄 أنواع العمليات: {sorted(operations)}")
        print(f"   📦 العناصر: {len(items)} عنصر مختلف")
        print(f"   📂 التصنيفات: {sorted(categories)}")
        
        # اختبار الفلاتر
        print("\n🧪 اختبار الفلاتر:")
        
        # فلتر العمليات
        if "إضافة" in operations:
            add_results = enhanced_manager.filter_activity_log_new(operation_type="إضافة")
            print(f"   ➕ فلتر 'إضافة': {len(add_results)} نتيجة")
        
        # فلتر العناصر
        first_item = list(items)[0] if items else None
        if first_item:
            # اختبار البحث الجزئي
            partial_search = first_item[:5] if len(first_item) > 5 else first_item
            item_results = enhanced_manager.filter_activity_log_new(item_name=partial_search)
            print(f"   📦 فلتر '{partial_search}': {len(item_results)} نتيجة")
            
            # اختبار البحث الكامل
            full_item_results = enhanced_manager.filter_activity_log_new(item_name=first_item)
            print(f"   📦 فلتر '{first_item}' (كامل): {len(full_item_results)} نتيجة")
        
        # فلتر التصنيفات
        first_category = list(categories)[0] if categories else None
        if first_category:
            cat_results = enhanced_manager.filter_activity_log_new(category=first_category)
            print(f"   📂 فلتر '{first_category}': {len(cat_results)} نتيجة")
        
        # فلتر مركب
        print("\n🔗 اختبار الفلتر المركب:")
        combined = enhanced_manager.filter_activity_log_new(
            operation_type="إضافة" if "إضافة" in operations else None,
            date_from="2025-11-01",
            date_to="2025-11-30"
        )
        print(f"   🔄+📅 إضافة + نوفمبر 2025: {len(combined)} نتيجة")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_filters_debug()