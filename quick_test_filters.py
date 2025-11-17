#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 اختبار سريع للنظام الجديد
=============================

هذا الملف لاختبار النظام الجديد بسرعة
"""

import sys
import os

# إضافة مسار المشروع
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_new_filter_system():
    """اختبار سريع للنظام الجديد"""
    
    print("🎯 اختبار النظام الجديد...")
    print("="*50)
    
    try:
        from new_activity_filter_system import NewActivityFilterSystem
        from sheets.manager import SheetsManager
        import tkinter as tk
        
        # الاتصال بـ Google Sheets
        sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
        if not sheets_manager.connect():
            print("❌ فشل في الاتصال!")
            return
            
        print("✅ تم الاتصال بـ Google Sheets")
        
        # إنشاء النافذة
        root = tk.Tk()
        
        # إنشاء النظام الجديد
        filter_system = NewActivityFilterSystem(parent=root, sheets_manager=sheets_manager)
        window = filter_system.create_window()
        
        if window:
            print("✅ تم إنشاء النافذة بنجاح!")
            print("\n🔍 جرب الآن:")
            print("1. غيّر فلتر التصنيف إلى 'أدوات سباكة'")
            print("2. لاحظ تغير العدد من 182 إلى 29")
            print("3. غيّر فلتر المستخدم إلى مستخدم معين")
            print("4. لاحظ تغير العدد مرة أخرى")
            print("5. اضغط 'إعادة تعيين' لإرجاع الكل")
            print("\n" + "="*50)
            
            # تشغيل النافذة
            window.mainloop()
        else:
            print("❌ فشل في إنشاء النافذة!")
            
    except Exception as e:
        print(f"❌ خطأ: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_new_filter_system()