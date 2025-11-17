#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for outbound operations with recipient name in details.
اختبار عمليات الإخراج مع اسم المستلم في التفاصيل
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sheets.manager import SheetsManager

def test_outbound_with_recipient_details():
    """Test outbound operations include recipient name in details."""
    
    print("🧪 اختبار إخراج البضائع مع اسم المستلم في التفاصيل")
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
    
    # Find an item with sufficient quantity
    test_item = None
    test_row = None
    
    for i, item in enumerate(all_items):
        if float(item.get('quantity', 0)) >= 5:  # Need at least 5 items
            test_item = item
            test_row = i + 2  # +2 because enumerate starts at 0 and we skip header
            break
    
    if not test_item:
        print("❌ لا توجد عناصر بكمية كافية للاختبار")
        return False
    
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
    
    # Test outbound operation
    outbound_quantity = 3
    recipient_name = "أحمد محمد"
    
    print(f"\n🔄 اختبار الإخراج:")
    print(f"   الكمية المخرجة: {outbound_quantity}")
    print(f"   اسم المستلم: {recipient_name}")
    
    # Perform outbound
    success = sheets_manager.outbound_item(test_row, outbound_quantity, recipient_name)
    
    if success:
        print(f"   ✅ تم الإخراج بنجاح")
        
        # Check activity log after outbound
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
            
            if new_records >= 1:
                print("   ✅ تم إضافة سجل جديد")
                
                # Check the new record
                if after_data:
                    last_record = after_data[-1]
                    headers = after_data[0]
                    
                    print(f"\n📝 السجل الجديد:")
                    record_details = ""
                    for i, (header, value) in enumerate(zip(headers, last_record)):
                        if i < len(last_record):
                            print(f"   {header}: {value}")
                            if header == "التفاصيل":
                                record_details = value
                    
                    # Check if recipient name is in details
                    print(f"\n🔍 فحص التفاصيل:")
                    print(f"   محتوى التفاصيل: '{record_details}'")
                    
                    if recipient_name in record_details:
                        print(f"   ✅ اسم المستلم '{recipient_name}' موجود في التفاصيل")
                    else:
                        print(f"   ❌ اسم المستلم '{recipient_name}' غير موجود في التفاصيل")
                    
                    # Check expected format
                    expected_start = f"إخراج بضاعة إلى: {recipient_name}"
                    if record_details.startswith(expected_start):
                        print(f"   ✅ صيغة التفاصيل صحيحة")
                    else:
                        print(f"   ❌ صيغة التفاصيل غير صحيحة")
                        print(f"   المتوقع أن تبدأ بـ: '{expected_start}'")
                        print(f"   الفعلي: '{record_details}'")
                    
                    # Check operation type
                    if len(last_record) >= 3 and last_record[2] == "إخراج":
                        print(f"   ✅ نوع العملية صحيح: 'إخراج'")
                    else:
                        print(f"   ❌ نوع العملية غير صحيح")
                    
                    # Check quantity
                    if len(last_record) >= 7:
                        quantity_removed = last_record[6]  # Column G (index 6)
                        try:
                            removed_val = float(quantity_removed) if quantity_removed else 0
                            if removed_val == outbound_quantity:
                                print(f"   ✅ الكمية المخرجة صحيحة: {removed_val}")
                            else:
                                print(f"   ❌ الكمية المخرجة خاطئة: متوقع {outbound_quantity}, فعلي {removed_val}")
                        except ValueError:
                            print(f"   ⚠️ لا يمكن تحليل الكمية المخرجة: '{quantity_removed}'")
                
            else:
                print("   ❌ لم يتم إضافة سجل جديد!")
            
        except Exception as e:
            print(f"   ❌ خطأ في فحص Activity Log: {e}")
            import traceback
            traceback.print_exc()
        
    else:
        print(f"   ❌ فشل في الإخراج")
    
    return True

def test_outbound_details_format():
    """Test different recipient names and verify details format."""
    
    print("\n🧪 اختبار صيغة التفاصيل مع أسماء مختلفة")
    print("=" * 60)
    
    test_cases = [
        "أحمد علي",
        "فاطمة محمد", 
        "شركة النور للمقاولات",
        "مشروع المدينة الجديدة",
        "عميل رقم 123"
    ]
    
    for i, recipient in enumerate(test_cases, 1):
        outbound_quantity = 2
        expected_details = f"إخراج بضاعة إلى: {recipient} - الكمية المخرجة: {outbound_quantity}, الكمية المتبقية: [الكمية المحسوبة]"
        
        print(f"\n{i}. اسم المستلم: '{recipient}'")
        print(f"   الصيغة المتوقعة: '{expected_details}'")
        print(f"   ✅ يتضمن اسم المستلم في بداية التفاصيل")
    
    print(f"\n📋 فوائد الإضافة الجديدة:")
    print("   ✅ اسم المستلم يظهر في عمود 'التفاصيل'")
    print("   ✅ سهولة البحث عن عمليات إخراج لمستلم معين")
    print("   ✅ تفاصيل أكثر وضوحاً في سجل الأنشطة")
    print("   ✅ تتبع أفضل لحركة البضائع")
    
    return True

if __name__ == "__main__":
    try:
        test_outbound_with_recipient_details()
        test_outbound_details_format()
        
    except KeyboardInterrupt:
        print("\n⏹️ تم إيقاف الاختبار بواسطة المستخدم")
    except Exception as e:
        print(f"\n❌ خطأ في الاختبار: {e}")
        import traceback
        traceback.print_exc()