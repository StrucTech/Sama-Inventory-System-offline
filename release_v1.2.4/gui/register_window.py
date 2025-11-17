"""
نافذة تسجيل حساب جديد - واجهة رسومية لإنشاء حسابات جديدة
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import re

class RegisterWindow:
    """نافذة تسجيل حساب جديد"""
    
    def __init__(self, users_manager, parent_window=None):
        """
        تهيئة نافذة تسجيل حساب جديد
        
        Args:
            users_manager: مدير المستخدمين
            parent_window: النافذة الأصلية
        """
        self.users_manager = users_manager
        self.parent_window = parent_window
        
        # إنشاء النافذة
        self.window = tk.Toplevel() if parent_window else tk.Tk()
        self.window.title("إنشاء حساب جديد - نظام إدارة المخزون")
        self.window.geometry("450x500")
        self.window.resizable(False, False)
        
        # تعيين النافذة في الوسط
        self.center_window()
        
        # جعل النافذة دائماً في المقدمة
        if parent_window:
            self.window.transient(parent_window)
            self.window.grab_set()
        
        # إنشاء واجهة المستخدم
        self.setup_ui()
    
    def center_window(self):
        """توسيط النافذة في الشاشة"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_ui(self):
        """إنشاء واجهة المستخدم"""
        # الإطار الرئيسي
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # العنوان
        title_label = ttk.Label(main_frame, text="➕ إنشاء حساب جديد", 
                               font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # معلومات المستخدم
        user_frame = ttk.LabelFrame(main_frame, text="معلومات المستخدم", padding="15")
        user_frame.grid(row=1, column=0, columnspan=2, pady=(0, 15), 
                       sticky=(tk.W, tk.E))
        
        # اسم المستخدم
        ttk.Label(user_frame, text="👤 اسم المستخدم:", 
                 font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(user_frame, textvariable=self.username_var,
                                       font=("Arial", 12), width=25)
        self.username_entry.grid(row=1, column=0, pady=(0, 10), ipady=3)
        
        # تسمية توضيحية
        ttk.Label(user_frame, text="• 3 أحرف على الأقل\n• حروف وأرقام فقط", 
                 font=("Arial", 8), foreground="gray").grid(row=2, column=0, 
                                                           sticky=tk.W, pady=(0, 15))
        
        # كلمة المرور
        ttk.Label(user_frame, text="🔒 كلمة المرور:", 
                 font=("Arial", 10)).grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(user_frame, textvariable=self.password_var,
                                       font=("Arial", 12), width=25, show="*")
        self.password_entry.grid(row=4, column=0, pady=(0, 10), ipady=3)
        
        # تسمية توضيحية
        ttk.Label(user_frame, text="• 4 أحرف على الأقل\n• مزيج من الحروف والأرقام مُفضل", 
                 font=("Arial", 8), foreground="gray").grid(row=5, column=0, 
                                                           sticky=tk.W, pady=(0, 15))
        
        # تأكيد كلمة المرور
        ttk.Label(user_frame, text="🔒 تأكيد كلمة المرور:", 
                 font=("Arial", 10)).grid(row=6, column=0, sticky=tk.W, pady=(0, 5))
        
        self.confirm_password_var = tk.StringVar()
        self.confirm_password_entry = ttk.Entry(user_frame, 
                                               textvariable=self.confirm_password_var,
                                               font=("Arial", 12), width=25, show="*")
        self.confirm_password_entry.grid(row=7, column=0, pady=(0, 15), ipady=3)
        
        # تعيين نوع المستخدم كمستخدم عادي افتراضياً (للأمان)
        self.user_type_var = tk.StringVar(value="user")
        
        # أزرار العمليات
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=2, column=0, columnspan=2, pady=(20, 15))
        
        # زر إنشاء الحساب
        self.create_btn = ttk.Button(buttons_frame, text="🚀 إنشاء الحساب",
                                    command=self.create_account, style="Accent.TButton")
        self.create_btn.grid(row=0, column=0, padx=(0, 10), ipadx=15, ipady=5)
        
        # زر الإلغاء
        self.cancel_btn = ttk.Button(buttons_frame, text="❌ إلغاء",
                                    command=self.cancel)
        self.cancel_btn.grid(row=0, column=1, padx=(10, 0), ipadx=15, ipady=5)
        
        # إطار الحالة
        status_frame = ttk.LabelFrame(main_frame, text="الحالة", padding="10")
        status_frame.grid(row=3, column=0, columnspan=2, pady=(20, 0), 
                         sticky=(tk.W, tk.E))
        
        # تسمية الحالة
        self.status_label = ttk.Label(status_frame, text="جاهز لإنشاء حساب جديد",
                                     font=("Arial", 9))
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        # شريط التقدم
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # ربط Enter بإنشاء الحساب
        self.window.bind('<Return>', lambda e: self.create_account())
        
        # تركيز على حقل اسم المستخدم
        self.username_entry.focus()
    
    def validate_input(self) -> tuple:
        """
        التحقق من صحة البيانات المدخلة
        
        Returns:
            (is_valid, error_message)
        """
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        confirm_password = self.confirm_password_var.get().strip()
        user_type = self.user_type_var.get()
        
        # التحقق من اسم المستخدم
        if not username:
            return False, "يرجى إدخال اسم المستخدم"
        
        if len(username) < 3:
            return False, "اسم المستخدم يجب أن يكون 3 أحرف على الأقل"
        
        if not re.match("^[a-zA-Z0-9_]+$", username):
            return False, "اسم المستخدم يجب أن يحتوي على حروف وأرقام فقط"
        
        # التحقق من كلمة المرور
        if not password:
            return False, "يرجى إدخال كلمة المرور"
        
        if len(password) < 4:
            return False, "كلمة المرور يجب أن تكون 4 أحرف على الأقل"
        
        # التحقق من تطابق كلمة المرور
        if password != confirm_password:
            return False, "كلمة المرور وتأكيدها غير متطابقتين"
        
        return True, ""
    
    def create_account(self):
        """إنشاء الحساب الجديد"""
        # التحقق من صحة البيانات
        is_valid, error_message = self.validate_input()
        if not is_valid:
            messagebox.showerror("خطأ في البيانات", error_message)
            return
        
        if not self.users_manager:
            messagebox.showerror("خطأ", "مدير المستخدمين غير متاح")
            return
        
        # تعطيل الأزرار أثناء المعالجة
        self.create_btn.config(state="disabled")
        self.cancel_btn.config(state="disabled")
        
        def create_user():
            try:
                self.update_status("جاري إنشاء الحساب...")
                self.show_progress()
                
                username = self.username_var.get().strip()
                password = self.password_var.get().strip()
                user_type = self.user_type_var.get()
                
                # محاولة إنشاء المستخدم
                success = self.users_manager.create_user(username, password, user_type)
                
                if success:
                    self.update_status("✅ تم إنشاء الحساب بنجاح")
                    self.hide_progress()
                    
                    # رسالة نجاح
                    self.window.after(0, lambda: messagebox.showinfo(
                        "نجح الإنشاء", 
                        f"تم إنشاء حساب '{username}' بنجاح!\nيمكنك الآن تسجيل الدخول."
                    ))
                    
                    # إغلاق النافذة
                    self.window.after(1000, self.cancel)
                else:
                    self.update_status("❌ فشل في إنشاء الحساب")
                    self.hide_progress()
                    
                    self.window.after(0, lambda: messagebox.showerror(
                        "خطأ", "فشل في إنشاء الحساب. يرجى المحاولة مرة أخرى."
                    ))
                
            except Exception as e:
                self.update_status(f"❌ خطأ: {str(e)}")
                self.hide_progress()
                self.window.after(0, lambda: messagebox.showerror("خطأ", f"حدث خطأ: {str(e)}"))
            
            finally:
                # إعادة تفعيل الأزرار
                self.window.after(0, lambda: self.create_btn.config(state="normal"))
                self.window.after(0, lambda: self.cancel_btn.config(state="normal"))
        
        # تشغيل الإنشاء في خيط منفصل
        thread = threading.Thread(target=create_user, daemon=True)
        thread.start()
    
    def update_status(self, message):
        """تحديث رسالة الحالة"""
        def update():
            self.status_label.config(text=message)
        
        if threading.current_thread() == threading.main_thread():
            update()
        else:
            self.window.after(0, update)
    
    def show_progress(self):
        """إظهار شريط التقدم"""
        def show():
            self.progress.start()
        
        if threading.current_thread() == threading.main_thread():
            show()
        else:
            self.window.after(0, show)
    
    def hide_progress(self):
        """إخفاء شريط التقدم"""
        def hide():
            self.progress.stop()
        
        if threading.current_thread() == threading.main_thread():
            hide()
        else:
            self.window.after(0, hide)
    
    def cancel(self):
        """إلغاء وإغلاق النافذة"""
        self.window.destroy()
    
    def show(self):
        """عرض النافذة"""
        self.window.mainloop()

# اختبار النافذة
if __name__ == "__main__":
    # محاكاة مدير المستخدمين
    class MockUsersManager:
        def create_user(self, username, password, user_type):
            print(f"إنشاء مستخدم: {username}, كلمة المرور: {password}, النوع: {user_type}")
            return True
    
    mock_manager = MockUsersManager()
    register_window = RegisterWindow(mock_manager)
    register_window.show()