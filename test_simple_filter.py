#!/usr/bin/env python3
"""
اختبار النافذة الجديدة المبسطة للفلاتر
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import ttk, messagebox
from gui.simple_filter_window import show_simple_filter_window
from sheets.manager import SheetsManager

def main():
    print("🚀 اختبار نافذة الفلاتر المبسطة...")
    
    # إنشاء النافذة الرئيسية
    root = tk.Tk()
    root.title("اختبار الفلاتر الجديدة")
    root.geometry("400x300")
    
    # إعداد SheetsManager
    sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
    
    if not sheets_manager.connect():
        messagebox.showerror("خطأ", "فشل الاتصال بـ Google Sheets")
        return
    
    # واجهة الاختبار
    main_frame = ttk.Frame(root, padding="30")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # العنوان
    title = ttk.Label(main_frame, text="🔧 نافذة الفلاتر الجديدة المحسنة", 
                     font=("Arial", 14, "bold"))
    title.pack(pady=(0, 20))
    
    # الوصف
    desc = ttk.Label(main_frame, text="""
هذه نسخة مبسطة ومحسنة من نافذة الفلاتر:

✅ تصميم أبسط وأوضح
✅ تحديث فوري للنتائج
✅ عدادات واضحة للبيانات  
✅ أزرار مسح وتحديث
✅ تصدير للنتائج

اضغط لتجربة النافذة الجديدة!
    """, font=("Arial", 10), justify=tk.CENTER)
    desc.pack(pady=(0, 30))
    
    def open_new_filter():
        """فتح النافذة الجديدة"""
        try:
            print("🔓 فتح نافذة الفلاتر الجديدة...")
            filter_window = show_simple_filter_window(root, sheets_manager)
            print("✅ تم فتح النافذة بنجاح")
            
        except Exception as e:
            print(f"❌ خطأ: {e}")
            messagebox.showerror("خطأ", f"فشل في فتح النافذة:\n{e}")
    
    # زر فتح النافذة
    open_btn = ttk.Button(main_frame, text="🚀 فتح نافذة الفلاتر الجديدة", 
                         command=open_new_filter)
    open_btn.pack(pady=20)
    
    # معلومات الحالة
    status = ttk.Label(main_frame, text="✅ متصل بـ Google Sheets", 
                      font=("Arial", 10), foreground="green")
    status.pack()
    
    print("✅ واجهة الاختبار جاهزة")
    
    root.mainloop()

if __name__ == "__main__":
    main()