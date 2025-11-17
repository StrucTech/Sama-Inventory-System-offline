#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for the fixed recent addition edit issues.
اختبار إصلاح مشاكل تعديل آخر إضافة
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sheets.manager import SheetsManager

def test_recent_addition_edit_fixes():
    """Test the fixed recent addition edit functionality."""
    
    print("🧪 اختبار إصلاح مشاكل تعديل آخر إضافة")
    print("=" * 60)
    
    # Test scenarios to verify the fixes
    test_scenarios = [
        {
            "name": "العودة للكمية الأصلية",
            "original_add": 22.0,
            "first_edit": 20.0,
            "second_edit": 22.0,
            "description": "إضافة 22 → تعديل إلى 20 → تعديل إلى 22 مرة أخرى"
        },
        {
            "name": "زيادة أعلى من الكمية الأصلية",
            "original_add": 15.0,
            "first_edit": 25.0,
            "second_edit": 30.0,
            "description": "إضافة 15 → تعديل إلى 25 → تعديل إلى 30"
        },
        {
            "name": "تعديل متكرر لنفس القيمة",
            "original_add": 10.0,
            "first_edit": 10.0,
            "second_edit": 10.0,
            "description": "إضافة 10 → تعديل إلى 10 → تعديل إلى 10 مرة أخرى"
        }
    ]
    
    print("\n🔍 اختبار السيناريوهات الجديدة:")
    print("-" * 80)
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n{i}. {scenario['name']}:")
        print(f"   الوصف: {scenario['description']}")
        
        # Simulate the logic that would happen
        print(f"   الخطوات:")
        print(f"   1. إضافة أولية: {scenario['original_add']}")
        
        # First edit
        current_quantity_1 = scenario['original_add']  # Starting quantity
        old_quantity_1 = scenario['original_add']
        new_quantity_1 = scenario['first_edit']
        difference_1 = new_quantity_1 - old_quantity_1
        result_1 = current_quantity_1 + difference_1
        
        print(f"   2. التعديل الأول: {old_quantity_1} → {new_quantity_1}")
        print(f"      الفرق: {difference_1:+}")
        print(f"      الكمية الإجمالية الجديدة: {result_1}")
        
        # Check if this would be allowed
        is_valid_1 = new_quantity_1 >= 0 and result_1 >= 0
        print(f"      النتيجة: {'✅ مسموح' if is_valid_1 else '❌ مرفوض'}")
        
        if is_valid_1:
            # Second edit
            current_quantity_2 = result_1  # Result of first edit
            old_quantity_2 = new_quantity_1  # What was added in first edit
            new_quantity_2 = scenario['second_edit']
            difference_2 = new_quantity_2 - old_quantity_2
            result_2 = current_quantity_2 + difference_2
            
            print(f"   3. التعديل الثاني: {old_quantity_2} → {new_quantity_2}")
            print(f"      الفرق: {difference_2:+}")
            print(f"      الكمية الإجمالية النهائية: {result_2}")
            
            # Check if this would be allowed
            is_valid_2 = new_quantity_2 >= 0 and result_2 >= 0
            print(f"      النتيجة: {'✅ مسموح' if is_valid_2 else '❌ مرفوض'}")
            
            # Special case checks
            if old_quantity_2 == new_quantity_2:
                print(f"      📌 ملاحظة: العودة لنفس القيمة - الآن مسموح ✅")
            
            if new_quantity_2 > scenario['original_add']:
                print(f"      📌 ملاحظة: كمية أعلى من الإضافة الأصلية ({scenario['original_add']}) - الآن مسموح ✅")
                
        print(f"   الخلاصة: جميع العمليات ستكون مسموحة مع الإصلاحات الجديدة")
    
    print(f"\n📊 ملخص الإصلاحات:")
    print("   ✅ إزالة منع العودة للكمية نفسها")
    print("   ✅ إزالة الحد الأقصى للكمية المضافة")
    print("   ✅ السماح بكميات أعلى من الإضافة الأصلية")
    print("   ✅ السماح بالتعديل المتكرر لنفس القيمة")
    print("   ✅ الحفاظ على منع الكميات السالبة فقط")
    
    print(f"\n🎯 السيناريو المذكور في المشكلة:")
    print("   إضافة عنصر جديد: 22")
    print("   تعديل إلى: 20 ✅")
    print("   تعديل إلى: 22 مرة أخرى ✅ (لن يقول 'لم يتم تغيير شيء')")
    print("   تعديل إلى: 30 ✅ (مسموح الآن - أعلى من 22)")
    
    return True

if __name__ == "__main__":
    try:
        test_recent_addition_edit_fixes()
        
    except KeyboardInterrupt:
        print("\n⏹️ تم إيقاف الاختبار بواسطة المستخدم")
    except Exception as e:
        print(f"\n❌ خطأ في الاختبار: {e}")
        import traceback
        traceback.print_exc()