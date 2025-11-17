#!/usr/bin/env python3
"""
🔥 اختبار مباشر لإصلاحات الفلاتر
التأكد من أن الفلاتر تغير البيانات فعلاً
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# إضافة مسار المشروع
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_filters_directly():
    """اختبار مباشر للفلاتر"""
    
    print("🔥 بدء اختبار الفلاتر المباشر...")
    
    try:
        from gui.advanced_filter_window import open_advanced_filter_window
        from sheets.manager import SheetsManager
        
        # إنشاء نافذة مؤقتة
        root = tk.Tk()
        root.title("🧪 اختبار إصلاحات الفلاتر")
        root.geometry("400x200")
        root.configure(bg="#2c3e50")
        
        # إخفاء النافذة أثناء التحميل
        root.withdraw()
        
        print("🔗 الاتصال بـ Google Sheets...")
        sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
        
        if not sheets_manager.connect():
            messagebox.showerror("خطأ", "فشل الاتصال!")
            return
            
        # عرض النافذة
        root.deiconify()
        
        # العنوان
        title = tk.Label(
            root,
            text="🧪 اختبار إصلاحات الفلاتر",
            font=("Arial", 16, "bold"),
            fg="#f1c40f", bg="#2c3e50"
        )
        title.pack(pady=20)
        
        # رسالة
        msg = tk.Label(
            root,
            text="سيتم الآن فتح نافذة الفلاتر المصلحة\nجرب تغيير أي فلتر وراقب تحديث البيانات",
            font=("Arial", 12),
            fg="#ecf0f1", bg="#2c3e50"
        )
        msg.pack(pady=20)
        
        # المستخدم الافتراضي
        current_user = {'username': 'admin', 'user_type': 'admin'}
        
        # دالة فتح الفلاتر
        def open_filters():
            try:
                print("🎛️ فتح نافذة الفلاتر المصلحة...")
                
                filter_window = open_advanced_filter_window(
                    parent=root,
                    sheets_manager=sheets_manager,
                    current_user=current_user
                )
                
                if filter_window:
                    print("✅ تم فتح الفلاتر المصلحة!")
                    messagebox.showinfo("جاهز للاختبار! 🧪",
                        "تم فتح نافذة الفلاتر المصلحة!\n\n"
                        "🔍 اختبر الآن:\n"
                        "• غيّر أي فلتر\n"
                        "• راقب تحديث البيانات فوراً\n"
                        "• تأكد من تغير عدد النتائج\n\n"
                        "💡 إذا لم تتغير البيانات، فهناك مشكلة!")
                else:
                    messagebox.showerror("خطأ", "فشل في فتح الفلاتر!")
                    
            except Exception as e:
                print(f"❌ خطأ: {e}")
                import traceback
                traceback.print_exc()
                messagebox.showerror("خطأ", f"حدث خطأ:\n{str(e)}")
        
        # زر الاختبار
        test_btn = tk.Button(
            root,
            text="🚀 اختبار الفلاتر الآن!",
            command=open_filters,
            font=("Arial", 14, "bold"),
            bg="#e74c3c", fg="white",
            padx=30, pady=15,
            relief="flat", cursor="hand2"
        )
        test_btn.pack(pady=30)
        
        print("🎯 نافذة الاختبار جاهزة!")
        root.mainloop()
        
    except Exception as e:
        print(f"💥 خطأ في الاختبار: {e}")
        import traceback
        traceback.print_exc()
        messagebox.showerror("خطأ", f"فشل الاختبار:\n{str(e)}")

if __name__ == "__main__":
    test_filters_directly()