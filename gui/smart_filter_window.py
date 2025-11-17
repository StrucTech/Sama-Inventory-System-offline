"""
نافذة البحث والفلترة الذكية - حل جديد من الصفر
تركز على البساطة والفعالية والاستجابة الفورية
"""

import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime


class SmartFilterWindow:
    """نافذة فلترة ذكية بسيطة وفعالة"""
    
    def __init__(self, parent, sheets_manager, current_user=None):
        self.parent = parent
        self.sheets_manager = sheets_manager
        self.current_user = current_user
        
        # بيانات
        self.raw_data = []
        self.filtered_data = []
        
        # متغيرات الفلاتر
        self.category_filter = tk.StringVar(value="الكل")
        self.project_filter = tk.StringVar(value="الكل") 
        self.item_filter = tk.StringVar(value="الكل")
        
        # تحميل البيانات
        self.load_inventory_data()
        
        # بناء الواجهة
        self.build_interface()
        
        # عرض البيانات الأولية
        self.apply_filters_instantly()
    
    def load_inventory_data(self):
        """تحميل بيانات المخزون"""
        try:
            print("📥 تحميل بيانات المخزون...")
            self.raw_data = self.sheets_manager.get_all_items_raw()
            
            # تنظيف البيانات
            self.clean_data = []
            for row in self.raw_data:
                if len(row) >= 4 and row[0]:  # التأكد من وجود اسم العنصر على الأقل
                    self.clean_data.append({
                        'item': row[0].strip(),
                        'category': row[1].strip() if row[1] else "غير محدد",
                        'quantity': str(row[2]).strip() if row[2] else "0",
                        'project': row[3].strip() if row[3] else "غير محدد",
                        'date': row[4][:10] if len(row) > 4 and row[4] else "غير محدد"
                    })
            
            print(f"✅ تم تحميل {len(self.clean_data)} عنصر بنجاح")
            
        except Exception as e:
            print(f"❌ خطأ في تحميل البيانات: {e}")
            self.clean_data = []
            messagebox.showerror("خطأ", f"فشل في تحميل البيانات:\n{e}")
    
    def build_interface(self):
        """بناء واجهة المستخدم"""
        # النافذة الرئيسية
        self.window = tk.Toplevel(self.parent)
        self.window.title("🔍 البحث الذكي في المخزون")
        self.window.geometry("1200x700")
        self.window.resizable(True, True)
        
        # إعداد الألوان والخط
        bg_color = "#f8f9fa"
        header_color = "#343a40"
        accent_color = "#007bff"
        
        self.window.configure(bg=bg_color)
        
        # === الشريط العلوي ===
        header_frame = tk.Frame(self.window, bg=header_color, height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # العنوان الرئيسي
        title_label = tk.Label(
            header_frame,
            text="🔍 البحث الذكي في المخزون",
            font=("Arial", 18, "bold"),
            fg="white", bg=header_color
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=15)
        
        # عداد النتائج
        self.results_counter = tk.Label(
            header_frame,
            text=f"إجمالي العناصر: {len(self.clean_data)}",
            font=("Arial", 12),
            fg="white", bg=header_color
        )
        self.results_counter.pack(side=tk.RIGHT, padx=20, pady=15)
        
        # === منطقة الفلاتر ===
        filters_frame = tk.LabelFrame(
            self.window,
            text=" 🎛️ الفلاتر ",
            font=("Arial", 12, "bold"),
            bg=bg_color,
            fg=header_color
        )
        filters_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # الفلاتر في صف واحد
        filter_row = tk.Frame(filters_frame, bg=bg_color)
        filter_row.pack(fill=tk.X, padx=15, pady=15)
        
        # فلتر التصنيف
        tk.Label(filter_row, text="التصنيف:", font=("Arial", 11, "bold"), 
                bg=bg_color, fg=header_color).grid(row=0, column=0, padx=(0,5), sticky="w")
        
        self.category_combo = ttk.Combobox(
            filter_row, textvariable=self.category_filter,
            font=("Arial", 10), width=20, state="readonly"
        )
        self.category_combo.grid(row=0, column=1, padx=(0,20), sticky="w")
        
        # فلتر المشروع
        tk.Label(filter_row, text="المشروع:", font=("Arial", 11, "bold"),
                bg=bg_color, fg=header_color).grid(row=0, column=2, padx=(0,5), sticky="w")
        
        self.project_combo = ttk.Combobox(
            filter_row, textvariable=self.project_filter,
            font=("Arial", 10), width=15, state="readonly"
        )
        self.project_combo.grid(row=0, column=3, padx=(0,20), sticky="w")
        
        # فلتر العنصر
        tk.Label(filter_row, text="العنصر:", font=("Arial", 11, "bold"),
                bg=bg_color, fg=header_color).grid(row=0, column=4, padx=(0,5), sticky="w")
        
        self.item_combo = ttk.Combobox(
            filter_row, textvariable=self.item_filter,
            font=("Arial", 10), width=25, state="readonly"
        )
        self.item_combo.grid(row=0, column=5, padx=(0,20), sticky="w")
        
        # أزرار التحكم
        buttons_frame = tk.Frame(filter_row, bg=bg_color)
        buttons_frame.grid(row=0, column=6, padx=(20,0), sticky="e")
        
        clear_btn = tk.Button(
            buttons_frame, text="🗑️ مسح الكل",
            command=self.clear_all_filters,
            bg="#dc3545", fg="white", font=("Arial", 9, "bold"),
            padx=10, pady=5, relief="flat", cursor="hand2"
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        export_btn = tk.Button(
            buttons_frame, text="📤 تصدير",
            command=self.export_results,
            bg="#28a745", fg="white", font=("Arial", 9, "bold"),
            padx=10, pady=5, relief="flat", cursor="hand2"
        )
        export_btn.pack(side=tk.LEFT, padx=5)
        
        # === جدول النتائج ===
        results_frame = tk.LabelFrame(
            self.window,
            text=" 📊 النتائج ",
            font=("Arial", 12, "bold"),
            bg=bg_color, fg=header_color
        )
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0,10))
        
        # إنشاء الجدول
        columns = ("العنصر", "التصنيف", "الكمية", "المشروع", "التاريخ")
        
        self.results_tree = ttk.Treeview(
            results_frame,
            columns=columns,
            show="headings",
            height=20
        )
        
        # إعداد أعمدة الجدول
        column_widths = {"العنصر": 300, "التصنيف": 200, "الكمية": 100, "المشروع": 150, "التاريخ": 120}
        
        for col in columns:
            self.results_tree.heading(col, text=col, anchor="center")
            self.results_tree.column(col, width=column_widths.get(col, 150), anchor="center")
        
        # أشرطة التمرير
        v_scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_tree.yview)
        h_scrollbar = ttk.Scrollbar(results_frame, orient="horizontal", command=self.results_tree.xview)
        
        self.results_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # تخطيط الجدول
        self.results_tree.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        v_scrollbar.grid(row=0, column=1, sticky="ns", pady=10)
        h_scrollbar.grid(row=1, column=0, sticky="ew", padx=10)
        
        results_frame.grid_rowconfigure(0, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)
        
        # === إعداد الفلاتر ===
        self.setup_filter_options()
        self.bind_filter_events()
    
    def setup_filter_options(self):
        """إعداد خيارات الفلاتر من البيانات"""
        categories = set(["الكل"])
        projects = set(["الكل"])
        items = set(["الكل"])
        
        for item in self.clean_data:
            categories.add(item['category'])
            projects.add(item['project'])
            items.add(item['item'])
        
        # تحديث القوائم
        self.category_combo['values'] = sorted(list(categories))
        self.project_combo['values'] = sorted(list(projects))
        self.item_combo['values'] = sorted(list(items))
        
        # القيم الافتراضية
        self.category_filter.set("الكل")
        self.project_filter.set("الكل")
        self.item_filter.set("الكل")
    
    def bind_filter_events(self):
        """ربط أحداث الفلاتر"""
        self.category_combo.bind("<<ComboboxSelected>>", self.on_filter_changed)
        self.project_combo.bind("<<ComboboxSelected>>", self.on_filter_changed) 
        self.item_combo.bind("<<ComboboxSelected>>", self.on_filter_changed)
    
    def on_filter_changed(self, event=None):
        """معالج تغيير الفلاتر"""
        print("="*60)
        print("🔄 تم تغيير فلتر - بدء المعالجة الفورية...")
        
        # طباعة القيم الحالية للفلاتر
        category = self.category_filter.get()
        project = self.project_filter.get() 
        item = self.item_filter.get()
        
        print(f"📋 القيم الجديدة:")
        print(f"   التصنيف: '{category}'")
        print(f"   المشروع: '{project}'")
        print(f"   العنصر: '{item}'")
        
        # تطبيق الفلاتر مع تأخير قصير لضمان التحديث
        self.window.after(100, self.apply_filters_instantly)
        
        print("✅ تم جدولة التحديث")
        print("="*60)
    
    def apply_filters_instantly(self):
        """تطبيق الفلاتر فوراً مع التحديث البصري"""
        # مسح الجدول بالكامل وبقوة
        print("🗑️ مسح محتوى الجدول...")
        
        # الحصول على جميع العناصر الموجودة
        current_items = self.results_tree.get_children()
        print(f"📊 العناصر الحالية في الجدول: {len(current_items)}")
        
        # مسح كل عنصر
        if current_items:
            self.results_tree.delete(*current_items)
            print(f"✅ تم مسح {len(current_items)} عنصر من الجدول")
        
        # فرض تحديث بعد المسح
        self.results_tree.update()
        self.results_tree.update_idletasks()
        
        # الحصول على قيم الفلاتر
        selected_category = self.category_filter.get()
        selected_project = self.project_filter.get()
        selected_item = self.item_filter.get()
        
        print(f"📋 الفلاتر: تصنيف='{selected_category}', مشروع='{selected_project}', عنصر='{selected_item}'")
        
        # تطبيق الفلاتر
        self.filtered_data = []
        
        for item in self.clean_data:
            # فلترة التصنيف
            if selected_category != "الكل" and item['category'] != selected_category:
                continue
            
            # فلترة المشروع
            if selected_project != "الكل" and item['project'] != selected_project:
                continue
                
            # فلترة العنصر
            if selected_item != "الكل" and item['item'] != selected_item:
                continue
            
            # إضافة للنتائج
            self.filtered_data.append(item)
        
        # عرض النتائج في الجدول مع فرض التحديث
        print(f"📋 إضافة {len(self.filtered_data)} صف للجدول...")
        
        row_count = 0
        for item in self.filtered_data:
            try:
                self.results_tree.insert("", "end", values=(
                    item['item'],
                    item['category'],
                    item['quantity'],
                    item['project'],
                    item['date']
                ))
                row_count += 1
            except Exception as e:
                print(f"⚠️ خطأ في إضافة صف: {e}")
        
        print(f"✅ تم إضافة {row_count} صف بنجاح")
        
        # فرض تحديث الجدول والواجهة
        self.results_tree.update()
        self.results_tree.update_idletasks()
        self.window.update()
        self.window.update_idletasks()
        
        # تحديث العداد
        self.update_results_counter()
        
        # تحديث عنوان النافذة
        self.update_window_title()
        
        # تحديث إضافي متأخر للتأكد
        self.window.after(50, lambda: self.results_tree.update_idletasks())
        
        print(f"🎯 النتيجة النهائية: {len(self.filtered_data)} من أصل {len(self.clean_data)} عنصر")
    
    def update_results_counter(self):
        """تحديث عداد النتائج"""
        total_quantity = 0
        try:
            for item in self.filtered_data:
                total_quantity += float(item['quantity']) if item['quantity'].replace('.','').isdigit() else 0
        except:
            pass
        
        counter_text = f"عرض: {len(self.filtered_data)} من {len(self.clean_data)} | إجمالي الكمية: {total_quantity:,.0f}"
        self.results_counter.config(text=counter_text)
    
    def update_window_title(self):
        """تحديث عنوان النافذة"""
        if len(self.filtered_data) == len(self.clean_data):
            title = "🔍 البحث الذكي في المخزون - جميع البيانات"
        else:
            title = f"🔍 البحث الذكي في المخزون - {len(self.filtered_data)} من {len(self.clean_data)} عنصر"
        
        self.window.title(title)
    
    def clear_all_filters(self):
        """مسح جميع الفلاتر"""
        print("🗑️ مسح جميع الفلاتر...")
        
        self.category_filter.set("الكل")
        self.project_filter.set("الكل")
        self.item_filter.set("الكل")
        
        self.apply_filters_instantly()
        
        messagebox.showinfo("تم المسح", "تم مسح جميع الفلاتر وعرض جميع البيانات")
    
    def export_results(self):
        """تصدير النتائج إلى ملف CSV"""
        try:
            if not self.filtered_data:
                messagebox.showwarning("تحذير", "لا توجد بيانات للتصدير")
                return
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"search_results_{timestamp}.csv"
            
            with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.writer(csvfile)
                
                # كتابة العناوين
                writer.writerow(['العنصر', 'التصنيف', 'الكمية', 'المشروع', 'التاريخ'])
                
                # كتابة البيانات
                for item in self.filtered_data:
                    writer.writerow([
                        item['item'],
                        item['category'],
                        item['quantity'],
                        item['project'],
                        item['date']
                    ])
            
            messagebox.showinfo("تم التصدير", 
                f"تم تصدير {len(self.filtered_data)} عنصر بنجاح إلى:\n{filename}")
            
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في التصدير:\n{e}")


def open_smart_filter_window(parent, sheets_manager, current_user=None):
    """فتح نافذة البحث الذكي"""
    try:
        return SmartFilterWindow(parent, sheets_manager, current_user)
    except Exception as e:
        print(f"❌ خطأ في فتح نافذة البحث: {e}")
        messagebox.showerror("خطأ", f"فشل في فتح نافذة البحث:\n{e}")
        return None