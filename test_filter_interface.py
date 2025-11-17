#!/usr/bin/env python3
"""
اختبار مباشر لواجهة الفلاتر المحسنة
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import ttk
from config.user_session import UserSession
from sheets.manager import SheetsManager

class TestFilterInterface:
    """واجهة اختبار للفلاتر"""
    
    def __init__(self):
        # إنشاء النافذة
        self.root = tk.Tk()
        self.root.title("اختبار واجهة الفلاتر")
        self.root.geometry("1000x700")
        
        # إنشاء جلسة مستخدم
        self.user_session = UserSession()
        self.user_session.login("مطور_النظام", "PRJ_TEST_001", is_admin=False)
        
        # متغيرات البيانات
        self.all_operations = []
        self.displayed_operations = []
        self.filter_combos = {}
        
        # إعداد الواجهة
        self.setup_interface()
        
        # تحميل البيانات
        self.load_data()
    
    def setup_interface(self):
        """إعداد الواجهة"""
        
        # إطار الفلاتر
        filter_frame = tk.LabelFrame(self.root, text="الفلاتر", font=("Arial", 12, "bold"))
        filter_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # شبكة الفلاتر
        grid = tk.Frame(filter_frame)
        grid.pack(fill=tk.X, padx=10, pady=10)
        
        # فلتر التصنيف
        tk.Label(grid, text="التصنيف:").grid(row=0, column=0, padx=5, sticky="e")
        self.filter_combos['category'] = ttk.Combobox(grid, width=15, state='readonly')
        self.filter_combos['category'].grid(row=0, column=1, padx=5)
        self.filter_combos['category'].bind('<<ComboboxSelected>>', self.on_filter_changed)
        
        # فلتر المستخدم
        tk.Label(grid, text="المستخدم:").grid(row=0, column=2, padx=5, sticky="e")
        self.filter_combos['user'] = ttk.Combobox(grid, width=15, state='disabled')
        self.filter_combos['user'].grid(row=0, column=3, padx=5)
        
        # فلتر المشروع
        tk.Label(grid, text="المشروع:").grid(row=0, column=4, padx=5, sticky="e")
        self.filter_combos['project'] = ttk.Combobox(grid, width=15, state='disabled')
        self.filter_combos['project'].grid(row=0, column=5, padx=5)
        
        # فلتر العنصر
        tk.Label(grid, text="العنصر:").grid(row=1, column=0, padx=5, sticky="e")
        self.filter_combos['item'] = ttk.Combobox(grid, width=20, state='readonly')
        self.filter_combos['item'].grid(row=1, column=1, padx=5)
        self.filter_combos['item'].bind('<<ComboboxSelected>>', self.on_filter_changed)
        
        # زر إعادة التعيين
        reset_btn = tk.Button(grid, text="إعادة تعيين", command=self.reset_filters)
        reset_btn.grid(row=1, column=2, padx=10)
        
        # ملاحظة للمستخدم العادي
        note_label = tk.Label(
            grid, 
            text="🔒 فلاتر المستخدم والمشروع محددة حسب صلاحياتك",
            fg="orange", font=("Arial", 9, "italic")
        )
        note_label.grid(row=1, column=3, columnspan=3, padx=5, sticky="w")
        
        # إطار الجدول
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # إنشاء الجدول
        columns = ('التاريخ', 'العنصر', 'التصنيف', 'المستخدم', 'المشروع', 'التفاصيل')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # تعيين عناوين الأعمدة
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")
        
        # شريط التمرير
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # ترتيب الجدول
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # شريط الحالة
        self.status_label = tk.Label(
            self.root, 
            text="جاري التحميل...", 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM)
    
    def load_data(self):
        """تحميل البيانات من Google Sheets"""
        
        self.status_label.config(text="جاري تحميل البيانات...")
        self.root.update()
        
        try:
            # الاتصال بـ Google Sheets
            sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
            
            if not sheets_manager.connect():
                raise Exception("فشل في الاتصال بـ Google Sheets")
            
            # الحصول على بيانات Activity Log
            activity_sheet = sheets_manager.spreadsheet.worksheet('Activity_Log_v2_20251108')
            all_values = activity_sheet.get_all_values()
            
            if not all_values:
                raise Exception("لا توجد بيانات في شيت العمليات")
            
            # تحويل البيانات
            headers = all_values[0]
            self.all_operations = []
            
            available_categories = set()
            available_users = set()
            available_projects = set()
            available_items = set()
            
            for i, row in enumerate(all_values[1:], start=2):
                if row and len(row) >= 5 and row[0]:
                    operation = {}
                    for j, header in enumerate(headers):
                        if j < len(row):
                            operation[header] = row[j].strip()
                        else:
                            operation[header] = ""
                    
                    self.all_operations.append(operation)
                    
                    # جمع الفلاتر المتاحة
                    if operation.get('التصنيف'):
                        available_categories.add(operation['التصنيف'])
                    if operation.get('اسم المستخدم'):
                        available_users.add(operation['اسم المستخدم'])
                    if operation.get('رقم المشروع'):
                        available_projects.add(operation['رقم المشروع'])
                    if operation.get('اسم العنصر'):
                        available_items.add(operation['اسم العنصر'])
            
            # إعداد قيم الفلاتر
            self.filter_combos['category']['values'] = ['الكل'] + sorted(available_categories)
            self.filter_combos['category'].set('الكل')
            
            # للمستخدم العادي - فلاتر مقيدة
            self.filter_combos['user']['values'] = [self.user_session.username]
            self.filter_combos['user'].set(self.user_session.username)
            
            self.filter_combos['project']['values'] = [self.user_session.project_number]
            self.filter_combos['project'].set(self.user_session.project_number)
            
            self.filter_combos['item']['values'] = ['الكل'] + sorted(available_items)
            self.filter_combos['item'].set('الكل')
            
            # تطبيق الفلاتر الأولية
            self.apply_filters()
            
            print(f"✅ تم تحميل {len(self.all_operations)} عملية")
            print(f"👥 المستخدمون: {sorted(available_users)}")
            print(f"🏢 المشاريع: {sorted(available_projects)}")
            print(f"📦 التصنيفات: {sorted(available_categories)}")
            
        except Exception as e:
            print(f"❌ خطأ في التحميل: {e}")
            self.status_label.config(text=f"خطأ: {e}")
    
    def on_filter_changed(self, event=None):
        """استدعاء عند تغيير الفلاتر"""
        
        print(f"\n🔄 تم تغيير فلتر: {event.widget if event else 'مجهول'}")
        self.apply_filters()
    
    def apply_filters(self):
        """تطبيق الفلاتر"""
        
        print(f"\n📋 تطبيق الفلاتر...")
        
        # البدء من جميع العمليات
        filtered = self.all_operations.copy()
        original_count = len(filtered)
        
        print(f"📊 العمليات الأصلية: {original_count}")
        
        # الحصول على قيم الفلاتر
        selected_category = self.filter_combos['category'].get()
        selected_user = self.user_session.username  # مقيد للمستخدم العادي
        selected_project = self.user_session.project_number  # مقيد للمستخدم العادي
        selected_item = self.filter_combos['item'].get()
        
        print(f"🔍 الفلاتر المطبقة:")
        print(f"   التصنيف: '{selected_category}'")
        print(f"   المستخدم: '{selected_user}' (مقيد)")
        print(f"   المشروع: '{selected_project}' (مقيد)")
        print(f"   العنصر: '{selected_item}'")
        
        # تطبيق فلتر المستخدم (دائماً مطبق للمستخدم العادي)
        if selected_user:
            filtered = [
                op for op in filtered 
                if op.get('اسم المستخدم', '').strip() == selected_user.strip()
            ]
            print(f"🔍 بعد فلتر المستخدم: {len(filtered)} عملية")
        
        # تطبيق فلتر المشروع (دائماً مطبق للمستخدم العادي)
        if selected_project:
            filtered = [
                op for op in filtered 
                if op.get('رقم المشروع', '').strip() == str(selected_project).strip()
            ]
            print(f"🔍 بعد فلتر المشروع: {len(filtered)} عملية")\n        \n        # تطبيق فلتر التصنيف\n        if selected_category and selected_category != 'الكل':\n            filtered = [\n                op for op in filtered \n                if op.get('التصنيف', '').strip() == selected_category.strip()\n            ]\n            print(f\"🔍 بعد فلتر التصنيف: {len(filtered)} عملية\")\n        \n        # تطبيق فلتر العنصر\n        if selected_item and selected_item != 'الكل':\n            filtered = [\n                op for op in filtered \n                if op.get('اسم العنصر', '').strip() == selected_item.strip()\n            ]\n            print(f\"🔍 بعد فلتر العنصر: {len(filtered)} عملية\")\n        \n        # تحديث البيانات المعروضة\n        self.displayed_operations = filtered\n        self.refresh_display()\n        \n        print(f\"✅ النتيجة النهائية: {original_count} → {len(filtered)} عملية\")\n    \n    def refresh_display(self):\n        \"\"\"تحديث عرض الجدول\"\"\"\n        \n        # مسح الجدول الحالي\n        for item in self.tree.get_children():\n            self.tree.delete(item)\n        \n        # إضافة البيانات المفلترة\n        for operation in self.displayed_operations:\n            values = (\n                operation.get('التاريخ', ''),\n                operation.get('اسم العنصر', ''),\n                operation.get('التصنيف', ''),\n                operation.get('اسم المستخدم', ''),\n                operation.get('رقم المشروع', ''),\n                operation.get('التفاصيل', '')[:50] + '...' if len(operation.get('التفاصيل', '')) > 50 else operation.get('التفاصيل', '')\n            )\n            self.tree.insert('', 'end', values=values)\n        \n        # تحديث شريط الحالة\n        status_text = f\"يعرض {len(self.displayed_operations)} عملية من أصل {len(self.all_operations)} | المستخدم: {self.user_session.username} | المشروع: {self.user_session.project_number}\"\n        self.status_label.config(text=status_text)\n    \n    def reset_filters(self):\n        \"\"\"إعادة تعيين الفلاتر القابلة للتعديل\"\"\"\n        \n        print(\"🔄 إعادة تعيين الفلاتر...\")\n        \n        # إعادة تعيين الفلاتر القابلة للتعديل فقط\n        self.filter_combos['category'].set('الكل')\n        self.filter_combos['item'].set('الكل')\n        \n        # لا نغير فلاتر المستخدم والمشروع لأنها مقيدة\n        \n        # تطبيق الفلاتر\n        self.apply_filters()\n    \n    def run(self):\n        \"\"\"تشغيل الواجهة\"\"\"\n        \n        print(f\"🖥️ تشغيل واجهة الاختبار للمستخدم: {self.user_session.username}\")\n        self.root.mainloop()\n\ndef main():\n    \"\"\"الدالة الرئيسية\"\"\"\n    \n    print(\"🧪 اختبار واجهة الفلاتر المحسنة\")\n    print(\"=\" * 50)\n    \n    try:\n        # إنشاء وتشغيل واجهة الاختبار\n        test_interface = TestFilterInterface()\n        test_interface.run()\n        \n    except KeyboardInterrupt:\n        print(\"\\n👋 تم إيقاف الاختبار\")\n    except Exception as e:\n        print(f\"❌ خطأ في الاختبار: {e}\")\n        import traceback\n        traceback.print_exc()\n\nif __name__ == \"__main__\":\n    main()