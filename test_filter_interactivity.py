#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار تفاعلي لنافذة الفلاتر - للتأكد من عمل الفلاتر في النافذة الحقيقية
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import ttk, messagebox
from gui.main_window import MainWindow
from config.settings import load_config

def test_filter_interactivity():
    """اختبار تفاعل الفلاتر في النافذة الحقيقية"""
    
    print("🧪 بدء اختبار تفاعلية الفلاتر...")
    
    # تحميل الإعدادات
    config = load_config()
    
    # إنشاء النافذة الرئيسية
    root = tk.Tk()
    root.title("اختبار الفلاتر التفاعلية")
    root.geometry("600x400")
    
    # إنشاء النافذة الرئيسية
    main_window = MainWindow(root, config)
    main_window.current_user = {'username': 'test_admin', 'user_type': 'admin'}
    
    print("✅ تم إنشاء النافذة الرئيسية")
    
    # إنشاء واجهة اختبار
    test_frame = ttk.Frame(root)
    test_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # العنوان
    title_label = ttk.Label(test_frame, text="🧪 اختبار تفاعلية نافذة الفلاتر", 
                           font=("Arial", 16, "bold"))
    title_label.pack(pady=(0, 20))
    
    # معلومات الاختبار
    info_text = """
📋 خطوات الاختبار:
1. اضغط على "فتح نافذة الفلاتر"
2. جرب تغيير الفلاتر في القوائم المنسدلة
3. لاحظ إذا كانت النتائج تتغير فوراً
4. جرب كتابة تاريخ والانتظار ثانية واحدة
5. جرب أزرار التاريخ السريعة (اليوم، أسبوع، شهر)

✅ المتوقع: الفلاتر تعمل تلقائياً بدون ضغط زر "تطبيق"
❌ إذا لم تعمل: سيتم عرض تشخيص مفصل
"""
    
    info_label = ttk.Label(test_frame, text=info_text, 
                          font=("Arial", 10), justify=tk.LEFT)
    info_label.pack(pady=(0, 20))
    
    # متغير لتتبع حالة الفلاتر
    filter_status = tk.StringVar(value="لم يتم فتح النافذة بعد")
    status_label = ttk.Label(test_frame, textvariable=filter_status,
                            font=("Arial", 12, "bold"), foreground="blue")
    status_label.pack(pady=(0, 10))
    
    # دالة فتح نافذة الفلاتر مع تشخيص
    def open_filter_with_diagnosis():
        try:
            filter_status.set("🔄 فتح نافذة الفلاتر...")
            root.update()
            
            # فتح النافذة
            main_window.open_filter_search_window()
            
            filter_status.set("✅ تم فتح النافذة - جرب الفلاتر الآن!")
            
            # إضافة تشخيص إضافي
            diagnosis_text = """
🔍 تشخيص إضافي:
• تأكد من أن القوائم المنسدلة تحتوي على خيارات
• جرب اختيار عنصر مختلف من قائمة "العنصر"
• لاحظ تغيير الأرقام في شريط الإحصائيات
• إذا لم تعمل، تحقق من وحدة التحكم للأخطاء
"""
            
            diagnosis_label = ttk.Label(test_frame, text=diagnosis_text,
                                       font=("Arial", 9), foreground="green",
                                       justify=tk.LEFT)
            diagnosis_label.pack(pady=10)
            
        except Exception as e:
            filter_status.set(f"❌ خطأ: {str(e)}")
            print(f"❌ خطأ في فتح نافذة الفلاتر: {e}")
            import traceback
            traceback.print_exc()
    
    # زر فتح النافذة
    open_btn = ttk.Button(test_frame, text="🔍 فتح نافذة الفلاتر للاختبار",
                         command=open_filter_with_diagnosis)
    open_btn.pack(pady=10)
    
    # زر إغلاق
    def close_test():
        root.quit()
        root.destroy()
    
    close_btn = ttk.Button(test_frame, text="❌ إغلاق الاختبار", 
                          command=close_test)
    close_btn.pack(pady=5)
    
    print("🖱️ النافذة جاهزة للاختبار")
    
    # تشغيل النافذة
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\n👋 تم إيقاف الاختبار")
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {e}")

if __name__ == "__main__":
    test_filter_interactivity()