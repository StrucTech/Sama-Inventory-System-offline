"""
حل أساسي مضمون لمشكلة تحديث الفلاتر
"""
import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime

class BasicFilterWindow:
    def __init__(self, parent, sheets_manager):
        self.parent = parent
        self.sheets_manager = sheets_manager
        
        # البيانات
        self.all_data = []
        self.displayed_data = []
        
        # متغيرات الفلاتر
        self.category_var = tk.StringVar()
        self.project_var = tk.StringVar()
        
        # تحميل البيانات
        self.load_data()
        
        # إنشاء النافذة
        self.create_window()
        
        # عرض أولي
        self.refresh_table()
    
    def load_data(self):
        """تحميل البيانات"""
        try:
            raw_data = self.sheets_manager.get_all_items_raw()
            self.all_data = []
            
            for row in raw_data:
                if len(row) >= 4 and row[0]:
                    self.all_data.append({
                        'item': row[0].strip(),
                        'category': row[1].strip() if row[1] else "غير محدد",
                        'quantity': str(row[2]).strip() if row[2] else "0", 
                        'project': row[3].strip() if row[3] else "غير محدد",
                        'date': row[4][:10] if len(row) > 4 and row[4] else "غير محدد"
                    })
            
            print(f"✅ تم تحميل {len(self.all_data)} عنصر")
            
        except Exception as e:
            print(f"❌ خطأ في تحميل البيانات: {e}")
            self.all_data = []
    
    def create_window(self):
        """إنشاء النافذة"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("🔍 فلاتر أساسية مضمونة")
        self.window.geometry("1100x600")
        
        # === الإطار الرئيسي ===
        main_frame = tk.Frame(self.window, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # === العنوان ===
        header_frame = tk.Frame(main_frame, bg="#2c3e50", height=50)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        title = tk.Label(header_frame, text="🔍 فلاتر أساسية مضمونة", 
                        font=("Arial", 16, "bold"), fg="white", bg="#2c3e50")
        title.pack(side=tk.LEFT, padx=15, pady=12)
        
        self.counter_label = tk.Label(header_frame, text=f"المجموع: {len(self.all_data)}", 
                                     font=("Arial", 12), fg="white", bg="#2c3e50")
        self.counter_label.pack(side=tk.RIGHT, padx=15, pady=12)
        
        # === الفلاتر ===
        filter_frame = tk.LabelFrame(main_frame, text=" الفلاتر ", 
                                    font=("Arial", 11, "bold"), bg="white")
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        filter_content = tk.Frame(filter_frame, bg="white")
        filter_content.pack(fill=tk.X, padx=15, pady=15)
        
        # فلتر التصنيف
        tk.Label(filter_content, text="التصنيف:", font=("Arial", 11, "bold"), 
                bg="white").grid(row=0, column=0, padx=(0,5), sticky="w")
        
        self.category_combo = ttk.Combobox(filter_content, textvariable=self.category_var,
                                          font=("Arial", 10), width=25, state="readonly")
        self.category_combo.grid(row=0, column=1, padx=(0,20), sticky="w")
        
        # فلتر المشروع
        tk.Label(filter_content, text="المشروع:", font=("Arial", 11, "bold"), 
                bg="white").grid(row=0, column=2, padx=(0,5), sticky="w")
        
        self.project_combo = ttk.Combobox(filter_content, textvariable=self.project_var,
                                         font=("Arial", 10), width=20, state="readonly")
        self.project_combo.grid(row=0, column=3, padx=(0,20), sticky="w")
        
        # أزرار
        btn_frame = tk.Frame(filter_content, bg="white")
        btn_frame.grid(row=0, column=4, padx=(20,0))
        
        clear_btn = tk.Button(btn_frame, text="🗑️ مسح", command=self.clear_filters,
                             bg="#e74c3c", fg="white", font=("Arial", 9, "bold"),
                             padx=15, pady=8, relief="flat")
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = tk.Button(btn_frame, text="🔄 تحديث", command=self.refresh_table,
                               bg="#3498db", fg="white", font=("Arial", 9, "bold"),
                               padx=15, pady=8, relief="flat")
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # === الجدول ===
        table_frame = tk.LabelFrame(main_frame, text=" النتائج ", 
                                   font=("Arial", 11, "bold"), bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # إنشاء Treeview
        columns = ("العنصر", "التصنيف", "الكمية", "المشروع", "التاريخ")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=18)
        
        # إعداد الأعمدة
        widths = {"العنصر": 250, "التصنيف": 180, "الكمية": 100, "المشروع": 150, "التاريخ": 120}
        for col in columns:
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, width=widths.get(col, 150), anchor="center")
        
        # أشرطة التمرير
        v_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        h_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        # ترتيب العناصر
        self.tree.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        v_scroll.grid(row=0, column=1, sticky="ns", pady=10)
        h_scroll.grid(row=1, column=0, sticky="ew", padx=10)
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # إعداد الفلاتر
        self.setup_filters()
        
        # ربط الأحداث بطريقة مختلفة
        self.bind_events()
    
    def setup_filters(self):
        """إعداد خيارات الفلاتر"""
        categories = ["الكل"]
        projects = ["الكل"]
        
        for item in self.all_data:
            if item['category'] not in categories:
                categories.append(item['category'])
            if item['project'] not in projects:
                projects.append(item['project'])
        
        self.category_combo['values'] = sorted(categories)
        self.project_combo['values'] = sorted(projects)
        
        # القيم الافتراضية
        self.category_var.set("الكل")
        self.project_var.set("الكل")
    
    def bind_events(self):
        """ربط الأحداث بطرق متعددة للضمان"""
        # الطريقة الأولى: ComboboxSelected
        self.category_combo.bind("<<ComboboxSelected>>", self.on_filter_change)
        self.project_combo.bind("<<ComboboxSelected>>", self.on_filter_change)
        
        # الطريقة الثانية: trace على المتغيرات
        self.category_var.trace('w', self.on_var_change)
        self.project_var.trace('w', self.on_var_change)
        
        # الطريقة الثالثة: Button-1 (النقر)
        self.category_combo.bind("<Button-1>", lambda e: self.window.after(200, self.check_change))
        self.project_combo.bind("<Button-1>", lambda e: self.window.after(200, self.check_change))
        
        print("✅ تم ربط الأحداث بطرق متعددة")
    
    def on_filter_change(self, event=None):
        """معالج تغيير الفلتر - الطريقة الأولى"""
        print(f"🔄 [طريقة 1] تغيير فلتر: {self.category_var.get()} | {self.project_var.get()}")
        self.refresh_table()
    
    def on_var_change(self, *args):
        """معالج تغيير المتغير - الطريقة الثانية"""
        print(f"🔄 [طريقة 2] تغيير متغير: {self.category_var.get()} | {self.project_var.get()}")
        self.refresh_table()
    
    def check_change(self):
        """فحص التغيير - الطريقة الثالثة"""
        print(f"🔄 [طريقة 3] فحص تغيير: {self.category_var.get()} | {self.project_var.get()}")
        self.refresh_table()
    
    def refresh_table(self):
        """تحديث الجدول - الدالة الرئيسية"""
        print("="*50)
        print("🔄 بدء تحديث الجدول...")
        
        # مسح الجدول
        items = self.tree.get_children()
        if items:
            self.tree.delete(*items)
            print(f"🗑️ تم مسح {len(items)} عنصر من الجدول")
        
        # تطبيق الفلاتر
        category_filter = self.category_var.get()
        project_filter = self.project_var.get()
        
        print(f"🎛️ الفلاتر المطبقة: تصنيف='{category_filter}', مشروع='{project_filter}'")
        
        # فلترة البيانات
        self.displayed_data = []
        for item in self.all_data:
            # فحص التصنيف
            if category_filter != "الكل" and item['category'] != category_filter:
                continue
            
            # فحص المشروع
            if project_filter != "الكل" and item['project'] != project_filter:
                continue
            
            self.displayed_data.append(item)
        
        # إضافة للجدول
        added_count = 0
        for item in self.displayed_data:
            self.tree.insert("", "end", values=(
                item['item'],
                item['category'],
                item['quantity'],
                item['project'],
                item['date']
            ))
            added_count += 1
        
        # فرض تحديث الواجهة
        self.tree.update()
        self.tree.update_idletasks()
        self.window.update()
        
        # تحديث العداد
        self.counter_label.config(text=f"عرض: {len(self.displayed_data)} من {len(self.all_data)}")
        
        # تحديث العنوان
        if len(self.displayed_data) == len(self.all_data):
            title = "🔍 فلاتر أساسية مضمونة - جميع البيانات"
        else:
            title = f"🔍 فلاتر أساسية مضمونة - {len(self.displayed_data)} من {len(self.all_data)}"
        
        self.window.title(title)
        
        print(f"✅ تم عرض {added_count} عنصر في الجدول")
        print(f"📊 النتيجة النهائية: {len(self.displayed_data)} من أصل {len(self.all_data)}")
        print("="*50)
    
    def clear_filters(self):
        """مسح الفلاتر"""
        print("🗑️ مسح جميع الفلاتر...")
        self.category_var.set("الكل")
        self.project_var.set("الكل")
        self.refresh_table()
        messagebox.showinfo("تم", "تم مسح جميع الفلاتر")


def open_basic_filter_window(parent, sheets_manager, current_user=None):
    """فتح النافذة الأساسية المضمونة"""
    try:
        return BasicFilterWindow(parent, sheets_manager)
    except Exception as e:
        print(f"❌ خطأ: {e}")
        messagebox.showerror("خطأ", f"فشل في فتح النافذة:\\n{e}")
        return None