#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار تفصيلي جداً لكل فلتر على حدة
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from enhanced_sheets_manager import EnhancedSheetsManager
from config.settings import load_config

def detailed_filter_debug():
    """اختبار تفصيلي جداً لكل فلتر"""
    print("🔍 اختبار تفصيلي جداً للفلاتر...")
    print("=" * 80)
    
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
        
        # عرض هيكل البيانات
        print(f"\n📋 هيكل البيانات:")
        if all_data:
            sample = all_data[0]
            for i, value in enumerate(sample):
                print(f"   العمود {i}: '{value}' (نوع: {type(value).__name__})")
        
        # تحليل البيانات
        print(f"\n🔍 تحليل البيانات:")
        operations = {}
        items = {}
        categories = {}
        recipients = {}
        projects = {}
        
        for i, record in enumerate(all_data):
            if len(record) >= 12:
                op = record[2].strip() if record[2] else ""
                item = record[3].strip() if record[3] else ""
                cat = record[4].strip() if record[4] else ""
                recipient = record[9].strip() if len(record) > 9 and record[9] else ""
                project = record[10].strip() if len(record) > 10 and record[10] else ""
                
                operations[op] = operations.get(op, 0) + 1
                items[item] = items.get(item, 0) + 1
                categories[cat] = categories.get(cat, 0) + 1
                if recipient:
                    recipients[recipient] = recipients.get(recipient, 0) + 1
                if project:
                    projects[project] = projects.get(project, 0) + 1
        
        print(f"   🔄 العمليات المتاحة: {dict(operations)}")
        print(f"   📦 العناصر المتاحة: {list(items.keys())[:5]}... (إجمالي: {len(items)})")
        print(f"   📂 التصنيفات المتاحة: {list(categories.keys())}")
        print(f"   👤 المستلمين: {list(recipients.keys())[:3]}... (إجمالي: {len(recipients)})")
        print(f"   🏗️ المشاريع: {list(projects.keys())[:3]}... (إجمالي: {len(projects)})")
        
        # اختبار كل فلتر بشكل منفصل
        print(f"\n" + "="*80)
        print("🧪 اختبار الفلاتر بشكل منفصل:")
        print("="*80)
        
        # 1. اختبار فلتر العمليات
        print(f"\n1️⃣ اختبار فلتر العمليات:")
        for op_type in operations.keys():
            if op_type:  # تجاهل القيم الفارغة
                print(f"\n   🔍 اختبار: operation_type='{op_type}'")
                
                # استدعاء الفلتر
                filtered = enhanced_manager.filter_activity_log_new(operation_type=op_type)
                print(f"      📊 النتائج: {len(filtered)} من {len(all_data)}")
                
                # فحص يدوي
                manual_count = 0
                for record in all_data:
                    if len(record) >= 3 and record[2].strip() == op_type.strip():
                        manual_count += 1
                print(f"      ✅ فحص يدوي: {manual_count} سجل")
                
                if len(filtered) != manual_count:
                    print(f"      ❌ عدم تطابق! الفلتر: {len(filtered)}, اليدوي: {manual_count}")
        
        # 2. اختبار فلتر العناصر
        print(f"\n2️⃣ اختبار فلتر العناصر:")
        test_items = list(items.keys())[:3]  # أول 3 عناصر
        for item_name in test_items:
            if item_name:
                print(f"\n   🔍 اختبار: item_name='{item_name}'")
                
                # استدعاء الفلتر
                filtered = enhanced_manager.filter_activity_log_new(item_name=item_name)
                print(f"      📊 النتائج: {len(filtered)} من {len(all_data)}")
                
                # فحص يدوي
                manual_count = 0
                for record in all_data:
                    if len(record) >= 4 and item_name.lower().strip() in record[3].lower():
                        manual_count += 1
                print(f"      ✅ فحص يدوي: {manual_count} سجل")
                
                if len(filtered) != manual_count:
                    print(f"      ❌ عدم تطابق! الفلتر: {len(filtered)}, اليدوي: {manual_count}")
                    
                    # طباعة تفاصيل أكثر
                    print(f"      🔍 تفاصيل السجلات المطابقة:")
                    for i, record in enumerate(all_data):
                        if len(record) >= 4 and item_name.lower().strip() in record[3].lower():
                            print(f"         - السجل {i}: العنصر='{record[3]}'")
        
        # 3. اختبار فلتر التصنيفات
        print(f"\n3️⃣ اختبار فلتر التصنيفات:")
        for cat_name in categories.keys():
            if cat_name:
                print(f"\n   🔍 اختبار: category='{cat_name}'")
                
                # استدعاء الفلتر
                filtered = enhanced_manager.filter_activity_log_new(category=cat_name)
                print(f"      📊 النتائج: {len(filtered)} من {len(all_data)}")
                
                # فحص يدوي
                manual_count = 0
                for record in all_data:
                    if len(record) >= 5 and cat_name.lower().strip() in record[4].lower():
                        manual_count += 1
                print(f"      ✅ فحص يدوي: {manual_count} سجل")
                
                if len(filtered) != manual_count:
                    print(f"      ❌ عدم تطابق! الفلتر: {len(filtered)}, اليدوي: {manual_count}")
        
        # 4. اختبار فلتر التاريخ
        print(f"\n4️⃣ اختبار فلتر التاريخ:")
        print(f"\n   🔍 اختبار: date_from='2025-10-01', date_to='2025-12-31'")
        
        # استدعاء الفلتر
        filtered = enhanced_manager.filter_activity_log_new(
            date_from="2025-10-01", 
            date_to="2025-12-31"
        )
        print(f"      📊 النتائج: {len(filtered)} من {len(all_data)}")
        
        # فحص يدوي
        manual_count = 0
        for record in all_data:
            if len(record) >= 1 and record[0]:
                try:
                    from datetime import datetime
                    record_date = datetime.strptime(record[0], "%Y-%m-%d")
                    date_from_obj = datetime.strptime("2025-10-01", "%Y-%m-%d")
                    date_to_obj = datetime.strptime("2025-12-31", "%Y-%m-%d")
                    if date_from_obj <= record_date <= date_to_obj:
                        manual_count += 1
                except ValueError:
                    pass
        print(f"      ✅ فحص يدوي: {manual_count} سجل")
        
        # اختبار فلتر مركب
        print(f"\n5️⃣ اختبار فلتر مركب:")
        if operations and items:
            first_op = list(operations.keys())[0]
            first_item = list(items.keys())[0]
            
            print(f"\n   🔍 اختبار: operation_type='{first_op}' + item_name='{first_item}'")
            
            filtered = enhanced_manager.filter_activity_log_new(
                operation_type=first_op,
                item_name=first_item
            )
            print(f"      📊 النتائج: {len(filtered)} من {len(all_data)}")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    detailed_filter_debug()