#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إصدار محديث من SheetsManager للتعامل مع Activity Log الجديد
"""

import re
import sys
import os
from datetime import datetime

# إضافة مسار المشروع
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from sheets.manager import SheetsManager as OriginalSheetsManager
    from config.settings import load_config
except ImportError as e:
    print(f"❌ خطأ في استيراد المكتبات: {e}")
    sys.exit(1)

class EnhancedSheetsManager(OriginalSheetsManager):
    """مدير شيتس محسن للتعامل مع الهيكل الجديد"""
    
    def __init__(self, credentials_file: str, spreadsheet_name: str, worksheet_name: str = "Inventory"):
        super().__init__(credentials_file, spreadsheet_name, worksheet_name)
        self.new_activity_log_name = "Activity_Log_v2_20251108"
        self.new_activity_log = None
        
    def connect(self) -> bool:
        """اتصال محسن مع دعم الشيت الجديد"""
        if not super().connect():
            return False
            
        try:
            # محاولة الوصول للشيت الجديد
            self.new_activity_log = self.spreadsheet.worksheet(self.new_activity_log_name)
            print(f"✅ تم العثور على الشيت الجديد: {self.new_activity_log_name}")
            return True
        except Exception as e:
            print(f"⚠️ لم يتم العثور على الشيت الجديد: {e}")
            print("🔄 سيتم استخدام الشيت القديم")
            return True
    
    def get_activity_log_new_format(self):
        """قراءة البيانات من الشيت الجديد"""
        try:
            if not self.new_activity_log:
                print("❌ الشيت الجديد غير متاح")
                return []
                
            # قراءة جميع البيانات
            all_values = self.new_activity_log.get_all_values()
            
            if len(all_values) <= 1:
                return []
            
            # إرجاع البيانات بدون العناوين
            return all_values[1:]
            
        except Exception as e:
            print(f"❌ خطأ في قراءة الشيت الجديد: {e}")
            return []
    
    def get_activity_log_headers_new(self):
        """الحصول على عناوين الشيت الجديد"""
        return [
            "التاريخ",           # 0
            "الوقت",             # 1
            "نوع العملية",       # 2
            "اسم العنصر",        # 3
            "التصنيف",          # 4
            "الكمية المضافة",     # 5
            "الكمية المخرجة",     # 6
            "الكمية السابقة",     # 7
            "الكمية الحالية",     # 8
            "اسم المستلم",       # 9
            "رقم المشروع",       # 10
            "التفاصيل"          # 11
        ]
    
    def add_activity_log_entry_new(self, operation_type: str, item_name: str, 
                                   quantity_added: float = 0, quantity_removed: float = 0,
                                   previous_quantity: float = 0, current_quantity: float = 0,
                                   recipient_name: str = "", project_number: str = "", 
                                   details: str = "", category: str = ""):
        """إضافة إدخال جديد للشيت المحسن"""
        try:
            if not self.new_activity_log:
                print("❌ الشيت الجديد غير متاح")
                return False
            
            # الحصول على التاريخ والوقت الحالي
            now = datetime.now()
            date_part = now.strftime("%Y-%m-%d")
            time_part = now.strftime("%H:%M:%S")
            
            # تحديد التصنيف تلقائياً إذا لم يكن محدداً
            if not category:
                category = self._auto_categorize(item_name)
            
            # تكوين السجل الجديد
            new_record = [
                date_part,
                time_part,
                operation_type,
                item_name,
                category,
                quantity_added,
                quantity_removed,
                previous_quantity,
                current_quantity,
                recipient_name,
                project_number,
                details
            ]
            
            # إضافة السجل للشيت
            self.new_activity_log.append_row(new_record)
            print(f"✅ تم إضافة سجل جديد: {operation_type} - {item_name}")
            return True
            
        except Exception as e:
            print(f"❌ خطأ في إضافة السجل: {e}")
            return False
    
    def _auto_categorize(self, item_name: str) -> str:
        """تصنيف تلقائي للعناصر"""
        if not item_name:
            return "متنوع"
        
        item_lower = item_name.lower()
        
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
    
    def filter_activity_log_new(self, date_from=None, date_to=None, operation_type=None, 
                               item_name=None, category=None, recipient=None, project=None):
        """فلترة متقدمة للبيانات الجديدة"""
        try:
            data = self.get_activity_log_new_format()
            filtered_data = []
            
            for record in data:
                if len(record) < 12:
                    continue
                    
                # فلترة التاريخ
                if date_from or date_to:
                    record_date = record[0]  # التاريخ في العمود الأول
                    if record_date:
                        try:
                            record_date_obj = datetime.strptime(record_date, "%Y-%m-%d")
                            
                            if date_from:
                                date_from_obj = datetime.strptime(date_from, "%Y-%m-%d")
                                if record_date_obj < date_from_obj:
                                    continue
                                    
                            if date_to:
                                date_to_obj = datetime.strptime(date_to, "%Y-%m-%d")
                                if record_date_obj > date_to_obj:
                                    continue
                        except ValueError:
                            continue
                
                # فلترة نوع العملية
                if operation_type and record[2].strip() != operation_type.strip():
                    continue
                
                # فلترة اسم العنصر (بحث جزئي)
                if item_name and item_name.lower().strip() not in record[3].lower():
                    continue
                
                # فلترة التصنيف (بحث جزئي)
                if category and category.lower().strip() not in record[4].lower():
                    continue
                
                # فلترة المستلم
                if recipient and recipient.lower().strip() not in record[9].lower():
                    continue
                
                # فلترة المشروع
                if project and project.lower().strip() not in record[10].lower():
                    continue
                
                filtered_data.append(record)
            
            return filtered_data
            
        except Exception as e:
            print(f"❌ خطأ في الفلترة: {e}")
            return []
    
    def get_statistics_new(self):
        """إحصائيات متقدمة من البيانات الجديدة"""
        try:
            data = self.get_activity_log_new_format()
            
            stats = {
                'total_records': len(data),
                'total_added': 0,
                'total_removed': 0,
                'operations_count': {},
                'categories_count': {},
                'projects_count': {},
                'monthly_summary': {}
            }
            
            for record in data:
                if len(record) < 12:
                    continue
                
                # إحصائيات الكميات
                try:
                    added = float(record[5]) if record[5] else 0
                    removed = float(record[6]) if record[6] else 0
                    stats['total_added'] += added
                    stats['total_removed'] += removed
                except ValueError:
                    pass
                
                # إحصائيات العمليات
                operation = record[2]
                stats['operations_count'][operation] = stats['operations_count'].get(operation, 0) + 1
                
                # إحصائيات التصنيفات
                category = record[4]
                if category:
                    stats['categories_count'][category] = stats['categories_count'].get(category, 0) + 1
                
                # إحصائيات المشاريع
                project = record[10]
                if project:
                    stats['projects_count'][project] = stats['projects_count'].get(project, 0) + 1
                
                # إحصائيات شهرية
                date_str = record[0]
                if date_str:
                    try:
                        month_key = date_str[:7]  # YYYY-MM
                        stats['monthly_summary'][month_key] = stats['monthly_summary'].get(month_key, 0) + 1
                    except:
                        pass
            
            return stats
            
        except Exception as e:
            print(f"❌ خطأ في حساب الإحصائيات: {e}")
            return {}

def test_enhanced_manager():
    """اختبار المدير المحسن"""
    print("🧪 اختبار المدير المحسن")
    print("=" * 40)
    
    try:
        # تحميل الإعدادات
        config = load_config()
        if not config:
            print("❌ فشل في تحميل الإعدادات")
            return
        
        # إنشاء المدير المحسن
        manager = EnhancedSheetsManager(
            credentials_file=config['credentials_file'],
            spreadsheet_name=config['spreadsheet_name'],
            worksheet_name=config['worksheet_name']
        )
        
        # الاتصال
        if not manager.connect():
            print("❌ فشل في الاتصال")
            return
        
        print("✅ تم الاتصال بنجاح")
        
        # اختبار قراءة البيانات الجديدة
        print("\n📊 اختبار قراءة البيانات الجديدة...")
        new_data = manager.get_activity_log_new_format()
        print(f"✅ تم قراءة {len(new_data)} سجل من الشيت الجديد")
        
        # عرض أول 3 سجلات
        if new_data:
            headers = manager.get_activity_log_headers_new()
            print(f"\n📋 العناوين الجديدة:")
            for i, header in enumerate(headers):
                print(f"   {i+1:2d}. {header}")
            
            print(f"\n📝 أول 3 سجلات:")
            for i, record in enumerate(new_data[:3]):
                print(f"\n--- السجل {i+1} ---")
                for j, (header, value) in enumerate(zip(headers, record)):
                    if value:  # عرض القيم غير الفارغة فقط
                        print(f"   {header}: {value}")
        
        # اختبار الإحصائيات
        print(f"\n📊 اختبار الإحصائيات...")
        stats = manager.get_statistics_new()
        if stats:
            print(f"   📁 إجمالي السجلات: {stats['total_records']}")
            print(f"   ⬆️ إجمالي المضاف: {stats['total_added']}")
            print(f"   ⬇️ إجمالي المخرج: {stats['total_removed']}")
            print(f"   🔄 أنواع العمليات: {stats['operations_count']}")
            print(f"   🏷️ التصنيفات: {stats['categories_count']}")
            print(f"   🏗️ المشاريع: {stats['projects_count']}")
        
        # اختبار الفلترة
        print(f"\n🔍 اختبار الفلترة...")
        filtered = manager.filter_activity_log_new(operation_type="إضافة")
        print(f"   ✅ عمليات الإضافة: {len(filtered)}")
        
        filtered = manager.filter_activity_log_new(category="أدوات معدنية")
        print(f"   ✅ الأدوات المعدنية: {len(filtered)}")
        
        print(f"\n🎉 اكتمل الاختبار بنجاح!")
        
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {e}")

if __name__ == "__main__":
    test_enhanced_manager()