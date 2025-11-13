#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أداة التحويل الفعلية لـ Activity Log
تحويل آمن مع نسخ احتياطية
"""

import re
import sys
import os
import json
from datetime import datetime

# إضافة مسار المشروع
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from sheets.manager import SheetsManager
    from config.settings import load_config
except ImportError as e:
    print(f"❌ خطأ في استيراد المكتبات: {e}")
    print("🔧 تأكد من وجود ملفات المشروع في المكان الصحيح")
    sys.exit(1)

class ActivityLogRestructurer:
    """فئة إعادة هيكلة Activity Log"""
    
    def __init__(self):
        self.config = None
        self.sheets_manager = None
        self.backup_data = []
        self.conversion_log = []
        
    def setup(self):
        """إعداد الاتصال بـ Google Sheets"""
        try:
            print("🔧 إعداد الاتصال...")
            
            # تحميل الإعدادات
            self.config = load_config()
            if not self.config:
                raise Exception("فشل في تحميل الإعدادات")
            
            # إنشاء مدير الشيتس
            self.sheets_manager = SheetsManager(
                credentials_file=self.config['credentials_file'],
                spreadsheet_name=self.config['spreadsheet_name'],
                worksheet_name=self.config['worksheet_name']
            )
            
            # الاتصال
            if not self.sheets_manager.connect():
                raise Exception("فشل في الاتصال بـ Google Sheets")
            
            print("✅ تم الإعداد بنجاح")
            return True
            
        except Exception as e:
            print(f"❌ خطأ في الإعداد: {e}")
            return False
    
    def create_backup(self):
        """إنشاء نسخة احتياطية من البيانات الحالية"""
        try:
            print("💾 إنشاء نسخة احتياطية...")
            
            # قراءة البيانات الحالية
            self.backup_data = self.sheets_manager.get_activity_log()
            
            # حفظ النسخة الاحتياطية في ملف JSON
            backup_file = f"activity_log_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            backup_path = os.path.join(os.path.dirname(__file__), "backups", backup_file)
            
            # إنشاء مجلد النسخ الاحتياطية إذا لم يكن موجوداً
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)
            
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(self.backup_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ تم حفظ النسخة الاحتياطية: {backup_file}")
            print(f"📁 المسار: {backup_path}")
            print(f"📊 عدد السجلات: {len(self.backup_data)}")
            
            return True
            
        except Exception as e:
            print(f"❌ خطأ في إنشاء النسخة الاحتياطية: {e}")
            return False
    
    def analyze_data_quality(self):
        """تحليل جودة البيانات قبل التحويل"""
        print("\n🔍 تحليل جودة البيانات...")
        
        total_records = len(self.backup_data)
        valid_records = 0
        issues = []
        
        for i, record in enumerate(self.backup_data):
            record_issues = []
            
            # فحص عدد الأعمدة
            if len(record) < 6:
                record_issues.append(f"عدد أعمدة أقل من المتوقع ({len(record)})")
            
            # فحص التاريخ
            if not record[0] or not record[0].strip():
                record_issues.append("التاريخ فارغ")
            else:
                try:
                    date_str = record[0].strip()
                    if ' ' in date_str:
                        date_part = date_str.split(' ')[0]
                        datetime.strptime(date_part, '%Y-%m-%d')
                except ValueError:
                    record_issues.append(f"تنسيق تاريخ غير صالح: {record[0]}")
            
            # فحص نوع العملية
            if not record[1] or not record[1].strip():
                record_issues.append("نوع العملية فارغ")
            
            # فحص اسم العنصر
            if not record[2] or not record[2].strip():
                record_issues.append("اسم العنصر فارغ")
            
            # فحص الكمية
            if record[3]:
                try:
                    float(record[3])
                except ValueError:
                    # محاولة استخراج رقم من النص
                    quantity_match = re.search(r'[\d.]+', str(record[3]))
                    if not quantity_match:
                        record_issues.append(f"كمية غير صالحة: {record[3]}")
            
            if record_issues:
                issues.append(f"السجل {i+1}: {', '.join(record_issues)}")
            else:
                valid_records += 1
        
        print(f"📊 نتائج التحليل:")
        print(f"   📁 إجمالي السجلات: {total_records}")
        print(f"   ✅ سجلات صالحة: {valid_records}")
        print(f"   ⚠️ سجلات بها مشاكل: {len(issues)}")
        
        if issues:
            print(f"\n⚠️ المشاكل المكتشفة (أول 5):")
            for issue in issues[:5]:
                print(f"   - {issue}")
            if len(issues) > 5:
                print(f"   ... و {len(issues)-5} مشاكل أخرى")
        
        # تحديد نسبة النجاح المتوقعة
        success_rate = (valid_records / total_records) * 100 if total_records > 0 else 0
        print(f"\n📈 نسبة النجاح المتوقعة: {success_rate:.1f}%")
        
        return success_rate >= 90  # متابعة فقط إذا كانت نسبة النجاح 90% أو أكثر
    
    def convert_record(self, old_record, index):
        """تحويل سجل واحد إلى الهيكل الجديد"""
        try:
            # التأكد من وجود 6 أعمدة على الأقل
            while len(old_record) < 6:
                old_record.append('')
            
            date_time = old_record[0].strip() if old_record[0] else ""
            operation = old_record[1].strip() if old_record[1] else ""
            item_name = old_record[2].strip() if old_record[2] else ""
            quantity = old_record[3].strip() if old_record[3] else ""
            recipient = old_record[4].strip() if old_record[4] else ""
            details = old_record[5].strip() if old_record[5] else ""
            
            # تفكيك التاريخ والوقت
            date_part = ""
            time_part = ""
            if date_time:
                if ' ' in date_time:
                    parts = date_time.split(' ', 1)
                    date_part = parts[0]
                    time_part = parts[1]
                else:
                    date_part = date_time
            
            # تحليل الكمية والعملية
            quantity_added = 0
            quantity_removed = 0
            previous_quantity = 0
            current_quantity = 0
            
            # معالجة الكمية الأساسية
            base_quantity = 0
            if quantity:
                try:
                    base_quantity = float(quantity)
                except ValueError:
                    # محاولة استخراج رقم من النص
                    quantity_match = re.search(r'[\d.]+', quantity)
                    if quantity_match:
                        base_quantity = float(quantity_match.group())
            
            # تحليل حسب نوع العملية
            if operation in ["إضافة", "إنشاء"]:
                quantity_added = base_quantity
                current_quantity = base_quantity
                
            elif operation == "إخراج":
                quantity_removed = base_quantity
                # محاولة استخراج الكمية المتبقية من التفاصيل
                remaining_match = re.search(r'الكمية المتبقية[:\s]*([0-9.]+)', details)
                if remaining_match:
                    current_quantity = float(remaining_match.group(1))
                    previous_quantity = current_quantity + quantity_removed
                else:
                    # إذا لم نجد الكمية المتبقية، نحاول تخمينها
                    previous_quantity = base_quantity
                    current_quantity = 0
                    
            elif operation == "تحديث":
                # في التحديث، نحتاج لتحليل أعمق
                current_quantity = base_quantity
                
                # محاولة الحصول على الكمية السابقة من عمود المستلم أو التفاصيل
                if recipient and recipient.replace('.', '').isdigit():
                    previous_quantity = float(recipient)
                else:
                    # البحث في التفاصيل
                    from_match = re.search(r'من\s+([0-9.]+)', details)
                    if from_match:
                        previous_quantity = float(from_match.group(1))
                
                # حساب الفرق
                if current_quantity > previous_quantity:
                    quantity_added = current_quantity - previous_quantity
                elif current_quantity < previous_quantity:
                    quantity_removed = previous_quantity - current_quantity
                    
            elif operation == "حذف":
                quantity_removed = base_quantity
                previous_quantity = base_quantity
                current_quantity = 0
            
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
                        if match.groups():
                            project_number = match.group(1)
                        else:
                            project_number = match.group(0)
                        break
            
            # الحصول على التصنيف
            category = self.get_item_category(item_name)
            
            # تنظيف التفاصيل
            clean_details = self.clean_details(details, project_number, base_quantity)
            
            # تنظيف حقل المستلم (في حالة التحديث قد يحتوي على كمية بدلاً من اسم)
            clean_recipient = recipient
            if operation == "تحديث" and recipient.replace('.', '').isdigit():
                clean_recipient = ""  # مسح الكمية من حقل المستلم
            
            # تكوين السجل الجديد
            new_record = [
                date_part,              # التاريخ
                time_part,              # الوقت
                operation,              # نوع العملية
                item_name,              # اسم العنصر
                category,               # التصنيف
                quantity_added,         # الكمية المضافة
                quantity_removed,       # الكمية المخرجة
                previous_quantity,      # الكمية السابقة
                current_quantity,       # الكمية الحالية
                clean_recipient,        # اسم المستلم
                project_number,         # رقم المشروع
                clean_details           # التفاصيل
            ]
            
            # تسجيل نجاح التحويل
            self.conversion_log.append({
                'index': index,
                'status': 'success',
                'original': old_record,
                'converted': new_record
            })
            
            return new_record
            
        except Exception as e:
            # تسجيل فشل التحويل
            self.conversion_log.append({
                'index': index,
                'status': 'error',
                'original': old_record,
                'error': str(e)
            })
            
            print(f"⚠️ خطأ في تحويل السجل {index}: {e}")
            return None
    
    def get_item_category(self, item_name):
        """تحديد تصنيف العنصر"""
        if not item_name:
            return ""
        
        item_lower = item_name.lower()
        
        # قواعد التصنيف التلقائي
        if any(word in item_lower for word in ["مسامير", "براغي", "معدن", "حديد"]):
            return "أدوات معدنية"
        elif any(word in item_lower for word in ["أسمنت", "خرسانة", "بناء"]):
            return "مواد البناء"  
        elif any(word in item_lower for word in ["كابل", "كهرباء", "سلك"]):
            return "أدوات كهربائية"
        elif any(word in item_lower for word in ["طلاء", "دهان", "ألوان"]):
            return "مواد التشطيب"
        elif any(word in item_lower for word in ["كمبيوتر", "خادم", "جهاز", "تقني"]):
            return "أجهزة تقنية"
        else:
            return "متنوع"
    
    def clean_details(self, details, project_number, quantity):
        """تنظيف حقل التفاصيل من المعلومات المكررة"""
        if not details:
            return ""
        
        clean = details
        
        # إزالة معلومات المشروع المكررة
        if project_number:
            clean = re.sub(rf'للمشروع\s+{re.escape(project_number)}', '', clean, flags=re.IGNORECASE)
            clean = re.sub(rf'{re.escape(project_number)}', '', clean)
        
        # إزالة معلومات الكمية المكررة
        clean = re.sub(rf'بكمية\s+{quantity}', '', clean)
        clean = re.sub(r'الكمية المخرجة[:\s]*[0-9.]+', '', clean)
        clean = re.sub(r'الكمية المتبقية[:\s]*[0-9.]+', '', clean)
        clean = re.sub(r'من\s+[0-9.]+\s+إلى\s+[0-9.]+', '', clean)
        clean = re.sub(r'\(إضافة\s+[0-9.]+\)', '', clean)
        
        # تنظيف المسافات الزائدة
        clean = re.sub(r'\s+', ' ', clean).strip()
        clean = re.sub(r'^[,.\s-]+|[,.\s-]+$', '', clean).strip()
        
        return clean
    
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
    
    def preview_conversion(self, num_samples=5):
        """معاينة التحويل على عينة من البيانات"""
        print(f"\n🔍 معاينة التحويل لـ {num_samples} سجلات...")
        
        sample_records = self.backup_data[:num_samples]
        converted_samples = []
        
        for i, record in enumerate(sample_records):
            print(f"\n--- عينة {i+1} ---")
            print(f"📥 الأصلي: {record}")
            
            converted = self.convert_record(record, i)
            if converted:
                print(f"📤 المحول: {converted}")
                converted_samples.append(converted)
            else:
                print("❌ فشل التحويل")
        
        success_rate = (len(converted_samples) / len(sample_records)) * 100
        print(f"\n📊 نسبة نجاح المعاينة: {success_rate:.1f}%")
        
        return success_rate >= 80
    
    def execute_conversion(self):
        """تنفيذ التحويل الكامل"""
        print(f"\n🔄 بدء التحويل الكامل...")
        print(f"📊 إجمالي السجلات: {len(self.backup_data)}")
        
        # إنشاء هيكل الشيت الجديد
        new_headers = self.create_new_sheet_structure()
        converted_data = [new_headers]  # البداية بالعناوين
        
        successful_conversions = 0
        failed_conversions = 0
        
        # تحويل كل سجل
        for i, record in enumerate(self.backup_data):
            converted = self.convert_record(record, i)
            if converted:
                converted_data.append(converted)
                successful_conversions += 1
            else:
                failed_conversions += 1
            
            # عرض التقدم كل 10 سجلات
            if (i + 1) % 10 == 0:
                print(f"📈 تم معالجة {i+1}/{len(self.backup_data)} سجل...")
        
        print(f"\n✅ انتهى التحويل:")
        print(f"   ✅ نجح: {successful_conversions}")
        print(f"   ❌ فشل: {failed_conversions}")
        print(f"   📊 نسبة النجاح: {(successful_conversions/len(self.backup_data)*100):.1f}%")
        
        return converted_data
    
    def save_converted_data(self, converted_data):
        """حفظ البيانات المحولة في شيت جديد"""
        try:
            print(f"\n💾 حفظ البيانات المحولة...")
            
            # إنشاء اسم شيت جديد
            new_sheet_name = f"Activity_Log_v2_{datetime.now().strftime('%Y%m%d')}"
            
            # محاولة إنشاء الشيت الجديد
            try:
                new_worksheet = self.sheets_manager.spreadsheet.add_worksheet(
                    title=new_sheet_name,
                    rows=len(converted_data) + 10,
                    cols=len(converted_data[0]) if converted_data else 12
                )
                print(f"✅ تم إنشاء الشيت الجديد: {new_sheet_name}")
                
            except Exception as e:
                print(f"⚠️ الشيت موجود مسبقاً أو خطأ في الإنشاء: {e}")
                # محاولة الوصول للشيت الموجود
                new_worksheet = self.sheets_manager.spreadsheet.worksheet(new_sheet_name)
                new_worksheet.clear()
            
            # كتابة البيانات
            if converted_data:
                new_worksheet.update('A1', converted_data)
                print(f"✅ تم حفظ {len(converted_data)-1} سجل في الشيت الجديد")
                
                # تنسيق العناوين
                new_worksheet.format('A1:L1', {
                    'backgroundColor': {'red': 0.8, 'green': 0.9, 'blue': 1.0},
                    'textFormat': {'bold': True}
                })
                
                return True
            
        except Exception as e:
            print(f"❌ خطأ في حفظ البيانات: {e}")
            return False
    
    def generate_conversion_report(self):
        """إنشاء تقرير التحويل"""
        print(f"\n📋 تقرير التحويل")
        print("=" * 50)
        
        total_records = len(self.conversion_log)
        successful = sum(1 for log in self.conversion_log if log['status'] == 'success')
        failed = total_records - successful
        
        print(f"📊 الإحصائيات:")
        print(f"   📁 إجمالي السجلات: {total_records}")
        print(f"   ✅ تم تحويلها بنجاح: {successful}")
        print(f"   ❌ فشل في تحويلها: {failed}")
        print(f"   📈 نسبة النجاح: {(successful/total_records*100):.1f}%")
        
        if failed > 0:
            print(f"\n❌ السجلات التي فشل تحويلها:")
            failed_logs = [log for log in self.conversion_log if log['status'] == 'error']
            for log in failed_logs[:5]:  # عرض أول 5 أخطاء
                print(f"   السجل {log['index']}: {log['error']}")
            if len(failed_logs) > 5:
                print(f"   ... و {len(failed_logs)-5} أخطاء أخرى")

def main():
    """تشغيل عملية إعادة الهيكلة الكاملة"""
    print("🏗️ أداة إعادة هيكلة Activity Log")
    print("=" * 50)
    
    restructurer = ActivityLogRestructurer()
    
    # المرحلة 1: الإعداد
    print("1️⃣ الإعداد والاتصال...")
    if not restructurer.setup():
        print("❌ فشل في الإعداد")
        return
    
    # المرحلة 2: النسخة الاحتياطية
    print("\n2️⃣ إنشاء نسخة احتياطية...")
    if not restructurer.create_backup():
        print("❌ فشل في إنشاء النسخة الاحتياطية")
        return
    
    # المرحلة 3: تحليل جودة البيانات
    print("\n3️⃣ تحليل جودة البيانات...")
    if not restructurer.analyze_data_quality():
        print("❌ جودة البيانات غير مقبولة للتحويل")
        response = input("هل تريد المتابعة رغم ذلك؟ (y/N): ")
        if response.lower() != 'y':
            return
    
    # المرحلة 4: معاينة التحويل
    print("\n4️⃣ معاينة التحويل...")
    if not restructurer.preview_conversion():
        print("❌ معاينة التحويل غير مرضية")
        response = input("هل تريد المتابعة رغم ذلك؟ (y/N): ")
        if response.lower() != 'y':
            return
    
    # تأكيد أخير
    print(f"\n⚠️ تأكيد أخير:")
    print(f"   سيتم إنشاء شيت جديد بالهيكل المحسن")
    print(f"   الشيت الأصلي سيبقى كما هو (نسخة احتياطية)")
    response = input("هل تريد المتابعة؟ (y/N): ")
    if response.lower() != 'y':
        print("❌ تم إلغاء العملية")
        return
    
    # المرحلة 5: التنفيذ
    print("\n5️⃣ تنفيذ التحويل...")
    converted_data = restructurer.execute_conversion()
    
    if converted_data:
        # المرحلة 6: الحفظ
        print("\n6️⃣ حفظ البيانات المحولة...")
        if restructurer.save_converted_data(converted_data):
            print("✅ تم حفظ البيانات بنجاح")
        else:
            print("❌ فشل في حفظ البيانات")
    
    # المرحلة 7: التقرير
    restructurer.generate_conversion_report()
    
    print(f"\n🎉 انتهت عملية إعادة الهيكلة!")
    print(f"📋 الخطوة التالية: تحديث الكود ليتعامل مع الهيكل الجديد")

if __name__ == "__main__":
    main()