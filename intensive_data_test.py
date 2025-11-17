#!/usr/bin/env python3
"""
اختبار مكثف للتأكد من عمل تحديث البيانات
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import messagebox
from gui.smart_filter_window import open_smart_filter_window
from sheets.manager import SheetsManager

def intensive_data_update_test():
    print("🧪 === اختبار مكثف لتحديث البيانات ===")
    
    # إعداد النافذة
    root = tk.Tk()
    root.title("اختبار تحديث البيانات")
    root.geometry("600x500")
    root.configure(bg="#2c3e50")
    
    # الاتصال
    sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
    
    if not sheets_manager.connect():
        messagebox.showerror("خطأ", "فشل الاتصال بـ Google Sheets")
        return
    
    # فحص البيانات
    data = sheets_manager.get_all_items_raw()
    print(f"📊 إجمالي البيانات: {len(data)} عنصر")
    
    # تحليل البيانات
    categories = set()
    projects = set()
    
    for row in data:
        if len(row) >= 4:
            if row[1]: categories.add(row[1])
            if row[3]: projects.add(row[3])
    
    print(f"📋 التصنيفات: {sorted(categories)}")
    print(f"🏗️ المشاريع: {sorted(projects)}")
    
    # بناء واجهة الاختبار
    main_frame = tk.Frame(root, bg="#2c3e50", padx=30, pady=30)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # العنوان
    title = tk.Label(
        main_frame,
        text="🧪 اختبار مكثف لتحديث البيانات",
        font=("Arial", 20, "bold"),
        fg="#ecf0f1", bg="#2c3e50"
    )
    title.pack(pady=(0, 20))
    
    # معلومات البيانات
    info_frame = tk.Frame(main_frame, bg="#34495e", relief="raised", bd=2)
    info_frame.pack(fill=tk.X, pady=(0, 20))
    
    info_title = tk.Label(
        info_frame,
        text="📊 معلومات البيانات المتاحة",
        font=("Arial", 14, "bold"),
        fg="#e74c3c", bg="#34495e"
    )
    info_title.pack(pady=10)
    
    info_text = f"""
📦 إجمالي العناصر: {len(data)} عنصر
📋 عدد التصنيفات: {len(categories)} ({', '.join(list(categories)[:3])}...)
🏗️ عدد المشاريع: {len(projects)} ({', '.join(list(projects))})

🎯 الهدف من الاختبار:
• التأكد من أن تغيير الفلتر يؤثر فوراً على البيانات المعروضة
• فحص التحديث البصري للجدول
• التأكد من دقة العدادات والإحصائيات
    """
    
    info_label = tk.Label(
        info_frame,
        text=info_text,
        font=("Arial", 11),
        fg="#bdc3c7", bg="#34495e",
        justify=tk.LEFT
    )
    info_label.pack(padx=15, pady=(0, 15))
    
    # تعليمات الاختبار
    instructions_frame = tk.Frame(main_frame, bg="#e67e22", relief="raised", bd=2)
    instructions_frame.pack(fill=tk.X, pady=(0, 20))
    
    inst_title = tk.Label(
        instructions_frame,
        text="📋 تعليمات الاختبار المكثف",
        font=("Arial", 14, "bold"),
        fg="white", bg="#e67e22"
    )
    inst_title.pack(pady=10)
    
    instructions = """
🔥 خطة الاختبار المكثف:

1️⃣ اضغط الزر أدناه لفتح النافذة الذكية
2️⃣ ستظهر جميع البيانات في البداية (11 عنصر)
3️⃣ جرب تغيير فلتر "التصنيف" إلى أي تصنيف محدد
4️⃣ راقب Terminal للرسائل التشخيصية المفصلة
5️⃣ تأكد من تغيير البيانات في الجدول فوراً
6️⃣ لاحظ تحديث العداد وعنوان النافذة
7️⃣ جرب فلاتر أخرى للتأكد من الاستجابة
8️⃣ اضغط "مسح الكل" للتأكد من إعادة عرض جميع البيانات

⚠️ مؤشرات النجاح:
✅ تغيير فوري في عدد الصفوف بالجدول
✅ تحديث العداد في أعلى النافذة
✅ تغيير عنوان النافذة
✅ رسائل مفصلة في Terminal
    """
    
    inst_label = tk.Label(
        instructions_frame,
        text=instructions,
        font=("Arial", 10),
        fg="white", bg="#e67e22",
        justify=tk.LEFT
    )
    inst_label.pack(padx=15, pady=(0, 15))
    
    def start_intensive_test():
        """بدء الاختبار المكثف"""
        try:
            print("\n🚀 === بدء الاختبار المكثف ===")
            print("🔓 فتح النافذة الذكية مع مراقبة مكثفة...")
            
            # فتح النافذة
            window = open_smart_filter_window(root, sheets_manager)
            
            if window:
                print("✅ تم فتح النافذة بنجاح!")
                print("\n📋 تعليمات التشغيل:")
                print("• راقب Terminal للرسائل التشخيصية")
                print("• جرب تغيير الفلاتر وراقب التأثير الفوري")
                print("• تأكد من تحديث الجدول والعدادات")
                
                messagebox.showinfo("🧪 بدء الاختبار المكثف", 
                    f"تم فتح النافذة الذكية للاختبار!\\n\\n"
                    f"📊 البيانات الجاهزة: {len(data)} عنصر\\n"
                    f"📋 التصنيفات: {len(categories)}\\n"
                    f"🏗️ المشاريع: {len(projects)}\\n\\n"
                    f"🔍 راقب Terminal للتشخيص المفصل\\n"
                    f"جرب الفلاتر وراقب التحديث الفوري!")
            
        except Exception as e:
            print(f"❌ خطأ: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("خطأ", f"فشل في الاختبار:\\n{e}")
    
    # زر بدء الاختبار
    test_btn = tk.Button(
        main_frame,
        text="🚀 بدء الاختبار المكثف",
        command=start_intensive_test,
        font=("Arial", 16, "bold"),
        bg="#27ae60", fg="white",
        padx=40, pady=20,
        relief="flat", cursor="hand2",
        activebackground="#2ecc71"
    )
    test_btn.pack(pady=30)
    
    # معلومات الحالة
    status_label = tk.Label(
        main_frame,
        text=f"🟢 متصل | 📊 {len(data)} عنصر | 📋 {len(categories)} تصنيف | 🏗️ {len(projects)} مشروع",
        font=("Arial", 12),
        fg="#2ecc71", bg="#2c3e50"
    )
    status_label.pack()
    
    print("✅ واجهة الاختبار المكثف جاهزة")
    print("👆 اضغط الزر لبدء الاختبار المكثف")
    
    root.mainloop()

if __name__ == "__main__":
    intensive_data_update_test()