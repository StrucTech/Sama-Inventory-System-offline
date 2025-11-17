"""
تطبيق اختبار النافذة المُصححة لحل مشاكل:
1. الكميات المتاحة تظهر صفر
2. عدم تطابق الكمية الابتدائية والداخلة  
3. الإحصائيات تستغرق وقتاً طويلاً
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# إضافة مسار المشروع
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """تشغيل النافذة المُصححة"""
    
    print("🔧 بدء تشغيل النافذة المُصححة...")
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
        root.title("🔧 اختبار النافذة المُصححة")
        root.geometry("500x400")
        root.configure(bg="#2c3e50")
        
        # إنشاء واجهة بسيطة
        main_frame = tk.Frame(root, bg="#2c3e50")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # عنوان
        title_label = tk.Label(
            main_frame,
            text="🔧 اختبار النافذة المُصححة",
            font=("Arial", 18, "bold"),
            bg="#2c3e50", fg="#ecf0f1"
        )
        title_label.pack(pady=20)
        
        # نص توضيحي
        info_text = """تم إصلاح المشاكل التالية:
✅ عرض الكميات الصحيحة (ابتدائية، داخلة، خارجة، متبقية)
✅ إحصائيات سريعة ودقيقة
✅ ألوان مختلفة حسب مستوى المخزون
✅ معدل الدوران وإحصائيات تفصيلية"""
        
        info_label = tk.Label(
            main_frame,
            text=info_text,
            font=("Arial", 11),
            bg="#2c3e50", fg="#bdc3c7",
            justify=tk.LEFT
        )
        info_label.pack(pady=15)
        
        # زر فتح النافذة المُصححة
        def open_fixed_window():
            try:
                from gui.fixed_filter_window import FixedFilterWindow
                filter_window = FixedFilterWindow(sheets_manager)
                print("📊 تم فتح النافذة المُصححة بنجاح")
            except Exception as e:
                print(f"❌ خطأ في فتح النافذة: {str(e)}")
                import traceback
                traceback.print_exc()
                messagebox.showerror("خطأ", f"حدث خطأ في فتح النافذة: {str(e)}")
        
        open_btn = tk.Button(
            main_frame,
            text="🔧 فتح النافذة المُصححة",
            command=open_fixed_window,
            bg="#e74c3c", fg="white",
            font=("Arial", 14, "bold"),
            relief="flat", cursor="hand2",
            pady=15
        )
        open_btn.pack(pady=20, fill=tk.X)
        
        # معلومات الإصلاحات
        fixes_text = """🔧 الإصلاحات المطبقة:
• أسماء الأعمدة مطابقة تماماً لـ Google Sheets
• عرض الكميات الفعلية بدلاً من الصفر
• حساب سريع للإحصائيات
• إضافة معدل دوران المخزون
• تحسين ألوان العرض والواجهة"""
        
        fixes_label = tk.Label(
            main_frame,
            text=fixes_text,
            font=("Arial", 9),
            bg="#2c3e50", fg="#ecf0f1",
            justify=tk.LEFT
        )
        fixes_label.pack(pady=10, anchor="w")
        
        print("📱 واجهة الاختبار جاهزة")
        print("🔧 انقر على زر 'فتح النافذة المُصححة' لرؤية الإصلاحات")
        
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
    print("🔧 اختبار النافذة المُصححة")
    print("حل مشاكل: الكميات الصفر، الإحصائيات البطيئة، عرض البيانات")
    print("=" * 60)
    
    success = main()
    
    if success:
        print("\n✅ تم إغلاق الاختبار بنجاح")
    else:
        print("\n❌ حدث خطأ أثناء الاختبار")
        input("اضغط Enter للمتابعة...")