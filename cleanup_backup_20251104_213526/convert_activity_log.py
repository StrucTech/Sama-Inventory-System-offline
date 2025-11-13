#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أداة تحويل Activity Log إلى الهيكل الجديد
تحويل آمن مع الحفاظ على البيانات الأصلية
"""

import re
import sys
import os
from datetime import datetime

# إضافة مسار المشروع للـ Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sheets.manager import SheetsManager

class ActivityLogConverter:
    def __init__(self, sheets_manager):
        self.sheets_manager = sheets_manager
        self.conversion_log = []
        
    def analyze_current_data(self):
        """تحليل البيانات الحالية لفهم التنسيقات المختلفة"""
        print("🔍 تحليل البيانات الحالية...")
        
        try:
            # قراءة البيانات الحالية
            current_data = self.sheets_manager.get_activity_log()
            
            analysis = {
                'total_records': len(current_data),
                'date_formats': set(),
                'operation_types': set(),
                'item_names': set(),
                'recipients': set(),
                'projects': set(),
                'parsing_issues': []
            }
            
            for i, record in enumerate(current_data):
                if len(record) >= 6:
                    date_time = record[0] if record[0] else ""
                    operation = record[1] if record[1] else ""
                    item_name = record[2] if record[2] else ""
                    quantity = record[3] if record[3] else ""
                    recipient = record[4] if record[4] else ""
                    details = record[5] if record[5] else ""
                    
                    # تحليل التاريخ
                    if date_time:
                        analysis['date_formats'].add(self._detect_date_format(date_time))
                    
                    # تحليل العمليات
                    if operation:
                        analysis['operation_types'].add(operation.strip())
                    
                    # تحليل أسماء العناصر
                    if item_name:
                        analysis['item_names'].add(item_name.strip())
                    
                    # تحليل المستلمين
                    if recipient:
                        analysis['recipients'].add(recipient.strip())
                    
                    # البحث عن أرقام المشاريع في التفاصيل
                    projects = self._extract_projects(details)
                    analysis['projects'].update(projects)
                    
                    # فحص المشاكل المحتملة
                    issues = self._check_parsing_issues(record, i)
                    analysis['parsing_issues'].extend(issues)
            
            return analysis
            
        except Exception as e:
            print(f"❌ خطأ في تحليل البيانات: {e}")
            return None
    
    def _detect_date_format(self, date_str):
        """اكتشاف تنسيق التاريخ"""
        if re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', date_str):
            return "YYYY-MM-DD HH:MM:SS"
        elif re.match(r'\d{2}/\d{2}/\d{4} \d{2}:\d{2}', date_str):
            return "DD/MM/YYYY HH:MM"
        else:
            return f"Unknown: {date_str[:20]}"
    
    def _extract_projects(self, details):
        """استخراج أرقام المشاريع من النص"""
        projects = set()
        if details:
            # البحث عن PRJ_xxx أو PROJ xxx أو TEST xxx
            patterns = [
                r'PRJ_\w+',
                r'PROJ\w*\d+',
                r'TEST\w*\d+',
                r'للمشروع\s+(\w+)'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, details, re.IGNORECASE)
                projects.update(matches)
        
        return projects
    
    def _check_parsing_issues(self, record, index):
        """فحص المشاكل المحتملة في السجل"""
        issues = []
        
        if len(record) < 6:
            issues.append(f"سجل {index}: عدد الأعمدة أقل من المتوقع ({len(record)})")
        
        # فحص التاريخ
        if record[0]:
            try:
                # محاولة معالجة التاريخ
                date_str = record[0].strip()
                if ' ' in date_str:
                    date_part, time_part = date_str.split(' ', 1)
                    datetime.strptime(date_part, '%Y-%m-%d')
                else:
                    datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                issues.append(f"سجل {index}: تنسيق تاريخ غير صالح '{record[0]}'")
        
        # فحص الكمية
        if record[3]:
            try:
                float(record[3])
            except ValueError:
                # قد تحتوي على نص إضافي، نحاول استخراج الرقم
                quantity_match = re.search(r'[\d.]+', str(record[3]))
                if not quantity_match:
                    issues.append(f"سجل {index}: كمية غير صالحة '{record[3]}'")
        
        return issues
    
    def convert_single_record(self, old_record):
        """تحويل سجل واحد إلى التنسيق الجديد"""
        try:
            if len(old_record) < 6:
                # إضافة قيم فارغة للأعمدة المفقودة
                old_record.extend([''] * (6 - len(old_record)))
            
            date_time = old_record[0] if old_record[0] else ""
            operation = old_record[1] if old_record[1] else ""
            item_name = old_record[2] if old_record[2] else ""
            quantity = old_record[3] if old_record[3] else ""
            recipient = old_record[4] if old_record[4] else ""
            details = old_record[5] if old_record[5] else ""
            
            # تفكيك التاريخ والوقت
            date_part = ""
            time_part = ""
            if date_time and ' ' in date_time:
                parts = date_time.split(' ', 1)
                date_part = parts[0]
                time_part = parts[1]
            elif date_time:
                date_part = date_time
                time_part = ""
            
            # تحليل الكمية والعملية
            quantity_added = 0
            quantity_removed = 0
            previous_quantity = 0
            current_quantity = 0
            
            operation_clean = operation.strip() if operation else ""
            
            # استخراج الكميات حسب نوع العملية
            if operation_clean in ["إضافة", "إنشاء"]:
                try:
                    quantity_added = float(quantity) if quantity else 0
                    current_quantity = quantity_added
                except ValueError:
                    quantity_added = 0
                    
            elif operation_clean == "إخراج":
                try:
                    quantity_removed = float(quantity) if quantity else 0
                    # محاولة استخراج الكمية المتبقية من التفاصيل
                    remaining_match = re.search(r'الكمية المتبقية[:\s]*([0-9.]+)', details)
                    if remaining_match:
                        current_quantity = float(remaining_match.group(1))
                        previous_quantity = current_quantity + quantity_removed
                except ValueError:
                    quantity_removed = 0
                    
            elif operation_clean == "تحديث":
                # تحليل تفاصيل التحديث
                try:
                    # البحث عن الكميات في التفاصيل
                    from_match = re.search(r'من\s+([0-9.]+)', details)
                    to_match = re.search(r'إلى\s+([0-9.]+)', details)
                    
                    if from_match and to_match:
                        previous_quantity = float(from_match.group(1))
                        current_quantity = float(to_match.group(1))
                        
                        if current_quantity > previous_quantity:
                            quantity_added = current_quantity - previous_quantity
                        else:
                            quantity_removed = previous_quantity - current_quantity
                    else:
                        # محاولة من الأعمدة الإضافية إذا كانت موجودة
                        try:
                            current_quantity = float(quantity)
                            if len(old_record) > 6:
                                previous_quantity = float(old_record[6]) if old_record[6] else 0
                                if current_quantity > previous_quantity:
                                    quantity_added = current_quantity - previous_quantity
                                else:
                                    quantity_removed = previous_quantity - current_quantity
                        except (ValueError, IndexError):
                            pass
                            
                except ValueError:
                    pass
            
            # استخراج رقم المشروع
            project_number = ""
            if details:
                project_patterns = [
                    r'PRJ_(\w+)',
                    r'PROJ(\w*\d+)',
                    r'TEST(\w*\d+)',
                    r'للمشروع\s+(\w+)'
                ]
                
                for pattern in project_patterns:
                    match = re.search(pattern, details, re.IGNORECASE)
                    if match:
                        project_number = match.group(1) if match.group(1) else match.group(0)
                        break
            
            # تنظيف التفاصيل (إزالة المعلومات المكررة)
            clean_details = details
            if details:
                # إزالة معلومات المشروع المكررة
                clean_details = re.sub(r'للمشروع\s+\w+', '', details)
                clean_details = re.sub(r'PRJ_\w+', '', clean_details)
                clean_details = re.sub(r'PROJ\w*\d+', '', clean_details)
                clean_details = re.sub(r'TEST\w*\d+', '', clean_details)
                # إزالة معلومات الكمية المكررة
                clean_details = re.sub(r'بكمية\s+[0-9.]+', '', clean_details)
                clean_details = re.sub(r'الكمية المخرجة[:\s]*[0-9.]+', '', clean_details)
                clean_details = re.sub(r'الكمية المتبقية[:\s]*[0-9.]+', '', clean_details)
                clean_details = clean_details.strip()
            
            # محاولة الحصول على التصنيف
            category = self._get_item_category(item_name)
            
            # تكوين السجل الجديد
            new_record = [
                date_part,              # التاريخ
                time_part,              # الوقت  
                operation_clean,        # نوع العملية
                item_name.strip() if item_name else "",  # اسم العنصر
                category,               # التصنيف
                quantity_added,         # الكمية المضافة
                quantity_removed,       # الكمية المخرجة
                previous_quantity,      # الكمية السابقة
                current_quantity,       # الكمية الحالية
                recipient.strip() if recipient else "",  # اسم المستلم
                project_number,         # رقم المشروع
                clean_details          # التفاصيل
            ]
            
            return new_record
            
        except Exception as e:
            print(f"❌ خطأ في تحويل السجل: {e}")
            print(f"السجل الأصلي: {old_record}")
            return None
    
    def _get_item_category(self, item_name):
        """محاولة الحصول على تصنيف العنصر من بيانات المخزون"""
        try:
            inventory_data = self.sheets_manager.get_all_items_raw()
            for item in inventory_data:
                if len(item) >= 2 and item[0] and item[1]:
                    if item[0].strip().lower() == item_name.strip().lower():
                        return item[1].strip()
        except:
            pass
        return ""
    
    def create_new_sheet_structure(self):
        """إنشاء هيكل الشيت الجديد"""
        new_headers = [
            "التاريخ",
            "الوقت", 
            "نوع العملية",
            "اسم العنصر",
            "التصنيف",
            "الكمية المضافة",
            "الكمية المخرجة", 
            "الكمية السابقة",
            "الكمية الحالية",
            "اسم المستلم",
            "رقم المشروع",
            "التفاصيل"
        ]
        return new_headers
    
    def preview_conversion(self, num_records=5):
        """معاينة التحويل على عدد محدود من السجلات"""
        print(f"🔍 معاينة تحويل أول {num_records} سجلات...")
        
        try:
            current_data = self.sheets_manager.get_activity_log()
            preview_results = []
            
            for i, record in enumerate(current_data[:num_records]):
                print(f"\n--- السجل {i+1} ---")
                print(f"📥 الأصلي: {record}")
                
                converted = self.convert_single_record(record)
                if converted:
                    print(f"📤 المحول: {converted}")
                    preview_results.append({
                        'original': record,
                        'converted': converted,
                        'success': True
                    })
                else:
                    print("❌ فشل التحويل")
                    preview_results.append({
                        'original': record,
                        'converted': None,
                        'success': False
                    })
            
            return preview_results
            
        except Exception as e:
            print(f"❌ خطأ في المعاينة: {e}")
            return None

def main():
    """تشغيل أداة التحليل والمعاينة"""
    print("🏗️ أداة تحويل Activity Log")
    print("=" * 50)
    
    # إنشاء مدير الشيتس
    sheets_manager = SheetsManager()
    
    # إنشاء محول البيانات
    converter = ActivityLogConverter(sheets_manager)
    
    print("1️⃣ تحليل البيانات الحالية...")
    analysis = converter.analyze_current_data()
    
    if analysis:
        print(f"\n📊 نتائج التحليل:")
        print(f"   📁 إجمالي السجلات: {analysis['total_records']}")
        print(f"   📅 تنسيقات التاريخ: {list(analysis['date_formats'])}")
        print(f"   ⚙️ أنواع العمليات: {list(analysis['operation_types'])}")
        print(f"   📦 عدد العناصر المختلفة: {len(analysis['item_names'])}")
        print(f"   👥 عدد المستلمين: {len(analysis['recipients'])}")
        print(f"   🏗️ أرقام المشاريع: {list(analysis['projects'])}")
        
        if analysis['parsing_issues']:
            print(f"\n⚠️ مشاكل محتملة ({len(analysis['parsing_issues'])}):")
            for issue in analysis['parsing_issues'][:5]:  # عرض أول 5 مشاكل
                print(f"   - {issue}")
            if len(analysis['parsing_issues']) > 5:
                print(f"   ... و {len(analysis['parsing_issues'])-5} مشاكل أخرى")
    
    print("\n2️⃣ معاينة التحويل...")
    preview = converter.preview_conversion(3)
    
    if preview:
        successful_conversions = sum(1 for p in preview if p['success'])
        print(f"\n✅ نجح تحويل {successful_conversions} من {len(preview)} سجلات في المعاينة")
    
    print("\n3️⃣ هيكل الشيت الجديد:")
    new_headers = converter.create_new_sheet_structure()
    for i, header in enumerate(new_headers, 1):
        print(f"   {i:2d}. {header}")
    
    print(f"\n🎯 الخطوة التالية:")
    print(f"   إذا كانت النتائج مرضية، يمكن تنفيذ التحويل الكامل")
    print(f"   سيتم إنشاء شيت جديد بالهيكل المحسن")

if __name__ == "__main__":
    main()