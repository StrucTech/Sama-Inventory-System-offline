#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نافذة التقارير والتحليل - عرض تفصيلي للمواد الداخلة والخارجة مع الفلاتر
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import calendar

class ReportsAnalysisWindow:
    """نافذة التقارير والتحليل"""
    
    def __init__(self, parent, sheets_manager, current_user=None):
        self.parent = parent
        self.sheets_manager = sheets_manager
        self.current_user = current_user
        
        # إنشاء النافذة
        self.window = tk.Toplevel(parent)
        self.window.title("التقارير والتحليل")
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
            'project_id': tk.StringVar(value="جميع المشاريع")
        }
        
        self.setup_ui()
        self.load_data()
        
        # توسيط النافذة
        self.center_window()
    
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
        title_label = ttk.Label(main_frame, text="التقارير والتحليل", 
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
        filters_frame = ttk.LabelFrame(parent, text="الفلاتر", padding="10")
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
        
        # فلتر المشروع
        ttk.Label(other_filters_frame, text="المشروع:").pack(side=tk.LEFT, padx=(0, 5))
        self.project_combobox = ttk.Combobox(other_filters_frame, textvariable=self.filter_vars['project_id'], 
                                            width=20, state="readonly")
        self.project_combobox.pack(side=tk.LEFT, padx=(0, 15))
        
        # أزرار التحكم
        controls_frame = ttk.Frame(other_filters_frame)
        controls_frame.pack(side=tk.RIGHT)
        
        ttk.Button(controls_frame, text="تطبيق الفلتر", command=self.apply_filters).pack(side=tk.LEFT, padx=2)
        ttk.Button(controls_frame, text="مسح الفلاتر", command=self.clear_filters).pack(side=tk.LEFT, padx=2)
        ttk.Button(controls_frame, text="تصدير Excel", command=self.export_to_excel).pack(side=tk.LEFT, padx=2)
    
    def setup_results_frame(self, parent):
        """إعداد إطار النتائج"""
        results_frame = ttk.LabelFrame(parent, text="النتائج", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # إنشاء Treeview للنتائج
        columns = ("العنصر", "الدخول", "تاريخ الدخول", "الخروج", "تاريخ الخروج", "المشروع")
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=15)
        
        # تعيين عناوين الأعمدة
        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=120, anchor=tk.CENTER)
        
        # تحسين عرض الأعمدة
        self.results_tree.column("العنصر", width=150)
        self.results_tree.column("الدخول", width=100)
        self.results_tree.column("تاريخ الدخول", width=120)
        self.results_tree.column("الخروج", width=100)
        self.results_tree.column("تاريخ الخروج", width=120)
        self.results_tree.column("المشروع", width=150)
        
        # شريط التمرير
        scrollbar_v = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        scrollbar_h = ttk.Scrollbar(results_frame, orient=tk.HORIZONTAL, command=self.results_tree.xview)
        self.results_tree.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
        
        # ترتيب العناصر - استخدام grid بدلاً من pack
        self.results_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_v.grid(row=0, column=1, sticky="ns")
        scrollbar_h.grid(row=1, column=0, sticky="ew")
        
        # تكوين الصفوف والأعمدة للتوسع
        results_frame.grid_rowconfigure(0, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)
    
    def setup_stats_frame(self, parent):
        """إعداد إطار الإحصائيات"""
        stats_frame = ttk.LabelFrame(parent, text="الإحصائيات", padding="10")
        stats_frame.pack(fill=tk.X)
        
        # إنشاء ثلاثة أعمدة للإحصائيات
        left_stats = ttk.Frame(stats_frame)
        left_stats.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        center_stats = ttk.Frame(stats_frame)
        center_stats.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        right_stats = ttk.Frame(stats_frame)
        right_stats.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # الإحصائيات اليسرى
        ttk.Label(left_stats, text="إجمالي الداخل", font=("Arial", 12, "bold")).pack()
        self.total_in_label = ttk.Label(left_stats, text="0", font=("Arial", 14), foreground="green")
        self.total_in_label.pack()
        
        # الإحصائيات الوسطى
        ttk.Label(center_stats, text="إجمالي الخارج", font=("Arial", 12, "bold")).pack()
        self.total_out_label = ttk.Label(center_stats, text="0", font=("Arial", 14), foreground="red")
        self.total_out_label.pack()
        
        # الإحصائيات اليمنى
        ttk.Label(right_stats, text="الرصيد الحالي", font=("Arial", 12, "bold")).pack()
        self.current_balance_label = ttk.Label(right_stats, text="0", font=("Arial", 14), foreground="blue")
        self.current_balance_label.pack()
    
    def show_date_picker(self, date_type):
        """عرض منتقي التاريخ"""
        # نافذة بسيطة لاختيار التاريخ
        date_window = tk.Toplevel(self.window)
        date_window.title("اختيار التاريخ")
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
            print(f"📅 تم تعيين اليوم: {date_str}")
        
        elif range_type == 'week':
            week_start = today - timedelta(days=today.weekday())
            week_end = week_start + timedelta(days=6)
            self.filter_vars['date_from'].set(week_start.strftime("%Y-%m-%d"))
            self.filter_vars['date_to'].set(week_end.strftime("%Y-%m-%d"))
            print(f"📅 تم تعيين الأسبوع: من {week_start.strftime('%Y-%m-%d')} إلى {week_end.strftime('%Y-%m-%d')}")
        
        elif range_type == 'month':
            month_start = today.replace(day=1)
            next_month = month_start.replace(month=month_start.month + 1) if month_start.month < 12 else month_start.replace(year=month_start.year + 1, month=1)
            month_end = next_month - timedelta(days=1)
            self.filter_vars['date_from'].set(month_start.strftime("%Y-%m-%d"))
            self.filter_vars['date_to'].set(month_end.strftime("%Y-%m-%d"))
            print(f"📅 تم تعيين الشهر: من {month_start.strftime('%Y-%m-%d')} إلى {month_end.strftime('%Y-%m-%d')}")
        
        # تطبيق الفلاتر تلقائياً
        self.apply_filters()
    
    def load_data(self):
        """تحميل البيانات من Google Sheets"""
        try:
            print("📊 تحميل بيانات التقارير...")
            
            # تحميل البيانات الحالية باستخدام الدالة الجديدة
            try:
                if hasattr(self.sheets_manager, 'get_all_items_raw'):
                    self.all_items = self.sheets_manager.get_all_items_raw()
                    print(f"📋 استخدام get_all_items_raw: تم تحميل {len(self.all_items)} عنصر")
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
                    print(f"📋 استخدام fallback: تم تحميل {len(self.all_items)} عنصر")
                        
            except Exception as items_error:
                print(f"⚠️ خطأ في تحميل العناصر: {items_error}")
                self.all_items = []
            
            # تحميل سجل النشاط
            try:
                self.activity_log = self.sheets_manager.get_activity_log()
                print(f"📊 تم تحميل {len(self.activity_log)} إدخال من سجل النشاط")
            except Exception as log_error:
                print(f"⚠️ خطأ في تحميل سجل النشاط: {log_error}")
                self.activity_log = []
            
            # تحديث قوائم الفلاتر
            self.update_filter_options()
            
            # تطبيق الفلاتر الافتراضية
            self.apply_filters()
            
            print("✅ تم تحميل البيانات بنجاح")
            
        except Exception as e:
            print(f"❌ خطأ عام في تحميل البيانات: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("خطأ", f"فشل في تحميل البيانات: {str(e)}\n\nيرجى التأكد من الاتصال بـ Google Sheets")
    
    def update_filter_options(self):
        """تحديث خيارات الفلاتر"""
        # جمع العناصر الفريدة
        items = set(["جميع العناصر"])
        projects = set(["جميع المشاريع"])
        
        for item in self.all_items:
            if len(item) >= 4:
                if item[0]:  # اسم العنصر
                    items.add(item[0])
                if item[3]:  # المشروع
                    projects.add(item[3])
        
        # تحديث القوائم
        self.item_combobox['values'] = sorted(list(items))
        self.project_combobox['values'] = sorted(list(projects))
    
    def apply_filters(self):
        """تطبيق الفلاتر وعرض النتائج"""
        try:
            print("🔍 تطبيق الفلاتر...")
            
            # مسح النتائج الحالية
            print(f"🗑️ مسح {len(self.results_tree.get_children())} صف من الجدول...")
            for item in self.results_tree.get_children():
                self.results_tree.delete(item)
            
            # تحديث العرض
            self.results_tree.update()
            
            filtered_data = []
            
            # الحصول على قيم الفلاتر
            filter_item = self.filter_vars['item_name'].get()
            filter_project = self.filter_vars['project_id'].get()
            filter_date_from = self.filter_vars['date_from'].get()
            filter_date_to = self.filter_vars['date_to'].get()
            
            print(f"🎯 الفلاتر: العنصر={filter_item}, المشروع={filter_project}")
            print(f"📅 التواريخ: من {filter_date_from} إلى {filter_date_to}")
            
            # تجميع البيانات حسب العنصر
            items_data = {}  # {'item_name': {'in_qty': 0, 'in_date': '', 'out_qty': 0, 'out_date': '', 'project': ''}}
            
            # معالجة سجل النشاط
            print(f"� معالجة {len(self.activity_log)} إدخال من سجل النشاط...")
            for log_entry in self.activity_log:
                if len(log_entry) >= 6:
                    date = log_entry[0] if log_entry[0] else ""
                    action = log_entry[1] if log_entry[1] else ""
                    item_name = log_entry[2] if log_entry[2] else ""
                    quantity = log_entry[3] if log_entry[3] else "0"
                    recipient_name = log_entry[4] if log_entry[4] else ""
                    details = log_entry[5] if log_entry[5] else ""
                    
                    # استخراج المشروع من التفاصيل
                    project_id = self.extract_project_from_details(details)
                    
                    # تطبيق الفلاتر
                    if self.matches_filters(item_name, project_id, date, 
                                          filter_item, filter_project, 
                                          filter_date_from, filter_date_to):
                        
                        # إنشاء مدخل للعنصر إذا لم يكن موجوداً
                        if item_name not in items_data:
                            items_data[item_name] = {
                                'in_qty': 0, 'in_date': '', 
                                'out_qty': 0, 'out_date': '', 
                                'project': project_id
                            }
                        
                        try:
                            qty = float(quantity) if quantity else 0
                            
                            if action == "إضافة" or action == "تعديل":
                                items_data[item_name]['in_qty'] += qty
                                if date and (not items_data[item_name]['in_date'] or date > items_data[item_name]['in_date']):
                                    items_data[item_name]['in_date'] = date
                            elif action == "إخراج":
                                items_data[item_name]['out_qty'] += qty
                                if date and (not items_data[item_name]['out_date'] or date > items_data[item_name]['out_date']):
                                    items_data[item_name]['out_date'] = date
                                    
                        except ValueError:
                            continue
            
            # إضافة البيانات للجدول
            total_in = 0
            total_out = 0
            
            print(f"📊 إضافة {len(items_data)} عنصر للجدول...")
            
            for item_name, data in items_data.items():
                in_qty = data['in_qty']
                out_qty = data['out_qty']
                
                total_in += in_qty
                total_out += out_qty
                
                # إضافة صف للجدول
                row_values = (
                    item_name,
                    f"{in_qty:.1f}" if in_qty > 0 else "",
                    data['in_date'] if in_qty > 0 else "",
                    f"{out_qty:.1f}" if out_qty > 0 else "",
                    data['out_date'] if out_qty > 0 else "",
                    data['project']
                )
                
                print(f"➕ إضافة صف: {row_values}")
                self.results_tree.insert("", "end", values=row_values)
            
            # تحديث العرض بقوة
            self.results_tree.update_idletasks()
            self.window.update_idletasks()
            print(f"🔄 تم تحديث الجدول - العدد الحالي: {len(self.results_tree.get_children())}")
            
            # التأكد من أن الجدول مرئي
            if hasattr(self.results_tree, 'see'):
                try:
                    children = self.results_tree.get_children()
                    if children:
                        self.results_tree.see(children[0])  # انتقال لأول عنصر
                except:
                    pass
            
            # حساب المتبقي
            remaining = total_in - total_out
            
            print(f"✅ تم فلترة {len(items_data)} عنصر")
            print(f"📊 الإحصائيات: إدخال={total_in:.1f}, إخراج={total_out:.1f}, متبقي={remaining:.1f}")
            
            # تحديث الإحصائيات
            self.total_in_label.config(text=f"{total_in:.1f}")
            self.total_out_label.config(text=f"{total_out:.1f}")
            self.current_balance_label.config(text=f"{remaining:.1f}")
            
            print("✅ تم تطبيق الفلاتر بنجاح")
        
        except Exception as e:
            print(f"❌ خطأ في تطبيق الفلاتر: {e}")
            messagebox.showerror("خطأ", f"حدث خطأ في تطبيق الفلاتر:\n{e}")
            self.calculate_statistics(filtered_data)
            
            print("✅ تم تطبيق الفلاتر بنجاح")
            
        except Exception as e:
            print(f"❌ خطأ في تطبيق الفلاتر: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("خطأ", f"فشل في تطبيق الفلاتر: {str(e)}")
    
    def extract_project_from_details(self, details):
        """استخراج رقم المشروع من التفاصيل"""
        if "للمشروع" in details:
            try:
                project_part = details.split("للمشروع")[1].strip()
                # استخراج أول كلمة بعد "للمشروع"
                project_id = project_part.split()[0]
                return project_id
            except:
                pass
        return ""
    
    def matches_filters(self, item_name, project_id, date, 
                       filter_item, filter_project, 
                       filter_date_from, filter_date_to):
        """فحص ما إذا كان العنصر يطابق الفلاتر"""
        
        # فلتر العنصر
        if filter_item and filter_item != "جميع العناصر":
            if not item_name or item_name.strip().lower() != filter_item.strip().lower():
                return False
        
        # فلتر المشروع
        if filter_project and filter_project != "جميع المشاريع":
            if not project_id or project_id.strip().lower() != filter_project.strip().lower():
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
                            pass
                
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
    
    def display_results(self, data):
        """عرض النتائج في الجدول"""
        for item in data:
            self.results_tree.insert("", tk.END, values=(
                item['item_name'],
                item['category'],
                item['type'],
                item['quantity'],
                item['project_id'],
                item['date'],
                item['details']
            ))
    
    def calculate_statistics(self, data):
        """حساب الإحصائيات"""
        total_in = 0
        total_out = 0
        current_balance = 0
        
        for item in data:
            try:
                quantity = float(item['quantity']) if item['quantity'] else 0
                
                if item['type'] in ['إدخال', 'إضافة', 'تحديث']:
                    total_in += quantity
                elif item['type'] in ['إخراج', 'خروج']:
                    total_out += quantity
                elif item['type'] == 'مخزون حالي':
                    current_balance += quantity
                    
            except (ValueError, TypeError):
                continue
        
        # تحديث التسميات
        self.total_in_label.config(text=f"{total_in:,.0f}")
        self.total_out_label.config(text=f"{total_out:,.0f}")
        self.current_balance_label.config(text=f"{current_balance:,.0f}")
        
        print(f"📊 الإحصائيات: إدخال={total_in}, إخراج={total_out}, رصيد={current_balance}")
    
    def clear_filters(self):
        """مسح جميع الفلاتر"""
        print("🗑️ مسح جميع الفلاتر...")
        
        for var in self.filter_vars.values():
            var.set("")
        
        # إعادة تعيين القيم الافتراضية
        self.filter_vars['item_name'].set("جميع العناصر")
        self.filter_vars['project_id'].set("جميع المشاريع") 
        
        # إعادة تطبيق الفلاتر
        self.apply_filters()
        print("✅ تم مسح الفلاتر وإعادة التطبيق")
    
    def export_to_excel(self):
        """تصدير النتائج إلى Excel"""
        try:
            from tkinter import filedialog
            import csv
            
            # اختيار مكان الحفظ
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="حفظ التقرير"
            )
            
            if filename:
                with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # كتابة العناوين
                    headers = ["العنصر", "التصنيف", "النوع", "الكمية", "المشروع", "التاريخ", "التفاصيل"]
                    writer.writerow(headers)
                    
                    # كتابة البيانات
                    for item in self.results_tree.get_children():
                        values = self.results_tree.item(item)['values']
                        writer.writerow(values)
                
                messagebox.showinfo("نجح", f"تم تصدير التقرير إلى:\n{filename}")
                
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في تصدير التقرير: {str(e)}")

def show_reports_window(parent, sheets_manager, current_user=None):
    """عرض نافذة التقارير والتحليل"""
    return ReportsAnalysisWindow(parent, sheets_manager, current_user)