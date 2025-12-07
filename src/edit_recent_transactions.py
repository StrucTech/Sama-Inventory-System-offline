# -*- coding: utf-8 -*-
"""
واجهة تعديل المعاملات الحديثة (آخر 24 ساعة)
"""

import pandas as pd
import os
from datetime import datetime, timedelta
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QTableWidget, QTableWidgetItem, 
                           QHeaderView, QMessageBox, QSpinBox, QFrame,
                           QGroupBox, QFormLayout, QTextEdit, QComboBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor
from excel_manager import excel_manager


class EditRecentTransactionsDialog(QDialog):
    """واجهة تعديل المعاملات الحديثة"""
    
    def __init__(self, project_name, parent=None):
        super().__init__(parent)
        self.project_name = project_name
        self.recent_transactions = pd.DataFrame()
        self.setup_ui()
        self.setup_styles()
        self.load_recent_transactions()
        
        # تحديث كل 30 ثانية للتحقق من المعاملات الجديدة
        self.timer = QTimer()
        self.timer.timeout.connect(self.load_recent_transactions)
        self.timer.start(30000)  # 30 ثانية
    
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        self.setWindowTitle(f"تعديل المعاملات الحديثة - {self.project_name}")
        self.setModal(True)
        
        # الحصول على حجم الشاشة وضبط حجم النافذة بناءً عليها
        from PyQt6.QtWidgets import QApplication
        screen = QApplication.primaryScreen().geometry()
        
        # جعل النافذة تأخذ 85% من عرض الشاشة و 90% من ارتفاعها
        window_width = int(screen.width() * 0.85)
        window_height = int(screen.height() * 0.90)
        
        self.resize(window_width, window_height)
        self.center_on_screen()
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        # التخطيط الرئيسي
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # العنوان والتوضيح
        title_label = QLabel("تعديل المعاملات الحديثة (آخر 24 ساعة)")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        info_label = QLabel("يمكنك تعديل الكميات المدخلة خلال آخر 24 ساعة فقط\nقيود الحماية من المخزون السالب:\n• لا يمكن تعديل معاملات الدخول إذا تمت عمليات إخراج بعدها\n• لا يمكن زيادة كمية الخروج لتتجاوز المخزون المتاح")
        info_label.setObjectName("info")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setMaximumHeight(70)
        main_layout.addWidget(info_label)
        
        # أزرار التحكم
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)
        
        refresh_btn = QPushButton("تحديث القائمة")
        refresh_btn.setObjectName("control_button")
        refresh_btn.setMaximumWidth(120)
        refresh_btn.clicked.connect(self.load_recent_transactions)
        controls_layout.addWidget(refresh_btn)
        
        controls_layout.addStretch()
        main_layout.addLayout(controls_layout)
        
        # جدول المعاملات الحديثة
        transactions_group = QGroupBox("المعاملات القابلة للتعديل")
        transactions_layout = QVBoxLayout(transactions_group)
        transactions_layout.setContentsMargins(10, 10, 10, 10)
        transactions_layout.setSpacing(5)
        
        self.transactions_table = QTableWidget()
        self.transactions_table.setObjectName("transactions_table")
        self.transactions_table.setSortingEnabled(True)
        self.transactions_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.transactions_table.setAlternatingRowColors(True)
        self.transactions_table.setMinimumHeight(300)
        
        # أعمدة الجدول
        columns = ['رقم المعاملة', 'التاريخ', 'العنصر', 'التصنيف', 'نوع العملية', 'كمية المعاملة', 
                  'الوقت المتبقي', 'حالة التعديل']
        self.transactions_table.setColumnCount(len(columns))
        self.transactions_table.setHorizontalHeaderLabels(columns)
        
        # ضبط عرض الأعمدة
        header = self.transactions_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # رقم المعاملة
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # التاريخ
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # العنصر
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # التصنيف
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # نوع العملية
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # الكمية
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)  # الوقت المتبقي
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)  # حالة التعديل
        
        # ضبط ارتفاع الصفوف
        header.setStretchLastSection(False)
        self.transactions_table.verticalHeader().setDefaultSectionSize(35)
        
        transactions_layout.addWidget(self.transactions_table)
        main_layout.addWidget(transactions_group, 3)  # 3x stretch factor للجدول
        
        # منطقة التعديل
        edit_group = QGroupBox("تعديل الكمية المختارة")
        edit_layout = QFormLayout(edit_group)
        edit_layout.setContentsMargins(10, 10, 10, 10)
        edit_layout.setSpacing(8)
        
        # عرض معلومات المعاملة المختارة
        self.selected_item_label = QLabel("لم يتم اختيار معاملة")
        self.selected_item_label.setObjectName("selected_info")
        edit_layout.addRow("المعاملة المختارة:", self.selected_item_label)
        
        self.current_quantity_label = QLabel("-")
        self.current_quantity_label.setObjectName("quantity_info")
        edit_layout.addRow("كمية المعاملة:", self.current_quantity_label)
        
        # إدخال الكمية الجديدة
        self.new_quantity_spinbox = QSpinBox()
        self.new_quantity_spinbox.setObjectName("quantity_input")
        self.new_quantity_spinbox.setRange(0, 999999)
        self.new_quantity_spinbox.setValue(0)
        self.new_quantity_spinbox.setEnabled(False)
        edit_layout.addRow("الكمية الجديدة:", self.new_quantity_spinbox)
        
        # عرض الفرق
        self.difference_label = QLabel("-")
        self.difference_label.setObjectName("difference_info")
        edit_layout.addRow("الفرق في الكمية:", self.difference_label)
        
        # سبب التعديل
        self.reason_combo = QComboBox()
        self.reason_combo.setObjectName("reason_combo")
        self.reason_combo.addItems([
            "تصحيح خطأ في الإدخال",
            "إعادة عد المخزون", 
            "تلف أو فقدان",
            "إضافة كمية إضافية",
            "سبب آخر"
        ])
        self.reason_combo.setEnabled(False)
        edit_layout.addRow("سبب التعديل:", self.reason_combo)
        
        # ملاحظات إضافية
        self.notes_text = QTextEdit()
        self.notes_text.setObjectName("notes_text")
        self.notes_text.setMaximumHeight(50)
        self.notes_text.setEnabled(False)
        self.notes_text.setPlaceholderText("ملاحظات إضافية (اختياري)")
        edit_layout.addRow("ملاحظات:", self.notes_text)
        
        main_layout.addWidget(edit_group, 1)  # 1x stretch factor لمنطقة التعديل
        
        # الأزرار
        buttons_layout = QHBoxLayout()
        
        # زر التحديث
        refresh_btn = QPushButton("تحديث القائمة")
        refresh_btn.setObjectName("refresh_button")
        refresh_btn.clicked.connect(self.load_recent_transactions)
        buttons_layout.addWidget(refresh_btn)
        
        buttons_layout.addStretch()
        
        # زر حفظ التعديل
        self.save_btn = QPushButton("حفظ التعديل")
        self.save_btn.setObjectName("save_button")
        self.save_btn.setEnabled(False)
        self.save_btn.clicked.connect(self.save_modification)
        buttons_layout.addWidget(self.save_btn)
        
        # زر الإغلاق
        close_btn = QPushButton("إغلاق")
        close_btn.setObjectName("close_button")
        close_btn.clicked.connect(self.close)
        buttons_layout.addWidget(close_btn)
        
        main_layout.addLayout(buttons_layout)
        
        # ربط الأحداث
        self.transactions_table.itemSelectionChanged.connect(self.on_selection_changed)
        self.new_quantity_spinbox.valueChanged.connect(self.calculate_difference)
    
    def center_on_screen(self):
        """توسيط النافذة على الشاشة"""
        from PyQt6.QtWidgets import QApplication
        
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
    
    def load_recent_transactions(self):
        """تحميل المعاملات الحديثة (آخر 24 ساعة)"""
        try:
            project_file = os.path.join("projects", f"{self.project_name}_Transactions.xlsx")
            
            if not os.path.exists(project_file):
                self.recent_transactions = pd.DataFrame()
                self.update_table()
                return
            
            # قراءة جميع المعاملات
            all_transactions = pd.read_excel(project_file, engine='openpyxl')
            
            if all_transactions.empty:
                self.recent_transactions = pd.DataFrame()
                self.update_table()
                return
            
            # تحويل عمود التاريخ
            all_transactions['التاريخ'] = pd.to_datetime(all_transactions['التاريخ'])
            
            # حساب الحد الزمني (آخر 24 ساعة)
            now = datetime.now()
            time_limit = now - timedelta(hours=24)
            
            # فلترة المعاملات الحديثة فقط
            recent_mask = all_transactions['التاريخ'] >= time_limit
            recent_transactions = all_transactions[recent_mask].copy()
            
            # فلترة المعاملات - إظهار الدخول والخروج الأصلية فقط (إخفاء المعاملات العكسية والتعديلات)
            # استبعاد جميع أنواع التعديلات والمعاملات العكسية نهائياً
            basic_operations_mask = recent_transactions['نوع_العملية'].isin(['دخول', 'خروج'])
            filtered_transactions = recent_transactions[basic_operations_mask].copy()
            
            # استبعاد المعاملات العكسية والمعاملات المعدلة
            if not filtered_transactions.empty:
                try:
                    # تحويل عمود الملاحظات إلى نصوص آمنة إذا كان موجوداً
                    if 'ملاحظات' in filtered_transactions.columns:
                        filtered_transactions['ملاحظات'] = filtered_transactions['ملاحظات'].astype(str).fillna('')
                    
                    # الحصول على قائمة المعاملات المعدلة من ملف التعديلات
                    modified_transaction_ids = self.get_modified_transaction_ids()
                    
                    # فلترة المعاملات
                    if 'ملاحظات' in filtered_transactions.columns and 'رقم_المعاملة' in filtered_transactions.columns:
                        # إخفاء المعاملات العكسية والمعاملات الأصلية المعدلة
                        exclude_mask = (
                            # المعاملات العكسية
                            filtered_transactions['ملاحظات'].str.contains('إلغاء معاملة رقم', na=False) |
                            # المعاملات الأصلية التي تم تعديلها
                            filtered_transactions['رقم_المعاملة'].isin(modified_transaction_ids)
                        )
                        filtered_transactions = filtered_transactions[~exclude_mask].copy()
                    elif 'ملاحظات' in filtered_transactions.columns:
                        # إخفاء المعاملات العكسية فقط إذا لم يكن هناك رقم معاملة
                        exclude_mask = filtered_transactions['ملاحظات'].str.contains('إلغاء معاملة رقم', na=False)
                        filtered_transactions = filtered_transactions[~exclude_mask].copy()
                        
                except Exception as e:
                    # في حالة وجود خطأ، نتجاهل فلترة الملاحظات ونكتفي بفلترة نوع العملية
                    pass
            
            # إظهار جميع المعاملات الأصلية الفردية (وليس فقط الأخيرة لكل عنصر)
            if not filtered_transactions.empty:
                # ترتيب حسب التاريخ (الأحدث أولاً) 
                self.recent_transactions = filtered_transactions.sort_values('التاريخ', ascending=False)
            else:
                self.recent_transactions = filtered_transactions
            
            # ترتيب حسب التاريخ (الأحدث أولاً)
            self.recent_transactions = self.recent_transactions.sort_values('التاريخ', ascending=False)
            
            # إضافة عمود الوقت المتبقي
            self.recent_transactions['الوقت_المتبقي'] = self.recent_transactions['التاريخ'].apply(
                lambda x: self.calculate_time_remaining(x, now)
            )
            
            # إضافة عمود حالة التعديل
            self.recent_transactions['تم_التعديل'] = self.recent_transactions.apply(
                lambda row: self.check_modification_status(row), axis=1
            )
            
            self.update_table()
            
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في تحميل المعاملات: {str(e)}")
            self.recent_transactions = pd.DataFrame()
            self.update_table()
    
    def calculate_time_remaining(self, transaction_time, current_time):
        """حساب الوقت المتبقي للتعديل"""
        time_limit = transaction_time + timedelta(hours=24)
        remaining = time_limit - current_time
        
        if remaining.total_seconds() <= 0:
            return "انتهت الصلاحية"
        
        hours = int(remaining.total_seconds() // 3600)
        minutes = int((remaining.total_seconds() % 3600) // 60)
        
        return f"{hours}س {minutes}د"
    
    def check_modification_status(self, row):
        """فحص حالة التعديل للمعاملة"""
        # فحص إذا كان هناك سجل تعديل لهذه المعاملة
        try:
            modifications_file = os.path.join("projects", f"{self.project_name}_Modifications.xlsx")
            if os.path.exists(modifications_file):
                modifications = pd.read_excel(modifications_file, engine='openpyxl')
                
                if not modifications.empty and 'معرف_المعاملة_الأصلية' in modifications.columns:
                    # البحث عن تعديلات لهذه المعاملة
                    transaction_id = f"{row['التاريخ']}_{row['اسم_العنصر']}_{row['الكمية']}"
                    modified = modifications['معرف_المعاملة_الأصلية'].str.contains(transaction_id, na=False)
                    
                    if modified.any():
                        mod_count = len(modifications[modified])
                        return f"تم التعديل {mod_count} مرة"
            
            return "قابل للتعديل"
            
        except Exception as e:
            return "قابل للتعديل"
    
    def get_modified_transaction_ids(self):
        """الحصول على قائمة أرقام المعاملات التي تم تعديلها"""
        try:
            modifications_file = os.path.join("projects", f"{self.project_name}_Modifications.xlsx")
            modified_ids = []
            
            if os.path.exists(modifications_file):
                modifications = pd.read_excel(modifications_file, engine='openpyxl')
                
                if not modifications.empty and 'معرف_المعاملة_الأصلية' in modifications.columns:
                    # استخراج أرقام المعاملات من المعرف
                    for _, row in modifications.iterrows():
                        transaction_id_str = str(row['معرف_المعاملة_الأصلية'])
                        # المعرف في شكل: "تاريخ_اسم_العنصر_كمية"، نحتاج لاستخراج رقم المعاملة من السجل الأصلي
                        parts = transaction_id_str.split('_')
                        if len(parts) >= 3:
                            # البحث في ملف المعاملات عن المعاملة المطابقة
                            matching_id = self.find_transaction_id_by_details(parts[0], parts[1], parts[2])
                            if matching_id:
                                modified_ids.append(matching_id)
            
            return modified_ids
            
        except Exception as e:
            return []
    
    def find_transaction_id_by_details(self, date_str, item_name, quantity_str):
        """البحث عن رقم المعاملة بناء على التفاصيل"""
        try:
            project_file = os.path.join("projects", f"{self.project_name}_Transactions.xlsx")
            
            if os.path.exists(project_file):
                all_transactions = pd.read_excel(project_file, engine='openpyxl')
                
                if not all_transactions.empty and 'رقم_المعاملة' in all_transactions.columns:
                    # تحويل التاريخ للمقارنة
                    all_transactions['التاريخ'] = pd.to_datetime(all_transactions['التاريخ'])
                    
                    # البحث عن المعاملة المطابقة
                    for _, row in all_transactions.iterrows():
                        row_date = row['التاريخ'].strftime('%Y-%m-%d %H:%M:%S')
                        if (row_date.startswith(date_str.split(' ')[0]) and  # مقارنة التاريخ فقط
                            str(row['اسم_العنصر']) == item_name and 
                            str(int(row['الكمية'])) == quantity_str.split('.')[0]):  # مقارنة الكمية كرقم صحيح
                            return row['رقم_المعاملة']
            
            return None
            
        except Exception as e:
            return None
    
    def is_transaction_editable(self, transaction):
        """تحديد ما إذا كانت المعاملة قابلة للتعديل"""
        try:
            # التحقق من انتهاء الصلاحية
            if "انتهت الصلاحية" in str(transaction['الوقت_المتبقي']):
                return False
                
            # التحقق من وجود عمليات إخراج بعد معاملات الدخول
            if transaction['نوع_العملية'] in ['دخول', 'تعديل زيادة']:
                if self.has_outgoing_transactions_after(transaction['التاريخ'], transaction['اسم_العنصر']):
                    return False
                    
            # باقي المعاملات قابلة للتعديل (مع قيود المخزون)
            return True
            
        except Exception as e:
            # في حالة الخطأ، نفترض عدم قابلية التعديل
            return False
    
    def get_available_stock_excluding_transaction(self, item_name, exclude_transaction_id):
        """حساب المخزون المتاح بدون احتساب معاملة محددة"""
        try:
            project_file = os.path.join("projects", f"{self.project_name}_Transactions.xlsx")
            
            if not os.path.exists(project_file):
                return 0
                
            # قراءة جميع المعاملات
            all_transactions = pd.read_excel(project_file, engine='openpyxl')
            
            if all_transactions.empty:
                return 0
            
            # استبعاد المعاملة المحددة من الحساب
            if 'رقم_المعاملة' in all_transactions.columns:
                item_transactions = all_transactions[
                    (all_transactions['اسم_العنصر'] == item_name) &
                    (all_transactions['رقم_المعاملة'] != exclude_transaction_id)
                ]
            else:
                # للملفات القديمة بدون أرقام معاملات
                item_transactions = all_transactions[all_transactions['اسم_العنصر'] == item_name]
            
            if item_transactions.empty:
                return 0
            
            # حساب المخزون
            incoming = item_transactions[item_transactions['نوع_العملية'] == 'دخول']['الكمية'].sum()
            outgoing = item_transactions[item_transactions['نوع_العملية'] == 'خروج']['الكمية'].sum()
            
            # إضافة عمليات التعديل
            modifications_increase = item_transactions[item_transactions['نوع_العملية'] == 'تعديل زيادة']['الكمية'].sum()
            modifications_decrease = item_transactions[item_transactions['نوع_العملية'] == 'تعديل نقص']['الكمية'].sum()
            
            available_stock = incoming - outgoing + modifications_increase - modifications_decrease
            
            return int(available_stock) if available_stock >= 0 else 0
            
        except Exception as e:
            # في حالة الخطأ، نرجع 0 للأمان
            return 0
    
    def has_outgoing_transactions_after(self, transaction_date, item_name):
        """التحقق من وجود عمليات إخراج بعد المعاملة المحددة"""
        try:
            project_file = os.path.join("projects", f"{self.project_name}_Transactions.xlsx")
            
            if not os.path.exists(project_file):
                return False
                
            # قراءة جميع المعاملات
            all_transactions = pd.read_excel(project_file, engine='openpyxl')
            
            if all_transactions.empty:
                return False
            
            # تحويل التواريخ للمقارنة
            all_transactions['التاريخ'] = pd.to_datetime(all_transactions['التاريخ'])
            transaction_datetime = pd.to_datetime(transaction_date)
            
            # فلترة معاملات نفس العنصر بعد التاريخ المحدد
            item_transactions = all_transactions[
                (all_transactions['اسم_العنصر'] == item_name) &
                (all_transactions['التاريخ'] > transaction_datetime)
            ]
            
            # التحقق من وجود عمليات إخراج
            outgoing_operations = item_transactions[
                item_transactions['نوع_العملية'].isin(['خروج', 'تعديل نقص'])
            ]
            
            return not outgoing_operations.empty
            
        except Exception as e:
            # في حالة الخطأ، نفترض وجود عمليات إخراج للأمان
            return True
    
    def get_current_stock(self, item_name):
        """حساب المخزون الحالي للعنصر بشكل مباشر"""
        try:
            # قراءة ملف المعاملات مباشرة وحساب المخزون
            project_file = os.path.join("projects", f"{self.project_name}_Transactions.xlsx")
            
            if not os.path.exists(project_file):
                return 0
                
            # قراءة جميع المعاملات
            all_transactions = pd.read_excel(project_file, engine='openpyxl')
            
            if all_transactions.empty:
                return 0
            
            # فلترة معاملات العنصر المحدد
            item_transactions = all_transactions[all_transactions['اسم_العنصر'] == item_name]
            
            if item_transactions.empty:
                return 0
            
            # حساب المخزون
            incoming = item_transactions[item_transactions['نوع_العملية'] == 'دخول']['الكمية'].sum()
            outgoing = item_transactions[item_transactions['نوع_العملية'] == 'خروج']['الكمية'].sum()
            
            # إضافة عمليات التعديل إذا كانت موجودة
            modifications_increase = item_transactions[item_transactions['نوع_العملية'] == 'تعديل زيادة']['الكمية'].sum()
            modifications_decrease = item_transactions[item_transactions['نوع_العملية'] == 'تعديل نقص']['الكمية'].sum()
            
            current_stock = incoming - outgoing + modifications_increase - modifications_decrease
            
            return int(current_stock) if current_stock >= 0 else 0
            
        except Exception as e:
            # في حالة الخطأ، محاولة استخدام الطريقة الأصلية
            try:
                inventory_summary = excel_manager.get_inventory_summary(self.project_name)
                if not inventory_summary.empty:
                    item_data = inventory_summary[inventory_summary['اسم_العنصر'] == item_name]
                    if not item_data.empty:
                        return int(item_data.iloc[0]['الكمية_الحالية'])
                return 0
            except:
                return 0
    
    def update_table(self):
        """تحديث جدول المعاملات"""
        if self.recent_transactions.empty:
            self.transactions_table.setRowCount(0)
            return
        
        self.transactions_table.setRowCount(len(self.recent_transactions))
        
        for idx, (_, row) in enumerate(self.recent_transactions.iterrows()):
            # رقم المعاملة
            transaction_id = row.get('رقم_المعاملة', idx + 1)  # استخدام الفهرس كبديل للملفات القديمة
            id_item = QTableWidgetItem(str(transaction_id))
            id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.transactions_table.setItem(idx, 0, id_item)
            
            # التاريخ
            date_item = QTableWidgetItem(row['التاريخ'].strftime('%Y-%m-%d %H:%M'))
            date_item.setFlags(date_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.transactions_table.setItem(idx, 1, date_item)
            
            # العنصر
            item_item = QTableWidgetItem(str(row['اسم_العنصر']))
            item_item.setFlags(item_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.transactions_table.setItem(idx, 2, item_item)
            
            # التصنيف
            category_item = QTableWidgetItem(str(row['التصنيف']))
            category_item.setFlags(category_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.transactions_table.setItem(idx, 3, category_item)
            
            # نوع العملية
            type_item = QTableWidgetItem(str(row['نوع_العملية']))
            type_item.setFlags(type_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.transactions_table.setItem(idx, 4, type_item)
            
            # كمية المعاملة الفردية
            transaction_quantity = int(row['الكمية'])
            quantity_item = QTableWidgetItem(str(transaction_quantity))
            quantity_item.setFlags(quantity_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.transactions_table.setItem(idx, 5, quantity_item)
            
            # الوقت المتبقي
            time_item = QTableWidgetItem(str(row['الوقت_المتبقي']))
            time_item.setFlags(time_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            
            # تلوين الصفوف حسب الوقت المتبقي
            if "انتهت الصلاحية" in str(row['الوقت_المتبقي']):
                time_item.setBackground(Qt.GlobalColor.red)
                time_item.setForeground(Qt.GlobalColor.white)
            elif "س" in str(row['الوقت_المتبقي']):
                hours = int(str(row['الوقت_المتبقي']).split('س')[0])
                if hours < 2:
                    time_item.setBackground(Qt.GlobalColor.yellow)
                else:
                    time_item.setBackground(Qt.GlobalColor.green)
                    time_item.setForeground(Qt.GlobalColor.white)
            
            self.transactions_table.setItem(idx, 6, time_item)
            
            # حالة التعديل - تحديد قابلية التعديل بناءً على القواعد الجديدة
            is_editable = self.is_transaction_editable(row)
            if is_editable:
                status_text = "قابل للتعديل"
                status_color = Qt.GlobalColor.green
                text_color = Qt.GlobalColor.white
            else:
                # تحديد سبب عدم قابلية التعديل
                if "انتهت الصلاحية" in str(row['الوقت_المتبقي']):
                    status_text = "منتهي الصلاحية"
                elif row['نوع_العملية'] in ['دخول', 'تعديل زيادة'] and \
                     self.has_outgoing_transactions_after(row['التاريخ'], row['اسم_العنصر']):
                    status_text = "محمي - وجود خروج لاحق"
                else:
                    status_text = "غير قابل للتعديل"
                status_color = Qt.GlobalColor.red
                text_color = Qt.GlobalColor.white
                
            status_item = QTableWidgetItem(status_text)
            status_item.setFlags(status_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            status_item.setBackground(status_color)
            status_item.setForeground(text_color)
            self.transactions_table.setItem(idx, 7, status_item)
            
            # تلوين الصف بالكامل إذا لم يكن قابلاً للتعديل
            if not is_editable:
                for col in range(8):  # جميع الأعمدة
                    item = self.transactions_table.item(idx, col)
                    if item and col != 7:  # تجنب تغيير عمود الحالة
                        item.setBackground(QColor(240, 240, 240))  # رمادي فاتح
                        item.setForeground(QColor(100, 100, 100))  # نص رمادي
    
    def on_selection_changed(self):
        """عند تغيير اختيار المعاملة"""
        selected_rows = self.transactions_table.selectionModel().selectedRows()
        
        if not selected_rows or self.recent_transactions.empty:
            self.reset_edit_form()
            return
        
        row_index = selected_rows[0].row()
        transaction = self.recent_transactions.iloc[row_index]
        
        # التحقق من صلاحية التعديل
        if "انتهت الصلاحية" in str(transaction['الوقت_المتبقي']):
            self.reset_edit_form()
            self.selected_item_label.setText("هذه المعاملة انتهت صلاحيتها للتعديل")
            return
        
        # التحقق من وجود عمليات إخراج بعد هذه المعاملة (للمعاملات الدخول فقط)
        if transaction['نوع_العملية'] in ['دخول', 'تعديل زيادة']:
            if self.has_outgoing_transactions_after(transaction['التاريخ'], transaction['اسم_العنصر']):
                self.reset_edit_form()
                self.selected_item_label.setText("لا يمكن تعديل هذه المعاملة - توجد عمليات إخراج بعدها")
                return
        
        # تحديث نموذج التعديل - العمل على كمية المعاملة الفردية
        transaction_quantity = int(transaction['الكمية'])
        self.selected_item_label.setText(f"{transaction['اسم_العنصر']} - {transaction['نوع_العملية']} (رقم: {transaction.get('رقم_المعاملة', 'غير محدد')})")
        self.current_quantity_label.setText(str(transaction_quantity))
        self.new_quantity_spinbox.setValue(transaction_quantity)
        
        # تفعيل عناصر التحكم
        self.new_quantity_spinbox.setEnabled(True)
        self.reason_combo.setEnabled(True)
        self.notes_text.setEnabled(True)
        self.save_btn.setEnabled(True)
        
        self.calculate_difference()
    
    def reset_edit_form(self):
        """إعادة تعيين نموذج التعديل"""
        self.selected_item_label.setText("لم يتم اختيار معاملة")
        self.current_quantity_label.setText("-")
        self.difference_label.setText("-")
        self.new_quantity_spinbox.setValue(0)
        self.new_quantity_spinbox.setEnabled(False)
        self.reason_combo.setEnabled(False)
        self.notes_text.setEnabled(False)
        self.notes_text.clear()
        self.save_btn.setEnabled(False)
    
    def calculate_difference(self):
        """حساب فرق الكمية"""
        if not hasattr(self, 'current_quantity_label') or self.current_quantity_label.text() == "-":
            return
        
        try:
            current_qty = int(self.current_quantity_label.text())
            new_qty = self.new_quantity_spinbox.value()
            difference = new_qty - current_qty
            
            # التحقق من عمليات الخروج وعرض تحذير إذا لزم
            selected_rows = self.transactions_table.selectionModel().selectedRows()
            if selected_rows:
                row_index = selected_rows[0].row()
                transaction = self.recent_transactions.iloc[row_index]
                
                if transaction['نوع_العملية'] in ['خروج', 'تعديل نقص']:
                    transaction_id = transaction.get('رقم_المعاملة', None)
                    available_stock = self.get_available_stock_excluding_transaction(
                        transaction['اسم_العنصر'], 
                        transaction_id
                    )
                    
                    if new_qty > available_stock:
                        self.difference_label.setText(f"{difference} - تحذير: يتجاوز المخزون ({available_stock})")
                        self.difference_label.setStyleSheet("color: red; font-weight: bold; background-color: #ffeeee;")
                        return
            
            if difference > 0:
                self.difference_label.setText(f"+{difference} (زيادة)")
                self.difference_label.setStyleSheet("color: green; font-weight: bold;")
            elif difference < 0:
                self.difference_label.setText(f"{difference} (نقص)")
                self.difference_label.setStyleSheet("color: red; font-weight: bold;")
            else:
                self.difference_label.setText("0 (بدون تغيير)")
                self.difference_label.setStyleSheet("color: gray;")
                
        except:
            self.difference_label.setText("-")
    
    def save_modification(self):
        """حفظ التعديل"""
        try:
            selected_rows = self.transactions_table.selectionModel().selectedRows()
            if not selected_rows:
                QMessageBox.warning(self, "خطأ", "يرجى اختيار معاملة للتعديل")
                return
            
            row_index = selected_rows[0].row()
            transaction = self.recent_transactions.iloc[row_index]
            
            # التحقق من وجود عمليات إخراج بعد هذه المعاملة (للمعاملات الدخول فقط)
            if transaction['نوع_العملية'] in ['دخول', 'تعديل زيادة']:
                if self.has_outgoing_transactions_after(transaction['التاريخ'], transaction['اسم_العنصر']):
                    QMessageBox.warning(
                        self, "تحذير", 
                        "لا يمكن تعديل هذه المعاملة لأنه توجد عمليات إخراج تمت بعدها.\n"
                        "تعديل هذه المعاملة قد يؤدي إلى مخزون سالب."
                    )
                    return
            
            current_qty = int(transaction['الكمية'])  # كمية المعاملة الفردية
            new_qty = self.new_quantity_spinbox.value()
            difference = new_qty - current_qty
            
            if difference == 0:
                QMessageBox.information(self, "تنبيه", "لا يوجد تغيير في الكمية")
                return
            
            # التحقق من عمليات الخروج لمنع تجاوز المخزون المتاح
            if transaction['نوع_العملية'] in ['خروج', 'تعديل نقص']:
                # حساب المخزون المتاح بدون احتساب هذه المعاملة
                transaction_id = transaction.get('رقم_المعاملة', None)
                available_stock = self.get_available_stock_excluding_transaction(
                    transaction['اسم_العنصر'], 
                    transaction_id
                )
                
                # التحقق من أن الكمية الجديدة لا تتجاوز المخزون المتاح
                if new_qty > available_stock:
                    QMessageBox.warning(
                        self, "تحذير", 
                        f"لا يمكن تعديل هذه المعاملة إلى {new_qty} وحدة.\n\n"
                        f"المخزون المتاح: {available_stock} وحدة\n"
                        f"الحد الأقصى للخروج: {available_stock} وحدة\n\n"
                        f"تعديل هذه المعاملة قد يؤدي إلى مخزون سالب."
                    )
                    return
            
            # تأكيد التعديل
            reply = QMessageBox.question(
                self, "تأكيد التعديل",
                f"هل أنت متأكد من تعديل الكمية؟\n\n"
                f"العنصر: {transaction['اسم_العنصر']}\n"
                f"الكمية الحالية: {current_qty}\n"
                f"الكمية الجديدة: {new_qty}\n"
                f"الفرق: {difference:+d}\n"
                f"السبب: {self.reason_combo.currentText()}",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply != QMessageBox.StandardButton.Yes:
                return
            
            # تطبيق التعديل
            success = self.apply_modification(transaction, new_qty, difference)
            
            if success:
                QMessageBox.information(self, "نجح", "تم حفظ التعديل بنجاح!")
                self.load_recent_transactions()  # إعادة تحميل البيانات
                self.reset_edit_form()
            
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في حفظ التعديل: {str(e)}")
    
    def apply_modification(self, original_transaction, new_quantity, difference):
        """تطبيق التعديل على المعاملة الفردية"""
        try:
            # 1. تسجيل التعديل في ملف منفصل
            self.log_modification(original_transaction, new_quantity, difference)
            
            # 2. تسجيل معاملة التعديل (بدون حذف الأصلية)
            self.record_modification_transaction(original_transaction, difference)
            
            # 3. تحديث المعاملة الأصلية بالكمية الجديدة
            self.add_corrected_individual_transaction(original_transaction, new_quantity)
            
            return True
            
        except Exception as e:
            raise e
    
    def record_modification_transaction(self, original_transaction, difference):
        """تسجيل معاملة التعديل في السجل (تعديل زيادة أو تعديل نقص)"""
        try:
            # تحديد نوع التعديل بناءً على الفرق
            if difference > 0:
                modification_type = 'تعديل زيادة'
            else:
                modification_type = 'تعديل نقص'
            
            # الحصول على رقم المعاملة المرجعية
            reference_id = original_transaction.get('رقم_المعاملة', None)
            
            # الحصول على التاريخ
            original_date = original_transaction['التاريخ']
            if isinstance(original_date, str):
                custom_date = original_date
            else:
                custom_date = original_date.strftime('%Y-%m-%d %H:%M:%S')
            
            # تسجيل معاملة التعديل مع نقل معلومات العنصر الكاملة (بما فيها الصلاحية)
            excel_manager.record_transaction(
                self.project_name,
                original_transaction['اسم_العنصر'],
                abs(difference),  # قيمة التعديل (موجبة دائماً)
                modification_type,  # نوع التعديل (زيادة أو نقص)
                f'{self.reason_combo.currentText()}',
                custom_date=custom_date,
                reference_id=reference_id,
                category=original_transaction['التصنيف'],
                item_details=original_transaction  # نقل معلومات العنصر بما فيها الصلاحية
            )
            
        except Exception as e:
            raise Exception(f"خطأ في تسجيل معاملة التعديل: {str(e)}")
    
    def log_modification(self, original_transaction, new_quantity, difference):
        """تسجيل التعديل في ملف منفصل"""
        try:
            modifications_file = os.path.join("projects", f"{self.project_name}_Modifications.xlsx")
            
            # إنشاء سجل التعديل
            modification_record = {
                'تاريخ_التعديل': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'معرف_المعاملة_الأصلية': f"{original_transaction['التاريخ']}_{original_transaction['اسم_العنصر']}_{original_transaction['الكمية']}",
                'اسم_العنصر': original_transaction['اسم_العنصر'],
                'التصنيف': original_transaction['التصنيف'],
                'نوع_العملية': original_transaction['نوع_العملية'],
                'تاريخ_المعاملة_الأصلية': original_transaction['التاريخ'],
                'الكمية_الأصلية': original_transaction['الكمية'],
                'الكمية_الجديدة': new_quantity,
                'فرق_الكمية': difference,
                'سبب_التعديل': self.reason_combo.currentText(),
                'ملاحظات': self.notes_text.toPlainText(),
                'المستخدم': 'النظام',  # يمكن إضافة نظام المستخدمين لاحقاً
            }
            
            # قراءة التعديلات الموجودة أو إنشاء ملف جديد
            if os.path.exists(modifications_file):
                modifications_df = pd.read_excel(modifications_file, engine='openpyxl')
                modifications_df = pd.concat([modifications_df, pd.DataFrame([modification_record])], ignore_index=True)
            else:
                modifications_df = pd.DataFrame([modification_record])
            
            # حفظ التعديلات
            modifications_df.to_excel(modifications_file, index=False, engine='openpyxl')
            
        except Exception as e:
            raise Exception(f"خطأ في تسجيل التعديل: {str(e)}")
    

    def add_corrected_individual_transaction(self, original_transaction, new_quantity):
        """تحديث المعاملة الأصلية بالكمية الجديدة (بدون إضافة معاملة جديدة)"""
        try:
            # بدلاً من إضافة معاملة جديدة، نحدث المعاملة الأصلية مباشرة في السجل
            project_file = os.path.join("projects", f"{self.project_name}_Transactions.xlsx")
            
            if not os.path.exists(project_file):
                raise Exception("ملف المشروع غير موجود")
            
            # قراءة ملف المعاملات
            transactions_df = pd.read_excel(project_file, engine='openpyxl')
            
            # البحث عن المعاملة الأصلية بناءً على التفاصيل
            original_date = original_transaction['التاريخ']
            if isinstance(original_date, str):
                search_date = original_date
            else:
                search_date = original_date.strftime('%Y-%m-%d %H:%M:%S')
            
            # إيجاد الصف المطابق
            mask = (
                (transactions_df['التاريخ'].astype(str).str.contains(search_date[:10], na=False)) &
                (transactions_df['اسم_العنصر'] == original_transaction['اسم_العنصر']) &
                (transactions_df['الكمية'] == original_transaction['الكمية']) &
                (transactions_df['نوع_العملية'] == original_transaction['نوع_العملية'])
            )
            
            matching_rows = transactions_df[mask]
            
            if matching_rows.empty:
                raise Exception("لم يتم العثور على المعاملة المراد تحديثها")
            
            # تحديث الكمية للمعاملة الأولى المطابقة
            first_match_idx = matching_rows.index[0]
            transactions_df.at[first_match_idx, 'الكمية'] = new_quantity
            
            # محاولة تحديث الصلاحية إذا كانت موجودة في المعاملة الأصلية
            if 'أيام_الصلاحية' in original_transaction and pd.notna(original_transaction['أيام_الصلاحية']):
                if 'أيام_الصلاحية' in transactions_df.columns:
                    transactions_df.at[first_match_idx, 'أيام_الصلاحية'] = original_transaction['أيام_الصلاحية']
            
            # تحديث الملاحظات بإضافة ملاحظة التعديل
            existing_notes = str(transactions_df.at[first_match_idx, 'ملاحظات']) if 'ملاحظات' in transactions_df.columns else ""
            if existing_notes and existing_notes != 'nan':
                new_notes = f"{existing_notes} | تم التعديل: {self.reason_combo.currentText()}"
            else:
                new_notes = f"تم التعديل: {self.reason_combo.currentText()}"
            
            if 'ملاحظات' in transactions_df.columns:
                transactions_df.at[first_match_idx, 'ملاحظات'] = new_notes
            
            # حفظ التغييرات
            transactions_df.to_excel(project_file, index=False, engine='openpyxl')
            
        except Exception as e:
            raise Exception(f"خطأ في تحديث المعاملة: {str(e)}")
    
    def setup_styles(self):
        """إعداد التنسيقات"""
        style = """
        QDialog {
            background-color: #ecf0f1;
        }
        
        QLabel#title {
            font-size: 18px;
            font-weight: bold;
            color: #1a252f;
            background-color: #ffffff;
            border: 2px solid #3498db;
            border-radius: 8px;
            padding: 15px;
        }
        
        QLabel#info {
            font-size: 9px;
            color: #2c3e50;
            background-color: #d5dbdb;
            border: 1px solid #85929e;
            border-radius: 15px;
            padding: 8px;
            font-weight: bold;
        }
        
        QGroupBox {
            font-size: 13px;
            font-weight: bold;
            color: #1a252f;
            background-color: #ffffff;
            border: 3px solid #2980b9;
            border-radius: 10px;
            margin-top: 15px;
            padding-top: 15px;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 15px;
            padding: 5px 12px;
            background-color: #2980b9;
            color: white;
            border-radius: 5px;
            font-weight: bold;
        }
        
        QTableWidget#transactions_table {
            background-color: #ffffff;
            border: 2px solid #2c3e50;
            border-radius: 8px;
            gridline-color: #bdc3c7;
            font-size: 11px;
            color: #1a252f;
            font-weight: bold;
            selection-background-color: #2980b9;
        }
        
        QTableWidget#transactions_table QHeaderView::section {
            background-color: #34495e;
            color: white;
            padding: 10px;
            border: 1px solid #2c3e50;
            font-weight: bold;
            font-size: 12px;
            height: 40px;
        }
        
        QTableWidget#transactions_table::item {
            padding: 10px;
            border-bottom: 1px solid #bdc3c7;
            color: #1a252f;
            height: 35px;
        }
        
        QTableWidget#transactions_table::item:selected {
            background-color: #2980b9;
            color: white;
            font-weight: bold;
        }
        
        QTableWidget#transactions_table::item:hover {
            background-color: #d5dbdb;
            color: #1a252f;
        }
        
        QLabel#selected_info, QLabel#quantity_info {
            font-size: 12px;
            font-weight: bold;
            color: #1a252f;
            background-color: #d5dbdb;
            border: 1px solid #85929e;
            border-radius: 4px;
            padding: 8px;
        }
        
        QSpinBox#quantity_input {
            font-size: 12px;
            font-weight: bold;
            padding: 8px;
            border: 2px solid #2c3e50;
            border-radius: 6px;
            background-color: #ffffff;
            color: #1a252f;
        }
        
        QSpinBox#quantity_input:focus {
            border-color: #e74c3c;
            background-color: #fdf2e9;
        }
        
        QComboBox#reason_combo {
            font-size: 12px;
            font-weight: bold;
            padding: 8px;
            border: 2px solid #2c3e50;
            border-radius: 6px;
            background-color: #ffffff;
            color: #1a252f;
        }
        
        QComboBox#reason_combo:focus {
            border-color: #e74c3c;
        }
        
        QTextEdit#notes_text {
            font-size: 11px;
            font-weight: bold;
            border: 2px solid #2c3e50;
            border-radius: 6px;
            background-color: #ffffff;
            color: #1a252f;
            padding: 8px;
        }
        
        QTextEdit#notes_text:focus {
            border-color: #e74c3c;
            background-color: #fdf2e9;
        }
        
        QPushButton#refresh_button {
            background-color: #17a2b8;
            color: white;
            font-size: 12px;
            font-weight: bold;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            min-width: 100px;
        }
        
        QPushButton#refresh_button:hover {
            background-color: #138496;
        }
        
        QPushButton#save_button {
            background-color: #28a745;
            color: white;
            font-size: 12px;
            font-weight: bold;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            min-width: 100px;
        }
        
        QPushButton#save_button:hover {
            background-color: #218838;
        }
        
        QPushButton#save_button:disabled {
            background-color: #6c757d;
        }
        
        QPushButton#close_button {
            background-color: #6c757d;
            color: white;
            font-size: 12px;
            font-weight: bold;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            min-width: 100px;
        }
        
        QPushButton#close_button:hover {
            background-color: #545b62;
        }
        
        QPushButton#control_button {
            background-color: #3498db;
            color: white;
            font-size: 11px;
            font-weight: bold;
            border: none;
            border-radius: 6px;
            padding: 6px 12px;
            min-width: 120px;
        }
        
        QPushButton#control_button:hover {
            background-color: #2980b9;
        }
        
        QPushButton#control_button:checked {
            background-color: #e74c3c;
        }
        
        QPushButton#control_button:checked:hover {
            background-color: #c0392b;
        }
        
        /* تنسيق إضافي للوضوح */
        QFormLayout QLabel {
            font-size: 12px;
            font-weight: bold;
            color: #1a252f;
            background-color: #aed6f1;
            padding: 6px 8px;
            border-radius: 4px;
            margin-right: 5px;
        }
        
        QLabel#difference_info {
            font-size: 12px;
            font-weight: bold;
            padding: 8px;
            border: 2px solid #2c3e50;
            border-radius: 6px;
            background-color: #ffffff;
        }
        
        QTableWidget QHeaderView::section {
            background-color: #2c3e50;
            color: white;
            font-weight: bold;
            font-size: 11px;
            padding: 8px;
            border: 1px solid #34495e;
        }
        
        QTableWidget QHeaderView::section:hover {
            background-color: #34495e;
        }
        """
        
        self.setStyleSheet(style)
        self.setup_message_box_style()
    
    def setup_message_box_style(self):
        """إعداد تنسيق رسائل التنبيه"""
        from PyQt6.QtWidgets import QApplication
        message_style = """
        QMessageBox {
            background-color: #ffffff;
            color: #2c3e50;
            font-size: 11px;
            font-weight: bold;
        }
        QMessageBox QLabel {
            color: #2c3e50;
            font-size: 11px;
            font-weight: bold;
            padding: 8px;
            min-height: 30px;
        }
        QMessageBox QPushButton {
            background-color: #17a2b8;
            color: white;
            font-size: 10px;
            font-weight: bold;
            border: none;
            border-radius: 5px;
            padding: 6px 12px;
            min-width: 70px;
        }
        QMessageBox QPushButton:hover {
            background-color: #138496;
        }
        QMessageBox QPushButton:pressed {
            background-color: #0e6674;
        }
        """
        QApplication.instance().setStyleSheet(QApplication.instance().styleSheet() + message_style)
    
    def closeEvent(self, event):
        """إيقاف التايمر عند إغلاق النافذة"""
        if hasattr(self, 'timer'):
            self.timer.stop()
        event.accept()