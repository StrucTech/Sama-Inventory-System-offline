"""
نافذة إدارة المشاريع للأدمن
تتيح للأدمن إنشاء مشاريع جديدة وتعيين المستخدمين لها
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, List, Dict
import threading

from sheets.projects_manager import ProjectsManager
from sheets.users_manager import UsersManager

class AdminProjectsWindow:
    """نافذة إدارة المشاريع للأدمن"""
    
    def __init__(self, parent, config: dict):
        """
        تهيئة نافذة إدارة المشاريع
        
        Args:
            parent: النافذة الرئيسية
            config: إعدادات التطبيق
        """
        self.parent = parent
        self.config = config
        self.window = None
        
        # المديرين
        self.projects_manager = None
        self.users_manager = None
        
        # البيانات
        self.projects_data = []
        self.users_data = []
        
    def show(self):
        """عرض نافذة إدارة المشاريع"""
        # إنشاء النافذة
        self.window = tk.Toplevel(self.parent)
        self.window.title("🏗️ إدارة المشاريع - المدير")
        self.window.geometry("1200x800")  # جعل النافذة أكبر
        self.window.resizable(True, True)
        
        # تعيين الحد الأدنى لحجم النافذة
        self.window.minsize(1000, 700)
        
        # توسيط النافذة
        self.center_window()
        
        # إعداد الواجهة
        self.setup_ui()
        
        # الاتصال والتحميل
        self.connect_and_load()
        
        # تفعيل الـ scroll التلقائي بعد تحميل المحتوى
        self.window.after(1000, self.enable_auto_scroll)  # تأخير لضمان تحميل المحتوى
        
        # تفعيل الـ scroll العالمي
        self.window.after(1500, self.force_global_scroll)
        
        # جعل النافذة modal
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # انتظار إغلاق النافذة
        self.window.wait_window()
    
    def center_window(self):
        """توسيط النافذة على الشاشة"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        # إنشاء Canvas مع Scrollbar
        self.canvas = tk.Canvas(self.window)
        self.scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        # ربط Canvas بـ Scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # إضافة الإطار القابل للتمرير
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # ربط أحداث التحديث
        self.scrollable_frame.bind('<Configure>', self.update_scroll_region)
        self.canvas.bind('<Configure>', self.configure_canvas_window)
        
        # وضع Canvas و Scrollbar
        self.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # إعداد الشبكة
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        
        # الإطار الرئيسي داخل Scrollable Frame
        main_frame = ttk.Frame(self.scrollable_frame, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # إعداد شبكة الإطار الرئيسي
        self.scrollable_frame.columnconfigure(0, weight=1)
        self.scrollable_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # العنوان
        title_label = ttk.Label(main_frame, text="🏗️ إدارة المشاريع والمستخدمين", 
                               font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 30))
        
        # إضافة دعم التمرير بالماوس المحسن
        self.bind_mouse_wheel()
        
        # قسم إنشاء مشروع جديد
        self.setup_create_project_section(main_frame)
        
        # فاصل كبير
        separator1 = ttk.Separator(main_frame, orient='horizontal')
        separator1.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=30)
        
        # قسم تعيين المستخدمين للمشاريع
        self.setup_assign_users_section(main_frame)
        
        # فاصل كبير
        separator2 = ttk.Separator(main_frame, orient='horizontal')
        separator2.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=30)
        
        # قسم عرض البيانات
        self.setup_data_display_section(main_frame)
        
        # فاصل كبير
        separator3 = ttk.Separator(main_frame, orient='horizontal')
        separator3.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=30)
        
        # شريط الحالة
        self.setup_status_bar(main_frame)
        
        # أزرار التحكم
        self.setup_control_buttons(main_frame)
    
    def update_scroll_region(self, event=None):
        """تحديث منطقة التمرير عند تغيير المحتوى"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def configure_canvas_window(self, event=None):
        """تكوين نافذة Canvas عند تغيير الحجم"""
        canvas_width = event.width if event else self.canvas.winfo_width()
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)
    
    def bind_mouse_wheel(self):
        """ربط التمرير بالماوس بشكل محسن"""
        def _on_mousewheel(event):
            # التمرير دائماً عندما تكون النافذة نشطة
            try:
                self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except:
                pass
        
        # ربط التمرير بالماوس للنافذة كاملة
        self.window.bind_all("<MouseWheel>", _on_mousewheel)
        
        # ربط التمرير لجميع العناصر الرئيسية
        self.canvas.bind("<MouseWheel>", _on_mousewheel)
        self.scrollable_frame.bind("<MouseWheel>", _on_mousewheel)
        
        # ربط مفاتيح لوحة المفاتيح
        self.window.bind('<Up>', lambda e: self.canvas.yview_scroll(-1, "units"))
        self.window.bind('<Down>', lambda e: self.canvas.yview_scroll(1, "units"))
        self.window.bind('<Prior>', lambda e: self.canvas.yview_scroll(-1, "pages"))  # Page Up
        self.window.bind('<Next>', lambda e: self.canvas.yview_scroll(1, "pages"))   # Page Down
        
        # ربط أحداث الدخول والخروج للتأكد
        def bind_children_recursively(widget):
            """ربط جميع العناصر الفرعية بالتمرير"""
            try:
                widget.bind("<MouseWheel>", _on_mousewheel)
                for child in widget.winfo_children():
                    bind_children_recursively(child)
            except:
                pass
        
        # ربط جميع العناصر بعد تأخير بسيط
        self.window.after(500, lambda: bind_children_recursively(self.scrollable_frame))
    
    def refresh_scroll_region(self):
        """إعادة تحديث منطقة التمرير (للاستخدام بعد تحديث المحتوى)"""
        self.window.after_idle(lambda: self.update_scroll_region())
    
    def setup_create_project_section(self, parent):
        """إعداد قسم إنشاء مشروع جديد"""
        # إطار إنشاء المشروع
        create_frame = ttk.LabelFrame(parent, text="➕ إنشاء مشروع جديد", padding="20")
        create_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N), pady=(0, 20))
        create_frame.columnconfigure(1, weight=1)
        
        # نص توضيحي
        intro_label = ttk.Label(create_frame, text="📋 املأ البيانات التالية لإنشاء مشروع جديد:",
                               font=("Arial", 10, "bold"), foreground="blue")
        intro_label.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 15))
        
        # اسم المشروع
        ttk.Label(create_frame, text="📁 اسم المشروع: *", 
                 font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, pady=(0, 8))
        
        self.project_name_var = tk.StringVar()
        self.project_name_entry = ttk.Entry(create_frame, textvariable=self.project_name_var,
                                           font=("Arial", 11), width=30)
        self.project_name_entry.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # إضافة event لمراقبة التغييرات
        self.project_name_var.trace_add('write', self.on_project_name_change)
        
        # وصف المشروع
        ttk.Label(create_frame, text="📝 وصف المشروع:", 
                 font=("Arial", 10)).grid(row=3, column=0, sticky=tk.W, pady=(0, 8))
        
        self.project_desc_var = tk.StringVar()
        self.project_desc_entry = ttk.Entry(create_frame, textvariable=self.project_desc_var,
                                           font=("Arial", 11), width=30)
        self.project_desc_entry.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # حالة المشروع
        ttk.Label(create_frame, text="🎯 حالة المشروع:", 
                 font=("Arial", 10)).grid(row=5, column=0, sticky=tk.W, pady=(0, 8))
        
        self.project_status_var = tk.StringVar(value="نشط")
        status_combo = ttk.Combobox(create_frame, textvariable=self.project_status_var,
                                   values=["نشط", "معلق", "مكتمل"], state="readonly",
                                   font=("Arial", 11), width=15)
        status_combo.grid(row=6, column=0, sticky=tk.W, pady=(0, 15))
        
        # فاصل
        separator = ttk.Separator(create_frame, orient='horizontal')
        separator.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 10))
        
        # زر إنشاء المشروع
        self.create_project_btn = ttk.Button(create_frame, text="🚀 إنشاء المشروع",
                                           command=self.create_new_project)
        self.create_project_btn.grid(row=8, column=0, columnspan=2, pady=(20, 0), 
                                   sticky=(tk.W, tk.E), ipadx=30, ipady=12)
        
        # إضافة نص توضيحي
        info_label = ttk.Label(create_frame, text="💡 اضغط على 'إنشاء المشروع' لحفظ البيانات",
                              font=("Arial", 9), foreground="gray")
        info_label.grid(row=9, column=0, columnspan=2, pady=(5, 0))
        
        # ملاحظة الحقول المطلوبة
        required_label = ttk.Label(create_frame, text="* الحقول المطلوبة",
                                  font=("Arial", 8), foreground="red")
        required_label.grid(row=10, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))
    
    def setup_assign_users_section(self, parent):
        """إعداد قسم تعيين المستخدمين للمشاريع"""
        # إطار تعيين المستخدمين
        assign_frame = ttk.LabelFrame(parent, text="👥 تعيين المستخدمين للمشاريع", padding="20")
        assign_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N), pady=(0, 20))
        assign_frame.columnconfigure(1, weight=1)
        
        # نص توضيحي
        intro_label = ttk.Label(assign_frame, text="🔗 اختر مستخدماً ومشروعاً لربطهما معاً:",
                               font=("Arial", 12, "bold"), foreground="green")
        intro_label.grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 20))
        
        # اختيار المستخدم
        ttk.Label(assign_frame, text="👤 اختر المستخدم:", 
                 font=("Arial", 11, "bold")).grid(row=1, column=0, sticky=tk.W, pady=(0, 8))
        
        self.user_var = tk.StringVar()
        self.user_combo = ttk.Combobox(assign_frame, textvariable=self.user_var,
                                      state="readonly", font=("Arial", 12), width=40)
        self.user_combo.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        self.user_combo.bind('<<ComboboxSelected>>', self.on_user_selected)
        
        # اختيار المشروع
        ttk.Label(assign_frame, text="📁 اختر المشروع:", 
                 font=("Arial", 11, "bold")).grid(row=3, column=0, sticky=tk.W, pady=(0, 8))
        
        self.assign_project_var = tk.StringVar()
        self.project_combo = ttk.Combobox(assign_frame, textvariable=self.assign_project_var,
                                         state="readonly", font=("Arial", 12), width=40)
        self.project_combo.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 30))
        self.project_combo.bind('<<ComboboxSelected>>', self.on_project_selected)
        
        # فاصل
        separator = ttk.Separator(assign_frame, orient='horizontal')
        separator.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(20, 20))
        
        # زر التعيين
        self.assign_btn = ttk.Button(assign_frame, text="🔗 تعيين المستخدم للمشروع",
                                   command=self.assign_user_to_project)
        self.assign_btn.grid(row=6, column=0, columnspan=3, pady=(10, 0), 
                           sticky=(tk.W, tk.E), ipadx=40, ipady=12)
        
        # إزالة التعيين
        self.unassign_btn = ttk.Button(assign_frame, text="❌ إزالة التعيين",
                                     command=self.unassign_user)
        self.unassign_btn.grid(row=7, column=0, columnspan=3, pady=(15, 0), 
                             sticky=(tk.W, tk.E), ipadx=40, ipady=10)
    
    def setup_data_display_section(self, parent):
        """إعداد قسم عرض البيانات"""
        # إطار قائمة المشاريع
        list_frame = ttk.LabelFrame(parent, text="📋 عرض البيانات", padding="20")
        list_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # إنشاء notebook للتبويبات
        notebook = ttk.Notebook(list_frame)
        notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # تبويبة المشاريع
        self.setup_projects_tab(notebook)
        
        # تبويبة المستخدمين
        self.setup_users_tab(notebook)
    
    def setup_projects_tab(self, notebook):
        """إعداد تبويبة المشاريع"""
        projects_frame = ttk.Frame(notebook)
        notebook.add(projects_frame, text="📁 المشاريع")
        
        # قائمة المشاريع
        columns = ("project_id", "name", "status", "users_count")
        self.projects_tree = ttk.Treeview(projects_frame, columns=columns, show="headings", height=8)
        
        # تعيين العناوين
        self.projects_tree.heading("project_id", text="رقم المشروع")
        self.projects_tree.heading("name", text="اسم المشروع")
        self.projects_tree.heading("status", text="الحالة")
        self.projects_tree.heading("users_count", text="عدد المستخدمين")
        
        # تعيين عرض الأعمدة
        self.projects_tree.column("project_id", width=120, anchor="center")
        self.projects_tree.column("name", width=300)
        self.projects_tree.column("status", width=100, anchor="center")
        self.projects_tree.column("users_count", width=120, anchor="center")
        
        # شريط التمرير للمشاريع
        projects_scrollbar = ttk.Scrollbar(projects_frame, orient="vertical", command=self.projects_tree.yview)
        self.projects_tree.configure(yscrollcommand=projects_scrollbar.set)
        
        # ترتيب المشاريع
        self.projects_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        projects_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        projects_frame.columnconfigure(0, weight=1)
        projects_frame.rowconfigure(0, weight=1)
    
    def setup_users_tab(self, notebook):
        """إعداد تبويبة المستخدمين"""
        users_frame = ttk.Frame(notebook)
        notebook.add(users_frame, text="👥 المستخدمين")
        
        # قائمة المستخدمين
        columns = ("user_id", "username", "project_id", "project_name")
        self.users_tree = ttk.Treeview(users_frame, columns=columns, show="headings", height=8)
        
        # تعيين العناوين
        self.users_tree.heading("user_id", text="رقم المستخدم")
        self.users_tree.heading("username", text="اسم المستخدم")
        self.users_tree.heading("project_id", text="رقم المشروع")
        self.users_tree.heading("project_name", text="اسم المشروع")
        
        # تعيين عرض الأعمدة
        self.users_tree.column("user_id", width=120, anchor="center")
        self.users_tree.column("username", width=200)
        self.users_tree.column("project_id", width=120, anchor="center")
        self.users_tree.column("project_name", width=200)
        
        # شريط التمرير للمستخدمين
        users_scrollbar = ttk.Scrollbar(users_frame, orient="vertical", command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=users_scrollbar.set)
        
        # ترتيب المستخدمين
        self.users_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        users_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        users_frame.columnconfigure(0, weight=1)
        users_frame.rowconfigure(0, weight=1)
    
    def setup_status_bar(self, parent):
        """إعداد شريط الحالة"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(20, 0))
        status_frame.columnconfigure(0, weight=1)
        
        self.status_label = ttk.Label(status_frame, text="جاهز لإدارة المشاريع",
                                     font=("Arial", 10), foreground="green")
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        # شريط التقدم
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
    
    def setup_control_buttons(self, parent):
        """إعداد أزرار التحكم"""
        buttons_frame = ttk.Frame(parent)
        buttons_frame.grid(row=7, column=0, columnspan=3, pady=(20, 0))
        
        # زر التحديث
        refresh_btn = ttk.Button(buttons_frame, text="🔄 تحديث البيانات",
                               command=self.refresh_data)
        refresh_btn.grid(row=0, column=0, padx=(0, 15), ipadx=20, ipady=8)
        
        # زر الإغلاق
        close_btn = ttk.Button(buttons_frame, text="❌ إغلاق",
                             command=self.close_window)
        close_btn.grid(row=0, column=1, ipadx=20, ipady=8)
    
    def connect_and_load(self):
        """الاتصال بالمديرين وتحميل البيانات"""
        def connect():
            try:
                # إظهار التقدم
                self.window.after(0, lambda: self.progress.start())
                self.window.after(0, lambda: self.status_label.config(text="جاري الاتصال...", foreground="orange"))
                
                # إنشاء المديرين
                credentials_file = self.config.get("credentials_file", "config/credentials.json")
                spreadsheet_name = self.config.get("spreadsheet_name", "Inventory Management")
                
                self.projects_manager = ProjectsManager(credentials_file, spreadsheet_name)
                self.users_manager = UsersManager(credentials_file, spreadsheet_name)
                
                # الاتصال
                if not self.projects_manager.connect():
                    raise Exception("فشل الاتصال بمدير المشاريع")
                
                if not self.users_manager.connect():
                    raise Exception("فشل الاتصال بمدير المستخدمين")
                
                # تحميل البيانات
                self.window.after(0, self.load_data)
                
            except Exception as e:
                self.window.after(0, lambda: self.on_connection_error(str(e)))
        
        # تشغيل الاتصال في thread منفصل
        thread = threading.Thread(target=connect, daemon=True)
        thread.start()
    
    def load_data(self):
        """تحميل البيانات من المديرين"""
        try:
            self.status_label.config(text="جاري تحميل البيانات...", foreground="orange")
            
            # تحميل المشاريع
            self.projects_data = self.projects_manager.get_all_projects()
            print(f"DEBUG: Loaded {len(self.projects_data)} projects")
            
            # تحميل المستخدمين العاديين فقط
            all_users = self.users_manager.get_all_users()
            print(f"DEBUG: Total users: {len(all_users)}")
            self.users_data = [user for user in all_users if user.get('user_type') == 'user']
            print(f"DEBUG: Regular users: {len(self.users_data)}")
            
            # طباعة بيانات عينة
            if self.users_data:
                print(f"DEBUG: Sample user: {self.users_data[0]}")
            if self.projects_data:
                print(f"DEBUG: Sample project: {self.projects_data[0]}")
            
            # تحديث الواجهة
            self.update_ui()
            
            self.progress.stop()
            self.status_label.config(text=f"تم تحميل {len(self.projects_data)} مشروع و {len(self.users_data)} مستخدم", 
                                   foreground="green")
            
        except Exception as e:
            self.progress.stop()
            self.status_label.config(text=f"خطأ في تحميل البيانات: {str(e)}", foreground="red")
            print(f"DEBUG: Error in load_data: {e}")
            import traceback
            traceback.print_exc()
    
    def update_ui(self):
        """تحديث عناصر الواجهة"""
        print("DEBUG: Updating UI...")
        
        # تحديث قائمة المستخدمين في الـ combo box
        user_options = []
        for user in self.users_data:
            user_display = f"{user.get('username', '')} ({user.get('user_id', '')})"
            user_options.append(user_display)
        
        print(f"DEBUG: User options: {user_options}")
        self.user_combo['values'] = user_options
        
        # تعيين القيمة الافتراضية للمستخدمين
        if user_options:
            self.user_combo.current(0)
            self.user_var.set(user_options[0])  # تعيين المتغير أيضاً
            # تحديث فوري للتأكد
            self.window.after(100, lambda: self.user_var.set(user_options[0]))
            print(f"DEBUG: Set default user to: {user_options[0]}")
        else:
            print("DEBUG: No users available")
        
        # تحديث قائمة المشاريع في الـ combo box
        project_options = []
        for project in self.projects_data:
            if project.get('status') == 'نشط':  # المشاريع النشطة فقط
                project_display = f"{project.get('name', '')} ({project.get('project_id', '')})"
                project_options.append(project_display)
        
        print(f"DEBUG: Project options: {project_options}")
        self.project_combo['values'] = project_options
        
        # تعيين القيمة الافتراضية للمشاريع
        if project_options:
            self.project_combo.current(0)
            self.assign_project_var.set(project_options[0])  # تعيين المتغير أيضاً
            # تحديث فوري للتأكد
            self.window.after(100, lambda: self.assign_project_var.set(project_options[0]))
            print(f"DEBUG: Set default project to: {project_options[0]}")
        else:
            print("DEBUG: No active projects available")
        
        # تحديث قائمة المشاريع
        self.update_projects_tree()
        
        # تحديث قائمة المستخدمين
        self.update_users_tree()
        
        # تحديث منطقة التمرير بعد تحديث المحتوى
        self.refresh_scroll_region()
    
    def update_projects_tree(self):
        """تحديث قائمة المشاريع"""
        # مسح البيانات الحالية
        for item in self.projects_tree.get_children():
            self.projects_tree.delete(item)
        
        # إضافة المشاريع
        for project in self.projects_data:
            project_id = project.get('project_id', '')
            name = project.get('name', '')
            status = project.get('status', '')
            
            # حساب عدد المستخدمين في هذا المشروع
            users_count = len([u for u in self.users_data if u.get('project_id') == project_id])
            
            self.projects_tree.insert("", "end", values=(project_id, name, status, users_count))
    
    def update_users_tree(self):
        """تحديث قائمة المستخدمين"""
        # مسح البيانات الحالية
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        # إضافة المستخدمين
        for user in self.users_data:
            user_id = user.get('user_id', '')
            username = user.get('username', '')
            project_id = user.get('project_id', '')
            
            # البحث عن اسم المشروع
            project_name = ""
            if project_id:
                for project in self.projects_data:
                    if project.get('project_id') == project_id:
                        project_name = project.get('name', '')
                        break
            else:
                project_id = "غير مُعيَّن"
                project_name = "بدون مشروع"
            
            self.users_tree.insert("", "end", values=(user_id, username, project_id, project_name))
    
    def create_new_project(self):
        """إنشاء مشروع جديد"""
        # الحصول على البيانات مباشرة من الحقول
        project_name_from_var = self.project_name_var.get().strip()
        project_name_from_entry = self.project_name_entry.get().strip()
        project_desc_from_var = self.project_desc_var.get().strip()
        project_desc_from_entry = self.project_desc_entry.get().strip()
        project_status = self.project_status_var.get()
        
        # استخدام القيمة المتاحة (من المتغير أو من الحقل مباشرة)
        project_name = project_name_from_var or project_name_from_entry
        project_desc = project_desc_from_var or project_desc_from_entry
        
        # إضافة تشخيص
        print(f"DEBUG: project_name_var.get() = '{project_name_from_var}'")
        print(f"DEBUG: project_name_entry.get() = '{project_name_from_entry}'")
        print(f"DEBUG: final project_name = '{project_name}'")
        print(f"DEBUG: project_desc = '{project_desc}'")
        print(f"DEBUG: project_status = '{project_status}'")
        
        if not project_name:
            messagebox.showerror("خطأ", f"يرجى إدخال اسم المشروع\n\nمن المتغير: '{project_name_from_var}'\nمن الحقل: '{project_name_from_entry}'")
            self.project_name_entry.focus()
            return
        
        # تأكيد الإنشاء
        confirm_msg = f"هل تريد إنشاء المشروع التالي؟\n\nالاسم: {project_name}\nالوصف: {project_desc or 'غير محدد'}\nالحالة: {project_status}"
        if not messagebox.askyesno("تأكيد الإنشاء", confirm_msg):
            return
        
        def create_project():
            try:
                self.window.after(0, lambda: self.progress.start())
                self.window.after(0, lambda: self.status_label.config(text="جاري إنشاء المشروع...", foreground="orange"))
                self.window.after(0, lambda: self.create_project_btn.config(state="disabled", text="⏳ جاري الإنشاء..."))
                
                # إنشاء المشروع
                project_id = self.projects_manager.create_project(project_name, project_desc, project_status)
                
                if project_id:
                    # مسح الحقول
                    self.window.after(0, self.clear_create_form)
                    
                    # تحديث البيانات
                    self.window.after(0, self.refresh_data)
                    
                    self.window.after(0, lambda: messagebox.showinfo("✅ نجح الإنشاء", f"تم إنشاء المشروع '{project_name}' بنجاح!\n\nرقم المشروع: {project_id}"))
                else:
                    self.window.after(0, lambda: messagebox.showerror("خطأ", "فشل في إنشاء المشروع. يرجى المحاولة مرة أخرى."))
                
            except Exception as e:
                self.window.after(0, lambda: messagebox.showerror("خطأ", f"خطأ في إنشاء المشروع:\n{str(e)}"))
            finally:
                self.window.after(0, lambda: self.progress.stop())
                self.window.after(0, lambda: self.create_project_btn.config(state="normal", text="🚀 إنشاء المشروع"))
        
        # تشغيل الإنشاء في thread منفصل
        thread = threading.Thread(target=create_project, daemon=True)
        thread.start()
    
    def assign_user_to_project(self):
        """تعيين مستخدم لمشروع"""
        print("🔄 بدء تعيين المستخدم للمشروع...")
        
        # الحصول على القيم المختارة من الـ combobox مباشرة
        user_selection = self.user_combo.get()
        project_selection = self.project_combo.get()
        
        print(f"📋 المستخدم المختار من combobox: '{user_selection}'")
        print(f"📋 المشروع المختار من combobox: '{project_selection}'")
        
        # التحقق من وجود قيم صحيحة
        if not user_selection or not project_selection:
            messagebox.showerror("خطأ", "يرجى اختيار المستخدم والمشروع من القوائم المنسدلة")
            return
        
        if user_selection.strip() == "" or project_selection.strip() == "":
            messagebox.showerror("خطأ", "يرجى اختيار قيم صحيحة من القوائم")
            return
        
        # استخراج معرفات المستخدم والمشروع
        try:
            # التحقق من وجود الأقواس في المستخدم
            if '(' not in user_selection or ')' not in user_selection:
                messagebox.showerror("خطأ", f"صيغة المستخدم غير صحيحة: {user_selection}")
                return
            
            # التحقق من وجود الأقواس في المشروع
            if '(' not in project_selection or ')' not in project_selection:
                messagebox.showerror("خطأ", f"صيغة المشروع غير صحيحة: {project_selection}")
                return
            
            user_id = user_selection.split('(')[-1].split(')')[0].strip()
            project_id = project_selection.split('(')[-1].split(')')[0].strip()
            
            print(f"📋 معرف المستخدم المستخرج: '{user_id}'")
            print(f"📋 معرف المشروع المستخرج: '{project_id}'")
            
            if not user_id or not project_id:
                messagebox.showerror("خطأ", f"فشل في استخراج المعرفات\nمعرف المستخدم: '{user_id}'\nمعرف المشروع: '{project_id}'")
                return
                
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في معالجة البيانات: {str(e)}")
            return
        
        def assign_user():
            try:
                self.window.after(0, lambda: self.progress.start())
                self.window.after(0, lambda: self.status_label.config(text="جاري تعيين المستخدم...", foreground="orange"))
                
                # تعيين المستخدم للمشروع
                if self.users_manager.assign_user_to_project(user_id, project_id):
                    # تحديث البيانات
                    self.window.after(0, self.refresh_data)
                    
                    # إشعار النوافذ الأخرى بالتحديث
                    self.window.after(0, lambda: self.notify_user_update(user_id))
                    
                    self.window.after(0, lambda: messagebox.showinfo("نجح", f"تم تعيين المستخدم للمشروع بنجاح"))
                else:
                    self.window.after(0, lambda: messagebox.showerror("خطأ", "فشل في تعيين المستخدم"))
                
            except Exception as e:
                self.window.after(0, lambda: messagebox.showerror("خطأ", f"خطأ في تعيين المستخدم: {str(e)}"))
            finally:
                self.window.after(0, lambda: self.progress.stop())
        
        # تشغيل التعيين في thread منفصل
        thread = threading.Thread(target=assign_user, daemon=True)
        thread.start()
    
    def unassign_user(self):
        """إزالة تعيين مستخدم من مشروع"""
        user_selection = self.user_var.get()
        
        if not user_selection:
            messagebox.showerror("خطأ", "يرجى اختيار المستخدم")
            return
        
        # استخراج معرف المستخدم
        user_id = user_selection.split('(')[-1].split(')')[0]
        
        def unassign_user():
            try:
                self.window.after(0, lambda: self.progress.start())
                self.window.after(0, lambda: self.status_label.config(text="جاري إزالة التعيين...", foreground="orange"))
                
                # إزالة تعيين المستخدم (تعيين مشروع فارغ)
                if self.users_manager.assign_user_to_project(user_id, ""):
                    # تحديث البيانات
                    self.window.after(0, self.refresh_data)
                    
                    self.window.after(0, lambda: messagebox.showinfo("نجح", f"تم إزالة تعيين المستخدم بنجاح"))
                else:
                    self.window.after(0, lambda: messagebox.showerror("خطأ", "فشل في إزالة تعيين المستخدم"))
                
            except Exception as e:
                self.window.after(0, lambda: messagebox.showerror("خطأ", f"خطأ في إزالة التعيين: {str(e)}"))
            finally:
                self.window.after(0, lambda: self.progress.stop())
        
        # تشغيل الإزالة في thread منفصل
        thread = threading.Thread(target=unassign_user, daemon=True)
        thread.start()
    
    def clear_create_form(self):
        """مسح نموذج إنشاء المشروع"""
        # مسح المتغيرات
        self.project_name_var.set("")
        self.project_desc_var.set("")
        self.project_status_var.set("نشط")
        
        # مسح الحقول مباشرة أيضاً للتأكد
        self.project_name_entry.delete(0, tk.END)
        self.project_desc_entry.delete(0, tk.END)
        
        print("DEBUG: Form cleared")
    
    def refresh_data(self):
        """تحديث البيانات"""
        def refresh():
            try:
                self.window.after(0, lambda: self.progress.start())
                self.window.after(0, lambda: self.status_label.config(text="جاري تحديث البيانات...", foreground="orange"))
                
                # إعادة تحميل البيانات
                self.projects_data = self.projects_manager.get_all_projects()
                all_users = self.users_manager.get_all_users()
                self.users_data = [user for user in all_users if user.get('user_type') == 'user']
                
                # تحديث الواجهة
                self.window.after(0, self.update_ui)
                
                # تحديث منطقة التمرير
                self.window.after(0, self.refresh_scroll_region)
                
                self.window.after(0, lambda: self.status_label.config(text="تم تحديث البيانات بنجاح", foreground="green"))
                
            except Exception as e:
                self.window.after(0, lambda: self.status_label.config(text=f"خطأ في التحديث: {str(e)}", foreground="red"))
            finally:
                self.window.after(0, lambda: self.progress.stop())
        
        # تشغيل التحديث في thread منفصل
        thread = threading.Thread(target=refresh, daemon=True)
        thread.start()
    
    def on_connection_error(self, error_message: str):
        """معالجة خطأ الاتصال"""
        self.progress.stop()
        self.status_label.config(text=f"خطأ في الاتصال: {error_message}", foreground="red")
        messagebox.showerror("خطأ في الاتصال", f"فشل في الاتصال بالنظام:\n{error_message}")
    
    def on_user_selected(self, event):
        """معالج حدث اختيار المستخدم"""
        selected = self.user_var.get()
        print(f"DEBUG: User selected event: '{selected}'")
        # تأكد من تحديث المتغير
        if selected:
            self.user_var.set(selected)
    
    def on_project_selected(self, event):
        """معالج حدث اختيار المشروع"""
        selected = self.assign_project_var.get()
        print(f"DEBUG: Project selected event: '{selected}'")
        # تأكد من تحديث المتغير
        if selected:
            self.assign_project_var.set(selected)
    
    def on_project_name_change(self, *args):
        """مراقب تغييرات اسم المشروع"""
        value = self.project_name_var.get()
        print(f"DEBUG: Project name changed to: '{value}'")
    
    def notify_user_update(self, user_id):
        """إشعار النوافذ الأخرى بتحديث المستخدم"""
        try:
            # البحث عن النافذة الرئيسية في النوافذ المفتوحة
            for child in self.parent.winfo_children():
                if hasattr(child, 'winfo_toplevel'):
                    toplevel = child.winfo_toplevel()
                    if hasattr(toplevel, 'children'):
                        for widget_name, widget in toplevel.children.items():
                            if hasattr(widget, 'current_user') and hasattr(widget, 'update_current_user_info'):
                                # تحقق من أن هذا هو المستخدم المحدث
                                if (widget.current_user and 
                                    widget.current_user.get('user_id') == user_id):
                                    print(f"🔄 إشعار النافذة الرئيسية بتحديث المستخدم {user_id}")
                                    # استدعاء تحديث معلومات المستخدم
                                    widget.after_idle(widget.update_current_user_info)
                                    break
        except Exception as e:
            print(f"⚠️ خطأ في إشعار تحديث المستخدم: {e}")
    
    def close_window(self):
        """إغلاق النافذة"""
        if self.window:
            self.window.destroy()
    
    def enable_auto_scroll(self):
        """تفعيل الـ scroll التلقائي عند الحاجة"""
        # إجبار تحديث المحتوى أولاً
        self.window.update_idletasks()
        
        # تحديث منطقة التمرير
        self.update_scroll_region()
        
        # إذا كان المحتوى أطول من النافذة، تفعيل الـ scroll
        bbox = self.canvas.bbox("all")
        if bbox:
            content_height = bbox[3] - bbox[1]
            canvas_height = self.canvas.winfo_height()
            
            if content_height > canvas_height:
                # المحتوى أطول من النافذة - تأكد من أن الـ scrollbar مرئي
                self.scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
            else:
                # المحتوى يناسب النافذة - يمكن إخفاء الـ scrollbar
                pass  # أبقي الـ scrollbar ظاهر دائماً للتناسق
        
        # التمرير لأعلى الصفحة
        self.canvas.yview_moveto(0)
        
        # تأكد من ربط التمرير مرة أخرى
        self.bind_mouse_wheel()
    
    def force_global_scroll(self):
        """إجبار الـ scroll على العمل في كل مكان في النافذة"""
        def universal_scroll(event):
            """دالة التمرير العامة التي تعمل في أي مكان"""
            try:
                # التأكد من أن النافذة نشطة
                if self.window and self.window.winfo_exists():
                    self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except Exception as e:
                print(f"خطأ في التمرير: {e}")
        
        # ربط التمرير بالنافذة الأساسية
        self.window.bind("<MouseWheel>", universal_scroll)
        
        # ربط التمرير بجميع العناصر بشكل متكرر
        def bind_all_widgets(widget):
            """ربط جميع العناصر بالتمرير بشكل متكرر"""
            try:
                # ربط العنصر الحالي
                widget.bind("<MouseWheel>", universal_scroll, add=True)
                
                # ربط جميع الأطفال
                for child in widget.winfo_children():
                    bind_all_widgets(child)
            except Exception as e:
                pass  # تجاهل الأخطاء
        
        # ربط جميع العناصر
        try:
            bind_all_widgets(self.window)
            bind_all_widgets(self.canvas)
            bind_all_widgets(self.scrollable_frame)
            print("✅ تم تفعيل الـ scroll العالمي")
        except Exception as e:
            print(f"⚠️ خطأ في تفعيل الـ scroll العالمي: {e}")
        
        # إعادة الربط كل فترة لضمان العمل المستمر
        self.window.after(5000, lambda: bind_all_widgets(self.window))