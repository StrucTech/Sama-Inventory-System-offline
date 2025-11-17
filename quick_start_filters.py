#!/usr/bin/env python3
"""
🚀 مشغل الفلاتر السريع - تجاوز كامل لتسجيل الدخول
الحل الأسرع والأكثر مباشرة
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# إضافة مسار المشروع
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.basic_filter_window import open_basic_filter_window
from sheets.manager import SheetsManager

def main():
    """التشغيل المباشر للفلاتر"""
    
    print("🚀 مشغل الفلاتر السريع - بدء فوري!")
    
    try:
        # إنشاء نافذة رئيسية مخفية (مطلوبة لـ tkinter)
        root = tk.Tk()
        root.withdraw()  # إخفاؤها فوراً
        
        # رسالة ترحيب
        messagebox.showinfo("مرحباً! 🔥",
            "مرحباً بك في مشغل الفلاتر السريع!\n\n"
            "🚀 سيتم الآن:\n"
            "• الاتصال التلقائي بـ Google Sheets\n"  
            "• فتح نافذة الفلاتر المتطورة مباشرة\n"
            "• تجاهل تماماً أي تعقيدات تسجيل الدخول\n\n"
            "⏳ انتظر قليلاً...")
        
        # الاتصال المباشر
        print("🔗 اتصال مباشر بـ Google Sheets...")
        sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
        
        if not sheets_manager.connect():
            messagebox.showerror("خطأ", 
                "فشل في الاتصال بـ Google Sheets!\n\n"
                "تأكد من:\n"
                "• وجود ملف config/credentials.json\n"
                "• صحة بيانات الاعتماد\n"
                "• اتصال الإنترنت")
            return
        
        # تحميل البيانات
        data = sheets_manager.get_all_items_raw()
        print(f"✅ تم تحميل {len(data)} عنصر من قاعدة البيانات")
        
        # مستخدم افتراضي فوري
        current_user = {
            'username': 'admin', 
            'user_type': 'admin',
            'project_id': None
        }
        
        print(f"👤 دخول تلقائي كمستخدم: {current_user['username']}")
        
        # إظهار النافذة الرئيسية
        root.deiconify()
        root.title("🔥 مشغل الفلاتر السريع")
        root.geometry("400x200")
        root.configure(bg="#2c3e50")
        
        # عنوان سريع
        title = tk.Label(
            root,
            text="🔥 مشغل الفلاتر السريع",
            font=("Arial", 16, "bold"),
            fg="#f1c40f", bg="#2c3e50"
        )
        title.pack(pady=20)
        
        # معلومات سريعة
        info = tk.Label(
            root,
            text=f"متصل بنجاح! تم تحميل {len(data)} عنصر",
            font=("Arial", 12),
            fg="#2ecc71", bg="#2c3e50"
        )
        info.pack(pady=10)
        
        # زر فتح الفلاتر
        def open_filters_now():
            try:
                print("🎛️ فتح نافذة الفلاتر...")
                
                filter_window = open_basic_filter_window(
                    parent=root,
                    sheets_manager=sheets_manager,
                    current_user=current_user
                )
                
                if filter_window:
                    print("🎉 تم فتح الفلاتر بنجاح!")
                    
                    messagebox.showinfo("نجح! 🚀",
                        "تم فتح نظام الفلاتر بنجاح!\n\n"
                        "🎛️ استمتع بالميزات التالية:\n"
                        "• فلتر التصنيف\n"
                        "• فلتر المشروع\n" 
                        "• تحديث فوري\n"
                        "• مسح الفلاتر\n"
                        "• تحديث البيانات\n\n"
                        "💡 جميع التغييرات فورية ومباشرة!")
                else:
                    messagebox.showerror("خطأ", "فشل في إنشاء نافذة الفلاتر!")
                    
            except Exception as e:
                print(f"❌ خطأ: {e}")
                messagebox.showerror("خطأ", f"حدث خطأ في فتح الفلاتر:\n{str(e)}")
        
        # زر كبير للفلاتر
        filter_btn = tk.Button(
            root,
            text="🎛️ فتح الفلاتر الآن!",
            command=open_filters_now,
            font=("Arial", 14, "bold"),
            bg="#e74c3c", fg="white",
            padx=30, pady=15,
            relief="flat", cursor="hand2"
        )
        filter_btn.pack(pady=20)
        
        # زر الإغلاق
        close_btn = tk.Button(
            root,
            text="❌ إغلاق",
            command=root.destroy,
            font=("Arial", 12),
            bg="#95a5a6", fg="white",
            padx=20, pady=10,
            relief="flat", cursor="hand2"
        )
        close_btn.pack(pady=10)
        
        print("🎉 المشغل السريع جاهز!")
        
        # تشغيل النافذة
        root.mainloop()
        
    except Exception as e:
        print(f"💥 خطأ في المشغل السريع: {e}")
        import traceback
        traceback.print_exc()
        
        messagebox.showerror("خطأ",
            f"حدث خطأ في المشغل السريع:\n{str(e)}\n\n"
            f"حاول:\n"
            f"• إعادة تشغيل التطبيق\n"
            f"• التحقق من ملفات الإعداد\n"
            f"• فحص اتصال الإنترنت")

if __name__ == "__main__":
    main()