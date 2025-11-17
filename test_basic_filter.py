#!/usr/bin/env python3
"""
اختبار النافذة الأساسية المضمونة
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import messagebox
from gui.basic_filter_window import open_basic_filter_window
from sheets.manager import SheetsManager

def test_basic_filter():
    print("🧪 اختبار النافذة الأساسية المضمونة...")
    
    root = tk.Tk()
    root.title("اختبار الفلاتر الأساسية")
    root.geometry("400x200")
    root.configure(bg="#34495e")
    
    # الاتصال
    sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
    
    if not sheets_manager.connect():
        messagebox.showerror("خطأ", "فشل الاتصال")
        return
    
    # فحص البيانات
    data = sheets_manager.get_all_items_raw()
    print(f"📊 البيانات: {len(data)} عنصر")
    
    # واجهة الاختبار
    main_frame = tk.Frame(root, bg="#34495e", padx=30, pady=30)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    title = tk.Label(main_frame, text="🧪 اختبار الفلاتر الأساسية المضمونة", 
                    font=("Arial", 14, "bold"), fg="white", bg="#34495e")
    title.pack(pady=(0, 20))
    
    info = tk.Label(main_frame, 
        text=f"البيانات المتاحة: {len(data)} عنصر\\n"
             f"هذه النافذة تستخدم 3 طرق مختلفة\\n"
             f"لضمان عمل الفلاتر بشكل مضمون!",
        font=("Arial", 11), fg="#bdc3c7", bg="#34495e")
    info.pack(pady=(0, 30))
    
    def open_test():
        try:
            print("🚀 فتح النافذة الأساسية المضمونة...")
            window = open_basic_filter_window(root, sheets_manager)
            
            if window:
                print("✅ تم فتح النافذة بنجاح!")
                messagebox.showinfo("نجح!", 
                    f"تم فتح النافذة الأساسية المضمونة!\\n\\n"
                    f"📊 البيانات: {len(data)} عنصر\\n"
                    f"🎛️ الفلاتر تستخدم 3 طرق للضمان\\n"
                    f"⚡ تحديث مضمون 100%\\n\\n"
                    f"جرب الفلاتر الآن!")
                
        except Exception as e:
            print(f"❌ خطأ: {e}")
            messagebox.showerror("خطأ", f"فشل: {e}")
    
    test_btn = tk.Button(main_frame, text="🚀 فتح النافذة المضمونة", 
                        command=open_test, font=("Arial", 12, "bold"),
                        bg="#27ae60", fg="white", padx=20, pady=10,
                        relief="flat", cursor="hand2")
    test_btn.pack()
    
    print("✅ جاهز للاختبار")
    root.mainloop()

if __name__ == "__main__":
    test_basic_filter()