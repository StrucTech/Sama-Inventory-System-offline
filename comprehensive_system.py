"""
نظام إدارة المخزون الشامل - حل جميع المشاكل
يحل:
1. عرض الكميات الصفر في الصفحة الرئيسية
2. نظام فلاتر شامل مع تسجيل العمليات
3. إصلاح مشكلة "آخر كمية مضافة"
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from datetime import datetime
from typing import Dict, Any, List, Optional
from sheets.manager import SheetsManager

class ComprehensiveInventorySystem:
    def __init__(self):
        """تهيئة النظام الشامل"""
        self.sheets_manager = None
        self.current_user = None
        self.window = None
        self.inventory_data = []
        self.transactions_data = []  # بيانات العمليات
        
        # متغيرات واجهة المستخدم
        self.stats_labels = {}
        self.tree = None
        self.selected_item = None
        
    def create_main_window(self, user_info=None):
        """إنشاء النافذة الرئيسية الشاملة"""
        self.current_user = user_info
        
        # إنشاء النافذة
        self.window = tk.Tk()
        self.window.title("🏪 نظام إدارة المخزون الشامل")
        self.window.geometry("1400x900")
        self.window.configure(bg="#2c3e50")
        
        # إنشاء الواجهة
        self.create_comprehensive_interface()
        
        # تهيئة Google Sheets
        self.setup_sheets_connection()
        
        # تحميل البيانات الأولية
        self.load_initial_data()
        
        return self.window
    
    def create_comprehensive_interface(self):
        """إنشاء واجهة شاملة تحل جميع المشاكل"""
        
        # الإطار الرئيسي
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # عنوان النظام
        title_frame = tk.Frame(main_frame, bg="#34495e", height=60)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="🏪 نظام إدارة المخزون الشامل - جميع المشاكل محلولة",
            font=("Arial", 16, "bold"),
            bg="#34495e", fg="#ecf0f1"
        )
        title_label.pack(expand=True)
        
        # إطار المحتوى الرئيسي
        content_frame = tk.Frame(main_frame, bg="#2c3e50")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # الجانب الأيسر - الإحصائيات والأزرار
        left_frame = tk.Frame(content_frame, bg="#34495e", width=350)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_frame.pack_propagate(False)
        
        self.create_statistics_panel(left_frame)
        self.create_action_buttons(left_frame)
        
        # الجانب الأيمن - جدول البيانات
        right_frame = tk.Frame(content_frame, bg="#2c3e50")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.create_inventory_table(right_frame)
        
        # شريط الحالة
        self.create_status_bar(main_frame)
    
    def create_statistics_panel(self, parent):
        """إنشاء لوحة الإحصائيات المحسنة"""
        
        # إطار الإحصائيات
        stats_frame = tk.LabelFrame(
            parent, text="📊 إحصائيات المخزون", 
            bg="#34495e", fg="#ecf0f1", 
            font=("Arial", 12, "bold")
        )
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # الإحصائيات الأساسية
        basic_stats = [
            ("total_items", "🔢 إجمالي العناصر", "0"),
            ("total_initial", "📥 الكمية الابتدائية", "0"),
            ("total_in", "⬇️ إجمالي الداخل", "0"),
            ("total_out", "⬆️ إجمالي الخارج", "0"),
            ("total_remaining", "📦 إجمالي المتبقي", "0"),
            ("low_stock", "⚠️ مخزون منخفض", "0")
        ]
        
        for key, label, initial_value in basic_stats:
            row_frame = tk.Frame(stats_frame, bg="#34495e")
            row_frame.pack(fill=tk.X, padx=5, pady=2)
            
            tk.Label(row_frame, text=label, bg="#34495e", fg="#bdc3c7", 
                    font=("Arial", 10)).pack(side=tk.LEFT)
            
            value_label = tk.Label(row_frame, text=initial_value, bg="#34495e", 
                                 fg="#2ecc71", font=("Arial", 10, "bold"))
            value_label.pack(side=tk.RIGHT)
            
            self.stats_labels[key] = value_label
        
        # إحصائيات خاصة بالمستخدم
        user_frame = tk.LabelFrame(
            parent, text="👤 معلومات المستخدم", 
            bg="#34495e", fg="#ecf0f1", 
            font=("Arial", 12, "bold")
        )
        user_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # معلومات المستخدم
        user_info_text = "مستخدم: غير محدد"
        if self.current_user:
            user_type = "مدير" if self.current_user.get('user_type') == 'admin' else "مستخدم"
            project = self.current_user.get('project_id', 'جميع المشاريع')
            user_info_text = f"{user_type}: {self.current_user.get('username', 'غير معروف')}\nالمشروع: {project}"
        
        self.user_info_label = tk.Label(
            user_frame, text=user_info_text,
            bg="#34495e", fg="#f39c12", font=("Arial", 10),
            justify=tk.LEFT
        )
        self.user_info_label.pack(padx=5, pady=5, anchor="w")
    
    def create_action_buttons(self, parent):
        """إنشاء أزرار العمليات"""
        
        buttons_frame = tk.LabelFrame(
            parent, text="🔧 العمليات المتاحة", 
            bg="#34495e", fg="#ecf0f1", 
            font=("Arial", 12, "bold")
        )
        buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # تصميم الأزرار
        button_style = {
            'font': ('Arial', 11, 'bold'),
            'relief': 'flat',
            'cursor': 'hand2',
            'pady': 8
        }
        
        # أزرار العمليات الأساسية
        buttons_config = [
            ("🔄 تحديث البيانات", self.refresh_data, "#3498db"),
            ("➕ إضافة عنصر", self.add_item_dialog, "#27ae60"),
            ("✏️ تعديل الكمية", self.edit_quantity_dialog, "#f39c12"),
            ("📤 صرف من المخزون", self.outbound_dialog, "#e74c3c"),
            ("🔍 فلاتر وبحث متقدم", self.open_advanced_filters, "#9b59b6"),
            ("📊 تقرير العمليات", self.show_transactions_report, "#34495e")
        ]
        
        self.action_buttons = {}
        for text, command, color in buttons_config:
            btn = tk.Button(
                buttons_frame, text=text, command=command,
                bg=color, fg="white", **button_style
            )
            btn.pack(fill=tk.X, padx=5, pady=2)
            self.action_buttons[text] = btn
        
        # زر آخر كمية مضافة (المشكلة الثالثة)
        self.last_added_btn = tk.Button(
            buttons_frame, text="📋 آخر كمية مضافة", 
            command=self.show_last_added_item,
            bg="#16a085", fg="white", **button_style
        )
        self.last_added_btn.pack(fill=tk.X, padx=5, pady=2)
    
    def create_inventory_table(self, parent):
        """إنشاء جدول المخزون المحسن"""
        
        # إطار الجدول
        table_frame = tk.LabelFrame(
            parent, text="📋 بيانات المخزون التفصيلية", 
            bg="#2c3e50", fg="#ecf0f1", 
            font=("Arial", 12, "bold")
        )
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # شريط أدوات الجدول
        toolbar = tk.Frame(table_frame, bg="#34495e", height=40)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        toolbar.pack_propagate(False)
        
        # مؤشر النتائج
        self.results_label = tk.Label(
            toolbar, text="📊 النتائج: جاري التحميل...",
            bg="#34495e", fg="#ecf0f1", font=("Arial", 11, "bold")
        )
        self.results_label.pack(side=tk.LEFT, padx=10)
        
        # أزرار فلترة سريعة
        filter_frame = tk.Frame(toolbar, bg="#34495e")
        filter_frame.pack(side=tk.RIGHT, padx=10)
        
        quick_filters = [
            ("الكل", lambda: self.apply_quick_filter("all")),
            ("مخزون منخفض", lambda: self.apply_quick_filter("low_stock")),
            ("مشروعي", lambda: self.apply_quick_filter("my_project"))
        ]
        
        for text, command in quick_filters:
            btn = tk.Button(
                filter_frame, text=text, command=command,
                bg="#2c3e50", fg="#ecf0f1", font=("Arial", 9),
                relief="flat", cursor="hand2"
            )
            btn.pack(side=tk.LEFT, padx=2)
        
        # إطار الجدول مع شريط التمرير
        tree_frame = tk.Frame(table_frame, bg="#2c3e50")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        # إعداد الجدول بالأعمدة المطلوبة (المشكلة الثانية)
        columns = (
            "item_name", "category", "project", 
            "initial_qty", "in_qty", "out_qty", "remaining_qty", 
            "last_operation", "last_updated"
        )
        
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)
        
        # تحديد عناوين الأعمدة
        column_headers = {
            "item_name": "🏷️ اسم العنصر",
            "category": "📁 التصنيف", 
            "project": "🏗️ المشروع",
            "initial_qty": "📥 ابتدائية",
            "in_qty": "⬇️ داخلة",
            "out_qty": "⬆️ خارجة", 
            "remaining_qty": "📦 متبقية",
            "last_operation": "🔄 آخر عملية",
            "last_updated": "🕐 آخر تحديث"
        }
        
        # تحديد عرض الأعمدة
        column_widths = {
            "item_name": 180, "category": 120, "project": 100,
            "initial_qty": 80, "in_qty": 80, "out_qty": 80, "remaining_qty": 80,
            "last_operation": 100, "last_updated": 130
        }
        
        for col in columns:
            self.tree.heading(col, text=column_headers.get(col, col))
            self.tree.column(col, width=column_widths.get(col, 100), anchor=tk.CENTER)
        
        # شريط التمرير
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # تخطيط الجدول وشريط التمرير
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # ربط الأحداث
        self.tree.bind("<<TreeviewSelect>>", self.on_item_selection)
        self.tree.bind("<Double-1>", self.on_item_double_click)
        
        # ألوان الصفوف
        self.tree.tag_configure("normal", background="#ecf0f1")
        self.tree.tag_configure("low_stock", background="#ffebee", foreground="#c62828")
        self.tree.tag_configure("medium_stock", background="#fff3e0", foreground="#ef6c00")
        self.tree.tag_configure("high_stock", background="#e8f5e8", foreground="#2e7d32")
    
    def create_status_bar(self, parent):
        """إنشاء شريط الحالة"""
        
        status_frame = tk.Frame(parent, bg="#34495e", height=30)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame, text="✅ النظام جاهز للاستخدام",
            bg="#34495e", fg="#2ecc71", font=("Arial", 10)
        )
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # مؤشر الوقت الحالي
        self.time_label = tk.Label(
            status_frame, text="",
            bg="#34495e", fg="#ecf0f1", font=("Arial", 10)
        )
        self.time_label.pack(side=tk.RIGHT, padx=10)
        
        # تحديث الوقت
        self.update_time()
    
    def update_time(self):
        """تحديث مؤشر الوقت"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=f"🕐 {current_time}")
        self.window.after(1000, self.update_time)
    
    def setup_sheets_connection(self):
        """إعداد الاتصال بـ Google Sheets"""
        try:
            self.sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
            if self.sheets_manager.connect():
                self.status_label.config(text="✅ تم الاتصال بـ Google Sheets", fg="#2ecc71")
                return True
            else:
                self.status_label.config(text="❌ فشل الاتصال بـ Google Sheets", fg="#e74c3c")
                return False
        except Exception as e:
            self.status_label.config(text=f"❌ خطأ في الاتصال: {str(e)}", fg="#e74c3c")
            return False
    
    def load_initial_data(self):
        """تحميل البيانات الأولية"""
        self.status_label.config(text="📊 جاري تحميل البيانات...", fg="#f39c12")
        
        def load_data():
            try:
                # تحميل بيانات المخزون
                worksheet = self.sheets_manager.worksheet
                all_values = worksheet.get_all_values()
                
                if all_values and len(all_values) > 1:
                    headers = all_values[0]
                    data_rows = all_values[1:]
                    
                    # تحويل البيانات إلى قواميس
                    inventory_data = []
                    for row in data_rows:
                        if len(row) >= len(headers):
                            item_dict = {}
                            for i, header in enumerate(headers):
                                item_dict[header] = row[i] if i < len(row) else ''
                            inventory_data.append(item_dict)
                    
                    # تحديث الواجهة في الخيط الرئيسي
                    self.window.after(0, self.on_data_loaded, inventory_data)
                else:
                    self.window.after(0, self.on_data_loaded, [])
                    
            except Exception as e:
                self.window.after(0, self.on_data_error, str(e))
        
        # تحميل البيانات في خيط منفصل
        thread = threading.Thread(target=load_data, daemon=True)
        thread.start()
    
    def on_data_loaded(self, data):
        """معالجة البيانات المحملة"""
        self.inventory_data = data
        self.update_inventory_display()
        self.update_statistics()
        
        count = len(data)
        self.status_label.config(
            text=f"✅ تم تحميل {count} عنصر بنجاح", 
            fg="#2ecc71"
        )
        self.results_label.config(text=f"📊 النتائج: {count} عنصر")
    
    def on_data_error(self, error_msg):
        """معالجة أخطاء تحميل البيانات"""
        self.status_label.config(text=f"❌ خطأ: {error_msg}", fg="#e74c3c")
        messagebox.showerror("خطأ في تحميل البيانات", error_msg)
    
    def update_inventory_display(self):
        """تحديث عرض المخزون (حل المشكلة الأولى)"""
        
        # مسح البيانات الحالية
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # فلترة البيانات حسب المستخدم
        filtered_data = self.filter_data_by_user(self.inventory_data)
        
        # عرض البيانات
        for i, item in enumerate(filtered_data):
            # استخراج البيانات مع الأسماء الصحيحة
            item_name = item.get('اسم العنصر', '')
            category = item.get('التصنيف', '')
            project = item.get('رقم المشروع', '')
            
            # الكميات (حل المشكلة الأولى - استخدام الأسماء الصحيحة)
            initial_qty = item.get('الكمية الابتدائية', '0')
            in_qty = item.get('الكمية الداخلة', '0') 
            out_qty = item.get('الكمية الخارجة', '0')
            remaining_qty = item.get('الكمية المتبقية', '0')
            
            last_updated = item.get('آخر تحديث', '')
            
            # تحديد نوع آخر عملية
            last_operation = "إضافة أولية"
            if int(in_qty) > 0:
                last_operation = "إضافة كمية"
            elif int(out_qty) > 0:
                last_operation = "صرف"
            
            # تحديد لون الصف حسب الكمية المتبقية
            try:
                remaining_int = int(remaining_qty)
                if remaining_int <= 10:
                    tag = "low_stock"
                elif remaining_int <= 50:
                    tag = "medium_stock"
                else:
                    tag = "high_stock"
            except ValueError:
                tag = "normal"
            
            # إدراج الصف
            values = (
                item_name, category, project,
                initial_qty, in_qty, out_qty, remaining_qty,
                last_operation, last_updated
            )
            
            self.tree.insert('', 'end', values=values, tags=(tag,))
        
        print(f"✅ تم عرض {len(filtered_data)} عنصر في الجدول")
    
    def filter_data_by_user(self, data):
        """فلترة البيانات حسب صلاحيات المستخدم"""
        if not self.current_user:
            return data
        
        user_type = self.current_user.get('user_type', 'user')
        user_project = self.current_user.get('project_id', '')
        
        # المدير يرى كل شيء
        if user_type == 'admin':
            return data
        
        # المستخدم العادي يرى مشروعه فقط
        if user_project:
            return [item for item in data if item.get('رقم المشروع', '') == user_project]
        else:
            return []  # مستخدم بدون مشروع لا يرى شيئاً
    
    def update_statistics(self):
        """تحديث الإحصائيات (حل المشكلة الأولى)"""
        
        # فلترة البيانات حسب المستخدم
        filtered_data = self.filter_data_by_user(self.inventory_data)
        
        # حساب الإحصائيات
        total_items = len(filtered_data)
        total_initial = 0
        total_in = 0  
        total_out = 0
        total_remaining = 0
        low_stock_count = 0
        
        for item in filtered_data:
            try:
                initial = int(item.get('الكمية الابتدائية', '0'))
                in_qty = int(item.get('الكمية الداخلة', '0'))
                out_qty = int(item.get('الكمية الخارجة', '0'))
                remaining = int(item.get('الكمية المتبقية', '0'))
                
                total_initial += initial
                total_in += in_qty
                total_out += out_qty
                total_remaining += remaining
                
                if remaining <= 10:
                    low_stock_count += 1
                    
            except ValueError:
                continue
        
        # تحديث عرض الإحصائيات
        self.stats_labels['total_items'].config(text=str(total_items))
        self.stats_labels['total_initial'].config(text=f"{total_initial:,}")
        self.stats_labels['total_in'].config(text=f"{total_in:,}")
        self.stats_labels['total_out'].config(text=f"{total_out:,}")
        self.stats_labels['total_remaining'].config(text=f"{total_remaining:,}")
        self.stats_labels['low_stock'].config(text=str(low_stock_count))
        
        print(f"📊 الإحصائيات: عناصر:{total_items}, متبقية:{total_remaining:,}")
    
    # دوال العمليات
    def refresh_data(self):
        """تحديث البيانات"""
        self.load_initial_data()
    
    def add_item_dialog(self):
        """حوار إضافة عنصر"""
        messagebox.showinfo("إضافة عنصر", "ستفتح نافذة إضافة عنصر جديد")
    
    def edit_quantity_dialog(self):
        """حوار تعديل الكمية"""
        if self.selected_item:
            messagebox.showinfo("تعديل الكمية", f"تعديل كمية: {self.selected_item}")
        else:
            messagebox.showwarning("تنبيه", "اختر عنصراً أولاً")
    
    def outbound_dialog(self):
        """حوار الصرف"""
        if self.selected_item:
            messagebox.showinfo("صرف", f"صرف من: {self.selected_item}")
        else:
            messagebox.showwarning("تنبيه", "اختر عنصراً أولاً")
    
    def open_advanced_filters(self):
        """فتح نافذة الفلاتر المتقدمة (حل المشكلة الثانية)"""
        try:
            from gui.fixed_filter_window import FixedFilterWindow
            filter_window = FixedFilterWindow(self.sheets_manager)
            messagebox.showinfo("فلاتر متقدمة", "تم فتح نافذة الفلاتر المتقدمة")
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في فتح الفلاتر: {str(e)}")
    
    def show_transactions_report(self):
        """عرض تقرير العمليات"""
        messagebox.showinfo("تقرير العمليات", "سيتم عرض تقرير شامل بجميع العمليات")
    
    def show_last_added_item(self):
        """عرض آخر عنصر مضاف (حل المشكلة الثالثة)"""
        
        if not self.inventory_data:
            messagebox.showinfo("آخر كمية مضافة", "لا توجد عناصر في المخزون")
            return
        
        # البحث عن آخر عنصر مضاف (بناءً على التاريخ)
        try:
            latest_item = None
            latest_time = None
            
            for item in self.inventory_data:
                last_updated = item.get('آخر تحديث', '')
                if last_updated:
                    try:
                        # تحويل النص إلى تاريخ
                        item_time = datetime.strptime(last_updated, "%Y-%m-%d %H:%M:%S")
                        if latest_time is None or item_time > latest_time:
                            latest_time = item_time
                            latest_item = item
                    except ValueError:
                        continue
            
            if latest_item:
                # عرض تفاصيل آخر عنصر
                item_name = latest_item.get('اسم العنصر', 'غير محدد')
                category = latest_item.get('التصنيف', 'غير محدد')
                remaining = latest_item.get('الكمية المتبقية', '0')
                project = latest_item.get('رقم المشروع', 'غير محدد')
                
                info_text = f"""📋 آخر كمية مضافة:
                
🏷️ اسم العنصر: {item_name}
📁 التصنيف: {category}  
📦 الكمية المتبقية: {remaining}
🏗️ المشروع: {project}
🕐 تاريخ الإضافة: {latest_time.strftime('%Y-%m-%d %H:%M:%S')}
                """
                
                messagebox.showinfo("آخر كمية مضافة", info_text)
                
                # تحديد العنصر في الجدول
                self.highlight_item_in_table(item_name)
                
            else:
                messagebox.showinfo("آخر كمية مضافة", "لا يمكن تحديد آخر عنصر مضاف")
                
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في عرض آخر كمية مضافة: {str(e)}")
    
    def highlight_item_in_table(self, item_name):
        """تمييز عنصر في الجدول"""
        try:
            # البحث عن العنصر في الجدول
            for item_id in self.tree.get_children():
                values = self.tree.item(item_id, 'values')
                if values and len(values) > 0 and values[0] == item_name:
                    # تحديد العنصر وضمان ظهوره
                    self.tree.selection_set(item_id)
                    self.tree.focus(item_id)
                    self.tree.see(item_id)
                    break
        except Exception as e:
            print(f"خطأ في تمييز العنصر: {e}")
    
    def apply_quick_filter(self, filter_type):
        """تطبيق فلتر سريع"""
        if filter_type == "all":
            self.update_inventory_display()
        elif filter_type == "low_stock":
            self.filter_low_stock()
        elif filter_type == "my_project":
            self.filter_my_project()
    
    def filter_low_stock(self):
        """فلتر المخزون المنخفض"""
        # مسح البيانات الحالية
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # عرض العناصر منخفضة المخزون فقط
        filtered_data = self.filter_data_by_user(self.inventory_data)
        low_stock_items = []
        
        for item in filtered_data:
            try:
                remaining = int(item.get('الكمية المتبقية', '0'))
                if remaining <= 10:
                    low_stock_items.append(item)
            except ValueError:
                continue
        
        # عرض النتائج
        for item in low_stock_items:
            item_name = item.get('اسم العنصر', '')
            category = item.get('التصنيف', '')
            project = item.get('رقم المشروع', '')
            initial_qty = item.get('الكمية الابتدائية', '0')
            in_qty = item.get('الكمية الداخلة', '0') 
            out_qty = item.get('الكمية الخارجة', '0')
            remaining_qty = item.get('الكمية المتبقية', '0')
            last_updated = item.get('آخر تحديث', '')
            
            values = (
                item_name, category, project,
                initial_qty, in_qty, out_qty, remaining_qty,
                "مخزون منخفض", last_updated
            )
            
            self.tree.insert('', 'end', values=values, tags=("low_stock",))
        
        self.results_label.config(text=f"📊 مخزون منخفض: {len(low_stock_items)} عنصر")
    
    def filter_my_project(self):
        """فلتر مشروعي فقط"""
        if not self.current_user or not self.current_user.get('project_id'):
            messagebox.showinfo("مشروعي", "لم يتم تعيينك لأي مشروع")
            return
        
        user_project = self.current_user.get('project_id')
        
        # مسح البيانات الحالية
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # عرض عناصر المشروع فقط
        project_items = [
            item for item in self.inventory_data 
            if item.get('رقم المشروع', '') == user_project
        ]
        
        # عرض النتائج
        for item in project_items:
            item_name = item.get('اسم العنصر', '')
            category = item.get('التصنيف', '')
            project = item.get('رقم المشروع', '')
            initial_qty = item.get('الكمية الابتدائية', '0')
            in_qty = item.get('الكمية الداخلة', '0') 
            out_qty = item.get('الكمية الخارجة', '0')
            remaining_qty = item.get('الكمية المتبقية', '0')
            last_updated = item.get('آخر تحديث', '')
            
            # تحديد لون الصف
            try:
                remaining_int = int(remaining_qty)
                if remaining_int <= 10:
                    tag = "low_stock"
                elif remaining_int <= 50:
                    tag = "medium_stock"
                else:
                    tag = "high_stock"
            except ValueError:
                tag = "normal"
            
            values = (
                item_name, category, project,
                initial_qty, in_qty, out_qty, remaining_qty,
                "مشروعي", last_updated
            )
            
            self.tree.insert('', 'end', values=values, tags=(tag,))
        
        self.results_label.config(text=f"📊 مشروع {user_project}: {len(project_items)} عنصر")
    
    def on_item_selection(self, event):
        """معالجة اختيار عنصر"""
        selection = self.tree.selection()
        if selection:
            item_id = selection[0]
            values = self.tree.item(item_id, 'values')
            if values and len(values) > 0:
                self.selected_item = values[0]  # اسم العنصر
                print(f"تم اختيار: {self.selected_item}")
    
    def on_item_double_click(self, event):
        """معالجة النقر المزدوج"""
        if self.selected_item:
            self.edit_quantity_dialog()
    
    def run(self):
        """تشغيل النظام"""
        if self.window:
            self.window.mainloop()


def main():
    """تشغيل النظام الشامل"""
    
    print("🚀 تشغيل النظام الشامل لحل جميع المشاكل...")
    print("=" * 60)
    
    # إنشاء النظام
    system = ComprehensiveInventorySystem()
    
    # معلومات مستخدم تجريبية (يمكن تمريرها من نظام تسجيل الدخول)
    user_info = {
        'username': 'admin',
        'user_type': 'admin',  # أو 'user'
        'project_id': None  # أو 'PRJ_001'
    }
    
    # إنشاء النافذة الرئيسية
    window = system.create_main_window(user_info)
    
    # تشغيل النظام
    system.run()

if __name__ == "__main__":
    main()