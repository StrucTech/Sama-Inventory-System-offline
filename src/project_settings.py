# -*- coding: utf-8 -*-
"""
نافذة إعدادات المشروع
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QSpinBox, QFrame, QFormLayout,
                           QMessageBox)
from PyQt6.QtCore import Qt
from excel_manager import excel_manager
import json
import os


class ProjectSettingsDialog(QDialog):
    """نافذة إعدادات المشروع"""
    
    def __init__(self, project_name, parent=None):
        super().__init__(parent)
        self.project_name = project_name
        self.settings_file = f"projects/{project_name}_settings.json"
        self.current_settings = self.load_settings()
        self.setup_ui()
        self.setup_styles()
    
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        self.setWindowTitle(f"إعدادات المشروع - {self.project_name}")
        self.setModal(True)
        self.resize(500, 300)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        # التخطيط الرئيسي
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # العنوان
        title_label = QLabel("إعدادات المشروع")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # إطار الإعدادات
        settings_frame = QFrame()
        settings_frame.setObjectName("settings_frame")
        settings_frame.setFrameStyle(QFrame.Shape.Box)
        settings_layout = QFormLayout(settings_frame)
        settings_layout.setSpacing(20)
        
        # عتبة المخزون المنخفض
        low_stock_label = QLabel("عتبة المخزون المنخفض:")
        self.low_stock_spinbox = QSpinBox()
        self.low_stock_spinbox.setObjectName("input_field")
        self.low_stock_spinbox.setMinimum(1)
        self.low_stock_spinbox.setMaximum(10000)
        self.low_stock_spinbox.setValue(self.current_settings.get('low_stock_threshold', 10))
        self.low_stock_spinbox.setSuffix(" وحدة")
        low_stock_desc = QLabel("الكمية التي يظهر عندها تنبيه المخزون المنخفض")
        low_stock_desc.setObjectName("description")
        
        settings_layout.addRow(low_stock_label, self.low_stock_spinbox)
        settings_layout.addRow("", low_stock_desc)
        
        # عتبة انتهاء الصلاحية
        expire_label = QLabel("عتبة انتهاء الصلاحية:")
        self.expire_spinbox = QSpinBox()
        self.expire_spinbox.setObjectName("input_field")
        self.expire_spinbox.setMinimum(1)
        self.expire_spinbox.setMaximum(365)
        self.expire_spinbox.setValue(self.current_settings.get('expiry_threshold_days', 30))
        self.expire_spinbox.setSuffix(" يوم")
        expire_desc = QLabel("عدد الأيام المتبقية التي يظهر عندها تنبيه انتهاء الصلاحية")
        expire_desc.setObjectName("description")
        
        settings_layout.addRow(expire_label, self.expire_spinbox)
        settings_layout.addRow("", expire_desc)
        
        main_layout.addWidget(settings_frame)
        
        # الأزرار
        buttons_layout = QHBoxLayout()
        
        # زر الحفظ
        save_btn = QPushButton("حفظ الإعدادات")
        save_btn.setObjectName("save_button")
        save_btn.clicked.connect(self.save_settings)
        buttons_layout.addWidget(save_btn)
        
        # زر الإلغاء
        cancel_btn = QPushButton("إلغاء")
        cancel_btn.setObjectName("cancel_button")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        main_layout.addLayout(buttons_layout)
    
    def setup_styles(self):
        """إعداد التنسيقات"""
        style = """
        QDialog {
            background-color: #ecf0f1;
        }
        
        QLabel#title {
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
            padding: 10px;
        }
        
        QLabel#description {
            font-size: 12px;
            color: #7f8c8d;
            font-style: italic;
        }
        
        QFrame#settings_frame {
            background-color: white;
            border: 2px solid #bdc3c7;
            border-radius: 10px;
            padding: 20px;
        }
        
        QSpinBox#input_field {
            font-size: 14px;
            padding: 8px;
            border: 2px solid #bdc3c7;
            border-radius: 5px;
            background-color: white;
            color: #2c3e50;
            min-width: 100px;
        }
        
        QSpinBox#input_field:focus {
            border-color: #3498db;
            background-color: #ffffff;
        }
        
        QPushButton#save_button {
            background-color: #27ae60;
            color: white;
            font-size: 14px;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            min-height: 20px;
        }
        
        QPushButton#save_button:hover {
            background-color: #2ecc71;
        }
        
        QPushButton#cancel_button {
            background-color: #e74c3c;
            color: white;
            font-size: 14px;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            min-height: 20px;
        }
        
        QPushButton#cancel_button:hover {
            background-color: #c0392b;
        }
        
        QFormLayout {
            spacing: 15px;
        }
        """
        
        self.setStyleSheet(style)
    
    def load_settings(self):
        """تحميل إعدادات المشروع"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # الإعدادات الافتراضية
                return {
                    'low_stock_threshold': 10,
                    'expiry_threshold_days': 30
                }
        except Exception as e:
            print(f"خطأ في تحميل الإعدادات: {e}")
            return {
                'low_stock_threshold': 10,
                'expiry_threshold_days': 30
            }
    
    def save_settings(self):
        """حفظ إعدادات المشروع"""
        try:
            settings = {
                'low_stock_threshold': self.low_stock_spinbox.value(),
                'expiry_threshold_days': self.expire_spinbox.value()
            }
            
            # إنشاء المجلد إذا لم يكن موجوداً
            os.makedirs('projects', exist_ok=True)
            
            # حفظ الإعدادات
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=4)
            
            QMessageBox.information(
                self, "نجح", 
                "تم حفظ إعدادات المشروع بنجاح"
            )
            self.accept()
        except Exception as e:
            QMessageBox.critical(
                self, "خطأ", 
                f"خطأ في حفظ الإعدادات: {str(e)}"
            )
    
    @staticmethod
    def get_project_settings(project_name):
        """الحصول على إعدادات المشروع بدون فتح النافذة"""
        settings_file = f"projects/{project_name}_settings.json"
        try:
            if os.path.exists(settings_file):
                with open(settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {
                    'low_stock_threshold': 10,
                    'expiry_threshold_days': 30
                }
        except Exception as e:
            print(f"خطأ في تحميل إعدادات المشروع: {e}")
            return {
                'low_stock_threshold': 10,
                'expiry_threshold_days': 30
            }
