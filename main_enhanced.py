"""
تطبيق إدارة المخزون مع الإحصائيات المحسّنة
نسخة محدثة تتضمن أعمدة الكمية (ابتدائية، داخلة، خارجة، متبقية) والإحصائيات السريعة
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# إضافة مسار المشروع
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """تشغيل التطبيق الرئيسي"""
    
    print("🚀 بدء تشغيل تطبيق إدارة المخزون المحسّن...")
    print("=" * 60)
    
    try:
        # إنشاء النافذة الجذر
        root = tk.Tk()
        root.withdraw()  # إخفاء النافذة الجذر مؤقتاً
        
        # استيراد وإنشاء مدير Google Sheets
        from sheets.manager import SheetsManager
        sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
        
        print("📡 محاولة الاتصال بـ Google Sheets...")
        
        if not sheets_manager.connect():
            messagebox.showerror("خطأ اتصال", "فشل في الاتصال بـ Google Sheets")
            return False
        
        print("✅ تم الاتصال بـ Google Sheets بنجاح")
        
        # إظهار النافذة الجذر
        root.deiconify()
        root.title("🏪 نظام إدارة المخزون - النسخة المحسّنة")
        root.geometry("400x300")
        root.configure(bg="#2c3e50")
        
        # إنشاء واجهة بسيطة لفتح النافذة المحسّنة
        main_frame = tk.Frame(root, bg="#2c3e50")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # عنوان
        title_label = tk.Label(
            main_frame,
            text="🏪 نظام إدارة المخزون",
            font=("Arial", 18, "bold"),
            bg="#2c3e50", fg="#ecf0f1"
        )
        title_label.pack(pady=20)
        
        # نص توضيحي
        info_label = tk.Label(
            main_frame,
            text="النسخة المحسّنة مع أعمدة الكمية والإحصائيات السريعة",
            font=("Arial", 12),
            bg="#2c3e50", fg="#bdc3c7"
        )
        info_label.pack(pady=10)
        
        # زر فتح النافذة المحسّنة
        def open_enhanced_window():
            try:
                from gui.enhanced_filter_window import AdvancedFilterWindow
                filter_window = AdvancedFilterWindow(sheets_manager)
                print("📊 تم فتح النافذة المحسّنة بنجاح")
            except Exception as e:
                print(f"❌ خطأ في فتح النافذة: {str(e)}")
                messagebox.showerror("خطأ", f"حدث خطأ في فتح النافذة: {str(e)}")
        
        open_btn = tk.Button(
            main_frame,
            text="🔍 فتح نافذة البحث والفلترة المحسّنة",
            command=open_enhanced_window,
            bg="#27ae60", fg="white",
            font=("Arial", 14, "bold"),
            relief="flat", cursor="hand2",
            pady=15
        )
        open_btn.pack(pady=20, fill=tk.X)
        
        # معلومات الميزات الجديدة
        features_text = """✨ الميزات الجديدة:
📊 أعمدة الكمية: ابتدائية، داخلة، خارجة، متبقية
📈 إحصائيات سريعة في أعلى النافذة
🎨 ألوان مختلفة للصفوف حسب مستوى المخزون
🔍 فلاتر متقدمة لجميع البيانات"""
        
        features_label = tk.Label(
            main_frame,
            text=features_text,
            font=("Arial", 10),
            bg="#2c3e50", fg="#ecf0f1",
            justify=tk.LEFT
        )
        features_label.pack(pady=10, anchor="w")
        
        print("📱 واجهة التطبيق جاهزة")
        print("🔍 انقر على زر 'فتح نافذة البحث والفلترة المحسّنة' للبدء")
        
        # تشغيل التطبيق
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في تشغيل التطبيق: {str(e)}")
        import traceback
        traceback.print_exc()
        messagebox.showerror("خطأ", f"حدث خطأ في تشغيل التطبيق: {str(e)}")
        return False

if __name__ == "__main__":
    print("🏪 تطبيق إدارة المخزون - النسخة المحسّنة")
    print("تطوير: StrucTech")
    print("الإصدار: 2.0 - مع الإحصائيات المحسّنة")
    print("=" * 60)
    
    success = main()
    
    if success:
        print("\n✅ تم إغلاق التطبيق بنجاح")
    else:
        print("\n❌ حدث خطأ أثناء تشغيل التطبيق")
        input("اضغط Enter للمتابعة...")