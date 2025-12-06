# -*- coding: utf-8 -*-
"""
Advanced Report Viewer - برنامج المدير المتقدم (النسخة 2.0)
نظام عرض التقارير مع جداول قابلة للترتيب وفلاتر متقدمة
"""

import sys
import os
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QTableWidget, 
                             QTableWidgetItem, QMessageBox, QFileDialog, 
                             QFrame, QTreeWidget, QTreeWidgetItem, QHeaderView,
                             QLineEdit, QComboBox, QDialog, QSpinBox)
from PyQt6.QtCore import Qt, QDate, QTimer, pyqtSignal, QThread
from PyQt6.QtGui import QFont, QIcon, QColor, QBrush
import pandas as pd


class TransactionsViewer(QDialog):
    """نافذة عرض جميع الحركات مع الفلاتر"""
    
    def __init__(self, transactions_df, project_name):
        super().__init__()
        self.transactions_df = transactions_df
        self.project_name = project_name
        self.gap_dates = self.check_date_continuity()  # الأيام المنقطعة
        self.setup_ui()
    
    def _format_days_remaining(self, value):
        """تنسيق الأيام المتبقية (من تاريخ العملية)"""
        try:
            if not value or value == "":
                return ""
            
            # استخراج الرقم من النص
            days_str = str(value).split()[0]
            days = int(days_str)
            
            if days <= 7:
                return f"{days} يوم" # تحذير لأيام قليلة
            elif days <= 30:
                return f"{days} يوم"
            else:
                return f"{days} يوم"
        except:
            return str(value)
    
    def check_date_continuity(self):
        """فحص الأيام المنقطعة في الحركات"""
        if self.transactions_df is None or self.transactions_df.empty:
            return set()
        
        # البحث عن عمود التاريخ
        date_col = None
        for col in ['التاريخ', 'تاريخ', 'Date', 'date']:
            if col in self.transactions_df.columns:
                date_col = col
                break
        
        if not date_col:
            return set()
        
        try:
            # تحويل جميع التواريخ إلى datetime ثم استخراج التاريخ فقط (date)
            dates_list = []
            for val in self.transactions_df[date_col]:
                try:
                    dt = pd.to_datetime(val)
                    dates_list.append(dt.date())
                except:
                    pass
            
            if not dates_list:
                return set()
            
            dates = sorted(set(dates_list))  # إزالة التكرارات والترتيب
            gap_dates = set()
            
            for i in range(len(dates) - 1):
                diff = (dates[i + 1] - dates[i]).days
                if diff > 1:  # قطع في التسلسل
                    current_date = dates[i] + timedelta(days=1)
                    while current_date < dates[i + 1]:
                        gap_dates.add(current_date)
                        current_date += timedelta(days=1)
            
            return gap_dates
        except Exception as e:
            return set()
    
    def setup_ui(self):
        """إعداد الواجهة"""
        self.setWindowTitle(f"جميع الحركات - {self.project_name}")
        self.setGeometry(200, 200, 1400, 700)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # العنوان
        title = QLabel(f"📊 جميع الحركات - {self.project_name}")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        main_layout.addWidget(title)
        
        # شريط الفلاتر
        filter_layout = QHBoxLayout()
        
        # فلتر البحث
        filter_layout.addWidget(QLabel("البحث:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("ابحث عن عنصر أو حركة...")
        self.search_input.setMinimumHeight(35)
        self.search_input.textChanged.connect(self.apply_filters)
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff;
                color: #000000;
                border: 2px solid #000000;
                border-radius: 5px;
                padding: 8px;
                font-size: 13px;
                font-weight: bold;
            }
            QLineEdit:focus {
                border: 2px solid #2980b9;
                background-color: #f0f8ff;
            }
        """)
        filter_layout.addWidget(self.search_input)
        
        # فلتر نوع الحركة
        if 'نوع_الحركة' in self.transactions_df.columns or 'النوع' in self.transactions_df.columns:
            filter_layout.addWidget(QLabel("نوع الحركة:"))
            self.type_filter = QComboBox()
            self.type_filter.addItem("الكل")
            type_col = 'نوع_الحركة' if 'نوع_الحركة' in self.transactions_df.columns else 'النوع'
            for item_type in self.transactions_df[type_col].unique():
                self.type_filter.addItem(str(item_type))
            self.type_filter.currentTextChanged.connect(self.apply_filters)
            self.type_filter.setMinimumHeight(35)
            self.type_filter.setMinimumWidth(150)
            self.type_filter.setStyleSheet("""
                QComboBox {
                    background-color: #ffffff;
                    color: #000000;
                    border: 2px solid #000000;
                    border-radius: 5px;
                    padding: 8px;
                    font-size: 13px;
                    font-weight: bold;
                }
                QComboBox:hover {
                    background-color: #f5f5f5;
                    border: 2px solid #2980b9;
                }
            """)
            filter_layout.addWidget(self.type_filter)
        
        filter_layout.addStretch()
        
        # زر التصدير
        export_btn = QPushButton("💾 تصدير")
        export_btn.setMinimumHeight(35)
        export_btn.clicked.connect(self.export_transactions)
        export_btn.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        filter_layout.addWidget(export_btn)
        
        main_layout.addLayout(filter_layout)
        
        # جدول الحركات
        self.transactions_table = QTableWidget()
        self.transactions_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #999999;
                background-color: #ffffff;
                border: 2px solid #999999;
                border-radius: 5px;
                font-size: 13px;
            }
            QHeaderView::section {
                background-color: #1a1a1a !important;
                color: #ffffff !important;
                padding: 12px !important;
                border: 2px solid #000000 !important;
                font-weight: bold !important;
                font-size: 13px !important;
                height: 45px !important;
            }
            QTableWidget::item {
                padding: 10px !important;
                border: 1px solid #cccccc !important;
                color: #000000 !important;
                font-size: 13px !important;
                height: 35px !important;
            }
            QTableWidget::item:alternate {
                background-color: #f0f0f0;
            }
            QScrollBar:vertical {
                background-color: #f0f0f0;
                width: 15px;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical {
                background-color: #888888;
                border-radius: 7px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #555555;
            }
        """)
        self.transactions_table.setAlternatingRowColors(True)
        self.transactions_table.setSortingEnabled(True)
        self.transactions_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # تعطيل التعديل
        self.transactions_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.transactions_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        main_layout.addWidget(self.transactions_table, 1)
        
        self.setLayout(main_layout)
        
        # عرض البيانات
        self.display_transactions()
    
    def apply_filters(self):
        """تطبيق الفلاتر"""
        df = self.transactions_df.copy()
        
        # فلتر البحث
        search_text = self.search_input.text().lower()
        if search_text:
            mask = False
            for col in df.columns:
                mask = mask | df[col].astype(str).str.lower().str.contains(search_text)
            df = df[mask]
        
        # فلتر نوع الحركة
        if hasattr(self, 'type_filter') and self.type_filter.currentText() != "الكل":
            type_col = 'نوع_الحركة' if 'نوع_الحركة' in df.columns else 'النوع'
            df = df[df[type_col] == self.type_filter.currentText()]
        
        self.display_transactions(df)
    
    def display_transactions(self, df=None):
        """عرض الحركات في الجدول"""
        if df is None:
            df = self.transactions_df.copy()
        else:
            df = df.copy()
        
        print(f"📊 عرض البيانات: {len(df)} صف، {len(df.columns)} عمود")
        print(f"أعمدة: {df.columns.tolist()}")
        
        if df.empty:
            print("⚠️ البيانات فارغة!")
            return
        
        # حساب الأيام المتبقية للصلاحية
        # الصيغة: مدة_الصلاحية_بالأيام - (تاريخ اليوم - تاريخ دخول العنصر)
        if 'الأيام_المتبقية' not in df.columns:
            try:
                today = datetime.now().date()
                
                def calc_remaining_days(row):
                    # تحقق من وجود عمود مدة الصلاحية
                    validity_days = None
                    if 'مدة_الصلاحية_بالأيام' in row.index:
                        try:
                            validity_days = float(row['مدة_الصلاحية_بالأيام'])
                        except:
                            pass
                    
                    # إذا لم تكن هناك مدة صلاحية، ارجع فارغ
                    if validity_days is None or pd.isna(validity_days):
                        return ""
                    
                    # احسب الفرق بين يوم الدخول واليوم الحالي
                    if 'التاريخ' in row.index and pd.notna(row['التاريخ']):
                        try:
                            entry_date = pd.to_datetime(row['التاريخ']).date()
                            days_passed = (today - entry_date).days
                            
                            # احسب الأيام المتبقية
                            remaining_days = validity_days - days_passed
                            
                            return f"{int(remaining_days)}"
                        except Exception as e:
                            return ""
                    return ""
                
                df['الأيام_المتبقية'] = df.apply(calc_remaining_days, axis=1)
            except Exception as e:
                print(f"خطأ في حساب الأيام المتبقية: {e}")
        
        self.transactions_table.setRowCount(0)
        self.transactions_table.setColumnCount(len(df.columns))
        self.transactions_table.setHorizontalHeaderLabels([str(col) for col in df.columns])
        
        # إيجاد عمود التاريخ
        date_col_idx = None
        for col_idx, col_name in enumerate(df.columns):
            if col_name in ['التاريخ', 'تاريخ', 'Date', 'date']:
                date_col_idx = col_idx
                break
        
        for row_idx, (idx, row) in enumerate(df.iterrows()):
            self.transactions_table.insertRow(row_idx)
            for col_idx, (col_name, value) in enumerate(row.items()):
                item = QTableWidgetItem(str(value))
                
                # تلوين الأيام المنقطعة بالأحمر
                if col_idx == date_col_idx and self.gap_dates:
                    try:
                        dt = pd.to_datetime(value)
                        item_date = dt.date() if hasattr(dt, 'date') else dt
                        
                        if item_date in self.gap_dates:
                            item.setBackground(QColor("#ff0000"))
                            item.setForeground(QColor("#ffffff"))
                    except Exception as e:
                        pass
                
                # تلوين الأيام المتبقية للصلاحية
                if col_name == 'الأيام_المتبقية' and value and value != "":
                    try:
                        days = int(str(value).strip())
                        
                        if days < 0:
                            # انتهت الصلاحية - أحمر غامق
                            item.setBackground(QColor("#d32f2f"))
                            item.setForeground(QColor("#ffffff"))
                            item.setFont(QFont("Arial", 11, QFont.Weight.Bold))
                        elif days == 0:
                            # تنتهي اليوم - برتقالي
                            item.setBackground(QColor("#ff6f00"))
                            item.setForeground(QColor("#ffffff"))
                            item.setFont(QFont("Arial", 11, QFont.Weight.Bold))
                        elif days <= 7:
                            # أقل من أسبوع - أحمر فاتح تحذير
                            item.setBackground(QColor("#ff5252"))
                            item.setForeground(QColor("#ffffff"))
                            item.setFont(QFont("Arial", 11, QFont.Weight.Bold))
                        elif days <= 30:
                            # أسبوع إلى شهر - أصفر تحذير
                            item.setBackground(QColor("#ffc107"))
                            item.setForeground(QColor("#000000"))
                            item.setFont(QFont("Arial", 11, QFont.Weight.Bold))
                        elif days <= 90:
                            # شهر إلى 3 أشهر - أخضر فاتح
                            item.setBackground(QColor("#81c784"))
                            item.setForeground(QColor("#000000"))
                        else:
                            # أكثر من 3 أشهر - أخضر غامق
                            item.setBackground(QColor("#388e3c"))
                            item.setForeground(QColor("#ffffff"))
                    except:
                        pass
                
                self.transactions_table.setItem(row_idx, col_idx, item)
            
            # زيادة ارتفاع الصف
            self.transactions_table.setRowHeight(row_idx, 45)
        
        # ضبط عرض الأعمدة
        self.transactions_table.resizeColumnsToContents()
    
    def export_transactions(self):
        """تصدير الحركات"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "حفظ الحركات", f"حركات_{self.project_name}.xlsx",
            "Excel Files (*.xlsx)"
        )
        
        if file_path:
            try:
                self.transactions_df.to_excel(file_path, index=False, engine='openpyxl')
                QMessageBox.information(self, "نجح", "تم التصدير بنجاح")
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"فشل التصدير: {str(e)}")


class ReportMonitor(QThread):
    """مراقب فولدر التقارير"""
    report_found = pyqtSignal(str)
    reports_updated = pyqtSignal(list)
    
    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path
        self.is_running = True
        self.last_files = set()
    
    def run(self):
        """مراقبة الفولدر"""
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path, exist_ok=True)
        
        while self.is_running:
            try:
                # استبعاد الملفات المؤقتة
                excel_files = [f for f in Path(self.folder_path).glob("*.xlsx") if not f.name.startswith("~")]
                current_files = {str(f) for f in excel_files}
                
                new_files = current_files - self.last_files
                
                for new_file in new_files:
                    self.report_found.emit(new_file)
                
                if current_files != self.last_files:
                    self.reports_updated.emit(sorted(list(current_files), reverse=True))
                
                self.last_files = current_files
                self.msleep(1000)
                
            except Exception as e:
                print(f"خطأ في مراقبة الفولدر: {e}")
                self.msleep(2000)
    
    def stop(self):
        self.is_running = False


class ReportAnalyzer:
    """محلل التقارير المتقدم"""
    
    def __init__(self, excel_file):
        self.excel_file = excel_file
        self.project_name = None
        self.inventory_df = None
        self.transactions_df = None
        self.load_report()
    
    def load_report(self):
        """تحميل التقرير"""
        try:
            # محاولة قراءة اسم المشروع من شيت "جميع الحركات"
            try:
                all_transactions_df = pd.read_excel(self.excel_file, sheet_name='جميع الحركات', engine='openpyxl')
                if 'المشروع' in all_transactions_df.columns:
                    projects = all_transactions_df['المشروع'].unique()
                    if len(projects) > 0:
                        self.project_name = str(projects[0]).strip()
            except:
                pass
            
            # إذا لم نجد من جميع الحركات، نحاول معلومات التقرير
            if not self.project_name:
                try:
                    info_df = pd.read_excel(self.excel_file, sheet_name='معلومات التقرير', engine='openpyxl')
                    
                    # البحث عن اسم المشروع
                    for idx, row in info_df.iterrows():
                        row_dict = row.to_dict()
                        # محاولة إيجاد عمود المعلومة والقيمة بأسماء مختلفة
                        for key, val in row_dict.items():
                            if isinstance(val, str) and 'المشروع' in val:
                                # الحصول على القيمة من العمود التالي
                                next_key = list(row_dict.keys())[list(row_dict.keys()).index(key) + 1] if list(row_dict.keys()).index(key) < len(row_dict) - 1 else None
                                if next_key:
                                    self.project_name = str(row_dict.get(next_key, 'غير معروف')).strip()
                                    break
                            elif isinstance(val, str) and val.strip() and 'مشروع' in val.lower():
                                self.project_name = str(val).strip()
                                break
                        if self.project_name:
                            break
                except:
                    pass
            
            # إذا لم نجد اسم المشروع، نستخدم اسم الملف
            if not self.project_name:
                self.project_name = os.path.basename(self.excel_file).replace('.xlsx', '')
            
            # قراءة المخزون الحالي
            try:
                self.inventory_df = pd.read_excel(self.excel_file, sheet_name='المخزون الحالي', engine='openpyxl')
                # إزالة التكرارات
                self.inventory_df = self.inventory_df.drop_duplicates(subset=['اسم_العنصر'])
            except:
                self.inventory_df = pd.DataFrame()
            
            # قراءة الحركات
            try:
                self.transactions_df = pd.read_excel(self.excel_file, sheet_name='الحركات', engine='openpyxl')
                # تحويل التاريخ
                self.transactions_df['التاريخ'] = pd.to_datetime(self.transactions_df['التاريخ'])
                # إزالة التكرارات
                self.transactions_df = self.transactions_df.drop_duplicates()
            except:
                self.transactions_df = pd.DataFrame()
            
            # قراءة جميع الحركات
            try:
                self.all_transactions_df = pd.read_excel(self.excel_file, sheet_name='جميع الحركات', engine='openpyxl')
                # تحويل التاريخ
                if 'التاريخ' in self.all_transactions_df.columns:
                    self.all_transactions_df['التاريخ'] = pd.to_datetime(self.all_transactions_df['التاريخ'])
                # إزالة التكرارات
                self.all_transactions_df = self.all_transactions_df.drop_duplicates()
            except:
                self.all_transactions_df = pd.DataFrame()
        
        except Exception as e:
            print(f"خطأ في تحميل التقرير: {e}")
            self.project_name = "خطأ في التحميل"
            self.inventory_df = pd.DataFrame()
            self.transactions_df = pd.DataFrame()
    
    def get_inventory_data(self):
        """الحصول على بيانات المخزون"""
        if self.inventory_df is None or self.inventory_df.empty:
            return pd.DataFrame()
        
        return self.inventory_df.copy()
    
    def get_categories(self):
        """الحصول على التصنيفات المتاحة"""
        if self.inventory_df is None or self.inventory_df.empty:
            return []
        
        if 'التصنيف' in self.inventory_df.columns:
            return sorted(self.inventory_df['التصنيف'].unique().tolist())
        return []
    
    def check_date_continuity(self):
        """فحص تسلسل التواريخ والإشارة إلى القطع"""
        if self.transactions_df is None or self.transactions_df.empty:
            return set()
        
        dates = sorted(self.transactions_df['التاريخ'].unique())
        gap_dates = set()
        
        for i in range(len(dates) - 1):
            diff = (dates[i + 1] - dates[i]).days
            if diff > 1:  # قطع في التسلسل
                current_date = dates[i] + timedelta(days=1)
                while current_date < dates[i + 1]:
                    gap_dates.add(current_date.date())
                    current_date += timedelta(days=1)
        
        return gap_dates


class AdvancedReportViewerV2(QMainWindow):
    """تطبيق المدير المتقدم النسخة 2.0"""
    
    def __init__(self):
        super().__init__()
        self.reports_folder = "manager_reports"
        self.reports_data = {}  # {project_name: [file_paths]}
        self.current_project = None
        self.current_analyzer = None
        self.gap_dates = set()
        self.transactions_window = None
        self.open_windows = []  # قائمة النوافذ المفتوحة
        
        os.makedirs(self.reports_folder, exist_ok=True)
        
        self.setup_ui()
        self.start_monitoring()
    
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        self.setWindowTitle("برنامج المدير - نظام التقارير المتقدم 2.0")
        self.setGeometry(100, 100, 1800, 1000)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # العنوان
        title_label = QLabel("نظام التقارير")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                background-color: #1c3a47;
                color: white;
                padding: 20px;
                border-radius: 10px;
            }
        """)
        main_layout.addWidget(title_label)
        
        # شريط المعلومات
        info_layout = QHBoxLayout()
        
        self.folder_label = QLabel(f"📁 المجلد: {self.reports_folder}")
        self.folder_label.setStyleSheet(self.get_info_label_style("#3498db"))
        info_layout.addWidget(self.folder_label)
        
        self.projects_count_label = QLabel("📊 المشاريع: 0")
        self.projects_count_label.setStyleSheet(self.get_info_label_style("#27ae60"))
        info_layout.addWidget(self.projects_count_label)
        
        self.status_label = QLabel("🔄 جاري المراقبة...")
        self.status_label.setStyleSheet(self.get_info_label_style("#f39c12"))
        info_layout.addWidget(self.status_label)
        
        main_layout.addLayout(info_layout)
        
        # المحتوى الرئيسي
        content_layout = QHBoxLayout()
        
        # القائمة الجانبية (المشاريع)
        left_panel_layout = QVBoxLayout()
        
        projects_title = QLabel("📋 المشاريع")
        projects_title.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        left_panel_layout.addWidget(projects_title)
        
        self.projects_tree = QTreeWidget()
        self.projects_tree.setHeaderLabels(["المشروع"])
        self.projects_tree.itemDoubleClicked.connect(self.on_project_selected)
        self.projects_tree.setStyleSheet(self.get_tree_style())
        left_panel_layout.addWidget(self.projects_tree)
        
        refresh_btn = QPushButton("🔄 تحديث")
        refresh_btn.setMinimumHeight(40)
        refresh_btn.setStyleSheet(self.get_button_style("#3498db"))
        refresh_btn.clicked.connect(self.refresh_reports)
        left_panel_layout.addWidget(refresh_btn)
        
        left_panel = QFrame()
        left_panel.setLayout(left_panel_layout)
        left_panel.setMaximumWidth(400)
        left_panel.setStyleSheet("background-color: #ecf0f1; border-radius: 10px; padding: 10px;")
        
        # اللوحة الرئيسية
        right_panel_layout = QVBoxLayout()
        
        self.data_title = QLabel("📊 بيانات المشروع")
        self.data_title.setFont(QFont("Arial", 15, QFont.Weight.Bold))
        self.data_title.setStyleSheet("color: #000000; background-color: #d0d0d0; padding: 12px; border-radius: 5px;")
        right_panel_layout.addWidget(self.data_title)
        
        # شريط الفلاتر
        filter_layout = QHBoxLayout()
        
        # تسميات الفلاتر
        category_label = QLabel("التصنيف:")
        category_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        category_label.setStyleSheet("color: #000000; background-color: #e0e0e0; padding: 8px; border-radius: 3px;")
        filter_layout.addWidget(category_label)
        
        self.category_filter = QComboBox()
        self.category_filter.addItem("الكل")
        self.category_filter.currentTextChanged.connect(self.apply_filters)
        self.category_filter.setMinimumHeight(40)
        self.category_filter.setMinimumWidth(250)
        self.category_filter.setMaximumWidth(350)
        self.category_filter.setStyleSheet("""
            QComboBox {
                background-color: #ffffff;
                color: #000000;
                border: 2px solid #000000;
                border-radius: 5px;
                padding: 8px;
                font-size: 13px;
                font-weight: bold;
                min-width: 250px;
            }
            QComboBox:hover {
                background-color: #f5f5f5;
                border: 2px solid #2980b9;
            }
            QComboBox::drop-down {
                border: none;
                background-color: #2980b9;
            }
            QComboBox QAbstractItemView {
                background-color: #ffffff;
                color: #000000;
                border: 2px solid #000000;
                selection-background-color: #2980b9;
                selection-color: #ffffff;
                padding: 5px;
                min-width: 300px;
            }
        """)
        filter_layout.addWidget(self.category_filter)
        
        search_label = QLabel("البحث عن عنصر:")
        search_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        search_label.setStyleSheet("color: #000000; background-color: #e0e0e0; padding: 8px; border-radius: 3px;")
        filter_layout.addWidget(search_label)
        
        self.item_search = QLineEdit()
        self.item_search.setPlaceholderText("اكتب اسم العنصر...")
        self.item_search.textChanged.connect(self.apply_filters)
        self.item_search.setMinimumHeight(40)
        self.item_search.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff;
                color: #000000;
                border: 2px solid #000000;
                border-radius: 5px;
                padding: 8px;
                font-size: 13px;
                font-weight: bold;
            }
            QLineEdit:focus {
                border: 2px solid #2980b9;
                background-color: #f0f8ff;
            }
            QLineEdit::placeholder {
                color: #888888;
            }
        """)
        filter_layout.addWidget(self.item_search)
        
        # زر حركة العنصر
        self.item_movement_btn = QPushButton("📈 حركة العنصر")
        self.item_movement_btn.setMinimumHeight(40)
        self.item_movement_btn.setMaximumWidth(150)
        self.item_movement_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #7f8c8d;
            }
        """)
        self.item_movement_btn.clicked.connect(self.show_item_movements)
        self.item_movement_btn.setEnabled(False)
        filter_layout.addWidget(self.item_movement_btn)
        
        filter_layout.addStretch()
        right_panel_layout.addLayout(filter_layout)
        
        # جدول البيانات
        self.inventory_table = QTableWidget()
        self.inventory_table.setStyleSheet(self.get_table_style())
        self.inventory_table.setAlternatingRowColors(True)
        self.inventory_table.setSortingEnabled(True)
        self.inventory_table.setColumnCount(0)
        self.inventory_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # تعطيل التعديل
        self.inventory_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.inventory_table.itemSelectionChanged.connect(self.on_item_selected)
        right_panel_layout.addWidget(self.inventory_table, 1)
        
        right_panel = QFrame()
        right_panel.setLayout(right_panel_layout)
        right_panel.setStyleSheet("background-color: #f8f9fa; border-radius: 10px; padding: 10px;")
        
        # إضافة اللوحات
        content_layout.addWidget(left_panel, 1)
        content_layout.addWidget(right_panel, 2)
        main_layout.addLayout(content_layout, 1)
        
        # شريط الأزرار السفلي
        button_layout = QHBoxLayout()
        
        open_folder_btn = QPushButton("📁 فتح المجلد")
        open_folder_btn.setMinimumHeight(45)
        open_folder_btn.setStyleSheet(self.get_button_style("#27ae60"))
        open_folder_btn.clicked.connect(self.open_folder)
        button_layout.addWidget(open_folder_btn)
        
        export_btn = QPushButton("💾 تصدير")
        export_btn.setMinimumHeight(45)
        export_btn.setStyleSheet(self.get_button_style("#9b59b6"))
        export_btn.clicked.connect(self.export_data)
        button_layout.addWidget(export_btn)
        
        delete_btn = QPushButton("🗑️ حذف المشروع")
        delete_btn.setMinimumHeight(45)
        delete_btn.setStyleSheet(self.get_button_style("#e74c3c"))
        delete_btn.clicked.connect(self.delete_report)
        button_layout.addWidget(delete_btn)
        
        self.transactions_btn = QPushButton("📊 عرض جميع الحركات")
        self.transactions_btn.setMinimumHeight(45)
        self.transactions_btn.setStyleSheet(self.get_button_style("#3498db"))
        self.transactions_btn.clicked.connect(self.show_all_transactions)
        self.transactions_btn.setEnabled(False)
        button_layout.addWidget(self.transactions_btn)
        
        main_layout.addLayout(button_layout)
    
    @staticmethod
    def get_info_label_style(bg_color):
        return f"""
            QLabel {{
                background-color: {bg_color};
                color: white;
                padding: 10px 15px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
            }}
        """
    
    @staticmethod
    def get_button_style(bg_color):
        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: white;
                font-weight: bold;
                font-size: 12px;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }}
            QPushButton:hover {{
                opacity: 0.8;
            }}
        """
    
    @staticmethod
    def get_tree_style():
        return """
            QTreeWidget {
                background-color: #ffffff;
                gridline-color: #cccccc;
                border: 2px solid #999999;
                border-radius: 5px;
                font-size: 14px;
                alternate-background-color: #f5f5f5;
            }
            QHeaderView::section {
                background-color: #1a1a1a !important;
                color: #ffffff !important;
                padding: 14px !important;
                border: 2px solid #000000 !important;
                font-weight: bold !important;
                font-size: 14px !important;
                height: 45px !important;
            }
            QTreeWidget::item {
                padding: 10px !important;
                border-bottom: 1px solid #dddddd;
                color: #000000 !important;
                font-size: 14px !important;
                height: 38px !important;
                font-weight: 500;
            }
            QTreeWidget::item:hover {
                background-color: #d4e6f1 !important;
                color: #000000 !important;
            }
            QTreeWidget::item:selected {
                background-color: #2980b9 !important;
                color: #ffffff !important;
                font-weight: bold !important;
            }
        """
    
    @staticmethod
    def get_table_style():
        return """
            QTableWidget {
                gridline-color: #999999;
                background-color: #ffffff;
                border: 2px solid #999999;
                border-radius: 5px;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #1a1a1a !important;
                color: #ffffff !important;
                padding: 14px !important;
                border: 2px solid #000000 !important;
                font-weight: bold !important;
                font-size: 14px !important;
                height: 50px !important;
            }
            QTableWidget::item {
                padding: 12px !important;
                border: 1px solid #cccccc !important;
                color: #000000 !important;
                font-size: 14px !important;
                height: 38px !important;
                font-weight: 500;
            }
            QTableWidget::item:alternate {
                background-color: #f0f0f0;
            }
            QTableWidget::item:hover {
                background-color: #e6f2ff !important;
                color: #000000 !important;
            }
            QTableWidget::item:selected {
                background-color: #2980b9 !important;
                color: #ffffff !important;
                font-weight: bold !important;
            }
        """
    
    def start_monitoring(self):
        """بدء المراقبة"""
        self.monitor = ReportMonitor(self.reports_folder)
        self.monitor.report_found.connect(self.on_report_found)
        self.monitor.reports_updated.connect(self.on_reports_updated)
        self.monitor.start()
    
    def on_report_found(self, file_path):
        """عند استقبال تقرير جديد"""
        filename = os.path.basename(file_path)
        self.status_label.setText(f"✅ تقرير جديد: {filename}")
    
    def on_reports_updated(self, reports_list):
        """تحديث قائمة التقارير"""
        self.update_projects_tree(reports_list)
    
    def update_projects_tree(self, reports_list):
        """تحديث قائمة المشاريع"""
        self.projects_tree.clear()
        self.reports_data = defaultdict(list)
        
        # تجميع التقارير حسب المشروع
        for file_path in reports_list:
            try:
                analyzer = ReportAnalyzer(file_path)
                project_name = analyzer.project_name
                self.reports_data[project_name].append(file_path)
            except:
                pass
        
        # عرض المشاريع
        for project_name in sorted(self.reports_data.keys()):
            item = QTreeWidgetItem()
            item.setText(0, f"📊 {project_name}")
            item.setData(0, Qt.ItemDataRole.UserRole, project_name)
            self.projects_tree.addTopLevelItem(item)
        
        self.projects_count_label.setText(f"📊 المشاريع: {len(self.reports_data)}")
        self.status_label.setText("✅ تم التحديث")
    
    def on_project_selected(self, item, column):
        """عند اختيار مشروع"""
        project_name = item.data(0, Qt.ItemDataRole.UserRole)
        
        if project_name and project_name in self.reports_data:
            self.current_project = project_name
            # استخدام آخر تقرير للمشروع
            file_path = self.reports_data[project_name][-1]
            self.load_project_data(file_path)
    
    def load_project_data(self, file_path):
        """تحميل بيانات المشروع"""
        try:
            self.current_analyzer = ReportAnalyzer(file_path)
            self.gap_dates = self.current_analyzer.check_date_continuity()
            
            # تحديث عنوان المشروع
            self.data_title.setText(f"📊 بيانات المشروع: {self.current_analyzer.project_name}")
            
            # تحديث فلاتر التصنيفات
            categories = self.current_analyzer.get_categories()
            self.category_filter.blockSignals(True)
            self.category_filter.clear()
            self.category_filter.addItem("الكل")
            for cat in categories:
                self.category_filter.addItem(str(cat))
            self.category_filter.blockSignals(False)
            
            # تفعيل زر الحركات إذا كانت هناك بيانات
            self.transactions_btn.setEnabled(not self.current_analyzer.all_transactions_df.empty)
            
            # عرض البيانات
            self.display_inventory_data()
            
            self.status_label.setText(f"✅ تم تحميل المشروع: {self.current_project}")
            
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في تحميل البيانات:\n{str(e)}")
    
    def display_inventory_data(self):
        """عرض بيانات المخزون"""
        if not self.current_analyzer:
            return
        
        df = self.current_analyzer.get_inventory_data()
        
        if df.empty:
            self.inventory_table.setRowCount(0)
            return
        
        self.inventory_table.setRowCount(len(df))
        self.inventory_table.setColumnCount(len(df.columns) + 1)  # عمود إضافي للترقيم
        
        # رؤوس الأعمدة مع عمود الترقيم
        headers = ["#"] + df.columns.astype(str).tolist()
        self.inventory_table.setHorizontalHeaderLabels(headers)
        
        # ضبط عرض عمود الترقيم
        self.inventory_table.setColumnWidth(0, 50)
        
        for row in range(len(df)):
            # عمود الترقيم
            row_number = QTableWidgetItem()
            row_number.setData(Qt.ItemDataRole.DisplayRole, row + 1)
            row_number.setData(Qt.ItemDataRole.UserRole, row + 1)
            row_number.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            row_number.setBackground(QColor("#e8e8e8"))
            row_number.setForeground(QColor("#000000"))
            self.inventory_table.setItem(row, 0, row_number)
            
            # البيانات
            for col in range(len(df.columns)):
                value = str(df.iloc[row, col])
                item = QTableWidgetItem(value)
                self.inventory_table.setItem(row, col + 1, item)
            
            # زيادة ارتفاع الصف
            self.inventory_table.setRowHeight(row, 40)
    
    def apply_filters(self):
        """تطبيق الفلاتر"""
        if not self.current_analyzer:
            return
        
        category = self.category_filter.currentText()
        search_text = self.item_search.text().lower()
        
        # الحصول على البيانات الأصلية
        df = self.current_analyzer.get_inventory_data()
        
        # تطبيق فلتر التصنيف
        if category != "الكل":
            df = df[df['التصنيف'] == category]
        
        # تطبيق فلتر البحث
        if search_text:
            if 'اسم_العنصر' in df.columns:
                df = df[df['اسم_العنصر'].str.lower().str.contains(search_text)]
        
        # عرض البيانات المفلترة مع الترقيم
        self.inventory_table.setRowCount(len(df))
        self.inventory_table.setColumnCount(len(df.columns) + 1)  # عمود إضافي للترقيم
        
        # رؤوس الأعمدة مع عمود الترقيم
        headers = ["#"] + df.columns.astype(str).tolist()
        self.inventory_table.setHorizontalHeaderLabels(headers)
        
        # ضبط عرض عمود الترقيم
        self.inventory_table.setColumnWidth(0, 50)
        
        for row in range(len(df)):
            # عمود الترقيم
            row_number = QTableWidgetItem()
            row_number.setData(Qt.ItemDataRole.DisplayRole, row + 1)
            row_number.setData(Qt.ItemDataRole.UserRole, row + 1)
            row_number.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            row_number.setBackground(QColor("#e8e8e8"))
            row_number.setForeground(QColor("#000000"))
            self.inventory_table.setItem(row, 0, row_number)
            
            # البيانات
            for col in range(len(df.columns)):
                value = str(df.iloc[row, col])
                item = QTableWidgetItem(value)
                self.inventory_table.setItem(row, col + 1, item)
            
            # زيادة ارتفاع الصف
            self.inventory_table.setRowHeight(row, 40)
    
    def open_folder(self):
        """فتح مجلد التقارير"""
        if sys.platform == "win32":
            os.startfile(self.reports_folder)
        elif sys.platform == "darwin":
            os.system(f"open {self.reports_folder}")
        else:
            os.system(f"xdg-open {self.reports_folder}")
    
    def export_data(self):
        """تصدير البيانات (الصفوف المحددة أو كل البيانات)"""
        if not self.current_project:
            QMessageBox.warning(self, "تحذير", "لم يتم اختيار مشروع")
            return
        
        # الحصول على الصفوف المحددة
        selected_rows = self.inventory_table.selectedIndexes()
        selected_row_numbers = set(index.row() for index in selected_rows)
        
        file_path, _ = QFileDialog.getSaveFileName(self, "حفظ البيانات", "", "ملفات Excel (*.xlsx)")
        if file_path:
            try:
                df = self.current_analyzer.get_inventory_data()
                
                # إذا كانت هناك صفوف محددة، صدّرها فقط
                if selected_row_numbers:
                    df_export = df.iloc[list(selected_row_numbers)].reset_index(drop=True)
                    message = f"تم تصدير {len(selected_row_numbers)} صفوف"
                else:
                    df_export = df
                    message = "تم تصدير جميع البيانات"
                
                df_export.to_excel(file_path, index=False)
                QMessageBox.information(self, "نجح", f"{message} إلى:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "خطأ", str(e))
    
    def delete_report(self):
        """حذف التقرير"""
        if not self.current_project:
            QMessageBox.warning(self, "تحذير", "لم يتم اختيار مشروع")
            return
        
        file_path = self.reports_data[self.current_project][-1]
        reply = QMessageBox.question(self, "تأكيد الحذف", 
                                    f"حذف:\n{os.path.basename(file_path)}?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                os.remove(file_path)
                self.current_project = None
                self.current_analyzer = None
                self.refresh_reports()
                QMessageBox.information(self, "نجح", "تم الحذف")
            except Exception as e:
                QMessageBox.critical(self, "خطأ", str(e))
    
    def on_item_selected(self):
        """عند اختيار عنصر من الجدول"""
        selected = self.inventory_table.selectedItems()
        if selected:
            self.item_movement_btn.setEnabled(True)
        else:
            self.item_movement_btn.setEnabled(False)
    
    def show_item_movements(self):
        """عرض حركات العنصر المختار"""
        selected = self.inventory_table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "تحذير", "اختر عنصر أولاً")
            return
        
        # الحصول على رقم الصف
        row = selected[0].row()
        
        # الحصول على اسم العنصر
        item_name = None
        for col in range(self.inventory_table.columnCount()):
            col_header = self.inventory_table.horizontalHeaderItem(col).text()
            if col_header in ['اسم_العنصر', 'اسم العنصر', 'العنصر']:
                item_name = self.inventory_table.item(row, col).text()
                break
        
        if not item_name:
            QMessageBox.warning(self, "تحذير", "لم يتم العثور على اسم العنصر")
            return
        
        if not self.current_analyzer or self.current_analyzer.all_transactions_df.empty:
            QMessageBox.warning(self, "تحذير", "لا توجد حركات للعنصر")
            return
        
        # تصفية الحركات للعنصر المختار
        transactions_df = self.current_analyzer.all_transactions_df.copy()
        
        # البحث عن عمود اسم العنصر
        for col in ['اسم_العنصر', 'اسم العنصر', 'العنصر']:
            if col in transactions_df.columns:
                transactions_df = transactions_df[transactions_df[col] == item_name]
                break
        
        if transactions_df.empty:
            QMessageBox.warning(self, "تحذير", f"لا توجد حركات للعنصر: {item_name}")
            return
        
        # إنشاء نافذة جديدة
        window = TransactionsViewer(
            transactions_df,
            f"{self.current_analyzer.project_name} - {item_name}"
        )
        # حفظ reference للنافذة لمنع حذفها من الذاكرة
        self.open_windows.append(window)
        window.show()
        
        # تنظيف النوافذ المُغلقة
        self.open_windows = [w for w in self.open_windows if w.isVisible()]
    
    def show_all_transactions(self):
        """عرض جميع الحركات"""
        if not self.current_analyzer or self.current_analyzer.all_transactions_df.empty:
            QMessageBox.warning(self, "تحذير", "لا توجد حركات للعرض")
            return
        
        # إغلاق النافذة السابقة إن وجدت
        if self.transactions_window and self.transactions_window.isVisible():
            self.transactions_window.close()
        
        # إنشاء نافذة جديدة
        self.transactions_window = TransactionsViewer(
            self.current_analyzer.all_transactions_df.copy(),
            self.current_analyzer.project_name
        )
        # حفظ reference
        self.open_windows.append(self.transactions_window)
        self.transactions_window.show()
        
        # تنظيف النوافذ المُغلقة
        self.open_windows = [w for w in self.open_windows if w.isVisible()]
    
    def refresh_reports(self):
        """تحديث التقارير"""
        self.status_label.setText("🔄 جاري التحديث...")
        reports_list = sorted(list(Path(self.reports_folder).glob("*.xlsx")), 
                             key=lambda x: x.stat().st_mtime, reverse=True)
        self.update_projects_tree([str(f) for f in reports_list])
    
    def closeEvent(self, event):
        """عند الإغلاق"""
        self.monitor.stop()
        self.monitor.wait()
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
    
    window = AdvancedReportViewerV2()
    window.showMaximized()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
