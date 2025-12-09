# -*- coding: utf-8 -*-
"""
الواجهة الرئيسية لنظام إدارة المخزن
"""

import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QPushButton, QGridLayout,
                           QFrame, QMessageBox, QStatusBar, QTableWidget, 
                           QTableWidgetItem, QHeaderView)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QIcon, QPalette, QColor
from datetime import datetime
from excel_manager import excel_manager
from report_manager import ReportManager


class MainWindow(QMainWindow):
    """الواجهة الرئيسية للنظام"""
    
    def __init__(self, project_name):
        super().__init__()
        self.project_name = project_name
        self.report_manager = ReportManager(excel_manager)
        self._changing_project = False  # متغير لتتبع حالة تغيير المشروع
        self._new_window = None  # مرجع للنافذة الجديدة
        self.setup_ui()
        self.setup_styles()
        
        # تحديث فوري للتنبيهات بعد تهيئة الواجهة
        QTimer.singleShot(100, self.update_project_info)
        
        # تحديث الوقت كل ثانية
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
    
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        self.setWindowTitle(f"نظام إدارة المخزن - {self.project_name}")
        self.showMaximized()
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        # الودجة الرئيسية
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # التخطيط الرئيسي
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # منطقة العنوان ومعلومات المشروع
        header_layout = self.create_header()
        main_layout.addLayout(header_layout)
        
        # منطقة الأزرار الرئيسية
        buttons_layout = self.create_main_buttons()
        main_layout.addLayout(buttons_layout)
        
        # مساحة مرنة
        main_layout.addStretch()
        
        # منطقة معلومات المشروع
        info_layout = self.create_project_info()
        main_layout.addLayout(info_layout)
        
        # شريط الحالة
        self.create_status_bar()
    
    def create_header(self):
        """إنشاء منطقة العنوان"""
        header_layout = QVBoxLayout()
        
        # العنوان الرئيسي
        title_label = QLabel("نظام إدارة المخزن الأوفلاين")
        title_label.setObjectName("main_title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title_label)
        
        # اسم المشروع
        project_label = QLabel(f"المشروع الحالي: {self.project_name}")
        project_label.setObjectName("project_name")
        project_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(project_label)
        
        # التاريخ والوقت
        self.datetime_label = QLabel()
        self.datetime_label.setObjectName("datetime")
        self.datetime_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.datetime_label)
        
        return header_layout
    
    def create_main_buttons(self):
        """إنشاء الأزرار الرئيسية"""
        layout = QGridLayout()
        layout.setSpacing(20)
        
        # تعريف الأزرار
        buttons_data = [
            ("إدخال عناصر للمخزن", "entry_button", self.show_entry_dialog),
            ("إخراج عناصر من المخزن", "exit_button", self.show_exit_dialog),
            ("عرض المخزون الحالي", "inventory_button", self.show_inventory),
            ("إنشاء عنصر جديد", "items_button", self.show_items_management),
            ("تعديل المعاملات الحديثة", "edit_recent_button", self.show_edit_recent_transactions),
            ("تصدير تقرير للمكتب", "excel_button", self.show_report_dialog),
            ("تغيير المشروع", "project_button", self.change_project)
        ]
        
        # إضافة الأزرار في شبكة 2×4
        for i, (text, object_name, callback) in enumerate(buttons_data):
            row = i // 2
            col = i % 2
            
            button = QPushButton(text)
            button.setObjectName(object_name)
            button.clicked.connect(callback)
            button.setMinimumHeight(80)
            button.setMinimumWidth(300)
            
            layout.addWidget(button, row, col)
        
        return layout
    
    def create_project_info(self):
        """إنشاء منطقة أزرار التنبيهات"""
        layout = QVBoxLayout()
        
        # إطار التنبيهات
        alerts_frame = QFrame()
        alerts_frame.setObjectName("alerts_frame")
        alerts_frame.setFrameStyle(QFrame.Shape.Box)
        
        alerts_layout = QVBoxLayout(alerts_frame)
        
        alerts_title = QLabel("تنبيهات المخزن")
        alerts_title.setObjectName("alerts_title")
        alerts_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        alerts_layout.addWidget(alerts_title)
        
        # تخطيط أفقي للأزرار
        buttons_layout = QHBoxLayout()
        
        # زر المخزون المنخفض
        self.low_stock_btn = QPushButton("📊 المخزون المنخفض")
        self.low_stock_btn.setObjectName("low_stock_alert_btn")
        self.low_stock_btn.setMinimumHeight(80)
        self.low_stock_btn.setMinimumWidth(200)
        self.low_stock_btn.clicked.connect(self.show_low_stock_alerts)
        buttons_layout.addWidget(self.low_stock_btn)
        
        # زر انتهاء الصلاحية
        self.expiry_alerts_btn = QPushButton("⏰ انتهاء الصلاحية")
        self.expiry_alerts_btn.setObjectName("expiry_alert_btn")
        self.expiry_alerts_btn.setMinimumHeight(80)
        self.expiry_alerts_btn.setMinimumWidth(200)
        self.expiry_alerts_btn.clicked.connect(self.show_expiry_alerts)
        buttons_layout.addWidget(self.expiry_alerts_btn)
        
        # معلومات سريعة عن التنبيهات
        info_layout = QHBoxLayout()
        
        self.low_stock_info = QLabel("🔄 جاري التحميل...")
        self.low_stock_info.setObjectName("alert_info")
        self.low_stock_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(self.low_stock_info)
        
        self.expiry_info = QLabel("🔄 جاري التحميل...")
        self.expiry_info.setObjectName("alert_info")
        self.expiry_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(self.expiry_info)
        
        # إضافة العناصر للتخطيط
        alerts_layout.addLayout(buttons_layout)
        alerts_layout.addLayout(info_layout)
        
        layout.addWidget(alerts_frame)
        return layout
    
    def create_status_bar(self):
        """إنشاء شريط الحالة"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("جاهز")
    
    def setup_styles(self):
        """إعداد التنسيقات"""
        style = """
        QMainWindow {
            background-color: #ecf0f1;
        }
        
        QLabel#main_title {
            font-size: 28px;
            font-weight: bold;
            color: #2c3e50;
            padding: 15px;
        }
        
        QLabel#project_name {
            font-size: 20px;
            font-weight: bold;
            color: #3498db;
            padding: 10px;
        }
        
        QLabel#datetime {
            font-size: 14px;
            color: #7f8c8d;
            padding: 5px;
        }
        
        QPushButton#entry_button {
            background-color: #27ae60;
            color: white;
            font-size: 16px;
            font-weight: bold;
            border: none;
            border-radius: 10px;
            padding: 15px;
        }
        
        QPushButton#entry_button:hover {
            background-color: #2ecc71;
        }
        
        QPushButton#exit_button {
            background-color: #e74c3c;
            color: white;
            font-size: 16px;
            font-weight: bold;
            border: none;
            border-radius: 10px;
            padding: 15px;
        }
        
        QPushButton#exit_button:hover {
            background-color: #c0392b;
        }
        
        QPushButton#inventory_button {
            background-color: #3498db;
            color: white;
            font-size: 16px;
            font-weight: bold;
            border: none;
            border-radius: 10px;
            padding: 15px;
        }
        
        QPushButton#inventory_button:hover {
            background-color: #2980b9;
        }
        
        QPushButton#items_button {
            background-color: #9b59b6;
            color: white;
            font-size: 16px;
            font-weight: bold;
            border: none;
            border-radius: 10px;
            padding: 15px;
        }
        
        QPushButton#items_button:hover {
            background-color: #8e44ad;
        }
        
        QPushButton#edit_recent_button {
            background-color: #17a2b8;
            color: white;
            font-size: 16px;
            font-weight: bold;
            border: none;
            border-radius: 10px;
            padding: 15px;
        }
        
        QPushButton#edit_recent_button:hover {
            background-color: #138496;
        }
        
        QPushButton#excel_button {
            background-color: #f39c12;
            color: white;
            font-size: 16px;
            font-weight: bold;
            border: none;
            border-radius: 10px;
            padding: 15px;
        }
        
        QPushButton#excel_button:hover {
            background-color: #e67e22;
        }
        
        QPushButton#project_button {
            background-color: #95a5a6;
            color: white;
            font-size: 16px;
            font-weight: bold;
            border: none;
            border-radius: 10px;
            padding: 15px;
        }
        
        QPushButton#project_button:hover {
            background-color: #7f8c8d;
        }
        
        QPushButton#low_stock_alert_btn {
            background-color: #e74c3c;
            color: white;
            font-size: 14px;
            font-weight: bold;
            border: none;
            border-radius: 10px;
            padding: 15px;
        }
        
        QPushButton#low_stock_alert_btn:hover {
            background-color: #c0392b;
        }
        
        QPushButton#expiry_alert_btn {
            background-color: #f39c12;
            color: white;
            font-size: 14px;
            font-weight: bold;
            border: none;
            border-radius: 10px;
            padding: 15px;
        }
        
        QPushButton#expiry_alert_btn:hover {
            background-color: #e67e22;
        }
        
        QFrame#alerts_frame {
            background-color: white;
            border: 2px solid #3498db;
            border-radius: 10px;
            padding: 15px;
        }
        
        QLabel#alerts_title {
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
            padding: 10px;
            background-color: #ecf0f1;
            border-radius: 5px;
        }
        
        QLabel#alert_info {
            font-size: 12px;
            color: #7f8c8d;
            padding: 5px;
            margin: 5px;
            background-color: #f8f9fa;
            border-radius: 3px;
            border: 1px solid #dee2e6;
        }
        
        QTableWidget#alert_table {
            background-color: white;
            border: 1px solid #bdc3c7;
            border-radius: 5px;
            gridline-color: #ecf0f1;
            font-size: 13px;
            font-weight: bold;
            selection-background-color: #3498db;
            selection-color: white;
        }
        
        QTableWidget#alert_table::item {
            padding: 8px;
            border-bottom: 1px solid #ecf0f1;
        }
        
        QTableWidget#alert_table::item:selected {
            background-color: #3498db;
            color: white;
        }
        
        QTableWidget#alert_table QHeaderView::section {
            background-color: #34495e;
            color: white;
            padding: 10px;
            font-size: 12px;
            font-weight: bold;
            border: none;
        }
        
        QTableWidget#alert_table QHeaderView::section:horizontal {
            border-right: 1px solid #2c3e50;
        }
        
        QTableWidget#alert_table::item {
            padding: 8px;
            border-bottom: 1px solid #ecf0f1;
        }
        
        QTableWidget#alert_table QHeaderView::section {
            background-color: #34495e;
            color: white;
            padding: 10px;
            border: none;
            font-weight: bold;
        }
        
        QLabel#info_item {
            font-size: 14px;
            color: #34495e;
            padding: 5px;
        }
        
        QStatusBar {
            background-color: #34495e;
            color: white;
            font-size: 12px;
        }
        
        QLineEdit {
            font-size: 13px;
            padding: 8px;
            border: 2px solid #bdc3c7;
            border-radius: 5px;
            background-color: white;
            color: #2c3e50;
        }
        
        QLineEdit:focus {
            border-color: #3498db;
            background-color: #ffffff;
            color: #2c3e50;
        }
        """
        
        self.setStyleSheet(style)
        self.setup_message_box_style()
    
    def update_time(self):
        """تحديث الوقت والتاريخ"""
        now = datetime.now()
        datetime_str = now.strftime("%A, %d %B %Y - %H:%M:%S")
        
        # ترجمة أيام الأسبوع للعربية
        day_translation = {
            'Monday': 'الاثنين',
            'Tuesday': 'الثلاثاء', 
            'Wednesday': 'الأربعاء',
            'Thursday': 'الخميس',
            'Friday': 'الجمعة',
            'Saturday': 'السبت',
            'Sunday': 'الأحد'
        }
        
        # ترجمة الشهور للعربية
        month_translation = {
            'January': 'يناير', 'February': 'فبراير', 'March': 'مارس',
            'April': 'أبريل', 'May': 'مايو', 'June': 'يونيو',
            'July': 'يوليو', 'August': 'أغسطس', 'September': 'سبتمبر',
            'October': 'أكتوبر', 'November': 'نوفمبر', 'December': 'ديسمبر'
        }
        
        for en, ar in day_translation.items():
            datetime_str = datetime_str.replace(en, ar)
        
        for en, ar in month_translation.items():
            datetime_str = datetime_str.replace(en, ar)
        
        self.datetime_label.setText(datetime_str)
    
    def update_project_info(self):
        """تحديث معلومات التنبيهات"""
        try:
            # تحديث معلومات التنبيهات فقط (بدون إنشاء بيانات تجريبية تلقائية)
            self.update_alerts_info()
        except Exception as e:
            print(f"خطأ في تحديث التنبيهات: {e}")
    
    def update_alerts_info(self):
        """تحديث معلومات التنبيهات في الأزرار"""
        try:
            from excel_manager import excel_manager
            import pandas as pd
            import os
            from datetime import datetime, timedelta
            
            # حساب عدد المواد ذات المخزون المنخفض
            low_stock_count = 0
            try:
                inventory_df = excel_manager.get_inventory_summary(self.project_name)
                if not inventory_df.empty:
                    for _, item in inventory_df.iterrows():
                        current_qty = item.get('الكمية_الحالية', 0)
                        if current_qty <= 10 and current_qty > 0:
                            low_stock_count += 1
            except:
                pass
            
            # حساب عدد المواد قاربة انتهاء الصلاحية
            expiry_count = 0
            try:
                project_file = os.path.join("projects", f"{self.project_name}_Transactions.xlsx")
                if os.path.exists(project_file):
                    transactions_df = pd.read_excel(project_file, engine='openpyxl')
                    if not transactions_df.empty:
                        incoming_transactions = transactions_df[transactions_df['نوع_العملية'] == 'دخول'].copy()
                        if not incoming_transactions.empty:
                            incoming_transactions['التاريخ'] = pd.to_datetime(incoming_transactions['التاريخ'])
                            for _, transaction in incoming_transactions.iterrows():
                                shelf_life_days = transaction.get('مدة_الصلاحية_بالأيام')
                                if pd.notna(shelf_life_days) and shelf_life_days > 0:
                                    entry_date = transaction['التاريخ']
                                    expiry_date = entry_date + timedelta(days=int(shelf_life_days))
                                    days_remaining = (expiry_date - datetime.now()).days
                                    if days_remaining <= 10 and days_remaining >= 0:
                                        expiry_count += 1
            except:
                pass
            
            # تحديث نص المعلومات
            if low_stock_count > 0:
                self.low_stock_info.setText(f"⚠️ {low_stock_count} مادة بمخزون منخفض")
                self.low_stock_info.setStyleSheet("color: #e74c3c; font-weight: bold;")
            else:
                self.low_stock_info.setText("✅ المخزون مناسب")
                self.low_stock_info.setStyleSheet("color: #27ae60; font-weight: bold;")
            
            if expiry_count > 0:
                self.expiry_info.setText(f"⏰ {expiry_count} مادة قاربة الانتهاء")
                self.expiry_info.setStyleSheet("color: #f39c12; font-weight: bold;")
            else:
                self.expiry_info.setText("✅ جميع المواد صالحة")
                self.expiry_info.setStyleSheet("color: #27ae60; font-weight: bold;")
                
        except Exception as e:
            print(f"خطأ في تحديث معلومات التنبيهات: {e}")
    
    def show_low_stock_alerts(self):
        """عرض نافذة المخزون المنخفض"""
        try:
            from low_stock_dialog import LowStockDialog
            dialog = LowStockDialog(self.project_name, self)
            dialog.exec()
        except ImportError:
            # إنشاء النافذة مباشرة إذا لم يكن الملف موجود
            self.create_low_stock_window()
    
    def show_expiry_alerts(self):
        """عرض نافذة انتهاء الصلاحية"""
        try:
            from expiry_alerts_dialog import ExpiryAlertsDialog
            dialog = ExpiryAlertsDialog(self.project_name, self)
            dialog.exec()
        except ImportError:
            # إنشاء النافذة مباشرة إذا لم يكن الملف موجود
            self.create_expiry_window()
    def create_low_stock_window(self):
        """إنشاء نافذة المخزون المنخفض مباشرة"""
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton
        from PyQt6.QtGui import QColor

        dialog = QDialog(self)
        dialog.setWindowTitle(f"تنبيهات المخزون المنخفض - {self.project_name}")
        dialog.setModal(True)
        dialog.resize(800, 600)

        layout = QVBoxLayout(dialog)

        # العنوان
        title = QLabel("📊 تنبيهات المخزون المنخفض")
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px; text-align: center;")
        layout.addWidget(title)

        # الجدول
        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["اسم المادة", "الكمية الحالية", "الحد الأدنى"])

        # ----- تحسينات الشكل -----
        table.setSortingEnabled(True)
        table.setAlternatingRowColors(True)
        table.setShowGrid(True)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setStretchLastSection(True)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        table.setStyleSheet("""
            QTableWidget {
                gridline-color: #d0d0d0;
                font-size: 14px;
                alternate-background-color: #f7f7f7;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 6px;
                font-size: 14px;
                border: none;
            }
            QTableWidget::item {
                padding-left: 8px;
                padding-right: 8px;
            }
            QTableCornerButton::section {
                background-color: #34495e;
                border: none;
            }
        """)

        # إضافة البيانات
        self.populate_low_stock_table(table)

        layout.addWidget(table)

        # زر الإغلاق
        close_btn = QPushButton("إغلاق")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)

        dialog.exec()


    def create_expiry_window(self):
        """إنشاء نافذة انتهاء الصلاحية مباشرة"""
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton
        from PyQt6.QtGui import QColor

        dialog = QDialog(self)
        dialog.setWindowTitle(f"تنبيهات انتهاء الصلاحية - {self.project_name}")
        dialog.setModal(True)
        dialog.resize(900, 600)

        layout = QVBoxLayout(dialog)

        # العنوان
        title = QLabel("⏰ تنبيهات انتهاء الصلاحية")
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px; text-align: center;")
        layout.addWidget(title)

        # الجدول
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["اسم المادة", "الكمية", "تاريخ الدخول", "الأيام المتبقية"])

        # ----- تحسينات الشكل -----
        table.setSortingEnabled(True)
        table.setAlternatingRowColors(True)
        table.setShowGrid(True)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setStretchLastSection(True)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        table.setStyleSheet("""
            QTableWidget {
                gridline-color: #d0d0d0;
                font-size: 14px;
                alternate-background-color: #f7f7f7;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 6px;
                font-size: 14px;
                border: none;
            }
            QTableWidget::item {
                padding-left: 8px;
                padding-right: 8px;
            }
            QTableCornerButton::section {
                background-color: #34495e;
                border: none;
            }
        """)

        # إضافة البيانات
        self.populate_expiry_table(table)

        layout.addWidget(table)

        # زر الإغلاق
        close_btn = QPushButton("إغلاق")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)

        dialog.exec()


    def populate_low_stock_table(self, table):
        """ملء جدول المخزون المنخفض"""
        try:
            from excel_manager import excel_manager
            from PyQt6.QtGui import QColor
            from PyQt6.QtWidgets import QTableWidgetItem

            inventory_df = excel_manager.get_inventory_summary(self.project_name)
            low_stock_items = []

            if not inventory_df.empty:
                for _, item in inventory_df.iterrows():
                    current_qty = item.get('الكمية_الحالية', 0)
                    min_qty = 10

                    if current_qty <= min_qty and current_qty > 0:
                        low_stock_items.append({
                            'item_name': item.get('اسم_العنصر', '').strip(),
                            'current_qty': current_qty,
                            'min_qty': min_qty
                        })

            # لا نضيف بيانات تجريبية - نعتمد على البيانات الحقيقية فقط

            low_stock_items = [
                item for item in low_stock_items
                if item.get('item_name') and item.get('item_name').strip() != ''
            ]

            low_stock_items.sort(key=lambda x: x['current_qty'])

            table.setRowCount(len(low_stock_items) if low_stock_items else 1)

            if low_stock_items:
                for row, item in enumerate(low_stock_items):
                    item_name = str(item['item_name']).strip()
                    current_qty = int(float(item['current_qty']))
                    min_qty = int(float(item['min_qty']))

                    table.setItem(row, 0, QTableWidgetItem(item_name))
                    table.setItem(row, 1, QTableWidgetItem(str(current_qty)))
                    table.setItem(row, 2, QTableWidgetItem(str(min_qty)))

                    for col in range(3):
                        widget = table.item(row, col)
                        widget.setBackground(QColor(231, 76, 60))
                        widget.setForeground(QColor(255, 255, 255))

            else:
                table.setItem(0, 0, QTableWidgetItem("لا توجد تنبيهات مخزون منخفض"))
                table.setItem(0, 1, QTableWidgetItem("-"))
                table.setItem(0, 2, QTableWidgetItem("-"))

            table.resizeColumnsToContents()

        except Exception as e:
            print(f"خطأ في ملء جدول المخزون المنخفض: {e}")


    def populate_expiry_table(self, table):
        """ملء جدول انتهاء الصلاحية"""
        try:
            import pandas as pd
            import os
            from datetime import datetime, timedelta
            from PyQt6.QtGui import QColor
            from PyQt6.QtWidgets import QTableWidgetItem

            expiry_items = []

            project_file = os.path.join("projects", f"{self.project_name}_Transactions.xlsx")
            if os.path.exists(project_file):
                transactions_df = pd.read_excel(project_file, engine='openpyxl')

                if not transactions_df.empty:
                    incoming_transactions = transactions_df[transactions_df['نوع_العملية'] == 'دخول'].copy()
                    incoming_transactions['التاريخ'] = pd.to_datetime(incoming_transactions['التاريخ'])

                    for _, transaction in incoming_transactions.iterrows():
                        shelf_life_days = transaction.get('مدة_الصلاحية_بالأيام')
                        item_name = transaction.get('اسم_العنصر', '').strip()

                        if pd.notna(shelf_life_days) and shelf_life_days > 0 and item_name:
                            entry_date = transaction['التاريخ']
                            expiry_date = entry_date + timedelta(days=int(shelf_life_days))
                            days_remaining = (expiry_date - datetime.now()).days

                            if 0 <= days_remaining <= 10:
                                expiry_items.append({
                                    'item_name': item_name,
                                    'quantity': int(float(transaction['الكمية'])),
                                    'entry_date': entry_date.strftime('%Y-%m-%d'),
                                    'days_remaining': days_remaining
                                })

            # لا نضيف بيانات تجريبية - نعتمد على البيانات الحقيقية فقط

            expiry_items = [x for x in expiry_items if x['item_name']]
            expiry_items.sort(key=lambda x: x['days_remaining'])

            table.setRowCount(len(expiry_items) if expiry_items else 1)

            if expiry_items:
                for row, item in enumerate(expiry_items):
                    table.setItem(row, 0, QTableWidgetItem(item['item_name']))
                    table.setItem(row, 1, QTableWidgetItem(str(item['quantity'])))
                    table.setItem(row, 2, QTableWidgetItem(item['entry_date']))
                    table.setItem(row, 3, QTableWidgetItem(f"{item['days_remaining']} يوم"))

                    if item['days_remaining'] <= 3:
                        bg = QColor(231, 76, 60)
                        fg = QColor(255, 255, 255)
                    else:
                        bg = QColor(241, 196, 15)
                        fg = QColor(0, 0, 0)

                    for col in range(4):
                        w = table.item(row, col)
                        w.setBackground(bg)
                        w.setForeground(fg)

            else:
                table.setItem(0, 0, QTableWidgetItem("لا توجد تنبيهات انتهاء صلاحية"))
                table.setItem(0, 1, QTableWidgetItem("-"))
                table.setItem(0, 2, QTableWidgetItem("-"))
                table.setItem(0, 3, QTableWidgetItem("-"))

            table.resizeColumnsToContents()

        except Exception as e:
            print(f"خطأ في ملء جدول انتهاء الصلاحية: {e}")


    

    

    
    def show_entry_dialog(self):
        """إظهار نافذة إدخال العناصر"""
        from transaction_dialog import TransactionDialog
        dialog = TransactionDialog(self.project_name, "دخول", self)
        if dialog.exec():
            self.update_project_info()
            self.status_bar.showMessage("تم إضافة حركة دخول بنجاح", 3000)
    
    def show_exit_dialog(self):
        """إظهار نافذة إخراج العناصر"""
        from transaction_dialog import TransactionDialog
        dialog = TransactionDialog(self.project_name, "خروج", self)
        if dialog.exec():
            self.update_project_info()
            self.status_bar.showMessage("تم إضافة حركة خروج بنجاح", 3000)
    
    def show_inventory(self):
        """إظهار المخزون الحالي"""
        from inventory_viewer import InventoryViewer
        viewer = InventoryViewer(self.project_name, self)
        viewer.show()
    
    def show_items_management(self):
        """إظهار نافذة إنشاء عنصر جديد"""
        from items_manager import ItemsManager
        manager = ItemsManager(self, self.project_name)
        manager.show()
    
    def show_edit_recent_transactions(self):
        """إظهار نافذة تعديل المعاملات الحديثة"""
        from edit_recent_transactions import EditRecentTransactionsDialog
        dialog = EditRecentTransactionsDialog(self.project_name, self)
        dialog.show()
    
    def show_report_dialog(self):
        """إظهار نافذة إدارة التقارير"""
        from reports_management_dialog import ReportsManagementDialog
        dialog = ReportsManagementDialog(self.project_name, self)
        dialog.exec()
    
    def load_sample_data(self):
        """تحميل بيانات تجريبية للاختبار"""
        try:
            from datetime import datetime, timedelta
            import random
            
            # إضافة عناصر تجريبية
            sample_items = [
                {'اسم_العنصر': 'أسمنت بورتلاندي', 'التصنيف': 'مواد بناء', 'مدة_الصلاحية_بالأيام': 180, 'وصف': 'أسمنت عادي 50 كيس'},
                {'اسم_العنصر': 'حديد تسليح', 'التصنيف': 'مواد بناء', 'مدة_الصلاحية_بالأيام': None, 'وصف': 'حديد تسليح 12 ملم'},
                {'اسم_العنصر': 'طلاء أبيض', 'التصنيف': 'مواد التشطيب', 'مدة_الصلاحية_بالأيام': 365, 'وصف': 'طلاء أبيض جدران'},
                {'اسم_العنصر': 'بلاط سيراميك', 'التصنيف': 'مواد التشطيب', 'مدة_الصلاحية_بالأيام': None, 'وصف': 'بلاط سيراميك 60x60'},
                {'اسم_العنصر': 'مسامير حديد', 'التصنيف': 'المعدات', 'مدة_الصلاحية_بالأيام': None, 'وصف': 'مسامير حديد 8 ملم'},
                {'اسم_العنصر': 'اسلاك كهرباء', 'التصنيف': 'كهرباء', 'مدة_الصلاحية_بالأيام': 730, 'وصف': 'اسلاك كهرباء 2.5 ملم'}
            ]
            
            # إضافة العناصر
            for item in sample_items:
                excel_manager.add_new_item(
                    item['اسم_العنصر'],
                    item['التصنيف'],
                    item['مدة_الصلاحية_بالأيام'],
                    item['وصف']
                )
            
            # إضافة حركات تجريبية
            start_date = datetime.now() - timedelta(days=30)  # 30 يوم ماضية
            
            # حركات الدخول
            for i in range(15):  # 15 حركة دخول
                random_days = random.randint(0, 30)
                transaction_date = start_date + timedelta(days=random_days)
                
                item_info = {
                    'اسم العنصر': random.choice(['أسمنت بورتلاندي', 'حديد تسليح', 'طلاء أبيض', 'بلاط سيراميك']),
                    'التصنيف': random.choice(['مواد بناء', 'مواد التشطيب', 'المعدات']),
                    'مدة الصلاحية (أيام)': random.choice([180, 365, None])
                }
                
                quantity = random.randint(10, 100)
                notes = f"حركة تجريبية - دخول {i+1}"
                
                # إضافة الحركة مع تاريخ مخصص
                self._add_transaction_with_date(item_info, 'دخول', quantity, '', notes, transaction_date)
            
            # حركات الخروج
            for i in range(8):  # 8 حركة خروج
                random_days = random.randint(5, 30)  # بعد الدخول
                transaction_date = start_date + timedelta(days=random_days)
                
                item_info = {
                    'اسم العنصر': random.choice(['أسمنت بورتلاندي', 'حديد تسليح', 'طلاء أبيض']),
                    'التصنيف': random.choice(['مواد بناء', 'مواد التشطيب']),
                    'مدة الصلاحية (أيام)': random.choice([180, 365])
                }
                
                quantity = random.randint(5, 30)
                receiver = random.choice(['محمد أحمد', 'علي حسن', 'فاطمة سعد', 'أحمد علي'])
                notes = f"حركة تجريبية - خروج {i+1}"
                
                self._add_transaction_with_date(item_info, 'خروج', quantity, receiver, notes, transaction_date)
            
            QMessageBox.information(self, "نجح", "تم تحميل البيانات التجريبية بنجاح!\nتم إضافة 6 عناصر و 23 حركة")
            
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في تحميل البيانات: {str(e)}")
    
    def _add_transaction_with_date(self, item_info, transaction_type, quantity, receiver, notes, custom_date):
        """إضافة حركة مع تاريخ مخصص"""
        try:
            import pandas as pd
            project_file = excel_manager.create_site_transactions_file(self.project_name)
            
            # قراءة الملف الحالي
            try:
                df = pd.read_excel(project_file, engine='openpyxl')
            except:
                df = pd.DataFrame(columns=[
                    'المشروع', 'التاريخ', 'اسم_العنصر', 'التصنيف', 
                    'نوع_العملية', 'الكمية', 'اسم_المستلم', 'مدة_الصلاحية_بالأيام', 'ملاحظات'
                ])
            
            # إضافة الحركة الجديدة
            new_transaction = {
                'المشروع': self.project_name,
                'التاريخ': custom_date.strftime('%Y-%m-%d %H:%M:%S'),
                'اسم_العنصر': item_info['اسم العنصر'],
                'التصنيف': item_info['التصنيف'],
                'نوع_العملية': transaction_type,
                'الكمية': float(quantity),
                'اسم_المستلم': receiver,
                'مدة_الصلاحية_بالأيام': item_info.get('مدة الصلاحية (أيام)', None),
                'ملاحظات': notes
            }
            
            df = pd.concat([df, pd.DataFrame([new_transaction])], ignore_index=True)
            df.to_excel(project_file, index=False, engine='openpyxl')
            
        except Exception as e:
            print(f"خطأ في إضافة الحركة: {e}")
    
    def print_report(self):
        """طباعة آخر تقرير"""
        try:
            # إنشاء تقرير PDF أولاً
            filepath, message = self.report_manager.export_inventory_to_pdf(self.project_name)
            
            if filepath:
                success, print_message = self.report_manager.print_report(filepath)
                if success:
                    QMessageBox.information(self, "نجح", print_message)
                    self.status_bar.showMessage("تم إرسال التقرير للطباعة", 3000)
                else:
                    QMessageBox.warning(self, "خطأ", print_message)
            else:
                QMessageBox.warning(self, "خطأ", message)
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في الطباعة: {str(e)}")
    
    def change_project(self):
        """تغيير المشروع"""
        reply = QMessageBox.question(
            self, 
            "تأكيد", 
            "هل تريد العودة لاختيار مشروع آخر؟",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                print("بدء عملية تغيير المشروع")
                
                # تعطيل closeEvent مؤقتاً لتجنب رسالة الخروج
                self._changing_project = True
                
                from project_selector import ProjectSelector
                
                # إنشاء نافذة اختيار المشروع الجديدة
                self.project_selector = ProjectSelector()
                
                # ربط الإشارة لفتح النافذة الجديدة
                self.project_selector.project_selected.connect(self.restart_with_new_project)
                
                print("تم إعداد نافذة اختيار المشروع")
                
                # إخفاء النافذة الحالية وإظهار نافذة الاختيار
                self.hide()
                self.project_selector.show()
                
                print("تم عرض نافذة اختيار المشروع")
                
            except Exception as e:
                self._changing_project = False
                print(f"خطأ في change_project: {e}")
                import traceback
                traceback.print_exc()
                QMessageBox.critical(self, "خطأ", f"خطأ في فتح نافذة اختيار المشروع: {str(e)}")
                self.show()  # إعادة إظهار النافذة الحالية في حالة الخطأ
    

    
    def restart_with_new_project(self, project_name):
        """إعادة تشغيل البرنامج مع مشروع جديد"""
        try:
            print(f"بدء فتح المشروع: {project_name}")
            
            # تأكيد أن هذه عملية تغيير مشروع وليس إغلاق
            self._changing_project = True
            
            # حفظ مرجع للنافذة الجديدة
            print("إنشاء نافذة جديدة...")
            self._new_window = MainWindow(project_name)
            
            # عرض النافذة الجديدة
            self._new_window.show()
            print("تم عرض النافذة الجديدة")
            
            # التأكد من عرض النافذة قبل المتابعة
            QApplication.processEvents()
            
            # استخدام QTimer لضمان العرض قبل الإغلاق
            QTimer.singleShot(100, self._cleanup_old_windows)
            
            print("تم جدولة عملية التنظيف")
                
        except Exception as e:
            self._changing_project = False
            print(f"خطأ في restart_with_new_project: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(None, "خطأ", f"خطأ في فتح المشروع الجديد: {str(e)}")
    
    def _cleanup_old_windows(self):
        """تنظيف النوافذ القديمة بعد عرض الجديدة"""
        try:
            print("بدء عملية تنظيف النوافذ القديمة")
            
            # إغلاق نافذة اختيار المشروع
            if hasattr(self, 'project_selector') and self.project_selector:
                print("إغلاق نافذة اختيار المشروع")
                self.project_selector.close()
                self.project_selector = None
            
            # إغلاق النافذة الحالية بدون تأكيد
            print("إغلاق النافذة القديمة")
            self.close()
            
            print("تم الانتهاء من تغيير المشروع بنجاح")
            
        except Exception as e:
            print(f"خطأ في _cleanup_old_windows: {e}")
            import traceback
            traceback.print_exc()
    
    def toggle_fullscreen(self):
        """تبديل وضع النافذة بين العادي والمكبر"""
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
    
    def keyPressEvent(self, event):
        """التعامل مع ضغط المفاتيح"""
        from PyQt6.QtCore import Qt
        if event.key() == Qt.Key.Key_Escape:
            if self.isMaximized():
                self.showNormal()
        super().keyPressEvent(event)
    def setup_message_box_style(self):
        """إعداد تنسيق رسائل التنبيه"""
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
            background-color: #3498db;
            color: white;
            font-size: 10px;
            font-weight: bold;
            border: none;
            border-radius: 5px;
            padding: 6px 12px;
            min-width: 70px;
        }
        QMessageBox QPushButton:hover {
            background-color: #2980b9;
        }
        QMessageBox QPushButton:pressed {
            background-color: #21618c;
        }
        """
        QApplication.instance().setStyleSheet(QApplication.instance().styleSheet() + message_style)
    
    def closeEvent(self, event):
        """التعامل مع إغلاق النافذة"""
        try:
            print(f"closeEvent مستدعى - _changing_project: {getattr(self, '_changing_project', False)}")
            
            # إذا كنا في عملية تغيير مشروع، لا نظهر رسالة التأكيد
            if hasattr(self, '_changing_project') and self._changing_project:
                print("إغلاق مقبول - تغيير مشروع")
                event.accept()
                return
            
            # في الحالات العادية، نظهر رسالة التأكيد
            reply = QMessageBox.question(
                self,
                "تأكيد الخروج",
                "هل تريد إغلاق البرنامج؟",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                print("المستخدم اختار إغلاق البرنامج")
                event.accept()
            else:
                print("المستخدم الغى إغلاق البرنامج")
                event.ignore()
                
        except Exception as e:
            print(f"خطأ في closeEvent: {e}")
            event.accept()  # في حالة الخطأ، نغلق النافذة


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # تطبيق النافذة الرئيسية لاختبار (يجب استخدام project_selector عادة)
    window = MainWindow("مشروع تجريبي")
    window.show()
    
    sys.exit(app.exec())