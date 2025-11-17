#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for quantity difference calculation in update operations.
اختبار حساب الفرق في الكمية عند التحديث
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sheets.manager import SheetsManager

def test_quantity_difference():
    """Test the new quantity difference calculation feature."""
    
    print("🧪 اختبار حساب الفرق في الكمية عند التعديل")
    print("=" * 60)
    
    # Initialize sheets manager
    sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
    sheets_manager.current_user = "مطور_النظام"
    
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
        if 'hamada_item' in item.get('item_name', '').lower():
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
    
    # Test scenarios
    scenarios = [
        {"new_qty": float(test_item['quantity']) + 10, "description": "زيادة 10"},
        {"new_qty": float(test_item['quantity']) + 10 - 5, "description": "تقليل 5"},
        {"new_qty": float(test_item['quantity']) + 10 - 5 - 3, "description": "تقليل 3 إضافية"},
    ]
    
    original_quantity = float(test_item['quantity'])
    current_quantity = original_quantity
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n🔄 سيناريو {i}: {scenario['description']}")
        print(f"   من: {current_quantity} إلى: {scenario['new_qty']}")
        print(f"   الفرق المتوقع: {scenario['new_qty'] - current_quantity:+.1f}")
        
        # Perform update
        success = sheets_manager.update_quantity(test_row, scenario['new_qty'])
        
        if success:
            print(f"   ✅ تم التحديث بنجاح")
            current_quantity = scenario['new_qty']
        else:
            print(f"   ❌ فشل في التحديث")
            break
        
        # Small delay to ensure operations are processed
        import time
        time.sleep(1)
    
    print(f"\n📊 النتيجة النهائية:")
    print(f"   الكمية الأصلية: {original_quantity}")
    print(f"   الكمية النهائية: {current_quantity}")
    print(f"   إجمالي التغيير: {current_quantity - original_quantity:+.1f}")
    
    return True

if __name__ == "__main__":
    try:
        test_quantity_difference()
        
    except KeyboardInterrupt:
        print("\n⏹️ تم إيقاف الاختبار بواسطة المستخدم")
    except Exception as e:
        print(f"\n❌ خطأ في الاختبار: {e}")
        import traceback
        traceback.print_exc()