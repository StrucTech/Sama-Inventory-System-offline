#!/usr/bin/env python3
"""
🚀 زر فلاتر مباشر للنافذة الرئيسية - حل بديل 
"""

import tkinter as tk
from tkinter import ttk, messagebox
from gui.basic_filter_window import open_basic_filter_window
from sheets.manager import SheetsManager

def add_direct_filter_button_to_main_window():
    """إضافة زر فلاتر مباشر للنافذة الرئيسية"""
    
    # البحث عن النافذة الرئيسية
    for widget in tk._default_root.winfo_children() if tk._default_root else []:
        if isinstance(widget, tk.Tk) or isinstance(widget, tk.Toplevel):
            if "نظام إدارة المخزون" in widget.title():
                print(f"✅ وجدت النافذة الرئيسية: {widget.title()}")
                
                # إضافة الزر للنافذة
                add_filter_button_to_window(widget)
                return widget
    
    print("❌ لم يتم العثور على النافذة الرئيسية")
    return None

def add_filter_button_to_window(window):
    """إضافة زر الفلاتر لنافذة معينة"""
    
    try:
        # إنشاء إطار للزر الجديد
        filter_frame = ttk.Frame(window)
        filter_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        # زر الفلاتر المباشر
        filter_btn = ttk.Button(
            filter_frame,
            text="🔍 فلاتر مباشرة (محسّن)",
            command=lambda: open_direct_filter_from_button(window),
            style="Accent.TButton"
        )
        filter_btn.pack(side=tk.LEFT, padx=5)
        
        # زر المساعدة
        help_btn = ttk.Button(
            filter_frame,
            text="❓ مساعدة",
            command=show_filter_help,
            style="Secondary.TButton"
        )
        help_btn.pack(side=tk.LEFT, padx=5)
        
        # ملصق التعليمات
        info_label = ttk.Label(
            filter_frame,
            text="💡 اضغط 'فلاتر مباشرة' لفتح نظام البحث والفلترة المتطور",
            foreground="blue"
        )
        info_label.pack(side=tk.LEFT, padx=20)
        
        print("✅ تم إضافة أزرار الفلاتر للنافذة الرئيسية")
        
    except Exception as e:
        print(f"❌ خطأ في إضافة الأزرار: {e}")

def open_direct_filter_from_button(parent_window):
    """فتح الفلاتر مباشرة من الزر"""
    
    try:
        print("🔍 فتح الفلاتر من الزر المباشر...")
        
        # إنشاء SheetsManager
        sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
        
        if not sheets_manager.connect():
            messagebox.showerror("خطأ", "فشل في الاتصال بـ Google Sheets!")
            return
        
        # مستخدم افتراضي
        current_user = {'username': 'admin', 'user_type': 'admin'}
        
        # فتح نافذة الفلاتر
        filter_window = open_basic_filter_window(
            parent=parent_window,
            sheets_manager=sheets_manager,
            current_user=current_user
        )
        
        if filter_window:
            print("🎉 نجح فتح الفلاتر من الزر المباشر!")
            messagebox.showinfo("نجح! 🔥", 
                "تم فتح نافذة الفلاتر المتطورة بنجاح!\n\n"
                "✨ الميزات الجديدة:\n"
                "• فلتر التصنيف المتقدم\n"
                "• فلتر المشروع الذكي\n"
                "• تحديث فوري للنتائج\n"
                "• أزرار التحكم الشامل\n\n"
                "🎯 استمتع بالتجربة المحسّنة!")
        else:
            messagebox.showerror("خطأ", "فشل في إنشاء نافذة الفلاتر!")
            
    except Exception as e:
        print(f"❌ خطأ: {e}")
        messagebox.showerror("خطأ", f"حدث خطأ في فتح الفلاتر:\n{str(e)}")

def show_filter_help():
    """عرض نافذة المساعدة للفلاتر"""
    
    help_window = tk.Toplevel()
    help_window.title("🔍 مساعدة نظام الفلاتر")
    help_window.geometry("600x500")
    help_window.configure(bg="#f0f0f0")
    
    # العنوان
    title = tk.Label(
        help_window,
        text="🔍 دليل استخدام نظام الفلاتر المتطور",
        font=("Arial", 16, "bold"),
        bg="#f0f0f0", fg="#2c3e50"
    )
    title.pack(pady=20)
    
    # النص التوضيحي
    help_text = """
🚀 نظام الفلاتر المتطور

📋 الميزات الرئيسية:
• فلتر التصنيف: يمكنك فلترة العناصر حسب فئتها
• فلتر المشروع: عرض عناصر مشروع محدد فقط  
• التحديث الفوري: النتائج تظهر مباشرة عند التغيير
• مسح الفلاتر: إعادة تعيين جميع الفلاتر بضغطة واحدة

🎯 طريقة الاستخدام:
1. اضغط "فلاتر مباشرة" لفتح النافذة
2. اختر التصنيف المطلوب من القائمة المنسدلة
3. اختر المشروع المطلوب (اختياري)
4. شاهد النتائج تتحدث فوراً في الجدول
5. استخدم "مسح الفلاتر" للعودة لجميع العناصر

💡 نصائح:
• اختر "الكل" لإظهار جميع العناصر في أي فئة
• يمكنك دمج فلاتر متعددة للوصول لنتائج دقيقة
• استخدم "تحديث" لإعادة تحميل البيانات من Google Sheets

🔧 استكشاف الأخطاء:
• إذا لم تظهر البيانات، تأكد من الاتصال بالإنترنت
• إذا كانت القوائم فارغة، تحقق من وجود بيانات في Google Sheets
• استخدم زر "تحديث" إذا كانت البيانات قديمة

🎉 استمتع باستخدام نظام الفلاتر المتطور!
"""
    
    # منطقة النص
    text_frame = tk.Frame(help_window, bg="#f0f0f0")
    text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    text_widget = tk.Text(
        text_frame,
        font=("Arial", 11),
        bg="white", fg="#2c3e50",
        wrap=tk.WORD,
        yscrollcommand=scrollbar.set
    )
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    text_widget.insert("1.0", help_text)
    text_widget.config(state=tk.DISABLED)
    
    scrollbar.config(command=text_widget.yview)
    
    # زر الإغلاق
    close_btn = ttk.Button(
        help_window,
        text="✅ فهمت",
        command=help_window.destroy
    )
    close_btn.pack(pady=20)

def main():
    """الدالة الرئيسية لتشغيل محسّن الفلاتر"""
    
    print("🚀 بدء محسّن الفلاتر للنافذة الرئيسية...")
    
    # محاولة العثور على النافذة الرئيسية وإضافة الأزرار
    main_window = add_direct_filter_button_to_main_window()
    
    if main_window:
        print("✅ تم تحسين النافذة الرئيسية بنجاح!")
        messagebox.showinfo("تحسين مكتمل! 🎉",
            "تم إضافة أزرار الفلاتر المباشرة للنافذة الرئيسية!\n\n"
            "🔍 ابحث عن زر 'فلاتر مباشرة (محسّن)' في الأعلى\n"
            "❓ اضغط 'مساعدة' للحصول على تعليمات مفصلة\n\n"
            "🚀 الآن يمكنك استخدام الفلاتر المتطورة!")
    else:
        # إنشاء نافذة اختبار إذا لم توجد النافذة الرئيسية
        create_test_window()

def create_test_window():
    """إنشاء نافذة اختبار للفلاتر"""
    
    test_window = tk.Tk()
    test_window.title("🧪 نافذة اختبار الفلاتر")
    test_window.geometry("500x300")
    test_window.configure(bg="#ecf0f1")
    
    # العنوان
    title = tk.Label(
        test_window,
        text="🧪 نافذة اختبار نظام الفلاتر",
        font=("Arial", 18, "bold"),
        bg="#ecf0f1", fg="#2c3e50"
    )
    title.pack(pady=30)
    
    # الوصف
    desc = tk.Label(
        test_window,
        text="هذه نافذة اختبار لتجربة نظام الفلاتر المتطور\nيمكنك اختبار جميع الميزات من هنا",
        font=("Arial", 12),
        bg="#ecf0f1", fg="#34495e",
        justify=tk.CENTER
    )
    desc.pack(pady=20)
    
    # إضافة الأزرار للنافذة الاختبار
    add_filter_button_to_window(test_window)
    
    print("✅ تم إنشاء نافذة اختبار الفلاتر")
    test_window.mainloop()

if __name__ == "__main__":
    main()