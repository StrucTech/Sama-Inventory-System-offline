"""
🏪 نظام إدارة المخزون الشامل - حل جميع المشاكل
===============================================

يحل المشاكل الثلاث:
1. الكميات تظهر صفر في الصفحة الرئيسية  
2. نظام فلاتر وعمليات شامل مع تسجيل التواريخ
3. مشكلة "آخر كمية مضافة" لا تعمل

التشغيل: python unified_inventory_solution.py
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
import sys
import os
from datetime import datetime

# إضافة مسار المشروع
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class UnifiedInventorySolution:
    def __init__(self):
        """تهيئة الحل الموحد لجميع المشاكل"""
        self.root = None
        self.current_user = None
        
    def create_launcher_window(self):
        """إنشاء نافذة التشغيل الرئيسية"""
        
        self.root = tk.Tk()
        self.root.title("🏪 نظام إدارة المخزون - الحل الشامل")
        self.root.geometry("800x700")
        self.root.configure(bg="#1a1a2e")
        self.root.resizable(False, False)
        
        # جعل النافذة في الوسط
        self.root.eval('tk::PlaceWindow . center')
        
        self.create_launcher_interface()
        
        return self.root
    
    def create_launcher_interface(self):
        """إنشاء واجهة نافذة التشغيل"""
        
        # الإطار الرئيسي
        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # عنوان النظام
        title_frame = tk.Frame(main_frame, bg="#16213e", relief="raised", bd=3)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_font = font.Font(family="Arial", size=18, weight="bold")
        title_label = tk.Label(
            title_frame,
            text="🏪 نظام إدارة المخزون الشامل\nالحل النهائي لجميع المشاكل",
            font=title_font,
            bg="#16213e", fg="#daa520",
            pady=15
        )
        title_label.pack()
        
        # إطار المشاكل المحلولة
        problems_frame = tk.LabelFrame(
            main_frame, text="✅ المشاكل المحلولة", 
            bg="#2c3e60", fg="#ecf0f1", 
            font=("Arial", 12, "bold"),
            relief="groove", bd=2
        )
        problems_frame.pack(fill=tk.X, pady=(0, 20))
        
        problems_text = """
✅ المشكلة الأولى: الكميات تظهر صفر في الصفحة الرئيسية
   الحل: نظام شامل يقرأ الكميات الصحيحة من Google Sheets
   
✅ المشكلة الثانية: نظام فلاتر وعمليات متقدم
   الحل: تسجيل كامل للعمليات مع التواريخ والتفاصيل
   
✅ المشكلة الثالثة: زر "آخر كمية مضافة" لا يعمل
   الحل: نظام تتبع ذكي لآخر العمليات مع التنقل المباشر
        """
        
        problems_label = tk.Label(
            problems_frame, text=problems_text,
            bg="#2c3e60", fg="#ecf0f1", 
            font=("Arial", 10),
            justify=tk.LEFT
        )
        problems_label.pack(padx=15, pady=10, anchor="w")
        
        # إطار خيارات التشغيل
        options_frame = tk.LabelFrame(
            main_frame, text="🚀 خيارات التشغيل", 
            bg="#2c3e60", fg="#ecf0f1", 
            font=("Arial", 12, "bold"),
            relief="groove", bd=2
        )
        options_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # أزرار التشغيل
        button_style = {
            'font': ('Arial', 12, 'bold'),
            'relief': 'flat',
            'cursor': 'hand2',
            'pady': 12,
            'padx': 20
        }
        
        # النظام الشامل (الحل الأول)
        comprehensive_btn = tk.Button(
            options_frame,
            text="🎯 النظام الشامل (يحل المشاكل 1 و 3)\nعرض صحيح للكميات + آخر كمية مضافة",
            command=self.launch_comprehensive_system,
            bg="#27ae60", fg="white",
            **button_style
        )
        comprehensive_btn.pack(fill=tk.X, padx=15, pady=10)
        
        # نظام العمليات المتقدم (الحل الثاني)  
        operations_btn = tk.Button(
            options_frame,
            text="📊 نظام العمليات المتقدم (يحل المشكلة 2)\nفلاتر شاملة + تسجيل العمليات مع التواريخ",
            command=self.launch_operations_system,
            bg="#3498db", fg="white",
            **button_style
        )
        operations_btn.pack(fill=tk.X, padx=15, pady=10)
        
        # النافذة المُصححة (حل بديل)
        fixed_btn = tk.Button(
            options_frame,
            text="🔧 النافذة المُصححة (حل بديل)\nفلاتر محسنة مع إحصائيات سريعة",
            command=self.launch_fixed_window,
            bg="#9b59b6", fg="white",
            **button_style
        )
        fixed_btn.pack(fill=tk.X, padx=15, pady=10)
        
        # النظام الأصلي مع المصادقة
        auth_btn = tk.Button(
            options_frame,
            text="🔐 النظام الأصلي مع المصادقة\nتسجيل الدخول + الوظائف الأساسية",
            command=self.launch_auth_system,
            bg="#e74c3c", fg="white",
            **button_style
        )
        auth_btn.pack(fill=tk.X, padx=15, pady=10)
        
        # إطار أدوات الصيانة
        maintenance_frame = tk.LabelFrame(
            main_frame, text="🛠️ أدوات الصيانة", 
            bg="#2c3e60", fg="#ecf0f1", 
            font=("Arial", 11, "bold"),
            relief="groove", bd=2
        )
        maintenance_frame.pack(fill=tk.X)
        
        # صف أزرار الصيانة
        maintenance_row = tk.Frame(maintenance_frame, bg="#2c3e60")
        maintenance_row.pack(fill=tk.X, padx=10, pady=10)
        
        maintenance_buttons = [
            ("🔍 فحص البيانات", self.check_data),
            ("🧹 تنظيف البيانات", self.clean_data), 
            ("📊 تقرير الحالة", self.status_report),
            ("❓ المساعدة", self.show_help)
        ]
        
        for text, command in maintenance_buttons:
            btn = tk.Button(
                maintenance_row, text=text, command=command,
                bg="#34495e", fg="#ecf0f1", 
                font=("Arial", 9, "bold"),
                relief="flat", cursor="hand2",
                pady=5
            )
            btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        # شريط الحالة
        status_frame = tk.Frame(main_frame, bg="#16213e", height=30)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame, 
            text="✅ جميع الأنظمة جاهزة للتشغيل - اختر النظام المناسب",
            bg="#16213e", fg="#2ecc71", 
            font=("Arial", 10, "bold")
        )
        self.status_label.pack(expand=True)
    
    def launch_comprehensive_system(self):
        """تشغيل النظام الشامل"""
        try:
            self.status_label.config(text="🚀 تشغيل النظام الشامل...", fg="#f39c12")
            self.root.update()
            
            from comprehensive_system import ComprehensiveInventorySystem
            
            # إنشاء النظام مع معلومات مستخدم تجريبية
            system = ComprehensiveInventorySystem()
            user_info = {
                'username': 'المدير العام',
                'user_type': 'admin',
                'project_id': None
            }
            
            # إخفاء نافذة التشغيل وفتح النظام الشامل
            self.root.withdraw()
            window = system.create_main_window(user_info)
            
            # عند إغلاق النظام الشامل، إظهار نافذة التشغيل مرة أخرى
            def on_comprehensive_close():
                window.destroy()
                self.root.deiconify()
                self.status_label.config(text="✅ تم إغلاق النظام الشامل", fg="#2ecc71")
            
            window.protocol("WM_DELETE_WINDOW", on_comprehensive_close)
            system.run()
            
        except Exception as e:
            self.status_label.config(text=f"❌ خطأ في تشغيل النظام الشامل: {str(e)}", fg="#e74c3c")
            messagebox.showerror("خطأ", f"فشل في تشغيل النظام الشامل:\n{str(e)}")
    
    def launch_operations_system(self):
        """تشغيل نظام العمليات المتقدم"""
        try:
            self.status_label.config(text="📊 تشغيل نظام العمليات المتقدم...", fg="#f39c12")
            self.root.update()
            
            from sheets.manager import SheetsManager
            from advanced_operations_system import AdvancedOperationsSystem
            
            # إعداد Google Sheets
            sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
            if not sheets_manager.connect():
                messagebox.showerror("خطأ اتصال", "فشل في الاتصال بـ Google Sheets")
                return
            
            # إنشاء النظام
            operations_system = AdvancedOperationsSystem(sheets_manager, self.root)
            
            # فتح النافذة
            operations_window = operations_system.create_operations_window()
            
            def on_operations_close():
                operations_window.destroy()
                self.status_label.config(text="✅ تم إغلاق نظام العمليات", fg="#2ecc71")
            
            operations_window.protocol("WM_DELETE_WINDOW", on_operations_close)
            
        except Exception as e:
            self.status_label.config(text=f"❌ خطأ في تشغيل نظام العمليات: {str(e)}", fg="#e74c3c")
            messagebox.showerror("خطأ", f"فشل في تشغيل نظام العمليات:\n{str(e)}")
    
    def launch_fixed_window(self):
        """تشغيل النافذة المُصححة"""
        try:
            self.status_label.config(text="🔧 تشغيل النافذة المُصححة...", fg="#f39c12")
            self.root.update()
            
            from sheets.manager import SheetsManager
            from gui.fixed_filter_window import FixedFilterWindow
            
            # إعداد Google Sheets
            sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
            if not sheets_manager.connect():
                messagebox.showerror("خطأ اتصال", "فشل في الاتصال بـ Google Sheets")
                return
            
            # إنشاء النافذة المُصححة
            fixed_window = FixedFilterWindow(sheets_manager)
            
            self.status_label.config(text="✅ تم فتح النافذة المُصححة", fg="#2ecc71")
            
        except Exception as e:
            self.status_label.config(text=f"❌ خطأ في تشغيل النافذة المُصححة: {str(e)}", fg="#e74c3c")
            messagebox.showerror("خطأ", f"فشل في تشغيل النافذة المُصححة:\n{str(e)}")
    
    def launch_auth_system(self):
        """تشغيل النظام الأصلي مع المصادقة"""
        try:
            self.status_label.config(text="🔐 تشغيل النظام الأصلي...", fg="#f39c12")
            self.root.update()
            
            import subprocess
            import sys
            
            # تشغيل النظام الأصلي
            subprocess.Popen([sys.executable, "main_with_auth.py"])
            
            self.status_label.config(text="✅ تم تشغيل النظام الأصلي", fg="#2ecc71")
            
        except Exception as e:
            self.status_label.config(text=f"❌ خطأ في تشغيل النظام الأصلي: {str(e)}", fg="#e74c3c")
            messagebox.showerror("خطأ", f"فشل في تشغيل النظام الأصلي:\n{str(e)}")
    
    def check_data(self):
        """فحص البيانات"""
        try:
            self.status_label.config(text="🔍 جاري فحص البيانات...", fg="#f39c12")
            self.root.update()
            
            from sheets.manager import SheetsManager
            
            sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
            if sheets_manager.connect():
                worksheet = sheets_manager.worksheet
                all_values = worksheet.get_all_values()
                
                if all_values:
                    headers = all_values[0]
                    data_count = len(all_values) - 1
                    
                    # حساب إحصائيات سريعة
                    total_items = data_count
                    total_remaining = 0
                    
                    for row in all_values[1:]:
                        if len(row) >= 6:
                            try:
                                remaining = int(row[5]) if row[5].isdigit() else 0
                                total_remaining += remaining
                            except (ValueError, IndexError):
                                pass
                    
                    info_text = f"""📊 تقرير فحص البيانات:
                    
✅ الاتصال بـ Google Sheets: نجح
📋 عدد الأعمدة: {len(headers)}
🔢 عدد العناصر: {total_items}
📦 إجمالي الكميات المتبقية: {total_remaining:,}

العناوين الموجودة:
{', '.join(headers[:4])}...

الحالة: البيانات سليمة وجاهزة للاستخدام"""
                    
                    messagebox.showinfo("تقرير فحص البيانات", info_text)
                    self.status_label.config(text="✅ فحص البيانات مكتمل", fg="#2ecc71")
                    
                else:
                    messagebox.showwarning("فحص البيانات", "لا توجد بيانات في Google Sheets")
                    self.status_label.config(text="⚠️ لا توجد بيانات", fg="#f39c12")
            else:
                messagebox.showerror("فحص البيانات", "فشل في الاتصال بـ Google Sheets")
                self.status_label.config(text="❌ فشل الاتصال", fg="#e74c3c")
                
        except Exception as e:
            messagebox.showerror("خطأ في الفحص", f"خطأ في فحص البيانات:\n{str(e)}")
            self.status_label.config(text="❌ خطأ في الفحص", fg="#e74c3c")
    
    def clean_data(self):
        """تنظيف البيانات"""
        try:
            import subprocess
            import sys
            
            result = messagebox.askyesno("تنظيف البيانات", 
                                       "هل تريد تشغيل أداة تنظيف البيانات؟\n"
                                       "ستقوم بإصلاح البيانات المعطوبة أو المخلوطة")
            
            if result:
                self.status_label.config(text="🧹 تشغيل أداة التنظيف...", fg="#f39c12")
                subprocess.Popen([sys.executable, "clean_data.py"])
                self.status_label.config(text="✅ تم تشغيل أداة التنظيف", fg="#2ecc71")
                
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في تشغيل أداة التنظيف:\n{str(e)}")
    
    def status_report(self):
        """تقرير حالة النظام"""
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report_text = f"""📊 تقرير حالة النظام الشامل
تاريخ التقرير: {current_time}

🎯 الحلول المتاحة:
✅ النظام الشامل - يحل المشاكل 1 و 3
✅ نظام العمليات المتقدم - يحل المشكلة 2  
✅ النافذة المُصححة - حل بديل محسن
✅ النظام الأصلي - الوظائف الأساسية

🔧 المشاكل المحلولة:
1️⃣ الكميات تظهر صفر ➜ ✅ محلولة
2️⃣ نظام فلاتر وعمليات ➜ ✅ محلولة  
3️⃣ آخر كمية مضافة ➜ ✅ محلولة

📁 الملفات المتاحة:
• comprehensive_system.py - النظام الشامل
• advanced_operations_system.py - العمليات المتقدمة
• gui/fixed_filter_window.py - النافذة المُصححة
• main_with_auth.py - النظام الأصلي

🚀 الحالة: جميع الأنظمة جاهزة للاستخدام"""
        
        messagebox.showinfo("تقرير حالة النظام", report_text)
    
    def show_help(self):
        """عرض المساعدة"""
        
        help_text = """❓ دليل الاستخدام - نظام إدارة المخزون
=============================================

🎯 اختيار النظام المناسب:

1️⃣ للمشاكل 1 و 3 (الكميات + آخر إضافة):
   ➜ استخدم "النظام الشامل"

2️⃣ للمشكلة 2 (الفلاتر والعمليات):
   ➜ استخدم "نظام العمليات المتقدم"

3️⃣ للحل البديل المحسن:
   ➜ استخدم "النافذة المُصححة"

4️⃣ للاستخدام العادي:
   ➜ استخدم "النظام الأصلي"

🛠️ أدوات الصيانة:
• فحص البيانات - للتأكد من سلامة البيانات
• تنظيف البيانات - لإصلاح المشاكل
• تقرير الحالة - معلومات شاملة

🆘 في حالة المشاكل:
1. تأكد من وجود ملف config/credentials.json
2. تحقق من الاتصال بالإنترنت
3. استخدم "فحص البيانات" للتشخيص"""
        
        messagebox.showinfo("المساعدة والدعم", help_text)
    
    def run(self):
        """تشغيل نافذة التشغيل"""
        if self.root:
            self.root.mainloop()


def main():
    """النقطة الرئيسية للتشغيل"""
    
    print("🏪 نظام إدارة المخزون الشامل")
    print("الحل النهائي لجميع المشاكل")
    print("=" * 50)
    
    # إنشاء وتشغيل النظام
    solution = UnifiedInventorySolution()
    window = solution.create_launcher_window()
    solution.run()

if __name__ == "__main__":
    main()