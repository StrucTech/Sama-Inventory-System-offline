"""
🔍 نظام البحث والفلاتر المحسن - يقرأ من Activity_Log_v2_20251108
==================================================================

الميزات:
- قراءة العمليات من شيت Activity_Log_v2_20251108
- عرض جميع العمليات (إدخال/إخراج) مع التفاصيل الكاملة
- فلاتر: التاريخ، التصنيف، اسم العنصر، المشروع
- إحصائيات: إجمالي الإدخال، الإخراج، المتبقي
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import sys
import os
import traceback

# إضافة مسار المشروع
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sheets.manager import SheetsManager

class ActivityLogSearchSystem:
    def __init__(self, parent=None, sheets_manager=None):
        """تهيئة نظام البحث في سجل العمليات"""
        
        self.parent = parent
        self.window = None
        self.sheets_manager = sheets_manager  # استخدام الاتصال الموجود
        
        # بيانات النظام
        self.activity_data = []       # بيانات العمليات من Activity_Log_v2_20251108
        self.filtered_data = []       # البيانات المفلترة
        self.inventory_data = []      # بيانات المخزون للحصول على الكميات المتبقية
        
        # متغيرات الفلاتر
        self.filter_vars = {}
        
        # خيارات الفلاتر
        self.filter_options = {
            'dates': ['الكل'],
            'categories': ['الكل'], 
            'items': ['الكل'],
            'projects': ['الكل']
        }
        
        # إحصائيات
        self.statistics = {
            'total_incoming': 0,
            'total_outgoing': 0,
            'total_remaining': 0,
            'operations_count': 0
        }

    def create_window(self):
        """إنشاء النافذة الرئيسية"""
        
        self.window = tk.Toplevel(self.parent) if self.parent else tk.Tk()
        self.window.title("🔍 نظام البحث في سجل العمليات - Activity_Log_v2_20251108")
        self.window.geometry("1600x900")
        self.window.configure(bg="#1a1a2e")
        self.window.resizable(True, True)
        
        # تهيئة متغيرات الفلاتر
        self.init_filter_vars()
        
        # إنشاء الواجهة
        self.create_interface()
        
        # تحميل البيانات
        self.load_data()
        
        return self.window

    def init_filter_vars(self):
        """تهيئة متغيرات الفلاتر"""
        self.filter_vars = {
            'date': tk.StringVar(value="الكل"),
            'category': tk.StringVar(value="الكل"),
            'item': tk.StringVar(value="الكل"),
            'project': tk.StringVar(value="الكل"),
            'date_from': tk.StringVar(),
            'date_to': tk.StringVar(),
            'user': tk.StringVar(value="الكل")
        }

    def create_interface(self):
        """إنشاء واجهة المستخدم"""
        
        # الإطار الرئيسي
        main_frame = tk.Frame(self.window, bg="#1a1a2e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # العنوان
        title_label = tk.Label(
            main_frame,
            text="🔍 نظام البحث والفلاتر - سجل العمليات",
            font=("Arial", 20, "bold"),
            bg="#1a1a2e", fg="#daa520",
            pady=20
        )
        title_label.pack(fill=tk.X)
        
        # إطار الفلاتر
        self.create_filters_frame(main_frame)
        
        # إطار الإحصائيات
        self.create_statistics_frame(main_frame)
        
        # إطار النتائج
        self.create_results_frame(main_frame)
        
        # شريط الحالة
        self.status_label = tk.Label(
            main_frame,
            text="🔄 جاري التهيئة...",
            bg="#1a1a2e", fg="#3498db",
            font=("Arial", 12, "bold")
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

    def create_filters_frame(self, parent):
        """إنشاء إطار الفلاتر"""
        
        filters_frame = tk.LabelFrame(
            parent,
            text="🎯 الفلاتر",
            font=("Arial", 16, "bold"),
            bg="#2c3e60", fg="#ecf0f1",
            relief="groove", bd=4
        )
        filters_frame.pack(fill=tk.X, pady=(0, 15))
        
        # الصف الأول من الفلاتر
        row1 = tk.Frame(filters_frame, bg="#2c3e60")
        row1.pack(fill=tk.X, padx=15, pady=10)
        
        # فلتر التاريخ المحدد
        tk.Label(row1, text="📅 التاريخ:", bg="#2c3e60", fg="#ecf0f1",
                font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, sticky="w")
        self.date_combo = ttk.Combobox(row1, textvariable=self.filter_vars['date'],
                                      width=15, state="readonly", font=("Arial", 11))
        self.date_combo.grid(row=0, column=1, padx=10)
        self.date_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_filters())
        
        # فلتر التصنيف
        tk.Label(row1, text="🏷️ التصنيف:", bg="#2c3e60", fg="#ecf0f1",
                font=("Arial", 12, "bold")).grid(row=0, column=2, padx=10, sticky="w")
        self.category_combo = ttk.Combobox(row1, textvariable=self.filter_vars['category'],
                                          width=18, state="readonly", font=("Arial", 11))
        self.category_combo.grid(row=0, column=3, padx=10)
        self.category_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_filters())
        
        # فلتر العنصر
        tk.Label(row1, text="📦 اسم العنصر:", bg="#2c3e60", fg="#ecf0f1",
                font=("Arial", 12, "bold")).grid(row=0, column=4, padx=10, sticky="w")
        self.item_combo = ttk.Combobox(row1, textvariable=self.filter_vars['item'],
                                      width=20, state="readonly", font=("Arial", 11))
        self.item_combo.grid(row=0, column=5, padx=10)
        self.item_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_filters())
        
        # الصف الثاني من الفلاتر
        row2 = tk.Frame(filters_frame, bg="#2c3e60")
        row2.pack(fill=tk.X, padx=15, pady=10)
        
        # فلتر المشروع
        tk.Label(row2, text="🎯 المشروع:", bg="#2c3e60", fg="#ecf0f1",
                font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, sticky="w")
        self.project_combo = ttk.Combobox(row2, textvariable=self.filter_vars['project'],
                                         width=18, state="readonly", font=("Arial", 11))
        self.project_combo.grid(row=0, column=1, padx=10)
        self.project_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_filters())
        
        # فلتر المستخدم
        tk.Label(row2, text="👤 المستخدم:", bg="#2c3e60", fg="#ecf0f1",
                font=("Arial", 12, "bold")).grid(row=0, column=2, padx=10, sticky="w")
        self.user_combo = ttk.Combobox(row2, textvariable=self.filter_vars['user'],
                                      width=18, state="readonly", font=("Arial", 11))
        self.user_combo.grid(row=0, column=3, padx=10)
        self.user_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_filters())
        
        # نطاق التواريخ
        tk.Label(row2, text="📅 من:", bg="#2c3e60", fg="#ecf0f1",
                font=("Arial", 12, "bold")).grid(row=0, column=4, padx=5, sticky="w")
        self.date_from_entry = tk.Entry(row2, textvariable=self.filter_vars['date_from'],
                                       width=12, font=("Arial", 11))
        self.date_from_entry.grid(row=0, column=5, padx=5)
        self.date_from_entry.bind('<KeyRelease>', lambda e: self.delayed_filter())
        
        tk.Label(row2, text="📅 إلى:", bg="#2c3e60", fg="#ecf0f1",
                font=("Arial", 12, "bold")).grid(row=0, column=6, padx=5, sticky="w")
        self.date_to_entry = tk.Entry(row2, textvariable=self.filter_vars['date_to'],
                                     width=12, font=("Arial", 11))
        self.date_to_entry.grid(row=0, column=7, padx=5)
        self.date_to_entry.bind('<KeyRelease>', lambda e: self.delayed_filter())
        
        # أزرار التحكم
        controls_frame = tk.Frame(filters_frame, bg="#2c3e60")
        controls_frame.pack(pady=15)
        
        # زر التطبيق
        apply_btn = tk.Button(
            controls_frame, text="🔍 تطبيق الفلاتر",
            command=self.apply_filters,
            bg="#27ae60", fg="white", font=("Arial", 13, "bold"),
            relief="flat", cursor="hand2", padx=20, pady=8
        )
        apply_btn.pack(side=tk.LEFT, padx=10)
        
        # زر المسح
        clear_btn = tk.Button(
            controls_frame, text="🗑️ مسح الفلاتر", 
            command=self.clear_filters,
            bg="#e74c3c", fg="white", font=("Arial", 13, "bold"),
            relief="flat", cursor="hand2", padx=20, pady=8
        )
        clear_btn.pack(side=tk.LEFT, padx=10)
        
        # زر التحديث
        refresh_btn = tk.Button(
            controls_frame, text="🔄 تحديث البيانات",
            command=self.refresh_data,
            bg="#3498db", fg="white", font=("Arial", 13, "bold"),
            relief="flat", cursor="hand2", padx=20, pady=8
        )
        refresh_btn.pack(side=tk.LEFT, padx=10)

    def create_statistics_frame(self, parent):
        """إنشاء إطار الإحصائيات"""
        
        stats_frame = tk.LabelFrame(
            parent,
            text="📊 الإحصائيات",
            font=("Arial", 16, "bold"),
            bg="#2c3e60", fg="#ecf0f1",
            relief="groove", bd=4
        )
        stats_frame.pack(fill=tk.X, pady=(0, 15))
        
        # إطار الإحصائيات
        stats_container = tk.Frame(stats_frame, bg="#2c3e60")
        stats_container.pack(fill=tk.X, padx=15, pady=15)
        
        # تسميات الإحصائيات
        self.stats_labels = {}
        
        stats_data = [
            ('العمليات', 'operations_count', '#3498db', '📈'),
            ('إجمالي الإدخال', 'total_incoming', '#27ae60', '📥'),
            ('إجمالي الإخراج', 'total_outgoing', '#e74c3c', '📤'),
            ('الكمية المتبقية', 'total_remaining', '#f39c12', '📦')
        ]
        
        for i, (label, key, color, icon) in enumerate(stats_data):
            frame = tk.Frame(stats_container, bg=color, relief="raised", bd=3)
            frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
            
            # أيقونة وعنوان
            header_label = tk.Label(frame, text=f"{icon} {label}", 
                                   bg=color, fg="white", font=("Arial", 12, "bold"))
            header_label.pack(pady=5)
            
            # القيمة
            self.stats_labels[key] = tk.Label(frame, text="0", 
                                             bg=color, fg="white", 
                                             font=("Arial", 16, "bold"))
            self.stats_labels[key].pack(pady=5)

    def create_results_frame(self, parent):
        """إنشاء إطار النتائج"""
        
        results_frame = tk.LabelFrame(
            parent,
            text="📋 نتائج البحث - العمليات",
            font=("Arial", 16, "bold"),
            bg="#2c3e60", fg="#ecf0f1",
            relief="groove", bd=4
        )
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # إطار الجدول
        table_frame = tk.Frame(results_frame, bg="#2c3e60")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # أعمدة الجدول
        columns = ('التاريخ', 'الوقت', 'العملية', 'اسم العنصر', 'التصنيف', 
                   'الكمية', 'اسم المستخدم', 'المشروع', 'التفاصيل')
        
        self.results_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20)
        
        # تحديد عناوين وأحجام الأعمدة
        column_widths = {
            'التاريخ': 100, 'الوقت': 80, 'العملية': 100, 'اسم العنصر': 150,
            'التصنيف': 120, 'الكمية': 80, 'اسم المستخدم': 120,
            'المشروع': 100, 'التفاصيل': 200
        }
        
        for col in columns:
            self.results_tree.heading(col, text=col, anchor='center')
            self.results_tree.column(col, width=column_widths.get(col, 100), anchor='center')
        
        # أشرطة التمرير
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, 
                                   command=self.results_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL,
                                   command=self.results_tree.xview)
        
        self.results_tree.configure(yscrollcommand=v_scrollbar.set, 
                                   xscrollcommand=h_scrollbar.set)
        
        # تخطيط الجدول
        self.results_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

    def load_data(self):
        """تحميل البيانات من Google Sheets"""
        
        try:
            self.status_label.config(text="📡 جاري الاتصال بـ Google Sheets...")
            self.window.update()
            
            # الاتصال بـ Google Sheets
            self.sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
            
            if not self.sheets_manager.connect():
                raise Exception("فشل في الاتصال بـ Google Sheets")
            
            print("✅ تم الاتصال بـ Google Sheets بنجاح")
            
            # تحميل بيانات سجل العمليات
            self.load_activity_log_data()
            
            # تحميل بيانات المخزون للكميات المتبقية
            self.load_inventory_data()
            
            # إعداد الفلاتر
            self.setup_filters()
            
            # عرض البيانات الأولية
            self.apply_filters()
            
            self.status_label.config(text="✅ تم تحميل جميع البيانات بنجاح")
            
        except Exception as e:
            error_msg = f"❌ خطأ في تحميل البيانات: {str(e)}"
            print(error_msg)
            print("تفاصيل الخطأ:")
            traceback.print_exc()
            self.status_label.config(text=error_msg)
            messagebox.showerror("خطأ", error_msg)

    def load_activity_log_data(self):
        """تحميل بيانات سجل العمليات من Activity_Log_v2_20251108"""
        
        try:
            self.status_label.config(text="📊 جاري تحميل سجل العمليات من Activity_Log_v2_20251108...")
            self.window.update()
            
            # محاولة الوصول لشيت سجل العمليات
            activity_worksheet = self.sheets_manager.spreadsheet.worksheet('Activity_Log_v2_20251108')
            activity_values = activity_worksheet.get_all_values()
            
            if not activity_values:
                print("⚠️ لا توجد بيانات في شيت Activity_Log_v2_20251108")
                self.activity_data = []
                return
            
            # استخراج العناوين والبيانات
            headers = activity_values[0]
            print(f"📋 عناوين الأعمدة: {headers}")
            
            self.activity_data = []
            
            for i, row in enumerate(activity_values[1:], 2):  # بدء من الصف الثاني
                if len(row) >= len(headers) and row[0]:  # التأكد من وجود تاريخ
                    activity_record = {}
                    
                    # تعيين البيانات حسب العناوين
                    for j, header in enumerate(headers):
                        activity_record[header] = row[j] if j < len(row) else ""
                    
                    # إضافة معرف الصف
                    activity_record['row_number'] = i
                    
                    self.activity_data.append(activity_record)
            
            print(f"✅ تم تحميل {len(self.activity_data)} عملية من سجل النشاط")
            
            # عرض عينة من البيانات
            if self.activity_data:
                print("🔍 عينة من البيانات:")
                for i, record in enumerate(self.activity_data[:3]):
                    print(f"   العملية {i+1}: {record}")
                
                # عرض البيانات فوراً بعد التحميل
                self.setup_filters()
                self.apply_filters()
            
        except Exception as e:
            error_msg = f"❌ خطأ في تحميل سجل العمليات: {str(e)}"
            print(error_msg)
            traceback.print_exc()
            
            # إنشاء بيانات تجريبية للاختبار
            self.create_sample_activity_data()

    def create_sample_activity_data(self):
        """إنشاء بيانات عمليات تجريبية للاختبار"""
        
        print("🔄 إنشاء بيانات عمليات تجريبية...")
        
        sample_data = []
        base_date = datetime.now()
        
        operations = ['إدخال', 'إخراج', 'تعديل']
        items = ['أسمنت أبيض', 'طوب أحمر', 'كابل كهرباء', 'مفاتيح كهربائية']
        categories = ['مواد البناء', 'أدوات كهربائية', 'أدوات سباكة']
        projects = ['PRJ_001', 'PRJ_002', 'PRJ_003']
        users = ['admin', 'محمد أحمد', 'فاطمة علي']
        
        for i in range(50):  # إنشاء 50 عملية تجريبية
            operation_date = base_date - timedelta(days=i//3)
            date_str = operation_date.strftime("%Y-%m-%d")
            time_str = operation_date.strftime("%H:%M:%S")
            
            operation_type = operations[i % len(operations)]
            item_name = items[i % len(items)]
            category = categories[i % len(categories)]
            project = projects[i % len(projects)]
            user = users[i % len(users)]
            quantity = (i % 10 + 1) * 5
            
            record = {
                'التاريخ': date_str,
                'الوقت': time_str,
                'نوع العملية': operation_type,
                'اسم العنصر': item_name,
                'التصنيف': category,
                'الكمية': str(quantity),
                'اسم المستخدم': user,
                'رقم المشروع': project,
                'التفاصيل': f'{operation_type} {quantity} من {item_name}',
                'row_number': i + 2
            }
            
            sample_data.append(record)
        
        self.activity_data = sample_data
        print(f"✅ تم إنشاء {len(self.activity_data)} عملية تجريبية")

    def load_inventory_data(self):
        """تحميل بيانات المخزون للحصول على الكميات المتبقية"""
        
        try:
            self.status_label.config(text="📦 جاري تحميل بيانات المخزون...")
            self.window.update()
            
            # الحصول على بيانات المخزون
            inventory_values = self.sheets_manager.worksheet.get_all_values()
            
            if not inventory_values:
                self.inventory_data = []
                return
            
            headers = inventory_values[0]
            self.inventory_data = []
            
            for row in inventory_values[1:]:
                if len(row) >= len(headers) and row[0]:
                    item_data = {}
                    for i, header in enumerate(headers):
                        item_data[header] = row[i] if i < len(row) else ""
                    self.inventory_data.append(item_data)
            
            print(f"✅ تم تحميل {len(self.inventory_data)} عنصر من المخزون")
            
        except Exception as e:
            print(f"⚠️ خطأ في تحميل بيانات المخزون: {str(e)}")
            self.inventory_data = []

    def setup_filters(self):
        """إعداد قوائم الفلاتر"""
        
        try:
            print("🔧 إعداد قوائم الفلاتر...")
            
            # استخراج القيم الفريدة للفلاتر
            dates_set = set()
            categories_set = set()
            items_set = set()
            projects_set = set()
            users_set = set()
            
            for record in self.activity_data:
                # التواريخ
                date_val = record.get('التاريخ', '')
                if date_val:
                    dates_set.add(date_val)
                
                # التصنيفات  
                category = record.get('التصنيف', '')
                if category:
                    categories_set.add(category)
                
                # العناصر
                item = record.get('اسم العنصر', '')
                if item:
                    items_set.add(item)
                
                # المشاريع
                project = record.get('رقم المشروع', '')
                if project:
                    projects_set.add(project)
                
                # المستخدمين
                user = record.get('اسم المستخدم', '')
                if user:
                    users_set.add(user)
            
            # تحديث قوائم الفلاتر
            self.filter_options['dates'] = ['الكل'] + sorted(list(dates_set))
            self.filter_options['categories'] = ['الكل'] + sorted(list(categories_set))
            self.filter_options['items'] = ['الكل'] + sorted(list(items_set))
            self.filter_options['projects'] = ['الكل'] + sorted(list(projects_set))
            self.filter_options['users'] = ['الكل'] + sorted(list(users_set))
            
            # تحديث الـ Comboboxes
            self.date_combo['values'] = self.filter_options['dates']
            self.category_combo['values'] = self.filter_options['categories']
            self.item_combo['values'] = self.filter_options['items']
            self.project_combo['values'] = self.filter_options['projects']
            self.user_combo['values'] = self.filter_options['users']
            
            print(f"🔧 تم تحديث قيم القوائم المنسدلة:")
            print(f"   📅 التواريخ: {len(self.filter_options['dates'])} قيمة")
            print(f"   🏷️ التصنيفات: {len(self.filter_options['categories'])} قيمة") 
            print(f"   📦 العناصر: {len(self.filter_options['items'])} قيمة")
            print(f"   🎯 المشاريع: {len(self.filter_options['projects'])} قيمة")
            print(f"   👤 المستخدمين: {len(self.filter_options['users'])} قيمة")
            
            # Note: Event bindings are already set in create_filters_frame() - no need to override them
            
            print("✅ تم إعداد قوائم الفلاتر بنجاح")
            print(f"   📅 التواريخ: {len(self.filter_options['dates'])-1}")
            print(f"   🏷️ التصنيفات: {len(self.filter_options['categories'])-1}")
            print(f"   📦 العناصر: {len(self.filter_options['items'])-1}")
            print(f"   🎯 المشاريع: {len(self.filter_options['projects'])-1}")
            
        except Exception as e:
            print(f"❌ خطأ في إعداد الفلاتر: {str(e)}")
            traceback.print_exc()

    def delayed_filter(self):
        """تطبيق الفلاتر بعد تأخير قصير (للحقول النصية)"""
        # تأخير تطبيق الفلاتر للحقول النصية
        if hasattr(self, '_filter_timer'):
            self.window.after_cancel(self._filter_timer)
        self._filter_timer = self.window.after(500, self.apply_filters)  # تأخير 500 ميلي ثانية

    def apply_filters(self):
        """تطبيق الفلاتر وعرض النتائج"""
        
        try:
            print("🔍 تطبيق الفلاتر...")
            
            # الحصول على قيم الفلاتر
            filters = {}
            for key, var in self.filter_vars.items():
                filters[key] = var.get().strip()
            
            print(f"📋 الفلاتر المطبقة: {filters}")
            print(f"📊 عدد السجلات الأصلية: {len(self.activity_data)}")
            
            # تطبيق الفلاتر
            self.filtered_data = []
            print(f"🔄 بدء تطبيق الفلاتر...")
            
            for record in self.activity_data:
                include_record = True
                
                # فلتر التاريخ
                if filters['date'] != "الكل":
                    record_date = record.get('التاريخ', '')
                    if record_date != filters['date']:
                        include_record = False
                
                # فلتر نطاق التواريخ
                if filters['date_from'] or filters['date_to']:
                    record_date = record.get('التاريخ', '')
                    if record_date:
                        try:
                            record_date_obj = datetime.strptime(record_date, "%Y-%m-%d")
                            
                            if filters['date_from']:
                                from_date = datetime.strptime(filters['date_from'], "%Y-%m-%d")
                                if record_date_obj < from_date:
                                    include_record = False
                            
                            if filters['date_to']:
                                to_date = datetime.strptime(filters['date_to'], "%Y-%m-%d")
                                if record_date_obj > to_date:
                                    include_record = False
                        except ValueError:
                            continue
                
                # فلتر التصنيف
                if filters['category'] != "الكل":
                    if record.get('التصنيف', '') != filters['category']:
                        include_record = False
                
                # فلتر العنصر
                if filters['item'] != "الكل":
                    if record.get('اسم العنصر', '') != filters['item']:
                        include_record = False
                
                # فلتر المشروع
                if filters['project'] != "الكل":
                    if record.get('رقم المشروع', '') != filters['project']:
                        include_record = False
                
                # فلتر المستخدم
                if filters['user'] != "الكل":
                    if record.get('اسم المستخدم', '') != filters['user']:
                        include_record = False
                
                if include_record:
                    self.filtered_data.append(record)
            
            print(f"📈 عدد السجلات بعد الفلترة: {len(self.filtered_data)}")
            
            # عرض النتائج
            print(f"🖥️ بدء عرض النتائج...")
            self.display_results()
            
            print(f"📊 حساب الإحصائيات...")
            self.calculate_statistics()
            
            print(f"✅ تم العثور على {len(self.filtered_data)} عملية مطابقة من أصل {len(self.activity_data)}")
            
            # تحديث شريط الحالة
            self.status_label.config(
                text=f"✅ النتائج: {len(self.filtered_data)} عملية من أصل {len(self.activity_data)}"
            )
            
            # تأكيد نهائي للتحديث
            if hasattr(self, 'results_tree'):
                actual_count = len(self.results_tree.get_children())
                print(f"🎯 التأكيد النهائي: الجدول يعرض {actual_count} عنصر")
                if actual_count != len(self.filtered_data):
                    print(f"⚠️ تحذير: عدم تطابق! متوقع {len(self.filtered_data)} لكن الجدول يعرض {actual_count}")
            
            print("="*50 + "\n")
            
        except Exception as e:
            error_msg = f"❌ خطأ في تطبيق الفلاتر: {str(e)}"
            print(error_msg)
            traceback.print_exc()
            self.status_label.config(text=error_msg)

    def display_results(self):
        """عرض نتائج البحث"""
        
        print(f"🖥️ عرض {len(self.filtered_data)} نتيجة...")
        
        # مسح البيانات السابقة
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # إضافة النتائج الجديدة
        for i, record in enumerate(self.filtered_data):
            # تحديد الكمية بناءً على نوع العملية
            added_qty = record.get('الكمية المضافة', '0')
            removed_qty = record.get('الكمية المخرجة', '0')
            
            # عرض الكمية المناسبة
            if added_qty != '0':
                quantity_display = f"+{added_qty}"
            elif removed_qty != '0':
                quantity_display = f"-{removed_qty}"
            else:
                quantity_display = "0"
            
            values = (
                record.get('التاريخ', ''),
                record.get('الوقت', ''),
                record.get('نوع العملية', ''),
                record.get('اسم العنصر', ''),
                record.get('التصنيف', ''),
                quantity_display,
                record.get('اسم المستخدم', ''),
                record.get('رقم المشروع', ''),
                record.get('التفاصيل', '')
            )
            self.results_tree.insert("", "end", values=values)
        
        print(f"✅ تم عرض {len(self.filtered_data)} نتيجة")
        
        # تحديث الواجهة
        if hasattr(self, 'window') and self.window:
            self.window.update_idletasks()
            if hasattr(self, 'results_tree'):
                self.results_tree.update_idletasks()

    def calculate_statistics(self):
        """حساب الإحصائيات"""
        
        try:
            # إعادة تعيين الإحصائيات
            stats = {
                'operations_count': len(self.filtered_data),
                'total_incoming': 0,
                'total_outgoing': 0,
                'total_remaining': 0
            }
            
            # حساب الإدخال والإخراج من العمليات المفلترة
            for record in self.filtered_data:
                operation_type = record.get('نوع العملية', '')
                
                # محاولة الحصول على الكمية من أعمدة مختلفة
                incoming_str = record.get('الكمية المضافة', '0')
                outgoing_str = record.get('الكمية المخرجة', '0')
                general_quantity = record.get('الكمية', '0')
                
                try:
                    # حساب الكميات الداخلة
                    incoming = int(incoming_str) if incoming_str.isdigit() else 0
                    if incoming > 0:
                        stats['total_incoming'] += incoming
                    
                    # حساب الكميات الخارجة
                    outgoing = int(outgoing_str) if outgoing_str.isdigit() else 0
                    if outgoing > 0:
                        stats['total_outgoing'] += outgoing
                    
                    # إذا لم توجد أعمدة منفصلة، استخدم نوع العملية والكمية العامة
                    if incoming == 0 and outgoing == 0 and general_quantity:
                        quantity = int(general_quantity) if general_quantity.isdigit() else 0
                        if operation_type in ['إدخال', 'إضافة']:
                            stats['total_incoming'] += quantity
                        elif operation_type in ['إخراج', 'حذف']:
                            stats['total_outgoing'] += quantity
                        
                except (ValueError, TypeError):
                    continue
            
            # حساب الكمية المتبقية من بيانات المخزون
            for item in self.inventory_data:
                remaining_str = item.get('الكمية المتبقية', '0')
                try:
                    remaining = int(remaining_str) if remaining_str.isdigit() else 0
                    stats['total_remaining'] += remaining
                except (ValueError, TypeError):
                    continue
            
            # تحديث التسميات
            self.stats_labels['operations_count'].config(text=str(stats['operations_count']))
            self.stats_labels['total_incoming'].config(text=f"{stats['total_incoming']:,}")
            self.stats_labels['total_outgoing'].config(text=f"{stats['total_outgoing']:,}")
            self.stats_labels['total_remaining'].config(text=f"{stats['total_remaining']:,}")
            
            self.statistics = stats
            
            print(f"📊 الإحصائيات: العمليات:{stats['operations_count']}, إدخال:{stats['total_incoming']}, إخراج:{stats['total_outgoing']}, متبقي:{stats['total_remaining']}")
            
        except Exception as e:
            print(f"❌ خطأ في حساب الإحصائيات: {str(e)}")
            traceback.print_exc()

    def clear_filters(self):
        """مسح جميع الفلاتر"""
        
        try:
            print("🗑️ مسح جميع الفلاتر...")
            
            # إعادة تعيين قيم الفلاتر
            for key, var in self.filter_vars.items():
                if key in ['date_from', 'date_to']:
                    var.set("")
                else:
                    var.set("الكل")
            
            # تحديث قيم القوائم المنسدلة فوراً
            if hasattr(self, 'date_combo'):
                self.date_combo.set("الكل")
            if hasattr(self, 'category_combo'):
                self.category_combo.set("الكل")
            if hasattr(self, 'item_combo'):
                self.item_combo.set("الكل")
            if hasattr(self, 'project_combo'):
                self.project_combo.set("الكل")
            if hasattr(self, 'user_combo'):
                self.user_combo.set("الكل")
            
            # إلغاء أي مؤقت تطبيق معلق
            if hasattr(self, '_filter_timer'):
                self.window.after_cancel(self._filter_timer)
            
            # تطبيق الفلاتر فوراً
            print("🔄 تطبيق الفلاتر بعد المسح...")
            self.apply_filters()
            
            # تأكيد التحديث
            if hasattr(self, 'window') and self.window:
                self.window.after(100, lambda: print(f"📊 عدد العناصر في الجدول بعد المسح: {len(self.results_tree.get_children())}"))
            
            print("✅ تم مسح جميع الفلاتر وإعادة عرض جميع البيانات")
            
        except Exception as e:
            print(f"❌ خطأ في مسح الفلاتر: {str(e)}")
            import traceback
            traceback.print_exc()

    def refresh_data(self):
        """تحديث البيانات"""
        
        self.status_label.config(text="🔄 جاري تحديث البيانات...")
        self.window.update()
        
        # إعادة تحميل البيانات
        self.load_data()

    def run(self):
        """تشغيل النافذة"""
        if self.window:
            self.window.mainloop()


def main():
    """الدالة الرئيسية"""
    
    print("🔍 نظام البحث والفلاتر - سجل العمليات من Activity_Log_v2_20251108")
    print("=" * 80)
    
    try:
        system = ActivityLogSearchSystem()
        window = system.create_window()
        system.run()
        
    except Exception as e:
        print(f"❌ خطأ في تشغيل النظام: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    main()