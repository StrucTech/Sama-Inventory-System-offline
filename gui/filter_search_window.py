#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نافذة البحث باستخدام الفلاتر - نسخة جديدة منظمة بالكامل
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
        
        # البيانات
        self.all_items = []
        self.activity_log = []
        self.filtered_results = []
        
        # متغيرات الفلاتر
        self.filter_vars = {
            'date_from': tk.StringVar(),
            'date_to': tk.StringVar(),
            'item_name': tk.StringVar(value="جميع العناصر"),
            'category': tk.StringVar(value="جميع التصنيفات"),
            'project_id': tk.StringVar(value="جميع المشاريع")
        }
        
        # إنشاء النافذة
        self.create_window()
        self.create_widgets()
        self.load_data()
        
        print("✅ تم إنشاء نافذة البحث باستخدام الفلاتر")
    
    def create_window(self):
        """إنشاء النافذة الرئيسية"""
        self.window = tk.Toplevel(self.parent)
        
        # تحديد عنوان النافذة حسب نوع المستخدم
        title = "🔍 البحث باستخدام الفلاتر"
        if self.current_user and self.current_user.get('user_type') == 'user':
            project_id = self.current_user.get('project_id', '')
            if project_id:
                title += f" - مشروع {project_id}"
        
        self.window.title(title)
        self.window.geometry("1500x900")
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
        main_frame = ttk.Frame(self.window, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # العنوان
        title_text = "🔍 البحث باستخدام الفلاتر"
        if self.current_user and self.current_user.get('user_type') == 'user':
            project_id = self.current_user.get('project_id', '')
            if project_id:
                title_text += f" - مشروع {project_id}"
        
        title_label = ttk.Label(main_frame, text=title_text, 
                               font=("Arial", 18, "bold"))
        title_label.pack(pady=(0, 20))
        
        # 1. إطار الفلاتر
        self.create_filters_frame(main_frame)
        
        # 2. إطار النتائج
        self.create_results_frame(main_frame)
        
        # 3. إطار الإحصائيات
        self.create_stats_frame(main_frame)
    
    def create_filters_frame(self, parent):
        """إنشاء إطار الفلاتر"""
        filters_frame = ttk.LabelFrame(parent, text="🎯 الفلاتر", padding="15")
        filters_frame.pack(fill=tk.X, pady=(0, 15))
        
        # الصف الأول: فلاتر التاريخ
        date_frame = ttk.Frame(filters_frame)
        date_frame.pack(fill=tk.X, pady=(0, 15))
        
        # من تاريخ مع أيقونة تقويم
        from_date_container = ttk.Frame(date_frame)
        from_date_container.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(from_date_container, text="من تاريخ:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(0, 5))
        
        from_entry_frame = ttk.Frame(from_date_container)
        from_entry_frame.pack(side=tk.LEFT)
        
        self.date_from_entry = ttk.Entry(from_entry_frame, textvariable=self.filter_vars['date_from'], 
                                       width=12, font=("Arial", 10))
        self.date_from_entry.pack(side=tk.LEFT, padx=(0, 2))
        self.date_from_entry.bind('<KeyRelease>', lambda e: self.on_filter_change())
        self.date_from_entry.bind('<FocusOut>', lambda e: self.on_filter_change())
        
        # أيقونة تقويم للتاريخ الأول
        from_cal_btn = ttk.Button(from_entry_frame, text="📅", width=3,
                                 command=lambda: self.show_date_picker('from'))
        from_cal_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Label(from_date_container, text="(YYYY-MM-DD)", font=("Arial", 8)).pack(side=tk.LEFT)
        
        # إلى تاريخ مع أيقونة تقويم
        to_date_container = ttk.Frame(date_frame)
        to_date_container.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(to_date_container, text="إلى تاريخ:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(0, 5))
        
        to_entry_frame = ttk.Frame(to_date_container)
        to_entry_frame.pack(side=tk.LEFT)
        
        self.date_to_entry = ttk.Entry(to_entry_frame, textvariable=self.filter_vars['date_to'], 
                                     width=12, font=("Arial", 10))
        self.date_to_entry.pack(side=tk.LEFT, padx=(0, 2))
        self.date_to_entry.bind('<KeyRelease>', lambda e: self.on_filter_change())
        self.date_to_entry.bind('<FocusOut>', lambda e: self.on_filter_change())
        
        # أيقونة تقويم للتاريخ الثاني
        to_cal_btn = ttk.Button(to_entry_frame, text="📅", width=3,
                               command=lambda: self.show_date_picker('to'))
        to_cal_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Label(to_date_container, text="(YYYY-MM-DD)", font=("Arial", 8)).pack(side=tk.LEFT)
        
        # أزرار تاريخ سريعة مع أيقونات
        quick_date_frame = ttk.Frame(date_frame)
        quick_date_frame.pack(side=tk.LEFT, padx=(20, 0))
        
        ttk.Button(quick_date_frame, text="📅 اليوم", 
                  command=lambda: self.set_date_range('today')).pack(side=tk.LEFT, padx=2)
        ttk.Button(quick_date_frame, text="📊 أسبوع", 
                  command=lambda: self.set_date_range('week')).pack(side=tk.LEFT, padx=2)
        ttk.Button(quick_date_frame, text="🗓️ شهر", 
                  command=lambda: self.set_date_range('month')).pack(side=tk.LEFT, padx=2)
        ttk.Button(quick_date_frame, text="🗑️ مسح التواريخ", 
                  command=self.clear_dates).pack(side=tk.LEFT, padx=2)
        
        # إنشاء فلاتر العناصر والتصنيفات
        self.create_filter_widgets(filters_frame)
    
    def on_filter_change(self):
        """معالج تغيير الفلاتر - تطبيق تلقائي بعد تأخير قصير"""
        # إلغاء أي تطبيق مؤجل سابق
        if hasattr(self, '_filter_timer'):
            self.window.after_cancel(self._filter_timer)
        
        # تطبيق الفلاتر بعد 500 مللي ثانية من آخر تغيير
        self._filter_timer = self.window.after(500, self.apply_filters)
    
    def create_filter_widgets(self, filters_frame):
        """إنشاء عناصر الفلاتر"""
        # الصف الثاني: فلاتر البيانات
        data_frame = ttk.Frame(filters_frame)
        data_frame.pack(fill=tk.X, pady=(0, 15))
        
        # الصف الأول من الفلاتر: القوائم المنسدلة
        combo_frame = ttk.Frame(data_frame)
        combo_frame.pack(fill=tk.X, pady=(0, 10))
        
        # فلتر العنصر (قائمة منسدلة)
        ttk.Label(combo_frame, text="اختيار العنصر:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(0, 5))
        self.item_combobox = ttk.Combobox(combo_frame, textvariable=self.filter_vars['item_name'], 
                                         width=20, state="readonly", font=("Arial", 10))
        self.item_combobox.pack(side=tk.LEFT, padx=(0, 15))
        self.item_combobox.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())
        
        # فلتر التصنيف (قائمة منسدلة)
        ttk.Label(combo_frame, text="اختيار التصنيف:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(0, 5))
        self.category_combobox = ttk.Combobox(combo_frame, textvariable=self.filter_vars['category'], 
                                            width=20, state="readonly", font=("Arial", 10))
        self.category_combobox.pack(side=tk.LEFT, padx=(0, 15))
        self.category_combobox.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())
        
        # فلتر المشروع (قائمة منسدلة)
        ttk.Label(combo_frame, text="المشروع:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(0, 5))
        self.project_combobox = ttk.Combobox(combo_frame, textvariable=self.filter_vars['project_id'], 
                                           width=15, state="readonly", font=("Arial", 10))
        self.project_combobox.pack(side=tk.LEFT, padx=(0, 15))
        self.project_combobox.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())
        
        # الصف الثاني من الفلاتر: البحث النصي
        search_frame = ttk.Frame(data_frame)
        search_frame.pack(fill=tk.X)
        
        # بحث نصي للعنصر
        ttk.Label(search_frame, text="🔍 بحث في العناصر:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(0, 5))
        self.item_search_var = tk.StringVar()
        self.item_search_entry = ttk.Entry(search_frame, textvariable=self.item_search_var, 
                                          width=20, font=("Arial", 10))
        self.item_search_entry.pack(side=tk.LEFT, padx=(0, 15))
        self.item_search_entry.bind('<KeyRelease>', lambda e: self.on_filter_change())
        
        # بحث نصي للتصنيف
        ttk.Label(search_frame, text="🔍 بحث في التصنيفات:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(0, 5))
        self.category_search_var = tk.StringVar()
        self.category_search_entry = ttk.Entry(search_frame, textvariable=self.category_search_var, 
                                              width=20, font=("Arial", 10))
        self.category_search_entry.pack(side=tk.LEFT, padx=(0, 15))
        self.category_search_entry.bind('<KeyRelease>', lambda e: self.on_filter_change())
        
        # الصف الثالث: أزرار التحكم
        control_frame = ttk.Frame(filters_frame)
        control_frame.pack(fill=tk.X)
        
        # أزرار رئيسية مع تنسيق محسن
        search_btn = ttk.Button(control_frame, text="🔍 بحث", command=self.apply_filters, width=15)
        search_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        ttk.Button(control_frame, text="🗑️ مسح الفلاتر", 
                  command=self.clear_filters, width=15).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(control_frame, text="🔄 تحديث البيانات", 
                  command=self.refresh_data, width=15).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(control_frame, text="📤 تصدير CSV", 
                  command=self.export_results, width=15).pack(side=tk.LEFT, padx=5, pady=5)
    
    def create_results_frame(self, parent):
        """إنشاء إطار النتائج"""
        results_frame = ttk.LabelFrame(parent, text="📊 النتائج", padding="15")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # إنشاء الجدول مع إمكانية الفرز
        columns = ("العنصر", "التصنيف", "النوع", "الكمية", "التاريخ", "التفاصيل")
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=18)
        
        # تعيين عناوين الأعمدة مع معالجات الفرز
        column_widths = {
            "العنصر": 200,
            "التصنيف": 150,
            "النوع": 120,
            "الكمية": 100,
            "التاريخ": 150,
            "التفاصيل": 300
        }
        
        for col in columns:
            self.results_tree.heading(col, text=col, anchor=tk.CENTER, 
                                    command=lambda c=col: self.sort_results(c))
            self.results_tree.column(col, width=column_widths.get(col, 120), anchor=tk.CENTER)
        
        # متغير لتتبع الفرز
        self.sort_column = None
        self.sort_reverse = False
        
        # أشرطة التمرير
        v_scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        h_scrollbar = ttk.Scrollbar(results_frame, orient=tk.HORIZONTAL, command=self.results_tree.xview)
        self.results_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # ترتيب العناصر
        self.results_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # تكوين التوسع
        results_frame.grid_rowconfigure(0, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)
        
        # عداد النتائج
        self.results_count_label = ttk.Label(results_frame, text="عدد النتائج: 0", 
                                           font=("Arial", 11, "bold"))
        self.results_count_label.grid(row=2, column=0, columnspan=2, pady=(10, 0))
    
    def create_stats_frame(self, parent):
        """إنشاء إطار الإحصائيات"""
        stats_frame = ttk.LabelFrame(parent, text="📈 إحصائيات الكميات", padding="15")
        stats_frame.pack(fill=tk.X)
        
        # تقسيم الإحصائيات على 5 أعمدة
        for i in range(5):
            stats_frame.grid_columnconfigure(i, weight=1)
        
        # إجمالي كمية الدخل
        in_qty_frame = ttk.Frame(stats_frame)
        in_qty_frame.grid(row=0, column=0, padx=10, pady=5)
        ttk.Label(in_qty_frame, text="📈 إجمالي الدخل", font=("Arial", 10, "bold")).pack()
        self.total_in_qty_label = ttk.Label(in_qty_frame, text="0", font=("Arial", 14), foreground="green")
        self.total_in_qty_label.pack()
        
        # إجمالي كمية الخرج
        out_qty_frame = ttk.Frame(stats_frame)
        out_qty_frame.grid(row=0, column=1, padx=10, pady=5)
        ttk.Label(out_qty_frame, text="📉 إجمالي الخرج", font=("Arial", 10, "bold")).pack()
        self.total_out_qty_label = ttk.Label(out_qty_frame, text="0", font=("Arial", 14), foreground="red")
        self.total_out_qty_label.pack()
        
        # الكمية الباقية
        remaining_frame = ttk.Frame(stats_frame)
        remaining_frame.grid(row=0, column=2, padx=10, pady=5)
        ttk.Label(remaining_frame, text="💰 الكمية الباقية", font=("Arial", 10, "bold")).pack()
        self.remaining_qty_label = ttk.Label(remaining_frame, text="0", font=("Arial", 14), foreground="blue")
        self.remaining_qty_label.pack()
        
        # عدد عمليات الإدخال
        in_count_frame = ttk.Frame(stats_frame)
        in_count_frame.grid(row=0, column=3, padx=10, pady=5)
        ttk.Label(in_count_frame, text="🔢 عدد الإدخال", font=("Arial", 10, "bold")).pack()
        self.in_count_label = ttk.Label(in_count_frame, text="0", font=("Arial", 14), foreground="darkgreen")
        self.in_count_label.pack()
        
        # عدد عمليات الإخراج
        out_count_frame = ttk.Frame(stats_frame)
        out_count_frame.grid(row=0, column=4, padx=10, pady=5)
        ttk.Label(out_count_frame, text="🔢 عدد الإخراج", font=("Arial", 10, "bold")).pack()
        self.out_count_label = ttk.Label(out_count_frame, text="0", font=("Arial", 14), foreground="darkred")
        self.out_count_label.pack()
        
        # الصف الثاني: الفترة الزمنية
        period_frame = ttk.Frame(stats_frame)
        period_frame.grid(row=1, column=0, columnspan=5, pady=(10, 0))
        ttk.Label(period_frame, text="📅 الفترة الزمنية:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(0, 10))
        self.period_label = ttk.Label(period_frame, text="غير محددة", font=("Arial", 10), foreground="purple")
        self.period_label.pack(side=tk.LEFT)
    
    def show_date_picker(self, date_type):
        """عرض نافذة اختيار التاريخ بتقويم بسيط"""
        try:
            # نافذة مخصصة لاختيار التاريخ
            date_window = tk.Toplevel(self.window)
            date_window.title("📅 اختيار التاريخ")
            date_window.geometry("400x500")
            date_window.transient(self.window)
            date_window.grab_set()
            
            # توسيط النافذة
            x = self.window.winfo_x() + (self.window.winfo_width() // 2) - 200
            y = self.window.winfo_y() + (self.window.winfo_height() // 2) - 250
            date_window.geometry(f"+{x}+{y}")
            
            # العنوان
            title_text = "اختيار تاريخ البداية" if date_type == 'from' else "اختيار تاريخ النهاية"
            ttk.Label(date_window, text=title_text, font=("Arial", 14, "bold")).pack(pady=10)
            
            # التاريخ الحالي
            current_date = datetime.now()
            selected_year = tk.IntVar(value=current_date.year)
            selected_month = tk.IntVar(value=current_date.month)
            selected_day = tk.IntVar(value=current_date.day)
            
            # إطار اختيار السنة والشهر
            top_frame = ttk.Frame(date_window)
            top_frame.pack(pady=10)
            
            # السنة
            ttk.Label(top_frame, text="السنة:", font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=5)
            year_spinbox = ttk.Spinbox(top_frame, from_=2020, to=2030, 
                                     textvariable=selected_year, width=8)
            year_spinbox.pack(side=tk.LEFT, padx=5)
            
            # الشهر
            ttk.Label(top_frame, text="الشهر:", font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=5)
            months = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو",
                     "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]
            month_combo = ttk.Combobox(top_frame, values=months, state="readonly", width=10)
            month_combo.set(months[current_date.month - 1])
            month_combo.pack(side=tk.LEFT, padx=5)
            
            # إطار التقويم
            cal_frame = ttk.LabelFrame(date_window, text="اختر اليوم", padding="10")
            cal_frame.pack(pady=20, padx=20, fill="both", expand=True)
            
            # متغير لحفظ اليوم المختار
            selected_day_button = None
            day_buttons = {}
            
            def update_calendar():
                """تحديث التقويم حسب السنة والشهر المختارين"""
                nonlocal selected_day_button, day_buttons
                
                # مسح التقويم السابق
                for widget in cal_frame.winfo_children():
                    widget.destroy()
                day_buttons.clear()
                selected_day_button = None
                
                year = selected_year.get()
                month_name = month_combo.get()
                month = months.index(month_name) + 1
                
                # عرض عناوين الأيام
                days_header = ["الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"]
                for i, day_name in enumerate(days_header):
                    ttk.Label(cal_frame, text=day_name, font=("Arial", 9, "bold")).grid(
                        row=0, column=i, padx=2, pady=2, sticky="nsew")
                
                # الحصول على تفاصيل الشهر
                import calendar
                cal = calendar.Calendar(firstweekday=6)  # بداية الأسبوع الأحد
                month_days = cal.monthdayscalendar(year, month)
                
                def select_day(day):
                    """اختيار يوم معين"""
                    nonlocal selected_day_button
                    
                    # إعادة تعيين لون الزر السابق
                    if selected_day_button:
                        selected_day_button.configure(style="TButton")
                    
                    # تعيين اليوم الجديد
                    selected_day.set(day)
                    selected_day_button = day_buttons[day]
                    selected_day_button.configure(style="Accent.TButton")
                
                # عرض أيام الشهر
                for week_num, week in enumerate(month_days, 1):
                    for day_num, day in enumerate(week):
                        if day == 0:  # يوم فارغ
                            continue
                        
                        btn = ttk.Button(cal_frame, text=str(day), width=4,
                                       command=lambda d=day: select_day(d))
                        btn.grid(row=week_num, column=day_num, padx=1, pady=1, sticky="nsew")
                        day_buttons[day] = btn
                        
                        # تحديد اليوم الحالي كافتراضي
                        if day == current_date.day and month == current_date.month and year == current_date.year:
                            select_day(day)
                
                # جعل الأعمدة قابلة للتوسع
                for i in range(7):
                    cal_frame.grid_columnconfigure(i, weight=1)
            
            # ربط تغيير السنة والشهر بتحديث التقويم
            year_spinbox.configure(command=update_calendar)
            month_combo.bind("<<ComboboxSelected>>", lambda e: update_calendar())
            
            # تحديث التقويم الأولي
            update_calendar()
            
            # أزرار سريعة
            quick_frame = ttk.Frame(date_window)
            quick_frame.pack(pady=10)
            
            def set_today():
                today = datetime.now()
                selected_year.set(today.year)
                selected_month.set(today.month)
                month_combo.set(months[today.month - 1])
                update_calendar()
                if today.day in day_buttons:
                    day_buttons[today.day].invoke()
            
            def set_yesterday():
                yesterday = datetime.now() - timedelta(days=1)
                selected_year.set(yesterday.year)
                selected_month.set(yesterday.month)
                month_combo.set(months[yesterday.month - 1])
                update_calendar()
                if yesterday.day in day_buttons:
                    day_buttons[yesterday.day].invoke()
            
            ttk.Button(quick_frame, text="📅 اليوم", command=set_today).pack(side=tk.LEFT, padx=5)
            ttk.Button(quick_frame, text="📆 أمس", command=set_yesterday).pack(side=tk.LEFT, padx=5)
            
            # أزرار التحكم
            button_frame = ttk.Frame(date_window)
            button_frame.pack(pady=20)
            
            def confirm_date():
                try:
                    year = selected_year.get()
                    month_name = month_combo.get()
                    month = months.index(month_name) + 1
                    day = selected_day.get()
                    
                    selected_date = datetime(year, month, day)
                    date_str = selected_date.strftime("%Y-%m-%d")
                    
                    if date_type == 'from':
                        self.filter_vars['date_from'].set(date_str)
                        print(f"📅 تم تعيين تاريخ البداية: {date_str}")
                    else:
                        self.filter_vars['date_to'].set(date_str)
                        print(f"📅 تم تعيين تاريخ النهاية: {date_str}")
                    
                    date_window.destroy()
                    
                    # تطبيق الفلاتر تلقائياً
                    self.apply_filters()
                    
                except Exception as e:
                    messagebox.showerror("خطأ", f"تاريخ غير صحيح: {e}")
            
            ttk.Button(button_frame, text="✅ تأكيد", command=confirm_date).pack(side=tk.LEFT, padx=10)
            ttk.Button(button_frame, text="❌ إلغاء", command=date_window.destroy).pack(side=tk.LEFT, padx=10)
            
        except Exception as e:
            print(f"❌ خطأ في عرض منتقي التاريخ: {e}")
            messagebox.showerror("خطأ", f"فشل في عرض منتقي التاريخ: {e}")
    
    def set_date_range(self, range_type):
        """تعيين نطاق تاريخ محدد مسبقاً"""
        today = datetime.now()
        
        if range_type == 'today':
            date_str = today.strftime("%Y-%m-%d")
            self.filter_vars['date_from'].set(date_str)
            self.filter_vars['date_to'].set(date_str)
            print(f"📅 تم تعيين اليوم: {date_str}")
            self.apply_filters()  # تطبيق تلقائي
        
        elif range_type == 'week':
            week_start = today - timedelta(days=today.weekday())
            week_end = week_start + timedelta(days=6)
            self.filter_vars['date_from'].set(week_start.strftime("%Y-%m-%d"))
            self.filter_vars['date_to'].set(week_end.strftime("%Y-%m-%d"))
            print(f"📅 تم تعيين الأسبوع: {week_start.strftime('%Y-%m-%d')} - {week_end.strftime('%Y-%m-%d')}")
            self.apply_filters()  # تطبيق تلقائي
        
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
            self.apply_filters()  # تطبيق تلقائي
    
    def clear_dates(self):
        """مسح تواريخ الفلترة"""
        self.filter_vars['date_from'].set("")
        self.filter_vars['date_to'].set("")
        print("📅 تم مسح فلاتر التاريخ")
        self.apply_filters()  # تطبيق تلقائي
    
    def clear_filters(self):
        """مسح جميع الفلاتر"""
        self.clear_dates()
        self.filter_vars['item_name'].set("جميع العناصر")
        self.filter_vars['category'].set("جميع التصنيفات")
        # مسح فلاتر البحث النصي
        if hasattr(self, 'item_search_var'):
            self.item_search_var.set("")
        if hasattr(self, 'category_search_var'):
            self.category_search_var.set("")
        print("🗑️ تم مسح جميع الفلاتر")
        self.apply_filters()
    
    def refresh_data(self):
        """تحديث البيانات من Google Sheets"""
        print("🔄 تحديث البيانات...")
        self.load_data()
    
    def export_results(self):
        """تصدير النتائج إلى ملف CSV"""
        if not self.filtered_results:
            messagebox.showwarning("تحذير", "لا توجد نتائج للتصدير")
            return
        
        try:
            from tkinter import filedialog
            import csv
            
            # طلب مكان حفظ الملف
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="حفظ النتائج كملف CSV"
            )
            
            if not file_path:
                return
            
            # كتابة البيانات في الملف
            with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.writer(csvfile)
                
                # كتابة العناوين
                headers = ["العنصر", "التصنيف", "النوع", "الكمية", "التاريخ", "التفاصيل"]
                writer.writerow(headers)
                
                # كتابة البيانات
                for result in self.filtered_results:
                    row = [
                        result['item_name'],
                        result['category'],
                        result['type'],
                        result['quantity'],
                        result['date'],
                        result['details']
                    ]
                    writer.writerow(row)
            
            messagebox.showinfo("تم التصدير", 
                              f"تم تصدير {len(self.filtered_results)} نتيجة إلى:\n{file_path}")
            print(f"📤 تم تصدير {len(self.filtered_results)} نتيجة إلى: {file_path}")
            
        except Exception as e:
            print(f"❌ خطأ في التصدير: {e}")
            messagebox.showerror("خطأ", f"فشل في تصدير النتائج:\n{e}")
    
    def load_data(self):
        """تحميل البيانات من Google Sheets"""
        try:
            print("📊 تحميل البيانات...")
            print(f"👤 التحقق من معلومات المستخدم: {self.current_user}")
            if self.current_user:
                print(f"   - اسم المستخدم: {self.current_user.get('username', 'غير محدد')}")
                print(f"   - نوع المستخدم: {self.current_user.get('user_type', 'غير محدد')}")
                print(f"   - مشروع المستخدم: {self.current_user.get('project_id', 'غير محدد')}")
            
            # تحميل البيانات من المخزون
            if hasattr(self.sheets_manager, 'get_all_items_raw'):
                self.all_items = self.sheets_manager.get_all_items_raw()
                print(f"📦 تم تحميل {len(self.all_items)} عنصر من المخزون")
            else:
                self.all_items = []
                print("⚠️ لا يمكن تحميل بيانات المخزون")
            
            # تحميل سجل النشاط
            if hasattr(self.sheets_manager, 'get_activity_log'):
                self.activity_log = self.sheets_manager.get_activity_log()
                print(f"📋 تم تحميل {len(self.activity_log)} إدخال من سجل النشاط")
            else:
                self.activity_log = []
                print("⚠️ لا يمكن تحميل سجل النشاط")
            
            # تحديث خيارات الفلاتر
            self.update_filter_options()
            
            # إعداد فلتر المشروع للمستخدمين العاديين (بعد تحديث القوائم)
            self.setup_project_filter()
            
            # تطبيق الفلاتر لعرض جميع البيانات
            self.apply_filters()
            
            print("✅ تم تحميل البيانات بنجاح")
            
        except Exception as e:
            print(f"❌ خطأ في تحميل البيانات: {e}")
            messagebox.showerror("خطأ", f"فشل في تحميل البيانات:\n{e}")
    
    def setup_project_filter(self):
        """إعداد فلتر المشروع للمستخدمين العاديين"""
        try:
            print(f"🔧 إعداد فلتر المشروع...")
            print(f"👤 المستخدم الحالي: {self.current_user}")
            
            if self.current_user and self.current_user.get('user_type') == 'user':
                user_project_id = self.current_user.get('project_id', '')
                print(f"📋 مشروع المستخدم: '{user_project_id}'")
                
                if user_project_id:
                    print(f"👤 ضبط فلتر المشروع للمستخدم العادي: {user_project_id}")
                    
                    # التأكد من وجود المشروع في القائمة
                    if hasattr(self, 'project_combobox'):
                        current_values = list(self.project_combobox['values'])
                        print(f"📝 القيم الحالية في قائمة المشاريع: {current_values}")
                        
                        # إضافة المشروع إلى القائمة إذا لم يكن موجوداً
                        if user_project_id not in current_values:
                            current_values.append(user_project_id)
                            self.project_combobox['values'] = current_values
                            print(f"➕ تم إضافة المشروع {user_project_id} إلى القائمة")
                        
                        # تعيين المشروع في الفلتر
                        self.filter_vars['project_id'].set(user_project_id)
                        print(f"✅ تم تعيين فلتر المشروع إلى: {user_project_id}")
                        
                        # تعطيل تعديل فلتر المشروع
                        self.project_combobox.config(state="disabled")
                        
                        # إضافة تسمية توضيحية (فقط إذا لم تكن موجودة)
                        if not hasattr(self, 'project_restriction_label'):
                            self.project_restriction_label = ttk.Label(self.project_combobox.master, 
                                                     text="(مُقيد للمستخدم)", 
                                                     font=("Arial", 8), 
                                                     foreground="gray")
                            self.project_restriction_label.pack(side=tk.LEFT, padx=(5, 0))
                        
                        print(f"🔒 تم تعطيل فلتر المشروع للمستخدم العادي")
                    else:
                        print("❌ لم يتم العثور على project_combobox")
                else:
                    print("⚠️ المستخدم العادي ليس لديه مشروع محدد")
            else:
                print("👨‍💼 مدير - فلتر المشروع متاح للتعديل")
        except Exception as e:
            print(f"❌ خطأ في إعداد فلتر المشروع: {e}")
            import traceback
            traceback.print_exc()
    
    def update_filter_options(self):
        """تحديث خيارات الفلاتر"""
        items = set(["جميع العناصر"])
        categories = set(["جميع التصنيفات"])
        projects = set(["جميع المشاريع"])
        
        # من بيانات المخزون
        for item in self.all_items:
            if len(item) >= 4:
                if item[0]:  # اسم العنصر
                    clean_item = item[0].strip() if item[0] else ""
                    if clean_item:  # تأكد من أن العنصر غير فارغ بعد التنظيف
                        items.add(clean_item)
                if item[1]:  # التصنيف
                    clean_category = item[1].strip() if item[1] else ""
                    if clean_category:  # تأكد من أن التصنيف غير فارغ بعد التنظيف
                        categories.add(clean_category)
                if item[3]:  # المشروع
                    clean_project = item[3].strip() if item[3] else ""
                    if clean_project:
                        projects.add(clean_project)
        
        # من سجل النشاط
        for log in self.activity_log:
            if len(log) >= 3:
                if log[2]:  # اسم العنصر
                    clean_item = log[2].strip() if log[2] else ""
                    if clean_item:
                        items.add(clean_item)
                # محاولة استخراج التصنيف من المخزون
                item_category = self.get_item_category(log[2])
                if item_category:
                    clean_category = item_category.strip() if item_category else ""
                    if clean_category:
                        categories.add(clean_category)
        
        # تحديث القوائم (فقط إذا كانت العناصر موجودة)
        if hasattr(self, 'item_combobox'):
            self.item_combobox['values'] = sorted(list(items))
        if hasattr(self, 'category_combobox'):
            self.category_combobox['values'] = sorted(list(categories))
        if hasattr(self, 'project_combobox'):
            self.project_combobox['values'] = sorted(list(projects))
        
        print(f"📋 تم تحديث الفلاتر: {len(items)-1} عنصر، {len(categories)-1} تصنيف، {len(projects)-1} مشروع")
    
    def get_item_category(self, item_name):
        """الحصول على تصنيف العنصر من بيانات المخزون"""
        if not item_name:
            return ""
        
        for item in self.all_items:
            if len(item) >= 2 and item[0] and item[0].strip().lower() == item_name.strip().lower():
                return item[1] if item[1] else ""
        return ""
    
    def extract_project_from_details(self, details):
        """استخراج رقم المشروع من التفاصيل"""
        if not details:
            return ""
        
        # البحث عن نمط PRJ_XXX في التفاصيل
        import re
        project_match = re.search(r'PRJ_\d+', details)
        if project_match:
            return project_match.group()
        
        return ""
    
    def apply_filters(self):
        """تطبيق الفلاتر وعرض النتائج"""
        try:
            print("🔍 تطبيق الفلاتر...")
            
            # مسح النتائج السابقة
            for item in self.results_tree.get_children():
                self.results_tree.delete(item)
            
            self.filtered_results = []
            
            # الحصول على قيم الفلاتر
            filter_item = self.filter_vars['item_name'].get()
            filter_category = self.filter_vars['category'].get()
            filter_project = self.filter_vars['project_id'].get()
            filter_date_from = self.filter_vars['date_from'].get()
            filter_date_to = self.filter_vars['date_to'].get()
            
            # الحصول على قيم البحث النصي
            item_search = self.item_search_var.get() if hasattr(self, 'item_search_var') else ""
            category_search = self.category_search_var.get() if hasattr(self, 'category_search_var') else ""
            
            print(f"🎯 الفلاتر المطبقة:")
            print(f"   - العنصر: '{filter_item}'")
            print(f"   - التصنيف: '{filter_category}'")
            print(f"   - المشروع: '{filter_project}'")
            print(f"   - بحث العنصر: '{item_search}'")
            print(f"   - بحث التصنيف: '{category_search}'")
            print(f"   - من تاريخ: '{filter_date_from}'")
            print(f"   - إلى تاريخ: '{filter_date_to}'")
            
            # عداد للتتبع
            total_items_checked = 0
            total_activity_checked = 0
            items_passed_filter = 0
            activity_passed_filter = 0
            
            # فلترة بيانات المخزون الحالي
            for item in self.all_items:
                total_items_checked += 1
                if len(item) >= 5:
                    item_name = item[0] if item[0] else ""
                    category = item[1] if item[1] else ""
                    quantity = item[2] if item[2] else "0"
                    project = item[3] if item[3] else ""
                    date = item[4] if item[4] else ""
                    
                    if self.matches_filters(item_name, category, project, date, filter_item, filter_category, 
                                           filter_project, filter_date_from, filter_date_to, item_search, category_search):
                        items_passed_filter += 1
                        self.filtered_results.append({
                            'item_name': item_name,
                            'category': category,
                            'type': 'مخزون حالي',
                            'quantity': quantity,
                            'date': date,
                            'details': f'المشروع: {project}'
                        })
            
            # فلترة سجل النشاط
            for log in self.activity_log:
                total_activity_checked += 1
                if len(log) >= 6:
                    date = log[0] if log[0] else ""
                    action = log[1] if log[1] else ""
                    item_name = log[2] if log[2] else ""
                    quantity = log[3] if log[3] else ""
                    recipient = log[4] if log[4] else ""
                    details = log[5] if log[5] else ""
                    
                    # الحصول على التصنيف والمشروع
                    category = self.get_item_category(item_name)
                    project = self.extract_project_from_details(details)
                    
                    # تحديد نوع العملية
                    operation_type = "إدخال" if action in ["إضافة", "تعديل"] else "إخراج" if action == "إخراج" else action
                    
                    if self.matches_filters(item_name, category, project, date, filter_item, filter_category, 
                                           filter_project, filter_date_from, filter_date_to, item_search, category_search):
                        activity_passed_filter += 1
                        self.filtered_results.append({
                            'item_name': item_name,
                            'category': category,
                            'type': operation_type,
                            'quantity': quantity,
                            'date': date,
                            'details': details
                        })
            
            # عرض النتائج في الجدول وحساب الإحصائيات
            total_in_qty = 0      # إجمالي كمية الدخل
            total_out_qty = 0     # إجمالي كمية الخرج
            in_operations = 0     # عدد عمليات الإدخال
            out_operations = 0    # عدد عمليات الإخراج
            
            for result in self.filtered_results:
                values = (
                    result['item_name'],
                    result['category'],
                    result['type'],
                    result['quantity'],
                    result['date'],
                    result['details']
                )
                self.results_tree.insert("", "end", values=values)
                
                # حساب الإحصائيات
                try:
                    quantity = float(result['quantity']) if result['quantity'] and result['quantity'].replace('.', '').replace('-', '').isdigit() else 0
                    
                    if result['type'] == 'إدخال' or result['type'] == 'إضافة':
                        total_in_qty += quantity
                        in_operations += 1
                    elif result['type'] == 'إخراج':
                        total_out_qty += quantity
                        out_operations += 1
                except ValueError:
                    print(f"⚠️ لا يمكن تحويل الكمية: {result['quantity']}")
            
            # حساب الكمية الباقية (الدخل - الخرج)
            remaining_qty = total_in_qty - total_out_qty
            
            # تحديث العدادات
            total_results = len(self.filtered_results)
            self.results_count_label.config(text=f"عدد النتائج: {total_results}")
            
            # تحديث إحصائيات الكميات
            self.total_in_qty_label.config(text=f"{total_in_qty:.0f}")
            self.total_out_qty_label.config(text=f"{total_out_qty:.0f}")
            self.remaining_qty_label.config(text=f"{remaining_qty:.0f}")
            self.in_count_label.config(text=str(in_operations))
            self.out_count_label.config(text=str(out_operations))
            
            # تلوين الكمية الباقية حسب القيمة
            if remaining_qty > 0:
                self.remaining_qty_label.config(foreground="green")
            elif remaining_qty < 0:
                self.remaining_qty_label.config(foreground="red")
            else:
                self.remaining_qty_label.config(foreground="blue")
            
            # تحديث الفترة الزمنية
            if filter_date_from and filter_date_to:
                self.period_label.config(text=f"{filter_date_from} إلى {filter_date_to}")
            elif filter_date_from:
                self.period_label.config(text=f"من {filter_date_from}")
            elif filter_date_to:
                self.period_label.config(text=f"حتى {filter_date_to}")
            else:
                self.period_label.config(text="جميع الفترات")
            
            print(f"✅ نتائج البحث:")
            print(f"   - تم فحص {total_items_checked} عنصر من المخزون")
            print(f"   - تم فحص {total_activity_checked} إدخال من سجل النشاط") 
            print(f"   - مر {items_passed_filter} عنصر مخزون عبر الفلاتر")
            print(f"   - مر {activity_passed_filter} إدخال نشاط عبر الفلاتر")
            print(f"   - إجمالي النتائج: {total_results}")
            
        except Exception as e:
            print(f"❌ خطأ في تطبيق الفلاتر: {e}")
            messagebox.showerror("خطأ", f"حدث خطأ في البحث:\n{e}")
    
    def matches_filters(self, item_name, category, project, date, filter_item, filter_category, filter_project, filter_date_from, filter_date_to, item_search="", category_search=""):
        """فحص ما إذا كان العنصر يطابق الفلاتر"""
        
        # تسجيل تفصيلي لأول 3 عناصر للتشخيص
        debug_mode = len(self.filtered_results) < 3
        
        if debug_mode:
            print(f"🔍 فحص العنصر: '{item_name}', التصنيف: '{category}', المشروع: '{project}', التاريخ: '{date}'")
        
        # فلتر العنصر من القائمة المنسدلة
        if filter_item and filter_item != "جميع العناصر":
            if not item_name:
                if debug_mode: print(f"   ❌ فشل فلتر العنصر: اسم العنصر فارغ")
                return False
            item_name_clean = item_name.strip().lower()
            filter_item_clean = filter_item.strip().lower()
            if item_name_clean != filter_item_clean:  # مطابقة تامة للقائمة المنسدلة
                if debug_mode: print(f"   ❌ فشل فلتر العنصر: '{filter_item_clean}' != '{item_name_clean}'")
                return False
            else:
                if debug_mode: print(f"   ✅ نجح فلتر العنصر (قائمة)")
        
        # فلتر البحث النصي للعنصر
        if item_search and item_search.strip():
            if not item_name:
                if debug_mode: print(f"   ❌ فشل بحث العنصر: اسم العنصر فارغ")
                return False
            item_name_clean = item_name.strip().lower()
            item_search_clean = item_search.strip().lower()
            if item_search_clean not in item_name_clean:
                if debug_mode: print(f"   ❌ فشل بحث العنصر: '{item_search_clean}' غير موجود في '{item_name_clean}'")
                return False
            else:
                if debug_mode: print(f"   ✅ نجح بحث العنصر")
        
        # فلتر التصنيف من القائمة المنسدلة
        if filter_category and filter_category != "جميع التصنيفات":
            if not category:
                if debug_mode: print(f"   ❌ فشل فلتر التصنيف: التصنيف فارغ")
                return False
            category_clean = category.strip().lower()
            filter_category_clean = filter_category.strip().lower()
            if category_clean != filter_category_clean:
                if debug_mode: print(f"   ❌ فشل فلتر التصنيف: '{category_clean}' != '{filter_category_clean}'")
                return False
            else:
                if debug_mode: print(f"   ✅ نجح فلتر التصنيف (قائمة)")
        
        # فلتر البحث النصي للتصنيف
        if category_search and category_search.strip():
            if not category:
                if debug_mode: print(f"   ❌ فشل بحث التصنيف: التصنيف فارغ")
                return False
            category_clean = category.strip().lower()
            category_search_clean = category_search.strip().lower()
            if category_search_clean not in category_clean:
                if debug_mode: print(f"   ❌ فشل بحث التصنيف: '{category_search_clean}' غير موجود في '{category_clean}'")
                return False
            else:
                if debug_mode: print(f"   ✅ نجح بحث التصنيف")
        
        # فلتر المشروع
        if filter_project and filter_project != "جميع المشاريع":
            if not project:
                if debug_mode: print(f"   ❌ فشل فلتر المشروع: المشروع فارغ")
                return False
            project_clean = project.strip().lower()
            filter_project_clean = filter_project.strip().lower()
            if project_clean != filter_project_clean:
                if debug_mode: print(f"   ❌ فشل فلتر المشروع: '{project_clean}' != '{filter_project_clean}'")
                return False
            else:
                if debug_mode: print(f"   ✅ نجح فلتر المشروع")
        
        # فلتر التاريخ
        if filter_date_from or filter_date_to:
            if not date:
                if debug_mode: print(f"   ❌ فشل فلتر التاريخ: التاريخ فارغ")
                return False
            
            try:
                # استخراج التاريخ من النص - معالجة أفضل للتنسيقات المختلفة
                date_to_parse = date.strip()
                
                # إذا كان التاريخ يحتوي على وقت، نأخذ الجزء الأول فقط
                if ' ' in date_to_parse:
                    date_part = date_to_parse.split(' ')[0]
                else:
                    date_part = date_to_parse
                
                # محاولة معالجة تنسيقات تاريخ مختلفة
                item_date = None
                date_formats = [
                    "%Y-%m-%d %H:%M:%S",  # 2025-10-21 21:49:02
                    "%Y-%m-%d",           # 2025-10-21
                    "%d/%m/%Y",           # 21/10/2025
                    "%d-%m-%Y",           # 21-10-2025
                    "%Y/%m/%d",           # 2025/10/21
                ]
                
                for date_format in date_formats:
                    try:
                        item_date = datetime.strptime(date_part, date_format)
                        if debug_mode: print(f"   ✅ تم معالجة التاريخ '{date_part}' بتنسيق {date_format}")
                        break
                    except ValueError:
                        continue
                
                if not item_date:
                    if debug_mode: print(f"   ❌ فشل فلتر التاريخ: لا يمكن معالجة '{date_part}'")
                    return False
                
                if filter_date_from:
                    from_date = datetime.strptime(filter_date_from, "%Y-%m-%d")
                    if item_date < from_date:
                        if debug_mode: print(f"   ❌ فشل فلتر التاريخ: {item_date.date()} < {from_date.date()}")
                        return False
                
                if filter_date_to:
                    to_date = datetime.strptime(filter_date_to, "%Y-%m-%d")
                    # إضافة 23:59:59 لليوم الأخير
                    to_date = to_date.replace(hour=23, minute=59, second=59)
                    if item_date > to_date:
                        if debug_mode: print(f"   ❌ فشل فلتر التاريخ: {item_date.date()} > {to_date.date()}")
                        return False
                
                if debug_mode: print(f"   ✅ نجح فلتر التاريخ")
                        
            except Exception as e:
                if debug_mode: print(f"   ❌ خطأ في معالجة التاريخ {date}: {e}")
                return False
        
        if debug_mode: print(f"   ✅ العنصر مطابق لجميع الفلاتر")
        return True
    
    def sort_results(self, column):
        """فرز النتائج حسب العمود المحدد"""
        try:
            # تبديل اتجاه الفرز إذا كان نفس العمود
            if self.sort_column == column:
                self.sort_reverse = not self.sort_reverse
            else:
                self.sort_column = column
                self.sort_reverse = False
            
            # الحصول على البيانات الحالية
            items = []
            for child in self.results_tree.get_children():
                values = self.results_tree.item(child)['values']
                items.append(values)
            
            # تحديد مؤشر العمود
            column_index = {"العنصر": 0, "التصنيف": 1, "النوع": 2, "الكمية": 3, "التاريخ": 4, "التفاصيل": 5}
            col_index = column_index.get(column, 0)
            
            # فرز البيانات
            if column == "الكمية":
                # فرز رقمي للكمية
                items.sort(key=lambda x: float(x[col_index]) if x[col_index].replace('.', '').replace('-', '').isdigit() else 0, 
                          reverse=self.sort_reverse)
            elif column == "التاريخ":
                # فرز التاريخ
                def parse_date(date_str):
                    try:
                        if ' ' in date_str:
                            date_part = date_str.split(' ')[0]
                        else:
                            date_part = date_str
                        return datetime.strptime(date_part, "%Y-%m-%d")
                    except:
                        return datetime.min
                
                items.sort(key=lambda x: parse_date(x[col_index]), reverse=self.sort_reverse)
            else:
                # فرز نصي
                items.sort(key=lambda x: x[col_index].lower(), reverse=self.sort_reverse)
            
            # مسح الجدول وإعادة ملئه
            for child in self.results_tree.get_children():
                self.results_tree.delete(child)
            
            for item in items:
                self.results_tree.insert("", "end", values=item)
            
            # تحديث عنوان العمود لإظهار اتجاه الفرز
            for col in ["العنصر", "التصنيف", "النوع", "الكمية", "التاريخ", "التفاصيل"]:
                if col == column:
                    arrow = " ↓" if self.sort_reverse else " ↑"
                    self.results_tree.heading(col, text=col + arrow)
                else:
                    self.results_tree.heading(col, text=col)
            
            print(f"🔄 تم فرز النتائج حسب {column} ({'تنازلي' if self.sort_reverse else 'تصاعدي'})")
            
        except Exception as e:
            print(f"❌ خطأ في فرز النتائج: {e}")


# دالة للاستخدام من النافذة الرئيسية
def show_filter_search_window(parent, sheets_manager, current_user=None):
    """عرض نافذة البحث باستخدام الفلاتر"""
    return FilterSearchWindow(parent, sheets_manager, current_user)