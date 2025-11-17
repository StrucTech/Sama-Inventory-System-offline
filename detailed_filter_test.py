#!/usr/bin/env python3
"""
اختبار مفصل لتتبع مشكلة الفلاتر
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import ttk
from gui.filter_search_window import FilterSearchWindow, show_filter_search_window
from sheets.manager import SheetsManager

print("🔍 بدء اختبار الفلاتر المفصل...")

# إنشاء النافذة الرئيسية
root = tk.Tk()
root.title('اختبار الفلاتر المفصل')
root.geometry('600x500')

# إعداد SheetsManager
sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')

if sheets_manager.connect():
    print("✅ تم الاتصال بـ Google Sheets")
    
    def test_filter_values():
        try:
            print("📋 فتح نافذة الفلاتر مع تتبع القيم...")
            filter_window = show_filter_search_window(root, sheets_manager)
            
            # إنشاء نافذة تعليمات مفصلة
            instructions = tk.Toplevel(root)
            instructions.title("🧪 تعليمات الاختبار المفصل")
            instructions.geometry('500x400')
            
            # إضافة نص التعليمات
            frame = ttk.Frame(instructions, padding="20")
            frame.pack(fill=tk.BOTH, expand=True)
            
            title = ttk.Label(frame, text="🔍 اختبار الفلاتر خطوة بخطوة", 
                             font=("Arial", 14, "bold"))
            title.pack(pady=(0, 15))
            
            # نص التعليمات
            instructions_text = """
اتبع هذه الخطوات لاختبار الفلاتر:

1️⃣ افتح Terminal/PowerShell وشاهد الرسائل

2️⃣ في نافذة الفلاتر:
   • جرب تغيير فلتر "العنصر"
   • لاحظ الرسائل في Terminal
   • تأكد من تغيير البيانات في الجدول

3️⃣ جرب فلتر "التصنيف":
   • اختر تصنيف محدد
   • لاحظ الرسائل التشخيصية
   • تحقق من النتائج

4️⃣ جرب فلتر "المشروع":
   • اختر مشروع محدد
   • راقب التغييرات

⚠️ إذا لم تتغير البيانات:
   • تحقق من الرسائل في Terminal
   • ابحث عن رسائل الخطأ
   • لاحظ قيم الفلاتر المطبوعة

🔧 ما نبحث عنه:
   • هل تظهر رسائل "🔄 تغيير فلتر"؟
   • هل تظهر رسائل "🔍 فحص العنصر"؟
   • هل تظهر رسائل "✅/❌ العنصر يطابق"؟
   • هل يتغير عدد النتائج؟

📊 في الإحصائيات:
   • لاحظ هل تتغير الأرقام؟
   • تأكد من صحة المجاميع
            """
            
            text_widget = tk.Text(frame, font=("Arial", 10), wrap=tk.WORD, 
                                height=15, width=60)
            text_widget.insert("1.0", instructions_text)
            text_widget.config(state="disabled")
            
            # إضافة scroll bar
            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
            
            # ترتيب العناصر
            text_widget.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # زر لإغلاق التعليمات
            close_btn = ttk.Button(instructions, text="✅ فهمت، ابدأ الاختبار", 
                                 command=instructions.destroy)
            close_btn.pack(pady=10)
            
            print("✅ تم فتح نافذة الفلاتر والتعليمات")
            print("🎯 راقب الرسائل هنا أثناء التفاعل مع الفلاتر...")
            
        except Exception as e:
            print(f"❌ خطأ: {e}")
            import traceback
            traceback.print_exc()
    
    # إعداد الواجهة
    main_frame = ttk.Frame(root, padding="30")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    title = ttk.Label(main_frame, text="🧪 اختبار الفلاتر المفصل", 
                     font=("Arial", 16, "bold"))
    title.pack(pady=(0, 20))
    
    desc = ttk.Label(main_frame, 
        text="سيتم فتح نافذة الفلاتر مع تتبع مفصل للأحداث\nراقب رسائل Terminal لمعرفة ما يحدث",
        font=("Arial", 11), justify=tk.CENTER)
    desc.pack(pady=(0, 30))
    
    test_btn = ttk.Button(main_frame, text="🚀 ابدأ اختبار الفلاتر", 
                         command=test_filter_values)
    test_btn.pack(pady=20)
    
    note = ttk.Label(main_frame, 
        text="💡 تأكد من مشاهدة Terminal/PowerShell أثناء الاختبار",
        font=("Arial", 10), foreground="blue")
    note.pack()
    
    print("📱 واجهة الاختبار جاهزة")
    print("👆 اضغط على الزر لبدء الاختبار")
    
    root.mainloop()
else:
    print("❌ فشل الاتصال بـ Google Sheets")