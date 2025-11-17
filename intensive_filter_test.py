#!/usr/bin/env python3
"""
اختبار مكثف لنافذة الفلاتر الجديدة - مع تشخيص كامل
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import ttk, messagebox
from gui.simple_filter_window import show_simple_filter_window
from sheets.manager import SheetsManager

def intensive_filter_test():
    print("🧪 === اختبار مكثف للفلاتر الجديدة ===")
    
    # إعداد النافذة
    root = tk.Tk()
    root.title("اختبار مكثف للفلاتر")
    root.geometry("500x400")
    
    # اتصال بالبيانات
    sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
    
    if not sheets_manager.connect():
        print("❌ فشل الاتصال")
        return
    
    # فحص البيانات
    raw_data = sheets_manager.get_all_items_raw()
    print(f"📊 إجمالي البيانات: {len(raw_data)} عنصر")
    
    if raw_data:
        # تحليل البيانات
        categories = set()
        projects = set()
        items = set()
        
        for row in raw_data:
            if len(row) >= 4:
                if row[0]: items.add(row[0])
                if row[1]: categories.add(row[1]) 
                if row[3]: projects.add(row[3])
        
        print(f"📋 التصنيفات المتاحة: {sorted(categories)}")
        print(f"🏗️ المشاريع المتاحة: {sorted(projects)}")
        print(f"📦 العناصر المتاحة: {len(items)} عنصر")
    
    # إنشاء واجهة الاختبار
    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # العنوان
    title = ttk.Label(main_frame, text="🔬 اختبار مكثف للفلاتر", 
                     font=("Arial", 16, "bold"))
    title.pack(pady=(0, 15))
    
    # معلومات البيانات
    info_text = f"""
📊 البيانات المتاحة للاختبار:
   • إجمالي العناصر: {len(raw_data)}
   • عدد التصنيفات: {len(categories)}
   • عدد المشاريع: {len(projects)}

🧪 خطة الاختبار:
   1. فتح النافذة الجديدة
   2. اختبار كل فلتر بشكل منفصل
   3. اختبار الفلاتر المدمجة
   4. اختبار مسح الفلاتر
   5. مراقبة الرسائل في Terminal

⚠️ تعليمات مهمة:
   • راقب Terminal للرسائل التشخيصية
   • جرب تغيير الفلاتر وراقب التحديث الفوري
   • تأكد من تغيير عنوان النافذة
   • لاحظ تغيير الإحصائيات
    """
    
    info_label = ttk.Label(main_frame, text=info_text, 
                          font=("Arial", 10), justify=tk.LEFT)
    info_label.pack(pady=(0, 20))
    
    def start_intensive_test():
        """بدء الاختبار المكثف"""
        try:
            print("\n🚀 بدء الاختبار المكثف...")
            print("🔓 فتح نافذة الفلاتر مع تشخيص كامل...")
            
            # فتح النافذة
            filter_window = show_simple_filter_window(root, sheets_manager)
            
            print("✅ تم فتح النافذة - ابدأ الاختبار!")
            print("\n📋 تعليمات الاختبار:")
            print("1. جرب تغيير فلتر 'التصنيف' إلى أي تصنيف محدد")
            print("2. راقب تحديث البيانات فوراً")
            print("3. جرب فلتر 'المشروع'")
            print("4. جرب دمج عدة فلاتر")
            print("5. استخدم زر 'مسح الكل' لإعادة التعيين")
            
            # رسالة تأكيد
            messagebox.showinfo("🧪 بدء الاختبار", 
                f"تم فتح نافذة الفلاتر الجديدة!\\n\\n"
                f"البيانات المتاحة: {len(raw_data)} عنصر\\n"
                f"راقب Terminal للرسائل التشخيصية\\n\\n"
                f"جرب الفلاتر وراقب التحديث الفوري!")
            
        except Exception as e:
            print(f"❌ خطأ: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("خطأ", f"فشل في الاختبار:\\n{e}")
    
    # زر الاختبار
    test_btn = ttk.Button(main_frame, text="🚀 ابدأ الاختبار المكثف", 
                         command=start_intensive_test)
    test_btn.pack(pady=20)
    
    # معلومات الحالة
    status_frame = ttk.Frame(main_frame)
    status_frame.pack()
    
    ttk.Label(status_frame, text="الحالة:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
    ttk.Label(status_frame, text=f"✅ متصل | {len(raw_data)} عنصر جاهز للاختبار", 
             font=("Arial", 10), foreground="green").pack(side=tk.LEFT, padx=(5, 0))
    
    print("✅ واجهة الاختبار المكثف جاهزة")
    print("👆 اضغط الزر لبدء الاختبار")
    
    root.mainloop()

if __name__ == "__main__":
    intensive_filter_test()