# -*- coding: utf-8 -*-
"""
الملف الرئيسي لتشغيل نظام إدارة المخزن الأوفلاين
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QTranslator, QLocale
from PyQt6.QtGui import QFont, QFontDatabase
from datetime import datetime

# إضافة مجلد src إلى المسار
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from project_selector import ProjectSelector
from main_window import MainWindow
from excel_manager import excel_manager


class InventoryApp:
    """التطبيق الرئيسي لنظام إدارة المخزن"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.setup_app()
        self.main_window = None
        
    def setup_app(self):
        """إعداد التطبيق"""
        # إعداد معلومات التطبيق
        self.app.setApplicationName("نظام إدارة المخزن الأوفلاين")
        self.app.setApplicationVersion("1.0.0")
        self.app.setOrganizationName("StrucTech")
        
        # إعداد خط افتراضي عربي
        try:
            # محاولة استخدام خط عربي متاح
            font = QFont("Arial Unicode MS", 10)
            if not font.exactMatch():
                font = QFont("Tahoma", 10)
            if not font.exactMatch():
                font = QFont("Segoe UI", 10)
            self.app.setFont(font)
        except Exception as e:
            print(f"تحذير: لا يمكن تحميل الخط العربي: {e}")
        
        # إعداد اتجاه النص للعربية
        self.app.setLayoutDirection(self.app.layoutDirection().RightToLeft)
    
    def initialize_system(self):
        """تهيئة النظام للمرة الأولى"""
        try:
            # إنشاء المجلدات المطلوبة
            os.makedirs("data", exist_ok=True)
            os.makedirs("projects", exist_ok=True)
            os.makedirs("reports", exist_ok=True)
            
            # إنشاء ملف العناصر الأساسي
            excel_manager.create_master_items_file()
            
            return True
            
        except Exception as e:
            QMessageBox.critical(
                None, "خطأ في التهيئة", 
                f"حدث خطأ في تهيئة النظام:\n{str(e)}\n\nيرجى التأكد من الصلاحيات والمساحة المتاحة"
            )
            return False
    
    def show_project_selector(self):
        """إظهار نافذة اختيار المشروع"""
        self.project_selector = ProjectSelector()
        self.project_selector.project_selected.connect(self.open_main_window)
        self.project_selector.show()
    
    def open_main_window(self, project_name):
        """فتح النافذة الرئيسية"""
        try:
            if self.main_window:
                self.main_window.close()
            
            self.main_window = MainWindow(project_name)
            self.main_window.show()
            
        except Exception as e:
            QMessageBox.critical(
                None, "خطأ", 
                f"خطأ في فتح النافذة الرئيسية:\n{str(e)}"
            )
    
    def run(self):
        """تشغيل التطبيق"""
        try:
            # تهيئة النظام
            if not self.initialize_system():
                return 1
            
            # إظهار نافذة اختيار المشروع
            self.show_project_selector()
            
            # تشغيل التطبيق
            return self.app.exec()
            
        except Exception as e:
            QMessageBox.critical(
                None, "خطأ عام", 
                f"حدث خطأ غير متوقع:\n{str(e)}"
            )
            return 1


def main():
    """الدالة الرئيسية"""
    try:
        # إنشاء وتشغيل التطبيق
        app = InventoryApp()
        exit_code = app.run()
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        print("\nتم إيقاف التطبيق بواسطة المستخدم")
        sys.exit(0)
    except Exception as e:
        print(f"خطأ غير متوقع: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()