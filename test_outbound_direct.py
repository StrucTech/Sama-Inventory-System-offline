#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test outbound operation with recipient name in details - Direct Test.
اختبار مباشر لعملية إخراج مع اسم المستلم في التفاصيل
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sheets.manager import SheetsManager

def test_outbound_operation():
    """Test outbound operation with recipient name."""
    
    print("🧪 اختبار مباشر لعملية الإخراج مع اسم المستلم")
    print("=" * 60)
    
    # Initialize sheets manager
    sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
    sheets_manager.current_user = 'مطور_النظام'
    sheets_manager.current_project_id = 'PRJ_TEST_001'
    
    if not sheets_manager.connect():
        print("❌ فشل الاتصال بـ Google Sheets")
        return False
    
    print("✅ تم الاتصال بـ Google Sheets بنجاح")
    
    # Add a test item first
    print("\n📦 إضافة عنصر للاختبار...")
    success = sheets_manager.add_item(
        item_name='اختبار_إخراج_المستلم',
        category='اختبار',
        quantity=25,
        project_id='PRJ_TEST_001'
    )
    
    if not success:
        print("❌ فشل في إضافة العنصر")
        return False
    
    print("✅ تم إضافة العنصر بنجاح")
    
    # Find the added item
    all_items = sheets_manager.get_all_items()
    test_item = None
    test_row = None
    
    for i, item in enumerate(all_items):
        if item.get('item_name') == 'اختبار_إخراج_المستلم':
            test_item = item
            test_row = i + 2
            break
    
    if not test_item:
        print("❌ لم يتم العثور على العنصر المضاف")
        return False
    
    print(f"📋 العنصر: {test_item['item_name']}")
    print(f"   الكمية: {test_item['quantity']}")
    print(f"   الصف: {test_row}")
    
    # Test outbound operation
    print(f"\n🔄 اختبار عملية الإخراج...")
    recipient_name = 'مؤسسة الاختبار التقني'
    outbound_quantity = 8
    
    print(f"   الكمية المخرجة: {outbound_quantity}")
    print(f"   اسم المستلم: '{recipient_name}'")
    
    # Perform outbound
    success = sheets_manager.outbound_item(test_row, outbound_quantity, recipient_name)
    
    if success:
        print(f"✅ تم الإخراج بنجاح")
        
        # Wait for the operation to be logged
        import time
        time.sleep(2)
        
        # Check activity log
        try:
            activity_sheet = sheets_manager.spreadsheet.worksheet('Activity_Log_v2_20251108')
            data = activity_sheet.get_all_values()
            
            if data and len(data) > 1:
                last_record = data[-1]
                headers = data[0]
                
                print(f"\n📝 آخر سجل في Activity Log:")
                
                record_dict = {}
                for i, (header, value) in enumerate(zip(headers, last_record)):
                    if i < len(last_record):
                        record_dict[header] = value
                        print(f"   {header}: {value}")
                
                # Specific checks
                print(f"\n🔍 فحص النتائج:")
                
                # Check operation type
                operation_type = record_dict.get('نوع العملية', '')
                if operation_type == 'إخراج':
                    print(f"   ✅ نوع العملية صحيح: '{operation_type}'")
                else:
                    print(f"   ❌ نوع العملية خاطئ: '{operation_type}'")
                
                # Check item name
                logged_item = record_dict.get('اسم العنصر', '')
                if logged_item == 'اختبار_إخراج_المستلم':
                    print(f"   ✅ اسم العنصر صحيح: '{logged_item}'")
                else:
                    print(f"   ❌ اسم العنصر خاطئ: '{logged_item}'")
                
                # Check quantity removed
                quantity_removed = record_dict.get('الكمية المخرجة', '')
                if quantity_removed == str(outbound_quantity):
                    print(f"   ✅ الكمية المخرجة صحيحة: {quantity_removed}")
                else:
                    print(f"   ❌ الكمية المخرجة خاطئة: '{quantity_removed}' (متوقع: {outbound_quantity})")
                
                # Check user name (should contain recipient)
                logged_user = record_dict.get('اسم المستخدم', '')
                print(f"   📌 اسم المستخدم المسجل: '{logged_user}'")
                
                # Check details (main focus)
                details = record_dict.get('التفاصيل', '')
                print(f"   📋 التفاصيل: '{details}'")
                
                # Check if recipient name is in details
                if recipient_name in details:
                    print(f"   ✅ اسم المستلم '{recipient_name}' موجود في التفاصيل")
                else:
                    print(f"   ❌ اسم المستلم '{recipient_name}' غير موجود في التفاصيل")
                
                # Check expected format
                expected_start = f"إخراج بضاعة إلى: {recipient_name}"
                if details.startswith(expected_start):
                    print(f"   ✅ صيغة التفاصيل صحيحة - تبدأ بـ: '{expected_start}'")
                else:
                    print(f"   ❌ صيغة التفاصيل غير صحيحة")
                    print(f"   المتوقع أن تبدأ بـ: '{expected_start}'")
                
                # Check if details contain quantity info
                if f"الكمية المخرجة: {outbound_quantity}" in details:
                    print(f"   ✅ التفاصيل تحتوي على الكمية المخرجة")
                else:
                    print(f"   ❌ التفاصيل لا تحتوي على الكمية المخرجة")
                
                print(f"\n🎯 خلاصة الاختبار:")
                if (recipient_name in details and 
                    details.startswith(expected_start) and
                    operation_type == 'إخراج'):
                    print(f"   ✅ جميع الفحوصات نجحت - الميزة تعمل بشكل صحيح!")
                else:
                    print(f"   ❌ بعض الفحوصات فشلت - تحتاج مراجعة")
                
            else:
                print("❌ لا توجد سجلات في Activity Log")
                
        except Exception as e:
            print(f"❌ خطأ في فحص Activity Log: {e}")
            import traceback
            traceback.print_exc()
        
    else:
        print(f"❌ فشل في الإخراج")
    
    return True

if __name__ == "__main__":
    try:
        test_outbound_operation()
        
    except KeyboardInterrupt:
        print("\n⏹️ تم إيقاف الاختبار بواسطة المستخدم")
    except Exception as e:
        print(f"\n❌ خطأ في الاختبار: {e}")
        import traceback
        traceback.print_exc()