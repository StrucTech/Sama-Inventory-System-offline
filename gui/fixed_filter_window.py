import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.ttk import Treeview
import re
from datetime import datetime

class FixedFilterWindow:
    def __init__(self, sheets_manager, main_window=None):
        """تهيئة نافذة الفلاتر المُصححة"""
        self.sheets_manager = sheets_manager
        self.main_window = main_window
        self.window = None
        self.all_data = []
        self.filtered_data = []
        self.tree = None
        
        # متغيرات الفلاتر
        self.selected_date = tk.StringVar(value="الكل")
        self.selected_item = tk.StringVar(value="الكل") 
        self.selected_category = tk.StringVar(value="الكل")
        self.selected_project = tk.StringVar(value="الكل")
        
        # قوائم البيانات للفلاتر
        self.dates = []
        self.items = []
        self.categories = []
        self.projects = []
        
        # متغيرات الإحصائيات
        self.stats_labels = {}
        
        self.create_window()
        self.load_data()

    def create_window(self):
        """إنشاء النافذة الرئيسية"""
        self.window = tk.Toplevel()
        self.window.title("🔍 البحث والفلترة المُصححة - مع الإحصائيات")
        self.window.geometry("1400x900")
        self.window.configure(bg="#2c3e50")
        self.window.resizable(True, True)
        
        # جعل النافذة في المقدمة
        self.window.transient()
        self.window.grab_set()
        
        # إنشاء الواجهة
        self.create_main_interface()
        
        # تحميل البيانات عند فتح النافذة
        self.window.after(100, self.setup_filters)
    
    def create_main_interface(self):
        """إنشاء الواجهة الرئيسية"""
        
        # الإطار الرئيسي
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # عنوان النافذة
        title_label = tk.Label(
            main_frame,
            text="🔍 نظام البحث والفلترة المُصحح مع الإحصائيات",
            font=("Arial", 16, "bold"),
            bg="#2c3e50", fg="#ecf0f1"
        )
        title_label.pack(pady=(0, 15))
        
        # إطار الفلاتر
        self.create_filters_frame(main_frame)
        
        # إطار الإحصائيات المُحسن
        self.create_enhanced_statistics_frame(main_frame)
        
        # إطار النتائج
        self.create_results_frame(main_frame)
        
        # شريط الحالة
        self.status_label = tk.Label(
            main_frame,
            text="✅ جاهز للاستخدام",
            font=("Arial", 10),
            bg="#2c3e50", fg="#2ecc71"
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))

    def create_filters_frame(self, parent):
        """إنشاء إطار الفلاتر"""
        
        # الإطار الرئيسي للفلاتر
        filters_frame = tk.LabelFrame(
            parent,
            text="🎯 الفلاتر",
            font=("Arial", 12, "bold"),
            bg="#34495e", fg="#ecf0f1",
            relief="groove", bd=2
        )
        filters_frame.pack(fill=tk.X, pady=(0, 10))
        
        # الصف الأول - فلاتر التاريخ والعنصر
        row1 = tk.Frame(filters_frame, bg="#34495e")
        row1.pack(fill=tk.X, padx=10, pady=5)
        
        # فلتر التاريخ
        tk.Label(row1, text="📅 التاريخ:", font=("Arial", 10, "bold"), bg="#34495e", fg="#ecf0f1").grid(row=0, column=0, sticky='w', padx=5)
        self.date_combo = ttk.Combobox(row1, textvariable=self.selected_date, state="readonly", width=15)
        self.date_combo.grid(row=0, column=1, padx=5)
        
        # فلتر العنصر
        tk.Label(row1, text="📦 العنصر:", font=("Arial", 10, "bold"), bg="#34495e", fg="#ecf0f1").grid(row=0, column=2, sticky='w', padx=5)
        self.item_combo = ttk.Combobox(row1, textvariable=self.selected_item, state="readonly", width=20)
        self.item_combo.grid(row=0, column=3, padx=5)
        
        # الصف الثاني - فلاتر التصنيف والمشروع
        row2 = tk.Frame(filters_frame, bg="#34495e")
        row2.pack(fill=tk.X, padx=10, pady=5)
        
        # فلتر التصنيف
        tk.Label(row2, text="🏷️ التصنيف:", font=("Arial", 10, "bold"), bg="#34495e", fg="#ecf0f1").grid(row=0, column=0, sticky='w', padx=5)
        self.category_combo = ttk.Combobox(row2, textvariable=self.selected_category, state="readonly", width=15)
        self.category_combo.grid(row=0, column=1, padx=5)
        
        # فلتر المشروع
        tk.Label(row2, text="🎯 المشروع:", font=("Arial", 10, "bold"), bg="#34495e", fg="#ecf0f1").grid(row=0, column=2, sticky='w', padx=5)
        self.project_combo = ttk.Combobox(row2, textvariable=self.selected_project, state="readonly", width=15)
        self.project_combo.grid(row=0, column=3, padx=5)
        
        # الصف الثالث - فلتر الكمية
        row3 = tk.Frame(filters_frame, bg="#34495e")
        row3.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(row3, text="🔢 الكمية المتبقية:", font=("Arial", 10, "bold"), bg="#34495e", fg="#ecf0f1").grid(row=0, column=0, sticky='w', padx=5)
        self.quantity_op_combo = ttk.Combobox(row3, values=["يساوي", "أكبر من", "أصغر من", "بين"], state="readonly", width=10)
        self.quantity_op_combo.set("يساوي")
        self.quantity_op_combo.grid(row=0, column=1, padx=5)
        
        self.quantity_entry = tk.Entry(row3, width=10)
        self.quantity_entry.grid(row=0, column=2, padx=5)
        
        # أزرار التحكم
        controls_frame = tk.Frame(filters_frame, bg="#34495e")
        controls_frame.pack(fill=tk.X, padx=10, pady=10)
        
        apply_btn = tk.Button(
            controls_frame,
            text="✅ تطبيق الفلاتر",
            command=self.apply_filters,
            bg="#27ae60", fg="white",
            font=("Arial", 11, "bold"),
            relief="flat", cursor="hand2"
        )
        apply_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(
            controls_frame,
            text="🗑️ مسح الفلاتر",
            command=self.clear_filters,
            bg="#e74c3c", fg="white",
            font=("Arial", 11, "bold"),
            relief="flat", cursor="hand2"
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = tk.Button(
            controls_frame,
            text="🔄 تحديث البيانات",
            command=self.refresh_data,
            bg="#3498db", fg="white",
            font=("Arial", 11, "bold"),
            relief="flat", cursor="hand2"
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)

    def create_enhanced_statistics_frame(self, parent):
        """إنشاء إطار الإحصائيات المحسن"""
        
        # إطار الإحصائيات الرئيسي
        main_stats_frame = tk.LabelFrame(
            parent, text="📊 الإحصائيات التفصيلية", 
            bg="#2c3e50", fg="#ecf0f1", 
            font=("Arial", 12, "bold"),
            relief="groove", bd=3
        )
        main_stats_frame.pack(fill='x', pady=(0, 10))
        
        # الصف الأول - الإحصائيات العامة
        general_frame = tk.Frame(main_stats_frame, bg="#34495e", relief="groove", bd=1)
        general_frame.pack(fill='x', padx=5, pady=5)
        
        general_title = tk.Label(general_frame, text="📈 الإحصائيات العامة", 
                                bg="#34495e", fg="#ecf0f1", font=("Arial", 10, "bold"))
        general_title.pack(pady=2)
        
        # صف الإحصائيات العامة
        general_row = tk.Frame(general_frame, bg="#34495e")
        general_row.pack(fill='x', padx=5, pady=2)
        
        self.stats_labels = {}
        
        # الإحصائيات الأساسية
        basic_stats = [
            ('total_items', '🔢 إجمالي العناصر: 0'),
            ('unique_categories', '🏷️ عدد التصنيفات: 0'),
            ('unique_projects', '🎯 عدد المشاريع: 0'),
            ('low_stock_items', '⚠️ مخزون منخفض: 0'),
        ]
        
        for i, (key, text) in enumerate(basic_stats):
            label = tk.Label(general_row, text=text, 
                           bg="#34495e", fg="#ecf0f1", font=("Arial", 9, "bold"))
            label.grid(row=0, column=i, padx=10, sticky='w')
            self.stats_labels[key] = label
        
        # الصف الثاني - إحصائيات الكميات
        quantities_frame = tk.Frame(main_stats_frame, bg="#2c3e50", relief="groove", bd=1)
        quantities_frame.pack(fill='x', padx=5, pady=5)
        
        quantities_title = tk.Label(quantities_frame, text="📦 إحصائيات الكميات", 
                                   bg="#2c3e50", fg="#ecf0f1", font=("Arial", 10, "bold"))
        quantities_title.pack(pady=2)
        
        # صف إحصائيات الكميات
        quantities_row = tk.Frame(quantities_frame, bg="#2c3e50")
        quantities_row.pack(fill='x', padx=5, pady=2)
        
        quantity_stats = [
            ('total_initial', '📥 إجمالي الكمية الابتدائية: 0'),
            ('total_in', '⬇️ إجمالي الواردات: 0'),
            ('total_out', '⬆️ إجمالي الصادرات: 0'),
            ('total_remaining', '📦 إجمالي المتبقي: 0'),
            ('turnover_rate', '🔄 معدل الدوران: 0%')
        ]
        
        for i, (key, text) in enumerate(quantity_stats):
            label = tk.Label(quantities_row, text=text, 
                           bg="#2c3e50", fg="#ecf0f1", font=("Arial", 9, "bold"))
            label.grid(row=0, column=i, padx=8, sticky='w')
            self.stats_labels[key] = label

    def create_results_frame(self, parent):
        """إنشاء إطار النتائج"""
        
        # إطار النتائج
        results_frame = tk.LabelFrame(
            parent,
            text="📋 النتائج التفصيلية",
            font=("Arial", 12, "bold"),
            bg="#34495e", fg="#ecf0f1",
            relief="groove", bd=2
        )
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # شريط أدوات النتائج
        toolbar_frame = tk.Frame(results_frame, bg="#34495e")
        toolbar_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.results_info = tk.Label(
            toolbar_frame,
            text="📊 النتائج: جاري التحميل...",
            font=("Arial", 12, "bold"),
            fg="#2ecc71", bg="#34495e"
        )
        self.results_info.pack(side=tk.LEFT)
        
        # إطار الجدول
        table_frame = tk.Frame(results_frame, bg="#34495e")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # إعداد الجدول مع الأعمدة المصححة
        columns = (
            "العنصر", "التصنيف", "الكمية الابتدائية", 
            "الكمية الداخلة", "الكمية الخارجة", "الكمية المتبقية", 
            "المشروع", "آخر تحديث"
        )
        self.tree = Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # تحديد عناوين وعروض الأعمدة
        column_widths = {
            "العنصر": 180, "التصنيف": 120, "الكمية الابتدائية": 120, 
            "الكمية الداخلة": 100, "الكمية الخارجة": 100, "الكمية المتبقية": 120, 
            "المشروع": 100, "آخر تحديث": 130
        }
        
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_by_column(c))
            self.tree.column(col, width=column_widths.get(col, 100), anchor=tk.CENTER)
        
        # شريط التمرير العمودي
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=v_scrollbar.set)
        
        # شريط التمرير الأفقي
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=h_scrollbar.set)
        
        # ترتيب العناصر
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # ألوان الصفوف
        self.tree.tag_configure("oddrow", background="#ecf0f1")
        self.tree.tag_configure("evenrow", background="#ffffff")
        self.tree.tag_configure("low_stock", background="#ffebee", foreground="#c62828")
        self.tree.tag_configure("medium_stock", background="#fff3e0", foreground="#ef6c00")  
        self.tree.tag_configure("high_stock", background="#e8f5e8", foreground="#2e7d32")

    def load_data(self):
        """تحميل البيانات من Google Sheets"""
        
        try:
            print("📊 بدء تحميل البيانات من Google Sheets...")
            self.status_label.config(text="📊 جاري تحميل البيانات...")
            self.window.update()
            
            # الحصول على البيانات مباشرة من ورقة العمل
            worksheet = self.sheets_manager.worksheet
            all_values = worksheet.get_all_values()
            
            if not all_values:
                print("❌ لا توجد بيانات في الورقة")
                self.status_label.config(text="❌ لا توجد بيانات")
                return
            
            # استخراج العناوين والبيانات
            headers = all_values[0]
            data_rows = all_values[1:]
            
            print(f"📋 العناوين: {headers}")
            print(f"📊 عدد الصفوف: {len(data_rows)}")
            
            # تحويل البيانات إلى قواميس مع التأكد من الأسماء الصحيحة
            self.all_data = []
            for row_num, row in enumerate(data_rows, 1):
                if len(row) >= len(headers):
                    item_dict = {}
                    for i, header in enumerate(headers):
                        item_dict[header] = row[i] if i < len(row) else ''
                    self.all_data.append(item_dict)
                    
                    # طباعة تفاصيل أول 3 عناصر للتحقق
                    if row_num <= 3:
                        print(f"عنصر {row_num}: {item_dict.get('اسم العنصر', 'غير محدد')}")
                        print(f"  ابتدائية: {item_dict.get('الكمية الابتدائية', '0')}")
                        print(f"  داخلة: {item_dict.get('الكمية الداخلة', '0')}")
                        print(f"  خارجة: {item_dict.get('الكمية الخارجة', '0')}")
                        print(f"  متبقية: {item_dict.get('الكمية المتبقية', '0')}")
            
            print(f"✅ تم تحميل {len(self.all_data)} عنصر")
            
            # استخراج القوائم للفلاتر
            self.extract_filter_options()
            
            # عرض جميع البيانات في البداية
            self.filtered_data = self.all_data.copy()
            self.display_data()
            
            self.status_label.config(text="✅ تم تحميل البيانات بنجاح")
            
        except Exception as e:
            print(f"❌ خطأ في تحميل البيانات: {str(e)}")
            self.status_label.config(text=f"❌ خطأ في تحميل البيانات: {str(e)}")
            import traceback
            traceback.print_exc()

    def extract_filter_options(self):
        """استخراج خيارات الفلاتر من البيانات - نسخة محسنة"""
        
        self.dates = set()
        self.items = set()
        self.categories = set()
        self.projects = set()
        
        print("🔍 استخراج خيارات الفلاتر من البيانات...")
        
        for i, item in enumerate(self.all_data):
            print(f"معالجة العنصر {i+1}: {item}")
            
            # استخراج التواريخ (من آخر تحديث)
            last_updated = item.get('آخر تحديث', '') or item.get('تاريخ آخر تحديث', '')
            if last_updated and last_updated.strip():
                try:
                    date_part = last_updated.split(' ')[0]
                    if date_part and len(date_part) >= 8:  # تأكد من وجود تاريخ صحيح
                        self.dates.add(date_part)
                        print(f"  ✓ تاريخ مضاف: {date_part}")
                except Exception as e:
                    print(f"  ⚠️ خطأ في معالجة التاريخ '{last_updated}': {e}")
            
            # استخراج العناصر
            item_name = item.get('اسم العنصر', '') or item.get('العنصر', '')
            if item_name and item_name.strip():
                self.items.add(item_name.strip())
                print(f"  ✓ عنصر مضاف: {item_name}")
            
            # استخراج التصنيفات
            category = item.get('التصنيف', '') or item.get('الفئة', '')
            if category and category.strip():
                self.categories.add(category.strip())
                print(f"  ✓ تصنيف مضاف: {category}")
            
            # استخراج المشاريع
            project = item.get('رقم المشروع', '') or item.get('المشروع', '')
            if project and project.strip():
                self.projects.add(project.strip())
                print(f"  ✓ مشروع مضاف: {project}")
        
        # تحويل إلى قوائم مرتبة وإضافة قيم افتراضية إذا لم توجد
        self.dates = sorted(list(self.dates)) if self.dates else ['2025-11-17']
        self.items = sorted(list(self.items)) if self.items else ['عنصر تجريبي']
        self.categories = sorted(list(self.categories)) if self.categories else ['تصنيف تجريبي']
        self.projects = sorted(list(self.projects)) if self.projects else ['مشروع تجريبي']
        
        print(f"📅 التواريخ المتاحة: {len(self.dates)} ({self.dates[:3]}...)")
        print(f"📦 العناصر المتاحة: {len(self.items)} ({self.items[:3]}...)")
        print(f"🏷️ التصنيفات المتاحة: {len(self.categories)} ({list(self.categories)})")
        print(f"🎯 المشاريع المتاحة: {len(self.projects)} ({list(self.projects)})")

    def setup_filters(self):
        """إعداد قوائم الفلاتر"""
        
        try:
            print("🔧 إعداد قوائم الفلاتر...")
            
            # إعداد قائمة التواريخ
            date_values = ["الكل"] + self.dates
            self.date_combo['values'] = date_values
            self.date_combo.set("الكل")
            
            # إعداد قائمة العناصر
            item_values = ["الكل"] + self.items
            self.item_combo['values'] = item_values
            self.item_combo.set("الكل")
            
            # إعداد قائمة التصنيفات
            category_values = ["الكل"] + self.categories
            self.category_combo['values'] = category_values
            self.category_combo.set("الكل")
            
            # إعداد قائمة المشاريع
            project_values = ["الكل"] + self.projects
            self.project_combo['values'] = project_values
            self.project_combo.set("الكل")
            
            # ربط الأحداث
            self.bind_events()
            
            print("✅ تم إعداد الفلاتر بنجاح")
            
        except Exception as e:
            print(f"❌ خطأ في إعداد الفلاتر: {str(e)}")

    def bind_events(self):
        """ربط أحداث التفاعل مع الفلاتر"""
        
        self.date_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_filters())
        self.item_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_filters())
        self.category_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_filters())
        self.project_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_filters())
        self.quantity_op_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_filters())
        self.quantity_entry.bind('<KeyRelease>', lambda e: self.apply_filters())

    def apply_filters(self):
        """تطبيق الفلاتر على البيانات"""
        
        try:
            print("\n🔍 تطبيق الفلاتر...")
            
            # الحصول على قيم الفلاتر
            selected_date = self.selected_date.get()
            selected_item = self.selected_item.get()
            selected_category = self.selected_category.get()
            selected_project = self.selected_project.get()
            quantity_op = self.quantity_op_combo.get()
            quantity_val = self.quantity_entry.get().strip()
            
            print(f"📅 التاريخ المختار: '{selected_date}'")
            print(f"📦 العنصر المختار: '{selected_item}'")
            print(f"🏷️ التصنيف المختار: '{selected_category}'")
            print(f"🎯 المشروع المختار: '{selected_project}'")
            print(f"🔢 الكمية: '{quantity_op}' '{quantity_val}'")
            
            # تطبيق الفلاتر
            self.filtered_data = []
            
            for item in self.all_data:
                include_item = True
                
                # فلتر التاريخ
                if selected_date != "الكل":
                    last_updated = item.get('آخر تحديث', '')
                    if selected_date not in last_updated:
                        include_item = False
                
                # فلتر العنصر
                if selected_item != "الكل":
                    item_name = item.get('اسم العنصر', '')
                    if item_name != selected_item:
                        include_item = False
                
                # فلتر التصنيف
                if selected_category != "الكل":
                    category = item.get('التصنيف', '')
                    if category != selected_category:
                        include_item = False
                
                # فلتر المشروع
                if selected_project != "الكل":
                    project = item.get('رقم المشروع', '')
                    if project != selected_project:
                        include_item = False
                
                # فلتر الكمية
                if quantity_val and quantity_op:
                    try:
                        remaining_qty = int(item.get('الكمية المتبقية', '0'))
                        filter_qty = int(quantity_val)
                        
                        if quantity_op == "يساوي" and remaining_qty != filter_qty:
                            include_item = False
                        elif quantity_op == "أكبر من" and remaining_qty <= filter_qty:
                            include_item = False
                        elif quantity_op == "أصغر من" and remaining_qty >= filter_qty:
                            include_item = False
                    except ValueError:
                        pass
                
                if include_item:
                    self.filtered_data.append(item)
            
            print(f"✅ تم العثور على {len(self.filtered_data)} عنصر مطابق من أصل {len(self.all_data)}")
            
            # عرض النتائج
            self.display_data()
            
        except Exception as e:
            print(f"❌ خطأ في تطبيق الفلاتر: {str(e)}")
            import traceback
            traceback.print_exc()

    def display_data(self):
        """عرض البيانات في الجدول مع تحديث الإحصائيات"""
        
        try:
            print(f"🔄 عرض {len(self.filtered_data)} عنصر في الجدول")
            
            # مسح البيانات الحالية
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # متغيرات الإحصائيات
            total_items = 0
            total_initial = 0
            total_in = 0
            total_out = 0
            total_remaining = 0
            low_stock_count = 0
            categories_set = set()
            projects_set = set()
            
            # عرض البيانات وحساب الإحصائيات
            for i, item in enumerate(self.filtered_data):
                # استخراج البيانات مع الأسماء الصحيحة
                item_name = item.get('اسم العنصر', '')
                category = item.get('التصنيف', '')
                initial_qty_str = item.get('الكمية الابتدائية', '0')
                in_qty_str = item.get('الكمية الداخلة', '0')
                out_qty_str = item.get('الكمية الخارجة', '0')
                remaining_qty_str = item.get('الكمية المتبقية', '0')
                project = item.get('رقم المشروع', '')
                last_updated = item.get('آخر تحديث', '')
                
                print(f"  عنصر {i+1}: {item_name} - ابتدائية:{initial_qty_str}, داخلة:{in_qty_str}, خارجة:{out_qty_str}, متبقية:{remaining_qty_str}")
                
                # تحويل إلى أرقام للإحصائيات
                try:
                    initial_qty = int(initial_qty_str) if initial_qty_str.isdigit() else 0
                    in_qty = int(in_qty_str) if in_qty_str.isdigit() else 0
                    out_qty = int(out_qty_str) if out_qty_str.isdigit() else 0
                    remaining_qty = int(remaining_qty_str) if remaining_qty_str.isdigit() else 0
                except ValueError:
                    initial_qty = in_qty = out_qty = remaining_qty = 0
                
                # تحديث الإحصائيات
                total_items += 1
                total_initial += initial_qty
                total_in += in_qty
                total_out += out_qty
                total_remaining += remaining_qty
                
                if remaining_qty <= 10:
                    low_stock_count += 1
                
                if category:
                    categories_set.add(category)
                if project:
                    projects_set.add(project)
                
                # تحديد لون الصف حسب الكمية المتبقية
                if remaining_qty <= 10:
                    tag = "low_stock"
                elif remaining_qty <= 50:
                    tag = "medium_stock"
                else:
                    tag = "high_stock"
                
                # إدراج الصف في الجدول
                values = (item_name, category, initial_qty_str, in_qty_str, out_qty_str, remaining_qty_str, project, last_updated)
                self.tree.insert('', 'end', values=values, tags=(tag,))
            
            # تحديث الإحصائيات المحسنة
            self.update_enhanced_statistics(total_items, total_initial, total_in, total_out, total_remaining, 
                                         len(categories_set), len(projects_set), low_stock_count)
            
            # تحديث معلومات النتائج
            results_text = f"📊 النتائج: {total_items} عنصر من أصل {len(self.all_data)}"
            if low_stock_count > 0:
                results_text += f" | ⚠️ مخزون منخفض: {low_stock_count}"
            self.results_info.config(text=results_text)
            
            print(f"✅ تم عرض {total_items} عنصر بنجاح")
            print(f"📊 الإحصائيات النهائية: ابتدائية:{total_initial:,}, داخلة:{total_in:,}, خارجة:{total_out:,}, متبقية:{total_remaining:,}")
            
        except Exception as e:
            print(f"❌ خطأ في عرض البيانات: {str(e)}")
            import traceback
            traceback.print_exc()
            if hasattr(self, 'stats_labels'):
                self.update_enhanced_statistics(0, 0, 0, 0, 0, 0, 0, 0)

    def update_enhanced_statistics(self, total_items, total_initial, total_in, total_out, 
                                 total_remaining, unique_categories, unique_projects, low_stock_count):
        """تحديث الإحصائيات المحسنة"""
        
        try:
            if hasattr(self, 'stats_labels'):
                # الإحصائيات الأساسية
                self.stats_labels['total_items'].config(text=f"🔢 إجمالي العناصر: {total_items}")
                self.stats_labels['unique_categories'].config(text=f"🏷️ عدد التصنيفات: {unique_categories}")
                self.stats_labels['unique_projects'].config(text=f"🎯 عدد المشاريع: {unique_projects}")
                self.stats_labels['low_stock_items'].config(text=f"⚠️ مخزون منخفض: {low_stock_count}")
                
                # إحصائيات الكميات
                self.stats_labels['total_initial'].config(text=f"📥 إجمالي الكمية الابتدائية: {total_initial:,}")
                self.stats_labels['total_in'].config(text=f"⬇️ إجمالي الواردات: {total_in:,}")
                self.stats_labels['total_out'].config(text=f"⬆️ إجمالي الصادرات: {total_out:,}")
                self.stats_labels['total_remaining'].config(text=f"📦 إجمالي المتبقي: {total_remaining:,}")
                
                # حساب معدل الدوران
                turnover_rate = 0
                if total_initial > 0:
                    turnover_rate = (total_out / total_initial) * 100
                self.stats_labels['turnover_rate'].config(text=f"🔄 معدل الدوران: {turnover_rate:.1f}%")
                
                print(f"📊 تم تحديث الإحصائيات بنجاح - معدل الدوران: {turnover_rate:.1f}%")
                
        except Exception as e:
            print(f"❌ خطأ في تحديث الإحصائيات: {str(e)}")

    def clear_filters(self):
        """مسح جميع الفلاتر"""
        
        print("\n🗑️ مسح جميع الفلاتر...")
        
        # إعادة تعيين جميع الفلاتر
        self.selected_date.set("الكل")
        self.selected_item.set("الكل")
        self.selected_category.set("الكل")
        self.selected_project.set("الكل")
        self.quantity_entry.delete(0, tk.END)
        
        # تحديث comboboxes
        self.date_combo.set("الكل")
        self.item_combo.set("الكل")
        self.category_combo.set("الكل")
        self.project_combo.set("الكل")
        self.quantity_op_combo.set("يساوي")
        
        # إعادة عرض جميع البيانات
        self.filtered_data = self.all_data.copy()
        self.display_data()
        
        print("✅ تم مسح جميع الفلاتر")

    def refresh_data(self):
        """تحديث البيانات من المصدر"""
        print("🔄 تحديث البيانات...")
        self.load_data()

    def sort_by_column(self, col):
        """فرز البيانات حسب العمود المحدد"""
        print(f"🔀 فرز حسب العمود: {col}")
        # يمكن تنفيذ منطق الفرز هنا

    def show(self):
        """عرض النافذة"""
        if self.window:
            self.window.deiconify()
            self.window.lift()
            self.window.focus_force()