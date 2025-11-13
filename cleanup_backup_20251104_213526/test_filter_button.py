#!/usr/bin/env python3
"""
اختبار سريع لفحص عمل زر الفلترة في نافذة التقارير
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# إضافة مسار المشروع
sys.path.append(os.path.dirname(__file__))

from gui.reports_window import ReportsWindow

def test_filter_button():
    """اختبار زر الفلترة"""
    print("🧪 بدء اختبار زر الفلترة...")
    
    # إنشاء النافذة الرئيسية
    root = tk.Tk()
    root.withdraw()  # إخفاء النافذة الرئيسية
    
    try:
        # إنشاء نافذة التقارير
        reports_window = ReportsWindow(root)
        
        # اختبار وجود الدالة
        if hasattr(reports_window, 'apply_filters'):
            print("✅ دالة apply_filters موجودة")
            
            # محاولة استدعاء الدالة مباشرة
            print("🔍 اختبار استدعاء apply_filters مباشرة...")
            reports_window.apply_filters()
            print("✅ تم استدعاء apply_filters بنجاح")
            
        else:
            print("❌ دالة apply_filters غير موجودة")
            
        # فحص وجود زر تطبيق الفلتر
        def find_filter_button(widget, depth=0):
            """البحث عن زر تطبيق الفلتر"""
            if depth > 10:  # تجنب البحث العميق
                return None
                
            if isinstance(widget, ttk.Button):
                if hasattr(widget, 'cget'):
                    try:
                        text = widget.cget('text')
                        if 'تطبيق' in text and 'فلتر' in text:
                            return widget
                    except:
                        pass
            
            # البحث في العناصر الفرعية
            if hasattr(widget, 'winfo_children'):
                for child in widget.winfo_children():
                    result = find_filter_button(child, depth + 1)
                    if result:
                        return result
            
            return None
        
        filter_button = find_filter_button(reports_window.window)
        
        if filter_button:
            print("✅ تم العثور على زر تطبيق الفلتر")
            
            # فحص الأمر المرتبط بالزر
            try:
                command = filter_button.cget('command')
                if command:
                    print("✅ الزر مرتبط بأمر")
                    print(f"🔗 الأمر: {command}")
                else:
                    print("❌ الزر غير مرتبط بأي أمر!")
            except Exception as e:
                print(f"❌ خطأ في فحص أمر الزر: {e}")
                
        else:
            print("❌ لم يتم العثور على زر تطبيق الفلتر")
        
        # إغلاق النافذة
        reports_window.window.destroy()
        
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {e}")
        import traceback
        traceback.print_exc()
    
    root.destroy()

if __name__ == "__main__":
    test_filter_button()