# -*- coding: utf-8 -*-
"""
واجهة إنشاء عنصر جديد
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QTableWidget, QTableWidgetItem,
                           QHeaderView, QMessageBox, QLineEdit, QFormLayout,
                           QFrame, QTextEdit, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from excel_manager import excel_manager
import pandas as pd


class ItemsManager(QDialog):
    """واجهة إنشاء عنصر جديد"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.items_data = pd.DataFrame()
        self.setup_ui()
        self.setup_styles()
        self.load_items_data()
    
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        self.setWindowTitle("إنشاء عنصر جديد")
        self.setModal(True)
        self.setFixedSize(1500, 1000)  # عرض 1000، ارتفاع 700
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        # التخطيط الرئيسي
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # العنوان
        title_label = QLabel("إنشاء عنصر جديد")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # قسم إضافة عنصر جديد
        add_section = self.create_add_item_section()
        main_layout.addWidget(add_section)
        
        # جدول العناصر الموجودة
        table_label = QLabel("العناصر الموجودة:")
        table_label.setObjectName("section_title")
        main_layout.addWidget(table_label)
        
        self.create_items_table()
        main_layout.addWidget(self.items_table)
        
        # الأزرار
        buttons_layout = self.create_buttons_section()
        main_layout.addLayout(buttons_layout)
    
    def create_add_item_section(self):
        """إنشاء قسم إضافة عنصر جديد"""
        frame = QFrame()
        frame.setObjectName("add_frame")
        frame.setFrameStyle(QFrame.Shape.Box)
        
        layout = QFormLayout(frame)
        layout.setSpacing(10)
        
        # عنوان القسم
        section_title = QLabel("إضافة عنصر جديد:")
        section_title.setObjectName("section_title")
        layout.addRow(section_title)
        
        # اسم العنصر
        self.item_name_edit = QLineEdit()
        self.item_name_edit.setPlaceholderText("أدخل اسم العنصر")
        self.item_name_edit.setObjectName("input_field")
        layout.addRow("اسم العنصر:", self.item_name_edit)
        
        # التصنيف - ComboBox يسمح بإدخال نصوص جديدة
        self.category_combo = QComboBox()
        self.category_combo.setObjectName("category_combo")
        self.category_combo.setEditable(True)  # السماح بإدخال نصوص جديدة
        self.category_combo.lineEdit().setPlaceholderText("اختر أو اكتب تصنيف جديد")
        
        # تحميل التصنيفات الموجودة
        self.load_categories()
        
        layout.addRow("التصنيف:", self.category_combo)
        
        # مدة الصلاحية
        self.shelf_life_input = QLineEdit()
        self.shelf_life_input.setPlaceholderText("عدد أيام الصلاحية (أتركه فارغاً إذا كان غير محدد)")
        self.shelf_life_input.setObjectName("input_field")
        layout.addRow("مدة الصلاحية:", self.shelf_life_input)
        
        # الوصف
        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("وصف العنصر (اختياري)")
        self.description_edit.setObjectName("text_area")
        self.description_edit.setMaximumHeight(80)
        layout.addRow("الوصف:", self.description_edit)
        
        # زر الإضافة
        add_btn = QPushButton("إضافة العنصر")
        add_btn.setObjectName("add_button")
        add_btn.clicked.connect(self.add_new_item)
        layout.addRow("", add_btn)
        
        return frame
    
    def create_items_table(self):
        """إنشاء جدول العناصر"""
        self.items_table = QTableWidget()
        self.items_table.setObjectName("items_table")
        
        # تعيين الأعمدة
        columns = [
            "ID",
            "اسم العنصر",
            "التصنيف",
            "مدة الصلاحية (أيام)",
            "الوصف"
        ]
        
        self.items_table.setColumnCount(len(columns))
        self.items_table.setHorizontalHeaderLabels(columns)
        
        # تنسيق الجدول
        header = self.items_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)  # ID عرض ثابت
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # اسم العنصر
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # التصنيف
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # مدة الصلاحية
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)  # الوصف
        
        # عرض عمود ID
        self.items_table.setColumnWidth(0, 60)
        
        # تفعيل الترتيب
        self.items_table.setSortingEnabled(True)
        
        # تنسيق الصفوف
        self.items_table.setAlternatingRowColors(True)
        self.items_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        # منع التعديل
        self.items_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    
    def create_buttons_section(self):
        """إنشاء قسم الأزرار"""
        layout = QHBoxLayout()
        
        # زر تحديث
        refresh_btn = QPushButton("تحديث القائمة")
        refresh_btn.setObjectName("refresh_button")
        refresh_btn.clicked.connect(self.load_items_data)
        layout.addWidget(refresh_btn)
        
        # زر حذف
        delete_btn = QPushButton("حذف العنصر المحدد")
        delete_btn.setObjectName("delete_button")
        delete_btn.clicked.connect(self.delete_selected_item)
        layout.addWidget(delete_btn)
        
        # مساحة مرنة
        layout.addStretch()
        
        # زر إغلاق
        close_btn = QPushButton("إغلاق")
        close_btn.setObjectName("close_button")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        return layout
    
    def setup_styles(self):
        """إعداد التنسيقات"""
        style = """
        QDialog {
            background-color: #ecf0f1;
        }
        
        QLabel#title {
            font-size: 22px;
            font-weight: bold;
            color: #2c3e50;
            padding: 15px;
        }
        
        QLabel#section_title {
            font-size: 16px;
            font-weight: bold;
            color: #34495e;
            padding: 10px 0px;
        }
        
        QFrame#add_frame {
            background-color: white;
            border: 2px solid #bdc3c7;
            border-radius: 10px;
            padding: 20px;
        }
        
        QLineEdit#input_field {
            font-size: 13px;
            padding: 8px;
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
        
        QSpinBox#spin_field {
            font-size: 13px;
            padding: 8px;
            border: 2px solid #bdc3c7;
            border-radius: 5px;
            background-color: white;
            color: #2c3e50;
            min-height: 20px;
        }
        
        QComboBox#category_combo {
            font-size: 13px;
            padding: 8px;
            border: 2px solid #bdc3c7;
            border-radius: 5px;
            background-color: white;
            color: #2c3e50;
            min-height: 20px;
        }
        
        QComboBox#category_combo:focus {
            border-color: #3498db;
            background-color: #ffffff;
        }
        
        QComboBox#category_combo::drop-down {
            border: none;
            background-color: #ecf0f1;
        }
        
        QComboBox#category_combo::down-arrow {
            image: none;
        }
        
        QComboBox#category_combo QAbstractItemView {
            border: 2px solid #bdc3c7;
            background-color: white;
            color: #2c3e50;
            selection-background-color: #3498db;
            selection-color: white;
            padding: 5px;
        }
        
        QSpinBox#spin_field:focus {
            border-color: #3498db;
            background-color: #ffffff;
            color: #2c3e50;
        }
        
        QTextEdit#text_area {
            font-size: 12px;
            border: 2px solid #bdc3c7;
            border-radius: 5px;
            background-color: white;
            color: #2c3e50;
        }
        
        QTextEdit#text_area:focus {
            border-color: #3498db;
            background-color: #ffffff;
            color: #2c3e50;
        }
        
        QTableWidget#items_table {
            background-color: white;
            border: 2px solid #bdc3c7;
            border-radius: 10px;
            gridline-color: #ecf0f1;
            font-size: 12px;
        }
        
        QTableWidget#items_table::item {
            padding: 8px;
            border-bottom: 1px solid #ecf0f1;
            color: #2c3e50;
            background-color: white;
        }
        
        QTableWidget#items_table::item:alternate {
            background-color: #f8f9fa;
            color: #2c3e50;
        }
        
        QTableWidget#items_table::item:selected {
            background-color: #3498db;
            color: white;
        }
        
        QHeaderView::section {
            background-color: #34495e;
            color: white;
            font-weight: bold;
            font-size: 13px;
            padding: 10px;
            border: none;
        }
        
        QPushButton#add_button {
            background-color: #27ae60;
            color: white;
            font-size: 14px;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            padding: 12px 20px;
            min-height: 25px;
        }
        
        QPushButton#add_button:hover {
            background-color: #2ecc71;
        }
        
        QPushButton#refresh_button {
            background-color: #3498db;
            color: white;
            font-size: 14px;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            padding: 12px 20px;
        }
        
        QPushButton#refresh_button:hover {
            background-color: #2980b9;
        }
        
        QPushButton#delete_button {
            background-color: #e74c3c;
            color: white;
            font-size: 14px;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            padding: 12px 20px;
        }
        
        QPushButton#delete_button:hover {
            background-color: #c0392b;
        }
        
        QPushButton#close_button {
            background-color: #95a5a6;
            color: white;
            font-size: 14px;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            padding: 12px 20px;
        }
        
        QPushButton#close_button:hover {
            background-color: #7f8c8d;
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
            background-color: #9b59b6;
            color: white;
            font-size: 10px;
            font-weight: bold;
            border: none;
            border-radius: 5px;
            padding: 6px 12px;
            min-width: 70px;
        }
        QMessageBox QPushButton:hover {
            background-color: #8e44ad;
        }
        QMessageBox QPushButton:pressed {
            background-color: #7d3c98;
        }
        """
        QApplication.instance().setStyleSheet(QApplication.instance().styleSheet() + message_style)
    
    def load_categories(self):
        """تحميل التصنيفات الموجودة في ComboBox"""
        try:
            df = pd.read_excel(excel_manager.master_items_file, engine='openpyxl')
            
            if not df.empty and 'التصنيف' in df.columns:
                # الحصول على التصنيفات الفريدة
                categories = df['التصنيف'].unique()
                categories = [cat for cat in categories if pd.notna(cat)]
                categories = sorted(categories)
                
                # إضافة التصنيفات إلى ComboBox
                self.category_combo.addItems(categories)
                
        except Exception as e:
            print(f"تحذير: خطأ في تحميل التصنيفات: {str(e)}")
    
    def load_items_data(self):
        """تحميل بيانات العناصر"""
        try:
            df = pd.read_excel(excel_manager.master_items_file, engine='openpyxl')
            self.items_data = df
            self.display_items_data()
            
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في تحميل بيانات العناصر: {str(e)}")
    
    def display_items_data(self):
        """عرض بيانات العناصر في الجدول"""
        self.items_table.setRowCount(len(self.items_data))
        
        for row, (_, item) in enumerate(self.items_data.iterrows()):
            # ID
            self.items_table.setItem(row, 0, QTableWidgetItem(str(item['Item_ID'])))
            
            # اسم العنصر
            self.items_table.setItem(row, 1, QTableWidgetItem(str(item['اسم_العنصر'])))
            
            # التصنيف
            self.items_table.setItem(row, 2, QTableWidgetItem(str(item['التصنيف'])))
            
            # مدة الصلاحية
            shelf_life = item['مدة_الصلاحية_بالأيام']
            if pd.notna(shelf_life) and shelf_life > 0:
                self.items_table.setItem(row, 3, QTableWidgetItem(f"{int(shelf_life)} يوم"))
            else:
                self.items_table.setItem(row, 3, QTableWidgetItem("غير محدد"))
            
            # الوصف
            description = item['وصف'] if pd.notna(item['وصف']) else ""
            self.items_table.setItem(row, 4, QTableWidgetItem(str(description)))
    
    def validate_new_item_inputs(self):
        """التحقق من صحة بيانات العنصر الجديد"""
        # التحقق من اسم العنصر
        item_name = self.item_name_edit.text().strip()
        if not item_name:
            QMessageBox.warning(self, "خطأ", "يرجى إدخال اسم العنصر")
            return False
        
        # التحقق من عدم تكرار الاسم
        if not self.items_data.empty:
            existing_names = self.items_data['اسم_العنصر'].str.lower()
            if item_name.lower() in existing_names.values:
                QMessageBox.warning(self, "خطأ", "يوجد عنصر بهذا الاسم مسبقاً")
                return False
        
        # التحقق من التصنيف
        category = self.category_combo.currentText().strip()
        if not category:
            QMessageBox.warning(self, "خطأ", "يرجى اختيار أو إدخال التصنيف")
            return False
        
        return True
    
    def add_new_item(self):
        """إضافة عنصر جديد"""
        if not self.validate_new_item_inputs():
            return
        
        try:
            # جمع البيانات
            item_name = self.item_name_edit.text().strip()
            category = self.category_combo.currentText().strip()
            
            # معالجة مدة الصلاحية - يمكن أن تكون فارغة أو رقم
            shelf_life_text = self.shelf_life_input.text().strip()
            shelf_life = None
            if shelf_life_text:
                try:
                    shelf_life = int(shelf_life_text)
                except ValueError:
                    QMessageBox.warning(self, "تنبيه", "مدة الصلاحية يجب أن تكون رقماً صحيحاً")
                    return
            
            description = self.description_edit.toPlainText().strip()
            
            # إضافة العنصر
            new_id = excel_manager.add_new_item(item_name, category, shelf_life, description)
            
            if new_id:
                QMessageBox.information(
                    self, "نجح", 
                    f"تم إضافة العنصر '{item_name}' بنجاح\nرقم العنصر: {new_id}"
                )
                
                # مسح الحقول
                self.clear_input_fields()
                
                # تحديث الجدول
                self.load_items_data()
            else:
                QMessageBox.critical(self, "خطأ", "فشل في إضافة العنصر")
                
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في إضافة العنصر: {str(e)}")
    
    def clear_input_fields(self):
        """مسح حقول الإدخال"""
        self.item_name_edit.clear()
        self.category_combo.setCurrentIndex(0)  # إعادة تعيين إلى أول خيار
        self.category_combo.lineEdit().clear()  # مسح النص المدخل يدوياً
        self.shelf_life_input.clear()
        self.description_edit.clear()
    
    def delete_selected_item(self):
        """حذف العنصر المحدد"""
        current_row = self.items_table.currentRow()
        
        if current_row < 0:
            QMessageBox.warning(self, "تنبيه", "يرجى تحديد عنصر للحذف")
            return
        
        # الحصول على معلومات العنصر المحدد
        item_id = int(self.items_table.item(current_row, 0).text())
        item_name = self.items_table.item(current_row, 1).text()
        
        # تأكيد الحذف
        reply = QMessageBox.question(
            self, "تأكيد الحذف",
            f"هل تريد حذف العنصر '{item_name}' (ID: {item_id})؟\n\n"
            "تحذير: سيؤثر هذا على جميع الحركات المرتبطة بهذا العنصر",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                # حذف من ملف Excel
                df = pd.read_excel(excel_manager.master_items_file, engine='openpyxl')
                df = df[df['Item_ID'] != item_id]
                df.to_excel(excel_manager.master_items_file, index=False, engine='openpyxl')
                
                QMessageBox.information(self, "نجح", f"تم حذف العنصر '{item_name}' بنجاح")
                
                # تحديث الجدول
                self.load_items_data()
                
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"خطأ في حذف العنصر: {str(e)}")