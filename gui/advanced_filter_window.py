#!/usr/bin/env python3
"""
🔥 نظام الفلاتر المتقدم للمخزون
فلاتر شاملة: التاريخ، العنصر، التصنيف، الكمية الداخلة، الخارجة، المتبقية
"""

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.ttk import Combobox, Treeview
import datetime
from typing import List, Dict, Any, Optional
import re

class AdvancedFilterWindow:
    """نافذة الفلاتر المتقدمة مع جميع الخيارات المطلوبة"""
    
    def __init__(self, parent: tk.Widget, sheets_manager, current_user: Dict[str, Any]):
        self.parent = parent
        self.sheets_manager = sheets_manager
        self.current_user = current_user
        
        # البيانات والفلاتر
        self.all_data = []
        self.filtered_data = []
        
        # متغيرات الفلاتر
        self.date_filter_var = tk.StringVar(value="الكل")
        self.item_filter_var = tk.StringVar(value="الكل")
        self.category_filter_var = tk.StringVar(value="الكل")
        self.project_filter_var = tk.StringVar(value="الكل")
        
        # متغيرات فلاتر الكمية
        self.quantity_min_var = tk.StringVar(value="")
        self.quantity_max_var = tk.StringVar(value="")
        self.quantity_operation_var = tk.StringVar(value="بين")
        
        # إنشاء النافذة
        self.create_window()
        self.load_data()
        self.setup_filters()
        self.setup_bindings()
        
        # تطبيق أولي للفلاتر
        print("🚀 تطبيق الفلاتر الأولي...")
        self.window.after(1500, self.force_apply_filters)
        
    def create_window(self):
        """إنشاء نافذة الفلاتر المتقدمة"""
        
        self.window = tk.Toplevel(self.parent)
        self.window.title("🔍 الفلاتر المتقدمة - نظام المخزون الشامل")
        self.window.geometry("1400x800")
        self.window.configure(bg="#2c3e50")
        
        # منع إغلاق النافذة بالخطأ
        self.window.protocol("WM_DELETE_WINDOW", self.on_window_close)
        
        # الإطار الرئيسي
        main_frame = tk.Frame(self.window, bg="#2c3e50")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # العنوان الرئيسي
        title_frame = tk.Frame(main_frame, bg="#34495e", relief="raised", bd=2)
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        title = tk.Label(
            title_frame,
            text="🔍 نظام الفلاتر المتقدم والشامل",
            font=("Arial", 18, "bold"),
            fg="#f1c40f", bg="#34495e"
        )
        title.pack(pady=15)
        
        # معلومات المستخدم والحالة
        info_frame = tk.Frame(title_frame, bg="#34495e")
        info_frame.pack(pady=(0, 15))
        
        user_info = f"👤 المستخدم: {self.current_user.get('username', 'غير محدد')} | النوع: {self.current_user.get('user_type', 'غير محدد')}"
        self.user_label = tk.Label(
            info_frame,
            text=user_info,
            font=("Arial", 12),
            fg="#bdc3c7", bg="#34495e"
        )
        self.user_label.pack(side=tk.LEFT)
        
        self.status_label = tk.Label(
            info_frame,
            text="📊 جاري تحميل البيانات...",
            font=("Arial", 12, "bold"),
            fg="#e67e22", bg="#34495e"
        )
        self.status_label.pack(side=tk.RIGHT)
        
        # منطقة الفلاتر والنتائج
        content_frame = tk.Frame(main_frame, bg="#2c3e50")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # الفلاتر على اليسار
        filters_frame = tk.LabelFrame(
            content_frame, 
            text="🎛️ الفلاتر والتحكم", 
            font=("Arial", 14, "bold"),
            fg="#3498db", bg="#34495e",
            padx=15, pady=15
        )
        filters_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        
        self.create_filters(filters_frame)
        
        # النتائج على اليمين
        results_frame = tk.LabelFrame(
            content_frame,
            text="📊 النتائج والبيانات",
            font=("Arial", 14, "bold"), 
            fg="#27ae60", bg="#34495e",
            padx=10, pady=10
        )
        results_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.create_results_table(results_frame)
        
    def create_filters(self, parent):
        """إنشاء منطقة الفلاتر"""
        
        # فلتر التاريخ
        date_frame = tk.LabelFrame(parent, text="📅 فلتر التاريخ", bg="#34495e", fg="#e67e22", font=("Arial", 11, "bold"))
        date_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(date_frame, text="تاريخ آخر تحديث:", bg="#34495e", fg="#ecf0f1").pack(anchor=tk.W, padx=5, pady=2)
        self.date_combo = Combobox(date_frame, textvariable=self.date_filter_var, state="readonly")
        self.date_combo.pack(fill=tk.X, padx=5, pady=2)
        
        # فلتر العنصر
        item_frame = tk.LabelFrame(parent, text="📦 فلتر العنصر", bg="#34495e", fg="#e67e22", font=("Arial", 11, "bold"))
        item_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(item_frame, text="اسم العنصر:", bg="#34495e", fg="#ecf0f1").pack(anchor=tk.W, padx=5, pady=2)
        self.item_combo = Combobox(item_frame, textvariable=self.item_filter_var, state="readonly")
        self.item_combo.pack(fill=tk.X, padx=5, pady=2)
        
        # فلتر التصنيف
        category_frame = tk.LabelFrame(parent, text="🏷️ فلتر التصنيف", bg="#34495e", fg="#e67e22", font=("Arial", 11, "bold"))
        category_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(category_frame, text="نوع التصنيف:", bg="#34495e", fg="#ecf0f1").pack(anchor=tk.W, padx=5, pady=2)
        self.category_combo = Combobox(category_frame, textvariable=self.category_filter_var, state="readonly")
        self.category_combo.pack(fill=tk.X, padx=5, pady=2)
        
        # فلتر المشروع
        project_frame = tk.LabelFrame(parent, text="🎯 فلتر المشروع", bg="#34495e", fg="#e67e22", font=("Arial", 11, "bold"))
        project_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(project_frame, text="رقم المشروع:", bg="#34495e", fg="#ecf0f1").pack(anchor=tk.W, padx=5, pady=2)
        self.project_combo = Combobox(project_frame, textvariable=self.project_filter_var, state="readonly")
        self.project_combo.pack(fill=tk.X, padx=5, pady=2)
        
        # فلتر الكمية المتقدم
        quantity_frame = tk.LabelFrame(parent, text="📊 فلتر الكمية المتقدم", bg="#34495e", fg="#e67e22", font=("Arial", 11, "bold"))
        quantity_frame.pack(fill=tk.X, pady=(0, 15))
        
        # نوع العملية
        tk.Label(quantity_frame, text="نوع المقارنة:", bg="#34495e", fg="#ecf0f1").pack(anchor=tk.W, padx=5, pady=2)
        operation_combo = Combobox(quantity_frame, textvariable=self.quantity_operation_var, 
                                 values=["الكل", "يساوي", "أكبر من", "أصغر من", "بين", "أكبر أو يساوي", "أصغر أو يساوي"],
                                 state="readonly")
        operation_combo.pack(fill=tk.X, padx=5, pady=2)
        
        # حقول الكمية
        qty_input_frame = tk.Frame(quantity_frame, bg="#34495e")
        qty_input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(qty_input_frame, text="من:", bg="#34495e", fg="#ecf0f1").pack(side=tk.LEFT)
        qty_min_entry = tk.Entry(qty_input_frame, textvariable=self.quantity_min_var, width=8)
        qty_min_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Label(qty_input_frame, text="إلى:", bg="#34495e", fg="#ecf0f1").pack(side=tk.LEFT, padx=(10, 0))
        qty_max_entry = tk.Entry(qty_input_frame, textvariable=self.quantity_max_var, width=8)
        qty_max_entry.pack(side=tk.LEFT, padx=5)
        
        # أزرار التحكم
        controls_frame = tk.Frame(parent, bg="#34495e")
        controls_frame.pack(fill=tk.X, pady=15)
        
        # الصف الأول من الأزرار
        row1_frame = tk.Frame(controls_frame, bg="#34495e")
        row1_frame.pack(fill=tk.X, pady=(0, 8))
        
        self.apply_btn = tk.Button(
            row1_frame,
            text="✅ تطبيق الفلاتر",
            command=self.force_apply_filters_with_debug,
            bg="#27ae60", fg="white",
            font=("Arial", 11, "bold"),
            relief="flat", cursor="hand2"
        )
        self.apply_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))
        
        clear_btn = tk.Button(
            row1_frame,
            text="🗑️ مسح الفلاتر",
            command=self.clear_filters,
            bg="#e74c3c", fg="white",
            font=("Arial", 11, "bold"),
            relief="flat", cursor="hand2"
        )
        clear_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4)
        
        # الصف الثاني من الأزرار
        row2_frame = tk.Frame(controls_frame, bg="#34495e")
        row2_frame.pack(fill=tk.X, pady=(0, 8))
        
        refresh_btn = tk.Button(
            row2_frame,
            text="🔄 تحديث البيانات",
            command=self.refresh_data,
            bg="#3498db", fg="white",
            font=("Arial", 11, "bold"),
            relief="flat", cursor="hand2"
        )
        refresh_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))
        
        export_btn = tk.Button(
            row2_frame,
            text="💾 تصدير النتائج",
            command=self.export_results,
            bg="#9b59b6", fg="white",
            font=("Arial", 11, "bold"),
            relief="flat", cursor="hand2"
        )
        export_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4)
        
        # إحصائيات سريعة
        stats_frame = tk.LabelFrame(parent, text="📈 إحصائيات سريعة", bg="#34495e", fg="#f39c12", font=("Arial", 11, "bold"))
        stats_frame.pack(fill=tk.X, pady=(15, 0))
        
        self.stats_label = tk.Label(
            stats_frame,
            text="جاري حساب الإحصائيات...",
            bg="#34495e", fg="#ecf0f1",
            font=("Arial", 10),
            justify=tk.LEFT
        )
        self.stats_label.pack(padx=10, pady=10, anchor=tk.W)
        
    def create_results_table(self, parent):
        """إنشاء جدول النتائج"""
        
        # شريط أدوات الجدول
        toolbar_frame = tk.Frame(parent, bg="#34495e")
        toolbar_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.results_info = tk.Label(
            toolbar_frame,
            text="📊 النتائج: جاري التحميل...",
            font=("Arial", 12, "bold"),
            fg="#2ecc71", bg="#34495e"
        )
        self.results_info.pack(side=tk.LEFT)
        
        # زر فرز
        sort_btn = tk.Button(
            toolbar_frame,
            text="🔀 فرز حسب الكمية",
            command=self.sort_by_quantity,
            bg="#34495e", fg="#ecf0f1",
            font=("Arial", 10),
            relief="flat", cursor="hand2"
        )
        sort_btn.pack(side=tk.RIGHT)
        
        # إطار الجدول مع شريط التمرير
        table_frame = tk.Frame(parent, bg="#34495e")
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # إعداد الجدول
        columns = ("العنصر", "التصنيف", "الكمية الابتدائية", "الداخلة", "الخارجة", "المتبقية", "المشروع", "آخر تحديث")
        self.tree = Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # تحديد عناوين الأعمدة
        column_widths = {
            "العنصر": 180, "التصنيف": 120, "الكمية الابتدائية": 100, 
            "الداخلة": 80, "الخارجة": 80, "المتبقية": 80, 
            "المشروع": 100, "آخر تحديث": 120
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
        
        # ألوان الصفوف المتبادلة
        self.tree.tag_configure("oddrow", background="#ecf0f1")
        self.tree.tag_configure("evenrow", background="#ffffff")
        
        # ألوان خاصة للكميات
        self.tree.tag_configure("low_stock", background="#ffebee", foreground="#c62828")  # كمية منخفضة
        self.tree.tag_configure("medium_stock", background="#fff3e0", foreground="#ef6c00")  # كمية متوسطة  
        self.tree.tag_configure("high_stock", background="#e8f5e8", foreground="#2e7d32")  # كمية عالية
        
    def load_data(self):
        """تحميل البيانات من Google Sheets بالطريقة الصحيحة"""
        
        try:
            print("📊 بدء تحميل البيانات من Google Sheets...")
            self.status_label.config(text="📊 جاري تحميل البيانات...")
            self.window.update()
            
            # الحصول على البيانات مباشرة من ورقة العمل
            worksheet = self.sheets_manager.worksheet
            all_values = worksheet.get_all_values()
            
            if not all_values or len(all_values) < 2:
                raise Exception("لا توجد بيانات في ورقة العمل")
            
            # العناوين في الصف الأول
            headers = all_values[0]
            data_rows = all_values[1:]
            
            print(f"📋 عناوين الأعمدة: {headers}")
            print(f"📊 عدد الصفوف: {len(data_rows)}")
            
            # تحويل البيانات للتنسيق المطلوب
            self.all_data = []
            for row in data_rows:
                if len(row) >= len(headers):
                    # إنشاء عنصر بياناتم مع معالجة القيم الفارغة
                    processed_item = {
                        'العنصر': str(row[0]).strip() if len(row) > 0 and row[0] else "",
                        'التصنيف': str(row[1]).strip() if len(row) > 1 and row[1] else "",
                        'الكمية': str(row[2]).strip() if len(row) > 2 and row[2] else "0",
                        'المشروع': str(row[3]).strip() if len(row) > 3 and row[3] else "",
                        'التاريخ': str(row[4]).strip() if len(row) > 4 and row[4] else ""
                    }
                    
                    # إضافة البيانات فقط إذا كان العنصر غير فارغ
                    if processed_item['العنصر']:
                        self.all_data.append(processed_item)
                        print(f"✓ تم تحميل: {processed_item['العنصر']} - {processed_item['التصنيف']} - {processed_item['الكمية']}")
            
            # نسخ البيانات للفلترة
            self.filtered_data = self.all_data.copy()
            
            print(f"✅ تم تحميل {len(self.all_data)} عنصر بنجاح")
            self.status_label.config(text=f"✅ تم تحميل {len(self.all_data)} عنصر")
            
        except Exception as e:
            print(f"❌ خطأ في تحميل البيانات: {e}")
            import traceback
            traceback.print_exc()
            
            self.status_label.config(text="❌ خطأ في تحميل البيانات")
            messagebox.showerror("خطأ", f"فشل في تحميل البيانات:\n{str(e)}")
            self.all_data = []
            self.filtered_data = []
    
    def setup_filters(self):
        """إعداد قوائم الفلاتر مع ضمان التحديث الصحيح"""
        
        if not self.all_data:
            print("⚠️ لا توجد بيانات لإعداد الفلاتر")
            return
        
        try:
            print("🔧 بدء إعداد الفلاتر...")
            
            # فلتر التاريخ
            dates = set()
            for item in self.all_data:
                date_str = item.get('التاريخ', '')
                if date_str:
                    try:
                        # استخراج التاريخ فقط (بدون الوقت)
                        if ' ' in date_str:
                            date_part = date_str.split(' ')[0]
                        else:
                            date_part = date_str
                        dates.add(date_part)
                    except:
                        dates.add(date_str)
            
            date_values = ["الكل"] + sorted(list(dates), reverse=True)
            self.date_combo['values'] = date_values
            self.date_combo.set("الكل")  # تعيين القيمة الافتراضية
            print(f"📅 فلتر التاريخ: {len(date_values)} خيار")
            
            # فلتر العنصر
            items = set(item.get('العنصر', '') for item in self.all_data if item.get('العنصر'))
            item_values = ["الكل"] + sorted(list(items))
            self.item_combo['values'] = item_values
            self.item_combo.set("الكل")  # تعيين القيمة الافتراضية
            print(f"📦 فلتر العنصر: {len(item_values)} خيار")
            
            # فلتر التصنيف  
            categories = set(item.get('التصنيف', '') for item in self.all_data if item.get('التصنيف'))
            category_values = ["الكل"] + sorted(list(categories))
            self.category_combo['values'] = category_values
            self.category_combo.set("الكل")  # تعيين القيمة الافتراضية
            print(f"🏷️ فلتر التصنيف: {len(category_values)} خيار ({list(categories)})")
            
            # فلتر المشروع
            projects = set(item.get('المشروع', '') for item in self.all_data if item.get('المشروع'))
            project_values = ["الكل"] + sorted(list(projects))
            self.project_combo['values'] = project_values
            self.project_combo.set("الكل")  # تعيين القيمة الافتراضية
            print(f"🎯 فلتر المشروع: {len(project_values)} خيار ({list(projects)})")
            
            # إجبار تحديث القيم المرتبطة
            self.date_filter_var.set("الكل")
            self.item_filter_var.set("الكل")
            self.category_filter_var.set("الكل")
            self.project_filter_var.set("الكل")
            
            print("✅ تم إعداد جميع الفلاتر بنجاح")
            
        except Exception as e:
            print(f"❌ خطأ في إعداد الفلاتر: {e}")
            import traceback
            traceback.print_exc()
    
    def setup_bindings(self):
        """ربط الأحداث للتحديث التلقائي مع حل مشكلة عدم التحديث"""
        
        print("🔗 إعداد ربط الأحداث...")
        
        # ربط تغيير الفلاتر بالتحديث التلقائي - مع تأخير قصير لتجنب التحديث المفرط
        def delayed_update(*args):
            if hasattr(self, '_update_timer'):
                self.window.after_cancel(self._update_timer)
            self._update_timer = self.window.after(200, self.force_apply_filters)
        
        # ربط جميع متغيرات الفلاتر
        self.date_filter_var.trace('w', delayed_update)
        self.item_filter_var.trace('w', delayed_update)
        self.category_filter_var.trace('w', delayed_update)
        self.project_filter_var.trace('w', delayed_update)
        self.quantity_operation_var.trace('w', delayed_update)
        self.quantity_min_var.trace('w', delayed_update)
        self.quantity_max_var.trace('w', delayed_update)
        
        # التأخير لضمان إنشاء جميع العناصر أولاً
        def setup_combobox_bindings():
            # ربط أحداث Combobox مع تحديث المتغيرات
            if hasattr(self, 'date_combo'):
                def on_date_change(event):
                    new_value = self.date_combo.get()
                    self.date_filter_var.set(new_value)
                    print(f"📅 تغيير التاريخ إلى: '{new_value}'")
                    self.window.after(100, self.force_apply_filters)
                
                self.date_combo.bind('<<ComboboxSelected>>', on_date_change)
                print("✓ تم ربط date_combo مع تحديث المتغير")
                
            if hasattr(self, 'item_combo'):
                def on_item_change(event):
                    new_value = self.item_combo.get()
                    self.item_filter_var.set(new_value)
                    print(f"📦 تغيير العنصر إلى: '{new_value}'")
                    self.window.after(100, self.force_apply_filters)
                
                self.item_combo.bind('<<ComboboxSelected>>', on_item_change)
                print("✓ تم ربط item_combo مع تحديث المتغير")
                
            if hasattr(self, 'category_combo'):
                def on_category_change(event):
                    new_value = self.category_combo.get()
                    self.category_filter_var.set(new_value)
                    print(f"🏷️ تغيير التصنيف إلى: '{new_value}'")
                    self.window.after(100, self.force_apply_filters)
                
                self.category_combo.bind('<<ComboboxSelected>>', on_category_change)
                print("✓ تم ربط category_combo مع تحديث المتغير")
                
            if hasattr(self, 'project_combo'):
                def on_project_change(event):
                    new_value = self.project_combo.get()
                    self.project_filter_var.set(new_value)
                    print(f"🎯 تغيير المشروع إلى: '{new_value}'")
                    self.window.after(100, self.force_apply_filters)
                
                self.project_combo.bind('<<ComboboxSelected>>', on_project_change)
                print("✓ تم ربط project_combo مع تحديث المتغير")
        
        # تأخير ربط Combobox حتى يتم إنشاؤها
        self.window.after(500, setup_combobox_bindings)
        
        print("✅ تم ربط جميع الأحداث")
        
        # تطبيق الفلاتر في البداية
        self.window.after(1000, self.force_apply_filters)
    
    def auto_apply_filters(self):
        """تطبيق تلقائي للفلاتر عند التغيير"""
        try:
            self.apply_filters()
        except Exception as e:
            print(f"⚠️ خطأ في التحديث التلقائي: {e}")
    
    def force_apply_filters(self):
        """تطبيق قسري للفلاتر مع تحديث فوري"""
        try:
            print("🔄 تطبيق قسري للفلاتر...")
            self.apply_filters()
            self.window.update_idletasks()  # تحديث فوري للواجهة
        except Exception as e:
            print(f"❌ خطأ في التطبيق القسري: {e}")
            import traceback
            traceback.print_exc()
    
    def force_apply_filters_with_debug(self):
        """تطبيق الفلاتر مع تشخيص مفصل للمشكلة"""
        try:
            print("🔍 === تشخيص شامل للفلاتر ===")
            
            # طباعة القيم الحالية للفلاتر
            if hasattr(self, 'date_combo'):
                print(f"📅 فلتر التاريخ - Combobox: '{self.date_combo.get()}', Variable: '{self.date_filter_var.get()}'")
            if hasattr(self, 'item_combo'):
                print(f"📦 فلتر العنصر - Combobox: '{self.item_combo.get()}', Variable: '{self.item_filter_var.get()}'")
            if hasattr(self, 'category_combo'):
                print(f"🏷️ فلتر التصنيف - Combobox: '{self.category_combo.get()}', Variable: '{self.category_filter_var.get()}'")
            if hasattr(self, 'project_combo'):
                print(f"🎯 فلتر المشروع - Combobox: '{self.project_combo.get()}', Variable: '{self.project_filter_var.get()}'")
            
            # عرض عينة من البيانات الأصلية
            if self.all_data:
                print(f"\n📊 عينة من البيانات الأصلية (أول عنصر):")
                first_item = self.all_data[0]
                for key, value in first_item.items():
                    print(f"   {key}: '{value}'")
            
            print("=" * 50)
            
            # تطبيق الفلاتر
            self.force_apply_filters()
            
        except Exception as e:
            print(f"❌ خطأ في التشخيص: {e}")
            import traceback
            traceback.print_exc()
    
    def apply_filters(self):
        """تطبيق جميع الفلاتر مع مخرجات تفصيلية وتشخيص المشاكل"""
        
        try:
            print("🔄 بدء تطبيق الفلاتر...")
            
            if not self.all_data:
                print("⚠️ لا توجد بيانات للفلترة")
                self.filtered_data = []
                self.update_table()
                self.update_statistics()
                return
            
            # بدء بجميع البيانات
            self.filtered_data = self.all_data.copy()
            initial_count = len(self.filtered_data)
            print(f"📊 البدء بـ {initial_count} عنصر")
            
            # قراءة قيم الفلاتر الفعلية من الـ comboboxes مباشرة
            date_filter_combo = self.date_combo.get() if hasattr(self, 'date_combo') else ""
            item_filter_combo = self.item_combo.get() if hasattr(self, 'item_combo') else ""
            category_filter_combo = self.category_combo.get() if hasattr(self, 'category_combo') else ""
            project_filter_combo = self.project_combo.get() if hasattr(self, 'project_combo') else ""
            
            # قراءة من المتغيرات أيضاً
            date_filter_var = self.date_filter_var.get()
            item_filter_var = self.item_filter_var.get()
            category_filter_var = self.category_filter_var.get()
            project_filter_var = self.project_filter_var.get()
            
            print(f"🔍 قيم الفلاتر من Combobox:")
            print(f"   📅 التاريخ: '{date_filter_combo}' | متغير: '{date_filter_var}'")
            print(f"   📦 العنصر: '{item_filter_combo}' | متغير: '{item_filter_var}'")
            print(f"   🏷️ التصنيف: '{category_filter_combo}' | متغير: '{category_filter_var}'")
            print(f"   🎯 المشروع: '{project_filter_combo}' | متغير: '{project_filter_var}'")
            
            # استخدام القيم من الـ combobox أولاً (الأكثر دقة)
            date_filter = date_filter_combo or date_filter_var
            item_filter = item_filter_combo or item_filter_var
            category_filter = category_filter_combo or category_filter_var
            project_filter = project_filter_combo or project_filter_var
            
            # فلتر التاريخ
            if date_filter != "الكل" and date_filter.strip():
                before_count = len(self.filtered_data)
                self.filtered_data = [item for item in self.filtered_data 
                                    if date_filter in str(item.get('التاريخ', ''))]
                after_count = len(self.filtered_data)
                print(f"📅 فلتر التاريخ '{date_filter}': {before_count} → {after_count}")
                
                if after_count == 0 and before_count > 0:
                    print(f"⚠️ لا توجد عناصر تطابق التاريخ '{date_filter}'")
                    # إظهار التواريخ المتاحة للتشخيص
                    available_dates = [item.get('التاريخ', '') for item in self.all_data]
                    print(f"📋 التواريخ المتاحة: {set(available_dates)}")
            
            # فلتر العنصر
            if item_filter != "الكل" and item_filter.strip():
                before_count = len(self.filtered_data)
                self.filtered_data = [item for item in self.filtered_data 
                                    if str(item.get('العنصر', '')) == item_filter]
                after_count = len(self.filtered_data)
                print(f"📦 فلتر العنصر '{item_filter}': {before_count} → {after_count}")
                
                if after_count == 0 and before_count > 0:
                    print(f"⚠️ لا توجد عناصر تطابق العنصر '{item_filter}'")
            
            # فلتر التصنيف
            if category_filter != "الكل" and category_filter.strip():
                before_count = len(self.filtered_data)
                self.filtered_data = [item for item in self.filtered_data 
                                    if str(item.get('التصنيف', '')) == category_filter]
                after_count = len(self.filtered_data)
                print(f"🏷️ فلتر التصنيف '{category_filter}': {before_count} → {after_count}")
                
                if after_count == 0 and before_count > 0:
                    print(f"⚠️ لا توجد عناصر تطابق التصنيف '{category_filter}'")
                    # إظهار التصنيفات المتاحة للتشخيص
                    available_categories = [item.get('التصنيف', '') for item in self.all_data]
                    print(f"📋 التصنيفات المتاحة: {set(available_categories)}")
            
            # فلتر المشروع
            if project_filter != "الكل" and project_filter.strip():
                before_count = len(self.filtered_data)
                self.filtered_data = [item for item in self.filtered_data 
                                    if str(item.get('المشروع', '')) == project_filter]
                after_count = len(self.filtered_data)
                print(f"🎯 فلتر المشروع '{project_filter}': {before_count} → {after_count}")
                
                if after_count == 0 and before_count > 0:
                    print(f"⚠️ لا توجد عناصر تطابق المشروع '{project_filter}'")
                    # إظهار المشاريع المتاحة للتشخيص
                    available_projects = [item.get('المشروع', '') for item in self.all_data]
                    print(f"📋 المشاريع المتاحة: {set(available_projects)}")
            
            # فلتر الكمية المتقدم
            self.apply_quantity_filter()
            
            # تحديث الجدول والإحصائيات
            self.update_table()
            self.update_statistics()
            
            print(f"✅ تم تطبيق جميع الفلاتر - النتائج النهائية: {len(self.filtered_data)} من أصل {initial_count}")
            
        except Exception as e:
            print(f"❌ خطأ في تطبيق الفلاتر: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("خطأ", f"فشل في تطبيق الفلاتر:\n{str(e)}")
    
    def apply_quantity_filter(self):
        """تطبيق فلتر الكمية المتقدم"""
        
        operation = self.quantity_operation_var.get()
        min_val = self.quantity_min_var.get().strip()
        max_val = self.quantity_max_var.get().strip()
        
        if operation == "الكل" or (not min_val and not max_val):
            return
        
        try:
            filtered_items = []
            
            for item in self.filtered_data:
                quantity_str = str(item.get('الكمية', '0'))
                
                # استخراج الرقم من النص
                try:
                    quantity = float(re.sub(r'[^\d.]', '', quantity_str))
                except:
                    quantity = 0
                
                # تطبيق المقارنة
                include_item = False
                
                if operation == "يساوي" and min_val:
                    try:
                        target = float(min_val)
                        include_item = quantity == target
                    except:
                        pass
                        
                elif operation == "أكبر من" and min_val:
                    try:
                        target = float(min_val)
                        include_item = quantity > target
                    except:
                        pass
                        
                elif operation == "أصغر من" and min_val:
                    try:
                        target = float(min_val)
                        include_item = quantity < target
                    except:
                        pass
                        
                elif operation == "أكبر أو يساوي" and min_val:
                    try:
                        target = float(min_val)
                        include_item = quantity >= target
                    except:
                        pass
                        
                elif operation == "أصغر أو يساوي" and min_val:
                    try:
                        target = float(min_val)
                        include_item = quantity <= target
                    except:
                        pass
                        
                elif operation == "بين" and min_val and max_val:
                    try:
                        min_target = float(min_val)
                        max_target = float(max_val)
                        include_item = min_target <= quantity <= max_target
                    except:
                        pass
                
                if include_item:
                    filtered_items.append(item)
            
            self.filtered_data = filtered_items
            
        except Exception as e:
            print(f"❌ خطأ في فلتر الكمية: {e}")
    
    def update_table(self):
        """تحديث جدول النتائج مع ضمان العرض الصحيح"""
        
        try:
            print(f"🔄 بدء تحديث الجدول - عدد العناصر للعرض: {len(self.filtered_data)}")
            
            # مسح البيانات الحالية بالكامل
            for item in self.tree.get_children():
                self.tree.delete(item)
            print("🗑️ تم مسح البيانات القديمة")
            
            # التأكد من وجود بيانات للعرض
            if not self.filtered_data:
                print("⚠️ لا توجد بيانات مفلترة للعرض")
                self.results_info.config(text="📊 النتائج: لا توجد بيانات تطابق الفلاتر")
                return
            
            # إضافة البيانات الجديدة واحدة تلو الأخرى
            for i, item in enumerate(self.filtered_data):
                try:
                    # تحديد لون الصف حسب الكمية
                    try:
                        quantity_str = str(item.get('الكمية', '0'))
                        quantity = float(re.sub(r'[^\d.]', '', quantity_str))
                        if quantity < 20:
                            tag = "low_stock"
                        elif quantity < 50:
                            tag = "medium_stock"
                        else:
                            tag = "high_stock"
                    except:
                        tag = "oddrow" if i % 2 == 0 else "evenrow"
                    
                    # تجهيز القيم للعرض
                    values = (
                        str(item.get('العنصر', '')),
                        str(item.get('التصنيف', '')),
                        str(item.get('الكمية', '')),
                        str(item.get('المشروع', '')),
                        str(item.get('التاريخ', ''))
                    )
                    
                    # إدراج الصف في الجدول
                    self.tree.insert("", tk.END, values=values, tags=(tag,))
                    print(f"✅ تمت إضافة العنصر {i+1}: {values[0]}")
                    
                except Exception as item_error:
                    print(f"❌ خطأ في إضافة العنصر {i}: {item_error}")
                    continue
            
            # تحديث معلومات النتائج
            total_items = len(self.all_data)
            filtered_items = len(self.filtered_data)
            self.results_info.config(text=f"📊 النتائج: {filtered_items} من أصل {total_items}")
            
            # إجبار تحديث الواجهة
            self.tree.update_idletasks()
            
            print(f"✅ تم تحديث الجدول بنجاح - عُرض {filtered_items} عنصر من أصل {total_items}")
            
        except Exception as e:
            print(f"❌ خطأ في تحديث الجدول: {e}")
            import traceback
            traceback.print_exc()
    
    def update_statistics_new(self, total_items, total_initial, total_in, total_out, total_remaining):
        """تحديث عرض الإحصائيات السريعة"""
        if hasattr(self, 'stats_labels'):
            self.stats_labels['total_items'].config(text=f"🔢 إجمالي العناصر: {total_items}")
            self.stats_labels['total_initial'].config(text=f"📥 الابتدائية: {total_initial:,}")
            self.stats_labels['total_in'].config(text=f"⬇️ الداخلة: {total_in:,}")
            self.stats_labels['total_out'].config(text=f"⬆️ الخارجة: {total_out:,}")
            self.stats_labels['total_remaining'].config(text=f"📦 المتبقية: {total_remaining:,}")
    
    def update_statistics(self):
        """تحديث الإحصائيات (الدالة القديمة للتوافق)"""
        
        try:
            if not self.filtered_data:
                if hasattr(self, 'stats_labels'):
                    self.update_statistics_new(0, 0, 0, 0, 0)
                return
            
            # حساب الإحصائيات من البيانات المفلترة
            total_items = len(self.filtered_data)
            total_initial = 0
            total_in = 0
            total_out = 0
            total_remaining = 0
            
            for item in self.filtered_data:
                try:
                    initial = int(item.get('الكمية الابتدائية', '0')) if str(item.get('الكمية الابتدائية', '0')).isdigit() else 0
                    in_qty = int(item.get('الداخلة', '0')) if str(item.get('الداخلة', '0')).isdigit() else 0
                    out_qty = int(item.get('الخارجة', '0')) if str(item.get('الخارجة', '0')).isdigit() else 0
                    remaining = int(item.get('المتبقية', '0')) if str(item.get('المتبقية', '0')).isdigit() else 0
                    
                    total_initial += initial
                    total_in += in_qty
                    total_out += out_qty
                    total_remaining += remaining
                        
                except Exception as e:
                    print(f"خطأ في قراءة بيانات عنصر: {e}")
                    pass
            
            # تحديث عرض الإحصائيات
            if hasattr(self, 'stats_labels'):
                self.update_statistics_new(total_items, total_initial, total_in, total_out, total_remaining)
            
        except Exception as e:
            print(f"❌ خطأ في الإحصائيات: {e}")
            if hasattr(self, 'stats_labels'):
                self.update_statistics_new(0, 0, 0, 0, 0)
    
    def clear_filters(self):
        """مسح جميع الفلاتر"""
        
        self.date_filter_var.set("الكل")
        self.item_filter_var.set("الكل")
        self.category_filter_var.set("الكل")
        self.project_filter_var.set("الكل")
        self.quantity_operation_var.set("الكل")
        self.quantity_min_var.set("")
        self.quantity_max_var.set("")
        
        print("🗑️ تم مسح جميع الفلاتر")
    
    def refresh_data(self):
        """تحديث البيانات من Google Sheets"""
        
        try:
            self.load_data()
            self.setup_filters()
            self.apply_filters()
            
            messagebox.showinfo("تحديث", f"تم تحديث البيانات بنجاح!\nتم تحميل {len(self.all_data)} عنصر")
            
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في تحديث البيانات:\n{str(e)}")
    
    def export_results(self):
        """تصدير النتائج المفلترة"""
        
        if not self.filtered_data:
            messagebox.showwarning("تحذير", "لا توجد بيانات للتصدير!")
            return
        
        try:
            from tkinter import filedialog
            import csv
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt"), ("All files", "*.*")],
                title="حفظ النتائج المفلترة"
            )
            
            if filename:
                with open(filename, 'w', newline='', encoding='utf-8-sig') as file:
                    writer = csv.writer(file)
                    
                    # كتابة العناوين
                    writer.writerow(["اسم العنصر", "التصنيف", "الكمية", "رقم المشروع", "آخر تحديث"])
                    
                    # كتابة البيانات
                    for item in self.filtered_data:
                        writer.writerow([
                            item.get('العنصر', ''),
                            item.get('التصنيف', ''),
                            item.get('الكمية', ''),
                            item.get('المشروع', ''),
                            item.get('التاريخ', '')
                        ])
                
                messagebox.showinfo("نجح التصدير", f"تم تصدير {len(self.filtered_data)} عنصر إلى:\n{filename}")
                
        except Exception as e:
            messagebox.showerror("خطأ في التصدير", f"فشل في تصدير البيانات:\n{str(e)}")
    
    def sort_by_quantity(self):
        """فرز النتائج حسب الكمية"""
        
        try:
            self.filtered_data.sort(key=lambda x: float(re.sub(r'[^\d.]', '', str(x.get('الكمية', '0')))), reverse=True)
            self.update_table()
            
        except Exception as e:
            print(f"❌ خطأ في الفرز: {e}")
    
    def sort_by_column(self, column):
        """فرز حسب العمود المحدد"""
        
        try:
            key_map = {
                "العنصر": 'العنصر',
                "التصنيف": 'التصنيف', 
                "الكمية": lambda x: float(re.sub(r'[^\d.]', '', str(x.get('الكمية', '0')))),
                "المشروع": 'المشروع',
                "آخر تحديث": 'التاريخ'
            }
            
            sort_key = key_map.get(column)
            if callable(sort_key):
                self.filtered_data.sort(key=sort_key, reverse=True)
            else:
                self.filtered_data.sort(key=lambda x: str(x.get(sort_key, '')))
                
            self.update_table()
            
        except Exception as e:
            print(f"❌ خطأ في فرز العمود: {e}")
    
    def on_window_close(self):
        """معالج إغلاق النافذة"""
        
        result = messagebox.askyesno("إغلاق النافذة", "هل تريد إغلاق نافذة الفلاتر؟")
        if result:
            self.window.destroy()

def open_advanced_filter_window(parent: tk.Widget, sheets_manager, current_user: Dict[str, Any]):
    """فتح نافذة الفلاتر المتقدمة"""
    
    try:
        print("🚀 فتح نافذة الفلاتر المتقدمة...")
        
        filter_window = AdvancedFilterWindow(parent, sheets_manager, current_user)
        
        print("✅ تم فتح نافذة الفلاتر المتقدمة بنجاح")
        return filter_window
        
    except Exception as e:
        print(f"❌ خطأ في فتح الفلاتر المتقدمة: {e}")
        import traceback
        traceback.print_exc()
        
        messagebox.showerror("خطأ", f"فشل في فتح نافذة الفلاتر المتقدمة:\n{str(e)}")
        return None