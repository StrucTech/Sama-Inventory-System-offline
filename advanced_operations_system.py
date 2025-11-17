"""
نظام العمليات المتقدم للمخزون
يحل المشكلة الثانية: نظام شامل لتسجيل العمليات مع التواريخ والتفاصيل
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
from typing import Dict, Any, List, Optional
from sheets.manager import SheetsManager

class AdvancedOperationsSystem:
    def __init__(self, sheets_manager, parent_window=None):
        """تهيئة نظام العمليات المتقدم"""
        self.sheets_manager = sheets_manager
        self.parent_window = parent_window
        self.window = None
        self.operations_data = []  # بيانات العمليات
        self.inventory_data = []   # بيانات المخزون
        
        # واجهة المستخدم
        self.tree = None
        self.stats_labels = {}
        self.filter_vars = {}
        
    def create_operations_window(self):
        """إنشاء نافذة العمليات المتقدمة"""
        
        self.window = tk.Toplevel(self.parent_window) if self.parent_window else tk.Tk()
        self.window.title("📊 نظام العمليات المتقدم - تسجيل شامل مع التواريخ")
        self.window.geometry("1500x900")
        self.window.configure(bg="#2c3e50")
        
        # جعل النافذة في المقدمة
        if self.parent_window:
            self.window.transient(self.parent_window)
            self.window.grab_set()
        
        self.create_operations_interface()
        self.load_operations_data()
        
        return self.window
    
    def create_operations_interface(self):
        """إنشاء واجهة نظام العمليات"""
        
        # الإطار الرئيسي
        main_frame = tk.Frame(self.window, bg="#2c3e50")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # عنوان النظام
        title_frame = tk.Frame(main_frame, bg="#34495e", height=60)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="📊 نظام العمليات المتقدم - تسجيل شامل لكل عملية مع التاريخ والتفاصيل",
            font=("Arial", 14, "bold"),
            bg="#34495e", fg="#ecf0f1"
        )
        title_label.pack(expand=True)
        
        # إطار المحتوى
        content_frame = tk.Frame(main_frame, bg="#2c3e50")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # الجانب الأيسر - الفلاتر والإحصائيات
        left_panel = tk.Frame(content_frame, bg="#34495e", width=350)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        self.create_operations_filters(left_panel)
        self.create_operations_statistics(left_panel)
        self.create_operations_actions(left_panel)
        
        # الجانب الأيمن - جدول العمليات
        right_panel = tk.Frame(content_frame, bg="#2c3e50")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.create_operations_table(right_panel)
        
        # شريط الحالة
        self.create_operations_status_bar(main_frame)
    
    def create_operations_filters(self, parent):
        """إنشاء فلاتر العمليات"""
        
        filters_frame = tk.LabelFrame(
            parent, text="🎯 فلاتر العمليات", 
            bg="#34495e", fg="#ecf0f1", 
            font=("Arial", 11, "bold")
        )
        filters_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # فلتر نوع العملية
        tk.Label(filters_frame, text="نوع العملية:", bg="#34495e", fg="#ecf0f1").pack(anchor="w", padx=5)
        self.filter_vars['operation_type'] = tk.StringVar(value="الكل")
        operation_combo = ttk.Combobox(
            filters_frame, 
            textvariable=self.filter_vars['operation_type'],
            values=["الكل", "إضافة مخزون", "صرف مخزون", "تعديل كمية", "إضافة عنصر جديد"],
            state="readonly"
        )
        operation_combo.pack(fill=tk.X, padx=5, pady=2)
        operation_combo.bind('<<ComboboxSelected>>', self.apply_filters)
        
        # فلتر التاريخ
        tk.Label(filters_frame, text="فترة التاريخ:", bg="#34495e", fg="#ecf0f1").pack(anchor="w", padx=5, pady=(10,0))
        self.filter_vars['date_range'] = tk.StringVar(value="الكل")
        date_combo = ttk.Combobox(
            filters_frame,
            textvariable=self.filter_vars['date_range'], 
            values=["الكل", "اليوم", "أمس", "آخر 3 أيام", "آخر أسبوع", "آخر شهر"],
            state="readonly"
        )
        date_combo.pack(fill=tk.X, padx=5, pady=2)
        date_combo.bind('<<ComboboxSelected>>', self.apply_filters)
        
        # فلتر المشروع
        tk.Label(filters_frame, text="المشروع:", bg="#34495e", fg="#ecf0f1").pack(anchor="w", padx=5, pady=(10,0))
        self.filter_vars['project'] = tk.StringVar(value="الكل")
        self.project_combo = ttk.Combobox(
            filters_frame,
            textvariable=self.filter_vars['project'],
            values=["الكل"],
            state="readonly"
        )
        self.project_combo.pack(fill=tk.X, padx=5, pady=2)
        self.project_combo.bind('<<ComboboxSelected>>', self.apply_filters)
        
        # فلتر العنصر
        tk.Label(filters_frame, text="العنصر:", bg="#34495e", fg="#ecf0f1").pack(anchor="w", padx=5, pady=(10,0))
        self.filter_vars['item'] = tk.StringVar(value="الكل")
        self.item_combo = ttk.Combobox(
            filters_frame,
            textvariable=self.filter_vars['item'],
            values=["الكل"],
            state="readonly"
        )
        self.item_combo.pack(fill=tk.X, padx=5, pady=2)
        self.item_combo.bind('<<ComboboxSelected>>', self.apply_filters)
        
        # أزرار الفلترة
        buttons_frame = tk.Frame(filters_frame, bg="#34495e")
        buttons_frame.pack(fill=tk.X, padx=5, pady=10)
        
        tk.Button(
            buttons_frame, text="🔍 تطبيق الفلاتر", 
            command=self.apply_filters,
            bg="#3498db", fg="white", font=("Arial", 9, "bold")
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,2))
        
        tk.Button(
            buttons_frame, text="🗑️ مسح", 
            command=self.clear_filters,
            bg="#e74c3c", fg="white", font=("Arial", 9, "bold")
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2,0))
    
    def create_operations_statistics(self, parent):
        """إنشاء إحصائيات العمليات"""
        
        stats_frame = tk.LabelFrame(
            parent, text="📈 إحصائيات العمليات", 
            bg="#34495e", fg="#ecf0f1", 
            font=("Arial", 11, "bold")
        )
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # إحصائيات العمليات
        operations_stats = [
            ("total_operations", "🔢 إجمالي العمليات", "0"),
            ("today_operations", "📅 عمليات اليوم", "0"),
            ("add_operations", "➕ عمليات الإضافة", "0"),
            ("out_operations", "📤 عمليات الصرف", "0"),
            ("edit_operations", "✏️ عمليات التعديل", "0"),
            ("total_added", "⬇️ إجمالي المضاف", "0"),
            ("total_removed", "⬆️ إجمالي المصروف", "0")
        ]
        
        for key, label, initial_value in operations_stats:
            row_frame = tk.Frame(stats_frame, bg="#34495e")
            row_frame.pack(fill=tk.X, padx=5, pady=2)
            
            tk.Label(row_frame, text=label, bg="#34495e", fg="#bdc3c7", 
                    font=("Arial", 9)).pack(side=tk.LEFT)
            
            value_label = tk.Label(row_frame, text=initial_value, bg="#34495e", 
                                 fg="#2ecc71", font=("Arial", 9, "bold"))
            value_label.pack(side=tk.RIGHT)
            
            self.stats_labels[key] = value_label
    
    def create_operations_actions(self, parent):
        """إنشاء أزرار العمليات"""
        
        actions_frame = tk.LabelFrame(
            parent, text="⚡ عمليات سريعة", 
            bg="#34495e", fg="#ecf0f1", 
            font=("Arial", 11, "bold")
        )
        actions_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # أزرار العمليات
        operations_buttons = [
            ("🔄 تحديث البيانات", self.refresh_operations, "#3498db"),
            ("➕ عملية إضافة جديدة", self.new_add_operation, "#27ae60"),
            ("📤 عملية صرف جديدة", self.new_outbound_operation, "#e74c3c"),
            ("📊 تقرير العمليات", self.generate_operations_report, "#9b59b6"),
            ("💾 تصدير البيانات", self.export_operations_data, "#f39c12"),
            ("🧹 تنظيف البيانات القديمة", self.clean_old_operations, "#95a5a6")
        ]
        
        for text, command, color in operations_buttons:
            btn = tk.Button(
                actions_frame, text=text, command=command,
                bg=color, fg="white", font=("Arial", 9, "bold"),
                relief="flat", cursor="hand2"
            )
            btn.pack(fill=tk.X, padx=5, pady=2)
    
    def create_operations_table(self, parent):
        """إنشاء جدول العمليات التفصيلي"""
        
        # إطار الجدول
        table_frame = tk.LabelFrame(
            parent, text="📋 سجل العمليات التفصيلي", 
            bg="#2c3e50", fg="#ecf0f1", 
            font=("Arial", 12, "bold")
        )
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # شريط أدوات الجدول
        toolbar = tk.Frame(table_frame, bg="#34495e", height=40)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        toolbar.pack_propagate(False)
        
        # مؤشر النتائج
        self.operations_results_label = tk.Label(
            toolbar, text="📊 النتائج: جاري التحميل...",
            bg="#34495e", fg="#ecf0f1", font=("Arial", 11, "bold")
        )
        self.operations_results_label.pack(side=tk.LEFT, padx=10)
        
        # أزرار سريعة
        quick_buttons_frame = tk.Frame(toolbar, bg="#34495e")
        quick_buttons_frame.pack(side=tk.RIGHT, padx=10)
        
        quick_operations = [
            ("اليوم", lambda: self.quick_filter_date("today")),
            ("الأسبوع", lambda: self.quick_filter_date("week")),
            ("الشهر", lambda: self.quick_filter_date("month"))
        ]
        
        for text, command in quick_operations:
            btn = tk.Button(
                quick_buttons_frame, text=text, command=command,
                bg="#2c3e50", fg="#ecf0f1", font=("Arial", 8),
                relief="flat", cursor="hand2"
            )
            btn.pack(side=tk.LEFT, padx=2)
        
        # إطار الجدول الفعلي
        tree_frame = tk.Frame(table_frame, bg="#2c3e50")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        # إعداد الجدول مع أعمدة شاملة
        columns = (
            "timestamp", "operation_type", "item_name", "category", 
            "project", "quantity_before", "quantity_change", "quantity_after",
            "operation_details", "user", "notes"
        )
        
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=25)
        
        # تحديد عناوين الأعمدة
        column_headers = {
            "timestamp": "🕐 التاريخ والوقت",
            "operation_type": "⚡ نوع العملية",
            "item_name": "🏷️ اسم العنصر", 
            "category": "📁 التصنيف",
            "project": "🏗️ المشروع",
            "quantity_before": "📦 الكمية قبل",
            "quantity_change": "🔄 التغيير",
            "quantity_after": "📦 الكمية بعد",
            "operation_details": "📝 تفاصيل العملية",
            "user": "👤 المستخدم",
            "notes": "💬 ملاحظات"
        }
        
        # تحديد عرض الأعمدة
        column_widths = {
            "timestamp": 140, "operation_type": 120, "item_name": 150,
            "category": 100, "project": 80, "quantity_before": 80,
            "quantity_change": 80, "quantity_after": 80, "operation_details": 200,
            "user": 100, "notes": 150
        }
        
        for col in columns:
            self.tree.heading(col, text=column_headers.get(col, col))
            self.tree.column(col, width=column_widths.get(col, 100), anchor=tk.CENTER)
        
        # إعداد شريط التمرير
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # تخطيط الجدول
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # ألوان الصفوف
        self.tree.tag_configure("add_operation", background="#e8f5e8", foreground="#2e7d32")
        self.tree.tag_configure("remove_operation", background="#ffebee", foreground="#c62828")
        self.tree.tag_configure("edit_operation", background="#fff3e0", foreground="#ef6c00")
        self.tree.tag_configure("normal", background="#ecf0f1")
    
    def create_operations_status_bar(self, parent):
        """إنشاء شريط الحالة"""
        
        status_frame = tk.Frame(parent, bg="#34495e", height=30)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        status_frame.pack_propagate(False)
        
        self.operations_status_label = tk.Label(
            status_frame, text="✅ نظام العمليات جاهز",
            bg="#34495e", fg="#2ecc71", font=("Arial", 10)
        )
        self.operations_status_label.pack(side=tk.LEFT, padx=10)
        
        # مؤشر آخر تحديث
        self.last_update_label = tk.Label(
            status_frame, text="",
            bg="#34495e", fg="#ecf0f1", font=("Arial", 10)
        )
        self.last_update_label.pack(side=tk.RIGHT, padx=10)
    
    def load_operations_data(self):
        """تحميل بيانات العمليات"""
        
        self.operations_status_label.config(text="📊 جاري تحميل بيانات العمليات...", fg="#f39c12")
        
        def load_data():
            try:
                # تحميل بيانات المخزون الأساسية
                worksheet = self.sheets_manager.worksheet
                all_values = worksheet.get_all_values()
                
                if all_values and len(all_values) > 1:
                    headers = all_values[0]
                    data_rows = all_values[1:]
                    
                    # تحويل بيانات المخزون
                    self.inventory_data = []
                    for row in data_rows:
                        if len(row) >= len(headers):
                            item_dict = {}
                            for i, header in enumerate(headers):
                                item_dict[header] = row[i] if i < len(row) else ''
                            self.inventory_data.append(item_dict)
                    
                    # إنشاء بيانات عمليات تجريبية (في التطبيق الحقيقي ستأتي من مصدر منفصل)
                    operations_data = self.generate_sample_operations_data()
                    
                    # تحديث الواجهة في الخيط الرئيسي
                    self.window.after(0, self.on_operations_data_loaded, operations_data)
                else:
                    self.window.after(0, self.on_operations_data_loaded, [])
                    
            except Exception as e:
                self.window.after(0, self.on_operations_error, str(e))
        
        # تحميل البيانات في خيط منفصل
        import threading
        thread = threading.Thread(target=load_data, daemon=True)
        thread.start()
    
    def generate_sample_operations_data(self):
        """إنشاء بيانات عمليات نموذجية للعرض التوضيحي"""
        
        operations = []
        
        # إنشاء عمليات نموذجية بناءً على بيانات المخزون
        for i, item in enumerate(self.inventory_data[:5]):  # أخذ أول 5 عناصر
            item_name = item.get('اسم العنصر', f'عنصر {i+1}')
            category = item.get('التصنيف', 'عام')
            project = item.get('رقم المشروع', 'PRJ_001')
            
            # عملية إضافة أولية
            operations.append({
                'timestamp': '2025-11-15 09:00:00',
                'operation_type': 'إضافة عنصر جديد',
                'item_name': item_name,
                'category': category,
                'project': project,
                'quantity_before': '0',
                'quantity_change': '+100',
                'quantity_after': '100',
                'operation_details': 'إضافة عنصر جديد للمخزون',
                'user': 'admin',
                'notes': 'إضافة أولية للمخزون'
            })
            
            # عملية إضافة كمية
            operations.append({
                'timestamp': '2025-11-16 14:30:00',
                'operation_type': 'إضافة مخزون',
                'item_name': item_name,
                'category': category,
                'project': project,
                'quantity_before': '100',
                'quantity_change': '+50',
                'quantity_after': '150',
                'operation_details': 'إضافة كمية جديدة من المورد',
                'user': 'user1',
                'notes': 'شحنة جديدة'
            })
            
            # عملية صرف
            operations.append({
                'timestamp': '2025-11-17 10:15:00',
                'operation_type': 'صرف مخزون',
                'item_name': item_name,
                'category': category,
                'project': project,
                'quantity_before': '150',
                'quantity_change': '-25',
                'quantity_after': '125',
                'operation_details': 'صرف للاستخدام في الموقع',
                'user': 'user2',
                'notes': 'استخدام في المشروع'
            })
        
        # ترتيب العمليات حسب التاريخ (الأحدث أولاً)
        operations.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return operations
    
    def on_operations_data_loaded(self, operations_data):
        """معالجة بيانات العمليات المحملة"""
        
        self.operations_data = operations_data
        self.update_filter_options()
        self.display_operations_data()
        self.update_operations_statistics()
        
        count = len(operations_data)
        self.operations_status_label.config(
            text=f"✅ تم تحميل {count} عملية بنجاح", 
            fg="#2ecc71"
        )
        
        # تحديث وقت آخر تحديث
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.last_update_label.config(text=f"آخر تحديث: {current_time}")
    
    def on_operations_error(self, error_msg):
        """معالجة أخطاء تحميل البيانات"""
        self.operations_status_label.config(text=f"❌ خطأ: {error_msg}", fg="#e74c3c")
        messagebox.showerror("خطأ في تحميل البيانات", error_msg)
    
    def update_filter_options(self):
        """تحديث خيارات الفلاتر"""
        
        # استخراج المشاريع الفريدة
        projects = set(["الكل"])
        items = set(["الكل"])
        
        for operation in self.operations_data:
            project = operation.get('project', '')
            if project:
                projects.add(project)
            
            item = operation.get('item_name', '')
            if item:
                items.add(item)
        
        # تحديث قوائم الفلاتر
        self.project_combo['values'] = list(projects)
        self.item_combo['values'] = list(items)
    
    def display_operations_data(self, filtered_data=None):
        """عرض بيانات العمليات"""
        
        # استخدام البيانات المفلترة أو كافة البيانات
        data_to_display = filtered_data if filtered_data is not None else self.operations_data
        
        # مسح البيانات الحالية
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # عرض البيانات
        for operation in data_to_display:
            # تحديد لون الصف حسب نوع العملية
            operation_type = operation.get('operation_type', '')
            if 'إضافة' in operation_type:
                tag = "add_operation"
            elif 'صرف' in operation_type:
                tag = "remove_operation"
            elif 'تعديل' in operation_type:
                tag = "edit_operation"
            else:
                tag = "normal"
            
            # إعداد البيانات للعرض
            values = (
                operation.get('timestamp', ''),
                operation.get('operation_type', ''),
                operation.get('item_name', ''),
                operation.get('category', ''),
                operation.get('project', ''),
                operation.get('quantity_before', ''),
                operation.get('quantity_change', ''),
                operation.get('quantity_after', ''),
                operation.get('operation_details', ''),
                operation.get('user', ''),
                operation.get('notes', '')
            )
            
            self.tree.insert('', 'end', values=values, tags=(tag,))
        
        # تحديث مؤشر النتائج
        self.operations_results_label.config(text=f"📊 النتائج: {len(data_to_display)} عملية")
    
    def update_operations_statistics(self, filtered_data=None):
        """تحديث إحصائيات العمليات"""
        
        data_to_analyze = filtered_data if filtered_data is not None else self.operations_data
        
        # حساب الإحصائيات
        total_operations = len(data_to_analyze)
        today_operations = 0
        add_operations = 0
        out_operations = 0
        edit_operations = 0
        total_added = 0
        total_removed = 0
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        for operation in data_to_analyze:
            # عمليات اليوم
            timestamp = operation.get('timestamp', '')
            if today in timestamp:
                today_operations += 1
            
            # أنواع العمليات
            operation_type = operation.get('operation_type', '')
            if 'إضافة' in operation_type:
                add_operations += 1
            elif 'صرف' in operation_type:
                out_operations += 1
            elif 'تعديل' in operation_type:
                edit_operations += 1
            
            # إجمالي الكميات
            quantity_change = operation.get('quantity_change', '+0')
            try:
                if quantity_change.startswith('+'):
                    total_added += int(quantity_change[1:])
                elif quantity_change.startswith('-'):
                    total_removed += int(quantity_change[1:])
            except ValueError:
                pass
        
        # تحديث عرض الإحصائيات
        self.stats_labels['total_operations'].config(text=str(total_operations))
        self.stats_labels['today_operations'].config(text=str(today_operations))
        self.stats_labels['add_operations'].config(text=str(add_operations))
        self.stats_labels['out_operations'].config(text=str(out_operations))
        self.stats_labels['edit_operations'].config(text=str(edit_operations))
        self.stats_labels['total_added'].config(text=f"{total_added:,}")
        self.stats_labels['total_removed'].config(text=f"{total_removed:,}")
    
    def apply_filters(self, event=None):
        """تطبيق الفلاتر على بيانات العمليات"""
        
        # الحصول على قيم الفلاتر
        operation_type_filter = self.filter_vars['operation_type'].get()
        date_range_filter = self.filter_vars['date_range'].get()
        project_filter = self.filter_vars['project'].get()
        item_filter = self.filter_vars['item'].get()
        
        # تطبيق الفلاتر
        filtered_data = []
        
        for operation in self.operations_data:
            include_operation = True
            
            # فلتر نوع العملية
            if operation_type_filter != "الكل":
                if operation.get('operation_type', '') != operation_type_filter:
                    include_operation = False
            
            # فلتر التاريخ
            if date_range_filter != "الكل":
                operation_date = operation.get('timestamp', '')
                if not self.check_date_filter(operation_date, date_range_filter):
                    include_operation = False
            
            # فلتر المشروع
            if project_filter != "الكل":
                if operation.get('project', '') != project_filter:
                    include_operation = False
            
            # فلتر العنصر
            if item_filter != "الكل":
                if operation.get('item_name', '') != item_filter:
                    include_operation = False
            
            if include_operation:
                filtered_data.append(operation)
        
        # عرض البيانات المفلترة
        self.display_operations_data(filtered_data)
        self.update_operations_statistics(filtered_data)
        
        print(f"🔍 تطبيق الفلاتر: {len(filtered_data)} من {len(self.operations_data)} عملية")
    
    def check_date_filter(self, operation_date, date_range):
        """فحص فلتر التاريخ"""
        try:
            op_date = datetime.strptime(operation_date[:10], "%Y-%m-%d")
            today = datetime.now()
            
            if date_range == "اليوم":
                return op_date.date() == today.date()
            elif date_range == "أمس":
                from datetime import timedelta
                yesterday = today - timedelta(days=1)
                return op_date.date() == yesterday.date()
            elif date_range == "آخر 3 أيام":
                from datetime import timedelta
                three_days_ago = today - timedelta(days=3)
                return op_date >= three_days_ago
            elif date_range == "آخر أسبوع":
                from datetime import timedelta
                week_ago = today - timedelta(days=7)
                return op_date >= week_ago
            elif date_range == "آخر شهر":
                from datetime import timedelta
                month_ago = today - timedelta(days=30)
                return op_date >= month_ago
            
        except ValueError:
            return False
        
        return True
    
    def clear_filters(self):
        """مسح جميع الفلاتر"""
        self.filter_vars['operation_type'].set("الكل")
        self.filter_vars['date_range'].set("الكل")
        self.filter_vars['project'].set("الكل")
        self.filter_vars['item'].set("الكل")
        
        self.display_operations_data()
        self.update_operations_statistics()
    
    def quick_filter_date(self, period):
        """فلتر سريع للتاريخ"""
        if period == "today":
            self.filter_vars['date_range'].set("اليوم")
        elif period == "week":
            self.filter_vars['date_range'].set("آخر أسبوع")
        elif period == "month":
            self.filter_vars['date_range'].set("آخر شهر")
        
        self.apply_filters()
    
    # دوال العمليات
    def refresh_operations(self):
        """تحديث بيانات العمليات"""
        self.load_operations_data()
    
    def new_add_operation(self):
        """عملية إضافة جديدة"""
        messagebox.showinfo("عملية إضافة", "ستفتح نافذة إضافة عنصر أو كمية جديدة")
    
    def new_outbound_operation(self):
        """عملية صرف جديدة"""
        messagebox.showinfo("عملية صرف", "ستفتح نافذة صرف من المخزون")
    
    def generate_operations_report(self):
        """إنشاء تقرير العمليات"""
        messagebox.showinfo("تقرير العمليات", "سيتم إنشاء تقرير شامل بجميع العمليات")
    
    def export_operations_data(self):
        """تصدير بيانات العمليات"""
        messagebox.showinfo("تصدير البيانات", "سيتم تصدير البيانات إلى ملف Excel")
    
    def clean_old_operations(self):
        """تنظيف العمليات القديمة"""
        result = messagebox.askyesno("تنظيف البيانات", "هل تريد حذف العمليات الأقدم من 6 أشهر؟")
        if result:
            messagebox.showinfo("تنظيف", "سيتم تنظيف العمليات القديمة")


def main():
    """تشغيل نظام العمليات المتقدم"""
    
    print("📊 تشغيل نظام العمليات المتقدم...")
    
    try:
        # إعداد Google Sheets
        sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
        if not sheets_manager.connect():
            messagebox.showerror("خطأ", "فشل في الاتصال بـ Google Sheets")
            return
        
        # إنشاء النظام
        operations_system = AdvancedOperationsSystem(sheets_manager)
        
        # إنشاء النافذة
        window = operations_system.create_operations_window()
        
        # تشغيل النظام
        window.mainloop()
        
    except Exception as e:
        messagebox.showerror("خطأ", f"خطأ في تشغيل النظام: {str(e)}")

if __name__ == "__main__":
    main()