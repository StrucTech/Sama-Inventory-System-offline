#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار إصلاح تحديث الكميات في المخزن
"""

from sheets.manager import SheetsManager

def test_quantity_update():
    print("🔧 اختبار إصلاح تحديث الكميات")
    
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
        
        # محاولة تحديث الكمية
        new_quantity = 15  # كمية جديدة للاختبار
        print(f"\n🔄 محاولة تحديث الكمية إلى {new_quantity}")
        
        sheets_manager.current_user = "test_system"
        success = sheets_manager.update_quantity(target_item['row'], new_quantity)
        
        if success:
            print("✅ تم تحديث الكمية بنجاح!")
            
            # التحقق من التحديث
            print("\n📊 التحقق من التحديث...")
            updated_items = sheets_manager.get_all_items()
            
            for item in updated_items:
                if item['item_name'] == 'hamada_item2':
                    print(f"   الكمية الجديدة: {item['quantity']}")
                    if float(item['quantity']) == float(new_quantity):
                        print("✅ تم تحديث الكمية في الشيت بنجاح!")
                    else:
                        print("❌ الكمية لم تُحدث في الشيت!")
                    break
        else:
            print("❌ فشل في تحديث الكمية")
            
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_quantity_update()