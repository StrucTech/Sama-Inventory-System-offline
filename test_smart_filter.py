#!/usr/bin/env python3
"""
اختبار النافذة الذكية الجديدة للفلاتر
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import ttk, messagebox
from gui.smart_filter_window import open_smart_filter_window
from sheets.manager import SheetsManager

def test_smart_filter():
    """اختبار النافذة الذكية"""
    print("🚀 اختبار النافذة الذكية الجديدة...")
    
    # النافذة الرئيسية للاختبار
    root = tk.Tk()
    root.title("اختبار النافذة الذكية")
    root.geometry("500x300")
    root.configure(bg="#f0f0f0")
    
    # الاتصال بـ Google Sheets
    sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
    
    if not sheets_manager.connect():
        messagebox.showerror("خطأ", "فشل الاتصال بـ Google Sheets")
        return
    
    # التحقق من البيانات
    try:
        data = sheets_manager.get_all_items_raw()
        print(f"✅ تم العثور على {len(data)} عنصر في البيانات")
    except Exception as e:
        print(f"❌ خطأ في البيانات: {e}")
        messagebox.showerror("خطأ", f"مشكلة في البيانات: {e}")
        return
    
    # بناء واجهة الاختبار
    main_frame = tk.Frame(root, bg="#f0f0f0", padx=30, pady=30)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # العنوان
    title = tk.Label(
        main_frame,
        text="🧪 اختبار النافذة الذكية الجديدة",
        font=("Arial", 18, "bold"),
        bg="#f0f0f0", fg="#2c3e50"
    )
    title.pack(pady=(0, 20))
    
    # الوصف
    description = tk.Text(
        main_frame,
        height=8, width=60,
        font=("Arial", 11),
        bg="white", fg="#34495e",
        relief="flat", borderwidth=10,
        wrap=tk.WORD
    )
    description.pack(pady=(0, 20))
    
    desc_text = """🎯 النافذة الذكية الجديدة تتميز بـ:

✅ تصميم احترافي وأنيق
✅ استجابة فورية للفلاتر
✅ عرض ديناميكي لعدد النتائج
✅ تصدير سهل للنتائج
✅ واجهة سهلة ومفهومة

🔥 جرب الفلاتر وستلاحظ الفرق فوراً!
📊 البيانات المتاحة: """ + f"{len(data)} عنصر جاهز للاختبار"
    
    description.insert("1.0", desc_text)
    description.config(state="disabled")
    
    def start_smart_test():
        """بدء اختبار النافذة الذكية"""
        try:
            print("🔓 فتح النافذة الذكية...")
            
            # فتح النافذة
            smart_window = open_smart_filter_window(root, sheets_manager)
            
            if smart_window:
                print("✅ تم فتح النافذة الذكية بنجاح!")
                
                # رسالة تأكيد
                messagebox.showinfo("نجح! 🎉", 
                    f"تم فتح النافذة الذكية بنجاح!\\n\\n"
                    f"📊 البيانات المحملة: {len(data)} عنصر\\n"
                    f"🎛️ الفلاتر جاهزة للاستخدام\\n"
                    f"⚡ تحديث فوري مضمون!\\n\\n"
                    f"جرب الفلاتر الآن وشاهد السحر!")
            
        except Exception as e:
            print(f"❌ خطأ: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("خطأ", f"فشل في فتح النافذة:\\n{e}")
    
    # زر التشغيل
    start_btn = tk.Button(
        main_frame,
        text="🚀 تشغيل النافذة الذكية",
        command=start_smart_test,
        font=("Arial", 14, "bold"),
        bg="#3498db", fg="white",
        padx=30, pady=15,
        relief="flat", cursor="hand2",
        activebackground="#2980b9"
    )
    start_btn.pack(pady=20)
    
    # معلومات الحالة
    status_frame = tk.Frame(main_frame, bg="#f0f0f0")
    status_frame.pack()
    
    tk.Label(
        status_frame,
        text="🟢 متصل",
        font=("Arial", 12, "bold"),
        fg="#27ae60", bg="#f0f0f0"
    ).pack(side=tk.LEFT, padx=(0, 10))
    
    tk.Label(
        status_frame,
        text=f"📊 {len(data)} عنصر جاهز",
        font=("Arial", 12),
        fg="#7f8c8d", bg="#f0f0f0"
    ).pack(side=tk.LEFT)
    
    print("✅ واجهة الاختبار جاهزة - اضغط الزر لبدء الاختبار")
    
    # تشغيل التطبيق
    root.mainloop()

if __name__ == "__main__":
    test_smart_filter()