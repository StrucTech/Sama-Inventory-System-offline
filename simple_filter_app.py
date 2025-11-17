#!/usr/bin/env python3
"""
🔥 تطبيق الفلاتر المبسط - بدون تسجيل دخول
حل فوري ومباشر لمشكلة الفلاتر
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# إضافة مسار المشروع
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.basic_filter_window import open_basic_filter_window
from sheets.manager import SheetsManager

class SimpleFilterApp:
    """تطبيق الفلاتر المبسط بدون تسجيل دخول"""
    
    def __init__(self):
        self.root = None
        self.sheets_manager = None
        # مستخدم افتراضي فوري
        self.current_user = {'username': 'admin', 'user_type': 'admin'}
        
    def start(self):
        """بدء التطبيق المبسط"""
        
        print("🚀 بدء التطبيق المبسط للفلاتر...")
        
        # إنشاء النافذة الرئيسية
        self.root = tk.Tk()
        self.root.title("🔥 نظام الفلاتر المتطور - دخول مباشر")
        self.root.geometry("800x600")
        self.root.configure(bg="#2c3e50")
        
        # تصميم الواجهة
        self.create_interface()
        
        # بدء التشغيل
        self.root.mainloop()
    
    def create_interface(self):
        """إنشاء واجهة التطبيق"""
        
        # الإطار الرئيسي
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # العنوان الرئيسي
        title = tk.Label(
            main_frame,
            text="🔥 نظام الفلاتر المتطور",
            font=("Arial", 24, "bold"),
            fg="#f1c40f", bg="#2c3e50"
        )
        title.pack(pady=(0, 10))
        
        # العنوان الفرعي
        subtitle = tk.Label(
            main_frame,
            text="دخول مباشر بدون تسجيل - جاهز للاستخدام فوراً!",
            font=("Arial", 14),
            fg="#ecf0f1", bg="#2c3e50"
        )
        subtitle.pack(pady=(0, 30))
        
        # معلومات المستخدم
        user_frame = tk.Frame(main_frame, bg="#34495e", relief="raised", bd=2)
        user_frame.pack(fill=tk.X, pady=(0, 30))
        
        user_title = tk.Label(
            user_frame,
            text="👤 معلومات المستخدم",
            font=("Arial", 14, "bold"),
            fg="#3498db", bg="#34495e"
        )
        user_title.pack(pady=10)
        
        user_info = f"المستخدم: {self.current_user['username']} | النوع: {self.current_user['user_type']} | الحالة: نشط ✅"
        user_label = tk.Label(
            user_frame,
            text=user_info,
            font=("Arial", 12),
            fg="#bdc3c7", bg="#34495e"
        )
        user_label.pack(pady=(0, 10))
        
        # منطقة الأزرار الرئيسية
        buttons_frame = tk.Frame(main_frame, bg="#2c3e50")
        buttons_frame.pack(pady=20)
        
        # زر الاتصال
        self.connect_btn = tk.Button(
            buttons_frame,
            text="🔗 اتصال Google Sheets",
            command=self.connect_sheets,
            font=("Arial", 14, "bold"),
            bg="#3498db", fg="white",
            padx=30, pady=15,
            relief="flat", cursor="hand2"
        )
        self.connect_btn.pack(side=tk.LEFT, padx=10)
        
        # حالة الاتصال
        self.status_label = tk.Label(
            buttons_frame,
            text="⚪ غير متصل",
            font=("Arial", 12, "bold"),
            fg="#e74c3c", bg="#2c3e50"
        )
        self.status_label.pack(side=tk.LEFT, padx=20)
        
        # زر الفلاتر الرئيسي
        self.filter_btn = tk.Button(
            buttons_frame,
            text="🎛️ فتح الفلاتر المتطورة",
            command=self.open_filters,
            font=("Arial", 14, "bold"),
            bg="#95a5a6", fg="white",
            padx=30, pady=15,
            relief="flat", cursor="hand2",
            state="disabled"
        )
        self.filter_btn.pack(side=tk.LEFT, padx=10)
        
        # منطقة المعلومات
        info_frame = tk.Frame(main_frame, bg="#34495e", relief="raised", bd=2)
        info_frame.pack(fill=tk.BOTH, expand=True, pady=(30, 0))
        
        info_title = tk.Label(
            info_frame,
            text="📋 تعليمات الاستخدام",
            font=("Arial", 16, "bold"),
            fg="#e67e22", bg="#34495e"
        )
        info_title.pack(pady=15)
        
        instructions = """
🎯 خطوات الاستخدام البسيطة:

1️⃣ اضغط "اتصال Google Sheets" للاتصال بقاعدة البيانات
2️⃣ انتظر رسالة "تم الاتصال بنجاح" 
3️⃣ اضغط "فتح الفلاتر المتطورة" لبدء الاستخدام
4️⃣ استمتع بتجربة الفلترة المتقدمة والفورية!

✨ الميزات المتاحة:
• فلتر التصنيف التفاعلي
• فلتر المشروع الذكي  
• تحديث فوري للنتائج
• أدوات المسح والتحديث
• واجهة سهلة ومريحة

💡 نصيحة: جميع الفلاتر تعمل بشكل فوري ومباشر!
لا حاجة لأي إعدادات إضافية أو تسجيل دخول معقد.

🚀 اضغط الآن وابدأ رحلتك مع أقوى نظام فلاتر!
        """
        
        info_text = tk.Label(
            info_frame,
            text=instructions,
            font=("Arial", 11),
            fg="#bdc3c7", bg="#34495e",
            justify=tk.LEFT
        )
        info_text.pack(padx=20, pady=(0, 20))
        
        print("✅ تم إنشاء واجهة التطبيق المبسط")
    
    def connect_sheets(self):
        """الاتصال بـ Google Sheets"""
        
        try:
            print("🔗 بدء الاتصال بـ Google Sheets...")
            
            # تحديث النص
            self.status_label.config(text="🔄 جاري الاتصال...", fg="#f39c12")
            self.connect_btn.config(state="disabled", text="🔄 جاري الاتصال...")
            self.root.update()
            
            # إنشاء الاتصال
            self.sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
            
            if self.sheets_manager.connect():
                # تحميل البيانات للتأكد
                data = self.sheets_manager.get_all_items_raw()
                
                # تحديث الواجهة
                self.status_label.config(
                    text=f"🟢 متصل - {len(data)} عنصر",
                    fg="#27ae60"
                )
                self.connect_btn.config(
                    state="normal",
                    text="✅ تم الاتصال",
                    bg="#27ae60"
                )
                self.filter_btn.config(
                    state="normal",
                    bg="#e74c3c"
                )
                
                print(f"✅ تم الاتصال بنجاح - {len(data)} عنصر متاح")
                
                messagebox.showinfo("نجح الاتصال! 🎉",
                    f"تم الاتصال بـ Google Sheets بنجاح!\n\n"
                    f"📊 عدد العناصر المحملة: {len(data)}\n"
                    f"👤 المستخدم: {self.current_user['username']}\n"
                    f"🔐 الصلاحيات: {self.current_user['user_type']}\n\n"
                    f"🚀 الآن يمكنك فتح الفلاتر والاستمتاع بالاستخدام!")
                
            else:
                raise Exception("فشل في الاتصال بـ Google Sheets")
                
        except Exception as e:
            print(f"❌ خطأ في الاتصال: {e}")
            
            self.status_label.config(
                text="🔴 فشل الاتصال",
                fg="#e74c3c"
            )
            self.connect_btn.config(
                state="normal",
                text="🔗 إعادة المحاولة",
                bg="#e74c3c"
            )
            
            messagebox.showerror("خطأ في الاتصال",
                f"فشل في الاتصال بـ Google Sheets!\n\n"
                f"السبب: {str(e)}\n\n"
                f"تأكد من:\n"
                f"• وجود ملف config/credentials.json\n"
                f"• صحة بيانات الاعتماد\n"
                f"• اتصال الإنترنت\n"
                f"• صلاحيات Google Sheets API")
    
    def open_filters(self):
        """فتح نظام الفلاتر المتطور"""
        
        if not self.sheets_manager:
            messagebox.showwarning("تحذير",
                "يجب الاتصال بـ Google Sheets أولاً!\n"
                "اضغط زر 'اتصال Google Sheets' أولاً.")
            return
        
        try:
            print("🎛️ فتح نظام الفلاتر المتطور...")
            
            # فتح نافذة الفلاتر
            filter_window = open_basic_filter_window(
                parent=self.root,
                sheets_manager=self.sheets_manager,
                current_user=self.current_user
            )
            
            if filter_window:
                print("🎉 تم فتح الفلاتر بنجاح!")
                
                messagebox.showinfo("مرحباً بالفلاتر! 🚀",
                    "تم فتح نظام الفلاتر المتطور بنجاح!\n\n"
                    "🎛️ الميزات المتاحة الآن:\n"
                    "• فلتر التصنيف (Category) - قائمة منسدلة\n"
                    "• فلتر المشروع (Project) - قائمة منسدلة\n"
                    "• تحديث فوري عند كل تغيير\n"
                    "• زر مسح الفلاتر\n"
                    "• زر تحديث البيانات\n\n"
                    "💡 جرب تغيير الفلاتر واستمتع بالنتائج الفورية!")
            else:
                raise Exception("فشل في إنشاء نافذة الفلاتر")
                
        except Exception as e:
            print(f"❌ خطأ في فتح الفلاتر: {e}")
            import traceback
            traceback.print_exc()
            
            messagebox.showerror("خطأ في الفلاتر",
                f"فشل في فتح نظام الفلاتر!\n\n"
                f"التفاصيل: {str(e)}\n\n"
                f"حاول:\n"
                f"• إعادة الاتصال بـ Google Sheets\n"
                f"• إعادة تشغيل التطبيق\n"
                f"• التحقق من ملفات المشروع")

def main():
    """الدالة الرئيسية"""
    
    try:
        print("🔥 بدء تطبيق الفلاتر المبسط...")
        
        app = SimpleFilterApp()
        app.start()
        
        print("✅ تم إغلاق التطبيق بنجاح")
        
    except Exception as e:
        print(f"💥 خطأ في التطبيق: {e}")
        import traceback
        traceback.print_exc()
        
        messagebox.showerror("خطأ في التطبيق",
            f"حدث خطأ غير متوقع:\n{str(e)}\n\n"
            f"يرجى إعادة تشغيل التطبيق أو التواصل مع الدعم الفني.")

if __name__ == "__main__":
    main()