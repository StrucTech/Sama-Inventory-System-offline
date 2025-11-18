"""
نظام التحديث التلقائي للبرنامج
يتحقق من التحديثات ويحملها تلقائياً
"""

import os
import sys
import json
import requests
import zipfile
import shutil
import subprocess
import threading
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import hashlib
from datetime import datetime, timedelta

class AutoUpdater:
    """كلاس التحديث التلقائي"""
    
    def __init__(self, config_file="update_info.json"):
        self.config_file = config_file
        self.current_version = None
        self.update_url = None
        self.check_interval = 0  # فحص في كل مرة (0 = دائماً)
        self.auto_update = True
        self.load_config()
        
    def load_config(self):
        """تحميل إعدادات التحديث"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.current_version = config.get('current_version', '1.0.0')
                    self.update_url = config.get('update_url', '')
                    self.check_interval = config.get('check_interval', 0)
                    self.auto_update = config.get('auto_update', True)
            else:
                # إنشاء ملف إعدادات افتراضي
                self.create_default_config()
        except Exception as e:
            print(f"خطأ في تحميل إعدادات التحديث: {e}")
            self.create_default_config()
    
    def create_default_config(self):
        """إنشاء ملف إعدادات افتراضي"""
        default_config = {
            "current_version": "1.0.0",
            "update_url": "https://github.com/your-repo/releases/latest",  # غيّر هذا
            "check_interval": 0,
            "auto_update": True,
            "last_check": ""
        }
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, ensure_ascii=False, indent=2)
            print("تم إنشاء ملف إعدادات التحديث")
        except Exception as e:
            print(f"خطأ في إنشاء ملف الإعدادات: {e}")
    
    def should_check_for_updates(self):
        """التحقق من ضرورة فحص التحديثات"""
        # الوضع اليدوي: عدم فحص تلقائي
        if not self.auto_update or self.check_interval == -1:
            return False
        
        # الفحص الدائم: فحص في كل مرة
        if self.check_interval == 0:
            print("🔄 فحص التحديثات في كل مرة يفتح البرنامج...")
            return True
            
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                last_check = config.get('last_check', '')
                
            if not last_check:
                print("🔄 أول فحص للتحديثات...")
                return True
                
            last_check_date = datetime.fromisoformat(last_check)
            time_diff = datetime.now() - last_check_date
            hours_passed = time_diff.total_seconds() / 3600
            
            should_check = hours_passed > self.check_interval
            
            if should_check:
                print(f"🔄 فحص التحديثات (مضى {hours_passed:.1f} ساعة من آخر فحص)...")
            else:
                print(f"⏱️ لا حاجة للفحص بعد (مضى {hours_passed:.1f} ساعة، مطلوب {self.check_interval} ساعة)")
            
            return should_check
            
        except Exception as e:
            print(f"خطأ في التحقق من تاريخ آخر فحص: {e}")
            return True
    
    def check_for_updates(self):
        """التحقق من وجود تحديثات"""
        if not self.update_url:
            return None
            
        try:
            print("🔍 التحقق من التحديثات...")
            
            # تحديث تاريخ آخر فحص
            self.update_last_check_date()
            
            # فحص GitHub Releases (مثال)
            if "github.com" in self.update_url:
                return self.check_github_updates()
            else:
                # فحص خادم مخصص
                return self.check_custom_server_updates()
                
        except Exception as e:
            print(f"خطأ في التحقق من التحديثات: {e}")
            return None
    
    def check_github_updates(self):
        """التحقق من التحديثات عبر GitHub"""
        try:
            # تحويل رابط GitHub إلى API
            api_url = self.update_url.replace('github.com', 'api.github.com/repos').replace('/releases/latest', '/releases/latest')
            
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200:
                release_data = response.json()
                latest_version = release_data['tag_name'].replace('v', '')
                
                if self.is_newer_version(latest_version, self.current_version):
                    return {
                        'version': latest_version,
                        'download_url': release_data['assets'][0]['browser_download_url'] if release_data['assets'] else None,
                        'release_notes': release_data['body'],
                        'published_date': release_data['published_at']
                    }
            return None
            
        except Exception as e:
            print(f"خطأ في فحص GitHub: {e}")
            return None
    
    def check_custom_server_updates(self):
        """التحقق من التحديثات عبر خادم مخصص"""
        try:
            response = requests.get(self.update_url, timeout=10)
            if response.status_code == 200:
                update_data = response.json()
                latest_version = update_data.get('version', '')
                
                if self.is_newer_version(latest_version, self.current_version):
                    return update_data
            return None
            
        except Exception as e:
            print(f"خطأ في فحص الخادم المخصص: {e}")
            return None
    
    def is_newer_version(self, latest_version, current_version):
        """مقارنة الإصدارات"""
        try:
            latest_parts = [int(x) for x in latest_version.split('.')]
            current_parts = [int(x) for x in current_version.split('.')]
            
            # إكمال الأجزاء الناقصة بصفر
            max_len = max(len(latest_parts), len(current_parts))
            latest_parts.extend([0] * (max_len - len(latest_parts)))
            current_parts.extend([0] * (max_len - len(current_parts)))
            
            return latest_parts > current_parts
            
        except Exception as e:
            print(f"خطأ في مقارنة الإصدارات: {e}")
            return False
    
    def download_update(self, download_url, progress_callback=None):
        """تحميل التحديث"""
        try:
            print(f"📥 تحميل التحديث من: {download_url}")
            
            # إنشاء مجلد التحديثات
            update_dir = Path("updates")
            update_dir.mkdir(exist_ok=True)
            
            # اسم الملف
            filename = update_dir / "update.zip"
            
            # تحميل الملف
            response = requests.get(download_url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if progress_callback and total_size > 0:
                            progress = (downloaded / total_size) * 100
                            progress_callback(progress)
            
            print("✅ تم تحميل التحديث بنجاح")
            return str(filename)
            
        except Exception as e:
            print(f"خطأ في تحميل التحديث: {e}")
            return None
    
    def apply_update(self, update_file):
        """تطبيق التحديث"""
        try:
            print("🔄 تطبيق التحديث...")
            
            # إنشاء نسخة احتياطية
            self.create_backup()
            
            # استخراج التحديث
            with zipfile.ZipFile(update_file, 'r') as zip_ref:
                zip_ref.extractall("temp_update")
            
            # نسخ الملفات الجديدة
            update_source = Path("temp_update")
            current_dir = Path(".")
            
            for item in update_source.rglob("*"):
                if item.is_file():
                    relative_path = item.relative_to(update_source)
                    destination = current_dir / relative_path
                    
                    # إنشاء المجلد إذا لم يكن موجود
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    
                    # نسخ الملف
                    shutil.copy2(item, destination)
            
            # تنظيف الملفات المؤقتة
            shutil.rmtree("temp_update")
            os.remove(update_file)
            
            print("✅ تم تطبيق التحديث بنجاح")
            return True
            
        except Exception as e:
            print(f"خطأ في تطبيق التحديث: {e}")
            self.restore_backup()
            return False
    
    def create_backup(self):
        """إنشاء نسخة احتياطية"""
        try:
            backup_dir = Path("backup")
            backup_dir.mkdir(exist_ok=True)
            
            # نسخ الملفات الرئيسية
            important_files = ["*.py", "gui/", "sheets/", "config/"]
            
            for pattern in important_files:
                for file_path in Path(".").glob(pattern):
                    if file_path.is_file():
                        shutil.copy2(file_path, backup_dir / file_path.name)
                    elif file_path.is_dir():
                        shutil.copytree(file_path, backup_dir / file_path.name, dirs_exist_ok=True)
            
            print("✅ تم إنشاء النسخة الاحتياطية")
            
        except Exception as e:
            print(f"خطأ في إنشاء النسخة الاحتياطية: {e}")
    
    def restore_backup(self):
        """استعادة النسخة الاحتياطية"""
        try:
            backup_dir = Path("backup")
            if backup_dir.exists():
                for item in backup_dir.iterdir():
                    if item.is_file():
                        shutil.copy2(item, item.name)
                    elif item.is_dir():
                        if Path(item.name).exists():
                            shutil.rmtree(item.name)
                        shutil.copytree(item, item.name)
                
                print("✅ تم استعادة النسخة الاحتياطية")
                
        except Exception as e:
            print(f"خطأ في استعادة النسخة الاحتياطية: {e}")
    
    def set_check_mode(self, mode="always"):
        """
        تحديد نوع فحص التحديثات
        
        الأوضاع المتاحة:
        - 'always': فحص في كل مرة يفتح البرنامج (الافتراضي الجديد)
        - 'daily': فحص يومياً (24 ساعة)
        - 'weekly': فحص أسبوعياً (168 ساعة)
        - 'manual': فحص يدوي فقط
        """
        check_intervals = {
            'always': 0,        # فحص دائماً
            'daily': 24,        # يومياً
            'weekly': 168,      # أسبوعياً
            'manual': -1        # يدوي فقط
        }
        
        if mode not in check_intervals:
            print(f"⚠️ وضع غير صحيح: {mode}. الأوضاع المتاحة: {list(check_intervals.keys())}")
            return False
        
        self.check_interval = check_intervals[mode]
        self.auto_update = (mode != 'manual')
        
        # حفظ الإعدادات الجديدة
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            else:
                config = {}
            
            config['check_interval'] = self.check_interval
            config['auto_update'] = self.auto_update
            config['check_mode'] = mode
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
                
            mode_names = {
                'always': 'في كل مرة يفتح البرنامج',
                'daily': 'يومياً (كل 24 ساعة)',
                'weekly': 'أسبوعياً (كل أسبوع)',
                'manual': 'يدوياً فقط'
            }
            
            print(f"✅ تم تحديد وضع فحص التحديثات إلى: {mode_names[mode]}")
            return True
            
        except Exception as e:
            print(f"❌ خطأ في حفظ إعدادات الفحص: {e}")
            return False
    
    def get_check_mode_info(self):
        """الحصول على معلومات وضع الفحص الحالي"""
        if self.check_interval == 0:
            return "في كل مرة يفتح البرنامج"
        elif self.check_interval == 24:
            return "يومياً (كل 24 ساعة)"
        elif self.check_interval == 168:
            return "أسبوعياً (كل أسبوع)"
        elif self.check_interval == -1 or not self.auto_update:
            return "يدوياً فقط"
        else:
            return f"كل {self.check_interval} ساعة"

    def update_last_check_date(self):
        """تحديث تاريخ آخر فحص"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                config['last_check'] = datetime.now().isoformat()
                
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(config, f, ensure_ascii=False, indent=2)
                    
        except Exception as e:
            print(f"خطأ في تحديث تاريخ الفحص: {e}")
    
    def show_update_dialog(self, update_info):
        """عرض نافذة التحديث"""
        def on_update():
            dialog.destroy()
            # بدء التحديث في thread منفصل
            threading.Thread(target=self.perform_update, args=(update_info,), daemon=True).start()
        
        def on_skip():
            dialog.destroy()
        
        # إنشاء نافذة التحديث
        dialog = tk.Toplevel()
        dialog.title("🔄 تحديث متاح")
        dialog.geometry("500x400")
        dialog.resizable(False, False)
        dialog.transient()
        dialog.grab_set()
        
        # المحتوى
        main_frame = tk.Frame(dialog, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # العنوان
        title_label = tk.Label(main_frame, text="🎉 تحديث جديد متاح!", 
                              font=("Arial", 16, "bold"), fg="#2E8B57")
        title_label.pack(pady=(0, 20))
        
        # معلومات الإصدار
        info_text = f"""
الإصدار الحالي: {self.current_version}
الإصدار الجديد: {update_info.get('version', 'غير معروف')}

ملاحظات الإصدار:
{update_info.get('release_notes', 'لا توجد ملاحظات متاحة')}
"""
        
        info_label = tk.Label(main_frame, text=info_text, 
                             font=("Arial", 10), justify=tk.LEFT)
        info_label.pack(pady=(0, 20), fill=tk.BOTH, expand=True)
        
        # الأزرار
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        update_btn = tk.Button(button_frame, text="🔄 تحديث الآن", 
                              command=on_update, bg="#4CAF50", fg="white",
                              font=("Arial", 12, "bold"))
        update_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        skip_btn = tk.Button(button_frame, text="⏭️ تخطي", 
                            command=on_skip, bg="#FF5722", fg="white",
                            font=("Arial", 12, "bold"))
        skip_btn.pack(side=tk.LEFT)
    
    def perform_update(self, update_info):
        """تنفيذ عملية التحديث"""
        download_url = update_info.get('download_url')
        if not download_url:
            messagebox.showerror("خطأ", "رابط التحميل غير متاح!")
            return
        
        # نافذة التقدم
        progress_window = self.create_progress_window()
        
        try:
            # تحميل التحديث
            def update_progress(percent):
                if progress_window and hasattr(progress_window, 'progress_var'):
                    progress_window.progress_var.set(percent)
                    progress_window.update()
            
            update_file = self.download_update(download_url, update_progress)
            
            if update_file and self.apply_update(update_file):
                # تحديث رقم الإصدار
                self.update_version_info(update_info['version'])
                
                if progress_window:
                    progress_window.destroy()
                
                # إظهار رسالة النجاح وإعادة التشغيل
                result = messagebox.askyesno("✅ تم التحديث", 
                                           "تم تطبيق التحديث بنجاح!\n\n"
                                           "هل تريد إعادة تشغيل البرنامج الآن؟")
                if result:
                    self.restart_application()
            else:
                if progress_window:
                    progress_window.destroy()
                messagebox.showerror("❌ خطأ", "فشل في تطبيق التحديث!")
                
        except Exception as e:
            if progress_window:
                progress_window.destroy()
            messagebox.showerror("❌ خطأ", f"خطأ في التحديث:\n{str(e)}")
    
    def create_progress_window(self):
        """إنشاء نافذة تقدم التحديث"""
        progress_window = tk.Toplevel()
        progress_window.title("جاري التحديث...")
        progress_window.geometry("400x150")
        progress_window.resizable(False, False)
        
        main_frame = tk.Frame(progress_window, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main_frame, text="🔄 جاري تحميل التحديث...", 
                font=("Arial", 12)).pack(pady=(0, 20))
        
        progress_window.progress_var = tk.DoubleVar()
        progress_bar = tk.ttk.Progressbar(main_frame, 
                                        variable=progress_window.progress_var,
                                        maximum=100)
        progress_bar.pack(fill=tk.X, pady=(0, 10))
        
        return progress_window
    
    def update_version_info(self, new_version):
        """تحديث معلومات الإصدار"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                config['current_version'] = new_version
                
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(config, f, ensure_ascii=False, indent=2)
                    
                self.current_version = new_version
                
        except Exception as e:
            print(f"خطأ في تحديث معلومات الإصدار: {e}")
    
    def restart_application(self):
        """إعادة تشغيل التطبيق"""
        try:
            if getattr(sys, 'frozen', False):
                # إذا كان التطبيق مجمد (exe)
                subprocess.Popen([sys.executable])
            else:
                # إذا كان التطبيق Python script
                subprocess.Popen([sys.executable] + sys.argv)
            
            # إغلاق التطبيق الحالي
            sys.exit(0)
            
        except Exception as e:
            print(f"خطأ في إعادة التشغيل: {e}")
    
    def auto_check_for_updates(self):
        """فحص تلقائي للتحديثات عند بدء التطبيق"""
        def check_updates():
            if self.should_check_for_updates():
                update_info = self.check_for_updates()
                if update_info:
                    # عرض نافذة التحديث في الـ main thread
                    import tkinter as tk
                    root = tk._default_root
                    if root:
                        root.after(0, lambda: self.show_update_dialog(update_info))
        
        # تشغيل الفحص في thread منفصل
        threading.Thread(target=check_updates, daemon=True).start()


# دالة للاستخدام في التطبيق الرئيسي
def init_auto_updater():
    """تهيئة نظام التحديث التلقائي"""
    try:
        updater = AutoUpdater()
        updater.auto_check_for_updates()
        return updater
    except Exception as e:
        print(f"خطأ في تهيئة نظام التحديث: {e}")
        return None


if __name__ == "__main__":
    # اختبار نظام التحديث
    updater = AutoUpdater()
    
    print("🔍 فحص التحديثات...")
    update_info = updater.check_for_updates()
    
    if update_info:
        print(f"✅ تحديث متاح: {update_info['version']}")
    else:
        print("✅ البرنامج محدث")