"""
🔧 إصلاح مشكلة بيانات الفلاتر وتواريخ العمليات
==================================================

المشاكل المطلوب حلها:
1. البيانات في قوائم الفلاتر غير مضبوطة
2. عدم ظهور تواريخ العمليات (إدخال/إخراج)

الحلول المتاحة:
"""

import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

# إضافة مسار المشروع
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_solution_selector():
    """إنشاء نافذة اختيار الحل"""
    
    root = tk.Tk()
    root.title("🔧 إصلاح مشاكل الفلاتر والتواريخ")
    root.geometry("700x500")
    root.configure(bg="#2c3e60")
    root.resizable(False, False)
    
    # العنوان
    title_label = tk.Label(
        root,
        text="🔧 إصلاح مشاكل الفلاتر وتواريخ العمليات",
        font=("Arial", 16, "bold"),
        bg="#2c3e60", fg="#ecf0f1",
        pady=20
    )
    title_label.pack()
    
    # وصف المشاكل
    problems_frame = tk.LabelFrame(
        root, text="❌ المشاكل المكتشفة", 
        bg="#34495e", fg="#e74c3c",
        font=("Arial", 12, "bold")
    )
    problems_frame.pack(fill=tk.X, padx=20, pady=10)
    
    problems_text = """
❌ المشكلة الأولى: البيانات في قوائم الفلاتر غير مضبوطة
   - قوائم التواريخ والعناصر والتصنيفات فارغة أو غير صحيحة
   - عدم استخراج البيانات بشكل صحيح من Google Sheets

❌ المشكلة الثانية: عدم ظهور تواريخ العمليات  
   - لا توجد تواريخ لعمليات الإدخال والإخراج
   - عدم وجود سجل للعمليات مع التواريخ
    """
    
    problems_label = tk.Label(
        problems_frame, text=problems_text,
        bg="#34495e", fg="#ecf0f1", 
        font=("Arial", 10), justify=tk.LEFT
    )
    problems_label.pack(padx=10, pady=10)
    
    # الحلول المتاحة
    solutions_frame = tk.LabelFrame(
        root, text="✅ الحلول المتاحة", 
        bg="#27ae60", fg="#ecf0f1",
        font=("Arial", 12, "bold")
    )
    solutions_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    # الحل الأول - النظام المحسن الجديد
    solution1_btn = tk.Button(
        solutions_frame,
        text="🚀 النظام المحسن الجديد\nيحل كلا المشكلتين + يضيف سجل العمليات",
        command=lambda: launch_enhanced_system(root),
        bg="#3498db", fg="white", font=("Arial", 12, "bold"),
        pady=10, relief="flat", cursor="hand2"
    )
    solution1_btn.pack(fill=tk.X, padx=10, pady=5)
    
    # الحل الثاني - إصلاح النافذة الحالية
    solution2_btn = tk.Button(
        solutions_frame,
        text="🔧 إصلاح النافذة الحالية\nيصحح البيانات في الفلاتر الموجودة",
        command=lambda: launch_fixed_window(root),
        bg="#27ae60", fg="white", font=("Arial", 12, "bold"),
        pady=10, relief="flat", cursor="hand2"
    )
    solution2_btn.pack(fill=tk.X, padx=10, pady=5)
    
    # الحل الثالث - النظام الشامل  
    solution3_btn = tk.Button(
        solutions_frame,
        text="🎯 النظام الشامل\nالحل الكامل لجميع المشاكل",
        command=lambda: launch_comprehensive_system(root),
        bg="#9b59b6", fg="white", font=("Arial", 12, "bold"),
        pady=10, relief="flat", cursor="hand2"
    )
    solution3_btn.pack(fill=tk.X, padx=10, pady=5)
    
    # فحص البيانات
    check_btn = tk.Button(
        solutions_frame,
        text="🔍 فحص البيانات الحالية\nللتشخيص والتحقق من المشكلة",
        command=lambda: check_current_data(root),
        bg="#f39c12", fg="white", font=("Arial", 11, "bold"),
        pady=8, relief="flat", cursor="hand2"
    )
    check_btn.pack(fill=tk.X, padx=10, pady=5)
    
    return root

def launch_enhanced_system(parent):
    """تشغيل النظام المحسن الجديد"""
    try:
        parent.withdraw()
        from enhanced_filters_operations import EnhancedFiltersWithOperations
        
        system = EnhancedFiltersWithOperations()
        window = system.create_window()
        
        def on_close():
            window.destroy()
            parent.deiconify()
        
        window.protocol("WM_DELETE_WINDOW", on_close)
        system.run()
        
    except Exception as e:
        messagebox.showerror("خطأ", f"فشل في تشغيل النظام المحسن:\n{str(e)}")
        parent.deiconify()

def launch_fixed_window(parent):
    """تشغيل النافذة المُصححة"""
    try:
        subprocess.Popen([sys.executable, "test_fixed_system.py"])
        messagebox.showinfo("تم التشغيل", "تم فتح النافذة المُصححة في نافذة منفصلة")
        
    except Exception as e:
        messagebox.showerror("خطأ", f"فشل في تشغيل النافذة المُصححة:\n{str(e)}")

def launch_comprehensive_system(parent):
    """تشغيل النظام الشامل"""
    try:
        subprocess.Popen([sys.executable, "comprehensive_system.py"])
        messagebox.showinfo("تم التشغيل", "تم فتح النظام الشامل في نافذة منفصلة")
        
    except Exception as e:
        messagebox.showerror("خطأ", f"فشل في تشغيل النظام الشامل:\n{str(e)}")

def check_current_data(parent):
    """فحص البيانات الحالية"""
    try:
        from sheets.manager import SheetsManager
        
        sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
        if sheets_manager.connect():
            
            # فحص بيانات المخزون
            all_values = sheets_manager.worksheet.get_all_values()
            headers = all_values[0] if all_values else []
            data_count = len(all_values) - 1 if len(all_values) > 1 else 0
            
            # فحص سجل النشاط
            activity_count = 0
            try:
                activity_sheet = sheets_manager.spreadsheet.worksheet('activity_log')
                activity_values = activity_sheet.get_all_values()
                activity_count = len(activity_values) - 1 if len(activity_values) > 1 else 0
            except:
                activity_count = 0
            
            # عرض النتائج
            result_text = f"""📊 نتائج فحص البيانات:

🗂️ بيانات المخزون:
   - الأعمدة: {len(headers)}
   - العناصر: {data_count}
   - العناوين: {', '.join(headers[:4])}...

⚡ سجل العمليات:
   - العمليات المسجلة: {activity_count}
   - الحالة: {'✅ موجود' if activity_count > 0 else '❌ غير موجود'}

🔍 التشخيص:
   {'✅ البيانات سليمة' if data_count > 0 else '❌ مشكلة في البيانات'}
   {'✅ سجل العمليات متاح' if activity_count > 0 else '⚠️ سجل العمليات مفقود'}

💡 التوصية:
   {'استخدم النظام المحسن الجديد للحصول على أفضل النتائج' if activity_count == 0 else 'جميع الأنظمة تعمل بشكل طبيعي'}"""
            
            messagebox.showinfo("نتائج الفحص", result_text)
            
        else:
            messagebox.showerror("خطأ", "فشل في الاتصال بـ Google Sheets")
            
    except Exception as e:
        messagebox.showerror("خطأ في الفحص", f"خطأ في فحص البيانات:\n{str(e)}")

def main():
    """الدالة الرئيسية"""
    
    print("🔧 أداة إصلاح مشاكل الفلاتر والتواريخ")
    print("=" * 50)
    
    root = create_solution_selector()
    root.mainloop()

if __name__ == "__main__":
    main()