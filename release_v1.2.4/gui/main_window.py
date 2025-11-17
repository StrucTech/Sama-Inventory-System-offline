"""
Main window for the Inventory Management System.
Contains the primary GUI interface and coordinates between components.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, List
import threading

from sheets.manager import SheetsManager
from .inventory_view import InventoryView
from .add_item_dialog import AddItemDialog
from .edit_quantity_dialog import EditQuantityDialog
from .outbound_dialog import OutboundDialog
from .admin_projects_window import AdminProjectsWindow
from sheets.manager import SheetsManager
from localization import get_text

# مخطط الألوان الفاخر للنافذة الرئيسية
LUXURY_MAIN_COLORS = {
    # الألوان الأساسية - درجات الذهبي والأزرق الداكن
    'primary_gold': '#DAA520',           # ذهبي داكن
    'primary_dark': '#1A1A2E',          # أزرق داكن عميق
    'secondary_gold': '#FFD700',        # ذهبي فاتح
    'secondary_dark': '#16213E',        # أزرق داكن ثانوي
    
    # ألوان الخلفية
    'bg_main': '#0F1419',              # خلفية رئيسية داكنة
    'bg_toolbar': '#1E2A4A',           # خلفية شريط الأدوات
    'bg_content': '#16213E',           # خلفية المحتوى
    'bg_card': '#2C3E60',              # خلفية البطاقات
    'bg_hover': '#34495E',             # لون عند التمرير
    
    # ألوان النصوص
    'text_primary': '#FFFFFF',         # نص أبيض رئيسي
    'text_secondary': '#BDC3C7',       # نص رمادي فاتح
    'text_accent': '#F39C12',          # نص ذهبي للتأكيد
    'text_title': '#DAA520',           # نص العناوين الذهبي
    
    # ألوان الحالة
    'success': '#27AE60',              # أخضر للنجاح
    'warning': '#F39C12',              # برتقالي للتحذير
    'error': '#E74C3C',                # أحمر للخطأ
    'info': '#3498DB',                 # أزرق للمعلومات
    
    # ألوان الأزرار
    'btn_primary': '#DAA520',          # أزرار رئيسية ذهبية
    'btn_secondary': '#2C3E60',        # أزرار ثانوية
    'btn_success': '#27AE60',          # أزرار النجاح
    'btn_danger': '#E74C3C',           # أزرار الخطر
}

class MainWindow:
    """Main application window."""
    
    def __init__(self, root: tk.Tk, config: Dict[str, Any]):
        """
        Initialize the main window.
        
        Args:
            root: Root tkinter window
            config: Application configuration
        """
        self.root = root
        self.config = config
        self.sheets_manager = None
        self.inventory_data = []
        self.current_user = None  # سيتم تعيينه من main_with_auth.py
        
        # Initialize components
        self.setup_ui()
        self.connect_to_sheets()
        
    def setup_ui(self):
        """Set up the user interface with luxury design."""
        # تطبيق الخلفية الفاخرة على النافذة الرئيسية
        self.root.configure(bg=LUXURY_MAIN_COLORS['bg_main'])
        
        # Create main frame with luxury styling
        main_frame = tk.Frame(self.root, 
                             bg=LUXURY_MAIN_COLORS['bg_main'],
                             padx=15, 
                             pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)  # تعديل لإضافة صف جديد
        
        # User info bar - إضافة شريط معلومات المستخدم الفاخر
        self.setup_user_info_bar(main_frame)
        
        # Title الفاخر مع تصميم ذهبي
        title_frame = tk.Frame(main_frame, bg=LUXURY_MAIN_COLORS['bg_main'])
        title_frame.grid(row=1, column=0, columnspan=3, pady=(10, 20), sticky=tk.EW)
        
        title_label = tk.Label(title_frame, 
                              text="👑 نظام إدارة المخزون 👑", 
                              font=("Tahoma", 20, "bold"),
                              fg=LUXURY_MAIN_COLORS['primary_gold'],
                              bg=LUXURY_MAIN_COLORS['bg_main'])
        title_label.pack()
        
        # العنوان الفرعي
        subtitle_label = tk.Label(title_frame, 
                                 text="✨ حلول متقدمة لإدارة المخزون والمواد ✨", 
                                 font=("Tahoma", 12),
                                 fg=LUXURY_MAIN_COLORS['text_secondary'],
                                 bg=LUXURY_MAIN_COLORS['bg_main'])
        subtitle_label.pack(pady=(5, 0))
        
        # خط فاصل ذهبي
        separator = tk.Frame(title_frame, 
                            height=2, 
                            bg=LUXURY_MAIN_COLORS['primary_gold'])
        separator.pack(fill=tk.X, padx=100, pady=(10, 0))
        
        # Status label الفاخر
        self.status_label = tk.Label(title_frame, 
                                    text=get_text("connecting"), 
                                    font=("Tahoma", 10, "bold"),
                                    fg=LUXURY_MAIN_COLORS['warning'],
                                    bg=LUXURY_MAIN_COLORS['bg_main'])
        self.status_label.pack(pady=(10, 0))
        
        # Buttons frame الفاخر
        buttons_frame = tk.Frame(main_frame, bg=LUXURY_MAIN_COLORS['bg_main'])
        buttons_frame.grid(row=2, column=0, sticky=(tk.W, tk.N), padx=(0, 15))
        
        # Create luxury button configuration
        luxury_button_config = {
            "font": ("Tahoma", 12, "bold"),
            "width": 20,
            "relief": "raised",
            "bd": 3,
            "cursor": "hand2",
            "activeforeground": LUXURY_MAIN_COLORS['text_primary']
        }
        
        # Refresh button - ذهبي فاخر
        self.refresh_btn = tk.Button(buttons_frame, text="🔄 " + get_text("refresh"), 
                                    command=self.refresh_data, state="disabled",
                                    bg=LUXURY_MAIN_COLORS['btn_primary'], 
                                    fg=LUXURY_MAIN_COLORS['primary_dark'],
                                    activebackground=LUXURY_MAIN_COLORS['secondary_gold'],
                                    **luxury_button_config)
        self.refresh_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Add item button - أخضر فاخر  
        self.add_btn = tk.Button(buttons_frame, text="➕ " + get_text("add_item"), 
                                command=self.add_item, state="disabled",
                                bg=LUXURY_MAIN_COLORS['btn_success'], 
                                fg=LUXURY_MAIN_COLORS['text_primary'],
                                activebackground='#2ECC71',
                                **luxury_button_config)
        self.add_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Edit quantity button - أزرق فاخر
        self.edit_btn = tk.Button(buttons_frame, text="✏️ " + get_text("edit_quantity"), 
                                 command=self.edit_quantity, state="disabled",
                                 bg=LUXURY_MAIN_COLORS['info'], 
                                 fg=LUXURY_MAIN_COLORS['text_primary'],
                                 activebackground='#5DADE2',
                                 **luxury_button_config)
        self.edit_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Outbound button - بنفسجي فاخر
        self.outbound_btn = tk.Button(buttons_frame, text="📤 " + get_text("outbound_item"), 
                                     command=self.outbound_item, state="disabled",
                                     bg='#8E44AD', 
                                     fg=LUXURY_MAIN_COLORS['text_primary'],
                                     activebackground='#A569BD',
                                     **luxury_button_config)
        self.outbound_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Remove button (Admin only) - أحمر فاخر
        self.remove_btn = tk.Button(buttons_frame, text="🗑️ " + get_text("remove_item"), 
                                   command=self.remove_item, state="disabled",
                                   bg=LUXURY_MAIN_COLORS['btn_danger'], 
                                   fg=LUXURY_MAIN_COLORS['text_primary'],
                                   activebackground='#EC7063',
                                   **luxury_button_config)
        self.remove_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Admin Projects button (only for admins) - بني فاخر
        self.admin_btn = tk.Button(buttons_frame, text="🏗️ إدارة المشاريع", 
                                  command=self.open_admin_window, state="disabled",
                                  bg='#8D6E63', 
                                  fg=LUXURY_MAIN_COLORS['text_primary'],
                                  activebackground='#A1887F',
                                  **luxury_button_config)
        self.admin_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Search with Filters button - رمادي فاخر
        self.reports_btn = tk.Button(buttons_frame, text="🔍 بحث بالفلاتر", 
                                    command=self.open_filter_search_window,
                                    state="disabled",  # معطل في البداية حتى تحميل البيانات
                                    bg='#2E86AB', 
                                    fg=LUXURY_MAIN_COLORS['text_primary'],
                                    activebackground='#3AA3C7',
                                    **luxury_button_config)
        self.reports_btn.pack(fill=tk.X, pady=(0, 10))
        

        
        # Analytics and Insights button (only for admins) - بنفسجي فاخر
        self.analytics_btn = tk.Button(buttons_frame, text="📊 تحليل ورؤى البيانات", 
                                      command=self.open_analytics_window, state="disabled",
                                      bg='#8E24AA', 
                                      fg=LUXURY_MAIN_COLORS['text_primary'],
                                      activebackground='#AB47BC',
                                      **luxury_button_config)
        self.analytics_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Inventory view
        self.inventory_view = InventoryView(main_frame, self.on_item_selected)
        self.inventory_view.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def connect_to_sheets(self):
        """Connect to Google Sheets in a separate thread."""
        def connect():
            try:
                self.sheets_manager = SheetsManager(
                    credentials_file=self.config["credentials_file"],
                    spreadsheet_name=self.config["spreadsheet_name"],
                    worksheet_name=self.config["worksheet_name"]
                )
                
                if self.sheets_manager.connect():
                    self.root.after(0, self.on_connection_success)
                else:
                    self.root.after(0, self.on_connection_error, "Failed to connect to Google Sheets")
                    
            except Exception as e:
                self.root.after(0, self.on_connection_error, str(e))
                
        # Start connection in background thread
        thread = threading.Thread(target=connect, daemon=True)
        thread.start()
        
    def on_connection_success(self):
        """Handle successful connection to Google Sheets."""
        self.status_label.config(text=get_text("connected"), 
                                foreground=LUXURY_MAIN_COLORS['btn_success'])
        
        # تعيين المستخدم الحالي في SheetsManager
        if self.current_user and hasattr(self.sheets_manager, 'set_current_user'):
            username = self.current_user.get('username', '')
            self.sheets_manager.set_current_user(username)
        
        # Enable buttons based on user type and project assignment
        self.refresh_btn.config(state="normal")
        
        # Enable action buttons only for admins or users with projects
        if (self.current_user and 
            (self.current_user.get('user_type') == 'admin' or 
             self.current_user.get('project_id'))):
            self.add_btn.config(state="normal")
        else:
            self.add_btn.config(state="disabled")
        
        # Enable admin button for admins only
        if (self.current_user and 
            self.current_user.get('user_type') == 'admin'):
            self.admin_btn.config(state="normal")
            self.analytics_btn.config(state="normal")
        else:
            self.admin_btn.pack_forget()  # إخفاء الزر للمستخدمين العاديين
            self.analytics_btn.pack_forget()  # إخفاء زر التحليل للمستخدمين العاديين
        
        # Hide remove button for non-admin users
        if not (self.current_user and 
                self.current_user.get('user_type') == 'admin'):
            self.remove_btn.pack_forget()  # إخفاء زر الحذف للمستخدمين العاديين
        
        # Update edit button text based on user type
        if (self.current_user and 
            self.current_user.get('user_type') == 'user'):
            self.edit_btn.config(text="تعديل آخر كمية مضافة")
        
        # Enable reports button for all users
        self.reports_btn.config(state="normal")
        
        # Load initial data
        self.refresh_data()
        
    def on_connection_error(self, error_message: str):
        """Handle connection error."""
        self.status_label.config(text=get_text("connection_failed"), 
                               foreground=LUXURY_MAIN_COLORS['btn_danger'])
        messagebox.showerror(get_text("connection_error"), 
                           get_text("connection_error_details", error_message))
    
    def update_current_user_info(self):
        """تحديث معلومات المستخدم الحالي من Google Sheets"""
        if not self.current_user or not self.sheets_manager:
            return
        
        try:
            # إنشاء مدير المستخدمين للحصول على البيانات المحدثة
            from sheets.users_manager import UsersManager
            users_manager = UsersManager(
                self.config.get('credentials_file', 'credentials.json'),
                self.config.get('spreadsheet_name', 'Inventory Database')
            )
            
            # الاتصال ثم الحصول على بيانات المستخدم المحدثة
            if users_manager.connect():
                updated_user = users_manager.get_user_by_id(self.current_user['user_id'])
            
            if updated_user:
                # تحديث معلومات المستخدم الحالي
                old_project_id = self.current_user.get('project_id')
                self.current_user.update(updated_user)
                new_project_id = self.current_user.get('project_id')
                
                # إذا تغير المشروع، أعلم المستخدم وحدّث البيانات
                if old_project_id != new_project_id:
                    if new_project_id:
                        print(f"✅ تم تحديث مشروع المستخدم إلى: {new_project_id}")
                        messagebox.showinfo("تحديث المشروع", 
                                          f"تم تعيينك لمشروع جديد: {new_project_id}\n"
                                          "سيتم تحديث البيانات المعروضة.")
                    else:
                        print("⚠️ تم إزالة المستخدم من المشروع")
                        messagebox.showwarning("إزالة من المشروع", 
                                             "تم إزالتك من المشروع.\n"
                                             "لن تتمكن من رؤية أو تعديل البيانات.")
                    
                    # تحديث واجهة المستخدم
                    self.update_user_info_display()
                    self.refresh_data()
                    
                return True
        except Exception as e:
            print(f"❌ خطأ في تحديث معلومات المستخدم: {e}")
            return False
    
    def update_user_info_display(self):
        """تحديث عرض معلومات المستخدم في الواجهة"""
        if hasattr(self, 'user_info_label') and self.current_user:
            username = self.current_user.get('username', 'غير معروف')
            user_type = self.current_user.get('user_type', 'غير محدد')
            project_id = self.current_user.get('project_id', '')
            
            if user_type == 'admin':
                user_text = f"👤 {username} (مدير)"
            elif project_id:
                user_text = f"👤 {username} (مشروع: {project_id})"
            else:
                user_text = f"👤 {username} (بدون مشروع)"
            
            self.user_info_label.config(text=user_text)
    
    def refresh_data(self):
        """Refresh inventory data from Google Sheets."""
        if not self.sheets_manager:
            return
        
        # تحديث معلومات المستخدم أولاً
        self.update_current_user_info()
            
        def load_data():
            try:
                # الحصول على البيانات حسب نوع المستخدم
                if self.current_user and self.current_user.get('user_type') == 'admin':
                    # المدير - عرض جميع العناصر
                    data = self.sheets_manager.get_all_items()
                elif (self.current_user and 
                      self.current_user.get('user_type') == 'user' and 
                      self.current_user.get('project_id')):
                    # مستخدم عادي منسوب لمشروع - عرض عناصر مشروعه فقط
                    data = self.sheets_manager.get_items_by_project(self.current_user['project_id'])
                else:
                    # مستخدم عادي بدون مشروع - لا يرى أي عناصر
                    data = []
                    print(f"⚠️ المستخدم '{self.current_user.get('username', 'غير معروف')}' غير منسوب لأي مشروع - لا توجد بيانات للعرض")
                    
                self.root.after(0, self.on_data_loaded, data)
            except Exception as e:
                self.root.after(0, self.on_data_error, str(e))
                
        # Show loading status
        self.status_label.config(text=get_text("loading_data"), 
                               foreground=LUXURY_MAIN_COLORS['warning'])
        
        # Load data in background thread
        thread = threading.Thread(target=load_data, daemon=True)
        thread.start()
        
    def on_data_loaded(self, data: List[Dict[str, Any]]):
        """Handle loaded inventory data."""
        self.inventory_data = data
        self.inventory_view.update_data(data)
        
        # رسالة الحالة حسب نوع المستخدم ومشروعه
        if len(data) == 0:
            if (self.current_user and 
                self.current_user.get('user_type') == 'user' and 
                not self.current_user.get('project_id')):
                # مستخدم بدون مشروع
                self.status_label.config(
                    text="⚠️ لم يتم تعيينك لأي مشروع - تواصل مع المدير لتعيينك لمشروع", 
                    foreground=LUXURY_MAIN_COLORS['btn_danger']
                )
            else:
                # لا توجد بيانات
                self.status_label.config(text=get_text("loaded_items", 0), 
                                       foreground=LUXURY_MAIN_COLORS['warning'])
        else:
            # توجد بيانات
            if (self.current_user and self.current_user.get('user_type') == 'user'):
                project_info = f" (مشروع: {self.current_user.get('project_id', 'غير معروف')})"
            else:
                project_info = " (جميع المشاريع)"
            
            self.status_label.config(
                text=f"تم تحميل {len(data)} عنصر{project_info}", 
                foreground=LUXURY_MAIN_COLORS['btn_success']
            )
        
        # تفعيل زر البحث بالفلاتر بعد تحميل البيانات
        self.reports_btn.config(state="normal")
        
    def on_data_error(self, error_message: str):
        """Handle data loading error."""
        self.status_label.config(text=get_text("failed_to_load"), 
                               foreground=LUXURY_MAIN_COLORS['btn_danger'])
        messagebox.showerror(get_text("data_error"), get_text("data_error_details", error_message))
        
        # إبقاء زر البحث بالفلاتر معطل في حالة الخطأ
        self.reports_btn.config(state="disabled")
        
    def on_item_selected(self, has_selection: bool):
        """Handle item selection change in the inventory view."""
        self.edit_btn.config(state="normal" if has_selection else "disabled")
        self.outbound_btn.config(state="normal" if has_selection else "disabled")
        
        # زر الحذف متاح للمديرين فقط (وسيكون مخفياً للمستخدمين العاديين)
        if (self.current_user and 
            self.current_user.get('user_type') == 'admin'):
            self.remove_btn.config(state="normal" if has_selection else "disabled")
        
    def add_item(self):
        """Open dialog to add a new item."""
        # التحقق من أن المستخدم العادي منسوب لمشروع
        if (self.current_user and 
            self.current_user.get('user_type') == 'user' and 
            not self.current_user.get('project_id')):
            messagebox.showerror(
                "غير مسموح", 
                "لا يمكنك إضافة عناصر لأنك غير منسوب لأي مشروع.\nيرجى التواصل مع المدير لتعيينك لمشروع."
            )
            return
        
        # Get existing items for the dropdown
        try:
            existing_items = self.sheets_manager.get_all_items()
        except:
            existing_items = []
        
        dialog = AddItemDialog(self.root, existing_items)
        result = dialog.show()
        
        if result:
            item_name, category, quantity = result
            
            def add_item_to_sheets():
                try:
                    # تحديد رقم المشروع حسب نوع المستخدم
                    project_id = ""
                    if (self.current_user and 
                        self.current_user.get('user_type') == 'user' and 
                        self.current_user.get('project_id')):
                        # مستخدم عادي - استخدم مشروعه
                        project_id = self.current_user['project_id']
                    
                    if self.sheets_manager.add_item(item_name, category, quantity, project_id):
                        self.root.after(0, self.on_item_added)
                    else:
                        self.root.after(0, self.on_operation_error, get_text("operation_failed"))
                except Exception as e:
                    self.root.after(0, self.on_operation_error, str(e))
                    
            # Show status
            self.status_label.config(text=get_text("adding_item"), 
                                    foreground=LUXURY_MAIN_COLORS['warning'])
            
            # Add item in background thread
            thread = threading.Thread(target=add_item_to_sheets, daemon=True)
            thread.start()
            
    def on_item_added(self):
        """Handle successful item addition."""
        self.status_label.config(text=get_text("item_added"), 
                                foreground=LUXURY_MAIN_COLORS['btn_success'])
        self.refresh_data()
        
    def edit_quantity(self):
        """Open dialog to edit item quantity."""
        # التحقق من أن المستخدم العادي منسوب لمشروع
        if (self.current_user and 
            self.current_user.get('user_type') == 'user' and 
            not self.current_user.get('project_id')):
            messagebox.showerror(
                "غير مسموح", 
                "لا يمكنك تعديل العناصر لأنك غير منسوب لأي مشروع.\nيرجى التواصل مع المدير لتعيينك لمشروع."
            )
            return
        
        # للمستخدمين العاديين - التحقق من العمليات الحديثة
        if (self.current_user and 
            self.current_user.get('user_type') == 'user'):
            return self.edit_recent_addition()
        
        selected_item = self.inventory_view.get_selected_item()
        if not selected_item:
            return
            
        dialog = EditQuantityDialog(self.root, selected_item)
        new_quantity = dialog.show()
        
        if new_quantity is not None:
            def update_quantity():
                try:
                    if self.sheets_manager.update_quantity(selected_item["row"], new_quantity):
                        self.root.after(0, self.on_quantity_updated)
                    else:
                        self.root.after(0, self.on_operation_error, "Failed to update quantity")
                except Exception as e:
                    self.root.after(0, self.on_operation_error, str(e))
                    
            # Show status
            self.status_label.config(text="Updating quantity...", 
                                    foreground=LUXURY_MAIN_COLORS['warning'])
            
            # Update in background thread
            thread = threading.Thread(target=update_quantity, daemon=True)
            thread.start()
            
    def on_quantity_updated(self):
        """Handle successful quantity update."""
        self.status_label.config(text=get_text("quantity_updated"), 
                                foreground=LUXURY_MAIN_COLORS['btn_success'])
        self.refresh_data()
    
    def edit_recent_addition(self):
        """Allow regular users to edit their recent additions within 24 hours."""
        selected_item = self.inventory_view.get_selected_item()
        if not selected_item:
            return
        
        try:
            # البحث عن العمليات الحديثة للمستخدم
            print(f"DEBUG: البحث عن العمليات الحديثة للعنصر: {selected_item['item_name']}")
            print(f"DEBUG: المستخدم: {self.current_user.get('username', '')}")
            recent_additions = self.get_user_recent_additions(
                None,  # لا نحتاج enhanced_manager بعد الآن
                selected_item['item_name'],
                self.current_user.get('username', '')
            )
            
            if not recent_additions:
                messagebox.showinfo(
                    "غير متاح", 
                    f"لم يتم العثور على إضافات حديثة لك في العنصر '{selected_item['item_name']}' خلال آخر 24 ساعة.\n"
                    "يمكنك فقط تعديل الكميات التي أضفتها خلال آخر 24 ساعة."
                )
                return
            
            # عرض نافذة تعديل مخصصة للعمليات الحديثة
            self.show_recent_addition_dialog(selected_item, recent_additions)
            
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في تحليل العمليات الحديثة: {str(e)}")
    
    def get_user_recent_additions(self, enhanced_manager, item_name, username):
        """Get user's recent additions within 24 hours."""
        from datetime import datetime, timedelta
        
        try:
            # الحصول على جميع العمليات من activity sheet مباشرة
            try:
                activity_sheet = self.sheets_manager.spreadsheet.worksheet('Activity_Log_v2_20251108')
            except Exception as e:
                print(f"DEBUG: لا يمكن الوصول لـ activity sheet: {e}")
                return []
            
            all_values = activity_sheet.get_all_values()
            if not all_values or len(all_values) < 2:
                print("DEBUG: لا توجد بيانات في activity sheet")
                return []
            
            headers = all_values[0]
            print(f"DEBUG: Headers في activity sheet: {headers}")
            
            # تصفية العمليات للمستخدم والعنصر خلال آخر 24 ساعة
            recent_additions = []
            cutoff_time = datetime.now() - timedelta(hours=24)
            
            for row in all_values[1:]:  # تجاهل الـ header
                if len(row) >= 12:  # التأكد من وجود جميع الأعمدة
                    date_str = row[0]  # التاريخ
                    time_str = row[1]  # الوقت  
                    operation_type = row[2]  # نوع العملية
                    activity_item = row[3]  # العنصر
                    category = row[4]  # التصنيف
                    quantity_added = row[5]  # الكمية المضافة
                    quantity_removed = row[6]  # الكمية المسحوبة
                    previous_quantity = row[7]  # الكمية السابقة
                    current_quantity = row[8]  # الكمية الحالية
                    recipient_name = row[9]  # اسم المستلم/المستخدم
                    project_number = row[10]  # رقم المشروع
                    details = row[11] if len(row) > 11 else ""  # التفاصيل
                    
                    # التحقق من أن العملية مطابقة
                    # البحث عن عمليات الإضافة أو التحديث التي تتضمن كمية مضافة
                    is_matching_operation = (
                        operation_type in ["إضافة", "تحديث", "إضافة عنصر", "تحديث كمية"] and 
                        activity_item == item_name and 
                        (recipient_name == username or details.find(username) != -1) and
                        float(quantity_added or 0) > 0
                    )
                    
                    if is_matching_operation:
                        try:
                            # تحويل التاريخ والوقت
                            activity_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
                            
                            # التحقق من أن العملية خلال آخر 24 ساعة
                            if activity_datetime >= cutoff_time:
                                print(f"DEBUG: عملية مطابقة وجدت: {operation_type} - {activity_item} - {quantity_added}")
                                recent_additions.append({
                                    'datetime': activity_datetime,
                                    'quantity_added': float(quantity_added or 0),
                                    'operation_type': operation_type,
                                    'details': details
                                })
                        except (ValueError, IndexError) as e:
                            print(f"DEBUG: خطأ في تحويل التاريخ: {e}")
                            continue
            
            print(f"DEBUG: إجمالي العمليات الحديثة الموجودة: {len(recent_additions)}")
            return recent_additions
            
        except Exception as e:
            print(f"DEBUG: خطأ في get_user_recent_additions: {e}")
            return []
    
    def show_recent_addition_dialog(self, selected_item, recent_additions):
        """Show dialog for editing recent additions."""
        total_recent_added = sum(addition['quantity_added'] for addition in recent_additions)
        
        print(f"DEBUG: إجمالي الكمية المضافة حديثاً: {total_recent_added}")
        print(f"DEBUG: الإضافات الحديثة: {recent_additions}")
        
        if total_recent_added <= 0:
            messagebox.showinfo(
                "غير متاح", 
                "لا توجد كميات مضافة حديثة يمكن تعديلها."
            )
            return
        
        # إنشاء نافذة تعديل مخصصة
        dialog_window = tk.Toplevel(self.root)
        dialog_window.title("تعديل آخر كمية مضافة")
        dialog_window.geometry("400x300")
        dialog_window.resizable(False, False)
        dialog_window.transient(self.root)
        dialog_window.grab_set()
        
        # محتوى النافذة
        main_frame = tk.Frame(dialog_window, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # معلومات العنصر
        tk.Label(main_frame, text=f"العنصر: {selected_item['item_name']}", 
                font=("Arial", 12, "bold")).pack(pady=(0, 10))
        tk.Label(main_frame, text=f"الكمية الحالية: {selected_item['quantity']}", 
                font=("Arial", 10)).pack(pady=(0, 5))
        tk.Label(main_frame, text=f"الكمية المضافة خلال آخر 24 ساعة: {total_recent_added}", 
                font=("Arial", 10), fg="green").pack(pady=(0, 15))
        
        # حقل الكمية الجديدة
        tk.Label(main_frame, text="تعديل الكمية المضافة إلى:", 
                font=("Arial", 10)).pack(pady=(0, 5))
        
        quantity_var = tk.StringVar(value=str(total_recent_added))
        
        quantity_entry = tk.Entry(main_frame, textvariable=quantity_var, 
                                 font=("Arial", 12), justify="center", width=10)
        quantity_entry.pack(pady=(0, 10))
        quantity_entry.select_range(0, tk.END)  # تحديد النص لسهولة التعديل
        quantity_entry.focus_set()  # تركيز على الحقل
        
        print(f"DEBUG: تم إنشاء الحقل بالقيمة الافتراضية: {quantity_var.get()}")
        
        # معلومات إضافية
        info_frame = tk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(info_frame, text="📌 يمكنك تعديل الكمية المضافة لأي قيمة موجبة", 
                font=("Arial", 8), fg="blue", wraplength=350).pack()
        tk.Label(info_frame, text="📌 الكمية المضافة الحالية: " + str(int(total_recent_added)), 
                font=("Arial", 8), fg="green").pack()
        
        # الأزرار
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        result = {'value': None}
        
        def on_confirm():
            try:
                # إزالة التركيز من الحقل لضمان حفظ التغييرات
                dialog_window.focus()
                dialog_window.update()  # تحديث النافذة
                
                # قراءة القيمة من الحقل مباشرة
                current_value = quantity_entry.get().strip()
                print(f"DEBUG: القيمة من الحقل مباشرة: '{current_value}'")
                
                # قراءة من المتغير أيضاً للمقارنة
                var_value = quantity_var.get().strip()
                print(f"DEBUG: النص من المتغير: '{var_value}' (length: {len(var_value)})")
                
                # استخدام القيمة من الحقل كأولوية
                input_text = current_value if current_value else var_value
                print(f"DEBUG: القيمة النهائية المستخدمة: '{input_text}'")
                
                if not input_text:
                    messagebox.showerror("خطأ", "يرجى إدخال قيمة")
                    return
                    
                new_quantity = float(input_text)
                print(f"DEBUG: الكمية الجديدة بعد التحويل: {new_quantity}")
                print(f"DEBUG: الكمية المضافة السابقة: {total_recent_added}")
                print(f"DEBUG: هل القيم متساوية؟ {new_quantity == total_recent_added}")
                print(f"DEBUG: نوع المتغير new_quantity: {type(new_quantity)}")
                print(f"DEBUG: نوع المتغير total_recent_added: {type(total_recent_added)}")
                
                # التحقق من صحة القيمة
                if new_quantity < 0:
                    messagebox.showerror("خطأ", "الكمية لا يمكن أن تكون سالبة")
                    return
                
                # إزالة القيد على الكمية الأعلى - السماح بالزيادة عن آخر إضافة
                # إزالة منع العودة للكمية نفسها
                print(f"DEBUG: قبول التعديل - من {total_recent_added} إلى {new_quantity}")
                
                # تأكيد من المستخدم قبل التطبيق
                confirmation_msg = (
                    f"هل تريد تعديل الكمية المضافة من {total_recent_added} إلى {new_quantity}؟\n\n"
                    f"التغيير سيكون: {new_quantity - total_recent_added:+}\n\n"
                    f"القيمة المُدخلة: {new_quantity}\n"
                    f"القيمة الحالية: {total_recent_added}"
                )
                print(f"DEBUG: رسالة التأكيد - القيمة الجديدة: {new_quantity}, القيمة القديمة: {total_recent_added}")
                
                if messagebox.askyesno("تأكيد التعديل", confirmation_msg):
                    result['value'] = new_quantity
                    print(f"DEBUG: تم قبول التأكيد - النتيجة: {result['value']}")
                    print(f"DEBUG: جاري إغلاق النافذة...")
                    dialog_window.destroy()
                    print(f"DEBUG: تم إغلاق النافذة")
                else:
                    print("DEBUG: تم إلغاء العملية من قبل المستخدم")
            except ValueError:
                messagebox.showerror("خطأ", "يرجى إدخال رقم صالح")
        
        def on_cancel():
            dialog_window.destroy()
        
        tk.Button(button_frame, text="تأكيد", command=on_confirm, 
                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(0, 10))
        tk.Button(button_frame, text="إلغاء", command=on_cancel, 
                 bg="#f44336", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        
        # انتظار إغلاق النافذة
        dialog_window.wait_window()
        
        # معالجة النتيجة
        if result['value'] is not None:
            print(f"DEBUG: النتيجة النهائية: {result['value']}")
            print(f"DEBUG: الكمية المضافة الأصلية: {total_recent_added}")
            self.process_recent_addition_edit(selected_item, total_recent_added, result['value'])
        else:
            print("DEBUG: تم إلغاء العملية - لا توجد نتيجة")
    
    def process_recent_addition_edit(self, selected_item, old_added_quantity, new_added_quantity):
        """Process the edit of recent addition."""
        try:
            print(f"DEBUG: بدء معالجة التعديل...")
            print(f"DEBUG: العنصر: {selected_item['item_name']}")
            print(f"DEBUG: القيم المُمررة - القديمة: {old_added_quantity}, الجديدة: {new_added_quantity}")
            
            # تحويل القيم لأرقام
            old_added_quantity = float(old_added_quantity)
            new_added_quantity = float(new_added_quantity)
            current_quantity = float(selected_item['quantity'])
            
            print(f"DEBUG: القيم بعد التحويل - القديمة: {old_added_quantity}, الجديدة: {new_added_quantity}, الحالية: {current_quantity}")
            
            # السماح بجميع التعديلات حتى لو كانت تعيد للكمية نفسها
            # إزالة التحقق من التساوي لأنه قد يكون مرغوب فيه أحياناً
            print(f"DEBUG: معالجة التعديل - من {old_added_quantity} إلى {new_added_quantity}")
            
            # حساب الفرق في الكمية المضافة
            quantity_difference = new_added_quantity - old_added_quantity
            
            # حساب الكمية الجديدة بناءً على التغيير
            new_total_quantity = current_quantity + quantity_difference
            
            print(f"DEBUG: تعديل الكمية الحديثة:")
            print(f"  - الكمية الحالية: {current_quantity}")
            print(f"  - الكمية المضافة السابقة: {old_added_quantity}")
            print(f"  - الكمية المضافة الجديدة: {new_added_quantity}")
            print(f"  - الفرق في الكمية: {quantity_difference}")
            print(f"  - الكمية الجديدة الإجمالية: {new_total_quantity}")
            
            # التحقق من أن الكمية النهائية ليست سالبة
            if new_total_quantity < 0:
                messagebox.showerror("خطأ", f"لا يمكن أن تكون الكمية الإجمالية سالبة\nالكمية الحالية: {current_quantity}\nالتغيير المطلوب: {quantity_difference}\nالنتيجة: {new_total_quantity}")
                return
            
            # التحقق من أن التعديل معقول (لا يمكن تقليل أكثر من الكمية الحالية)
            if quantity_difference < 0 and abs(quantity_difference) > current_quantity:
                messagebox.showerror("خطأ", f"لا يمكن تقليل الكمية بأكثر من الكمية الحالية\nالكمية الحالية: {current_quantity}\nالتقليل المطلوب: {abs(quantity_difference)}")
                return
            
            def update_quantity():
                try:
                    # تحديث الكمية في الشيت
                    print(f"DEBUG: تحديث الكمية في الشيت - الصف: {selected_item['row']}, الكمية الجديدة: {new_total_quantity}")
                    if self.sheets_manager.update_quantity(selected_item["row"], new_total_quantity):
                        # لا حاجة لتسجيل إضافي - update_quantity تسجل تلقائياً
                        # تم إزالة التسجيل المزدوج لتجنب ظهور سطرين
                        
                        self.root.after(0, self.on_recent_addition_updated)
                    else:
                        self.root.after(0, self.on_operation_error, "فشل في تحديث الكمية")
                except Exception as e:
                    self.root.after(0, self.on_operation_error, str(e))
            
            # إظهار حالة التحديث
            self.status_label.config(text="جاري تحديث الكمية المضافة...", 
                                    foreground=LUXURY_MAIN_COLORS['warning'])
            
            # التحديث في خيط منفصل
            thread = threading.Thread(target=update_quantity, daemon=True)
            thread.start()
            
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في معالجة التعديل: {str(e)}")
    
    def on_recent_addition_updated(self):
        """Handle successful recent addition update."""
        self.status_label.config(text="تم تحديث الكمية المضافة بنجاح", 
                                foreground=LUXURY_MAIN_COLORS['btn_success'])
        self.refresh_data()
        
    def outbound_item(self):
        """Open dialog to process outbound items."""
        # التحقق من أن المستخدم العادي منسوب لمشروع
        if (self.current_user and 
            self.current_user.get('user_type') == 'user' and 
            not self.current_user.get('project_id')):
            messagebox.showerror(
                "غير مسموح", 
                "لا يمكنك إخراج عناصر لأنك غير منسوب لأي مشروع.\nيرجى التواصل مع المدير لتعيينك لمشروع."
            )
            return
        
        selected_item = self.inventory_view.get_selected_item()
        if not selected_item:
            return
            
        dialog = OutboundDialog(self.root, selected_item)
        result = dialog.show()
        
        if result:
            outbound_quantity, recipient_name = result
            
            def process_outbound():
                try:
                    if self.sheets_manager.outbound_item(selected_item["row"], outbound_quantity, recipient_name):
                        self.root.after(0, self.on_outbound_processed)
                    else:
                        self.root.after(0, self.on_operation_error, get_text("insufficient_quantity"))
                except Exception as e:
                    self.root.after(0, self.on_operation_error, str(e))
                    
            # Show status
            self.status_label.config(text=get_text("processing_outbound"), 
                                    foreground=LUXURY_MAIN_COLORS['warning'])
            
            # Process in background thread
            thread = threading.Thread(target=process_outbound, daemon=True)
            thread.start()
            
    def on_outbound_processed(self):
        """Handle successful outbound processing."""
        self.status_label.config(text=get_text("outbound_processed"), 
                                foreground=LUXURY_MAIN_COLORS['btn_success'])
        self.refresh_data()
        
    def remove_item(self):
        """Remove the selected item - Admin only."""
        # التحقق من أن المستخدم مدير
        if not self.current_user or self.current_user.get('user_type') != 'admin':
            messagebox.showerror(
                "غير مسموح", 
                "عذراً، حذف العناصر متاح للمديرين فقط.\nيرجى التواصل مع المدير لحذف هذا العنصر."
            )
            return
        
        selected_item = self.inventory_view.get_selected_item()
        if not selected_item:
            return
            
        # Confirm removal
        result = messagebox.askyesno(get_text("confirm_removal"), 
                                   get_text("confirm_remove_item", selected_item['item_name']))
        
        if result:
            def remove_from_sheets():
                try:
                    if self.sheets_manager.remove_item(selected_item["row"]):
                        self.root.after(0, self.on_item_removed)
                    else:
                        self.root.after(0, self.on_operation_error, get_text("operation_failed"))
                except Exception as e:
                    self.root.after(0, self.on_operation_error, str(e))
                    
            # Show status
            self.status_label.config(text=get_text("removing_item"), 
                                    foreground=LUXURY_MAIN_COLORS['warning'])
            
            # Remove in background thread
            thread = threading.Thread(target=remove_from_sheets, daemon=True)
            thread.start()
            
    def on_item_removed(self):
        """Handle successful item removal."""
        self.status_label.config(text=get_text("item_removed"), 
                                foreground=LUXURY_MAIN_COLORS['btn_success'])
        self.refresh_data()
        
    def on_operation_error(self, error_message: str):
        """Handle operation error."""
        self.status_label.config(text=get_text("operation_failed"), 
                                foreground=LUXURY_MAIN_COLORS['btn_danger'])
        messagebox.showerror(get_text("operation_error"), get_text("operation_error_details", error_message))
    
    def open_admin_window(self):
        """فتح نافذة إدارة المشاريع للمدراء فقط."""
        if not self.current_user or self.current_user.get('user_type') != 'admin':
            messagebox.showerror("خطأ", "هذه الميزة متاحة للمدراء فقط!")
            return
        
        try:
            admin_window = AdminProjectsWindow(self.root, self.config)
            admin_window.show()
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في فتح نافذة الإدارة: {e}")
    
    def open_analytics_window(self):
        """عرض رسالة أن ميزة التحليل والرؤى ستكون متاحة قريباً."""
        messagebox.showinfo(
            "📊 تحليل ورؤى البيانات", 
            "🚀 هذه الميزة قيد التطوير وستكون متاحة في الإصدارات القادمة!\n\n"
            "ستتضمن:\n"
            "• 📈 تحليل استهلاك المواد\n"
            "• 📊 إحصائيات المشاريع\n"
            "• 🔍 تقارير مفصلة\n"
            "• 📋 مؤشرات الأداء\n\n"
            "ترقبوا التحديثات القادمة! 🎉"
        )
    
    def open_filter_search_window(self):
        """فتح نافذة الفلاتر المتقدمة والشاملة الجديدة."""
        
        # التأكد من وجود sheets_manager
        if not self.sheets_manager:
            print("⚠️ sheets_manager غير متوفر، محاولة إنشاؤه...")
            try:
                # محاولة إنشاء SheetsManager
                credentials_file = self.config.get('credentials_path', 'config/credentials.json')
                spreadsheet_name = self.config.get('spreadsheet_name', 'Inventory Management')
                
                self.sheets_manager = SheetsManager(credentials_file, spreadsheet_name)
                
                if not self.sheets_manager.connect():
                    messagebox.showerror("خطأ", "فشل في الاتصال بـ Google Sheets!\nيرجى التحقق من إعدادات الاتصال.")
                    return
                    
                print("✅ تم إنشاء والاتصال بـ SheetsManager بنجاح")
                
            except Exception as e:
                print(f"❌ خطأ في إنشاء SheetsManager: {e}")
                messagebox.showerror("خطأ", f"فشل في إنشاء اتصال Google Sheets:\n{str(e)}")
                return
        
        # التأكد من معلومات المستخدم
        if not hasattr(self, 'current_user') or not self.current_user:
            self.current_user = {'username': 'admin', 'user_type': 'admin'}
            print("⚠️ تم استخدام مستخدم افتراضي")
        
        try:
            print("🔍 فتح نظام البحث في سجل العمليات الجديد...")
            
            # استيراد وفتح النظام الجديد المحدث
            from new_activity_filter_system import NewActivityFilterSystem
            
            # إنشاء وفتح النظام الجديد مع الاتصال الموجود ومعلومات المستخدم
            search_system = NewActivityFilterSystem(
                parent=self.root, 
                sheets_manager=self.sheets_manager,
                current_user=self.current_user
            )
            filter_window = search_system.create_window()
            
            if filter_window:
                print("✅ تم فتح نظام البحث في سجل العمليات بنجاح")
                messagebox.showinfo("نجح! 🚀", 
                    "تم فتح نظام البحث والفلاتر الجديد!\n\n"
                    "📊 يقرأ من: Activity_Log_v2_20251108\n\n"
                    "🎛️ الفلاتر المتاحة:\n"
                    "• 📅 فلتر التاريخ (مع نطاق تواريخ)\n"
                    "• 🏷️ فلتر التصنيف\n"
                    "• 📦 فلتر اسم العنصر\n"
                    "• 🎯 فلتر المشروع\n"
                    "• 👤 فلتر المستخدم\n\n"
                    "📈 الإحصائيات المتاحة:\n"
                    "• إجمالي الإدخال والإخراج\n"
                    "• الكمية المتبقية\n"
                    "• عدد العمليات\n\n"
                    "📋 العرض الشامل:\n"
                    "• جميع العمليات مع التواريخ\n"
                    "• تفاصيل كاملة لكل عملية\n"
                    "• فلترة متقدمة ودقيقة\n\n"
                    "🎉 استمتع بالنظام المحسن!")
            else:
                raise Exception("فشل في إنشاء نظام البحث الجديد")
                
        except ImportError as e:
            print(f"❌ خطأ في استيراد نظام البحث الجديد: {e}")
            
            # التراجع للنظام البديل في حالة الخطأ
            try:
                print("🔄 محاولة التراجع للنظام البديل...")
                from gui.fixed_filter_window import FixedFilterWindow
                
                filter_window = FixedFilterWindow(self.sheets_manager)
                
                if filter_window:
                    messagebox.showinfo("تم التراجع للنظام البديل", 
                        "تم فتح النظام البديل بنجاح!\n"
                        "النظام الجديد غير متاح حالياً.")
                        
            except Exception as fallback_e:
                print(f"❌ خطأ في النظام البديل أيضاً: {fallback_e}")
                messagebox.showerror("خطأ", f"فشل في فتح أي نظام فلاتر:\n{str(e)}")
                
        except Exception as e:
            print(f"❌ خطأ في فتح نافذة البحث: {e}")
            messagebox.showerror("خطأ", f"فشل في فتح نافذة البحث: {e}")
    
    def open_old_filters_window(self):
        """فتح نظام الفلاتر التقليدي"""
        
        if not self.sheets_manager:
            messagebox.showerror("خطأ", "لا يوجد اتصال بـ Google Sheets")
            return
        
        try:
            print("🔧 فتح نظام الفلاتر التقليدي...")
            from gui.fixed_filter_window import FixedFilterWindow
            
            filter_window = FixedFilterWindow(self.sheets_manager)
            
            messagebox.showinfo("نظام الفلاتر التقليدي", 
                "تم فتح نظام الفلاتر التقليدي!\n\n"
                "📋 المتاح:\n"
                "• فلاتر أساسية للمخزون\n"
                "• إحصائيات سريعة\n"
                "• عرض بسيط للبيانات\n\n"
                "💡 للحصول على ميزات متقدمة،\n"
                "استخدم 'بحث في سجل العمليات'")
            
        except Exception as e:
            print(f"❌ خطأ في فتح الفلاتر التقليدية: {e}")
            messagebox.showerror("خطأ", f"فشل في فتح الفلاتر التقليدية:\n{str(e)}")
    
    def setup_user_info_bar(self, parent):
        """إعداد شريط معلومات المستخدم وتسجيل الخروج"""
        # إطار شريط المستخدم الفاخر
        user_bar = tk.Frame(parent, 
                           bg=LUXURY_MAIN_COLORS['bg_toolbar'],
                           relief="raised", 
                           bd=2,
                           padx=5, 
                           pady=2)
        user_bar.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        user_bar.columnconfigure(1, weight=1)  # للمساحة الفارغة في الوسط
        
        # معلومات المستخدم على اليسار بتصميم فاخر
        if self.current_user:
            username = self.current_user.get('username', 'غير معروف')
            user_type = self.current_user.get('user_type', 'user')
            user_type_text = "👑 مدير النظام" if user_type == "admin" else "👤 مستخدم عادي"
            
            # أيقونة الترحيب
            welcome_icon = tk.Label(user_bar, 
                                   text="💎", 
                                   font=("Arial", 16),
                                   fg=LUXURY_MAIN_COLORS['primary_gold'],
                                   bg=LUXURY_MAIN_COLORS['bg_toolbar'])
            welcome_icon.grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
            
            welcome_text = f"مرحباً {username}"
            welcome_label = tk.Label(user_bar, text=welcome_text, 
                                    font=("Tahoma", 12, "bold"), 
                                    fg=LUXURY_MAIN_COLORS['text_primary'],
                                    bg=LUXURY_MAIN_COLORS['bg_toolbar'])
            welcome_label.grid(row=0, column=1, sticky=tk.W)
            
            # نوع المستخدم
            user_type_label = tk.Label(user_bar, text=user_type_text, 
                                      font=("Tahoma", 10), 
                                      fg=LUXURY_MAIN_COLORS['text_accent'],
                                      bg=LUXURY_MAIN_COLORS['bg_toolbar'])
            user_type_label.grid(row=1, column=1, sticky=tk.W, pady=(2, 0))
        
        # زر تسجيل الخروج الفاخر على اليمين
        logout_btn = tk.Button(user_bar, text="🚪 تسجيل الخروج", 
                              command=self.logout,
                              bg=LUXURY_MAIN_COLORS['error'], 
                              fg=LUXURY_MAIN_COLORS['text_primary'], 
                              activebackground='#C0392B',
                              activeforeground=LUXURY_MAIN_COLORS['text_primary'],
                              font=("Tahoma", 10, "bold"),
                              padx=15, pady=6,
                              width=12,
                              relief="raised", bd=2,
                              cursor="hand2")
        logout_btn.grid(row=0, rowspan=2, column=2, sticky=tk.E)
        
        # تأثيرات hover لزر تسجيل الخروج
        def on_logout_enter(e):
            logout_btn.config(bg='#C0392B')
        
        def on_logout_leave(e):
            logout_btn.config(bg=LUXURY_MAIN_COLORS['error'])
        
        logout_btn.bind("<Enter>", on_logout_enter)
        logout_btn.bind("<Leave>", on_logout_leave)
        
        # حفظ المرجع للاستخدام من التطبيق الرئيسي
        self.user_info_bar = user_bar
        self.logout_button = logout_btn
    
    def logout(self):
        """دالة تسجيل الخروج - ستربط بالتطبيق الرئيسي"""
        # سيتم استبدال هذه الدالة من قبل التطبيق الرئيسي
        if hasattr(self, 'logout_callback') and callable(self.logout_callback):
            self.logout_callback()
        else:
            messagebox.showinfo("تسجيل الخروج", "يرجى إغلاق التطبيق يدوياً")