#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نافذة التقارير والتحليل المُعاد بناؤها - نسخة منظمة
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import calendar

class ReportsWindow:
    """نافذة التقارير والتحليل - نسخة محسنة"""
    
    def __init__(self, parent, sheets_manager, current_user=None):
        self.parent = parent
        self.sheets_manager = sheets_manager
        self.current_user = current_user
        
        # البيانات
        self.all_items = []
        self.activity_log = []
        
        # متغيرات الفلاتر
        self.filter_vars = {
            'date_from': tk.StringVar(),
            'date_to': tk.StringVar(),
            'item_name': tk.StringVar(value="جميع العناصر"),
            'project_id': tk.StringVar(value="جميع المشاريع")
        }
        
        # إنشاء النافذة
        self.create_window()
        self.create_widgets()
        self.load_data()
        
        print("✅ تم إنشاء نافذة التقارير الجديدة")
    
    def create_window(self):
        """إنشاء النافذة الرئيسية"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("📊 التقارير والتحليل")
        self.window.geometry("1400x900")
        self.window.resizable(True, True)
        self.window.transient(self.parent)
        
        # توسيط النافذة
        self.center_window()
    
    def center_window(self):
        """توسيط النافذة على الشاشة"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (self.window.winfo_width() // 2)
        y = (self.window.winfo_screenheight() // 2) - (self.window.winfo_height() // 2)
        self.window.geometry(f"+{x}+{y}")
    
    def create_widgets(self):
        """إنشاء جميع العناصر"""
        # الإطار الرئيسي
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 1. إطار الفلاتر
        self.create_filters_frame(main_frame)
        
        # 2. إطار الجدول
        self.create_table_frame(main_frame)
        
        # 3. إطار الإحصائيات
        self.create_stats_frame(main_frame)
    
    def create_filters_frame(self, parent):
        """إطار الفلاتر"""
        filters_frame = ttk.LabelFrame(parent, text="🔍 الفلاتر", padding="10")
        filters_frame.pack(fill=tk.X, pady=(0, 10))
        
        # الصف الأول: التواريخ
        date_row = ttk.Frame(filters_frame)
        date_row.pack(fill=tk.X, pady=(0, 10))
        
        # من تاريخ
        ttk.Label(date_row, text="من تاريخ:").pack(side=tk.LEFT, padx=(0, 5))
        self.date_from_entry = ttk.Entry(date_row, textvariable=self.filter_vars['date_from'], width=12)
        self.date_from_entry.pack(side=tk.LEFT, padx=(0, 15))
        
        # إلى تاريخ
        ttk.Label(date_row, text="إلى تاريخ:").pack(side=tk.LEFT, padx=(0, 5))
        self.date_to_entry = ttk.Entry(date_row, textvariable=self.filter_vars['date_to'], width=12)
        self.date_to_entry.pack(side=tk.LEFT, padx=(0, 15))
        
        # أزرار التواريخ السريعة
        ttk.Button(date_row, text="اليوم", command=lambda: self.set_date_range('today')).pack(side=tk.LEFT, padx=2)
        ttk.Button(date_row, text="أسبوع", command=lambda: self.set_date_range('week')).pack(side=tk.LEFT, padx=2)
        ttk.Button(date_row, text="شهر", command=lambda: self.set_date_range('month')).pack(side=tk.LEFT, padx=2)
        ttk.Button(date_row, text="مسح التواريخ", command=self.clear_dates).pack(side=tk.LEFT, padx=2)
        
        # الصف الثاني: باقي الفلاتر
        filter_row = ttk.Frame(filters_frame)
        filter_row.pack(fill=tk.X, pady=(0, 10))
        
        # فلتر العنصر
        ttk.Label(filter_row, text="العنصر:").pack(side=tk.LEFT, padx=(0, 5))
        self.item_combobox = ttk.Combobox(filter_row, textvariable=self.filter_vars['item_name'], 
                                         width=20, state="readonly")
        self.item_combobox.pack(side=tk.LEFT, padx=(0, 15))
        
        # فلتر المشروع
        ttk.Label(filter_row, text="المشروع:").pack(side=tk.LEFT, padx=(0, 5))
        self.project_combobox = ttk.Combobox(filter_row, textvariable=self.filter_vars['project_id'], 
                                            width=20, state="readonly")
        self.project_combobox.pack(side=tk.LEFT, padx=(0, 15))
        
        # الصف الثالث: أزرار التحكم
        control_row = ttk.Frame(filters_frame)
        control_row.pack(fill=tk.X)
        
        ttk.Button(control_row, text="🔍 تطبيق الفلتر", command=self.apply_filters).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_row, text="🗑️ مسح الفلاتر", command=self.clear_filters).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_row, text="🔄 تحديث البيانات", command=self.refresh_data).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_row, text="📤 تصدير Excel", command=self.export_excel).pack(side=tk.LEFT, padx=2)
    
    def create_table_frame(self, parent):
        """إطار الجدول"""
        table_frame = ttk.LabelFrame(parent, text="📊 النتائج", padding="10")
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # إنشاء الجدول
        columns = ("العنصر", "الدخول", "تاريخ الدخول", "الخروج", "تاريخ الخروج", "المشروع")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        
        # تعيين عناوين الأعمدة
        for col in columns:
            self.tree.heading(col, text=col, anchor=tk.CENTER)
            self.tree.column(col, width=150, anchor=tk.CENTER)
        
        # تحسين عرض الأعمدة
        self.tree.column("العنصر", width=200)
        self.tree.column("الدخول", width=100)
        self.tree.column("تاريخ الدخول", width=130)
        self.tree.column("الخروج", width=100)
        self.tree.column("تاريخ الخروج", width=130)
        self.tree.column("المشروع", width=150)
        
        # أشرطة التمرير
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # ترتيب العناصر
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # تكوين التوسع
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # متغير لعرض عدد النتائج
        self.results_label = ttk.Label(table_frame, text="عدد النتائج: 0", font=("Arial", 10))
        self.results_label.grid(row=2, column=0, columnspan=2, pady=(5, 0))
    
    def create_stats_frame(self, parent):
        """إطار الإحصائيات"""
        stats_frame = ttk.LabelFrame(parent, text="📈 الإحصائيات", padding="10")
        stats_frame.pack(fill=tk.X)
        
        # ثلاثة أعمدة للإحصائيات
        for i in range(3):
            stats_frame.grid_columnconfigure(i, weight=1)
        
        # إجمالي الدخول
        in_frame = ttk.Frame(stats_frame)
        in_frame.grid(row=0, column=0, padx=10, pady=5)
        ttk.Label(in_frame, text="إجمالي الدخول", font=("Arial", 12, "bold")).pack()
        self.total_in_label = ttk.Label(in_frame, text="0.0", font=("Arial", 16), foreground="green")
        self.total_in_label.pack()
        
        # إجمالي الخروج
        out_frame = ttk.Frame(stats_frame)
        out_frame.grid(row=0, column=1, padx=10, pady=5)
        ttk.Label(out_frame, text="إجمالي الخروج", font=("Arial", 12, "bold")).pack()
        self.total_out_label = ttk.Label(out_frame, text="0.0", font=("Arial", 16), foreground="red")
        self.total_out_label.pack()
        
        # الرصيد الحالي
        balance_frame = ttk.Frame(stats_frame)
        balance_frame.grid(row=0, column=2, padx=10, pady=5)
        ttk.Label(balance_frame, text="الرصيد الحالي", font=("Arial", 12, "bold")).pack()
        self.balance_label = ttk.Label(balance_frame, text="0.0", font=("Arial", 16), foreground="blue")
        self.balance_label.pack()
    
    def set_date_range(self, range_type):
        """تعيين نطاق تاريخ محدد"""
        today = datetime.now()
        
        if range_type == 'today':
            date_str = today.strftime("%Y-%m-%d")
            self.filter_vars['date_from'].set(date_str)
            self.filter_vars['date_to'].set(date_str)
            print(f"📅 تم تعيين تاريخ اليوم: {date_str}")
        
        elif range_type == 'week':
            week_start = today - timedelta(days=today.weekday())
            week_end = week_start + timedelta(days=6)
            self.filter_vars['date_from'].set(week_start.strftime("%Y-%m-%d"))
            self.filter_vars['date_to'].set(week_end.strftime("%Y-%m-%d"))
            print(f"📅 تم تعيين الأسبوع: {week_start.strftime('%Y-%m-%d')} - {week_end.strftime('%Y-%m-%d')}")
        
        elif range_type == 'month':
            month_start = today.replace(day=1)
            if month_start.month == 12:
                next_month = month_start.replace(year=month_start.year + 1, month=1)
            else:
                next_month = month_start.replace(month=month_start.month + 1)
            month_end = next_month - timedelta(days=1)
            self.filter_vars['date_from'].set(month_start.strftime("%Y-%m-%d"))
            self.filter_vars['date_to'].set(month_end.strftime("%Y-%m-%d"))
            print(f"📅 تم تعيين الشهر: {month_start.strftime('%Y-%m-%d')} - {month_end.strftime('%Y-%m-%d')}")
        
        # تطبيق الفلاتر
        self.apply_filters()
    
    def clear_dates(self):
        """مسح التواريخ"""
        self.filter_vars['date_from'].set("")
        self.filter_vars['date_to'].set("")
        print("📅 تم مسح التواريخ")
        self.apply_filters()
    
    def clear_filters(self):
        """مسح جميع الفلاتر"""
        for var in self.filter_vars.values():
            var.set("")
        self.filter_vars['item_name'].set("جميع العناصر")
        self.filter_vars['project_id'].set("جميع المشاريع")
        print("🗑️ تم مسح جميع الفلاتر")
        self.apply_filters()
    
    def refresh_data(self):
        """تحديث البيانات"""
        print("🔄 تحديث البيانات...")
        self.load_data()
    
    def export_excel(self):
        """تصدير إلى Excel"""
        messagebox.showinfo("تصدير", "سيتم إضافة تصدير Excel قريباً")
    
    def load_data(self):
        """تحميل البيانات"""
        try:
            print("📊 تحميل البيانات...")
            
            # تحميل المخزون الحالي
            if hasattr(self.sheets_manager, 'get_all_items_raw'):
                self.all_items = self.sheets_manager.get_all_items_raw()
                print(f"📦 تم تحميل {len(self.all_items)} عنصر من المخزون")
            else:
                self.all_items = []
                print("⚠️ لا يمكن تحميل المخزون")
            
            # تحميل سجل النشاط
            if hasattr(self.sheets_manager, 'get_activity_log'):
                self.activity_log = self.sheets_manager.get_activity_log()
                print(f"📋 تم تحميل {len(self.activity_log)} إدخال من سجل النشاط")
            else:
                self.activity_log = []
                print("⚠️ لا يمكن تحميل سجل النشاط")
            
            # تحديث خيارات الفلاتر
            self.update_filter_options()
            
            # تطبيق الفلاتر
            self.apply_filters()
            
            print("✅ تم تحميل البيانات بنجاح")
            
        except Exception as e:
            print(f"❌ خطأ في تحميل البيانات: {e}")
            messagebox.showerror("خطأ", f"فشل في تحميل البيانات:\n{e}")
    
    def update_filter_options(self):
        """تحديث خيارات الفلاتر"""
        items = set(["جميع العناصر"])
        projects = set(["جميع المشاريع"])
        
        # من المخزون الحالي
        for item in self.all_items:
            if len(item) >= 4:
                if item[0]:  # اسم العنصر
                    items.add(item[0])
                if item[3]:  # المشروع
                    projects.add(item[3])
        
        # من سجل النشاط
        for log in self.activity_log:
            if len(log) >= 6:
                if log[2]:  # اسم العنصر
                    items.add(log[2])
                # استخراج المشروع من التفاصيل
                project = self.extract_project_from_details(log[5] if len(log) > 5 else "")
                if project:
                    projects.add(project)
        
        # تحديث القوائم
        self.item_combobox['values'] = sorted(list(items))
        self.project_combobox['values'] = sorted(list(projects))
    
    def extract_project_from_details(self, details):
        """استخراج رقم المشروع من التفاصيل"""
        if not details:
            return ""
        if "للمشروع" in details:
            try:
                project_part = details.split("للمشروع")[1].strip()
                project_id = project_part.split()[0]
                return project_id
            except:
                pass
        return ""
    
    def apply_filters(self):
        """تطبيق الفلاتر"""
        try:
            print("🔍 تطبيق الفلاتر...")
            
            # مسح الجدول
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # الحصول على قيم الفلاتر
            filter_item = self.filter_vars['item_name'].get()
            filter_project = self.filter_vars['project_id'].get()
            filter_date_from = self.filter_vars['date_from'].get()
            filter_date_to = self.filter_vars['date_to'].get()
            
            print(f"🎯 الفلاتر: العنصر={filter_item}, المشروع={filter_project}")
            print(f"📅 التواريخ: من {filter_date_from} إلى {filter_date_to}")
            
            # تجميع البيانات حسب العنصر
            items_data = {}
            
            # معالجة سجل النشاط
            for log in self.activity_log:
                if len(log) >= 6:
                    date = log[0] if log[0] else ""
                    action = log[1] if log[1] else ""
                    item_name = log[2] if log[2] else ""
                    quantity = log[3] if log[3] else "0"
                    details = log[5] if len(log) > 5 else ""
                    
                    # استخراج المشروع
                    project = self.extract_project_from_details(details)
                    
                    # تطبيق الفلاتر
                    if self.matches_filters(item_name, project, date, filter_item, filter_project, filter_date_from, filter_date_to):
                        # إنشاء مدخل للعنصر
                        if item_name not in items_data:
                            items_data[item_name] = {
                                'in_qty': 0, 'in_date': '',
                                'out_qty': 0, 'out_date': '',
                                'project': project
                            }
                        
                        try:
                            qty = float(quantity) if quantity else 0
                            
                            if action in ["إضافة", "تعديل", "إدخال"]:
                                items_data[item_name]['in_qty'] += qty
                                if date and (not items_data[item_name]['in_date'] or date > items_data[item_name]['in_date']):
                                    items_data[item_name]['in_date'] = date
                            elif action in ["إخراج", "خروج"]:
                                items_data[item_name]['out_qty'] += qty
                                if date and (not items_data[item_name]['out_date'] or date > items_data[item_name]['out_date']):
                                    items_data[item_name]['out_date'] = date
                        except ValueError:
                            continue
            
            # إضافة البيانات للجدول
            total_in = 0
            total_out = 0
            
            for item_name, data in items_data.items():
                in_qty = data['in_qty']
                out_qty = data['out_qty']
                
                total_in += in_qty
                total_out += out_qty
                
                # إضافة الصف
                values = (
                    item_name,
                    f"{in_qty:.1f}" if in_qty > 0 else "",
                    data['in_date'] if in_qty > 0 else "",
                    f"{out_qty:.1f}" if out_qty > 0 else "",
                    data['out_date'] if out_qty > 0 else "",
                    data['project']
                )
                
                self.tree.insert("", "end", values=values)
                print(f"➕ {values}")
            
            # تحديث الإحصائيات
            balance = total_in - total_out
            self.total_in_label.config(text=f"{total_in:.1f}")
            self.total_out_label.config(text=f"{total_out:.1f}")
            self.balance_label.config(text=f"{balance:.1f}")
            
            # تحديث عدد النتائج
            count = len(items_data)
            self.results_label.config(text=f"عدد النتائج: {count}")
            
            print(f"✅ تم عرض {count} عنصر")
            print(f"📊 الإحصائيات: دخول={total_in:.1f}, خروج={total_out:.1f}, رصيد={balance:.1f}")
            
        except Exception as e:
            print(f"❌ خطأ في تطبيق الفلاتر: {e}")
            messagebox.showerror("خطأ", f"حدث خطأ في تطبيق الفلاتر:\n{e}")
    
    def matches_filters(self, item_name, project, date, filter_item, filter_project, filter_date_from, filter_date_to):
        """فحص ما إذا كان العنصر يطابق الفلاتر"""
        
        # فلتر العنصر
        if filter_item and filter_item != "جميع العناصر":
            if not item_name or item_name.strip().lower() != filter_item.strip().lower():
                return False
        
        # فلتر المشروع
        if filter_project and filter_project != "جميع المشاريع":
            if not project or project.strip().lower() != filter_project.strip().lower():
                return False
        
        # فلتر التاريخ
        if filter_date_from or filter_date_to:
            if not date:
                return False
            
            try:
                # استخراج التاريخ
                if ' ' in date:
                    date_part = date.split(' ')[0]
                else:
                    date_part = date
                
                from datetime import datetime
                item_date = datetime.strptime(date_part, "%Y-%m-%d")
                
                if filter_date_from:
                    from_date = datetime.strptime(filter_date_from, "%Y-%m-%d")
                    if item_date < from_date:
                        return False
                
                if filter_date_to:
                    to_date = datetime.strptime(filter_date_to, "%Y-%m-%d")
                    if item_date > to_date:
                        return False
                        
            except Exception as e:
                print(f"⚠️ خطأ في معالجة التاريخ {date}: {e}")
                return False
        
        return True


# استخدام النافذة الجديدة بدلاً من القديمة
ReportsAnalysisWindow = ReportsWindow