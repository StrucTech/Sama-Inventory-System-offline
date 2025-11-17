#!/usr/bin/env python3
"""
اختبار نهائي مبسط - إثبات عمل الفلاتر
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import ttk, messagebox
from gui.filter_search_window import FilterSearchWindow, show_filter_search_window
from sheets.manager import SheetsManager

def main():
    print("🧪 === اختبار نهائي لإثبات عمل الفلاتر ===")
    
    # إعداد النافذة الرئيسية
    root = tk.Tk()
    root.title('إثبات عمل الفلاتر')
    root.geometry('600x400')
    
    # إعداد SheetsManager
    sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
    
    if not sheets_manager.connect():
        messagebox.showerror("خطأ", "فشل الاتصال بـ Google Sheets")
        return
    
    # عرض البيانات المتاحة
    try:
        all_items = sheets_manager.get_all_items_raw()
        print(f"\n📊 إجمالي العناصر المتاحة: {len(all_items)}")
        
        if all_items:
            categories = set()
            projects = set()
            items = set()
            
            for item in all_items:
                if len(item) >= 4:
                    if item[0]: items.add(item[0])
                    if item[1]: categories.add(item[1])
                    if item[3]: projects.add(item[3])
            
            print(f"📋 التصنيفات: {sorted(categories)}")
            print(f"🏗️ المشاريع: {sorted(projects)}")
            print(f"📦 العناصر: {len(items)} عنصر")
        
    except Exception as e:
        print(f"❌ خطأ في قراءة البيانات: {e}")
        return
    
    # إعداد الواجهة
    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # العنوان
    title = ttk.Label(main_frame, text="🧪 اختبار نهائي - إثبات عمل الفلاتر", 
                     font=("Arial", 14, "bold"))
    title.pack(pady=(0, 15))
    
    # الإرشادات
    instructions = f"""
🔍 خطوات الاختبار:

1️⃣ اضغط "فتح نافذة الفلاتر" أدناه
2️⃣ ستظهر جميع البيانات ({len(all_items)} عنصر) في البداية
3️⃣ جرب تغيير فلتر "التصنيف" إلى أي تصنيف محدد
4️⃣ لاحظ أن البيانات تتغير فوراً
5️⃣ جرب فلتر "المشروع" 
6️⃣ اضغط "مسح" لعرض جميع البيانات مرة أخرى

💡 النتيجة المتوقعة:
   ✅ عند اختيار فلتر محدد: تظهر البيانات المطابقة فقط
   ✅ عند اختيار "جميع...": تظهر جميع البيانات
   ✅ عند الضغط على "مسح": تظهر جميع البيانات
   ✅ عنوان النافذة يتغير ليعرض عدد النتائج

⚠️ إذا لم تظهر نتائج:
   • تأكد من اختيار "جميع العناصر" في كل الفلاتر
   • أو اضغط زر "مسح" لإعادة تعيين كل شيء
    """
    
    text_widget = tk.Text(main_frame, font=("Arial", 10), height=15, width=70,
                         wrap=tk.WORD, bg="#f8f9fa", relief="flat", borderwidth=10)
    text_widget.insert("1.0", instructions)
    text_widget.config(state="disabled")
    text_widget.pack(pady=(0, 15))
    
    def open_filter_test():
        """فتح نافذة الفلاتر للاختبار"""
        try:
            print("🚀 فتح نافذة الفلاتر...")
            filter_window = show_filter_search_window(root, sheets_manager)
            print("✅ تم فتح نافذة الفلاتر بنجاح")
            
            # رسالة تأكيد
            messagebox.showinfo("تم!", 
                f"تم فتح نافذة الفلاتر\\n\\n"
                f"📊 البيانات المتاحة: {len(all_items)} عنصر\\n"
                f"📋 التصنيفات: {len(categories)}\\n"
                f"🏗️ المشاريع: {len(projects)}\\n\\n"
                f"جرب الفلاتر وراقب التغييرات!")
            
        except Exception as e:
            print(f"❌ خطأ: {e}")
            messagebox.showerror("خطأ", f"فشل في فتح نافذة الفلاتر:\\n{e}")
    
    # أزرار التحكم
    buttons_frame = ttk.Frame(main_frame)
    buttons_frame.pack()
    
    open_btn = ttk.Button(buttons_frame, text="🚀 فتح نافذة الفلاتر للاختبار", 
                         command=open_filter_test, style="Accent.TButton")
    open_btn.pack(pady=10)
    
    status_label = ttk.Label(main_frame, 
        text=f"حالة الاتصال: ✅ متصل | البيانات: {len(all_items)} عنصر متاح",
        font=("Arial", 10), foreground="green")
    status_label.pack(pady=(10, 0))
    
    print("✅ واجهة الاختبار جاهزة")
    print("👆 اضغط على الزر لبدء الاختبار")
    
    root.mainloop()

if __name__ == "__main__":
    main()