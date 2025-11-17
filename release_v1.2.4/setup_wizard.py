"""
معالج الإعداد الأولي - نظام إدارة المخزون Sama
يساعد المستخدم في إعداد Google Sheets API والبدء السريع
"""

import os
import sys
import json
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import webbrowser
from pathlib import Path

class SetupWizard:
    """معالج الإعداد الأولي"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("معالج الإعداد الأولي - نظام Sama لإدارة المخزون")
        self.root.geometry("800x600")
        self.root.configure(bg='#1A1A2E')
        
        # الألوان
        self.colors = {
            'bg': '#1A1A2E',
            'card': '#2D2D2D', 
            'gold': '#DAA520',
            'text': 'white',
            'success': '#4CAF50',
            'warning': '#FF9800'
        }
        
        self.current_step = 0
        self.steps = [
            self.step_welcome,
            self.step_google_setup,
            self.step_credentials,
            self.step_test_connection,
            self.step_complete
        ]
        
        self.setup_ui()
        self.show_current_step()
    
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        # العنوان الرئيسي
        title_frame = tk.Frame(self.root, bg=self.colors['bg'])
        title_frame.pack(fill='x', pady=20)
        
        title_label = tk.Label(
            title_frame,
            text="🚀 معالج الإعداد الأولي",
            font=('Arial', 24, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['gold']
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="نظام Sama لإدارة المخزون - الإعداد السريع",
            font=('Arial', 12),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        subtitle_label.pack()
        
        # منطقة المحتوى
        self.content_frame = tk.Frame(self.root, bg=self.colors['bg'])
        self.content_frame.pack(fill='both', expand=True, padx=40, pady=20)
        
        # أزرار التنقل
        button_frame = tk.Frame(self.root, bg=self.colors['bg'])
        button_frame.pack(fill='x', pady=20)
        
        self.back_btn = tk.Button(
            button_frame,
            text="← السابق",
            font=('Arial', 12),
            bg=self.colors['card'],
            fg=self.colors['text'],
            command=self.previous_step,
            padx=20
        )
        self.back_btn.pack(side='left', padx=20)
        
        self.next_btn = tk.Button(
            button_frame,
            text="التالي →",
            font=('Arial', 12, 'bold'),
            bg=self.colors['gold'],
            fg='black',
            command=self.next_step,
            padx=20
        )
        self.next_btn.pack(side='right', padx=20)
    
    def clear_content(self):
        """مسح محتوى المنطقة الحالية"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_current_step(self):
        """عرض الخطوة الحالية"""
        self.clear_content()
        self.steps[self.current_step]()
        
        # تحديث أزرار التنقل
        self.back_btn.config(state='normal' if self.current_step > 0 else 'disabled')
        if self.current_step == len(self.steps) - 1:
            self.next_btn.config(text="إنهاء", command=self.finish_setup)
        else:
            self.next_btn.config(text="التالي →", command=self.next_step)
    
    def step_welcome(self):
        """خطوة الترحيب"""
        welcome_frame = tk.Frame(self.content_frame, bg=self.colors['card'], relief='solid', bd=2)
        welcome_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(
            welcome_frame,
            text="مرحباً بك في نظام Sama لإدارة المخزون! 🎉",
            font=('Arial', 18, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['gold']
        ).pack(pady=20)
        
        welcome_text = """
هذا المعالج سيساعدك في:

✅ إعداد الاتصال مع Google Sheets
✅ تكوين ملف الـ credentials
✅ اختبار الاتصال
✅ إنشاء المستخدم الأول

سوف نقوم بإعداد كل شيء خطوة بخطوة لضمان عمل النظام بشكل مثالي.

المدة المتوقعة: 5-10 دقائق
        """
        
        tk.Label(
            welcome_frame,
            text=welcome_text,
            font=('Arial', 12),
            bg=self.colors['card'],
            fg=self.colors['text'],
            justify='right'
        ).pack(pady=20, padx=40)
        
        # تحذير الأمان
        security_frame = tk.Frame(welcome_frame, bg='#FFA500', relief='solid', bd=2)
        security_frame.pack(fill='x', padx=40, pady=20)
        
        tk.Label(
            security_frame,
            text="🔒 ملاحظة أمان مهمة",
            font=('Arial', 12, 'bold'),
            bg='#FFA500',
            fg='black'
        ).pack(pady=5)
        
        tk.Label(
            security_frame,
            text="ملف credentials.json يحتوي على معلومات حساسة. لا تشاركه مع أحد!",
            font=('Arial', 10),
            bg='#FFA500',
            fg='black'
        ).pack(pady=5)
    
    def step_google_setup(self):
        """خطوة إعداد Google API"""
        setup_frame = tk.Frame(self.content_frame, bg=self.colors['card'], relief='solid', bd=2)
        setup_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(
            setup_frame,
            text="📊 إعداد Google Sheets API",
            font=('Arial', 16, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['gold']
        ).pack(pady=20)
        
        steps_text = """
اتبع الخطوات التالية لإنشاء Service Account:

1️⃣ اذهب إلى Google Cloud Console
2️⃣ أنشئ مشروع جديد أو اختر مشروع موجود
3️⃣ فعّل Google Sheets API
4️⃣ أنشئ Service Account
5️⃣ حمّل مفتاح JSON للـ Service Account
6️⃣ انسخ الملف هنا واختره في الخطوة التالية

سنقوم بفتح الروابط المطلوبة لك...
        """
        
        tk.Label(
            setup_frame,
            text=steps_text,
            font=('Arial', 11),
            bg=self.colors['card'],
            fg=self.colors['text'],
            justify='right'
        ).pack(pady=20, padx=30)
        
        # أزرار فتح الروابط
        links_frame = tk.Frame(setup_frame, bg=self.colors['card'])
        links_frame.pack(pady=20)
        
        tk.Button(
            links_frame,
            text="🌐 فتح Google Cloud Console",
            font=('Arial', 12),
            bg=self.colors['gold'],
            fg='black',
            command=lambda: webbrowser.open('https://console.cloud.google.com/'),
            padx=15
        ).pack(pady=5)
        
        tk.Button(
            links_frame,
            text="📚 دليل مفصل (فيديو)",
            font=('Arial', 12),
            bg=self.colors['success'],
            fg='white',
            command=lambda: webbrowser.open('https://www.youtube.com/watch?v=cnPlKLEGR7E'),
            padx=15
        ).pack(pady=5)
    
    def step_credentials(self):
        """خطوة اختيار ملف credentials"""
        creds_frame = tk.Frame(self.content_frame, bg=self.colors['card'], relief='solid', bd=2)
        creds_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(
            creds_frame,
            text="🔑 اختيار ملف Credentials",
            font=('Arial', 16, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['gold']
        ).pack(pady=20)
        
        # حالة الملف
        self.creds_status = tk.Label(
            creds_frame,
            text="❌ لم يتم اختيار ملف credentials بعد",
            font=('Arial', 12),
            bg=self.colors['card'],
            fg=self.colors['warning']
        )
        self.creds_status.pack(pady=10)
        
        # زر اختيار الملف
        tk.Button(
            creds_frame,
            text="📂 اختيار ملف credentials.json",
            font=('Arial', 14, 'bold'),
            bg=self.colors['gold'],
            fg='black',
            command=self.select_credentials_file,
            padx=20,
            pady=10
        ).pack(pady=20)
        
        # معلومات إضافية
        info_text = """
تأكد من أن ملف JSON يحتوي على:
• type: "service_account"
• private_key
• client_email
• project_id

إذا لم تجد الملف، ارجع للخطوة السابقة لإنشائه.
        """
        
        tk.Label(
            creds_frame,
            text=info_text,
            font=('Arial', 10),
            bg=self.colors['card'],
            fg=self.colors['text'],
            justify='right'
        ).pack(pady=20)
    
    def select_credentials_file(self):
        """اختيار ملف credentials"""
        file_path = filedialog.askopenfilename(
            title="اختر ملف credentials.json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            defaultextension=".json"
        )
        
        if file_path:
            try:
                # التحقق من صحة الملف
                with open(file_path, 'r', encoding='utf-8') as f:
                    creds_data = json.load(f)
                
                required_fields = ['type', 'private_key', 'client_email', 'project_id']
                missing_fields = [field for field in required_fields if field not in creds_data]
                
                if missing_fields:
                    messagebox.showerror(
                        "خطأ في الملف",
                        f"الملف لا يحتوي على الحقول المطلوبة:\n{', '.join(missing_fields)}"
                    )
                    return
                
                if creds_data.get('type') != 'service_account':
                    messagebox.showerror(
                        "نوع خاطئ",
                        "هذا الملف ليس Service Account. تأكد من اختيار النوع الصحيح."
                    )
                    return
                
                # نسخ الملف إلى مجلد config
                os.makedirs('config', exist_ok=True)
                target_path = 'config/credentials.json'
                
                with open(target_path, 'w', encoding='utf-8') as f:
                    json.dump(creds_data, f, indent=2)
                
                self.creds_status.config(
                    text=f"✅ تم حفظ الملف بنجاح: {target_path}",
                    fg=self.colors['success']
                )
                
                messagebox.showinfo("نجح!", "تم حفظ ملف credentials بنجاح!")
                
            except json.JSONDecodeError:
                messagebox.showerror("خطأ", "الملف ليس JSON صحيح!")
            except Exception as e:
                messagebox.showerror("خطأ", f"فشل في قراءة الملف:\n{str(e)}")
    
    def step_test_connection(self):
        """خطوة اختبار الاتصال"""
        test_frame = tk.Frame(self.content_frame, bg=self.colors['card'], relief='solid', bd=2)
        test_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(
            test_frame,
            text="🧪 اختبار الاتصال مع Google Sheets",
            font=('Arial', 16, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['gold']
        ).pack(pady=20)
        
        # نتيجة الاختبار
        self.test_result = tk.Label(
            test_frame,
            text="⏳ اضغط على 'اختبار الاتصال' للبدء",
            font=('Arial', 12),
            bg=self.colors['card'],
            fg=self.colors['text']
        )
        self.test_result.pack(pady=10)
        
        # زر الاختبار
        tk.Button(
            test_frame,
            text="🔧 اختبار الاتصال",
            font=('Arial', 14, 'bold'),
            bg=self.colors['gold'],
            fg='black',
            command=self.test_google_connection,
            padx=20,
            pady=10
        ).pack(pady=20)
        
        # تفاصيل إضافية
        self.connection_details = tk.Text(
            test_frame,
            height=10,
            width=80,
            bg='#3D3D3D',
            fg=self.colors['text'],
            font=('Consolas', 9),
            wrap='word'
        )
        self.connection_details.pack(pady=20, padx=20, fill='both', expand=True)
    
    def test_google_connection(self):
        """اختبار الاتصال مع Google"""
        self.test_result.config(text="⏳ جاري الاختبار...", fg=self.colors['warning'])
        self.connection_details.delete(1.0, 'end')
        self.root.update()
        
        try:
            self.connection_details.insert('end', "🔍 فحص ملف credentials...\n")
            self.root.update()
            
            if not os.path.exists('config/credentials.json'):
                raise FileNotFoundError("ملف credentials.json غير موجود")
            
            self.connection_details.insert('end', "✅ ملف credentials موجود\n\n")
            
            # محاولة الاتصال
            self.connection_details.insert('end', "🔗 محاولة الاتصال بـ Google Sheets API...\n")
            self.root.update()
            
            import gspread
            from google.oauth2.service_account import Credentials
            
            # الـ scopes المطلوبة
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            
            creds = Credentials.from_service_account_file(
                'config/credentials.json',
                scopes=scopes
            )
            client = gspread.authorize(creds)
            
            self.connection_details.insert('end', "✅ تم الاتصال بـ Google Sheets API بنجاح!\n\n")
            
            # محاولة إنشاء/فتح الـ spreadsheet
            self.connection_details.insert('end', "📊 إعداد Inventory Management spreadsheet...\n")
            self.root.update()
            
            try:
                spreadsheet = client.open("Inventory Management")
                self.connection_details.insert('end', "✅ تم فتح Inventory Management\n")
            except gspread.SpreadsheetNotFound:
                self.connection_details.insert('end', "📝 إنشاء Inventory Management جديد...\n")
                spreadsheet = client.create("Inventory Management")
                self.connection_details.insert('end', "✅ تم إنشاء Inventory Management بنجاح!\n")
            
            # إعداد الشيتس المطلوبة
            self.setup_required_sheets(spreadsheet)
            
            self.test_result.config(
                text="🎉 تم الاختبار بنجاح! النظام جاهز للاستخدام",
                fg=self.colors['success']
            )
            
        except Exception as e:
            error_msg = f"❌ فشل في الاختبار: {str(e)}"
            self.test_result.config(text=error_msg, fg='#FF5555')
            self.connection_details.insert('end', f"\n❌ خطأ: {str(e)}\n")
            self.connection_details.insert('end', "\n💡 تأكد من:\n")
            self.connection_details.insert('end', "• صحة ملف credentials.json\n")
            self.connection_details.insert('end', "• تفعيل Google Sheets API\n")
            self.connection_details.insert('end', "• صلاحيات Service Account\n")
    
    def setup_required_sheets(self, spreadsheet):
        """إعداد الشيتس المطلوبة"""
        # شيت Users
        try:
            users_sheet = spreadsheet.worksheet("Users")
            self.connection_details.insert('end', "✅ شيت Users موجود\n")
        except gspread.WorksheetNotFound:
            self.connection_details.insert('end', "👥 إنشاء شيت Users...\n")
            users_sheet = spreadsheet.add_worksheet(title="Users", rows="100", cols="10")
            users_sheet.update('A1:C1', [['username', 'password', 'role']])
            users_sheet.update('A2:C2', [['admin', 'admin123', 'admin']])
            self.connection_details.insert('end', "✅ تم إنشاء شيت Users مع مستخدم admin\n")
        
        # شيت Inventory
        try:
            inventory_sheet = spreadsheet.worksheet("Inventory")
            self.connection_details.insert('end', "✅ شيت Inventory موجود\n")
        except gspread.WorksheetNotFound:
            self.connection_details.insert('end', "📦 إنشاء شيت Inventory...\n")
            inventory_sheet = spreadsheet.add_worksheet(title="Inventory", rows="1000", cols="10")
            inventory_sheet.update('A1:E1', [['Item Name', 'Quantity', 'Unit Price', 'Total Value', 'Last Updated']])
            self.connection_details.insert('end', "✅ تم إنشاء شيت Inventory\n")
        
        self.connection_details.insert('end', "\n🎯 تم إعداد جميع الشيتس المطلوبة!\n")
    
    def step_complete(self):
        """خطوة الإكمال"""
        complete_frame = tk.Frame(self.content_frame, bg=self.colors['card'], relief='solid', bd=2)
        complete_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(
            complete_frame,
            text="🎉 تم إكمال الإعداد بنجاح!",
            font=('Arial', 18, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['success']
        ).pack(pady=20)
        
        success_text = """
تهانينا! تم إعداد نظام Sama لإدارة المخزون بنجاح.

✅ تم إعداد Google Sheets API
✅ تم إنشاء/إعداد Inventory Management spreadsheet
✅ تم إنشاء المستخدم الافتراضي

🔑 بيانات تسجيل الدخول:
👤 اسم المستخدم: admin
🔐 كلمة المرور: admin123

الآن يمكنك:
• تسجيل الدخول والبدء في استخدام النظام
• إنشاء مستخدمين جدد
• إدارة المخزون
• استخدام التقارير والتحليلات

استمتع باستخدام النظام! 🚀
        """
        
        tk.Label(
            complete_frame,
            text=success_text,
            font=('Arial', 12),
            bg=self.colors['card'],
            fg=self.colors['text'],
            justify='center'
        ).pack(pady=20)
    
    def next_step(self):
        """الانتقال للخطوة التالية"""
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.show_current_step()
    
    def previous_step(self):
        """العودة للخطوة السابقة"""
        if self.current_step > 0:
            self.current_step -= 1
            self.show_current_step()
    
    def finish_setup(self):
        """إنهاء الإعداد"""
        messagebox.showinfo(
            "تم الإكمال!",
            "تم إكمال الإعداد بنجاح!\n\nسيتم الآن فتح النظام الرئيسي."
        )
        self.root.destroy()
        
        # تشغيل النظام الرئيسي
        try:
            import main_with_auth
        except ImportError:
            os.system('python main_with_auth.py')
    
    def run(self):
        """تشغيل المعالج"""
        self.root.mainloop()

def main():
    """دالة رئيسية لفحص الحاجة للإعداد"""
    # فحص إذا كان الإعداد مطلوب
    if not os.path.exists('config/credentials.json'):
        print("🔧 تشغيل معالج الإعداد الأولي...")
        wizard = SetupWizard()
        wizard.run()
    else:
        print("✅ تم الإعداد مسبقاً. تشغيل النظام الرئيسي...")
        try:
            import main_with_auth
        except ImportError:
            os.system('python main_with_auth.py')

if __name__ == "__main__":
    main()