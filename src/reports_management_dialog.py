"""
نافذة إدارة التقارير المحدثة - نظام متكامل للتقارير
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QFrame, QGridLayout, QMessageBox,
                           QSpacerItem, QSizePolicy, QDateEdit, QFileDialog,
                           QGroupBox, QFormLayout)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QIcon
import json
import os
from datetime import datetime

class ReportsManagementDialog(QDialog):
    def __init__(self, project_name, parent=None):
        super().__init__(parent)
        self.project_name = project_name
        self.parent_window = parent
        self.settings_file = f"data/{project_name}/report_settings.json"
        self.current_step = "choose_type"
        self.report_type = None
        self.start_date = None
        self.end_date = None
        self.save_path = None
        
        # تطبيق stylesheet عام لجميع النوافذ
        self.apply_global_stylesheet()
        
        self.setup_ui()
        self.load_last_report_info()
    
    def apply_global_stylesheet(self):
        """تطبيق stylesheet عام قوي للتقويم والعناصر"""
        stylesheet = """
            QDateEdit {
                font-size: 15px !important;
                padding: 10px !important;
                border: 3px solid #3498db !important;
                border-radius: 8px !important;
                background-color: white !important;
                color: #2c3e50 !important;
                font-weight: bold !important;
            }
            
            QDateEdit:focus {
                border-color: #2980b9 !important;
                background-color: #ecf0f1 !important;
            }
            
            QCalendarWidget {
                background-color: white !important;
                color: #2c3e50 !important;
                gridline-color: #bdc3c7 !important;
                min-width: 450px !important;
                min-height: 350px !important;
            }
            
            QCalendarWidget QAbstractItemView {
                background-color: white !important;
                color: #2c3e50 !important;
                font-size: 13px !important;
                font-weight: bold !important;
                selection-background-color: #3498db !important;
                selection-color: white !important;
                border: 1px solid #bdc3c7 !important;
                padding: 8px !important;
            }
            
            QCalendarWidget QAbstractItemView:item {
                padding: 8px !important;
                color: #2c3e50 !important;
                min-width: 50px !important;
                min-height: 40px !important;
            }
            
            QCalendarWidget QAbstractItemView:item:selected {
                background-color: #3498db !important;
                color: white !important;
            }
            
            QCalendarWidget QAbstractItemView:item:hover {
                background-color: #ecf0f1 !important;
                color: #2c3e50 !important;
            }
            
            QCalendarWidget QToolButton {
                background-color: white !important;
                color: #2c3e50 !important;
                font-weight: bold !important;
                font-size: 14px !important;
                border: 2px solid #bdc3c7 !important;
                padding: 6px !important;
                min-width: 60px !important;
                min-height: 40px !important;
            }
            
            QCalendarWidget QToolButton:hover {
                background-color: #3498db !important;
                color: white !important;
            }
            
            QCalendarWidget QMenu {
                background-color: white !important;
                color: #2c3e50 !important;
                font-size: 14px !important;
                font-weight: bold !important;
            }
            
            QCalendarWidget QSpinBox {
                background-color: white !important;
                color: #2c3e50 !important;
                font-size: 13px !important;
                font-weight: bold !important;
                border: 1px solid #bdc3c7 !important;
                min-width: 80px !important;
                min-height: 35px !important;
            }
        """
        self.setStyleSheet(stylesheet)
        
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        self.setWindowTitle("إدارة التقارير")
        self.setModal(True)
        self.setMinimumSize(900, 750)
        self.resize(1000, 850)
        
        # التخطيط الرئيسي
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # العنوان الرئيسي
        self.title_label = QLabel("📊 إدارة التقارير")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                padding: 20px;
                background-color: #ecf0f1;
                border-radius: 10px;
                margin-bottom: 10px;
            }
        """)
        main_layout.addWidget(self.title_label)
        
        # معلومات المشروع
        project_info_label = QLabel(f"المشروع الحالي: {self.project_name}")
        project_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        project_info_label.setStyleSheet("""
            QLabel {
                color: #34495e;
                font-size: 14px;
                padding: 10px;
                background-color: #f8f9fa;
                border-radius: 5px;
                border: 1px solid #dee2e6;
            }
        """)
        main_layout.addWidget(project_info_label)
        
        # إطار آخر تقرير
        self.last_report_frame = QFrame()
        self.last_report_frame.setStyleSheet("""
            QFrame {
                background-color: #fff3cd;
                border-radius: 8px;
                border: 1px solid #ffeaa7;
                padding: 10px;
            }
        """)
        self.last_report_layout = QVBoxLayout(self.last_report_frame)
        self.last_report_label = QLabel("📋 آخر تقرير: لم يتم إنشاء تقرير بعد")
        self.last_report_label.setStyleSheet("color: #856404; font-weight: bold;")
        self.last_report_layout.addWidget(self.last_report_label)
        main_layout.addWidget(self.last_report_frame)
        
        # الإطار الديناميكي للمحتوى
        self.content_frame = QFrame()
        self.content_layout = QVBoxLayout(self.content_frame)
        main_layout.addWidget(self.content_frame)
        
        # أزرار التحكم
        self.control_layout = QHBoxLayout()
        
        self.back_btn = QPushButton("⬅️ رجوع")
        self.back_btn.setMinimumSize(120, 40)
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 15px;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #545b62;
            }
        """)
        self.back_btn.clicked.connect(self.go_back)
        self.back_btn.setVisible(False)
        
        self.close_btn = QPushButton("❌ إغلاق")
        self.close_btn.setMinimumSize(120, 40)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 15px;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.close_btn.clicked.connect(self.close)
        
        self.control_layout.addWidget(self.back_btn)
        self.control_layout.addStretch()
        self.control_layout.addWidget(self.close_btn)
        
        main_layout.addLayout(self.control_layout)
        
        # تطبيق الستايل العام
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
        """)
        
        # إظهار الخطوة الأولى
        self.show_report_type_selection()
    
    def show_report_type_selection(self):
        """إظهار خيارات نوع التقرير"""
        self.clear_content()
        self.title_label.setText("📊 اختر نوع التقرير")
        self.current_step = "choose_type"
        
        # إطار الأزرار
        buttons_frame = QFrame()
        buttons_frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 15px;
                border: 2px solid #e9ecef;
            }
        """)
        buttons_layout = QGridLayout(buttons_frame)
        buttons_layout.setSpacing(20)
        buttons_layout.setContentsMargins(30, 30, 30, 30)
        
        # زر التقرير الشامل
        comprehensive_btn = QPushButton("تقرير شامل ومفصل")
        comprehensive_btn.setMinimumSize(320, 110)
        comprehensive_btn.setMaximumSize(400, 140)
        comprehensive_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 20px 30px;
                border: 2px solid #1e8449;
                border-radius: 12px;
                text-align: center;
                min-height: 110px;
                min-width: 320px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
                border: 2px solid #27ae60;
            }
            QPushButton:pressed {
                background-color: #1e8449;
                border: 2px solid #145a32;
            }
        """)
        comprehensive_btn.clicked.connect(self.select_comprehensive_report)
        buttons_layout.addWidget(comprehensive_btn, 0, 0)
        
        # وصف التقرير الشامل
        comprehensive_desc = QLabel("• يحتوي على 12 ورقة عمل تفصيلية\n• تحليل شامل للمخزون والحركات\n• إحصائيات متقدمة وتنبيهات\n• جاهز للإدارة والمكتب")
        comprehensive_desc.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 12px;
                padding: 10px;
                background-color: #d5f4e6;
                border-radius: 8px;
                border-left: 4px solid #27ae60;
            }
        """)
        buttons_layout.addWidget(comprehensive_desc, 1, 0)
        
        # زر التقرير المخصص
        custom_btn = QPushButton("تقرير مخصص بالتاريخ")
        custom_btn.setMinimumSize(320, 110)
        custom_btn.setMaximumSize(400, 140)
        custom_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 20px 30px;
                border: 2px solid #2980b9;
                border-radius: 12px;
                text-align: center;
                min-height: 110px;
                min-width: 320px;
            }
            QPushButton:hover {
                background-color: #5dade2;
                border: 2px solid #3498db;
            }
            QPushButton:pressed {
                background-color: #2980b9;
                border: 2px solid #1b4f72;
            }
        """)
        custom_btn.clicked.connect(self.select_custom_report)
        buttons_layout.addWidget(custom_btn, 0, 1)
        
        # وصف التقرير المخصص
        custom_desc = QLabel("• تحديد فترة زمنية محددة\n• اختيار نوع التقرير المطلوب\n• تصفية البيانات حسب التاريخ\n• مناسب للتقارير الدورية")
        custom_desc.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 12px;
                padding: 10px;
                background-color: #d6eaf8;
                border-radius: 8px;
                border-left: 4px solid #3498db;
            }
        """)
        buttons_layout.addWidget(custom_desc, 1, 1)
        
        self.content_layout.addWidget(buttons_frame)
        self.back_btn.setVisible(False)
    
    def select_comprehensive_report(self):
        """اختيار التقرير الشامل"""
        self.report_type = "comprehensive"
        self.show_save_location_selection()
    
    def select_custom_report(self):
        """اختيار التقرير المخصص"""
        self.report_type = "custom"
        self.show_date_range_selection()
    
    def show_date_range_selection(self):
        """إظهار اختيار نطاق التواريخ"""
        self.clear_content()
        self.title_label.setText("📅 اختر نطاق التواريخ")
        self.current_step = "date_range"
        
        # إطار التواريخ
        date_frame = QFrame()
        date_frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 15px;
                border: 2px solid #e9ecef;
                padding: 20px;
            }
        """)
        date_layout = QFormLayout(date_frame)
        date_layout.setSpacing(15)
        
        # تاريخ البداية
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setDate(QDate.currentDate().addDays(-30))
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setMinimumHeight(50)
        self.start_date_edit.setMinimumWidth(250)
        date_layout.addRow("📅 من تاريخ:", self.start_date_edit)
        
        # تاريخ النهاية
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setDate(QDate.currentDate())
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setMinimumHeight(50)
        self.end_date_edit.setMinimumWidth(250)
        date_layout.addRow("📅 إلى تاريخ:", self.end_date_edit)
        
        # زر المتابعة
        continue_btn = QPushButton("متابعة")
        continue_btn.setMinimumSize(400, 50)
        continue_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 15px;
                border: none;
                border-radius: 10px;
                margin-top: 20px;
                min-width: 400px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)
        continue_btn.clicked.connect(self.proceed_with_date_range)
        date_layout.addRow("", continue_btn)
        
        self.content_layout.addWidget(date_frame)
        self.back_btn.setVisible(True)
    
    def proceed_with_date_range(self):
        """المتابعة مع نطاق التواريخ المحدد"""
        try:
            self.start_date = self.start_date_edit.date().toPyDate()
            self.end_date = self.end_date_edit.date().toPyDate()
        except AttributeError:
            # استخدام طريقة بديلة للتحويل
            from datetime import datetime
            start_qdate = self.start_date_edit.date()
            end_qdate = self.end_date_edit.date()
            self.start_date = datetime(start_qdate.year(), start_qdate.month(), start_qdate.day()).date()
            self.end_date = datetime(end_qdate.year(), end_qdate.month(), end_qdate.day()).date()
        
        if self.start_date > self.end_date:
            QMessageBox.warning(self, "خطأ", "تاريخ البداية يجب أن يكون قبل تاريخ النهاية!")
            return
        
        self.show_save_location_selection()
    
    def show_save_location_selection(self):
        """إظهار اختيار مكان الحفظ"""
        self.clear_content()
        self.title_label.setText("💾 اختر مكان حفظ التقرير")
        self.current_step = "save_location"
        
        # إطار اختيار المكان
        save_frame = QFrame()
        save_frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 15px;
                border: 2px solid #e9ecef;
                padding: 30px;
            }
        """)
        save_layout = QVBoxLayout(save_frame)
        save_layout.setSpacing(20)
        
        # رسالة توضيحية
        if self.report_type == "comprehensive":
            info_text = "سيتم إنشاء تقرير شامل يحتوي على 12 ورقة عمل تفصيلية"
        else:
            info_text = f"سيتم إنشاء تقرير مخصص للفترة من {self.start_date.strftime('%Y/%m/%d')} إلى {self.end_date.strftime('%Y/%m/%d')}"
            
        info_label = QLabel(info_text)
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 14px;
                font-weight: bold;
                padding: 15px;
                background-color: #e8f5e8;
                border-radius: 8px;
                border: 1px solid #27ae60;
            }
        """)
        save_layout.addWidget(info_label)
        
        # رسالة اختيار المجلد
        folder_label = QLabel("اختر المجلد الذي تريد حفظ التقرير فيه")
        folder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        folder_label.setStyleSheet("""
            QLabel {
                color: #34495e;
                font-size: 16px;
                padding: 10px;
            }
        """)
        save_layout.addWidget(folder_label)
        
        # زر اختيار المجلد
        choose_folder_btn = QPushButton("اختر مجلد الحفظ وإنشاء التقرير")
        choose_folder_btn.setMinimumSize(450, 70)
        choose_folder_btn.setStyleSheet("""
            QPushButton {
                background-color: #17a2b8;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 20px;
                border: none;
                border-radius: 12px;
                min-width: 450px;
                min-height: 70px;
            }
            QPushButton:hover {
                background-color: #138496;
            }
            QPushButton:pressed {
                background-color: #0c5460;
            }
        """)
        choose_folder_btn.clicked.connect(self.choose_save_location)
        save_layout.addWidget(choose_folder_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # معلومات إضافية
        additional_info = QLabel("سيتم حفظ التقرير بصيغة Excel (.xlsx) في المجلد المختار")
        additional_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        additional_info.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 12px;
                font-style: italic;
                padding: 10px;
            }
        """)
        save_layout.addWidget(additional_info)
        
        self.content_layout.addWidget(save_frame)
        self.back_btn.setVisible(True)
    
    def choose_save_location(self):
        """اختيار مكان الحفظ وتصدير التقرير"""
        folder = QFileDialog.getExistingDirectory(
            self, 
            "اختر مجلد حفظ التقرير", 
            os.path.expanduser("~/Desktop")
        )
        
        if folder:
            self.save_path = folder
            self.generate_report()
    
    def generate_report(self):
        """إنشاء التقرير"""
        try:
            if self.report_type == "comprehensive":
                self.generate_comprehensive_report()
            elif self.report_type == "custom":
                self.generate_custom_report()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في إنشاء التقرير: {str(e)}")
    
    def generate_comprehensive_report(self):
        """إنشاء التقرير الشامل"""
        try:
            if self.parent_window and hasattr(self.parent_window, 'report_manager'):
                # إنشاء اسم الملف
                filename = f"تقرير_شامل_{self.project_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                filepath = os.path.join(self.save_path, filename)
                
                # إنشاء التقرير الشامل
                filepath_result, message = self.parent_window.report_manager.export_ultra_comprehensive_report(self.project_name)
                
                if filepath_result:
                    # نسخ الملف إلى المكان المطلوب
                    import shutil
                    shutil.copy2(filepath_result, filepath)
                    
                    # حفظ معلومات آخر تقرير
                    self.save_last_report_info("شامل ومفصل", None, None, filepath)
                    
                    QMessageBox.information(
                        self, 
                        "تم بنجاح! 🎉", 
                        f"تم إنشاء التقرير الشامل بنجاح!\n\n"
                        f"📊 التقرير يحتوي على 12 ورقة عمل تفصيلية\n"
                        f"📁 موقع الملف:\n{filepath}\n\n"
                        f"سيتم فتح مجلد الحفظ الآن..."
                    )
                    
                    # فتح مجلد الحفظ
                    os.startfile(self.save_path)
                    
                    # إغلاق النافذة
                    self.close()
                else:
                    QMessageBox.warning(self, "خطأ", message or "فشل في إنشاء التقرير")
            else:
                QMessageBox.critical(self, "خطأ", "لا يمكن الوصول إلى إدارة التقارير")
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في إنشاء التقرير الشامل: {str(e)}")
    
    def generate_custom_report(self):
        """إنشاء التقرير المخصص بالتاريخ"""
        try:
            if self.parent_window and hasattr(self.parent_window, 'report_manager'):
                # إنشاء اسم الملف مع التواريخ
                filename = f"تقرير_مخصص_{self.project_name}_{self.start_date.strftime('%Y%m%d')}_الى_{self.end_date.strftime('%Y%m%d')}.xlsx"
                filepath = os.path.join(self.save_path, filename)
                
                # استدعاء دالة التقرير المخصص من report_manager
                result_filepath, message = self.parent_window.report_manager.export_filtered_report(
                    self.project_name, 
                    self.start_date, 
                    self.end_date,
                    filepath
                )
                
                if result_filepath:
                    # حفظ معلومات آخر تقرير
                    self.save_last_report_info("مخصص بالتاريخ", self.start_date, self.end_date, filepath)
                    
                    QMessageBox.information(
                        self,
                        "تم بنجاح! 🎉",
                        f"تم إنشاء التقرير المخصص بنجاح!\n\n"
                        f"📅 الفترة: من {self.start_date.strftime('%Y/%m/%d')} إلى {self.end_date.strftime('%Y/%m/%d')}\n"
                        f"📁 موقع الملف:\n{filepath}\n\n"
                        f"سيتم فتح مجلد الحفظ الآن..."
                    )
                    
                    # فتح مجلد الحفظ
                    os.startfile(self.save_path)
                    
                    # إغلاق النافذة
                    self.close()
                else:
                    QMessageBox.warning(self, "خطأ", message or "فشل في إنشاء التقرير")
            else:
                QMessageBox.critical(self, "خطأ", "لا يمكن الوصول إلى إدارة التقارير")
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في إنشاء التقرير المخصص: {str(e)}")
    
    def clear_content(self):
        """مسح المحتوى الحالي"""
        for i in reversed(range(self.content_layout.count())):
            child = self.content_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
    
    def go_back(self):
        """العودة للخطوة السابقة"""
        if self.current_step == "date_range":
            self.show_report_type_selection()
        elif self.current_step == "save_location":
            if self.report_type == "custom":
                self.show_date_range_selection()
            else:
                self.show_report_type_selection()
    
    def load_last_report_info(self):
        """تحميل معلومات آخر تقرير"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    last_report = data.get('last_report', {})
                    
                    if last_report:
                        report_type = last_report.get('type', '')
                        report_date = last_report.get('date', '')
                        start_date = last_report.get('start_date', '')
                        end_date = last_report.get('end_date', '')
                        
                        if report_type and report_date:
                            if start_date and end_date:
                                self.last_report_label.setText(
                                    f"📋 آخر تقرير: {report_type} - {report_date}\n"
                                    f"📅 الفترة: من {start_date} إلى {end_date}"
                                )
                            else:
                                self.last_report_label.setText(f"📋 آخر تقرير: {report_type} - {report_date}")
        except:
            pass
    
    def save_last_report_info(self, report_type, start_date, end_date, filepath):
        """حفظ معلومات آخر تقرير"""
        try:
            # إنشاء مجلد البيانات إذا لم يكن موجوداً
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
            
            data = {}
            if os.path.exists(self.settings_file):
                try:
                    with open(self.settings_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                except:
                    data = {}
            
            report_info = {
                'type': report_type,
                'date': datetime.now().strftime('%Y/%m/%d %H:%M'),
                'filepath': filepath
            }
            
            if start_date and end_date:
                report_info['start_date'] = start_date.strftime('%Y/%m/%d')
                report_info['end_date'] = end_date.strftime('%Y/%m/%d')
            
            data['last_report'] = report_info
            
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving last report info: {e}")