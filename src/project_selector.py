# -*- coding: utf-8 -*-
"""
واجهة اختيار المشروع لنظام إدارة المخزن
"""

import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QPushButton, QComboBox, 
                           QLineEdit, QMessageBox, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QColor
from excel_manager import excel_manager


class ProjectSelector(QMainWindow):
    """واجهة اختيار المشروع"""
    
    project_selected = pyqtSignal(str)  # إشارة عند اختيار مشروع
    
    def __init__(self):
        super().__init__()
        self.selected_project = None
        self.setup_ui()
        self.setup_styles()
        self.load_existing_projects()
    
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        self.setWindowTitle("نظام إدارة المخزن - اختيار المشروع")
        self.setFixedSize(600, 700)  # عرض 600، ارتفاع 500
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        # الودجة الرئيسية
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # التخطيط الرئيسي
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(40, 40, 40, 40)
        
        # العنوان الرئيسي
        title_label = QLabel("نظام إدارة المخزن")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # العنوان الفرعي
        subtitle_label = QLabel("اختر المشروع للمتابعة")
        subtitle_label.setObjectName("subtitle")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(subtitle_label)
        
        # إطار اختيار المشروع الموجود
        existing_frame = QFrame()
        existing_frame.setFrameStyle(QFrame.Shape.Box)
        existing_frame.setObjectName("frame")
        existing_layout = QVBoxLayout(existing_frame)
        
        existing_title = QLabel("اختيار مشروع موجود:")
        existing_title.setObjectName("section_title")
        existing_layout.addWidget(existing_title)
        
        self.project_combo = QComboBox()
        self.project_combo.setObjectName("combo")
        existing_layout.addWidget(self.project_combo)
        
        select_existing_btn = QPushButton("فتح المشروع المحدد")
        select_existing_btn.setObjectName("primary_button")
        select_existing_btn.clicked.connect(self.select_existing_project)
        existing_layout.addWidget(select_existing_btn)
        
        main_layout.addWidget(existing_frame)
        
        # فاصل
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setObjectName("separator")
        main_layout.addWidget(separator)
        
        # إطار إنشاء مشروع جديد
        new_frame = QFrame()
        new_frame.setFrameStyle(QFrame.Shape.Box)
        new_frame.setObjectName("frame")
        new_layout = QVBoxLayout(new_frame)
        
        new_title = QLabel("إنشاء مشروع جديد:")
        new_title.setObjectName("section_title")
        new_layout.addWidget(new_title)
        
        self.new_project_edit = QLineEdit()
        self.new_project_edit.setPlaceholderText("أدخل اسم المشروع الجديد")
        self.new_project_edit.setObjectName("text_input")
        new_layout.addWidget(self.new_project_edit)
        
        create_new_btn = QPushButton("إنشاء مشروع جديد")
        create_new_btn.setObjectName("secondary_button")
        create_new_btn.clicked.connect(self.create_new_project)
        new_layout.addWidget(create_new_btn)
        
        main_layout.addWidget(new_frame)
        
        # مساحة مرنة
        main_layout.addStretch()
        
        # زر الخروج
        exit_btn = QPushButton("خروج")
        exit_btn.setObjectName("exit_button")
        exit_btn.clicked.connect(self.close)
        main_layout.addWidget(exit_btn)
        
        # إضافة اختصار Escape للخروج من Full Screen
        self.setStyleSheet(self.styleSheet() + """
        QWidget {
            /* اضغط Escape للخروج من وضع ملء الشاشة */
        }
        """)
    
    def setup_styles(self):
        """إعداد التنسيقات"""
        style = """
        QMainWindow {
            background-color: #f0f0f0;
        }
        
        QLabel#title {
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            padding: 10px;
        }
        
        QLabel#subtitle {
            font-size: 16px;
            color: #7f8c8d;
            padding: 5px;
        }
        
        QLabel#section_title {
            font-size: 14px;
            font-weight: bold;
            color: #34495e;
            padding: 5px 0px;
        }
        
        QFrame#frame {
            background-color: white;
            border: 2px solid #bdc3c7;
            border-radius: 10px;
            padding: 10px;
        }
        
        QFrame#separator {
            color: #bdc3c7;
        }
        
        QPushButton#primary_button {
            background-color: #3498db;
            color: white;
            font-size: 14px;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            padding: 12px;
            min-height: 20px;
        }
        
        QPushButton#primary_button:hover {
            background-color: #2980b9;
        }
        
        QPushButton#primary_button:pressed {
            background-color: #21618c;
        }
        
        QPushButton#secondary_button {
            background-color: #2ecc71;
            color: white;
            font-size: 14px;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            padding: 12px;
            min-height: 20px;
        }
        
        QPushButton#secondary_button:hover {
            background-color: #27ae60;
        }
        
        QPushButton#secondary_button:pressed {
            background-color: #1e8449;
        }
        
        QPushButton#exit_button {
            background-color: #e74c3c;
            color: white;
            font-size: 14px;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            padding: 12px;
            min-height: 20px;
        }
        
        QPushButton#exit_button:hover {
            background-color: #c0392b;
        }
        
        QPushButton#exit_button:pressed {
            background-color: #a93226;
        }
        
        QComboBox#combo {
            font-size: 13px;
            padding: 8px;
            border: 2px solid #bdc3c7;
            border-radius: 5px;
            background-color: white;
            color: #2c3e50;
            min-height: 20px;
        }
        
        QComboBox#combo::drop-down {
            border: none;
            width: 20px;
        }
        
        QComboBox#combo::down-arrow {
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid #2c3e50;
            width: 0px;
            height: 0px;
        }
        
        QComboBox#combo QAbstractItemView {
            background-color: white;
            color: #2c3e50;
            selection-background-color: #3498db;
            selection-color: white;
            border: 1px solid #bdc3c7;
        }
        
        QComboBox#combo:focus {
            border-color: #3498db;
        }
        
        QLineEdit#text_input {
            font-size: 13px;
            padding: 10px;
            border: 2px solid #bdc3c7;
            border-radius: 5px;
            background-color: white;
            color: #2c3e50;
            min-height: 20px;
        }
        
        QLineEdit#text_input:focus {
            border-color: #3498db;
            background-color: #ffffff;
            color: #2c3e50;
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
            background-color: #27ae60;
            color: white;
            font-size: 10px;
            font-weight: bold;
            border: none;
            border-radius: 5px;
            padding: 6px 12px;
            min-width: 70px;
        }
        QMessageBox QPushButton:hover {
            background-color: #229954;
        }
        QMessageBox QPushButton:pressed {
            background-color: #1e8449;
        }
        """
        QApplication.instance().setStyleSheet(QApplication.instance().styleSheet() + message_style)
    
    def load_existing_projects(self):
        """تحميل المشاريع الموجودة"""
        try:
            projects = excel_manager.get_all_projects()
            
            self.project_combo.clear()
            if projects:
                self.project_combo.addItems(projects)
            else:
                self.project_combo.addItem("لا توجد مشاريع محفوظة")
        except Exception as e:
            QMessageBox.warning(self, "خطأ", f"خطأ في تحميل المشاريع: {str(e)}")
    
    def select_existing_project(self):
        """اختيار مشروع موجود"""
        if self.project_combo.count() == 0 or self.project_combo.currentText() == "لا توجد مشاريع محفوظة":
            QMessageBox.warning(self, "تنبيه", "لا توجد مشاريع محفوظة")
            return
        
        project_name = self.project_combo.currentText()
        if project_name:
            self.selected_project = project_name
            self.project_selected.emit(project_name)
            self.close()
    
    def create_new_project(self):
        """إنشاء مشروع جديد"""
        project_name = self.new_project_edit.text().strip()
        
        if not project_name:
            QMessageBox.warning(self, "خطأ", "يرجى إدخال اسم المشروع")
            return
        
        # التحقق من عدم وجود مشروع بنفس الاسم
        existing_projects = excel_manager.get_all_projects()
        if project_name in existing_projects:
            QMessageBox.warning(self, "خطأ", "يوجد مشروع بهذا الاسم مسبقاً")
            return
        
        try:
            # إنشاء ملف المشروع الجديد
            excel_manager.create_site_transactions_file(project_name)
            
            self.selected_project = project_name
            self.project_selected.emit(project_name)
            
            QMessageBox.information(self, "نجح", f"تم إنشاء المشروع '{project_name}' بنجاح")
            self.close()
            
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في إنشاء المشروع: {str(e)}")
    
    def get_selected_project(self):
        """الحصول على المشروع المحدد"""
        return self.selected_project


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # إنشاء ملف العناصر الأساسي إذا لم يكن موجوداً
    excel_manager.create_master_items_file()
    
    # إظهار واجهة اختيار المشروع
    project_selector = ProjectSelector()
    project_selector.show()
    
    sys.exit(app.exec())