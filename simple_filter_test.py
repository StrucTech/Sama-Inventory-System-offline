#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار الفلاتر مع debugging مباشر في الواجهة
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from enhanced_sheets_manager import EnhancedSheetsManager
from config.settings import load_config

class SimpleFilterTest:
    """اختبار بسيط للفلاتر"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔍 اختبار الفلاتر البسيط")
        self.root.geometry("800x600")
        
        # تحميل البيانات
        self.setup_manager()
        self.create_widgets()
        self.load_data()
    
    def setup_manager(self):
        """إعداد المدير"""
        try:
            config = load_config()
            self.manager = EnhancedSheetsManager(
                config['credentials_file'],
                config['spreadsheet_name'],
                config['worksheet_name']
            )
            
            if not self.manager.connect():
                messagebox.showerror("خطأ", "فشل في الاتصال")
                return False
            
            print("✅ تم الاتصال بنجاح")
            return True
            
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في الإعداد: {e}")
            return False
    
    def create_widgets(self):
        """إنشاء العناصر"""
        # منطقة الفلاتر
        filters_frame = ttk.LabelFrame(self.root, text="🔍 اختبار الفلاتر", padding="10")
        filters_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # فلتر العمليات
        ttk.Label(filters_frame, text="نوع العملية:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.operation_var = tk.StringVar()
        self.operation_combo = ttk.Combobox(filters_frame, textvariable=self.operation_var, 
                                          values=["", "إضافة", "إخراج", "تحديث", "إنشاء", "حذف"],
                                          state="readonly", width=15)
        self.operation_combo.grid(row=0, column=1, padx=5, pady=5)
        self.operation_combo.bind("<<ComboboxSelected>>", self.test_operation_filter)
        
        # فلتر العناصر
        ttk.Label(filters_frame, text="اسم العنصر:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.item_var = tk.StringVar()
        self.item_combo = ttk.Combobox(filters_frame, textvariable=self.item_var, 
                                     state="readonly", width=30)
        self.item_combo.grid(row=1, column=1, padx=5, pady=5)
        self.item_combo.bind("<<ComboboxSelected>>", self.test_item_filter)
        
        # فلتر التصنيفات
        ttk.Label(filters_frame, text="التصنيف:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(filters_frame, textvariable=self.category_var, 
                                         state="readonly", width=20)
        self.category_combo.grid(row=2, column=1, padx=5, pady=5)
        self.category_combo.bind("<<ComboboxSelected>>", self.test_category_filter)
        
        # أزرار
        ttk.Button(filters_frame, text="🗑️ مسح الكل", command=self.clear_all).grid(row=3, column=0, padx=5, pady=10)
        ttk.Button(filters_frame, text="🔄 تحديث", command=self.load_data).grid(row=3, column=1, padx=5, pady=10)
        
        # منطقة النتائج
        results_frame = ttk.LabelFrame(self.root, text="📊 النتائج", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # عرض النتائج
        self.results_text = tk.Text(results_frame, height=15, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # منطقة الحالة
        self.status_label = ttk.Label(self.root, text="جاري التحميل...", font=("Arial", 10, "bold"))
        self.status_label.pack(pady=5)
    
    def load_data(self):
        """تحميل البيانات"""
        try:
            self.all_data = self.manager.get_activity_log_new_format()
            
            # تحديث القوائم
            operations = set([""])
            items = set([""])
            categories = set([""])
            
            for record in self.all_data:
                if len(record) >= 5:
                    operations.add(record[2].strip())
                    items.add(record[3].strip())
                    categories.add(record[4].strip())
            
            self.operation_combo['values'] = sorted(list(operations))
            self.item_combo['values'] = sorted(list(items))
            self.category_combo['values'] = sorted(list(categories))
            
            # عرض البيانات الأولية
            self.display_results(self.all_data, "جميع البيانات")
            self.status_label.config(text=f"✅ تم تحميل {len(self.all_data)} سجل")
            
        except Exception as e:
            self.status_label.config(text=f"❌ خطأ: {e}")
            print(f"خطأ في تحميل البيانات: {e}")
    
    def test_operation_filter(self, event=None):
        """اختبار فلتر العمليات"""
        operation = self.operation_var.get()
        
        if not operation:
            self.display_results(self.all_data, "جميع البيانات")
            return
        
        print(f"🔍 اختبار فلتر العمليات: '{operation}'")
        
        # طريقة 1: يدوي
        manual_results = []
        for record in self.all_data:
            if len(record) >= 3 and record[2].strip() == operation.strip():
                manual_results.append(record)
        
        # طريقة 2: المدير
        manager_results = self.manager.filter_activity_log_new(operation_type=operation)
        
        print(f"   📊 نتائج يدوية: {len(manual_results)}")
        print(f"   📊 نتائج المدير: {len(manager_results)}")
        
        self.display_results(manager_results, f"فلتر العمليات: {operation}")
        self.status_label.config(text=f"🔍 فلتر العمليات: {len(manager_results)} نتيجة")
    
    def test_item_filter(self, event=None):
        """اختبار فلتر العناصر"""
        item = self.item_var.get()
        
        if not item:
            self.display_results(self.all_data, "جميع البيانات")
            return
        
        print(f"🔍 اختبار فلتر العناصر: '{item}'")
        
        # طريقة 1: يدوي
        manual_results = []
        for record in self.all_data:
            if len(record) >= 4 and item.lower().strip() in record[3].lower():
                manual_results.append(record)
        
        # طريقة 2: المدير
        manager_results = self.manager.filter_activity_log_new(item_name=item)
        
        print(f"   📊 نتائج يدوية: {len(manual_results)}")
        print(f"   📊 نتائج المدير: {len(manager_results)}")
        
        self.display_results(manager_results, f"فلتر العناصر: {item}")
        self.status_label.config(text=f"🔍 فلتر العناصر: {len(manager_results)} نتيجة")
    
    def test_category_filter(self, event=None):
        """اختبار فلتر التصنيفات"""
        category = self.category_var.get()
        
        if not category:
            self.display_results(self.all_data, "جميع البيانات")
            return
        
        print(f"🔍 اختبار فلتر التصنيفات: '{category}'")
        
        # طريقة 1: يدوي
        manual_results = []
        for record in self.all_data:
            if len(record) >= 5 and category.lower().strip() in record[4].lower():
                manual_results.append(record)
        
        # طريقة 2: المدير
        manager_results = self.manager.filter_activity_log_new(category=category)
        
        print(f"   📊 نتائج يدوية: {len(manual_results)}")
        print(f"   📊 نتائج المدير: {len(manager_results)}")
        
        self.display_results(manager_results, f"فلتر التصنيفات: {category}")
        self.status_label.config(text=f"🔍 فلتر التصنيفات: {len(manager_results)} نتيجة")
    
    def clear_all(self):
        """مسح جميع الفلاتر"""
        self.operation_var.set("")
        self.item_var.set("")
        self.category_var.set("")
        self.display_results(self.all_data, "جميع البيانات")
        self.status_label.config(text=f"📊 جميع البيانات: {len(self.all_data)} سجل")
    
    def display_results(self, data, title):
        """عرض النتائج"""
        self.results_text.delete(1.0, tk.END)
        
        self.results_text.insert(tk.END, f"📋 {title}\n")
        self.results_text.insert(tk.END, "=" * 50 + "\n\n")
        
        if not data:
            self.results_text.insert(tk.END, "❌ لا توجد نتائج\n")
            return
        
        for i, record in enumerate(data[:10], 1):  # أول 10 فقط
            if len(record) >= 5:
                self.results_text.insert(tk.END, f"{i}. {record[0]} | {record[2]} | {record[3]} | {record[4]}\n")
        
        if len(data) > 10:
            self.results_text.insert(tk.END, f"\n... و {len(data) - 10} سجل آخر\n")
        
        self.results_text.insert(tk.END, f"\n📊 إجمالي النتائج: {len(data)}")
    
    def run(self):
        """تشغيل الاختبار"""
        self.root.mainloop()

if __name__ == "__main__":
    try:
        app = SimpleFilterTest()
        print("🧪 بدء اختبار الفلاتر البسيط...")
        app.run()
    except Exception as e:
        print(f"❌ خطأ: {e}")
        import traceback
        traceback.print_exc()