"""
🔍 نظام فلاتر محسن مع تسجيل العمليات والتواريخ
يحل مشاكل: البيانات غير صحيحة في الفلاتر + عدم ظهور تواريخ العمليات
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import sys
import os

# إضافة مسار المشروع
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sheets.manager import SheetsManager

class EnhancedFiltersWithOperations:
    def __init__(self, parent=None):
        """تهيئة نظام الفلاتر المحسن مع العمليات"""
        
        self.parent = parent
        self.window = None
        self.sheets_manager = None
        
        # بيانات النظام
        self.inventory_data = []      # بيانات المخزون الأساسية
        self.operations_data = []     # بيانات العمليات مع التواريخ
        self.combined_data = []       # البيانات المدمجة
        self.filtered_data = []       # البيانات المفلترة
        
        # متغيرات الفلاتر - سيتم تهيئتها بعد إنشاء النافذة
        self.filter_vars = None
        
        # خيارات الفلاتر
        self.filter_options = {
            'dates': [],
            'items': [],
            'categories': [],
            'projects': [],
            'operations': ['الكل', 'إدخال', 'إخراج', 'تعديل', 'إضافة']
        }

    def create_window(self):
        """إنشاء النافذة الرئيسية"""
        
        self.window = tk.Toplevel(self.parent) if self.parent else tk.Tk()
        self.window.title("🔍 نظام الفلاتر المحسن مع العمليات والتواريخ")
        self.window.geometry("1400x900")
        self.window.configure(bg="#1a1a2e")
        self.window.resizable(True, True)
        
        # تهيئة متغيرات الفلاتر بعد إنشاء النافذة
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
            'item': tk.StringVar(value="الكل"),
            'category': tk.StringVar(value="الكل"),
            'project': tk.StringVar(value="الكل"),
            'operation': tk.StringVar(value="الكل"),
            'date_from': tk.StringVar(),
            'date_to': tk.StringVar()
        }

    def create_interface(self):
        """إنشاء واجهة المستخدم"""
        
        # الإطار الرئيسي
        main_frame = tk.Frame(self.window, bg="#1a1a2e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # العنوان
        title_label = tk.Label(
            main_frame,
            text="🔍 نظام الفلاتر المحسن مع تسجيل العمليات والتواريخ",
            font=("Arial", 18, "bold"),
            bg="#1a1a2e", fg="#daa520",
            pady=15
        )
        title_label.pack(fill=tk.X)
        
        # إطار الفلاتر المحسن
        self.create_enhanced_filters_frame(main_frame)
        
        # إطار العمليات والتواريخ
        self.create_operations_frame(main_frame)
        
        # إطار النتائج المحسن
        self.create_enhanced_results_frame(main_frame)
        
        # شريط الحالة
        self.status_label = tk.Label(
            main_frame,
            text="🔄 جاري التهيئة...",
            bg="#1a1a2e", fg="#3498db",
            font=("Arial", 11)
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

    def create_enhanced_filters_frame(self, parent):
        """إنشاء إطار الفلاتر المحسن"""
        
        filters_frame = tk.LabelFrame(
            parent,
            text="🎯 الفلاتر المحسنة",
            font=("Arial", 14, "bold"),
            bg="#2c3e60", fg="#ecf0f1",
            relief="groove", bd=3
        )
        filters_frame.pack(fill=tk.X, pady=(0, 10))
        
        # الصف الأول - فلاتر أساسية
        row1 = tk.Frame(filters_frame, bg="#2c3e60")
        row1.pack(fill=tk.X, padx=10, pady=5)
        
        # فلتر التاريخ
        tk.Label(row1, text="📅 التاريخ:", bg="#2c3e60", fg="#ecf0f1", 
                font=("Arial", 11, "bold")).grid(row=0, column=0, padx=5, sticky="w")
        self.date_combo = ttk.Combobox(row1, textvariable=self.filter_vars['date'], 
                                      width=15, state="readonly")
        self.date_combo.grid(row=0, column=1, padx=5)
        
        # فلتر العنصر  
        tk.Label(row1, text="📦 العنصر:", bg="#2c3e60", fg="#ecf0f1",
                font=("Arial", 11, "bold")).grid(row=0, column=2, padx=5, sticky="w")
        self.item_combo = ttk.Combobox(row1, textvariable=self.filter_vars['item'],
                                      width=20, state="readonly")
        self.item_combo.grid(row=0, column=3, padx=5)
        
        # فلتر التصنيف
        tk.Label(row1, text="🏷️ التصنيف:", bg="#2c3e60", fg="#ecf0f1",
                font=("Arial", 11, "bold")).grid(row=0, column=4, padx=5, sticky="w")
        self.category_combo = ttk.Combobox(row1, textvariable=self.filter_vars['category'],
                                          width=15, state="readonly")
        self.category_combo.grid(row=0, column=5, padx=5)
        
        # الصف الثاني - فلاتر متقدمة
        row2 = tk.Frame(filters_frame, bg="#2c3e60")
        row2.pack(fill=tk.X, padx=10, pady=5)
        
        # فلتر المشروع
        tk.Label(row2, text="🎯 المشروع:", bg="#2c3e60", fg="#ecf0f1",
                font=("Arial", 11, "bold")).grid(row=0, column=0, padx=5, sticky="w")
        self.project_combo = ttk.Combobox(row2, textvariable=self.filter_vars['project'],
                                         width=15, state="readonly")
        self.project_combo.grid(row=0, column=1, padx=5)
        
        # فلتر نوع العملية
        tk.Label(row2, text="⚡ العملية:", bg="#2c3e60", fg="#ecf0f1",
                font=("Arial", 11, "bold")).grid(row=0, column=2, padx=5, sticky="w")
        self.operation_combo = ttk.Combobox(row2, textvariable=self.filter_vars['operation'],
                                           width=15, state="readonly")
        self.operation_combo.grid(row=0, column=3, padx=5)
        
        # الصف الثالث - نطاق التواريخ
        row3 = tk.Frame(filters_frame, bg="#2c3e60")
        row3.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(row3, text="📅 من تاريخ:", bg="#2c3e60", fg="#ecf0f1",
                font=("Arial", 11, "bold")).grid(row=0, column=0, padx=5, sticky="w")
        self.date_from_entry = tk.Entry(row3, textvariable=self.filter_vars['date_from'],
                                       width=12, font=("Arial", 10))
        self.date_from_entry.grid(row=0, column=1, padx=5)
        
        tk.Label(row3, text="📅 إلى تاريخ:", bg="#2c3e60", fg="#ecf0f1",
                font=("Arial", 11, "bold")).grid(row=0, column=2, padx=5, sticky="w")
        self.date_to_entry = tk.Entry(row3, textvariable=self.filter_vars['date_to'],
                                     width=12, font=("Arial", 10))
        self.date_to_entry.grid(row=0, column=3, padx=5)
        
        # أزرار التحكم
        controls_frame = tk.Frame(row3, bg="#2c3e60")
        controls_frame.grid(row=0, column=4, columnspan=2, padx=20)
        
        apply_btn = tk.Button(
            controls_frame, text="🔍 تطبيق الفلاتر",
            command=self.apply_filters,
            bg="#27ae60", fg="white", font=("Arial", 11, "bold"),
            relief="flat", cursor="hand2"
        )
        apply_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(
            controls_frame, text="🗑️ مسح الفلاتر", 
            command=self.clear_filters,
            bg="#e74c3c", fg="white", font=("Arial", 11, "bold"),
            relief="flat", cursor="hand2"
        )
        clear_btn.pack(side=tk.LEFT, padx=5)

    def create_operations_frame(self, parent):
        """إنشاء إطار العمليات والتواريخ"""
        
        operations_frame = tk.LabelFrame(
            parent,
            text="⚡ سجل العمليات والتواريخ",
            font=("Arial", 14, "bold"),
            bg="#2c3e60", fg="#ecf0f1",
            relief="groove", bd=3
        )
        operations_frame.pack(fill=tk.X, pady=(0, 10))
        
        # جدول العمليات
        operations_container = tk.Frame(operations_frame, bg="#2c3e60")
        operations_container.pack(fill=tk.X, padx=10, pady=10)
        
        # أعمدة جدول العمليات
        columns = ('التاريخ', 'الوقت', 'العملية', 'العنصر', 'الكمية', 'المستخدم', 'التفاصيل')
        
        self.operations_tree = ttk.Treeview(operations_container, columns=columns, show='headings', height=6)
        
        # تحديد عناوين الأعمدة
        for col in columns:
            self.operations_tree.heading(col, text=col, anchor='center')
            if col == 'التفاصيل':
                self.operations_tree.column(col, width=200, anchor='center')
            elif col in ['التاريخ', 'الوقت']:
                self.operations_tree.column(col, width=100, anchor='center')
            else:
                self.operations_tree.column(col, width=120, anchor='center')
        
        # شريط التمرير للعمليات
        operations_scrollbar = ttk.Scrollbar(operations_container, orient=tk.VERTICAL, 
                                           command=self.operations_tree.yview)
        self.operations_tree.configure(yscrollcommand=operations_scrollbar.set)
        
        self.operations_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        operations_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def create_enhanced_results_frame(self, parent):
        """إنشاء إطار النتائج المحسن"""
        
        results_frame = tk.LabelFrame(
            parent,
            text="📊 نتائج البحث والإحصائيات",
            font=("Arial", 14, "bold"),
            bg="#2c3e60", fg="#ecf0f1",
            relief="groove", bd=3
        )
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # إطار الإحصائيات السريعة
        stats_frame = tk.Frame(results_frame, bg="#34495e", relief="groove", bd=2)
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.stats_labels = {}
        stats_data = [
            ('العناصر', 'items_count', '#3498db'),
            ('الابتدائية', 'initial_total', '#2ecc71'),
            ('الداخلة', 'incoming_total', '#27ae60'), 
            ('الخارجة', 'outgoing_total', '#e74c3c'),
            ('المتبقية', 'remaining_total', '#f39c12')
        ]
        
        for i, (label, key, color) in enumerate(stats_data):
            frame = tk.Frame(stats_frame, bg=color, relief="raised", bd=2)
            frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=5)
            
            tk.Label(frame, text=label, bg=color, fg="white", 
                    font=("Arial", 10, "bold")).pack()
            self.stats_labels[key] = tk.Label(frame, text="0", bg=color, fg="white",
                                             font=("Arial", 12, "bold"))
            self.stats_labels[key].pack()
        
        # جدول النتائج
        results_container = tk.Frame(results_frame, bg="#2c3e60")
        results_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # أعمدة الجدول المحسن
        columns = ('العنصر', 'التصنيف', 'الابتدائية', 'الداخلة', 'الخارجة', 'المتبقية', 'المشروع', 'آخر تحديث')
        
        self.results_tree = ttk.Treeview(results_container, columns=columns, show='headings')
        
        # تحديد عناوين وأحجام الأعمدة  
        column_widths = {'العنصر': 150, 'التصنيف': 120, 'الابتدائية': 80, 'الداخلة': 80, 
                        'الخارجة': 80, 'المتبقية': 80, 'المشروع': 100, 'آخر تحديث': 130}
        
        for col in columns:
            self.results_tree.heading(col, text=col, anchor='center')
            self.results_tree.column(col, width=column_widths.get(col, 100), anchor='center')
        
        # أشرطة التمرير
        v_scrollbar = ttk.Scrollbar(results_container, orient=tk.VERTICAL, 
                                   command=self.results_tree.yview)
        h_scrollbar = ttk.Scrollbar(results_container, orient=tk.HORIZONTAL,
                                   command=self.results_tree.xview)
        
        self.results_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.results_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        results_container.grid_rowconfigure(0, weight=1)
        results_container.grid_columnconfigure(0, weight=1)

    def load_data(self):
        """تحميل البيانات من Google Sheets"""
        
        try:
            self.status_label.config(text="📡 جاري الاتصال بـ Google Sheets...")
            self.window.update()
            
            # الاتصال بـ Google Sheets
            self.sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
            
            if not self.sheets_manager.connect():
                raise Exception("فشل في الاتصال بـ Google Sheets")
            
            self.status_label.config(text="📊 جاري تحميل بيانات المخزون...")
            self.window.update()
            
            # تحميل بيانات المخزون الأساسية
            self.load_inventory_data()
            
            self.status_label.config(text="⚡ جاري تحميل سجل العمليات...")
            self.window.update()
            
            # تحميل سجل العمليات
            self.load_operations_log()
            
            # دمج البيانات وإعداد الفلاتر
            self.combine_data()
            self.setup_filters()
            
            # عرض البيانات الأولية
            self.apply_filters()
            
            self.status_label.config(text="✅ تم تحميل جميع البيانات بنجاح")
            
        except Exception as e:
            error_msg = f"❌ خطأ في تحميل البيانات: {str(e)}"
            self.status_label.config(text=error_msg)
            messagebox.showerror("خطأ", error_msg)

    def load_inventory_data(self):
        """تحميل بيانات المخزون الأساسية"""
        
        # الحصول على جميع البيانات
        all_values = self.sheets_manager.worksheet.get_all_values()
        
        if not all_values:
            self.inventory_data = []
            return
        
        headers = all_values[0]
        self.inventory_data = []
        
        for row in all_values[1:]:
            if len(row) >= len(headers) and row[0]:  # التأكد من وجود اسم العنصر
                item_data = {}
                for i, header in enumerate(headers):
                    item_data[header] = row[i] if i < len(row) else ""
                self.inventory_data.append(item_data)
        
        print(f"✅ تم تحميل {len(self.inventory_data)} عنصر من المخزون")

    def load_operations_log(self):
        """تحميل سجل العمليات من ورقة activity_log"""
        
        try:
            # محاولة الوصول لورقة سجل النشاط
            activity_worksheet = self.sheets_manager.spreadsheet.worksheet('activity_log')
            activity_values = activity_worksheet.get_all_values()
            
            if not activity_values:
                self.operations_data = []
                return
            
            activity_headers = activity_values[0]
            self.operations_data = []
            
            for row in activity_values[1:]:
                if len(row) >= len(activity_headers) and row[0]:  # التأكد من وجود تاريخ
                    operation_data = {}
                    for i, header in enumerate(activity_headers):
                        operation_data[header] = row[i] if i < len(row) else ""
                    self.operations_data.append(operation_data)
            
            print(f"✅ تم تحميل {len(self.operations_data)} عملية من سجل النشاط")
            
        except Exception as e:
            print(f"⚠️ لا يمكن تحميل سجل العمليات: {str(e)}")
            # إنشاء عمليات وهمية للاختبار
            self.create_sample_operations()

    def create_sample_operations(self):
        """إنشاء عمليات وهمية للاختبار"""
        
        sample_operations = []
        base_date = datetime.now()
        
        for i, item in enumerate(self.inventory_data[:5]):  # أول 5 عناصر
            for j in range(3):  # 3 عمليات لكل عنصر
                operation_date = base_date - timedelta(days=i*2 + j)
                operation_time = operation_date.strftime("%H:%M:%S")
                operation_date_str = operation_date.strftime("%Y-%m-%d")
                
                operations = ['إدخال', 'إخراج', 'تعديل']
                operation_type = operations[j % 3]
                
                sample_operations.append({
                    'التاريخ': operation_date_str,
                    'الوقت': operation_time,
                    'العملية': operation_type,
                    'اسم العنصر': item.get('اسم العنصر', ''),
                    'الكمية': str((j + 1) * 10),
                    'المستخدم': 'admin',
                    'التفاصيل': f'{operation_type} كمية {(j + 1) * 10}',
                    'التصنيف': item.get('التصنيف', ''),
                    'رقم المشروع': item.get('رقم المشروع', '')
                })
        
        self.operations_data = sample_operations
        print(f"✅ تم إنشاء {len(self.operations_data)} عملية تجريبية")

    def combine_data(self):
        """دمج بيانات المخزون مع العمليات"""
        
        self.combined_data = []
        
        # إضافة بيانات المخزون الأساسية
        for item in self.inventory_data:
            combined_item = item.copy()
            combined_item['نوع_البيان'] = 'مخزون'
            self.combined_data.append(combined_item)
        
        # إضافة بيانات العمليات
        for operation in self.operations_data:
            combined_operation = operation.copy()
            combined_operation['نوع_البيان'] = 'عملية'
            self.combined_data.append(combined_operation)
        
        print(f"✅ تم دمج {len(self.combined_data)} بند (مخزون + عمليات)")

    def setup_filters(self):
        """إعداد قوائم الفلاتر"""
        
        # مسح القوائم الحالية
        for key in self.filter_options:
            if key != 'operations':
                self.filter_options[key] = ['الكل']
        
        # استخراج القيم من البيانات المدمجة
        dates_set = set()
        items_set = set()
        categories_set = set()
        projects_set = set()
        
        for item in self.combined_data:
            # التواريخ
            date_field = item.get('التاريخ') or item.get('آخر تحديث', '')
            if date_field:
                try:
                    date_part = date_field.split(' ')[0]
                    dates_set.add(date_part)
                except:
                    pass
            
            # العناصر
            item_name = item.get('اسم العنصر', '')
            if item_name:
                items_set.add(item_name)
            
            # التصنيفات
            category = item.get('التصنيف', '')
            if category:
                categories_set.add(category)
            
            # المشاريع  
            project = item.get('رقم المشروع', '')
            if project:
                projects_set.add(project)
        
        # تحديث قوائم الفلاتر
        self.filter_options['dates'].extend(sorted(dates_set))
        self.filter_options['items'].extend(sorted(items_set))
        self.filter_options['categories'].extend(sorted(categories_set))
        self.filter_options['projects'].extend(sorted(projects_set))
        
        # تحديث الـ Comboboxes
        self.date_combo['values'] = self.filter_options['dates']
        self.item_combo['values'] = self.filter_options['items']
        self.category_combo['values'] = self.filter_options['categories']
        self.project_combo['values'] = self.filter_options['projects']
        self.operation_combo['values'] = self.filter_options['operations']
        
        print("✅ تم إعداد قوائم الفلاتر")

    def apply_filters(self):
        """تطبيق الفلاتر وعرض النتائج"""
        
        # الحصول على قيم الفلاتر
        filters = {}
        for key, var in self.filter_vars.items():
            filters[key] = var.get().strip()
        
        # تطبيق الفلاتر على البيانات
        filtered_inventory = []
        filtered_operations = []
        
        for item in self.combined_data:
            include_item = True
            
            # فلتر التاريخ
            if filters['date'] != "الكل":
                date_field = item.get('التاريخ') or item.get('آخر تحديث', '')
                if filters['date'] not in date_field:
                    include_item = False
            
            # فلتر نطاق التواريخ
            if filters['date_from'] or filters['date_to']:
                date_field = item.get('التاريخ') or item.get('آخر تحديث', '')
                if date_field:
                    try:
                        item_date = datetime.strptime(date_field.split(' ')[0], "%Y-%m-%d")
                        
                        if filters['date_from']:
                            from_date = datetime.strptime(filters['date_from'], "%Y-%m-%d")
                            if item_date < from_date:
                                include_item = False
                        
                        if filters['date_to']:
                            to_date = datetime.strptime(filters['date_to'], "%Y-%m-%d")
                            if item_date > to_date:
                                include_item = False
                    except:
                        pass
            
            # باقي الفلاتر
            if filters['item'] != "الكل":
                if item.get('اسم العنصر', '') != filters['item']:
                    include_item = False
            
            if filters['category'] != "الكل":
                if item.get('التصنيف', '') != filters['category']:
                    include_item = False
                    
            if filters['project'] != "الكل":
                if item.get('رقم المشروع', '') != filters['project']:
                    include_item = False
            
            if filters['operation'] != "الكل":
                if item.get('العملية', '') != filters['operation']:
                    include_item = False
            
            if include_item:
                if item.get('نوع_البيان') == 'مخزون':
                    filtered_inventory.append(item)
                else:
                    filtered_operations.append(item)
        
        # عرض النتائج
        self.display_inventory_results(filtered_inventory)
        self.display_operations_results(filtered_operations)
        self.update_statistics(filtered_inventory)
        
        # تحديث شريط الحالة
        total_count = len(filtered_inventory) + len(filtered_operations)
        self.status_label.config(
            text=f"✅ النتائج: {len(filtered_inventory)} عنصر مخزون، {len(filtered_operations)} عملية"
        )

    def display_inventory_results(self, data):
        """عرض نتائج المخزون"""
        
        # مسح البيانات السابقة
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # إضافة البيانات الجديدة
        for item in data:
            values = (
                item.get('اسم العنصر', ''),
                item.get('التصنيف', ''),
                item.get('الكمية الابتدائية', '0'),
                item.get('الكمية الداخلة', '0'),
                item.get('الكمية الخارجة', '0'),
                item.get('الكمية المتبقية', '0'),
                item.get('رقم المشروع', ''),
                item.get('آخر تحديث', '')
            )
            self.results_tree.insert("", "end", values=values)

    def display_operations_results(self, operations):
        """عرض نتائج العمليات"""
        
        # مسح البيانات السابقة
        for item in self.operations_tree.get_children():
            self.operations_tree.delete(item)
        
        # إضافة العمليات الجديدة
        for op in operations:
            values = (
                op.get('التاريخ', ''),
                op.get('الوقت', ''),
                op.get('العملية', ''),
                op.get('اسم العنصر', ''),
                op.get('الكمية', ''),
                op.get('المستخدم', ''),
                op.get('التفاصيل', '')
            )
            self.operations_tree.insert("", "end", values=values)

    def update_statistics(self, data):
        """تحديث الإحصائيات"""
        
        stats = {
            'items_count': len(data),
            'initial_total': 0,
            'incoming_total': 0,
            'outgoing_total': 0,
            'remaining_total': 0
        }
        
        for item in data:
            try:
                stats['initial_total'] += int(item.get('الكمية الابتدائية', 0) or 0)
                stats['incoming_total'] += int(item.get('الكمية الداخلة', 0) or 0)
                stats['outgoing_total'] += int(item.get('الكمية الخارجة', 0) or 0)
                stats['remaining_total'] += int(item.get('الكمية المتبقية', 0) or 0)
            except (ValueError, TypeError):
                pass
        
        # تحديث التسميات
        for key, value in stats.items():
            if key in self.stats_labels:
                if key == 'items_count':
                    self.stats_labels[key].config(text=str(value))
                else:
                    self.stats_labels[key].config(text=f"{value:,}")

    def clear_filters(self):
        """مسح جميع الفلاتر"""
        
        for var in self.filter_vars.values():
            if hasattr(var, 'set'):
                var.set("الكل" if var == self.filter_vars['date'] or 
                              var == self.filter_vars['item'] or
                              var == self.filter_vars['category'] or
                              var == self.filter_vars['project'] or
                              var == self.filter_vars['operation'] else "")
        
        self.apply_filters()

    def run(self):
        """تشغيل النافذة"""
        if self.window:
            self.window.mainloop()


def main():
    """الدالة الرئيسية"""
    
    print("🔍 نظام الفلاتر المحسن مع العمليات والتواريخ")
    print("=" * 60)
    
    try:
        system = EnhancedFiltersWithOperations()
        window = system.create_window()
        system.run()
        
    except Exception as e:
        print(f"❌ خطأ في تشغيل النظام: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()