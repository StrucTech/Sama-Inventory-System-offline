#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار وظيفة إخراج البضائع
"""

from sheets.manager import SheetsManager

def test_outbound():
    print("📦 اختبار وظيفة إخراج البضائع")
    
    # الاتصال بـ Google Sheets
    sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
    
    if not sheets_manager.connect():
        print("❌ فشل في الاتصال بـ Google Sheets")
        return
    
    print("✅ تم الاتصال بـ Google Sheets")
    
    try:
        # البحث عن العنصر hamada_item2
        all_items = sheets_manager.get_all_items()
        target_item = None
        
        for item in all_items:
            if item['item_name'] == 'hamada_item2':
                target_item = item
                break
        
        if not target_item:
            print("❌ لم يتم العثور على العنصر hamada_item2")
            return
            
        print(f"🔍 تم العثور على العنصر: {target_item['item_name']}")
        print(f"   الكمية الحالية: {target_item['quantity']}")
        print(f"   الصف: {target_item['row']}")
        
        # محاولة إخراج كمية
        outbound_quantity = 3  # كمية للإخراج
        recipient = "مستلم تجريبي"
        
        if float(target_item['quantity']) < outbound_quantity:
            print(f"❌ الكمية غير كافية للإخراج (متاح: {target_item['quantity']}, مطلوب: {outbound_quantity})")
            return
        
        print(f"\n📤 محاولة إخراج كمية {outbound_quantity} للمستلم: {recipient}")
        
        sheets_manager.current_user = "test_system"
        success = sheets_manager.outbound_item(target_item['row'], outbound_quantity, recipient)
        
        if success:
            print("✅ تم إخراج البضاعة بنجاح!")
            
            # التحقق من التحديث
            print("\n📊 التحقق من التحديث...")
            updated_items = sheets_manager.get_all_items()
            
            for item in updated_items:
                if item['item_name'] == 'hamada_item2':
                    expected_quantity = float(target_item['quantity']) - outbound_quantity
                    print(f"   الكمية المتوقعة: {expected_quantity}")
                    print(f"   الكمية الفعلية: {item['quantity']}")
                    
                    if float(item['quantity']) == expected_quantity:
                        print("✅ تم تحديث الكمية بعد الإخراج بنجاح!")
                    else:
                        print("❌ الكمية لم تُحدث بشكل صحيح!")
                    break
        else:
            print("❌ فشل في إخراج البضاعة")
            
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_outbound()