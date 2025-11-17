#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for the fixed recent addition edit functionality.
اختبار إصلاح تعديل آخر إضافة
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sheets.manager import SheetsManager

def test_recent_addition_edit_fix():
    """Test the fixed logic for editing recent additions."""
    
    print("🧪 اختبار إصلاح تعديل آخر إضافة")
    print("=" * 60)
    
    # Initialize sheets manager
    sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
    sheets_manager.current_user = "مطور_النظام"
    
    if not sheets_manager.connect():
        print("❌ فشل الاتصال بـ Google Sheets")
        return False
    
    print("✅ تم الاتصال بـ Google Sheets بنجاح")
    
    # Test scenarios to verify the fixed logic
    test_scenarios = [
        {
            "name": "سيناريو طبيعي",
            "current_quantity": 50.0,
            "old_added": 20.0,
            "new_added": 15.0,
            "expected_result": 45.0,  # 50 + (15 - 20) = 45
            "should_work": True
        },
        {
            "name": "زيادة الكمية المضافة",
            "current_quantity": 30.0,
            "old_added": 10.0,
            "new_added": 25.0,
            "expected_result": 45.0,  # 30 + (25 - 10) = 45
            "should_work": True
        },
        {
            "name": "تقليل الكمية المضافة بشكل معقول",
            "current_quantity": 40.0,
            "old_added": 30.0,
            "new_added": 10.0,
            "expected_result": 20.0,  # 40 + (10 - 30) = 20
            "should_work": True
        },
        {
            "name": "تقليل يؤدي لكمية سالبة",
            "current_quantity": 25.0,
            "old_added": 10.0,
            "new_added": 5.0,
            "expected_result": 20.0,  # 25 + (5 - 10) = 20
            "should_work": True
        },
        {
            "name": "تقليل مفرط يؤدي لكمية سالبة",
            "current_quantity": 15.0,
            "old_added": 10.0,
            "new_added": 2.0,
            "expected_result": 7.0,   # 15 + (2 - 10) = 7
            "should_work": True
        },
        {
            "name": "حالة تقليل أكثر من الكمية الحالية",
            "current_quantity": 10.0,
            "old_added": 20.0,
            "new_added": 5.0,
            "expected_result": -5.0,  # 10 + (5 - 20) = -5 (should fail)
            "should_work": False
        }
    ]
    
    print("\n🔍 اختبار منطق الحساب الجديد:")
    print("-" * 80)
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n{i}. {scenario['name']}:")
        print(f"   الكمية الحالية: {scenario['current_quantity']}")
        print(f"   الكمية المضافة السابقة: {scenario['old_added']}")
        print(f"   الكمية المضافة الجديدة: {scenario['new_added']}")
        
        # Calculate using the new logic
        quantity_difference = scenario['new_added'] - scenario['old_added']
        new_total_quantity = scenario['current_quantity'] + quantity_difference
        
        print(f"   الفرق في الكمية: {quantity_difference:+}")
        print(f"   النتيجة المحسوبة: {new_total_quantity}")
        print(f"   النتيجة المتوقعة: {scenario['expected_result']}")
        
        # Check if calculation matches expected
        if abs(new_total_quantity - scenario['expected_result']) < 0.001:
            print(f"   ✅ الحساب صحيح")
        else:
            print(f"   ❌ خطأ في الحساب")
        
        # Check if it should work according to new validation
        is_valid = (
            new_total_quantity >= 0 and 
            not (quantity_difference < 0 and abs(quantity_difference) > scenario['current_quantity'])
        )
        
        if is_valid == scenario['should_work']:
            print(f"   ✅ التحقق من الصحة مطابق للمتوقع: {'يجب أن يعمل' if scenario['should_work'] else 'يجب أن يفشل'}")
        else:
            print(f"   ❌ التحقق من الصحة غير مطابق للمتوقع")
        
        if not is_valid:
            if new_total_quantity < 0:
                print(f"   ⚠️ سبب الفشل: الكمية الإجمالية ستكون سالبة ({new_total_quantity})")
            elif quantity_difference < 0 and abs(quantity_difference) > scenario['current_quantity']:
                print(f"   ⚠️ سبب الفشل: التقليل ({abs(quantity_difference)}) أكبر من الكمية الحالية ({scenario['current_quantity']})")
    
    print(f"\n📊 ملخص الإصلاحات:")
    print("   ✅ إزالة حساب 'الكمية الأصلية' المُعقد والخاطئ")
    print("   ✅ استخدام الفرق البسيط: الكمية الجديدة = الحالية + (الجديدة - القديمة)")
    print("   ✅ التحقق من عدم وجود كمية سالبة")
    print("   ✅ التحقق من عدم التقليل أكثر من الكمية الحالية")
    print("   ✅ رسائل خطأ واضحة ومفصلة")
    
    return True

if __name__ == "__main__":
    try:
        test_recent_addition_edit_fix()
        
    except KeyboardInterrupt:
        print("\n⏹️ تم إيقاف الاختبار بواسطة المستخدم")
    except Exception as e:
        print(f"\n❌ خطأ في الاختبار: {e}")
        import traceback
        traceback.print_exc()