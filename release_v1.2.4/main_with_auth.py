"""
نقطة البداية الرئيسية للتطبيق مع نظام تسجيل الدخول
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os
import socket
import urllib.request
import urllib.error

# إضافة مسار المشروع
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# فحص الإعداد الأولي
def check_initial_setup():
    """فحص إذا كان الإعداد الأولي مطلوب"""
    if not os.path.exists('config/credentials.json'):
        print("🔧 الإعداد الأولي مطلوب...")
        try:
            from setup_wizard import SetupWizard
            wizard = SetupWizard()
            wizard.run()
            return True
        except Exception as e:
            messagebox.showerror(
                "خطأ في الإعداد", 
                f"فشل في تشغيل معالج الإعداد:\n{str(e)}\n\nيرجى إعداد ملف config/credentials.json يدوياً"
            )
            return False
    return False

from gui.login_window import LoginWindow
from gui.main_window import MainWindow
from config.settings import load_config

# نظام التحديث التلقائي
try:
    from auto_updater import init_auto_updater
    AUTO_UPDATE_AVAILABLE = True
except ImportError:
    AUTO_UPDATE_AVAILABLE = False
    print("⚠️ نظام التحديث التلقائي غير متاح")

def check_internet_connection():
    """فحص الاتصال بالإنترنت"""
    try:
        # محاولة الاتصال بـ Google DNS
        socket.setdefaulttimeout(3)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
        return True
    except socket.error:
        try:
            # محاولة بديلة - فحص الاتصال بـ Google
            urllib.request.urlopen('http://www.google.com', timeout=3)
            return True
        except urllib.error.URLError:
            return False

def show_no_internet_message():
    """عرض رسالة عدم وجود اتصال بالإنترنت"""
    root = tk.Tk()
    root.withdraw()  # إخفاء النافذة الرئيسية
    
    result = messagebox.askretrycancel(
        "⚠️ لا يوجد اتصال بالإنترنت", 
        "لا يمكن الاتصال بالإنترنت!\n\n"
        "يرجى التأكد من:\n"
        "• الاتصال بالإنترنت\n"
        "• إعدادات الشبكة\n"
        "• جدار الحماية\n\n"
        "اضغط 'إعادة المحاولة' للتحقق مرة أخرى\n"
        "أو 'إلغاء' للخروج من التطبيق"
    )
    root.destroy()
    return result

class InventoryApp:
    """التطبيق الرئيسي مع نظام تسجيل الدخول"""
    
    def __init__(self):
        """تهيئة التطبيق"""
        self.current_user = None
        self.main_window = None
        self.config = load_config()
        
    def start(self):
        """بدء التطبيق"""
        print("🚀 بدء تشغيل نظام إدارة المخزون...")
        
        # فحص الإعداد الأولي أولاً
        if check_initial_setup():
            print("✅ تم اكتمال الإعداد الأولي، إعادة تشغيل التطبيق...")
            # إعادة تحميل الإعدادات بعد الإعداد
            self.config = load_config()
        
        # فحص الاتصال بالإنترنت
        print("🔍 فحص الاتصال بالإنترنت...")
        while not check_internet_connection():
            print("❌ لا يوجد اتصال بالإنترنت")
            retry = show_no_internet_message()
            if not retry:  # إذا اختار المستخدم إلغاء
                print("❌ تم إغلاق التطبيق بسبب عدم وجود اتصال بالإنترنت")
                return False
            print("🔄 إعادة فحص الاتصال...")
        
        print("✅ تم التأكد من وجود اتصال بالإنترنت")
        
        # التحقق من الإعدادات
        if not self.config:
            messagebox.showerror("خطأ", "فشل في تحميل إعدادات التطبيق")
            return False
        
        # عرض نافذة تسجيل الدخول
        print("📋 عرض نافذة تسجيل الدخول...")
        self.show_login()
        
        return True
    
    def show_login(self):
        """عرض نافذة تسجيل الدخول"""
        self.login_window = LoginWindow(on_login_success=self.on_login_success)
        user_info = self.login_window.show()
        
        if not user_info:
            print("❌ لم يتم تسجيل الدخول - إغلاق التطبيق")
            return False
    
    def on_login_success(self, user_info):
        """معالجة نجاح تسجيل الدخول"""
        self.current_user = user_info
        print(f"🎉 مرحباً {user_info['username']} ({user_info['user_type']})")
        
        # إخفاء نافذة تسجيل الدخول
        if hasattr(self, 'login_window') and self.login_window.root:
            self.login_window.root.withdraw()
            print("👁️ تم إخفاء نافذة تسجيل الدخول")
        
        # فتح النافذة الرئيسية
        self.open_main_window()
    
    def open_main_window(self):
        """فتح النافذة الرئيسية للتطبيق"""
        try:
            print("🖥️ فتح النافذة الرئيسية...")
            
            # إنشاء النافذة الرئيسية
            root = tk.Tk()
            
            # تخصيص العنوان حسب المستخدم
            username = self.current_user['username']
            user_type = self.current_user['user_type']
            user_type_text = "مدير" if user_type == "admin" else "مستخدم"
            
            root.title(f"نظام إدارة المخزون - {user_type_text}: {username}")
            
            # إنشاء النافذة الرئيسية
            self.main_window = MainWindow(root, self.config)
            
            # إضافة معلومات المستخدم الحالي
            self.main_window.current_user = self.current_user
            
            # ربط دالة تسجيل الخروج
            self.main_window.logout_callback = self.logout
            
            # معالج إغلاق النافذة الرئيسية
            root.protocol("WM_DELETE_WINDOW", self.on_main_window_close)
            
            # تشغيل النافذة
            root.mainloop()
            
        except Exception as e:
            print(f"❌ خطأ في فتح النافذة الرئيسية: {e}")
            messagebox.showerror("خطأ", f"فشل في فتح النافذة الرئيسية:\n{str(e)}")
    
    def logout(self):
        """تسجيل الخروج"""
        result = messagebox.askyesno(
            "تسجيل الخروج",
            f"هل تريد تسجيل الخروج من حساب '{self.current_user['username']}'؟"
        )
        
        if result:
            print(f"👋 تسجيل خروج المستخدم: {self.current_user['username']}")
            
            # إغلاق النافذة الرئيسية
            if self.main_window and hasattr(self.main_window, 'root'):
                self.main_window.root.destroy()
            
            # إظهار نافذة تسجيل الدخول مرة أخرى إذا كانت مخفية
            if hasattr(self, 'login_window') and self.login_window.root:
                self.login_window.root.deiconify()
                print("👁️ تم إظهار نافذة تسجيل الدخول مرة أخرى")
            else:
                # إنشاء نافذة تسجيل دخول جديدة
                self.current_user = None
                self.main_window = None
                self.show_login()
    
    def on_main_window_close(self):
        """معالج إغلاق النافذة الرئيسية"""
        # سؤال المستخدم عن الخروج
        result = messagebox.askyesno(
            "إغلاق التطبيق", 
            "هل تريد إغلاق التطبيق نهائياً أم العودة لنافذة تسجيل الدخول؟\n\nاضغط 'نعم' للخروج نهائياً\nاضغط 'لا' للعودة لتسجيل الدخول"
        )
        
        if result:  # إغلاق نهائي
            print("🔚 إغلاق التطبيق نهائياً")
            if hasattr(self, 'login_window') and self.login_window.root:
                self.login_window.root.destroy()
            self.main_window.root.destroy()
        else:  # العودة لتسجيل الدخول
            print("🔄 العودة لنافذة تسجيل الدخول")
            self.logout()

def main():
    """الدالة الرئيسية"""
    try:
        # تهيئة نظام التحديث التلقائي
        auto_updater = None
        if AUTO_UPDATE_AVAILABLE:
            try:
                print("🔄 تهيئة نظام التحديث التلقائي...")
                auto_updater = init_auto_updater()
                if auto_updater:
                    print("✅ تم تهيئة نظام التحديث التلقائي")
                else:
                    print("⚠️ فشل في تهيئة نظام التحديث التلقائي")
            except Exception as e:
                print(f"⚠️ خطأ في نظام التحديث: {e}")
        
        # إنشاء وتشغيل التطبيق
        app = InventoryApp()
        app.auto_updater = auto_updater  # ربط نظام التحديث بالتطبيق
        success = app.start()
        
        if not success:
            print("❌ فشل في تشغيل التطبيق")
            return 1
        
        print("✅ تم إغلاق التطبيق بنجاح")
        return 0
        
    except KeyboardInterrupt:
        print("\n⚠️ تم إيقاف التطبيق بواسطة المستخدم")
        return 1
    except Exception as e:
        print(f"💥 خطأ غير متوقع: {e}")
        messagebox.showerror("خطأ", f"حدث خطأ غير متوقع:\n{str(e)}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)