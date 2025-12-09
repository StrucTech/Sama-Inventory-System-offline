# -*- coding: utf-8 -*-
"""
واجهة فلتر التقرير بالتاريخ
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QFormLayout, QFrame, QMessageBox,
                           QDateEdit, QTextEdit)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from datetime import datetime as dt, timedelta
from report_manager import ReportManager
from excel_manager import excel_manager
import os


class ReportFilterDialog(QDialog):
    """واجهة فلتر التقرير بالتاريخ"""
    
    def __init__(self, project_name, parent=None):
        super().__init__(parent)
        self.project_name = project_name
        self.report_manager = ReportManager(excel_manager)
        self.setup_ui()
        self.setup_styles()
        self.load_last_report_info()
    
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        self.setWindowTitle("تصدير تقرير للمكتب")
        self.setModal(True)
        self.resize(800, 650)
        self.center_on_screen()
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        # التخطيط الرئيسي
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # العنوان
        title_label = QLabel("تصدير تقرير للمكتب")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # معلومات المشروع
        project_label = QLabel(f"المشروع: {self.project_name}")
        project_label.setObjectName("project_info")
        project_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(project_label)
        
        # معلومات التقرير السابق
        self.last_report_label = QLabel("جاري تحميل معلومات التقرير السابق...")
        self.last_report_label.setObjectName("last_report_info")
        self.last_report_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.last_report_label.setWordWrap(True)
        main_layout.addWidget(self.last_report_label)
        
        # إطار الفلتر
        filter_frame = QFrame()
        filter_frame.setObjectName("filter_frame")
        filter_frame.setFrameStyle(QFrame.Shape.Box)
        form_layout = QFormLayout(filter_frame)
        form_layout.setSpacing(15)
        
        # تاريخ البداية
        self.start_date = QDateEdit()
        self.start_date.setObjectName("date_input")
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate().addDays(-30))  # آخر 30 يوم
        form_layout.addRow("من تاريخ:", self.start_date)
        
        # تاريخ النهاية
        self.end_date = QDateEdit()
        self.end_date.setObjectName("date_input")
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())
        form_layout.addRow("إلى تاريخ:", self.end_date)
        
        main_layout.addWidget(filter_frame)
        
        # منطقة المعاينة
        preview_label = QLabel("معاينة نطاق التقرير:")
        preview_label.setObjectName("section_label")
        main_layout.addWidget(preview_label)
        
        self.preview_text = QTextEdit()
        self.preview_text.setObjectName("preview_text")
        self.preview_text.setMaximumHeight(80)
        self.preview_text.setReadOnly(True)
        main_layout.addWidget(self.preview_text)
        
        # تحديث المعاينة عند تغيير التاريخ
        self.start_date.dateChanged.connect(self.update_preview)
        self.end_date.dateChanged.connect(self.update_preview)
        self.update_preview()
        
        # نوع التقرير
        report_type_label = QLabel("نوع التقرير:")
        report_type_label.setObjectName("section_label")
        main_layout.addWidget(report_type_label)
        
        # أزرار نوع التقرير
        report_buttons_layout = QHBoxLayout()
        
        # زر التقرير الشامل
        comprehensive_btn = QPushButton("تقرير شامل (جميع البيانات)")
        comprehensive_btn.setObjectName("primary_button")
        comprehensive_btn.clicked.connect(self.export_comprehensive_report)
        report_buttons_layout.addWidget(comprehensive_btn)
        
        # زر التقرير المفلتر
        filtered_btn = QPushButton("تقرير مفلتر (حسب التاريخ)")
        filtered_btn.setObjectName("secondary_button")
        filtered_btn.clicked.connect(self.export_filtered_report)
        report_buttons_layout.addWidget(filtered_btn)
        
        main_layout.addLayout(report_buttons_layout)
        
        # فاصل
        main_layout.addWidget(QFrame())
        
        # الأزرار
        buttons_layout = QHBoxLayout()
        
        # زر التصدير

        
        # زر الإلغاء
        cancel_btn = QPushButton("إلغاء")
        cancel_btn.setObjectName("cancel_button")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        main_layout.addLayout(buttons_layout)
    
    def center_on_screen(self):
        """توسيط النافذة على الشاشة"""
        from PyQt6.QtWidgets import QApplication
        
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
    
    def load_last_report_info(self):
        """تحميل معلومات التقرير السابق"""
        try:
            # البحث عن آخر تقرير في مجلد التقارير
            reports_path = "reports"
            if not os.path.exists(reports_path):
                self.last_report_label.setText("لا توجد تقارير سابقة")
                return
            
            # البحث عن ملفات التقارير للمشروع الحالي (شامل ومفلتر)
            report_files = [f for f in os.listdir(reports_path) 
                           if (f.startswith(f"تقرير_شامل_{self.project_name}") or 
                               f.startswith(f"تقرير_مفلتر_{self.project_name}")) and f.endswith('.xlsx')]
            
            if not report_files:
                self.last_report_label.setText("لا توجد تقارير سابقة لهذا المشروع")
                return
            
            # أحدث ملف تقرير
            latest_file = max(report_files, key=lambda f: os.path.getctime(os.path.join(reports_path, f)))
            file_path = os.path.join(reports_path, latest_file)
            
            # استخراج التاريخ من اسم الملف أو من تاريخ الإنشاء
            creation_time = dt.fromtimestamp(os.path.getctime(file_path))
            
            # تحديد نوع التقرير
            report_type = "مفلتر" if "تقرير_مفلتر_" in latest_file else "شامل"
            
            # محاولة قراءة التقرير لمعرفة نطاق التواريخ
            try:
                import pandas as pd
                
                # محاولة قراءة أوراق مختلفة حسب نوع التقرير
                sheet_names = ['جميع الحركات', 'الحركات المفلترة', 'معلومات التقرير']
                df = None
                
                for sheet_name in sheet_names:
                    try:
                        df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')
                        if not df.empty:
                            break
                    except:
                        continue
                
                # إذا كان تقرير مفلتر، محاولة قراءة التواريخ من معلومات التقرير
                if report_type == "مفلتر":
                    try:
                        info_df = pd.read_excel(file_path, sheet_name='معلومات التقرير', engine='openpyxl')
                        if not info_df.empty:
                            # البحث عن التواريخ في معلومات التقرير
                            info_text = str(info_df.iloc[:, 0].tolist())
                            import re
                            dates = re.findall(r'\d{4}-\d{2}-\d{2}', info_text)
                            if len(dates) >= 2:
                                self.last_report_label.setText(
                                    f"التقرير السابق ({report_type}) كان من {dates[0]} "
                                    f"إلى {dates[1]}\n"
                                    f"تم إنشاؤه في: {creation_time.strftime('%Y-%m-%d %H:%M')}"
                                )
                                return
                    except:
                        pass
                
                # محاولة قراءة التواريخ من بيانات الحركات
                if df is not None and not df.empty and 'التاريخ' in df.columns:
                    # تحويل التواريخ
                    df['التاريخ'] = pd.to_datetime(df['التاريخ'], errors='coerce')
                    min_date = df['التاريخ'].min()
                    max_date = df['التاريخ'].max()
                    
                    if pd.notna(min_date) and pd.notna(max_date):
                        self.last_report_label.setText(
                            f"التقرير السابق ({report_type}) كان من {min_date.strftime('%Y-%m-%d')} "
                            f"إلى {max_date.strftime('%Y-%m-%d')}\n"
                            f"تم إنشاؤه في: {creation_time.strftime('%Y-%m-%d %H:%M')}"
                        )
                    else:
                        self.last_report_label.setText(
                            f"آخر تقرير ({report_type}): {creation_time.strftime('%Y-%m-%d %H:%M')}"
                        )
                else:
                    self.last_report_label.setText(
                        f"آخر تقرير ({report_type}): {creation_time.strftime('%Y-%m-%d %H:%M')}"
                    )
                    
            except Exception as e:
                self.last_report_label.setText(
                    f"آخر تقرير ({report_type}): {creation_time.strftime('%Y-%m-%d %H:%M')}"
                )
                
        except Exception as e:
            self.last_report_label.setText("خطأ في تحميل معلومات التقرير السابق")
    
    def update_preview(self):
        """تحديث معاينة نطاق التقرير"""
        start = self.start_date.date().toString("yyyy-MM-dd")
        end = self.end_date.date().toString("yyyy-MM-dd")
        
        days_diff = self.start_date.date().daysTo(self.end_date.date())
        
        preview_text = f"سيشمل التقرير الفترة من {start} إلى {end}\n"
        preview_text += f"إجمالي الأيام: {days_diff + 1} يوم"
        
        if days_diff < 0:
            preview_text += "\n⚠️ تحذير: تاريخ البداية أكبر من تاريخ النهاية"
        elif days_diff > 365:
            preview_text += "\n⚠️ تحذير: الفترة أكثر من سنة"
        
        self.preview_text.setText(preview_text)
    
    def export_comprehensive_report(self):
        """تصدير تقرير شامل مع اختيار مكان الحفظ"""
        try:
            from PyQt6.QtWidgets import QFileDialog
            
            # اختيار مكان حفظ الملف
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            default_filename = f"تقرير_شامل_{self.project_name}_{timestamp}.xlsx"
            
            filepath, _ = QFileDialog.getSaveFileName(
                self,
                "حفظ التقرير الشامل",
                default_filename,
                "Excel files (*.xlsx);;All files (*.*)"
            )
            
            if not filepath:
                return
                
            self.setEnabled(False)
            
            # إنشاء التقرير الشامل مع استخدام المسار المختار
            success = self.create_comprehensive_report_at_path(filepath)
            
            self.setEnabled(True)
            
            if success:
                # تحديث معلومات التقرير السابق
                self.load_last_report_info()
                
                QMessageBox.information(
                    self, "نجح", 
                    f"تم تصدير التقرير الشامل بنجاح!\n\n"
                    f"يتضمن جميع البيانات والإحصائيات\n"
                    f"مسار الملف:\n{filepath}"
                )
                self.accept()
            else:
                QMessageBox.warning(self, "خطأ", "فشل في إنشاء التقرير الشامل")
                
        except Exception as e:
            self.setEnabled(True)
            QMessageBox.critical(self, "خطأ", f"خطأ في معاينة التقرير: {str(e)}")
    
    def create_comprehensive_report_at_path(self, filepath):
        """إنشاء تقرير شامل في المسار المحدد"""
        try:
            import pandas as pd
            
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                
                # 1. ملخص المخزون الحالي
                inventory_df = self.report_manager.excel_manager.get_inventory_summary(self.project_name)
                if not inventory_df.empty:
                    inventory_df.to_excel(writer, sheet_name='المخزون الحالي', index=False)
                
                # 2. جميع الحركات التفصيلية
                project_file = os.path.join("projects", f"{self.project_name}_Transactions.xlsx")
                if os.path.exists(project_file):
                    transactions_df = pd.read_excel(project_file, engine='openpyxl')
                    
                    # ترتيب الحركات حسب التاريخ (الأحدث أولاً)
                    transactions_df['التاريخ'] = pd.to_datetime(transactions_df['التاريخ'])
                    transactions_df = transactions_df.sort_values('التاريخ', ascending=False)
                    
                    # تنسيق التاريخ للعرض
                    transactions_df['التاريخ'] = transactions_df['التاريخ'].dt.strftime('%Y-%m-%d %H:%M:%S')
                    
                    transactions_df.to_excel(writer, sheet_name='جميع الحركات', index=False)
                    
                    # 3. تقرير حركات الدخول
                    incoming_df = transactions_df[transactions_df['نوع_العملية'] == 'دخول'].copy()
                    if not incoming_df.empty:
                        incoming_df.to_excel(writer, sheet_name='حركات الدخول', index=False)
                    
                    # 4. تقرير حركات الخروج
                    outgoing_df = transactions_df[transactions_df['نوع_العملية'] == 'خروج'].copy()
                    if not outgoing_df.empty:
                        outgoing_df.to_excel(writer, sheet_name='حركات الخروج', index=False)
                
                # 5. إحصائيات المشروع
                stats = self.report_manager.get_project_statistics(self.project_name)
                if stats:
                    stats_df = pd.DataFrame([stats]).T
                    stats_df.columns = ['القيمة']
                    stats_df.index.name = 'الإحصائية'
                    stats_df.to_excel(writer, sheet_name='إحصائيات المشروع')
                
                # 6. ملخص عناصر المشروع
                project_items = self.report_manager.excel_manager.get_all_items(self.project_name)
                if not project_items.empty:
                    project_items.to_excel(writer, sheet_name='عناصر المشروع', index=False)
                
                # 7. تقرير منفصل حسب التصنيف
                if not inventory_df.empty and 'التصنيف' in inventory_df.columns:
                    categories = inventory_df['التصنيف'].unique()
                    for category in categories:
                        category_data = inventory_df[inventory_df['التصنيف'] == category]
                        sheet_name = f"تصنيف_{category}"[:31]  # Excel sheet name limit
                        category_data.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # تنسيق جميع الأوراق
                workbook = writer.book
                for sheet_name in writer.sheets:
                    sheet = writer.sheets[sheet_name]
                    self.report_manager._format_excel_sheet(sheet, workbook)
            
            return True
            
        except Exception as e:
            print(f"خطأ في إنشاء التقرير الشامل: {str(e)}")
            return False
    
    def create_filtered_report_at_path(self, filepath, start_date, end_datetime):
        """إنشاء تقرير مفلتر في المسار المحدد"""
        try:
            import pandas as pd
            
            # تحويل التواريخ
            if isinstance(start_date, str):
                start_date = pd.to_datetime(start_date)
            elif hasattr(start_date, 'date') and callable(start_date.date):
                start_date = pd.to_datetime(start_date.date())
            elif not isinstance(start_date, (pd.Timestamp, dt)):
                start_date = pd.to_datetime(start_date)
            
            if isinstance(end_datetime, str):
                end_datetime = pd.to_datetime(end_datetime)
            elif hasattr(end_datetime, 'date') and callable(end_datetime.date):
                end_datetime = pd.to_datetime(end_datetime.date())
            elif not isinstance(end_datetime, (pd.Timestamp, dt)):
                end_datetime = pd.to_datetime(end_datetime)
            
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                
                # 1. معلومات الفلتر
                filter_info = pd.DataFrame({
                    'المعلومة': ['المشروع', 'من تاريخ', 'إلى تاريخ', 'تاريخ إنشاء التقرير'],
                    'القيمة': [
                        self.project_name,
                        start_date.strftime('%Y-%m-%d'),
                        end_datetime.strftime('%Y-%m-%d'),
                        dt.now().strftime('%Y-%m-%d %H:%M:%S')
                    ]
                })
                filter_info.to_excel(writer, sheet_name='معلومات التقرير', index=False)
                
                # 2. الحركات المفلترة
                project_file = os.path.join("projects", f"{self.project_name}_Transactions.xlsx")
                if os.path.exists(project_file):
                    all_transactions = pd.read_excel(project_file, engine='openpyxl')
                    
                    if not all_transactions.empty:
                        # فلترة البيانات حسب التاريخ
                        all_transactions['التاريخ'] = pd.to_datetime(all_transactions['التاريخ'])
                        filtered_transactions = all_transactions[
                            (all_transactions['التاريخ'] >= start_date) & 
                            (all_transactions['التاريخ'] <= end_datetime)
                        ].copy()
                        
                        if not filtered_transactions.empty:
                            # ترتيب الحركات حسب التاريخ (الأحدث أولاً)
                            filtered_transactions = filtered_transactions.sort_values('التاريخ', ascending=False)
                            
                            # تنسيق التاريخ للعرض
                            filtered_transactions['التاريخ'] = filtered_transactions['التاريخ'].dt.strftime('%Y-%m-%d %H:%M:%S')
                            
                            # جميع الحركات المفلترة
                            filtered_transactions.to_excel(writer, sheet_name='الحركات المفلترة', index=False)
                            
                            # حركات الدخول المفلترة
                            incoming_filtered = filtered_transactions[filtered_transactions['نوع_العملية'] == 'دخول']
                            if not incoming_filtered.empty:
                                incoming_filtered.to_excel(writer, sheet_name='دخول مفلتر', index=False)
                            
                            # حركات الخروج المفلترة
                            outgoing_filtered = filtered_transactions[filtered_transactions['نوع_العملية'] == 'خروج']
                            if not outgoing_filtered.empty:
                                outgoing_filtered.to_excel(writer, sheet_name='خروج مفلتر', index=False)
                            
                            # إحصائيات الفترة
                            period_stats = self.get_period_statistics(filtered_transactions)
                            if period_stats:
                                stats_df = pd.DataFrame([period_stats]).T
                                stats_df.columns = ['القيمة']
                                stats_df.index.name = 'الإحصائية'
                                stats_df.to_excel(writer, sheet_name='إحصائيات الفترة')
                
                # تنسيق جميع الأوراق
                workbook = writer.book
                for sheet_name in writer.sheets:
                    sheet = writer.sheets[sheet_name]
                    self.report_manager._format_excel_sheet(sheet, workbook)
            
            return True
            
        except Exception as e:
            print(f"خطأ في إنشاء التقرير المفلتر: {str(e)}")
            return False
    
    def get_period_statistics(self, transactions_df):
        """حساب إحصائيات فترة محددة"""
        try:
            if transactions_df.empty:
                return {}
            
            stats = {
                'إجمالي عدد الحركات': len(transactions_df),
                'عدد حركات الدخول': len(transactions_df[transactions_df['نوع_العملية'] == 'دخول']),
                'عدد حركات الخروج': len(transactions_df[transactions_df['نوع_العملية'] == 'خروج']),
                'إجمالي كمية الدخول': transactions_df[transactions_df['نوع_العملية'] == 'دخول']['الكمية'].sum(),
                'إجمالي كمية الخروج': transactions_df[transactions_df['نوع_العملية'] == 'خروج']['الكمية'].sum(),
                'عدد العناصر المختلفة': transactions_df['اسم_العنصر'].nunique(),
                'عدد التصنيفات': transactions_df['التصنيف'].nunique() if 'التصنيف' in transactions_df.columns else 0
            }
            
            return stats
            
        except Exception as e:
            return {}
    
    def export_filtered_report(self):
        """تصدير التقرير المفلتر بالتاريخ مع اختيار مكان الحفظ"""
        try:
            from PyQt6.QtWidgets import QFileDialog
            
            # التحقق من صحة التواريخ
            if self.start_date.date() > self.end_date.date():
                QMessageBox.warning(self, "خطأ", "تاريخ البداية يجب أن يكون أقل من أو يساوي تاريخ النهاية")
                return
            
            # تحويل التواريخ للعرض
            qstart_date = self.start_date.date()
            qend_date = self.end_date.date()
            date_range = f"{qstart_date.toString('yyyy-MM-dd')}_إلى_{qend_date.toString('yyyy-MM-dd')}"
            
            # اختيار مكان حفظ الملف
            timestamp = dt.now().strftime('%Y%m%d_%H%M%S')
            default_filename = f"تقرير_مفلتر_{self.project_name}_{date_range}_{timestamp}.xlsx"
            
            filepath, _ = QFileDialog.getSaveFileName(
                self,
                "حفظ التقرير المفلتر",
                default_filename,
                "Excel files (*.xlsx);;All files (*.*)"
            )
            
            if not filepath:
                return
            
            # تحويل التواريخ (استخدام الاستيرادات الموجودة)
            from datetime import time, date
            
            # تحويل QDate إلى Python date
            qstart_date = self.start_date.date()
            qend_date = self.end_date.date()
            
            start_date = date(qstart_date.year(), qstart_date.month(), qstart_date.day())
            end_date = date(qend_date.year(), qend_date.month(), qend_date.day())
            
            # إضافة الوقت للتاريخ النهائي
            end_datetime = dt.combine(end_date, time(23, 59, 59))
            
            self.setEnabled(False)
            
            # إنشاء التقرير المفلتر مع استخدام المسار المختار
            success = self.create_filtered_report_at_path(filepath, start_date, end_datetime)
            
            self.setEnabled(True)
            
            if success:
                # تحديث معلومات التقرير السابق
                self.load_last_report_info()
                
                QMessageBox.information(
                    self, "نجح", 
                    f"تم تصدير التقرير المفلتر بنجاح!\n\n"
                    f"الفترة: من {start_date.strftime('%Y-%m-%d')} إلى {end_date.strftime('%Y-%m-%d')}\n"
                    f"مسار الملف:\n{filepath}"
                )
                self.accept()
            else:
                QMessageBox.warning(self, "خطأ", "فشل في إنشاء التقرير المفلتر")
                
        except Exception as e:
            self.setEnabled(True)
            QMessageBox.critical(self, "خطأ", f"خطأ في تصدير التقرير: {str(e)}")
    
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
        
        QLabel#last_report_info {
            font-size: 13px;
            color: #7f8c8d;
            background-color: #ffffff;
            border: 1px solid #bdc3c7;
            border-radius: 5px;
            padding: 10px;
            margin: 5px 0px;
        }
        
        QLabel#section_label {
            font-size: 14px;
            font-weight: bold;
            color: #34495e;
            padding: 5px 0px;
        }
        
        QFrame#filter_frame {
            background-color: white;
            border: 2px solid #bdc3c7;
            border-radius: 10px;
            padding: 20px;
        }
        
        QDateEdit#date_input {
            font-size: 14px;
            padding: 10px;
            border: 2px solid #bdc3c7;
            border-radius: 5px;
            background-color: white;
            color: #2c3e50;
            min-height: 20px;
        }
        
        QDateEdit#date_input:focus {
            border-color: #3498db;
        }
        
        QTextEdit#preview_text {
            font-size: 12px;
            border: 1px solid #bdc3c7;
            border-radius: 5px;
            background-color: #f8f9fa;
            color: #2c3e50;
            padding: 8px;
        }
        
        QPushButton#export_button {
            background-color: #27ae60;
            color: white;
            font-size: 14px;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            padding: 12px 20px;
            min-width: 120px;
        }
        
        QPushButton#export_button:hover {
            background-color: #229954;
        }
        
        QPushButton#export_button:pressed {
            background-color: #1e8449;
        }
        
        QPushButton#cancel_button {
            background-color: #95a5a6;
            color: white;
            font-size: 14px;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            padding: 12px 20px;
            min-width: 120px;
        }
        
        QPushButton#cancel_button:hover {
            background-color: #7f8c8d;
        }
        
        QPushButton#primary_button {
            background-color: #3498db;
            color: white;
            font-size: 14px;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            padding: 15px 25px;
            min-width: 200px;
        }
        
        QPushButton#primary_button:hover {
            background-color: #2980b9;
        }
        
        QPushButton#primary_button:pressed {
            background-color: #21618c;
        }
        
        QPushButton#secondary_button {
            background-color: #e74c3c;
            color: white;
            font-size: 14px;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            padding: 15px 25px;
            min-width: 200px;
        }
        
        QPushButton#secondary_button:hover {
            background-color: #c0392b;
        }
        
        QPushButton#secondary_button:pressed {
            background-color: #a93226;
        }
        """
        
        self.setStyleSheet(style)
    
    def showEvent(self, event):
        """إعادة تحميل معلومات التقرير عند إظهار النافذة"""
        super().showEvent(event)
        # إعادة تحميل معلومات التقرير السابق في كل مرة تُفتح النافذة
        self.load_last_report_info()
    
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
            background-color: #e74c3c;
            color: white;
            font-size: 10px;
            font-weight: bold;
            border: none;
            border-radius: 5px;
            padding: 6px 12px;
            min-width: 70px;
        }
        QMessageBox QPushButton:hover {
            background-color: #c0392b;
        }
        QMessageBox QPushButton:pressed {
            background-color: #a93226;
        }
        """
        QApplication.instance().setStyleSheet(QApplication.instance().styleSheet() + message_style)