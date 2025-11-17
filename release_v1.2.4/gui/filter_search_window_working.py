#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نافذة البحث باستخدام الفلاتر - النسخة المستقرة العاملة
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import calendar

class FilterSearchWindow:
    """نافذة البحث باستخدام الفلاتر"""
    
    def __init__(self, parent, sheets_manager, current_user=None):
        self.parent = parent
        self.sheets_manager = sheets_manager
        self.current_user = current_user
        
        # إنشاء النافذة
        self.window = tk.Toplevel(parent)
        self.window.title("🔍 البحث باستخدام الفلاتر")
        self.window.geometry("1200x800")
        self.window.resizable(True, True)
        self.window.transient(parent)
        
        # البيانات
        self.all_items = []
        self.activity_log = []
        self.filtered_data = []
        
        # متغيرات الفلاتر
        self.filter_vars = {
            'date_from': tk.StringVar(),
            'date_to': tk.StringVar(),
            'item_name': tk.StringVar(value="جميع العناصر"),
            'category': tk.StringVar(value="جميع التصنيفات"),
            'project_id': tk.StringVar(value="جميع المشاريع")
        }
        
        self.setup_ui()
        self.load_data()
        
        # توسيط النافذة
        self.center_window()
        
        print("✅ تم إنشاء نافذة البحث باستخدام الفلاتر")
    
    def center_window(self):
        """توسيط النافذة على الشاشة"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (self.window.winfo_width() // 2)
        y = (self.window.winfo_screenheight() // 2) - (self.window.winfo_height() // 2)
        self.window.geometry(f"+{x}+{y}")
    
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        # الإطار الرئيسي
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # العنوان
        title_text = "🔍 البحث باستخدام الفلاتر"
        if self.current_user and self.current_user.get('user_type') == 'user':
            project_id = self.current_user.get('project_id', '')
            if project_id:
                title_text += f" - مشروع {project_id}"
        
        title_label = ttk.Label(main_frame, text=title_text, 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 10))
        
        # إطار الفلاتر
        self.setup_filters_frame(main_frame)
        
        # إطار النتائج
        self.setup_results_frame(main_frame)
        
        # إطار الإحصائيات
        self.setup_stats_frame(main_frame)
    
    def setup_filters_frame(self, parent):
        """إعداد إطار الفلاتر"""
        filters_frame = ttk.LabelFrame(parent, text="🔍 الفلاتر", padding="10")
        filters_frame.pack(fill=tk.X, pady=(0, 10))
        
        # الصف الأول: التواريخ
        date_frame = ttk.Frame(filters_frame)
        date_frame.pack(fill=tk.X, pady=(0, 5))
        
        # تاريخ من
        ttk.Label(date_frame, text="من تاريخ:").pack(side=tk.LEFT, padx=(0, 5))
        self.date_from_entry = ttk.Entry(date_frame, textvariable=self.filter_vars['date_from'], width=12)
        self.date_from_entry.pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(date_frame, text="📅", width=3, 
                  command=lambda: self.show_date_picker('date_from')).pack(side=tk.LEFT, padx=(0, 15))
        
        # تاريخ إلى
        ttk.Label(date_frame, text="إلى تاريخ:").pack(side=tk.LEFT, padx=(0, 5))
        self.date_to_entry = ttk.Entry(date_frame, textvariable=self.filter_vars['date_to'], width=12)
        self.date_to_entry.pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(date_frame, text="📅", width=3,
                  command=lambda: self.show_date_picker('date_to')).pack(side=tk.LEFT, padx=(0, 15))
        
        # أزرار التواريخ المحددة مسبقاً
        ttk.Button(date_frame, text="اليوم", command=lambda: self.set_date_range('today')).pack(side=tk.LEFT, padx=2)
        ttk.Button(date_frame, text="أسبوع", command=lambda: self.set_date_range('week')).pack(side=tk.LEFT, padx=2)
        ttk.Button(date_frame, text="شهر", command=lambda: self.set_date_range('month')).pack(side=tk.LEFT, padx=2)
        
        # الصف الثاني: باقي الفلاتر
        other_filters_frame = ttk.Frame(filters_frame)
        other_filters_frame.pack(fill=tk.X, pady=(5, 0))
        
        # فلتر العنصر
        ttk.Label(other_filters_frame, text="العنصر:").pack(side=tk.LEFT, padx=(0, 5))
        self.item_combobox = ttk.Combobox(other_filters_frame, textvariable=self.filter_vars['item_name'], 
                                         width=20, state="readonly")
        self.item_combobox.pack(side=tk.LEFT, padx=(0, 15))
        
        # فلتر التصنيف
        ttk.Label(other_filters_frame, text="التصنيف:").pack(side=tk.LEFT, padx=(0, 5))
        self.category_combobox = ttk.Combobox(other_filters_frame, textvariable=self.filter_vars['category'], 
                                             width=20, state="readonly")
        self.category_combobox.pack(side=tk.LEFT, padx=(0, 15))
        
        # فلتر المشروع
        ttk.Label(other_filters_frame, text="المشروع:").pack(side=tk.LEFT, padx=(0, 5))
        self.project_combobox = ttk.Combobox(other_filters_frame, textvariable=self.filter_vars['project_id'], 
                                            width=20, state="readonly")
        self.project_combobox.pack(side=tk.LEFT, padx=(0, 15))
        
        # أزرار التحكم
        controls_frame = ttk.Frame(other_filters_frame)
        controls_frame.pack(side=tk.RIGHT)
        
        ttk.Button(controls_frame, text="🔍 تطبيق", command=self.apply_filters).pack(side=tk.LEFT, padx=2)
        ttk.Button(controls_frame, text="🗑️ مسح", command=self.clear_filters).pack(side=tk.LEFT, padx=2)
        ttk.Button(controls_frame, text="📤 تصدير", command=self.export_to_csv).pack(side=tk.LEFT, padx=2)
        ttk.Button(controls_frame, text="🔄 تحديث", command=self.refresh_data).pack(side=tk.LEFT, padx=2)
    
    def setup_results_frame(self, parent):
        """إعداد إطار النتائج"""
        results_frame = ttk.LabelFrame(parent, text="📋 النتائج", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # إنشاء Treeview للنتائج
        columns = ("العنصر", "التصنيف", "النوع", "الكمية", "التاريخ", "المشروع", "التفاصيل")
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=15)
        
        # تعيين عناوين الأعمدة
        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=120, anchor=tk.CENTER)
        
        # تحسين عرض الأعمدة
        self.results_tree.column("العنصر", width=150)
        self.results_tree.column("التصنيف", width=120)
        self.results_tree.column("النوع", width=100)
        self.results_tree.column("الكمية", width=80)
        self.results_tree.column("التاريخ", width=120)
        self.results_tree.column("المشروع", width=120)
        self.results_tree.column("التفاصيل", width=200)
        
        # شريط التمرير
        scrollbar_v = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        scrollbar_h = ttk.Scrollbar(results_frame, orient=tk.HORIZONTAL, command=self.results_tree.xview)
        self.results_tree.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
        
        # ترتيب العناصر
        self.results_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_v.grid(row=0, column=1, sticky="ns")
        scrollbar_h.grid(row=1, column=0, sticky="ew")
        
        # تكوين الصفوف والأعمدة للتوسع
        results_frame.grid_rowconfigure(0, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)
    
    def setup_stats_frame(self, parent):
        """إعداد إطار الإحصائيات"""
        stats_frame = ttk.LabelFrame(parent, text="📊 الإحصائيات", padding="10")
        stats_frame.pack(fill=tk.X)
        
        # إنشاء أربعة أعمدة للإحصائيات
        left_stats = ttk.Frame(stats_frame)
        left_stats.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        center_left_stats = ttk.Frame(stats_frame)
        center_left_stats.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        center_right_stats = ttk.Frame(stats_frame)
        center_right_stats.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        right_stats = ttk.Frame(stats_frame)
        right_stats.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # إجمالي النتائج
        ttk.Label(left_stats, text="إجمالي النتائج", font=("Arial", 12, "bold")).pack()
        self.total_results_label = ttk.Label(left_stats, text="0", font=("Arial", 14), foreground="blue")
        self.total_results_label.pack()
        
        # المخزون الحالي
        ttk.Label(center_left_stats, text="المخزون الحالي", font=("Arial", 12, "bold")).pack()
        self.current_stock_label = ttk.Label(center_left_stats, text="0", font=("Arial", 14), foreground="green")
        self.current_stock_label.pack()
        
        # النشاط
        ttk.Label(center_right_stats, text="نشاط السجل", font=("Arial", 12, "bold")).pack()
        self.activity_count_label = ttk.Label(center_right_stats, text="0", font=("Arial", 14), foreground="orange")
        self.activity_count_label.pack()
        
        # المشاريع
        ttk.Label(right_stats, text="عدد المشاريع", font=("Arial", 12, "bold")).pack()
        self.projects_count_label = ttk.Label(right_stats, text="0", font=("Arial", 14), foreground="purple")
        self.projects_count_label.pack()
    
    def show_date_picker(self, date_type):
        """عرض منتقي التاريخ"""
        date_window = tk.Toplevel(self.window)
        date_window.title("📅 اختيار التاريخ")
        date_window.geometry("300x100")
        date_window.transient(self.window)
        date_window.grab_set()
        
        # توسيط النافذة
        date_window.update_idletasks()
        x = self.window.winfo_x() + (self.window.winfo_width() // 2) - (date_window.winfo_width() // 2)
        y = self.window.winfo_y() + (self.window.winfo_height() // 2) - (date_window.winfo_height() // 2)
        date_window.geometry(f"+{x}+{y}")
        
        frame = ttk.Frame(date_window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="أدخل التاريخ (YYYY-MM-DD):").pack(pady=(0, 10))
        
        date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        date_entry = ttk.Entry(frame, textvariable=date_var, width=20)
        date_entry.pack(pady=(0, 10))
        date_entry.focus()
        
        def set_date():
            try:
                # التحقق من صحة التاريخ
                datetime.strptime(date_var.get(), "%Y-%m-%d")
                self.filter_vars[date_type].set(date_var.get())
                date_window.destroy()
            except ValueError:
                messagebox.showerror("خطأ", "تنسيق التاريخ غير صحيح. استخدم YYYY-MM-DD")
        
        ttk.Button(frame, text="موافق", command=set_date).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame, text="إلغاء", command=date_window.destroy).pack(side=tk.LEFT, padx=5)
        
        date_entry.bind("<Return>", lambda e: set_date())
    
    def set_date_range(self, range_type):
        """تعيين نطاق تاريخ محدد مسبقاً"""
        print(f"📅 تعيين نطاق التاريخ: {range_type}")
        today = datetime.now()
        
        if range_type == 'today':
            date_str = today.strftime("%Y-%m-%d")
            self.filter_vars['date_from'].set(date_str)
            self.filter_vars['date_to'].set(date_str)
        
        elif range_type == 'week':
            week_start = today - timedelta(days=today.weekday())
            week_end = week_start + timedelta(days=6)
            self.filter_vars['date_from'].set(week_start.strftime("%Y-%m-%d"))
            self.filter_vars['date_to'].set(week_end.strftime("%Y-%m-%d"))
        
        elif range_type == 'month':
            month_start = today.replace(day=1)
            next_month = month_start.replace(month=month_start.month + 1) if month_start.month < 12 else month_start.replace(year=month_start.year + 1, month=1)
            month_end = next_month - timedelta(days=1)
            self.filter_vars['date_from'].set(month_start.strftime("%Y-%m-%d"))
            self.filter_vars['date_to'].set(month_end.strftime("%Y-%m-%d"))
        
        # تطبيق الفلاتر تلقائياً
        self.apply_filters()
    
    def load_data(self):
        """تحميل البيانات من Google Sheets"""
        try:
            print("📊 تحميل بيانات البحث...")
            
            # تحميل البيانات الحالية
            try:
                if hasattr(self.sheets_manager, 'get_all_items_raw'):
                    self.all_items = self.sheets_manager.get_all_items_raw()
                    print(f"📋 تم تحميل {len(self.all_items)} عنصر من المخزون")
                else:
                    # fallback للطريقة القديمة
                    raw_items = self.sheets_manager.get_all_items()
                    self.all_items = []
                    
                    if isinstance(raw_items, list) and raw_items:
                        if isinstance(raw_items[0], dict):
                            for item in raw_items:
                                self.all_items.append([
                                    item.get('item_name', ''),
                                    item.get('category', ''),
                                    str(item.get('quantity', 0)),
                                    item.get('project_id', ''),
                                    item.get('last_updated', '')
                                ])
                        else:
                            self.all_items = raw_items
                    print(f"📋 تم تحميل {len(self.all_items)} عنصر (fallback)")
                        
            except Exception as items_error:
                print(f"⚠️ خطأ في تحميل العناصر: {items_error}")
                self.all_items = []
            
            # تحميل سجل النشاط
            try:
                if hasattr(self.sheets_manager, 'get_activity_log'):
                    self.activity_log = self.sheets_manager.get_activity_log()
                    print(f"📊 تم تحميل {len(self.activity_log)} إدخال من سجل النشاط")
                else:
                    self.activity_log = []
                    print("⚠️ سجل النشاط غير متاح")
            except Exception as log_error:
                print(f"⚠️ خطأ في تحميل سجل النشاط: {log_error}")
                self.activity_log = []
            
            # تحديث قوائم الفلاتر
            self.update_filter_options()
            
            # تطبيق الفلاتر الأولية
            self.apply_filters()
            
            print("✅ تم تحميل البيانات بنجاح")
            
        except Exception as e:
            print(f"❌ خطأ في تحميل البيانات: {e}")
            messagebox.showerror("خطأ", f"فشل في تحميل البيانات:\n{e}")
    
    def update_filter_options(self):
        """تحديث خيارات الفلاتر"""
        items = set(["جميع العناصر"])
        categories = set(["جميع التصنيفات"])
        projects = set(["جميع المشاريع"])
        
        # من بيانات المخزون
        for item in self.all_items:
            if len(item) >= 4:
                if item[0]:  # اسم العنصر
                    items.add(item[0].strip())
                if item[1]:  # التصنيف
                    categories.add(item[1].strip())
                if item[3]:  # المشروع
                    projects.add(item[3].strip())
        
        # من سجل النشاط
        for log in self.activity_log:
            if len(log) >= 4:
                if log[1]:  # اسم العنصر
                    items.add(log[1].strip())
                if log[0]:  # التصنيف (قد يكون في العمود الأول)
                    if log[0] not in ['إدخال', 'إخراج', 'تحديث']:
                        categories.add(log[0].strip())
        
        # تحديث القوائم
        self.item_combobox['values'] = sorted(list(items))
        self.category_combobox['values'] = sorted(list(categories))
        self.project_combobox['values'] = sorted(list(projects))
        
        print(f"📝 تم تحديث الفلاتر: {len(items)} عنصر، {len(categories)} تصنيف، {len(projects)} مشروع")
    
    def clear_filters(self):
        """مسح جميع الفلاتر"""
        print("🗑️ مسح جميع الفلاتر...")
        
        for var in self.filter_vars.values():
            var.set("")
        
        # إعادة تعيين القيم الافتراضية
        self.filter_vars['item_name'].set("جميع العناصر")
        self.filter_vars['category'].set("جميع التصنيفات")
        self.filter_vars['project_id'].set("جميع المشاريع") 
        
        # إعادة تطبيق الفلاتر
        self.apply_filters()
        print("✅ تم مسح الفلاتر وإعادة التطبيق")
    
    def refresh_data(self):
        """تحديث البيانات"""
        print("🔄 تحديث البيانات...")
        self.load_data()
    
    def apply_filters(self):
        """تطبيق الفلاتر وعرض النتائج"""
        try:
            print("🔍 تطبيق الفلاتر...")
            
            # مسح النتائج السابقة
            for item in self.results_tree.get_children():
                self.results_tree.delete(item)
            
            self.filtered_data = []
            
            # الحصول على قيم الفلاتر
            filter_item = self.filter_vars['item_name'].get()
            filter_category = self.filter_vars['category'].get()
            filter_project = self.filter_vars['project_id'].get()
            filter_date_from = self.filter_vars['date_from'].get()
            filter_date_to = self.filter_vars['date_to'].get()
            
            print(f"🔍 الفلاتر: العنصر='{filter_item}', التصنيف='{filter_category}', المشروع='{filter_project}', من='{filter_date_from}', إلى='{filter_date_to}'")
            
            # فلترة المخزون الحالي
            current_stock_count = 0
            for item in self.all_items:
                if len(item) >= 5:
                    item_name = item[0] if item[0] else ""
                    category = item[1] if item[1] else ""
                    quantity = item[2] if item[2] else "0"
                    project = item[3] if item[3] else ""
                    date = item[4] if item[4] else ""
                    
                    if self.matches_filters(item_name, category, project, date, 
                                           filter_item, filter_category, filter_project, 
                                           filter_date_from, filter_date_to):
                        current_stock_count += 1
                        self.filtered_data.append({
                            'item_name': item_name,
                            'category': category,
                            'type': 'مخزون حالي',
                            'quantity': quantity,
                            'date': date,
                            'project': project,
                            'details': f'الكمية الحالية: {quantity}'
                        })
            
            # فلترة سجل النشاط
            activity_count = 0
            for log in self.activity_log:
                if len(log) >= 6:
                    action = log[0] if log[0] else ""
                    item_name = log[1] if log[1] else ""
                    quantity = log[2] if log[2] else "0"
                    project = log[3] if log[3] else ""
                    date = log[4] if log[4] else ""
                    details = log[5] if log[5] else ""
                    
                    # استنتاج التصنيف من التفاصيل أو تعيين قيمة افتراضية
                    category = "غير محدد"
                    if "التصنيف:" in details:
                        try:
                            category = details.split("التصنيف:")[1].split(",")[0].strip()
                        except:
                            pass
                    
                    if self.matches_filters(item_name, category, project, date, 
                                           filter_item, filter_category, filter_project, 
                                           filter_date_from, filter_date_to):
                        activity_count += 1
                        self.filtered_data.append({
                            'item_name': item_name,
                            'category': category,
                            'type': action,
                            'quantity': quantity,
                            'date': date,
                            'project': project,
                            'details': details
                        })
            
            # إضافة النتائج للجدول
            for result in self.filtered_data:
                self.results_tree.insert("", "end", values=(
                    result['item_name'],
                    result['category'],
                    result['type'],
                    result['quantity'],
                    result['date'],
                    result['project'],
                    result['details']
                ))
            
            # تحديث الإحصائيات
            self.update_statistics(current_stock_count, activity_count)
            
            print(f"✅ تم فلترة {len(self.filtered_data)} نتيجة (مخزون: {current_stock_count}, نشاط: {activity_count})")
            
        except Exception as e:
            print(f"❌ خطأ في تطبيق الفلاتر: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("خطأ", f"فشل في تطبيق الفلاتر:\n{e}")
    
    def matches_filters(self, item_name, category, project, date, 
                       filter_item, filter_category, filter_project, 
                       filter_date_from, filter_date_to):
        """فحص ما إذا كان العنصر يطابق الفلاتر"""
        
        # فلتر العنصر
        if filter_item and filter_item != "جميع العناصر":
            if not item_name or filter_item.lower() not in item_name.lower():
                return False
        
        # فلتر التصنيف
        if filter_category and filter_category != "جميع التصنيفات":
            if not category or filter_category.lower() not in category.lower():
                return False
        
        # فلتر المشروع
        if filter_project and filter_project != "جميع المشاريع":
            if not project or filter_project.lower() not in project.lower():
                return False
        
        # فلتر التاريخ
        if filter_date_from or filter_date_to:
            if not date:
                return False
                
            try:
                # استخراج التاريخ من النص
                item_date = None
                date_str = date.strip()
                
                # محاولة استخراج التاريخ بصيغ مختلفة
                if len(date_str) >= 10:
                    try:
                        item_date = datetime.strptime(date_str[:10], "%Y-%m-%d")
                    except ValueError:
                        try:
                            item_date = datetime.strptime(date_str[:10], "%d/%m/%Y")
                        except ValueError:
                            # محاولة استخراج التاريخ من نص أطول
                            import re
                            date_pattern = r'\d{4}-\d{2}-\d{2}'
                            match = re.search(date_pattern, date_str)
                            if match:
                                item_date = datetime.strptime(match.group(), "%Y-%m-%d")
                
                if item_date:
                    if filter_date_from:
                        try:
                            from_date = datetime.strptime(filter_date_from, "%Y-%m-%d")
                            if item_date < from_date:
                                return False
                        except ValueError:
                            pass
                    
                    if filter_date_to:
                        try:
                            to_date = datetime.strptime(filter_date_to, "%Y-%m-%d")
                            if item_date > to_date:
                                return False
                        except ValueError:
                            pass
                else:
                    # إذا لم نتمكن من تحليل التاريخ، نعتبر أنه لا يطابق فلتر التاريخ
                    if filter_date_from or filter_date_to:
                        return False
                        
            except Exception as e:
                print(f"⚠️ خطأ في معالجة التاريخ {date}: {e}")
                return False
        
        return True
    
    def update_statistics(self, current_stock_count, activity_count):
        """تحديث الإحصائيات"""
        total_results = len(self.filtered_data)
        
        # حساب عدد المشاريع الفريدة
        projects = set()
        for result in self.filtered_data:
            if result['project']:
                projects.add(result['project'])
        
        # تحديث التسميات
        self.total_results_label.config(text=str(total_results))
        self.current_stock_label.config(text=str(current_stock_count))
        self.activity_count_label.config(text=str(activity_count))
        self.projects_count_label.config(text=str(len(projects)))
        
        print(f"📊 الإحصائيات: إجمالي={total_results}, مخزون={current_stock_count}, نشاط={activity_count}, مشاريع={len(projects)}")
    
    def export_to_csv(self):
        """تصدير النتائج إلى CSV"""
        try:
            if not self.filtered_data:
                messagebox.showwarning("تحذير", "لا توجد نتائج للتصدير")
                return
                
            from tkinter import filedialog
            import csv
            
            # اختيار مكان الحفظ
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="حفظ النتائج"
            )
            
            if filename:
                with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # كتابة العناوين
                    headers = ["العنصر", "التصنيف", "النوع", "الكمية", "التاريخ", "المشروع", "التفاصيل"]
                    writer.writerow(headers)
                    
                    # كتابة البيانات
                    for result in self.filtered_data:
                        writer.writerow([
                            result['item_name'],
                            result['category'],
                            result['type'],
                            result['quantity'],
                            result['date'],
                            result['project'],
                            result['details']
                        ])
                
                messagebox.showinfo("نجح", f"تم تصدير {len(self.filtered_data)} نتيجة إلى:\n{filename}")
                print(f"📤 تم تصدير {len(self.filtered_data)} نتيجة إلى: {filename}")
                
        except Exception as e:
            print(f"❌ خطأ في التصدير: {e}")
            messagebox.showerror("خطأ", f"فشل في تصدير النتائج:\n{e}")

def show_filter_search_window(parent, sheets_manager, current_user=None):
    """عرض نافذة البحث باستخدام الفلاتر"""
    return FilterSearchWindow(parent, sheets_manager, current_user)