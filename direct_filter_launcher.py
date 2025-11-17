#!/usr/bin/env python3
"""
حل مباشر وفوري لفتح نافذة الفلاتر من التطبيق الرئيسي
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import messagebox
from gui.basic_filter_window import open_basic_filter_window
from sheets.manager import SheetsManager

def create_direct_filter_launcher():
    """إنشاء مشغل مباشر لنافذة الفلاتر"""
    
    print("🚀 بدء مشغل الفلاتر المباشر...")
    
    # إنشاء النافذة الرئيسية
    root = tk.Tk()
    root.title("🔍 مشغل الفلاتر المباشر")
    root.geometry("600x400")
    root.configure(bg="#2c3e50")
    
    # منع إغلاق النافذة بالخطأ
    root.protocol("WM_DELETE_WINDOW", lambda: None)
    
    # الإطار الرئيسي
    main_frame = tk.Frame(root, bg="#2c3e50", padx=30, pady=30)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # العنوان
    title = tk.Label(
        main_frame,
        text="🔍 نظام البحث والفلترة المباشر",
        font=("Arial", 20, "bold"),
        fg="#ecf0f1", bg="#2c3e50"
    )
    title.pack(pady=(0, 20))
    
    # معلومات الحالة
    status_frame = tk.Frame(main_frame, bg="#34495e", relief="raised", bd=2)
    status_frame.pack(fill=tk.X, pady=(0, 20))
    
    status_title = tk.Label(
        status_frame,
        text="📊 حالة النظام",
        font=("Arial", 14, "bold"),
        fg="#e74c3c", bg="#34495e"
    )
    status_title.pack(pady=10)
    
    status_label = tk.Label(
        status_frame,
        text="جاري التحقق من الاتصال...",
        font=("Arial", 12),
        fg="#bdc3c7", bg="#34495e"
    )
    status_label.pack(pady=(0, 10))
    
    # متغيرات النظام
    sheets_manager = None
    current_user = None
    
    def check_system_status():
        """فحص حالة النظام"""
        nonlocal sheets_manager, current_user
        
        try:
            # محاولة الاتصال بـ Google Sheets
            sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
            
            if sheets_manager.connect():
                # فحص البيانات
                data = sheets_manager.get_all_items_raw()
                
                # إعداد مستخدم افتراضي
                current_user = {'username': 'admin', 'user_type': 'admin'}
                
                status_text = f"""✅ النظام جاهز للعمل
📊 البيانات المتاحة: {len(data)} عنصر
🔗 الاتصال: متصل بـ Google Sheets
👤 المستخدم: {current_user['username']} ({current_user['user_type']})

🎯 يمكنك الآن فتح نافذة الفلاتر والاستفادة من جميع الميزات"""
                
                status_label.config(text=status_text, fg="#2ecc71")
                
                # تفعيل الأزرار
                filter_btn.config(state="normal", bg="#27ae60")
                login_btn.config(state="normal", bg="#3498db")
                
                return True
                
            else:
                status_label.config(text="❌ فشل الاتصال بـ Google Sheets", fg="#e74c3c")
                return False
                
        except Exception as e:
            status_label.config(text=f"❌ خطأ في النظام: {e}", fg="#e74c3c")
            return False
    
    def open_filter_window():
        """فتح نافذة الفلاتر"""
        if not sheets_manager:
            messagebox.showerror("خطأ", "يجب فحص حالة النظام أولاً!")
            return
        
        try:
            print("🔓 فتح نافذة الفلاتر المباشرة...")
            
            # فتح النافذة
            filter_window = open_basic_filter_window(root, sheets_manager, current_user)
            
            if filter_window:
                print("✅ تم فتح نافذة الفلاتر بنجاح!")
                
                messagebox.showinfo("نجح! 🎉", 
                    f"تم فتح نافذة الفلاتر بنجاح!\\n\\n"
                    f"🎛️ الفلاتر المتاحة:\\n"
                    f"• فلتر التصنيف\\n"
                    f"• فلتر المشروع\\n"
                    f"• أزرار المسح والتحديث\\n\\n"
                    f"💡 جرب الفلاتر وراقب التحديث الفوري!")
                    
        except Exception as e:
            print(f"❌ خطأ: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("خطأ", f"فشل في فتح نافذة الفلاتر:\\n{e}")
    
    def open_login_window():
        """فتح نافذة تسجيل الدخول (مؤقتاً غير متاح)"""
        messagebox.showinfo("قريباً", "نافذة تسجيل الدخول ستكون متاحة قريباً!\\nيمكنك استخدام الفلاتر الآن بالمستخدم الافتراضي.")
    
    def handle_login_success(user):
        """معالجة نجاح تسجيل الدخول"""
        nonlocal current_user
        current_user = user
        
        status_text = f"""✅ تم تسجيل الدخول بنجاح
👤 المستخدم: {user.get('username', 'غير معروف')}
🏷️ النوع: {user.get('user_type', 'غير محدد')}
📊 البيانات: متاحة للاستخدام

🎯 يمكنك الآن فتح نافذة الفلاتر"""
        
        status_label.config(text=status_text, fg="#2ecc71")
    
    # الأزرار
    buttons_frame = tk.Frame(main_frame, bg="#2c3e50")
    buttons_frame.pack(pady=30)
    
    # زر فحص النظام
    check_btn = tk.Button(
        buttons_frame,
        text="🔍 فحص حالة النظام",
        command=check_system_status,
        font=("Arial", 14, "bold"),
        bg="#f39c12", fg="white",
        padx=25, pady=15,
        relief="flat", cursor="hand2"
    )
    check_btn.pack(side=tk.LEFT, padx=10)
    
    # زر فتح الفلاتر
    filter_btn = tk.Button(
        buttons_frame,
        text="🎛️ فتح نافذة الفلاتر",
        command=open_filter_window,
        font=("Arial", 14, "bold"),
        bg="#95a5a6", fg="white",
        padx=25, pady=15,
        relief="flat", cursor="hand2",
        state="disabled"
    )
    filter_btn.pack(side=tk.LEFT, padx=10)
    
    # زر تسجيل الدخول
    login_btn = tk.Button(
        buttons_frame,
        text="👤 تسجيل الدخول",
        command=open_login_window,
        font=("Arial", 14, "bold"),
        bg="#95a5a6", fg="white",
        padx=25, pady=15,
        relief="flat", cursor="hand2",
        state="disabled"
    )
    login_btn.pack(side=tk.LEFT, padx=10)
    
    # زر الإغلاق
    close_btn = tk.Button(
        buttons_frame,
        text="❌ إغلاق",
        command=root.destroy,
        font=("Arial", 14, "bold"),
        bg="#e74c3c", fg="white",
        padx=25, pady=15,
        relief="flat", cursor="hand2"
    )
    close_btn.pack(side=tk.LEFT, padx=10)
    
    # تعليمات الاستخدام
    instructions_frame = tk.Frame(main_frame, bg="#34495e", relief="raised", bd=2)
    instructions_frame.pack(fill=tk.X, pady=(20, 0))
    
    inst_title = tk.Label(
        instructions_frame,
        text="📋 تعليمات الاستخدام",
        font=("Arial", 14, "bold"),
        fg="#e67e22", bg="#34495e"
    )
    inst_title.pack(pady=10)
    
    instructions = """
🔥 خطوات الاستخدام:

1️⃣ اضغط "فحص حالة النظام" للتأكد من الاتصال
2️⃣ بعد نجاح الفحص، اضغط "فتح نافذة الفلاتر"
3️⃣ جرب الفلاتر وراقب التحديث الفوري للبيانات
4️⃣ استخدم "تسجيل الدخول" للمستخدمين المسجلين

⚡ ميزة خاصة: هذا المشغل يتجاوز جميع مشاكل التكامل ويفتح الفلاتر مباشرة!
    """
    
    inst_label = tk.Label(
        instructions_frame,
        text=instructions,
        font=("Arial", 10),
        fg="#bdc3c7", bg="#34495e",
        justify=tk.LEFT
    )
    inst_label.pack(padx=15, pady=(0, 15))
    
    print("✅ مشغل الفلاتر المباشر جاهز!")
    print("👆 اضغط 'فحص حالة النظام' للبدء")
    
    # بدء التطبيق
    root.mainloop()

if __name__ == "__main__":
    create_direct_filter_launcher()