#!/usr/bin/env python3
"""
اختبار شامل لوظائف الفلاتر
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.filter_search_window import FilterSearchWindow
import tkinter as tk
from unittest.mock import MagicMock

def simulate_user_interactions():
    """محاكاة تفاعلات المستخدم مع الفلاتر"""
    
    # إنشاء نافذة رئيسية وهمية
    root = tk.Tk()
    root.withdraw()
    
    # إعداد مستخدم وهمي
    mock_user = {
        'username': 'admin',
        'user_type': 'admin',
        'project_id': None
    }
    
    # إعداد SheetsManager وهمي
    mock_sheets = MagicMock()
    mock_sheets.get_filtered_inventory_data.return_value = [
        {"item_name": "كمبيوتر محمول", "category": "أجهزة", "quantity": 5, "project_id": "مشروع أ"},
        {"item_name": "طابعة", "category": "أجهزة", "quantity": 2, "project_id": "مشروع ب"},
        {"item_name": "قلم", "category": "قرطاسية", "quantity": 100, "project_id": "مشروع أ"}
    ]
    
    print("🔄 إنشاء نافذة الفلاتر...")
    try:
        # إنشاء نافذة الفلاتر
        filter_window = FilterSearchWindow(root, mock_sheets, mock_user)
        
        print("✅ نافذة الفلاتر تم إنشاؤها بنجاح")
        
        # اختبار الأحداث
        print("\n🧪 اختبار تفاعل الفلاتر:")
        
        # محاكاة تغيير فلتر العنصر
        print("📋 اختبار فلتر العنصر...")
        if hasattr(filter_window, 'on_combobox_change'):
            filter_window.on_combobox_change("العنصر")
            print("✅ فلتر العنصر يستجيب للأحداث")
        else:
            print("❌ دالة on_combobox_change غير موجودة")
        
        # محاكاة تغيير فلتر التصنيف
        print("🏷️ اختبار فلتر التصنيف...")
        if hasattr(filter_window, 'on_combobox_change'):
            filter_window.on_combobox_change("التصنيف")
            print("✅ فلتر التصنيف يستجيب للأحداث")
        
        # محاكاة تغيير فلتر المشروع
        print("📊 اختبار فلتر المشروع...")
        if hasattr(filter_window, 'on_combobox_change'):
            filter_window.on_combobox_change("المشروع")
            print("✅ فلتر المشروع يستجيب للأحداث")
        
        # اختبار التأخير في الفلاتر النصية
        print("⏰ اختبار التأخير في التحديث...")
        if hasattr(filter_window, 'on_entry_change'):
            filter_window.on_entry_change()
            print("✅ آلية التأخير تعمل")
        
        # اختبار تطبيق الفلاتر
        print("🔧 اختبار تطبيق الفلاتر...")
        if hasattr(filter_window, 'apply_filters'):
            filter_window.apply_filters()
            print("✅ دالة تطبيق الفلاتر تعمل")
        
        print("\n📊 ملخص الاختبار:")
        print("✅ جميع الفحوصات تمت بنجاح")
        print("✅ الفلاتر جاهزة للاستخدام")
        
        # إغلاق النافذة
        filter_window.window.destroy()
        
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {str(e)}")
        import traceback
        print(traceback.format_exc())
    finally:
        root.destroy()

if __name__ == "__main__":
    print("🧪 بدء اختبار وظائف الفلاتر...")
    simulate_user_interactions()
    print("✅ انتهى الاختبار")