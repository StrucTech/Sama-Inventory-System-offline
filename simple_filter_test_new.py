#!/usr/bin/env python3
"""
تطبيق اختبار بسيط للفلاتر
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import ttk
from config.user_session import UserSession
from sheets.manager import SheetsManager

class SimpleFilterTest:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("اختبار الفلاتر")
        self.root.geometry("800x600")
        
        # جلسة المستخدم
        self.user_session = UserSession()
        self.user_session.login("مطور_النظام", "PRJ_TEST_001", is_admin=False)
        
        # البيانات
        self.all_operations = []
        self.displayed_operations = []
        
        # إعداد الواجهة
        self.setup_ui()
        
        # تحميل البيانات
        self.load_data()
    
    def setup_ui(self):
        # إطار الفلاتر
        filter_frame = tk.LabelFrame(self.root, text="الفلاتر")
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # فلتر التصنيف
        tk.Label(filter_frame, text="التصنيف:").grid(row=0, column=0, padx=5, pady=5)
        self.category_combo = ttk.Combobox(filter_frame, state='readonly')
        self.category_combo.grid(row=0, column=1, padx=5, pady=5)
        self.category_combo.bind('<<ComboboxSelected>>', self.on_filter_change)
        
        # معلومات المستخدم
        info_frame = tk.Frame(filter_frame)
        info_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        tk.Label(info_frame, text=f"المستخدم: {self.user_session.username} (مقيد)", fg="blue").pack(side=tk.LEFT, padx=10)
        tk.Label(info_frame, text=f"المشروع: {self.user_session.project_number} (مقيد)", fg="blue").pack(side=tk.LEFT, padx=10)
        
        # الجدول
        self.tree = ttk.Treeview(self.root, columns=('date', 'item', 'category', 'user'), show='headings')
        self.tree.heading('date', text='التاريخ')
        self.tree.heading('item', text='العنصر')
        self.tree.heading('category', text='التصنيف')
        self.tree.heading('user', text='المستخدم')
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # شريط الحالة
        self.status_label = tk.Label(self.root, text="جاري التحميل...", relief=tk.SUNKEN)
        self.status_label.pack(fill=tk.X)
    
    def load_data(self):
        try:
            sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
            
            if not sheets_manager.connect():
                raise Exception("فشل في الاتصال")
            
            activity_sheet = sheets_manager.spreadsheet.worksheet('Activity_Log_v2_20251108')
            all_values = activity_sheet.get_all_values()
            
            headers = all_values[0]
            self.all_operations = []
            categories = set()
            
            for row in all_values[1:]:
                if row and row[0]:
                    operation = {}
                    for i, header in enumerate(headers):
                        operation[header] = row[i] if i < len(row) else ""
                    self.all_operations.append(operation)
                    
                    if operation.get('التصنيف'):
                        categories.add(operation['التصنيف'])
            
            # إعداد فلتر التصنيف
            self.category_combo['values'] = ['الكل'] + sorted(categories)
            self.category_combo.set('الكل')
            
            # تطبيق الفلاتر الأولية
            self.apply_filters()
            
            print(f"تم تحميل {len(self.all_operations)} عملية")
            
        except Exception as e:
            print(f"خطأ: {e}")
            self.status_label.config(text=f"خطأ: {e}")
    
    def on_filter_change(self, event=None):
        print("تم تغيير الفلتر")
        self.apply_filters()
    
    def apply_filters(self):
        # البدء من جميع العمليات
        filtered = self.all_operations.copy()
        original_count = len(filtered)
        
        # فلتر المستخدم (مقيد)
        user_filter = self.user_session.username
        filtered = [op for op in filtered if op.get('اسم المستخدم', '') == user_filter]
        print(f"بعد فلتر المستخدم '{user_filter}': {len(filtered)}")
        
        # فلتر المشروع (مقيد)
        project_filter = self.user_session.project_number
        filtered = [op for op in filtered if op.get('رقم المشروع', '') == project_filter]
        print(f"بعد فلتر المشروع '{project_filter}': {len(filtered)}")
        
        # فلتر التصنيف (قابل للتعديل)
        category_filter = self.category_combo.get()
        if category_filter and category_filter != 'الكل':
            filtered = [op for op in filtered if op.get('التصنيف', '') == category_filter]
            print(f"بعد فلتر التصنيف '{category_filter}': {len(filtered)}")
        
        # حفظ النتائج
        self.displayed_operations = filtered
        
        # تحديث العرض
        self.refresh_display()
        
        print(f"النتيجة النهائية: {original_count} → {len(filtered)}")
    
    def refresh_display(self):
        # مسح الجدول
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # إضافة البيانات الجديدة
        for op in self.displayed_operations:
            self.tree.insert('', 'end', values=(
                op.get('التاريخ', ''),
                op.get('اسم العنصر', ''),
                op.get('التصنيف', ''),
                op.get('اسم المستخدم', '')
            ))
        
        # تحديث الحالة
        self.status_label.config(text=f"يعرض {len(self.displayed_operations)} من {len(self.all_operations)} عملية")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    print("🧪 اختبار الفلاتر البسيط")
    
    app = SimpleFilterTest()
    app.run()