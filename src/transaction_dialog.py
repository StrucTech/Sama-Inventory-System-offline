# -*- coding: utf-8 -*-
"""
واجهة إدخال وإخراج العناصر من المخزن
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QLineEdit, QTextEdit, QFormLayout,
                           QMessageBox, QSpinBox, QFrame, QComboBox, QTableWidget, 
                           QTableWidgetItem, QHeaderView, QSplitter)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIntValidator, QDoubleValidator
from excel_manager import excel_manager
import pandas as pd


class TransactionDialog(QDialog):
    """نافذة إدخال وإخراج العناصر"""
    
    def __init__(self, project_name, transaction_type, parent=None):
        super().__init__(parent)
        self.project_name = project_name
        self.transaction_type = transaction_type  # "دخول" أو "خروج"
        self.item_info = None
        self.setup_ui()
        self.setup_styles()
    
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        title = f"إدخال عناصر للمخزن" if self.transaction_type == "دخول" else "إخراج عناصر من المخزن"
        self.setWindowTitle(title)
        self.setModal(True)
        
        # تحديد حجم النافذة وتوسيطها
        if self.transaction_type == "خروج":
            # إعداد النافذة لأقصى عرض وطول
            from PyQt6.QtWidgets import QApplication
            screen = QApplication.primaryScreen().geometry()
            self.setMinimumSize(screen.width(), screen.height())
            self.setMaximumSize(screen.width(), screen.height())
            self.resize(screen.width(), screen.height())
            self.showMaximized()
        else:
            self.resize(600, 500)  # حجم عادي للدخول
            self.center_on_screen()
        
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        # التخطيط الرئيسي
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        if self.transaction_type == "خروج":
            main_layout.setContentsMargins(20, 20, 20, 20)  # هوامش أصغر للخروج
        else:
            main_layout.setContentsMargins(30, 30, 30, 30)  # هوامش عادية للدخول
        
        # العنوان
        title_label = QLabel(title)
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # معلومات المشروع
        project_label = QLabel(f"المشروع: {self.project_name}")
        project_label.setObjectName("project_info")
        project_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(project_label)
        
        # للخروج، إضافة جدول العناصر المتاحة
        if self.transaction_type == "خروج":
            self.create_inventory_table()
            main_layout.addWidget(self.inventory_table)
        
        # إطار البيانات
        form_frame = QFrame()
        form_frame.setObjectName("form_frame")
        form_frame.setFrameStyle(QFrame.Shape.Box)
        form_layout = QFormLayout(form_frame)
        form_layout.setSpacing(15)
        
        if self.transaction_type == "خروج":
            # للخروج: عرض معلومات العنصر المحدد
            self.selected_item_label = QLabel("اختر عنصر من الجدول أعلاه")
            self.selected_item_label.setObjectName("selected_item")
            self.selected_item_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            form_layout.addRow("العنصر المحدد:", self.selected_item_label)
            
            # الكمية المتاحة
            self.available_qty_label = QLabel("-")
            self.available_qty_label.setObjectName("readonly_field")
            form_layout.addRow("الكمية المتاحة:", self.available_qty_label)
        else:
            # للدخول: النظام القديم
            self.category_combo = QComboBox()
            self.category_combo.setObjectName("combo_field")
            self.category_combo.setPlaceholderText("اختر التصنيف")
            self.category_combo.currentTextChanged.connect(self.load_items_by_category)
            form_layout.addRow("التصنيف:", self.category_combo)
            
            self.item_combo = QComboBox()
            self.item_combo.setObjectName("combo_field")
            self.item_combo.setPlaceholderText("اختر العنصر")
            self.item_combo.currentTextChanged.connect(self.load_selected_item_info)
            self.item_combo.setEnabled(False)
            form_layout.addRow("العنصر:", self.item_combo)
            
            self.shelf_life_label = QLabel("-")
            self.shelf_life_label.setObjectName("readonly_field")
            form_layout.addRow("مدة الصلاحية (أيام):", self.shelf_life_label)
        
        # الكمية المطلوبة
        self.quantity_edit = QLineEdit()
        self.quantity_edit.setPlaceholderText("أدخل الكمية")
        self.quantity_edit.setObjectName("input_field")
        self.quantity_edit.setValidator(QDoubleValidator(0.0, 999999.99, 2))
        form_layout.addRow("الكمية:", self.quantity_edit)
        
        # اسم المستلم (للخروج فقط)
        if self.transaction_type == "خروج":
            self.receiver_edit = QLineEdit()
            self.receiver_edit.setPlaceholderText("أدخل اسم المستلم")
            self.receiver_edit.setObjectName("input_field")
            form_layout.addRow("اسم المستلم:", self.receiver_edit)
        
        # الملاحظات
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("ملاحظات إضافية (اختيارية)")
        self.notes_edit.setObjectName("text_area")
        self.notes_edit.setMaximumHeight(100)
        form_layout.addRow("ملاحظات:", self.notes_edit)
        
        main_layout.addWidget(form_frame)
        
        # الأزرار
        buttons_layout = QHBoxLayout()
        
        # زر الحفظ
        save_text = "حفظ الدخول" if self.transaction_type == "دخول" else "حفظ الخروج"
        self.save_btn = QPushButton(save_text)
        self.save_btn.setObjectName("save_button")
        self.save_btn.clicked.connect(self.save_transaction)
        buttons_layout.addWidget(self.save_btn)
        
        # زر الإلغاء
        cancel_btn = QPushButton("إلغاء")
        cancel_btn.setObjectName("cancel_button")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        main_layout.addLayout(buttons_layout)
        
        # إضافة زر لإدارة العناصر
        manage_items_btn = QPushButton("إنشاء عنصر جديد")
        manage_items_btn.setObjectName("manage_button")
        manage_items_btn.clicked.connect(self.show_items_manager)
        main_layout.addWidget(manage_items_btn)
        
        # تحميل التصنيفات للدخول فقط
        if self.transaction_type == "دخول":
            self.load_categories()
    
    def center_on_screen(self):
        """توسيط النافذة على الشاشة"""
        from PyQt6.QtWidgets import QApplication
        
        # الحصول على حجم الشاشة
        screen = QApplication.primaryScreen().geometry()
        
        # حساب الموقع لتوسيط النافذة
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        
        # تحديد موقع النافذة
        self.move(x, y)
    
    def create_inventory_table(self):
        """إنشاء جدول العناصر المتاحة للخروج"""
        self.inventory_table = QTableWidget()
        self.inventory_table.setObjectName("inventory_table")
        
        # إعداد الأعمدة
        self.inventory_table.setColumnCount(4)
        headers = ["اسم العنصر", "التصنيف", "الكمية المتاحة", "مدة الصلاحية"]
        self.inventory_table.setHorizontalHeaderLabels(headers)
        
        # إعداد خصائص الجدول
        self.inventory_table.setAlternatingRowColors(True)
        self.inventory_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.inventory_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        
        # ضبط عرض الأعمدة
        header = self.inventory_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # اسم العنصر
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # التصنيف
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # الكمية
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # الصلاحية
        
        # الجدول يستخدم كامل المساحة المتاحة
        self.inventory_table.setMinimumHeight(500)
        # إزالة الحد الأقصى ليتوسع حسب النافذة
        
        # تحميل البيانات
        self.load_inventory_data()
        
        # ربط حدث اختيار الصف
        self.inventory_table.itemSelectionChanged.connect(self.on_inventory_selection_changed)
    
    def load_inventory_data(self):
        """تحميل بيانات المخزون في الجدول"""
        try:
            inventory = excel_manager.get_inventory_summary(self.project_name)
            
            if not inventory.empty:
                # تصفية العناصر المتاحة فقط (الكمية > 0)
                available_inventory = inventory[inventory['الكمية_الحالية'] > 0]
                
                self.inventory_table.setRowCount(len(available_inventory))
                
                for row, (_, item) in enumerate(available_inventory.iterrows()):
                    # اسم العنصر
                    self.inventory_table.setItem(row, 0, QTableWidgetItem(str(item['اسم_العنصر'])))
                    
                    # التصنيف
                    self.inventory_table.setItem(row, 1, QTableWidgetItem(str(item['التصنيف'])))
                    
                    # الكمية المتاحة
                    qty_item = QTableWidgetItem(str(item['الكمية_الحالية']))
                    qty_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.inventory_table.setItem(row, 2, qty_item)
                    
                    # مدة الصلاحية
                    shelf_life = item.get('مدة_الصلاحية_بالأيام', None)
                    if shelf_life is not None and pd.notna(shelf_life):
                        shelf_text = f"{int(shelf_life)} أيام"
                    else:
                        shelf_text = "غير محدد"
                    shelf_item = QTableWidgetItem(shelf_text)
                    shelf_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.inventory_table.setItem(row, 3, shelf_item)
            else:
                self.inventory_table.setRowCount(0)
                
        except Exception as e:
            print(f"خطأ في تحميل بيانات المخزون: {e}")
            QMessageBox.warning(self, "خطأ", f"خطأ في تحميل بيانات المخزون: {str(e)}")
    
    def on_inventory_selection_changed(self):
        """عند اختيار عنصر من الجدول"""
        if self.transaction_type != "خروج":
            return
            
        current_row = self.inventory_table.currentRow()
        if current_row >= 0:
            # الحصول على بيانات العنصر من الجدول
            item_name = self.inventory_table.item(current_row, 0).text()
            category = self.inventory_table.item(current_row, 1).text()
            available_qty = float(self.inventory_table.item(current_row, 2).text())
            shelf_life = self.inventory_table.item(current_row, 3).text()
            
            # تحديث المعلومات المعروضة
            self.selected_item_label.setText(f"{item_name} - {category}")
            self.available_qty_label.setText(str(available_qty))
            
            # البحث عن معلومات العنصر الكاملة
            try:
                # البحث في ملف العناصر الأساسية
                master_items = excel_manager.get_all_items()
                if not master_items.empty:
                    item_row = master_items[master_items['اسم_العنصر'] == item_name]
                    if not item_row.empty:
                        self.selected_item_id = item_row.iloc[0]['Item_ID']
                        self.item_info = {
                            'اسم العنصر': item_name,
                            'التصنيف': category,
                            'مدة الصلاحية (أيام)': item_row.iloc[0]['مدة_الصلاحية_بالأيام'],
                            'وصف': item_row.iloc[0]['وصف'],
                            'Item_ID': self.selected_item_id
                        }
                        
                        # تحديد الحد الأقصى للكمية
                        validator = self.quantity_edit.validator()
                        if isinstance(validator, QDoubleValidator):
                            validator.setTop(available_qty)
                            
            except Exception as e:
                print(f"خطأ في تحميل معلومات العنصر: {e}")
    
    def setup_styles(self):
        """إعداد التنسيقات"""
        style = """
        QDialog {
            background-color: #ecf0f1;
        }
        
        QLabel#title {
            font-size: 20px;
            font-weight: bold;
            color: #2c3e50;
            padding: 10px;
        }
        
        QLabel#project_info {
            font-size: 16px;
            font-weight: bold;
            color: #3498db;
            padding: 5px;
        }
        
        QFrame#form_frame {
            background-color: white;
            border: 2px solid #bdc3c7;
            border-radius: 10px;
            padding: 20px;
        }
        
        QLineEdit#input_field {
            font-size: 14px;
            padding: 10px;
            border: 2px solid #bdc3c7;
            border-radius: 5px;
            background-color: white;
            color: #2c3e50;
            min-height: 20px;
        }
        
        QLineEdit#input_field:focus {
            border-color: #3498db;
            background-color: #ffffff;
            color: #2c3e50;
        }
        
        QLabel#readonly_field {
            font-size: 14px;
            font-weight: bold;
            color: #2c3e50;
            background-color: #ecf0f1;
            border: 1px solid #bdc3c7;
            border-radius: 5px;
            padding: 10px;
            min-height: 20px;
        }
        
        QLabel#selected_item {
            font-size: 14px;
            font-weight: bold;
            color: #3498db;
            background-color: #e8f4fd;
            border: 2px solid #3498db;
            border-radius: 5px;
            padding: 10px;
            min-height: 20px;
        }
        
        QTextEdit#text_area {
            font-size: 13px;
            border: 2px solid #bdc3c7;
            border-radius: 5px;
            background-color: white;
            color: #2c3e50;
        }
        
        QComboBox#combo_field {
            font-size: 14px;
            padding: 10px;
            border: 2px solid #bdc3c7;
            border-radius: 5px;
            background-color: white;
            color: #2c3e50;
            min-height: 20px;
        }
        
        QComboBox#combo_field:focus {
            border-color: #3498db;
        }
        
        QComboBox#combo_field::drop-down {
            border: none;
            width: 25px;
        }
        
        QComboBox#combo_field::down-arrow {
            image: none;
            border-left: 6px solid transparent;
            border-right: 6px solid transparent;
            border-top: 6px solid #2c3e50;
            width: 0px;
            height: 0px;
        }
        
        QComboBox#combo_field QAbstractItemView {
            background-color: white;
            color: #2c3e50;
            selection-background-color: #3498db;
            selection-color: white;
            border: 1px solid #bdc3c7;
        }
        
        QTextEdit#text_area:focus {
            border-color: #3498db;
            background-color: #ffffff;
        }
        
        QTableWidget#inventory_table {
            background-color: white;
            border: 2px solid #bdc3c7;
            border-radius: 5px;
            gridline-color: #bdc3c7;
            font-size: 14px;
            color: #2c3e50;
        }
        
        QTableWidget#inventory_table::item {
            padding: 10px;
            border-bottom: 1px solid #bdc3c7;
            color: #2c3e50;
            background-color: white;
        }
        
        QTableWidget#inventory_table::item:selected {
            background-color: #3498db;
            color: white;
            font-weight: bold;
            border: 2px solid #2980b9;
        }
        
        QTableWidget#inventory_table::item:hover {
            background-color: #e8f4fd;
            color: #2c3e50;
        }
        
        QTableWidget#inventory_table::item:alternate {
            background-color: #f1f2f6;
            color: #2c3e50;
        }
        
        QHeaderView::section {
            background-color: #2c3e50;
            color: white;
            padding: 12px;
            border: 1px solid #34495e;
            font-weight: bold;
            font-size: 14px;
        }
        
        QPushButton#save_button {
            background-color: #27ae60;
            color: white;
            font-size: 16px;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            padding: 12px 30px;
            min-height: 25px;
        }
        
        QPushButton#save_button:hover {
            background-color: #2ecc71;
        }
        
        QPushButton#save_button:disabled {
            background-color: #bdc3c7;
        }
        
        QPushButton#cancel_button {
            background-color: #e74c3c;
            color: white;
            font-size: 16px;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            padding: 12px 30px;
            min-height: 25px;
        }
        
        QPushButton#cancel_button:hover {
            background-color: #c0392b;
        }
        
        QPushButton#small_button {
            background-color: #3498db;
            color: white;
            font-size: 12px;
            border: none;
            border-radius: 5px;
            padding: 8px 15px;
            min-height: 15px;
        }
        
        QPushButton#small_button:hover {
            background-color: #2980b9;
        }
        
        QPushButton#manage_button {
            background-color: #9b59b6;
            color: white;
            font-size: 14px;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            padding: 10px;
            min-height: 20px;
        }
        
        QPushButton#manage_button:hover {
            background-color: #8e44ad;
        }
        """
        
        self.setStyleSheet(style)
    
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
            background-color: #f39c12;
            color: white;
            font-size: 10px;
            font-weight: bold;
            border: none;
            border-radius: 5px;
            padding: 6px 12px;
            min-width: 70px;
        }
        QMessageBox QPushButton:hover {
            background-color: #e67e22;
        }
        QMessageBox QPushButton:pressed {
            background-color: #d35400;
        }
        """
        QApplication.instance().setStyleSheet(QApplication.instance().styleSheet() + message_style)
    
    def load_categories(self):
        """تحميل قائمة التصنيفات"""
        try:
            categories = excel_manager.get_all_categories()
            self.category_combo.clear()
            self.category_combo.addItem("اختر التصنيف")
            if categories:
                self.category_combo.addItems(categories)
        except Exception as e:
            QMessageBox.warning(self, "خطأ", f"خطأ في تحميل التصنيفات: {str(e)}")
    
    def load_items_by_category(self):
        """تحميل العناصر حسب التصنيف المختار"""
        category = self.category_combo.currentText()
        
        # إعادة تعيين العناصر والمعلومات
        self.item_combo.clear()
        self.clear_item_info()
        
        if not category or category == "اختر التصنيف":
            self.item_combo.setEnabled(False)
            return
        
        try:
            items = excel_manager.get_items_by_category(category)
            self.item_combo.setEnabled(True)
            self.item_combo.addItem("اختر العنصر")
            
            if not items.empty:
                for _, item in items.iterrows():
                    item_text = f"{item['اسم_العنصر']} (ID: {item['Item_ID']})"
                    self.item_combo.addItem(item_text, item['Item_ID'])
        except Exception as e:
            QMessageBox.warning(self, "خطأ", f"خطأ في تحميل العناصر: {str(e)}")
    
    def load_selected_item_info(self):
        """تحميل معلومات العنصر المختار"""
        if self.item_combo.currentIndex() <= 0:  # إذا لم يتم اختيار عنصر
            self.clear_item_info()
            return
        
        try:
            item_id = self.item_combo.currentData()
            if item_id:
                self.item_info = excel_manager.get_item_info(item_id)
                
                if self.item_info is not None:
                    # عرض مدة الصلاحية
                    shelf_life = self.item_info.get('مدة الصلاحية (أيام)', None)
                    if shelf_life is not None and pd.notna(shelf_life):
                        self.shelf_life_label.setText(f"{int(shelf_life)} أيام")
                    else:
                        self.shelf_life_label.setText("غير محدد")
                    
                    # للخروج، تحميل الكمية المتاحة
                    if self.transaction_type == "خروج":
                        self.load_available_quantity(item_id)
                else:
                    QMessageBox.warning(self, "تنبيه", f"لم يتم العثور على معلومات العنصر")
        except Exception as e:
            QMessageBox.warning(self, "خطأ", f"خطأ في تحميل معلومات العنصر: {str(e)}")
    
    def clear_item_info(self):
        """مسح معلومات العنصر"""
        self.item_id_label.setText("-")
        self.shelf_life_label.setText("-")
        if hasattr(self, 'available_qty_label'):
            self.available_qty_label.setText("-")
        self.item_info = None
    
    def load_item_info(self):
        """تحميل معلومات العنصر عند إدخال الرقم - دالة قديمة للتوافق"""
        try:
            item_id = self.item_id_edit.text().strip()
            if not item_id:
                self.clear_item_info()
                return
            
            # التحقق من صحة الرقم
            try:
                item_id = int(item_id)
            except ValueError:
                self.clear_item_info()
                return
            
            # هذه الدالة لم تعد مستخدمة - تم استبدالها بالنظام الجديد
            pass
                
        except Exception as e:
            print(f"خطأ في الدالة القديمة: {e}")
    
    def load_available_quantity(self, item_id):
        """تحميل الكمية المتاحة للعنصر"""
        try:
            inventory = excel_manager.get_inventory_summary(self.project_name)
            
            if not inventory.empty:
                item_inventory = inventory[inventory['اسم_العنصر'] == self.item_info['اسم العنصر']]
                if not item_inventory.empty:
                    available_qty = item_inventory.iloc[0]['الكمية_الحالية']
                    self.available_qty_label.setText(f"{available_qty}")
                    
                    # تحديد الحد الأقصى للكمية المسموح إخراجها
                    if hasattr(self.quantity_edit, 'validator'):
                        validator = self.quantity_edit.validator()
                        if isinstance(validator, QDoubleValidator):
                            validator.setTop(available_qty)
                else:
                    self.available_qty_label.setText("0")
            else:
                self.available_qty_label.setText("0")
                
        except Exception as e:
            self.available_qty_label.setText("غير محدد")
            print(f"خطأ في تحميل الكمية المتاحة: {e}")
    
    def clear_item_info(self):
        """مسح معلومات العنصر"""
        self.shelf_life_label.setText("-")
        if hasattr(self, 'available_qty_label'):
            self.available_qty_label.setText("-")
        self.item_info = None
    
    def refresh_item_info(self):
        """تحديث معلومات العنصر"""
        self.load_item_info()
    
    def validate_inputs(self):
        """التحقق من صحة البيانات المدخلة"""
        if self.transaction_type == "خروج":
            # للخروج: التحقق من اختيار عنصر من الجدول
            if not hasattr(self, 'selected_item_id') or not self.item_info:
                QMessageBox.warning(self, "خطأ", "يرجى اختيار عنصر من الجدول أعلاه")
                return False
        else:
            # للدخول: التحقق من اختيار التصنيف والعنصر
            if self.category_combo.currentIndex() <= 0:
                QMessageBox.warning(self, "خطأ", "يرجى اختيار التصنيف")
                return False
            
            if self.item_combo.currentIndex() <= 0:
                QMessageBox.warning(self, "خطأ", "يرجى اختيار العنصر")
                return False
        
        # التحقق من وجود معلومات العنصر
        if not self.item_info:
            QMessageBox.warning(self, "خطأ", "خطأ في معلومات العنصر")
            return False
        
        # التحقق من الكمية
        try:
            quantity = float(self.quantity_edit.text().strip())
            if quantity <= 0:
                QMessageBox.warning(self, "خطأ", "يجب أن تكون الكمية أكبر من صفر")
                return False
        except ValueError:
            QMessageBox.warning(self, "خطأ", "يرجى إدخال كمية صحيحة")
            return False
        
        # التحقق من الكمية المتاحة عند الخروج
        if self.transaction_type == "خروج":
            try:
                available_text = self.available_qty_label.text()
                if available_text != "-" and available_text != "غير محدد":
                    available_qty = float(available_text)
                    if quantity > available_qty:
                        QMessageBox.warning(
                            self, "خطأ", 
                            f"الكمية المطلوبة ({quantity}) أكبر من المتاحة ({available_qty})"
                        )
                        return False
            except ValueError:
                QMessageBox.warning(self, "خطأ", "خطأ في قراءة الكمية المتاحة")
                return False
        
        return True
    
    def save_transaction(self):
        """حفظ الحركة"""
        if not self.validate_inputs():
            return
        
        try:
            quantity = float(self.quantity_edit.text().strip())
            notes = self.notes_edit.toPlainText().strip()
            
            # اسم المستلم (للخروج فقط)
            receiver_name = ""
            if self.transaction_type == "خروج" and hasattr(self, 'receiver_edit'):
                receiver_name = self.receiver_edit.text().strip()
                # التحقق من وجود اسم المستلم في عمليات الخروج
                if not receiver_name:
                    QMessageBox.warning(
                        self, "تحذير", 
                        "يجب إدخال اسم المستلم في عمليات الخروج."
                    )
                    return
            
            # حفظ الحركة
            success = excel_manager.add_transaction(
                self.project_name,
                self.item_info,
                self.transaction_type,
                quantity,
                receiver_name,
                notes
            )
            
            if success:
                operation = "إدخال" if self.transaction_type == "دخول" else "إخراج"
                QMessageBox.information(
                    self, "نجح", 
                    f"تم {operation} {quantity} من {self.item_info['اسم العنصر']} بنجاح"
                )
                self.accept()
            else:
                QMessageBox.critical(self, "خطأ", "فشل في حفظ الحركة")
                
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في حفظ الحركة: {str(e)}")
    
    def show_items_manager(self):
        """إظهار مدير العناصر"""
        from items_manager import ItemsManager
        manager = ItemsManager(self)
        if manager.exec():
            # تحديث معلومات العنصر إذا تم تعديلها
            self.load_item_info()