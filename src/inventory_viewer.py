# -*- coding: utf-8 -*-
"""
واجهة عرض المخزون الحالي
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QPushButton, QTableWidget, QTableWidgetItem,
                           QHeaderView, QMessageBox, QLineEdit, QComboBox,
                           QFrame, QStatusBar)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor
from excel_manager import excel_manager
import pandas as pd


class InventoryViewer(QMainWindow):
    """واجهة عرض المخزون"""
    
    def __init__(self, project_name, parent=None):
        super().__init__(parent)
        self.project_name = project_name
        self.inventory_data = pd.DataFrame()
        self.filtered_data = pd.DataFrame()
        self.setup_ui()
        self.setup_styles()
        self.load_inventory_data()
        
        # تحديث البيانات كل 30 ثانية
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_data)
        self.refresh_timer.start(30000)  # 30 ثانية
    
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        self.setWindowTitle(f"المخزون الحالي - {self.project_name}")
        self.showMaximized()
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        # الودجة الرئيسية
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # التخطيط الرئيسي
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # منطقة العنوان
        header_layout = self.create_header()
        main_layout.addLayout(header_layout)
        
        # منطقة البحث والتصفية
        filter_layout = self.create_filter_section()
        main_layout.addLayout(filter_layout)
        
        # جدول المخزون
        self.create_inventory_table()
        main_layout.addWidget(self.inventory_table)
        
        # منطقة الأزرار
        buttons_layout = self.create_buttons_section()
        main_layout.addLayout(buttons_layout)
        
        # شريط الحالة
        self.create_status_bar()
    
    def create_header(self):
        """إنشاء منطقة العنوان"""
        layout = QVBoxLayout()
        
        # العنوان الرئيسي
        title_label = QLabel("المخزون الحالي")
        title_label.setObjectName("main_title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # اسم المشروع
        project_label = QLabel(f"المشروع: {self.project_name}")
        project_label.setObjectName("project_name")
        project_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(project_label)
        
        return layout
    
    def create_filter_section(self):
        """إنشاء منطقة البحث والتصفية"""
        filter_frame = QFrame()
        filter_frame.setObjectName("filter_frame")
        filter_frame.setFrameStyle(QFrame.Shape.Box)
        
        layout = QHBoxLayout(filter_frame)
        
        # بحث بالاسم
        search_label = QLabel("بحث:")
        layout.addWidget(search_label)
        
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("ابحث باسم العنصر...")
        self.search_edit.setObjectName("search_input")
        self.search_edit.textChanged.connect(self.filter_data)
        layout.addWidget(self.search_edit)
        
        # تصفية بالتصنيف
        category_label = QLabel("التصنيف:")
        layout.addWidget(category_label)
        
        self.category_combo = QComboBox()
        self.category_combo.setObjectName("category_combo")
        self.category_combo.currentTextChanged.connect(self.filter_data)
        layout.addWidget(self.category_combo)
        
        # تصفية بحالة المخزون
        stock_label = QLabel("حالة المخزون:")
        layout.addWidget(stock_label)
        
        self.stock_combo = QComboBox()
        self.stock_combo.setObjectName("stock_combo")
        self.stock_combo.addItems(["الكل", "متوفر", "نفد المخزون", "مخزون منخفض"])
        self.stock_combo.currentTextChanged.connect(self.filter_data)
        layout.addWidget(self.stock_combo)
        
        # زر تحديث
        refresh_btn = QPushButton("تحديث")
        refresh_btn.setObjectName("refresh_button")
        refresh_btn.clicked.connect(self.refresh_data)
        layout.addWidget(refresh_btn)
        
        return QVBoxLayout().addWidget(filter_frame) or QVBoxLayout()
    
    def create_inventory_table(self):
        """إنشاء جدول المخزون"""
        self.inventory_table = QTableWidget()
        self.inventory_table.setObjectName("inventory_table")
        
        # تعيين الأعمدة (بدون أعمدة الدخول والخروج)
        columns = [
            "اسم العنصر",
            "التصنيف", 
            "الكمية المتبقية",
            "مدة الصلاحية (أيام)",
            "حالة المخزون"
        ]
        
        self.inventory_table.setColumnCount(len(columns))
        self.inventory_table.setHorizontalHeaderLabels(columns)
        
        # تنسيق الجدول
        header = self.inventory_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # تفعيل الترتيب
        self.inventory_table.setSortingEnabled(True)
        
        # تنسيق الصفوف
        self.inventory_table.setAlternatingRowColors(True)
        self.inventory_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        # منع التعديل
        self.inventory_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    
    def create_buttons_section(self):
        """إنشاء منطقة الأزرار"""
        layout = QHBoxLayout()
        
        # زر تصدير Excel
        excel_btn = QPushButton("تصدير إلى Excel")
        excel_btn.setObjectName("excel_button")
        excel_btn.clicked.connect(self.export_to_excel)
        layout.addWidget(excel_btn)
        
        # زر تصدير PDF
        pdf_btn = QPushButton("تصدير إلى PDF")
        pdf_btn.setObjectName("pdf_button")
        pdf_btn.clicked.connect(self.export_to_pdf)
        layout.addWidget(pdf_btn)
        
        # زر إدخال عنصر
        entry_btn = QPushButton("إدخال عنصر")
        entry_btn.setObjectName("entry_button")
        entry_btn.clicked.connect(self.add_entry)
        layout.addWidget(entry_btn)
        
        # زر إخراج عنصر
        exit_btn = QPushButton("إخراج عنصر")
        exit_btn.setObjectName("exit_button")
        exit_btn.clicked.connect(self.add_exit)
        layout.addWidget(exit_btn)
        
        # مساحة مرنة
        layout.addStretch()
        
        # زر إغلاق
        close_btn = QPushButton("إغلاق")
        close_btn.setObjectName("close_button")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
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
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            padding: 15px;
        }
        
        QLabel#project_name {
            font-size: 18px;
            font-weight: bold;
            color: #3498db;
            padding: 10px;
        }
        
        QFrame#filter_frame {
            background-color: white;
            border: 2px solid #bdc3c7;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0px;
        }
        
        QLineEdit#search_input {
            font-size: 13px;
            padding: 8px;
            border: 2px solid #bdc3c7;
            border-radius: 5px;
            background-color: white;
            color: #2c3e50;
            min-width: 200px;
        }
        
        QLineEdit#search_input:focus {
            border-color: #3498db;
            background-color: #ffffff;
            color: #2c3e50;
        }
        
        QComboBox#category_combo, QComboBox#stock_combo {
            font-size: 13px;
            padding: 8px;
            border: 2px solid #bdc3c7;
            border-radius: 5px;
            background-color: white;
            min-width: 120px;
        }
        
        QTableWidget#inventory_table {
            background-color: white;
            border: 2px solid #bdc3c7;
            border-radius: 10px;
            gridline-color: #ecf0f1;
            font-size: 12px;
        }
        
        QTableWidget#inventory_table::item {
            padding: 8px;
            border-bottom: 1px solid #ecf0f1;
            color: #2c3e50;
            background-color: white;
        }
        
        QTableWidget#inventory_table::item:alternate {
            background-color: #f8f9fa;
            color: #2c3e50;
        }
        
        QTableWidget#inventory_table::item:selected {
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
        
        QPushButton#refresh_button {
            background-color: #3498db;
            color: white;
            font-size: 13px;
            font-weight: bold;
            border: none;
            border-radius: 5px;
            padding: 8px 15px;
        }
        
        QPushButton#refresh_button:hover {
            background-color: #2980b9;
        }
        
        QPushButton#excel_button {
            background-color: #f39c12;
            color: white;
            font-size: 14px;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            padding: 12px 20px;
        }
        
        QPushButton#excel_button:hover {
            background-color: #e67e22;
        }
        
        QPushButton#pdf_button {
            background-color: #e67e22;
            color: white;
            font-size: 14px;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            padding: 12px 20px;
        }
        
        QPushButton#pdf_button:hover {
            background-color: #d35400;
        }
        
        QPushButton#entry_button {
            background-color: #27ae60;
            color: white;
            font-size: 14px;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            padding: 12px 20px;
        }
        
        QPushButton#entry_button:hover {
            background-color: #2ecc71;
        }
        
        QPushButton#exit_button {
            background-color: #e74c3c;
            color: white;
            font-size: 14px;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            padding: 12px 20px;
        }
        
        QPushButton#exit_button:hover {
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
    
    def load_inventory_data(self):
        """تحميل بيانات المخزون"""
        try:
            self.inventory_data = excel_manager.get_inventory_summary(self.project_name)
            
            # تحميل التصنيفات للتصفية
            self.load_categories()
            
            # عرض البيانات
            self.display_data(self.inventory_data)
            
            # تحديث شريط الحالة
            total_items = len(self.inventory_data)
            self.status_bar.showMessage(f"إجمالي العناصر: {total_items}")
            
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في تحميل بيانات المخزون: {str(e)}")
    
    def load_categories(self):
        """تحميل التصنيفات للتصفية"""
        self.category_combo.clear()
        self.category_combo.addItem("جميع التصنيفات")
        
        if not self.inventory_data.empty:
            categories = self.inventory_data['التصنيف'].unique()
            for category in sorted(categories):
                self.category_combo.addItem(category)
    
    def display_data(self, data):
        """عرض البيانات في الجدول"""
        self.inventory_table.setRowCount(len(data))
        
        for row, (_, item) in enumerate(data.iterrows()):
            # اسم العنصر
            self.inventory_table.setItem(row, 0, QTableWidgetItem(str(item['اسم_العنصر'])))
            
            # التصنيف
            self.inventory_table.setItem(row, 1, QTableWidgetItem(str(item['التصنيف'])))
            
            # الكمية الحالية
            current_qty = float(item['الكمية_الحالية'])
            qty_item = QTableWidgetItem(str(current_qty))
            
            # تلوين الكمية حسب المستوى
            if current_qty == 0:
                qty_item.setBackground(QColor("#e74c3c"))  # أحمر للنفاد
                qty_item.setForeground(QColor("white"))
            elif current_qty < 10:  # مخزون منخفض
                qty_item.setBackground(QColor("#f39c12"))  # برتقالي للمنخفض
                qty_item.setForeground(QColor("white"))
            else:
                qty_item.setBackground(QColor("#27ae60"))  # أخضر للمتوفر
                qty_item.setForeground(QColor("white"))
            
            self.inventory_table.setItem(row, 2, qty_item)
            
            # مدة الصلاحية
            shelf_life = item['مدة_الصلاحية_بالأيام']
            if pd.notna(shelf_life):
                self.inventory_table.setItem(row, 3, QTableWidgetItem(f"{int(shelf_life)} يوم"))
            else:
                self.inventory_table.setItem(row, 3, QTableWidgetItem("غير محدد"))
            
            # حالة المخزون
            if current_qty == 0:
                status = "نفد المخزون"
                status_color = QColor("#e74c3c")
            elif current_qty < 10:
                status = "مخزون منخفض"
                status_color = QColor("#f39c12")
            else:
                status = "متوفر"
                status_color = QColor("#27ae60")
            
            status_item = QTableWidgetItem(status)
            status_item.setBackground(status_color)
            status_item.setForeground(QColor("white"))
            self.inventory_table.setItem(row, 4, status_item)
    
    def filter_data(self):
        """تصفية البيانات"""
        if self.inventory_data.empty:
            return
        
        filtered_data = self.inventory_data.copy()
        
        # تصفية بالبحث
        search_text = self.search_edit.text().strip().lower()
        if search_text:
            filtered_data = filtered_data[
                filtered_data['اسم_العنصر'].str.lower().str.contains(search_text)
            ]
        
        # تصفية بالتصنيف
        selected_category = self.category_combo.currentText()
        if selected_category != "جميع التصنيفات":
            filtered_data = filtered_data[filtered_data['التصنيف'] == selected_category]
        
        # تصفية بحالة المخزون
        stock_status = self.stock_combo.currentText()
        if stock_status == "متوفر":
            filtered_data = filtered_data[filtered_data['الكمية_الحالية'] > 10]
        elif stock_status == "نفد المخزون":
            filtered_data = filtered_data[filtered_data['الكمية_الحالية'] == 0]
        elif stock_status == "مخزون منخفض":
            filtered_data = filtered_data[
                (filtered_data['الكمية_الحالية'] > 0) & 
                (filtered_data['الكمية_الحالية'] <= 10)
            ]
        
        self.filtered_data = filtered_data
        self.display_data(filtered_data)
        
        # تحديث شريط الحالة
        total_items = len(filtered_data)
        if len(filtered_data) != len(self.inventory_data):
            self.status_bar.showMessage(f"عرض {total_items} من {len(self.inventory_data)} عنصر")
        else:
            self.status_bar.showMessage(f"إجمالي العناصر: {total_items}")
    
    def refresh_data(self):
        """تحديث البيانات"""
        self.status_bar.showMessage("جاري تحديث البيانات...")
        self.load_inventory_data()
        self.filter_data()
        self.status_bar.showMessage("تم تحديث البيانات", 2000)
    
    def export_to_excel(self):
        """تصدير إلى Excel"""
        try:
            from report_manager import ReportManager
            report_manager = ReportManager(excel_manager)
            
            filepath, message = report_manager.export_inventory_to_excel(self.project_name)
            if filepath:
                QMessageBox.information(self, "نجح", f"{message}\nمسار الملف: {filepath}")
            else:
                QMessageBox.warning(self, "خطأ", message)
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في تصدير Excel: {str(e)}")
    
    def export_to_pdf(self):
        """تصدير إلى PDF"""
        try:
            from report_manager import ReportManager
            report_manager = ReportManager(excel_manager)
            
            filepath, message = report_manager.export_inventory_to_pdf(self.project_name)
            if filepath:
                QMessageBox.information(self, "نجح", f"{message}\nمسار الملف: {filepath}")
            else:
                QMessageBox.warning(self, "خطأ", message)
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في تصدير PDF: {str(e)}")
    
    def add_entry(self):
        """إضافة حركة دخول"""
        from transaction_dialog import TransactionDialog
        dialog = TransactionDialog(self.project_name, "دخول", self)
        if dialog.exec():
            self.refresh_data()
    
    def add_exit(self):
        """إضافة حركة خروج"""
        from transaction_dialog import TransactionDialog
        dialog = TransactionDialog(self.project_name, "خروج", self)
        if dialog.exec():
            self.refresh_data()
    
    def closeEvent(self, event):
        """التعامل مع إغلاق النافذة"""
        self.refresh_timer.stop()
        event.accept()