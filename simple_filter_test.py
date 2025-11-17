#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار بسيط للفلاتر مع تتبع الأحداث
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import ttk
from gui.filter_search_window import show_filter_search_window
from sheets.manager import SheetsManager

def main():
    print('🧪 اختبار الفلاتر التفاعلية...')
    
    # إنشاء النافذة الرئيسية
    root = tk.Tk()
    root.title('اختبار الفلاتر التفاعلية')
    root.geometry('600x200')
    
    # النص التوضيحي
    main_label = ttk.Label(root, text='اختبار الفلاتر مع تتبع الأحداث', 
                          font=('Arial', 14, 'bold'))
    main_label.pack(pady=20)
    
    info_label = ttk.Label(root, 
                          text='سيتم فتح نافذة الفلاتر مع تتبع مفصل للأحداث\nراقب الرسائل في وحدة التحكم وتغيير عنوان النافذة',
                          font=('Arial', 11))
    info_label.pack(pady=10)
    
    # دالة فتح نافذة الفلاتر
    def open_filters():
        # إنشاء SheetsManager
        sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
        
        if sheets_manager.connect():
            print('✅ تم الاتصال بـ Google Sheets')
            
            try:
                print('🚀 فتح نافذة الفلاتر مع التتبع...')
                filter_window = show_filter_search_window(root, sheets_manager)
                print('✅ تم فتح نافذة الفلاتر')
                
                # نافذة التعليمات
                instructions = tk.Toplevel(root)
                instructions.title('📋 تعليمات الاختبار')
                instructions.geometry('400x300')
                
                inst_text = "تعليمات اختبار الفلاتر:\n\n"
                inst_text += "1. راقب تغيير عنوان النافذة عند التفاعل\n"
                inst_text += "2. لاحظ الرسائل في وحدة التحكم\n"
                inst_text += "3. جرب تغيير فلتر العنصر أو التصنيف\n"
                inst_text += "4. انتظر وشاهد العنوان يتغير\n"
                inst_text += "5. راقب تغيير الأرقام في الإحصائيات\n\n"
                inst_text += "إذا رأيت الرسائل التالية فالفلاتر تعمل:\n"
                inst_text += "• 'تغيير فلتر' - الحدث مُسجل\n"
                inst_text += "• 'تم مسح X نتيجة' - المسح يعمل\n"
                inst_text += "• 'تم إضافة Y نتيجة' - الإضافة تعمل\n"
                inst_text += "• تغيير عنوان النافذة - التفاعل واضح\n\n"
                inst_text += "إذا لم تر هذه الرسائل، فهناك مشكلة!"
                
                inst_label = tk.Label(instructions, text=inst_text, 
                                     font=('Arial', 10), justify=tk.LEFT)
                inst_label.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
                
                print('📋 تم فتح نافذة التعليمات')
                
            except Exception as e:
                print(f'❌ خطأ في فتح نافذة الفلاتر: {e}')
                import traceback
                traceback.print_exc()
        else:
            print('❌ فشل في الاتصال بـ Google Sheets')
    
    # زر فتح النافذة
    open_btn = ttk.Button(root, text='🔍 فتح نافذة الفلاتر للاختبار',
                         command=open_filters)
    open_btn.pack(pady=20)
    
    # تشغيل النافذة
    print('🖱️ اضغط على الزر لبدء الاختبار')
    root.mainloop()

if __name__ == "__main__":
    main()