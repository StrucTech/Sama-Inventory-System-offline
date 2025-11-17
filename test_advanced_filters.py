#!/usr/bin/env python3
"""
🔥 تجربة النظام المتقدم للفلاتر
جميع الفلاتر المطلوبة: التاريخ، العنصر، التصنيف، الكمية، المشروع
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# إضافة مسار المشروع
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.advanced_filter_window import open_advanced_filter_window
from sheets.manager import SheetsManager

def main():
    """التشغيل المباشر للنظام المتقدم"""
    
    print("🚀 تشغيل النظام المتقدم للفلاتر...")
    
    try:
        # إنشاء النافذة الرئيسية
        root = tk.Tk()
        root.title("🔥 النظام المتقدم للفلاتر - تجربة مباشرة")
        root.geometry("500x300")
        root.configure(bg="#2c3e50")
        
        # العنوان
        title = tk.Label(
            root,
            text="🔥 النظام المتقدم للفلاتر",
            font=("Arial", 20, "bold"),
            fg="#f1c40f", bg="#2c3e50"
        )
        title.pack(pady=30)
        
        # الوصف
        desc_text = """
النظام الجديد يشمل جميع الفلاتر المطلوبة:

📅 فلتر التاريخ - آخر تحديث للعناصر
📦 فلتر العنصر - البحث باسم العنصر
🏷️ فلتر التصنيف - نوع التصنيف
🎯 فلتر المشروع - رقم المشروع
📊 فلتر الكمية المتقدم - مع عمليات المقارنة

✨ ميزات إضافية:
• إحصائيات تفصيلية فورية
• ألوان تمييز للكميات (منخفض/متوسط/عالي)
• فرز وترتيب متقدم
• تصدير النتائج المفلترة
        """
        
        desc = tk.Label(
            root,
            text=desc_text,
            font=("Arial", 11),
            fg="#ecf0f1", bg="#2c3e50",
            justify=tk.LEFT
        )
        desc.pack(pady=20)
        
        # حالة الاتصال
        status_label = tk.Label(
            root,
            text="🔄 جاري الاتصال بـ Google Sheets...",
            font=("Arial", 12, "bold"),
            fg="#f39c12", bg="#2c3e50"
        )
        status_label.pack(pady=10)
        
        # تحديث حالة الاتصال
        root.update()
        
        # الاتصال بـ Google Sheets
        print("🔗 اتصال بـ Google Sheets...")
        sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
        
        if not sheets_manager.connect():
            status_label.config(text="❌ فشل في الاتصال", fg="#e74c3c")
            messagebox.showerror("خطأ", "فشل في الاتصال بـ Google Sheets!")
            return
        
        # تحميل البيانات
        data = sheets_manager.get_all_items_raw()
        status_label.config(text=f"✅ تم الاتصال - {len(data)} عنصر", fg="#2ecc71")
        print(f"✅ تم تحميل {len(data)} عنصر")
        
        # مستخدم افتراضي
        current_user = {
            'username': 'admin',
            'user_type': 'admin'
        }
        
        print(f"👤 دخول كمستخدم: {current_user['username']}")
        
        # دالة فتح النظام المتقدم
        def open_advanced_system():
            try:
                print("🎛️ فتح النظام المتقدم للفلاتر...")
                
                # فتح النظام المتقدم
                filter_window = open_advanced_filter_window(
                    parent=root,
                    sheets_manager=sheets_manager,
                    current_user=current_user
                )
                
                if filter_window:
                    print("🎉 تم فتح النظام المتقدم بنجاح!")
                    
                    messagebox.showinfo("مرحباً بالنظام المتقدم! 🚀",
                        "تم فتح النظام المتقدم للفلاتر بنجاح!\n\n"
                        "🎛️ الفلاتر المتاحة:\n"
                        "• فلتر التاريخ 📅\n"
                        "• فلتر العنصر 📦\n"
                        "• فلتر التصنيف 🏷️\n" 
                        "• فلتر المشروع 🎯\n"
                        "• فلتر الكمية المتقدم 📊\n\n"
                        "✨ جميع الفلاتر تعمل بشكل فوري ومتقدم!\n"
                        "جرب الآن واستمتع بالتجربة!")
                else:
                    messagebox.showerror("خطأ", "فشل في إنشاء النظام المتقدم!")
                    
            except Exception as e:
                print(f"❌ خطأ: {e}")
                import traceback
                traceback.print_exc()
                messagebox.showerror("خطأ", f"حدث خطأ في النظام المتقدم:\n{str(e)}")
        
        # زر فتح النظام المتقدم
        open_btn = tk.Button(
            root,
            text="🚀 تشغيل النظام المتقدم الآن!",
            command=open_advanced_system,
            font=("Arial", 16, "bold"),
            bg="#e74c3c", fg="white",
            padx=40, pady=20,
            relief="flat", cursor="hand2"
        )
        open_btn.pack(pady=30)
        
        print("🎉 تطبيق التجربة جاهز!")
        
        # تشغيل النافذة
        root.mainloop()
        
    except Exception as e:
        print(f"💥 خطأ في التطبيق: {e}")
        import traceback
        traceback.print_exc()
        
        messagebox.showerror("خطأ",
            f"حدث خطأ في تطبيق التجربة:\n{str(e)}\n\n"
            f"تأكد من:\n"
            f"• وجود ملفات المشروع\n"
            f"• صحة إعدادات Google Sheets\n"
            f"• اتصال الإنترنت")

if __name__ == "__main__":
    main()