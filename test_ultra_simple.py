#!/usr/bin/env python3
"""
اختبار النافذة البسيطة جداً
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import messagebox
from gui.ultra_simple_filter import show_ultra_simple_filter_window
from sheets.manager import SheetsManager

def test_ultra_simple():
    print("🚀 اختبار النافذة البسيطة جداً...")
    
    root = tk.Tk()
    root.title("اختبار الفلاتر البسيطة")
    root.geometry("300x200")
    
    # الاتصال
    sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
    
    if sheets_manager.connect():
        print("✅ متصل بنجاح")
        
        # فحص البيانات
        data = sheets_manager.get_all_items_raw()
        print(f"📊 البيانات: {len(data)} عنصر")
        
        def open_filter():
            try:
                print("🔓 فتح النافذة البسيطة...")
                window = show_ultra_simple_filter_window(root, sheets_manager)
                print("✅ تم فتح النافذة")
                
                messagebox.showinfo("نجح!", 
                    f"تم فتح النافذة البسيطة جداً!\\n\\n"
                    f"البيانات: {len(data)} عنصر\\n"
                    f"جرب تغيير الفلاتر وراقب التحديث الفوري!")
                
            except Exception as e:
                print(f"❌ خطأ: {e}")
                import traceback
                traceback.print_exc()
        
        # زر الاختبار
        tk.Button(root, text="🚀 فتح النافذة البسيطة", 
                 command=open_filter, font=("Arial", 12),
                 bg="#4CAF50", fg="white", padx=20, pady=10).pack(pady=50)
        
        tk.Label(root, text=f"البيانات جاهزة: {len(data)} عنصر", 
                font=("Arial", 10), fg="green").pack()
        
        print("✅ جاهز للاختبار")
        root.mainloop()
        
    else:
        print("❌ فشل الاتصال")
        messagebox.showerror("خطأ", "فشل الاتصال بـ Google Sheets")

if __name__ == "__main__":
    test_ultra_simple()