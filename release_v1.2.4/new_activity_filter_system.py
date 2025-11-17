#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 نظام بحث العمليات الجديد - مع إصلاح مشكلة الفلاتر
================================================================

نسخة جديدة كاملة لحل مشكلة عدم تحديث البيانات عند تغيير الفلاتر
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import sys
import os

# إضافة مسار المشروع
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sheets.manager import SheetsManager

class NewActivityFilterSystem:
    def __init__(self, parent=None, sheets_manager=None, current_user=None):
        """تهيئة نظام الفلاتر الجديد"""
        
        self.parent = parent
        self.window = None
        self.sheets_manager = sheets_manager
        self.current_user = current_user  # معلومات المستخدم الحالي
        
        # البيانات
        self.all_operations = []      # جميع العمليات من الشيت
        self.displayed_operations = [] # العمليات المعروضة حالياً
        
        # عناصر الواجهة
        self.tree = None
        self.filter_combos = {}
        self.status_label = None
        
        # خيارات الفلاتر
        self.available_categories = set()
        self.available_users = set()
        self.available_projects = set()
        self.available_items = set()
        
        print("🆕 تم إنشاء نظام الفلاتر الجديد")

    def create_window(self):
        """إنشاء النافذة"""
        
        if self.parent:
            self.window = tk.Toplevel(self.parent)
        else:
            self.window = tk.Tk()
            
        # تحديد عنوان النافذة حسب نوع المستخدم
        if self.current_user and self.current_user.get('user_type') == 'user':
            user_project = self.current_user.get('project_id', 'غير محدد')
            title = f"🔍 سجل العمليات - المشروع: {user_project}"
        else:
            title = "🔍 نظام البحث الجديد - سجل العمليات (جميع المشاريع)"
        
        self.window.title(title)
        self.window.geometry("1400x800")
        self.window.configure(bg="#2b2b3d")
        
        # تحميل البيانات أولاً
        if not self.load_operations_data():
            messagebox.showerror("خطأ", "فشل في تحميل البيانات!")
            return None
            
        # إنشاء الواجهة
        self.create_interface()
        
        # عرض جميع البيانات في البداية
        self.refresh_display()
        
        print(f"✅ تم إنشاء النافذة وعرض {len(self.displayed_operations)} عنصر")
        
        return self.window

    def load_operations_data(self):
        """تحميل بيانات العمليات من Google Sheets"""
        
        try:
            print("📊 جاري تحميل بيانات العمليات...")
            
            # الاتصال إذا لم يكن متصلاً
            if not self.sheets_manager:
                self.sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
                if not self.sheets_manager.connect():
                    raise Exception("فشل في الاتصال بـ Google Sheets")
            
            # الوصول لشيت العمليات
            activity_sheet = self.sheets_manager.spreadsheet.worksheet('Activity_Log_v2_20251108')
            all_values = activity_sheet.get_all_values()
            
            if not all_values:
                raise Exception("لا توجد بيانات في شيت العمليات")
            
            # استخراج البيانات
            headers = all_values[0]
            self.all_operations = []
            
            print(f"📋 الأعمدة: {headers}")
            
            for i, row in enumerate(all_values[1:], start=2):
                if row and len(row) >= 5 and row[0]:  # التأكد من وجود بيانات أساسية
                    operation = {}
                    
                    # تعيين البيانات حسب الفهارس
                    for j, header in enumerate(headers):
                        if j < len(row):
                            operation[header] = row[j].strip()
                        else:
                            operation[header] = ""
                    
                    operation['row_index'] = i
                    self.all_operations.append(operation)
                    
                    # جمع خيارات الفلاتر
                    category = operation.get('التصنيف', '').strip()
                    if category:
                        self.available_categories.add(category)
                        
                    user = operation.get('اسم المستخدم', '').strip()
                    if user:
                        self.available_users.add(user)
                        
                    project = operation.get('رقم المشروع', '').strip()
                    if project:
                        self.available_projects.add(project)
                        
                    item = operation.get('اسم العنصر', '').strip()
                    if item:
                        self.available_items.add(item)
            
            # فلترة البيانات حسب نوع المستخدم
            if self.current_user and self.current_user.get('user_type') == 'user':
                # المستخدم العادي يرى فقط عمليات مشروعه
                user_project = self.current_user.get('project_id', '')
                if user_project:
                    self.all_operations = [
                        op for op in self.all_operations 
                        if op.get('رقم المشروع', '').strip() == user_project
                    ]
                    print(f"🔒 المستخدم العادي - فلترة حسب المشروع: {user_project}")
                else:
                    # إذا لم يكن للمستخدم مشروع محدد، لا يرى أي عمليات
                    self.all_operations = []
                    print("⚠️ المستخدم ليس لديه مشروع محدد")
            else:
                # المدير يرى جميع العمليات
                print("👑 مدير - عرض جميع العمليات")
            
            # نسخ العمليات المفلترة للعرض في البداية
            self.displayed_operations = self.all_operations.copy()
            
            print(f"✅ تم تحميل {len(self.all_operations)} عملية")
            print(f"📊 التصنيفات المتاحة: {sorted(self.available_categories)}")
            print(f"👥 المستخدمون: {sorted(self.available_users)}")
            
            return True
            
        except Exception as e:
            print(f"❌ خطأ في تحميل البيانات: {e}")
            return False

    def create_interface(self):
        """إنشاء واجهة المستخدم"""
        
        # الإطار الرئيسي
        main_frame = tk.Frame(self.window, bg="#2b2b3d")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # إطار الفلاتر
        filters_frame = tk.LabelFrame(
            main_frame, 
            text="🔍 الفلاتر", 
            font=("Arial", 12, "bold"),
            bg="#2b2b3d", fg="#ffffff"
        )
        filters_frame.pack(fill=tk.X, pady=(0, 10))
        
        # إطار الفلاتر الداخلي
        filters_grid = tk.Frame(filters_frame, bg="#2b2b3d")
        filters_grid.pack(fill=tk.X, padx=10, pady=10)
        
        # فلتر التصنيف
        tk.Label(filters_grid, text="التصنيف:", bg="#2b2b3d", fg="#ffffff").grid(row=0, column=0, padx=5, sticky="e")
        self.filter_combos['category'] = ttk.Combobox(filters_grid, width=15)
        self.filter_combos['category'].grid(row=0, column=1, padx=5)
        self.filter_combos['category']['values'] = ['الكل'] + sorted(self.available_categories)
        self.filter_combos['category'].set('الكل')
        
        # فلتر المستخدم - تحديد الحالة حسب نوع المستخدم
        tk.Label(filters_grid, text="المستخدم:", bg="#2b2b3d", fg="#ffffff").grid(row=0, column=2, padx=5, sticky="e")
        self.filter_combos['user'] = ttk.Combobox(filters_grid, width=15)
        self.filter_combos['user'].grid(row=0, column=3, padx=5)
        
        if self.current_user and self.current_user.get('user_type') == 'user':
            # المستخدم العادي - فلتر المستخدم مُحدد مسبقاً وغير قابل للتعديل
            current_username = self.current_user.get('username', 'المستخدم الحالي')
            self.filter_combos['user']['values'] = [current_username]
            self.filter_combos['user'].set(current_username)
            self.filter_combos['user']['state'] = 'disabled'
        else:
            # المدير - يمكنه اختيار أي مستخدم
            self.filter_combos['user']['values'] = ['الكل'] + sorted(self.available_users)
            self.filter_combos['user'].set('الكل')
            self.filter_combos['user']['state'] = 'readonly'
        
        # فلتر العنصر
        tk.Label(filters_grid, text="العنصر:", bg="#2b2b3d", fg="#ffffff").grid(row=0, column=4, padx=5, sticky="e")
        self.filter_combos['item'] = ttk.Combobox(filters_grid, width=20)
        self.filter_combos['item'].grid(row=0, column=5, padx=5)
        self.filter_combos['item']['values'] = ['الكل'] + sorted(self.available_items)
        self.filter_combos['item'].set('الكل')
        
        # فلتر المشروع - تحديد الحالة حسب نوع المستخدم
        tk.Label(filters_grid, text="المشروع:", bg="#2b2b3d", fg="#ffffff").grid(row=1, column=0, padx=5, sticky="e")
        self.filter_combos['project'] = ttk.Combobox(filters_grid, width=15)
        self.filter_combos['project'].grid(row=1, column=1, padx=5)
        
        if self.current_user and self.current_user.get('user_type') == 'user':
            # المستخدم العادي - فلتر المشروع مُحدد مسبقاً وغير قابل للتعديل
            user_project = self.current_user.get('project_id', 'مشروع المستخدم')
            self.filter_combos['project']['values'] = [user_project]
            self.filter_combos['project'].set(user_project)
            self.filter_combos['project']['state'] = 'disabled'
        else:
            # المدير - يمكنه اختيار أي مشروع
            self.filter_combos['project']['values'] = ['الكل'] + sorted(self.available_projects)
            self.filter_combos['project'].set('الكل')
            self.filter_combos['project']['state'] = 'readonly'
        
        # إضافة ملاحظة للمستخدم العادي
        if self.current_user and self.current_user.get('user_type') == 'user':
            info_label = tk.Label(
                filters_grid,
                text="🔒 فلاتر المشروع والمستخدم مُحددة حسب صلاحياتك",
                bg="#2b2b3d", fg="#FFA500",
                font=("Arial", 9, "italic")
            )
            info_label.grid(row=1, column=2, columnspan=4, padx=5, pady=5, sticky="w")
        
        # ربط أحداث الفلاتر
        for combo_name, combo in self.filter_combos.items():
            # تطبيق الأحداث فقط للفلاتر القابلة للتعديل
            if combo['state'] != 'disabled':
                combo.bind('<<ComboboxSelected>>', self.on_filter_changed)
                combo.bind('<KeyRelease>', self.on_filter_changed)
        
        # زر إعادة التعيين
        reset_btn = tk.Button(
            filters_grid,
            text="🔄 إعادة تعيين",
            command=self.reset_filters,
            bg="#4CAF50", fg="white",
            font=("Arial", 10, "bold")
        )
        reset_btn.grid(row=1, column=2, padx=10)
        
        # إطار الجدول
        table_frame = tk.Frame(main_frame, bg="#2b2b3d")
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # إنشاء الجدول
        columns = ('التاريخ', 'الوقت', 'العملية', 'العنصر', 'التصنيف', 'المضاف', 'المخرج', 'المستخدم', 'المشروع')
        
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20)
        
        # تعيين عناوين الأعمدة
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
        
        # شريط التمرير
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # تعبئة الجدول
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # شريط الحالة
        status_frame = tk.Frame(main_frame, bg="#2b2b3d")
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = tk.Label(
            status_frame,
            text="جاري التحميل...",
            bg="#2b2b3d", fg="#00ff00",
            font=("Arial", 10)
        )
        self.status_label.pack()

    def on_filter_changed(self, event=None):
        """استدعاء عند تغيير أي فلتر"""
        
        # تجاهل الأحداث للفلاتر المعطلة
        if event and hasattr(event.widget, 'state') and 'disabled' in str(event.widget['state']):
            print("🔒 تجاهل حدث من فلتر معطل")
            return
        
        print("\n🔄 تم تغيير الفلتر - بدء التحديث...")
        
        # الحصول على قيم الفلاتر الحالية
        selected_category = self.filter_combos['category'].get()
        
        # تحديد قيم الفلاتر حسب نوع المستخدم
        if hasattr(self, 'user_session') and hasattr(self.user_session, 'is_admin') and not self.user_session.is_admin:
            # مستخدم عادي - استخدام القيم من الجلسة
            selected_user = self.user_session.username
            selected_project = str(self.user_session.project_number)
        elif self.current_user and self.current_user.get('user_type') == 'user':
            # نظام قديم - مستخدم عادي
            selected_user = self.current_user.get('username', '')
            selected_project = self.current_user.get('project_id', '')
        else:
            # مدير - يمكن اختيار أي قيم
            selected_user = self.filter_combos['user'].get()
            selected_project = self.filter_combos['project'].get()
        
        selected_item = self.filter_combos['item'].get()
        
        print(f"📋 الفلاتر المختارة:")
        print(f"   التصنيف: {selected_category}")
        print(f"   المستخدم: {selected_user}")
        print(f"   العنصر: {selected_item}")
        print(f"   المشروع: {selected_project}")
        
        # تطبيق الفلاتر
        self.apply_filters()
        
        # إجبار تحديث الواجهة
        self.window.update_idletasks()
        
        print(f"✅ تم التحديث - يعرض الآن {len(self.displayed_operations)} عنصر")

    def apply_filters(self):
        """تطبيق الفلاتر وتحديث العرض"""
        
        print("\n📋 بدء تطبيق الفلاتر...")
        
        # البدء من جميع العمليات
        filtered_operations = self.all_operations.copy()
        print(f"📊 العمليات الأصلية: {len(filtered_operations)}")
        
        # الحصول على قيم الفلاتر
        selected_category = self.filter_combos['category'].get()
        
        # تحديد قيم الفلاتر حسب نوع المستخدم
        if hasattr(self, 'user_session') and hasattr(self.user_session, 'is_admin') and not self.user_session.is_admin:
            # مستخدم عادي - استخدام القيم من الجلسة
            selected_user = self.user_session.username
            selected_project = str(self.user_session.project_number)
            print(f"🔒 مستخدم عادي - استخدام القيم المحددة: المستخدم={selected_user}, المشروع={selected_project}")
        elif self.current_user and self.current_user.get('user_type') == 'user':
            # نظام قديم - مستخدم عادي
            selected_user = self.current_user.get('username', '')
            selected_project = self.current_user.get('project_id', '')
            print(f"🔒 مستخدم عادي (نظام قديم) - المستخدم={selected_user}, المشروع={selected_project}")
        else:
            # مدير - يمكن اختيار أي قيم
            selected_user = self.filter_combos['user'].get()
            selected_project = self.filter_combos['project'].get()
            print(f"👑 مدير - الفلاتر المختارة: المستخدم={selected_user}, المشروع={selected_project}")
        
        selected_item = self.filter_combos['item'].get()
        
        print(f"🔍 قيم الفلاتر النهائية:")
        print(f"   التصنيف: '{selected_category}'")
        print(f"   المستخدم: '{selected_user}'")
        print(f"   المشروع: '{selected_project}'")
        print(f"   العنصر: '{selected_item}'")
        
        original_count = len(filtered_operations)
        
        # تطبيق فلتر التصنيف
        if selected_category and selected_category != 'الكل' and selected_category.strip():
            before_count = len(filtered_operations)
            filtered_operations = [
                op for op in filtered_operations 
                if op.get('التصنيف', '').strip() == selected_category.strip()
            ]
            print(f"🔍 فلتر التصنيف '{selected_category}': {before_count} → {len(filtered_operations)} عنصر")
            
            # تشخيص إضافي
            if len(filtered_operations) == 0 and before_count > 0:
                available_categories = set(op.get('التصنيف', '').strip() for op in self.all_operations if op.get('التصنيف', '').strip())
                print(f"⚠️ لا توجد نتائج للتصنيف '{selected_category}'")
                print(f"📋 التصنيفات المتاحة: {sorted(available_categories)}")
        
        # تطبيق فلتر المستخدم
        if selected_user and selected_user != 'الكل' and selected_user.strip():
            before_count = len(filtered_operations)
            filtered_operations = [
                op for op in filtered_operations 
                if op.get('اسم المستخدم', '').strip() == selected_user.strip()
            ]
            print(f"🔍 فلتر المستخدم '{selected_user}': {before_count} → {len(filtered_operations)} عنصر")
            
            # تشخيص إضافي
            if len(filtered_operations) == 0 and before_count > 0:
                available_users = set(op.get('اسم المستخدم', '').strip() for op in self.all_operations if op.get('اسم المستخدم', '').strip())
                print(f"⚠️ لا توجد نتائج للمستخدم '{selected_user}'")
                print(f"👥 المستخدمون المتاحون: {sorted(available_users)}")
        
        # تطبيق فلتر العنصر
        if selected_item and selected_item != 'الكل' and selected_item.strip():
            before_count = len(filtered_operations)
            filtered_operations = [
                op for op in filtered_operations 
                if op.get('اسم العنصر', '').strip() == selected_item.strip()
            ]
            print(f"🔍 فلتر العنصر '{selected_item}': {before_count} → {len(filtered_operations)} عنصر")
            
            # تشخيص إضافي
            if len(filtered_operations) == 0 and before_count > 0:
                available_items = set(op.get('اسم العنصر', '').strip() for op in self.all_operations if op.get('اسم العنصر', '').strip())
                print(f"⚠️ لا توجد نتائج للعنصر '{selected_item}'")
                print(f"📺 العناصر المتاحة: {sorted(list(available_items)[:10])}..." if len(available_items) > 10 else f"📺 العناصر المتاحة: {sorted(available_items)}")
        
        # تطبيق فلتر المشروع
        if selected_project and selected_project != 'الكل' and selected_project.strip():
            before_count = len(filtered_operations)
            filtered_operations = [
                op for op in filtered_operations 
                if op.get('رقم المشروع', '').strip() == selected_project.strip()
            ]
            print(f"🔍 فلتر المشروع '{selected_project}': {before_count} → {len(filtered_operations)} عنصر")
            
            # تشخيص إضافي
            if len(filtered_operations) == 0 and before_count > 0:
                available_projects = set(op.get('رقم المشروع', '').strip() for op in self.all_operations if op.get('رقم المشروع', '').strip())
                print(f"⚠️ لا توجد نتائج للمشروع '{selected_project}'")
                print(f"🏢 المشاريع المتاحة: {sorted(available_projects)}")
        
        # تحديث البيانات المعروضة
        self.displayed_operations = filtered_operations
        
        # تحديث العرض
        self.refresh_display()
        
        print(f"\n✅ انتهى تطبيق الفلاتر")
        print(f"📊 النتيجة النهائية: {original_count} → {len(filtered_operations)} عنصر")
        
        # عرض عينة من البيانات المفلترة للتشخيص
        if len(filtered_operations) > 0:
            print(f"🔎 عينة من النتائج:")
            sample_op = filtered_operations[0]
            for key in ['التاريخ', 'اسم العنصر', 'التصنيف', 'اسم المستخدم', 'رقم المشروع']:
                print(f"   {key}: '{sample_op.get(key, '')}'")
        else:
            print("⚠️ لا توجد نتائج بعد تطبيق الفلاتر")
        
        print("="*50)

    def refresh_display(self):
        """تحديث عرض الجدول"""
        
        # مسح الجدول الحالي
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # إضافة البيانات المفلترة
        for operation in self.displayed_operations:
            values = (
                operation.get('التاريخ', ''),
                operation.get('الوقت', ''),
                operation.get('نوع العملية', ''),
                operation.get('اسم العنصر', ''),
                operation.get('التصنيف', ''),
                operation.get('الكمية المضافة', ''),
                operation.get('الكمية المخرجة', ''),
                operation.get('اسم المستخدم', ''),
                operation.get('رقم المشروع', '')
            )
            self.tree.insert('', 'end', values=values)
        
        # حساب إجماليات المدخلات والمخرجات والمتبقي
        total_input = 0
        total_output = 0
        
        for operation in self.displayed_operations:
            try:
                # المدخلات
                input_qty = operation.get('الكمية المضافة', '0')
                if input_qty and input_qty.replace('.', '').replace('-', '').isdigit():
                    total_input += float(input_qty)
                
                # المخرجات
                output_qty = operation.get('الكمية المخرجة', '0')
                if output_qty and output_qty.replace('.', '').replace('-', '').isdigit():
                    total_output += float(output_qty)
            except (ValueError, TypeError):
                continue
        
        # حساب المتبقي
        remaining = total_input - total_output
        
        # تحديث شريط الحالة مع الإحصائيات
        status_text = f"📊 العمليات: {len(self.displayed_operations)} | المدخلات: {total_input:.0f} | المخرجات: {total_output:.0f} | المتبقي: {remaining:.0f}"
        self.status_label.config(text=status_text)
        
        print(f"🖥️ تم تحديث الجدول: {len(self.displayed_operations)} عنصر معروض")
        print(f"📈 الإحصائيات: مدخلات={total_input:.0f}, مخرجات={total_output:.0f}, متبقي={remaining:.0f}")

    def reset_filters(self):
        """إعادة تعيين جميع الفلاتر"""
        
        print("🔄 إعادة تعيين الفلاتر...")
        
        # إعادة تعيين الفلاتر القابلة للتعديل فقط
        for combo_name, combo in self.filter_combos.items():
            if combo['state'] != 'disabled':
                combo.set('الكل')
                print(f"   تم إعادة تعيين فلتر {combo_name}")
            else:
                print(f"   فلتر {combo_name} مقيد - لم يتم تغييره")
        
        # تطبيق الفلاتر من جديد (سيحترم القيود المطبقة)
        self.apply_filters()
        
        print(f"✅ تم إعادة التعيين - يعرض {len(self.displayed_operations)} عنصر")

def main():
    """الاختبار المباشر للنظام الجديد"""
    
    print("🚀 بدء تشغيل نظام الفلاتر الجديد...")
    
    try:
        # إنشاء النافذة الرئيسية
        root = tk.Tk()
        root.withdraw()  # إخفاء النافذة الرئيسية
        
        # الاتصال بـ Google Sheets
        sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
        if not sheets_manager.connect():
            print("❌ فشل في الاتصال بـ Google Sheets!")
            return
        
        # إنشاء النظام الجديد
        filter_system = NewActivityFilterSystem(parent=root, sheets_manager=sheets_manager)
        window = filter_system.create_window()
        
        if window:
            print("✅ تم تشغيل النظام الجديد بنجاح!")
            print("🔍 اختبر الفلاتر الآن...")
            window.mainloop()
        else:
            print("❌ فشل في إنشاء النافذة!")
            
    except Exception as e:
        print(f"❌ خطأ: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()