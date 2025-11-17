#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for the fixed double logging and negative quantity placement.
اختبار إصلاح التسجيل المزدوج ووضع الفرق السالب في الكمية المضافة
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sheets.manager import SheetsManager

def test_quantity_edit_logging():
    """Test the fixed logging system for quantity edits."""
    
    print("🧪 اختبار إصلاح تسجيل تعديل الكميات")
    print("=" * 60)
    
    # Initialize sheets manager
    sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
    sheets_manager.current_user = "مطور_النظام"
    sheets_manager.current_project_id = "PRJ_TEST_001"
    
    if not sheets_manager.connect():
        print("❌ فشل الاتصال بـ Google Sheets")
        return False
    
    print("✅ تم الاتصال بـ Google Sheets بنجاح")
    
    # Get current inventory data
    all_items = sheets_manager.get_all_items()
    
    if not all_items:
        print("❌ لا توجد عناصر في المخزن للاختبار")
        return False
    
    # Find a test item or use the first item
    test_item = None
    test_row = None
    
    for i, item in enumerate(all_items):
        if item.get('item_name', '').startswith('test'):
            test_item = item
            test_row = i + 2  # +2 because enumerate starts at 0 and we skip header
            break
    
    if not test_item:
        # Use first item if no test item found
        test_item = all_items[0]
        test_row = 2  # First data row (after header)
    
    print(f"\n📋 عنصر الاختبار: {test_item['item_name']}")
    print(f"   الكمية الحالية: {test_item['quantity']}")
    print(f"   رقم الصف: {test_row}")
    
    # Get activity log count before test
    try:
        activity_sheet = sheets_manager.spreadsheet.worksheet('Activity_Log_v2_20251108')
        before_data = activity_sheet.get_all_values()
        before_count = len(before_data) - 1  # excluding header
        print(f"   عدد سجلات Activity Log قبل الاختبار: {before_count}")
    except Exception as e:
        print(f"   ❌ خطأ في قراءة Activity Log: {e}")
        return False
    
    original_quantity = float(test_item['quantity'])
    
    # Test scenario: reduce quantity by 10
    new_quantity = original_quantity - 10
    
    print(f"\n🔄 اختبار التعديل:")
    print(f"   من: {original_quantity} إلى: {new_quantity}")
    print(f"   الفرق المتوقع: {new_quantity - original_quantity}")
    
    # Perform update
    success = sheets_manager.update_quantity(test_row, new_quantity)
    
    if success:
        print(f"   ✅ تم التحديث بنجاح")
        
        # Check activity log after update
        try:
            import time
            time.sleep(2)  # Wait for update to be processed
            
            after_data = activity_sheet.get_all_values()
            after_count = len(after_data) - 1
            new_records = after_count - before_count
            
            print(f"\n📊 نتائج التحقق:")
            print(f"   عدد السجلات قبل: {before_count}")
            print(f"   عدد السجلات بعد: {after_count}")
            print(f"   السجلات الجديدة: {new_records}")
            
            if new_records == 1:
                print("   ✅ تم إضافة سجل واحد فقط (لا يوجد تسجيل مزدوج)")
                
                # Check the new record
                if after_data:
                    last_record = after_data[-1]
                    headers = after_data[0]
                    
                    print(f"\n📝 السجل الجديد:")
                    for i, (header, value) in enumerate(zip(headers, last_record)):
                        if i < len(last_record):
                            print(f"   {header}: {value}")
                    
                    # Check if quantity added contains the negative difference
                    if len(last_record) >= 6:
                        quantity_added = last_record[5]  # Column F (index 5)
                        quantity_removed = last_record[6]  # Column G (index 6)
                        
                        try:
                            added_val = float(quantity_added) if quantity_added else 0
                            removed_val = float(quantity_removed) if quantity_removed else 0
                            expected_diff = new_quantity - original_quantity
                            
                            print(f"\n🔍 تحليل الكميات:")
                            print(f"   الكمية المضافة المسجلة: {added_val}")
                            print(f"   الكمية المخرجة المسجلة: {removed_val}")
                            print(f"   الفرق المتوقع: {expected_diff}")
                            
                            if abs(added_val - expected_diff) < 0.001:
                                print("   ✅ الكمية المضافة تحتوي على الفرق الصحيح")
                            else:
                                print("   ❌ خطأ في تسجيل الفرق")
                            
                            if removed_val == 0:
                                print("   ✅ الكمية المخرجة صفر (صحيح)")
                            else:
                                print("   ❌ الكمية المخرجة ليست صفر")
                                
                        except ValueError:
                            print("   ⚠️ لا يمكن تحليل القيم الرقمية")
                
            elif new_records == 0:
                print("   ❌ لم يتم إضافة أي سجل!")
            else:
                print(f"   ❌ تم إضافة {new_records} سجل (يجب أن يكون واحد فقط)")
                
                # Show the new records
                if new_records > 0 and len(after_data) > before_count + 1:
                    print("\n📝 السجلات الجديدة:")
                    for i in range(new_records):
                        record_index = before_count + 1 + i
                        if record_index < len(after_data):
                            record = after_data[record_index]
                            print(f"   سجل {i+1}: {record[:4]}...")  # Show first 4 fields
            
        except Exception as e:
            print(f"   ❌ خطأ في فحص Activity Log: {e}")
            import traceback
            traceback.print_exc()
        
    else:
        print(f"   ❌ فشل في التحديث")
    
    return True

if __name__ == "__main__":
    try:
        test_quantity_edit_logging()
        
    except KeyboardInterrupt:
        print("\n⏹️ تم إيقاف الاختبار بواسطة المستخدم")
    except Exception as e:
        print(f"\n❌ خطأ في الاختبار: {e}")
        import traceback
        traceback.print_exc()