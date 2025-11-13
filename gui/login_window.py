"""
نافذة تسجيل الدخول - واجهة رسومية لتسجيل الدخول
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from sheets.users_manager import UsersManager
from config.settings import load_config

# مخطط الألوان الفاخر لنافذة تسجيل الدخول
LUXURY_LOGIN_COLORS = {
    # الألوان الأساسية - درجات الذهبي والأزرق الداكن
    'primary_gold': '#DAA520',           # ذهبي داكن
    'primary_dark': '#1A1A2E',          # أزرق داكن عميق
    'secondary_gold': '#FFD700',        # ذهبي فاتح
    'secondary_dark': '#16213E',        # أزرق داكن ثانوي
    
    # ألوان الخلفية
    'bg_main': '#0F1419',              # خلفية رئيسية داكنة
    'bg_card': '#1E2A4A',              # خلفية البطاقات
    'bg_input': '#2C3E60',             # خلفية حقول الإدخال
    'bg_hover': '#34495E',             # لون عند التمرير
    
    # ألوان النصوص
    'text_primary': '#FFFFFF',         # نص أبيض رئيسي
    'text_secondary': '#BDC3C7',       # نص رمادي فاتح
    'text_accent': '#F39C12',          # نص ذهبي للتأكيد
    'text_placeholder': '#95A5A6',     # نص placeholder
    
    # ألوان الحالة
    'success': '#27AE60',              # أخضر للنجاح
    'warning': '#F39C12',              # برتقالي للتحذير
    'error': '#E74C3C',                # أحمر للخطأ
    'info': '#3498DB',                 # أزرق للمعلومات
}

class LoginWindow:
    """نافذة تسجيل الدخول"""
    
    def __init__(self, on_login_success=None):
        """
        تهيئة نافذة تسجيل الدخول
        
        Args:
            on_login_success: دالة يتم استدعاؤها عند نجاح تسجيل الدخول
        """
        self.on_login_success = on_login_success
        self.users_manager = None
        self.user_info = None
        
        # إنشاء النافذة الرئيسية بتصميم فاخر
        self.root = tk.Tk()
        self.root.title("🔐 تسجيل الدخول - نظام إدارة المخزون ")
        self.root.geometry("450x550")
        self.root.resizable(False, False)
        
        # تطبيق الألوان الفاخرة
        self.root.configure(bg=LUXURY_LOGIN_COLORS['bg_main'])
        
        # تعيين أيقونة النافذة (إذا كانت متوفرة)
        try:
            # يمكن إضافة أيقونة هنا لاحقاً
            pass
        except:
            pass
        
        # تعيين النافذة في الوسط
        self.center_window()
        
        # تحميل الإعدادات
        self.config = load_config()
        
        # إنشاء واجهة المستخدم
        self.setup_ui()
        
        # تهيئة مدير المستخدمين
        self.initialize_users_manager()
    
    def center_window(self):
        """توسيط النافذة في الشاشة"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_ui(self):
        """إنشاء واجهة المستخدم الفاخرة"""
        # الإطار الرئيسي الفاخر
        main_frame = tk.Frame(self.root, 
                             bg=LUXURY_LOGIN_COLORS['bg_main'],
                             padx=30, 
                             pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # إطار الشعار والعنوان
        header_frame = tk.Frame(main_frame, bg=LUXURY_LOGIN_COLORS['bg_main'])
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        # العنوان الفاخر مع الأيقونات
        title_label = tk.Label(header_frame, 
                              text="تسجيل الدخول", 
                              font=("Tahoma", 22, "bold"),
                              fg=LUXURY_LOGIN_COLORS['primary_gold'],
                              bg=LUXURY_LOGIN_COLORS['bg_main'])
        title_label.pack(pady=(0, 5))
        
        # العنوان الفرعي
        subtitle_label = tk.Label(header_frame,
                                 text="✨نظام إدارة المخزون✨",
                                 font=("Tahoma", 12),
                                 fg=LUXURY_LOGIN_COLORS['text_secondary'],
                                 bg=LUXURY_LOGIN_COLORS['bg_main'])
        subtitle_label.pack(pady=(0, 10))
        
        # خط فاصل ذهبي
        separator = tk.Frame(header_frame, 
                            height=2, 
                            bg=LUXURY_LOGIN_COLORS['primary_gold'])
        separator.pack(fill=tk.X, padx=50)
        
        # إطار حقول الإدخال
        input_frame = tk.Frame(main_frame, bg=LUXURY_LOGIN_COLORS['bg_main'])
        input_frame.pack(fill=tk.X, pady=(30, 20))
        
        # حقل اسم المستخدم
        username_label = tk.Label(input_frame, 
                                 text="👤 اسم المستخدم", 
                                 font=("Tahoma", 12, "bold"),
                                 fg=LUXURY_LOGIN_COLORS['text_primary'],
                                 bg=LUXURY_LOGIN_COLORS['bg_main'])
        username_label.pack(anchor=tk.W, pady=(0, 8))
        
        self.username_var = tk.StringVar()
        self.username_entry = tk.Entry(input_frame, 
                                      textvariable=self.username_var,
                                      font=("Tahoma", 12),
                                      bg=LUXURY_LOGIN_COLORS['bg_input'],
                                      fg=LUXURY_LOGIN_COLORS['text_primary'],
                                      insertbackground=LUXURY_LOGIN_COLORS['primary_gold'],
                                      bd=2,
                                      relief='raised',
                                      width=30)
        self.username_entry.pack(fill=tk.X, pady=(0, 20), ipady=8)
        
        # حقل كلمة المرور
        password_label = tk.Label(input_frame, 
                                 text="🔒 كلمة المرور", 
                                 font=("Tahoma", 12, "bold"),
                                 fg=LUXURY_LOGIN_COLORS['text_primary'],
                                 bg=LUXURY_LOGIN_COLORS['bg_main'])
        password_label.pack(anchor=tk.W, pady=(0, 8))
        
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(input_frame, 
                                      textvariable=self.password_var,
                                      font=("Tahoma", 12),
                                      bg=LUXURY_LOGIN_COLORS['bg_input'],
                                      fg=LUXURY_LOGIN_COLORS['text_primary'],
                                      insertbackground=LUXURY_LOGIN_COLORS['primary_gold'],
                                      bd=2,
                                      relief='raised',
                                      width=30,
                                      show="*")
        self.password_entry.pack(fill=tk.X, pady=(0, 25), ipady=8)
        
        # إطار الأزرار الفاخر
        buttons_frame = tk.Frame(main_frame, bg=LUXURY_LOGIN_COLORS['bg_main'])
        buttons_frame.pack(fill=tk.X, pady=(10, 20))
        
        # زر تسجيل الدخول الذهبي مع تأثيرات
        self.login_btn = tk.Button(buttons_frame, 
                                  text="🚀 تسجيل الدخول",
                                  command=self.login,
                                  font=("Tahoma", 14, "bold"),
                                  bg=LUXURY_LOGIN_COLORS['primary_gold'],
                                  fg=LUXURY_LOGIN_COLORS['primary_dark'],
                                  activebackground=LUXURY_LOGIN_COLORS['secondary_gold'],
                                  activeforeground=LUXURY_LOGIN_COLORS['primary_dark'],
                                  bd=3,
                                  relief='raised',
                                  padx=25,
                                  pady=10,
                                  cursor='hand2')
        self.login_btn.pack(side=tk.TOP, fill=tk.X, pady=(0, 10))
        
        # إضافة تأثيرات hover للزر
        def on_login_enter(e):
            self.login_btn.config(bg=LUXURY_LOGIN_COLORS['secondary_gold'])
        
        def on_login_leave(e):
            self.login_btn.config(bg=LUXURY_LOGIN_COLORS['primary_gold'])
        
        self.login_btn.bind("<Enter>", on_login_enter)
        self.login_btn.bind("<Leave>", on_login_leave)
        
        # زر إنشاء حساب جديد مع تأثيرات
        self.register_btn = tk.Button(buttons_frame, 
                                     text="➕ إنشاء حساب جديد",
                                     command=self.open_register_window,
                                     font=("Tahoma", 12, "bold"),
                                     bg=LUXURY_LOGIN_COLORS['bg_card'],
                                     fg=LUXURY_LOGIN_COLORS['text_primary'],
                                     activebackground=LUXURY_LOGIN_COLORS['bg_hover'],
                                     activeforeground=LUXURY_LOGIN_COLORS['text_primary'],
                                     bd=2,
                                     relief='raised',
                                     padx=20,
                                     pady=8,
                                     cursor='hand2')
        self.register_btn.pack(side=tk.TOP, fill=tk.X)
        
        # إضافة تأثيرات hover للزر الثاني
        def on_register_enter(e):
            self.register_btn.config(bg=LUXURY_LOGIN_COLORS['bg_hover'])
        
        def on_register_leave(e):
            self.register_btn.config(bg=LUXURY_LOGIN_COLORS['bg_card'])
        
        self.register_btn.bind("<Enter>", on_register_enter)
        self.register_btn.bind("<Leave>", on_register_leave)
        
        # إطار الحالة الفاخر
        status_frame = tk.LabelFrame(main_frame, 
                                    text="📊 الحالة", 
                                    font=("Tahoma", 10, "bold"),
                                    fg=LUXURY_LOGIN_COLORS['text_accent'],
                                    bg=LUXURY_LOGIN_COLORS['bg_main'],
                                    bd=2,
                                    relief='sunken')
        status_frame.pack(fill=tk.X, pady=(15, 0))
        
        # تسمية الحالة
        self.status_label = tk.Label(status_frame, 
                                    text="✅ جاهز لتسجيل الدخول",
                                    font=("Tahoma", 10),
                                    fg=LUXURY_LOGIN_COLORS['success'],
                                    bg=LUXURY_LOGIN_COLORS['bg_main'])
        self.status_label.pack(pady=8)
        
        # شريط التقدم (سيتم تخصيصه لاحقاً)
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        # ربط Enter بتسجيل الدخول
        self.root.bind('<Return>', lambda e: self.login())
        
        # تركيز على حقل اسم المستخدم
        self.username_entry.focus()
        self.username_entry.focus()
    
    def initialize_users_manager(self):
        """تهيئة مدير المستخدمين في خيط منفصل"""
        def init_users():
            try:
                self.update_status("جاري الاتصال بقاعدة البيانات...")
                self.show_progress()
                
                if not self.config:
                    self.update_status("❌ فشل في تحميل الإعدادات")
                    self.hide_progress()
                    return
                
                # إنشاء مدير المستخدمين
                self.users_manager = UsersManager(
                    credentials_file=self.config.get('credentials_file', ''),
                    spreadsheet_name=self.config.get('spreadsheet_name', '')
                )
                
                # محاولة الاتصال
                if self.users_manager.connect():
                    self.update_status("✅ تم الاتصال بقاعدة البيانات بنجاح")
                    
                    # التحقق من وجود مستخدم أدمن
                    if not self.users_manager.user_exists("admin"):
                        self.update_status("إنشاء حساب الأدمن الافتراضي...")
                        self.users_manager.create_admin_user()
                        
                    self.update_status("جاهز لتسجيل الدخول")
                else:
                    self.update_status("❌ فشل في الاتصال بقاعدة البيانات")
                
                self.hide_progress()
                
            except Exception as e:
                self.update_status(f"❌ خطأ: {str(e)}")
                self.hide_progress()
        
        # تشغيل التهيئة في خيط منفصل
        thread = threading.Thread(target=init_users, daemon=True)
        thread.start()
    
    def update_status(self, message):
        """تحديث رسالة الحالة مع ألوان فاخرة"""
        def update():
            # تحديد لون الرسالة حسب المحتوى
            if "✅" in message or "تم" in message or "جاهز" in message:
                color = LUXURY_LOGIN_COLORS['success']
            elif "❌" in message or "خطأ" in message or "فشل" in message:
                color = LUXURY_LOGIN_COLORS['error']  
            elif "جاري" in message or "انتظار" in message:
                color = LUXURY_LOGIN_COLORS['warning']
            elif "💎" in message or "فاخر" in message:
                color = LUXURY_LOGIN_COLORS['primary_gold']
            else:
                color = LUXURY_LOGIN_COLORS['info']
                
            self.status_label.config(text=message, fg=color)
        
        if threading.current_thread() == threading.main_thread():
            update()
        else:
            self.root.after(0, update)
    
    def show_progress(self):
        """إظهار شريط التقدم"""
        def show():
            self.progress.start()
        
        if threading.current_thread() == threading.main_thread():
            show()
        else:
            self.root.after(0, show)
    
    def hide_progress(self):
        """إخفاء شريط التقدم"""
        def hide():
            self.progress.stop()
        
        if threading.current_thread() == threading.main_thread():
            hide()
        else:
            self.root.after(0, hide)
    
    def login(self):
        """تسجيل الدخول"""
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        
        # التحقق من البيانات
        if not username:
            messagebox.showerror("خطأ", "يرجى إدخال اسم المستخدم")
            self.username_entry.focus()
            return
        
        if not password:
            messagebox.showerror("خطأ", "يرجى إدخال كلمة المرور")
            self.password_entry.focus()
            return
        
        if not self.users_manager:
            messagebox.showerror("خطأ", "لم يتم الاتصال بقاعدة البيانات بعد")
            return
        
        # تعطيل الأزرار أثناء المعالجة
        self.login_btn.config(state="disabled")
        self.register_btn.config(state="disabled")
        
        def authenticate():
            try:
                self.update_status("جاري التحقق من البيانات...")
                self.show_progress()
                
                # التحقق من صحة البيانات
                user_info = self.users_manager.authenticate_user(username, password)
                
                if user_info:
                    self.user_info = user_info
                    self.update_status("✅ تم تسجيل الدخول بنجاح")
                    self.hide_progress()
                    
                    # إغلاق نافذة تسجيل الدخول
                    self.root.after(1000, self.on_successful_login)
                else:
                    self.update_status("❌ اسم المستخدم أو كلمة المرور غير صحيحة")
                    self.hide_progress()
                    self.root.after(0, lambda: messagebox.showerror(
                        "خطأ في تسجيل الدخول", 
                        "اسم المستخدم أو كلمة المرور غير صحيحة"
                    ))
                
            except Exception as e:
                self.update_status(f"❌ خطأ: {str(e)}")
                self.hide_progress()
                self.root.after(0, lambda: messagebox.showerror("خطأ", f"حدث خطأ: {str(e)}"))
            
            finally:
                # إعادة تفعيل الأزرار
                self.root.after(0, lambda: self.login_btn.config(state="normal"))
                self.root.after(0, lambda: self.register_btn.config(state="normal"))
        
        # تشغيل التحقق في خيط منفصل
        thread = threading.Thread(target=authenticate, daemon=True)
        thread.start()
    
    def on_successful_login(self):
        """معالجة نجاح تسجيل الدخول"""
        if self.on_login_success and self.user_info:
            self.on_login_success(self.user_info)
        
        self.root.destroy()
    
    def open_register_window(self):
        """فتح نافذة إنشاء حساب جديد"""
        try:
            from gui.register_window import RegisterWindow
            register_window = RegisterWindow(self.users_manager, self.root)
            register_window.show()
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في فتح نافذة التسجيل: {str(e)}")
    
    def show(self):
        """عرض النافذة"""
        self.root.mainloop()
        return self.user_info

# اختبار النافذة
if __name__ == "__main__":
    def on_login(user_info):
        print(f"تم تسجيل دخول المستخدم: {user_info}")
    
    login_window = LoginWindow(on_login_success=on_login)
    user_info = login_window.show()
    
    if user_info:
        print(f"✅ نجح تسجيل الدخول: {user_info['username']}")
    else:
        print("❌ لم يتم تسجيل الدخول")
