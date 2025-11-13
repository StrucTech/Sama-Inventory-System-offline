#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نافذة البحث المحديثة للتعامل مع Activity Log الجديد
"""

import tkinter as tk
from tkinter import ttk, messagebox
import re
from datetime import datetime, timedelta
from enhanced_sheets_manager import EnhancedSheetsManager

class NewFilterSearchWindow:
    """نافذة البحث المحديثة مع الهيكل الجديد"""
    
    def __init__(self, parent, enhanced_manager, current_user=None):
        self.parent = parent
        self.enhanced_manager = enhanced_manager
        self.current_user = current_user
        
        # إنشاء النافذة
        self.window = tk.Toplevel(parent)
        
        # تحديد عنوان النافذة حسب نوع المستخدم
        title = "🔍 البحث والفلترة المحسن"
        if self.current_user and self.current_user.get('user_type') == 'user':
            project_id = self.current_user.get('project_id', '')
            if project_id:
                title += f" - مشروع {project_id}"
        
        self.window.title(title)
        self.window.geometry("1400x800")
        self.window.resizable(True, True)
        
        # البيانات
        self.all_data = []
        self.filtered_data = []
        
        # متغيرات الفلاتر
        self.filter_vars = {
            'date_from': tk.StringVar(),
            'date_to': tk.StringVar(),
            'operation_type': tk.StringVar(),
            'item_name': tk.StringVar(),
            'category': tk.StringVar(),
            'recipient': tk.StringVar(),
            'project': tk.StringVar()
        }
        
        # إنشاء الواجهة
        self.create_widgets()
        self.load_data()
        
        # تطبيق الفلاتر الأولية
        self.apply_filters()
    
    def create_widgets(self):
        """إنشاء عناصر الواجهة"""
        # الإطار الرئيسي
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # إطار الفلاتر
        self.create_filters_frame(main_frame)
        
        # إطار النتائج
        self.create_results_frame(main_frame)
        
        # إطار الإحصائيات
        self.create_statistics_frame(main_frame)
    
    def create_filters_frame(self, parent):
        """إنشاء إطار الفلاتر"""
        filters_frame = ttk.LabelFrame(parent, text="🔍 فلاتر البحث المحسنة", padding="15")
        filters_frame.pack(fill=tk.X, pady=(0, 10))
        
        # الصف الأول: التواريخ
        date_frame = ttk.Frame(filters_frame)
        date_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(date_frame, text="📅 من تاريخ:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(0, 5))
        self.date_from_entry = ttk.Entry(date_frame, textvariable=self.filter_vars['date_from'], width=12)
        self.date_from_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.date_from_entry.insert(0, "YYYY-MM-DD")
        self.date_from_entry.config(foreground="gray")
        ttk.Button(date_frame, text="📅", command=lambda: self.show_date_picker('from'), width=3).pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Label(date_frame, text="📅 إلى تاريخ:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(0, 5))
        self.date_to_entry = ttk.Entry(date_frame, textvariable=self.filter_vars['date_to'], width=12)
        self.date_to_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.date_to_entry.insert(0, "YYYY-MM-DD")
        self.date_to_entry.config(foreground="gray")
        ttk.Button(date_frame, text="📅", command=lambda: self.show_date_picker('to'), width=3).pack(side=tk.LEFT, padx=(0, 15))
        
        # أزرار التواريخ السريعة
        ttk.Button(date_frame, text="اليوم", command=self.set_today, width=8).pack(side=tk.LEFT, padx=2)
        ttk.Button(date_frame, text="هذا الأسبوع", command=self.set_this_week, width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(date_frame, text="هذا الشهر", command=self.set_this_month, width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(date_frame, text="مسح التواريخ", command=self.clear_dates, width=12).pack(side=tk.LEFT, padx=2)
        
        # الصف الثاني: الفلاتر الرئيسية
        main_filters_frame = ttk.Frame(filters_frame)
        main_filters_frame.pack(fill=tk.X, pady=(0, 10))
        
        # نوع العملية
        ttk.Label(main_filters_frame, text="⚙️ نوع العملية:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(0, 5))
        self.operation_combo = ttk.Combobox(main_filters_frame, textvariable=self.filter_vars['operation_type'], 
                                          width=15, state="readonly")
        self.operation_combo.pack(side=tk.LEFT, padx=(0, 15))
        
        # التصنيف
        ttk.Label(main_filters_frame, text="🏷️ التصنيف:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(0, 5))
        self.category_combo = ttk.Combobox(main_filters_frame, textvariable=self.filter_vars['category'], 
                                         width=20, state="readonly")
        self.category_combo.pack(side=tk.LEFT, padx=(0, 15))
        
        # اسم العنصر (قائمة منسدلة)
        ttk.Label(main_filters_frame, text="📦 اسم العنصر:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(0, 5))
        self.item_combo = ttk.Combobox(main_filters_frame, textvariable=self.filter_vars['item_name'], 
                                      width=25, state="readonly")
        self.item_combo.pack(side=tk.LEFT, padx=(0, 15))
        
        # الصف الثالث: فلاتر إضافية
        extra_filters_frame = ttk.Frame(filters_frame)
        extra_filters_frame.pack(fill=tk.X, pady=(0, 10))
        
        # المستلم
        ttk.Label(extra_filters_frame, text="👤 المستلم:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(0, 5))
        self.recipient_entry = ttk.Entry(extra_filters_frame, textvariable=self.filter_vars['recipient'], width=15)
        self.recipient_entry.pack(side=tk.LEFT, padx=(0, 15))
        
        # المشروع
        ttk.Label(extra_filters_frame, text="🏗️ المشروع:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(0, 5))
        self.project_combo = ttk.Combobox(extra_filters_frame, textvariable=self.filter_vars['project'], 
                                         width=15, state="readonly")
        self.project_combo.pack(side=tk.LEFT, padx=(0, 15))
        
        # أزرار التحكم
        control_frame = ttk.Frame(filters_frame)
        control_frame.pack(fill=tk.X)
        
        ttk.Button(control_frame, text="🔍 بحث", command=self.apply_filters, width=12).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="🗑️ مسح جميع الفلاتر", command=self.clear_filters, width=18).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="🔄 تحديث", command=self.refresh_data, width=12).pack(side=tk.LEFT, padx=(0, 5))
        
        # ربط الأحداث
        # إزالة trace للمتغيرات لتجنب التضارب
        # for var in self.filter_vars.values():
        #     var.trace('w', lambda *args: self.on_filter_change())
        
        # ربط أحداث تغيير القوائم المنسدلة فقط
        self.operation_combo.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())
        self.category_combo.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())
        self.item_combo.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())
        
        # ربط أحداث النص للحقول الأخرى
        self.recipient_entry.bind("<KeyRelease>", lambda e: self.apply_filters())
        self.project_combo.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())
        
        # ربط أحداث placeholder text للتواريخ
        self.date_from_entry.bind("<FocusIn>", lambda e: self.on_date_focus_in(self.date_from_entry))
        self.date_from_entry.bind("<FocusOut>", lambda e: self.on_date_focus_out(self.date_from_entry, 'date_from'))
        self.date_to_entry.bind("<FocusIn>", lambda e: self.on_date_focus_in(self.date_to_entry))
        self.date_to_entry.bind("<FocusOut>", lambda e: self.on_date_focus_out(self.date_to_entry, 'date_to'))
    
    def create_results_frame(self, parent):
        """إنشاء إطار النتائج"""
        results_frame = ttk.LabelFrame(parent, text="📊 النتائج", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # إنشاء Treeview للنتائج
        columns = ["التاريخ", "الوقت", "العملية", "العنصر", "التصنيف", 
                  "مضاف", "مخرج", "سابق", "حالي", "المستلم", "المشروع", "التفاصيل"]
        
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=15)
        
        # تكوين الأعمدة
        column_widths = [80, 70, 80, 150, 120, 60, 60, 60, 60, 100, 80, 200]
        for col, width in zip(columns, column_widths):
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=width, minwidth=50)
        
        # شريط التمرير
        scrollbar_y = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        scrollbar_x = ttk.Scrollbar(results_frame, orient=tk.HORIZONTAL, command=self.results_tree.xview)
        self.results_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # تخطيط العناصر
        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_statistics_frame(self, parent):
        """إنشاء إطار الإحصائيات"""
        stats_frame = ttk.LabelFrame(parent, text="📈 إحصائيات سريعة", padding="10")
        stats_frame.pack(fill=tk.X)
        
        # تقسيم الإحصائيات إلى أعمدة
        col1 = ttk.Frame(stats_frame)
        col1.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        col2 = ttk.Frame(stats_frame)
        col2.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        col3 = ttk.Frame(stats_frame)
        col3.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # العمود الأول: الكميات
        ttk.Label(col1, text="📊 الكميات", font=("Arial", 10, "bold")).pack()
        self.total_added_label = ttk.Label(col1, text="مضاف: 0")
        self.total_added_label.pack()
        self.total_removed_label = ttk.Label(col1, text="مخرج: 0")
        self.total_removed_label.pack()
        self.net_quantity_label = ttk.Label(col1, text="الصافي: 0")
        self.net_quantity_label.pack()
        
        # العمود الثاني: العمليات
        ttk.Label(col2, text="⚙️ العمليات", font=("Arial", 10, "bold")).pack()
        self.operations_label = ttk.Label(col2, text="إجمالي: 0")
        self.operations_label.pack()
        self.add_operations_label = ttk.Label(col2, text="إضافة: 0")
        self.add_operations_label.pack()
        self.remove_operations_label = ttk.Label(col2, text="إخراج: 0")
        self.remove_operations_label.pack()
        
        # العمود الثالث: التصنيفات
        ttk.Label(col3, text="🏷️ التصنيفات", font=("Arial", 10, "bold")).pack()
        self.categories_label = ttk.Label(col3, text="مختلفة: 0")
        self.categories_label.pack()
        self.projects_label = ttk.Label(col3, text="مشاريع: 0")
        self.projects_label.pack()
        self.date_range_label = ttk.Label(col3, text="المدى: -")
        self.date_range_label.pack()
    
    def load_data(self):
        """تحميل البيانات من الشيت الجديد"""
        try:
            print("📊 تحميل البيانات من الشيت الجديد...")
            all_data = self.enhanced_manager.get_activity_log_new_format()
            
            # التحقق من نوع المستخدم وفلترة البيانات
            user_project_id = None
            is_regular_user = False
            if self.current_user:
                user_type = self.current_user.get('user_type', 'user')
                user_project_id = self.current_user.get('project_id', '')
                is_regular_user = user_type == 'user'
                
                if is_regular_user:
                    print(f"👤 مستخدم عادي - سيتم عرض بيانات المشروع: {user_project_id}")
                else:
                    print(f"👨‍💼 مدير - سيتم عرض جميع البيانات")
            
            # فلترة البيانات للمستخدمين العاديين
            if is_regular_user and user_project_id:
                self.all_data = []
                for i, record in enumerate(all_data):
                    if len(record) >= 11:  # التأكد من وجود عمود رقم المشروع
                        record_project = record[10] if record[10] else ""  # عمود رقم المشروع
                        if record_project == user_project_id:
                            self.all_data.append(record)
                        # طباعة عينة للتحقق
                        if i < 3:
                            print(f"   📋 سجل {i+1}: مشروع='{record_project}' مطابق={record_project == user_project_id}")
                print(f"✅ تم تحميل {len(self.all_data)} سجل من مشروع '{user_project_id}' (من أصل {len(all_data)})")
            else:
                self.all_data = all_data
                print(f"✅ تم تحميل {len(self.all_data)} سجل")
            
            # تحديث قوائم الفلاتر
            self.update_filter_options()
            
        except Exception as e:
            print(f"❌ خطأ في تحميل البيانات: {e}")
            messagebox.showerror("خطأ", f"فشل في تحميل البيانات:\n{e}")
    
    def update_filter_options(self):
        """تحديث خيارات الفلاتر"""
        operations = set(["جميع العمليات"])
        categories = set(["جميع التصنيفات"])
        items = set(["جميع العناصر"])
        
        for record in self.all_data:
            if len(record) >= 12:
                if record[2]:  # نوع العملية
                    operations.add(record[2])
                if record[4]:  # التصنيف
                    categories.add(record[4])
                if record[3]:  # اسم العنصر
                    items.add(record[3].strip())
        
        # تحديث القوائم المنسدلة مع وضع "جميع..." في البداية مع أيقونات توضيحية
        operations_list = ["🔄 جميع العمليات"] + sorted([op for op in operations if op != "جميع العمليات"])
        self.operation_combo['values'] = operations_list
        self.operation_combo.set("🔄 جميع العمليات")
        
        categories_list = ["📂 جميع التصنيفات"] + sorted([cat for cat in categories if cat != "جميع التصنيفات"])
        self.category_combo['values'] = categories_list
        self.category_combo.set("📂 جميع التصنيفات")
        
        items_list = ["📦 جميع العناصر"] + sorted([item for item in items if item != "جميع العناصر"])
        self.item_combo['values'] = items_list
        self.item_combo.set("📦 جميع العناصر")
        
        # إعداد فلتر المشروع
        self.setup_project_filter()
    
    def setup_project_filter(self):
        """إعداد فلتر المشروع بناء على نوع المستخدم"""
        try:
            print("🏗️ إعداد فلتر المشروع...")
            
            # للمستخدمين العاديين - إظهار المشروع المخصص لهم فقط
            if self.current_user and self.current_user.get('user_type') == 'user':
                user_project_id = self.current_user.get('project_id', '')
                print(f"👤 المستخدم العادي - مشروع: {user_project_id}")
                
                if user_project_id:
                    # عرض المشروع المخصص فقط
                    self.project_combo['values'] = [user_project_id]
                    self.project_combo.set(user_project_id)
                    self.project_combo.config(state="disabled")  # منع التغيير
                    print(f"✅ تم تعيين مشروع المستخدم: {user_project_id}")
                else:
                    # إذا لم يكن له مشروع مخصص
                    self.project_combo['values'] = ["لا يوجد مشروع مخصص"]
                    self.project_combo.set("لا يوجد مشروع مخصص")
                    self.project_combo.config(state="disabled")
                    print("⚠️ المستخدم ليس له مشروع مخصص")
            
            # للمديرين - إظهار جميع المشاريع
            else:
                print("👨‍💼 المدير - سيتم عرض جميع المشاريع المتاحة")
                
                # جمع جميع المشاريع من البيانات
                projects = set(["جميع المشاريع"])
                for record in self.all_data:
                    if len(record) >= 11 and record[10]:  # عمود رقم المشروع
                        projects.add(record[10].strip())
                
                # إضافة المشاريع من قاعدة البيانات
                try:
                    from sheets.projects_manager import ProjectsManager
                    projects_manager = ProjectsManager()
                    all_projects = projects_manager.get_all_projects()
                    for project in all_projects:
                        if project.get('project_id'):
                            projects.add(project['project_id'])
                    print(f"📊 تم العثور على {len(projects)-1} مشروع")
                except Exception as e:
                    print(f"⚠️ تعذر تحميل المشاريع من قاعدة البيانات: {e}")
                
                # تحديث القائمة المنسدلة
                projects_list = ["🏗️ جميع المشاريع"] + sorted([p for p in projects if p != "جميع المشاريع"])
                self.project_combo['values'] = projects_list
                self.project_combo.set("🏗️ جميع المشاريع")
                self.project_combo.config(state="readonly")  # قابل للتغيير للمديرين
                
        except Exception as e:
            print(f"❌ خطأ في إعداد فلتر المشروع: {e}")
            # القيم الافتراضية في حالة الخطأ
            self.project_combo['values'] = ["🏗️ جميع المشاريع"]
            self.project_combo.set("🏗️ جميع المشاريع")
    
    def apply_filters(self):
        """تطبيق الفلاتر وعرض النتائج"""
        try:
            # مسح النتائج السابقة
            for item in self.results_tree.get_children():
                self.results_tree.delete(item)
            
            # الحصول على قيم الفلاتر
            date_from = self.filter_vars['date_from'].get()
            date_to = self.filter_vars['date_to'].get()
            operation_type = self.operation_combo.get()  # قراءة مباشرة من الكومبو
            item_name = self.item_combo.get()           # قراءة مباشرة من الكومبو
            category = self.category_combo.get()         # قراءة مباشرة من الكومبو
            recipient = self.recipient_entry.get()       # قراءة مباشرة من حقل النص
            project = self.project_combo.get()           # قراءة مباشرة من كومبو المشروع
            
            # تنظيف placeholder text
            if date_from == "YYYY-MM-DD":
                date_from = ""
            if date_to == "YYYY-MM-DD":
                date_to = ""
            
            # تحويل القيم الافتراضية (مع الأيقونات الجديدة)
            if operation_type in ["جميع العمليات", "🔄 جميع العمليات"] or not operation_type:
                operation_type = None
            if category in ["جميع التصنيفات", "📂 جميع التصنيفات"] or not category:
                category = None
            if item_name in ["جميع العناصر", "📦 جميع العناصر"] or not item_name:
                item_name = None
            if project in ["جميع المشاريع", "🏗️ جميع المشاريع", "لا يوجد مشروع مخصص"] or not project:
                project = None
            
            # تنظيف قيم المستلم والمشروع من المسافات
            recipient = recipient.strip() if recipient else None
            project = project.strip() if project else None
            
            # طباعة للتأكد من قيم المستلم والمشروع
            if recipient or project:
                print(f"🔍 فلاتر النص:")
                print(f"   👤 المستلم: '{recipient}'")
                print(f"   🏗️ المشروع: '{project}'")
            
            # تطبيق الفلترة باستخدام المدير المحسن
            self.filtered_data = self.enhanced_manager.filter_activity_log_new(
                date_from=date_from if date_from else None,
                date_to=date_to if date_to else None,
                operation_type=operation_type,
                item_name=item_name if item_name else None,
                category=category,
                recipient=recipient if recipient else None,
                project=project if project else None
            )
            
            # عرض النتائج
            for record in self.filtered_data:
                if len(record) >= 12:
                    # تنسيق القيم للعرض
                    display_values = [
                        record[0],  # التاريخ
                        record[1],  # الوقت
                        record[2],  # العملية
                        record[3][:20] + "..." if len(record[3]) > 20 else record[3],  # العنصر (مختصر)
                        record[4],  # التصنيف
                        f"{float(record[5]):.0f}" if record[5] and record[5] != '0' else "",  # مضاف
                        f"{float(record[6]):.0f}" if record[6] and record[6] != '0' else "",  # مخرج
                        f"{float(record[7]):.0f}" if record[7] and record[7] != '0' else "",  # سابق
                        f"{float(record[8]):.0f}" if record[8] and record[8] != '0' else "",  # حالي
                        record[9],  # المستلم
                        record[10], # المشروع
                        record[11][:30] + "..." if len(record[11]) > 30 else record[11]  # التفاصيل (مختصرة)
                    ]
                    self.results_tree.insert("", "end", values=display_values)
            
            # تحديث الإحصائيات
            self.update_statistics()
            
            # إظهار الفلاتر النشطة
            active_filters = []
            if date_from or date_to:
                date_text = f"📅 {date_from or '...'} - {date_to or '...'}"
                active_filters.append(date_text)
            if operation_type:
                active_filters.append(f"🔄 {operation_type}")
            if item_name:
                active_filters.append(f"📦 {item_name[:15]}...")
            if category:
                active_filters.append(f"📂 {category}")
            if recipient:
                active_filters.append(f"👤 {recipient}")
            if project:
                active_filters.append(f"🏗️ {project}")
            
            # تحديث عنوان النافذة مع الفلاتر النشطة
            if active_filters:
                filter_text = " | ".join(active_filters)
                self.window.title(f"🔍 البحث والفلترة - {len(self.filtered_data)} نتيجة - [{filter_text}]")
            else:
                self.window.title(f"🔍 البحث والفلترة المحسن - {len(self.filtered_data)} نتيجة")
            
            print(f"✅ تم عرض {len(self.filtered_data)} نتيجة")
            
        except Exception as e:
            print(f"❌ خطأ في تطبيق الفلاتر: {e}")
            messagebox.showerror("خطأ", f"خطأ في البحث:\n{e}")
    
    def update_statistics(self):
        """تحديث الإحصائيات"""
        try:
            total_added = 0
            total_removed = 0
            operations_count = {}
            categories = set()
            projects = set()
            dates = []
            
            for record in self.filtered_data:
                if len(record) >= 12:
                    # حساب الكميات
                    try:
                        added = float(record[5]) if record[5] else 0
                        removed = float(record[6]) if record[6] else 0
                        total_added += added
                        total_removed += removed
                    except ValueError:
                        pass
                    
                    # عد العمليات
                    operation = record[2]
                    operations_count[operation] = operations_count.get(operation, 0) + 1
                    
                    # جمع التصنيفات والمشاريع
                    if record[4]:
                        categories.add(record[4])
                    if record[10]:
                        projects.add(record[10])
                    
                    # جمع التواريخ
                    if record[0]:
                        dates.append(record[0])
            
            # تحديث التسميات
            net_quantity = total_added - total_removed
            self.total_added_label.config(text=f"مضاف: {total_added:.0f}")
            self.total_removed_label.config(text=f"مخرج: {total_removed:.0f}")
            self.net_quantity_label.config(text=f"الصافي: {net_quantity:.0f}", 
                                         foreground="green" if net_quantity >= 0 else "red")
            
            self.operations_label.config(text=f"إجمالي: {len(self.filtered_data)}")
            self.add_operations_label.config(text=f"إضافة: {operations_count.get('إضافة', 0)}")
            self.remove_operations_label.config(text=f"إخراج: {operations_count.get('إخراج', 0)}")
            
            self.categories_label.config(text=f"تصنيفات: {len(categories)}")
            self.projects_label.config(text=f"مشاريع: {len(projects)}")
            
            # المدى الزمني
            if dates:
                dates.sort()
                date_range = f"{dates[0]} : {dates[-1]}" if len(dates) > 1 else dates[0]
                self.date_range_label.config(text=f"المدى: {date_range}")
            else:
                self.date_range_label.config(text="المدى: -")
                
        except Exception as e:
            print(f"❌ خطأ في تحديث الإحصائيات: {e}")
    
    def on_date_focus_in(self, entry):
        """إزالة placeholder عند التركيز"""
        if entry.get() == "YYYY-MM-DD":
            entry.delete(0, tk.END)
            entry.config(foreground="black")
    
    def on_date_focus_out(self, entry, var_name):
        """إضافة placeholder عند فقدان التركيز"""
        if not entry.get():
            entry.insert(0, "YYYY-MM-DD")
            entry.config(foreground="gray")
            self.filter_vars[var_name].set("")
        else:
            self.filter_vars[var_name].set(entry.get())
    
    def on_filter_change(self):
        """استجابة لتغيير الفلاتر"""
        # تطبيق تأخير للتجنب الاستدعاءات المتكررة
        if hasattr(self, '_filter_timer'):
            self.window.after_cancel(self._filter_timer)
        self._filter_timer = self.window.after(500, self.apply_filters)
    
    def set_today(self):
        """تعيين تاريخ اليوم"""
        today = datetime.now().strftime("%Y-%m-%d")
        self.filter_vars['date_from'].set(today)
        self.filter_vars['date_to'].set(today)
        # تحديث حقول النص مباشرة
        self.date_from_entry.delete(0, tk.END)
        self.date_from_entry.insert(0, today)
        self.date_from_entry.config(foreground="black")
        self.date_to_entry.delete(0, tk.END)
        self.date_to_entry.insert(0, today)
        self.date_to_entry.config(foreground="black")
        # تطبيق الفلاتر فوراً
        self.apply_filters()
    
    def set_this_week(self):
        """تعيين هذا الأسبوع"""
        today = datetime.now()
        start_week = today - timedelta(days=today.weekday())
        end_week = start_week + timedelta(days=6)
        date_from = start_week.strftime("%Y-%m-%d")
        date_to = end_week.strftime("%Y-%m-%d")
        self.filter_vars['date_from'].set(date_from)
        self.filter_vars['date_to'].set(date_to)
        # تحديث حقول النص مباشرة
        self.date_from_entry.delete(0, tk.END)
        self.date_from_entry.insert(0, date_from)
        self.date_from_entry.config(foreground="black")
        self.date_to_entry.delete(0, tk.END)
        self.date_to_entry.insert(0, date_to)
        self.date_to_entry.config(foreground="black")
        # تطبيق الفلاتر فوراً
        self.apply_filters()
    
    def set_this_month(self):
        """تعيين هذا الشهر"""
        today = datetime.now()
        start_month = today.replace(day=1)
        if today.month == 12:
            end_month = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            end_month = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
        date_from = start_month.strftime("%Y-%m-%d")
        date_to = end_month.strftime("%Y-%m-%d")
        self.filter_vars['date_from'].set(date_from)
        self.filter_vars['date_to'].set(date_to)
        # تحديث حقول النص مباشرة
        self.date_from_entry.delete(0, tk.END)
        self.date_from_entry.insert(0, date_from)
        self.date_from_entry.config(foreground="black")
        self.date_to_entry.delete(0, tk.END)
        self.date_to_entry.insert(0, date_to)
        self.date_to_entry.config(foreground="black")
        # تطبيق الفلاتر فوراً
        self.apply_filters()
    
    def clear_dates(self):
        """مسح التواريخ"""
        self.filter_vars['date_from'].set("")
        self.filter_vars['date_to'].set("")
        # مسح حقول النص وإعادة placeholder
        self.date_from_entry.delete(0, tk.END)
        self.date_from_entry.insert(0, "YYYY-MM-DD")
        self.date_from_entry.config(foreground="gray")
        self.date_to_entry.delete(0, tk.END)
        self.date_to_entry.insert(0, "YYYY-MM-DD")
        self.date_to_entry.config(foreground="gray")
        # تطبيق الفلاتر فوراً
        self.apply_filters()
    
    def clear_filters(self):
        """مسح جميع الفلاتر"""
        # مسح متغيرات الفلاتر
        self.filter_vars['date_from'].set("")
        self.filter_vars['date_to'].set("")
        self.filter_vars['recipient'].set("")
        
        # إعادة تعيين القوائم المنسدلة
        self.operation_combo.set("🔄 جميع العمليات")
        self.category_combo.set("📂 جميع التصنيفات")
        self.item_combo.set("📦 جميع العناصر")
        
        # إعادة إعداد فلتر المشروع حسب نوع المستخدم
        if self.current_user and self.current_user.get('user_type') == 'user':
            user_project_id = self.current_user.get('project_id', '')
            if user_project_id:
                self.project_combo.set(user_project_id)
            else:
                self.project_combo.set("لا يوجد مشروع مخصص")
        else:
            self.project_combo.set("🏗️ جميع المشاريع")
        
        self.apply_filters()
    
    def show_date_picker(self, date_type):
        """عرض منتقي التاريخ"""
        try:
            # إنشاء نافذة التقويم
            calendar_window = tk.Toplevel(self.window)
            calendar_window.title("📅 اختيار التاريخ")
            calendar_window.geometry("300x250")
            calendar_window.resizable(False, False)
            
            # جعل النافذة في المقدمة
            calendar_window.transient(self.window)
            calendar_window.grab_set()
            
            # إطار التحكم
            control_frame = ttk.Frame(calendar_window)
            control_frame.pack(fill=tk.X, padx=10, pady=10)
            
            # التاريخ الحالي
            today = datetime.now()
            selected_year = tk.IntVar(value=today.year)
            selected_month = tk.IntVar(value=today.month)
            selected_day = tk.IntVar(value=today.day)
            
            # اختيار السنة والشهر
            ttk.Label(control_frame, text="السنة:").pack(side=tk.LEFT, padx=(0, 5))
            year_combo = ttk.Combobox(control_frame, textvariable=selected_year, 
                                     values=list(range(2020, 2030)), width=8, state="readonly")
            year_combo.pack(side=tk.LEFT, padx=(0, 10))
            
            ttk.Label(control_frame, text="الشهر:").pack(side=tk.LEFT, padx=(0, 5))
            months = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو",
                     "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]
            month_combo = ttk.Combobox(control_frame, values=months, state="readonly", width=10)
            month_combo.set(months[today.month - 1])
            month_combo.pack(side=tk.LEFT)
            
            # إطار التقويم
            calendar_frame = ttk.Frame(calendar_window)
            calendar_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
            
            def update_calendar():
                """تحديث عرض التقويم"""
                # مسح التقويم السابق
                for widget in calendar_frame.winfo_children():
                    widget.destroy()
                
                year = selected_year.get()
                month = selected_month.get()
                
                # عرض أيام الأسبوع
                days_header = ["أحد", "اثنين", "ثلاثاء", "أربعاء", "خميس", "جمعة", "سبت"]
                for i, day_name in enumerate(days_header):
                    label = ttk.Label(calendar_frame, text=day_name, font=("Arial", 9, "bold"))
                    label.grid(row=0, column=i, padx=1, pady=1, sticky="nsew")
                
                # حساب اليوم الأول من الشهر
                import calendar
                first_day = datetime(year, month, 1)
                start_day = first_day.weekday() + 1  # تحويل لتقويم أحد-سبت
                if start_day == 7:
                    start_day = 0
                
                # عدد أيام الشهر
                days_in_month = calendar.monthrange(year, month)[1]
                
                # عرض الأيام
                row = 1
                col = start_day
                
                for day in range(1, days_in_month + 1):
                    def make_day_button(d=day):
                        return lambda: select_date(d)
                    
                    btn = tk.Button(calendar_frame, text=str(day), width=4, height=2,
                                   command=make_day_button())
                    
                    # تمييز اليوم الحالي
                    if (year == today.year and month == today.month and day == today.day):
                        btn.config(bg="lightblue")
                    
                    btn.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
                    
                    col += 1
                    if col > 6:
                        col = 0
                        row += 1
                
                # تكوين الأعمدة والصفوف
                for i in range(7):
                    calendar_frame.columnconfigure(i, weight=1)
                for i in range(row + 1):
                    calendar_frame.rowconfigure(i, weight=1)
            
            def select_date(day):
                """اختيار التاريخ وإغلاق النافذة"""
                selected_day.set(day)
                year = selected_year.get()
                month = selected_month.get()
                
                # تنسيق التاريخ
                date_str = f"{year:04d}-{month:02d}-{day:02d}"
                
                # تحديث مربع النص المناسب
                if date_type == 'from':
                    self.filter_vars['date_from'].set(date_str)
                    self.date_from_entry.delete(0, tk.END)
                    self.date_from_entry.insert(0, date_str)
                    self.date_from_entry.config(foreground="black")
                else:
                    self.filter_vars['date_to'].set(date_str)
                    self.date_to_entry.delete(0, tk.END)
                    self.date_to_entry.insert(0, date_str)
                    self.date_to_entry.config(foreground="black")
                
                # تطبيق الفلاتر فوراً
                self.apply_filters()
                
                calendar_window.destroy()
            
            def on_month_change(event=None):
                """تحديث الشهر عند تغيير الاختيار"""
                try:
                    month_name = month_combo.get()
                    if month_name in months:
                        selected_month.set(months.index(month_name) + 1)
                        update_calendar()
                except:
                    pass
            
            def on_year_change(event=None):
                """تحديث السنة عند تغيير الاختيار"""
                update_calendar()
            
            # ربط الأحداث
            year_combo.bind("<<ComboboxSelected>>", on_year_change)
            month_combo.bind("<<ComboboxSelected>>", on_month_change)
            
            # عرض التقويم الأولي
            update_calendar()
            
            # أزرار إضافية
            button_frame = ttk.Frame(calendar_window)
            button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
            
            ttk.Button(button_frame, text="اليوم", 
                      command=lambda: select_date(today.day)).pack(side=tk.LEFT, padx=(0, 5))
            ttk.Button(button_frame, text="إلغاء", 
                      command=calendar_window.destroy).pack(side=tk.RIGHT)
            
        except Exception as e:
            print(f"❌ خطأ في منتقي التاريخ: {e}")
            messagebox.showerror("خطأ", f"فشل في فتح منتقي التاريخ: {e}")
    
    def refresh_data(self):
        """تحديث البيانات"""
        self.load_data()
        self.apply_filters()
    
    def show_statistics(self):
        """عرض إحصائيات مفصلة"""
        stats = self.enhanced_manager.get_statistics_new()
        if stats:
            stats_window = tk.Toplevel(self.window)
            stats_window.title("📊 إحصائيات مفصلة")
            stats_window.geometry("600x500")
            
            text_widget = tk.Text(stats_window, wrap=tk.WORD, font=("Arial", 11))
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            stats_text = f"""📊 إحصائيات مفصلة للنظام

📁 إجمالي السجلات: {stats['total_records']}
⬆️ إجمالي المضاف: {stats['total_added']:.0f}
⬇️ إجمالي المخرج: {stats['total_removed']:.0f}
📈 الصافي: {stats['total_added'] - stats['total_removed']:.0f}

🔄 العمليات:
"""
            for operation, count in stats['operations_count'].items():
                stats_text += f"   • {operation}: {count}\n"
            
            stats_text += "\n🏷️ التصنيفات:\n"
            for category, count in stats['categories_count'].items():
                stats_text += f"   • {category}: {count}\n"
            
            stats_text += "\n🏗️ المشاريع:\n"
            for project, count in stats['projects_count'].items():
                stats_text += f"   • {project}: {count}\n"
            
            stats_text += "\n📅 الملخص الشهري:\n"
            for month, count in sorted(stats['monthly_summary'].items()):
                stats_text += f"   • {month}: {count}\n"
            
            text_widget.insert("1.0", stats_text)
            text_widget.config(state=tk.DISABLED)

def test_new_filter_window():
    """اختبار النافذة الجديدة"""
    print("🧪 اختبار نافذة البحث الجديدة")
    
    try:
        from config.settings import load_config
        
        root = tk.Tk()
        root.withdraw()
        
        # تحميل الإعدادات
        config = load_config()
        if not config:
            print("❌ فشل في تحميل الإعدادات")
            return
        
        # إنشاء المدير المحسن
        enhanced_manager = EnhancedSheetsManager(
            credentials_file=config['credentials_file'],
            spreadsheet_name=config['spreadsheet_name'],
            worksheet_name=config['worksheet_name']
        )
        
        if not enhanced_manager.connect():
            print("❌ فشل في الاتصال")
            return
        
        # إنشاء مستخدم تجريبي للاختبار
        test_user = {
            'user_id': 'USR_002',
            'user_type': 'user',
            'project_id': 'P001'
        }
        
        # إنشاء النافذة
        filter_window = NewFilterSearchWindow(root, enhanced_manager, test_user)
        
        print("✅ تم إنشاء النافذة بنجاح")
        root.mainloop()
        
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {e}")

if __name__ == "__main__":
    test_new_filter_window()