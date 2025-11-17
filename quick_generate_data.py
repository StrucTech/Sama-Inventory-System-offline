#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏗️ مولد البيانات السريع - نسخة محسنة
===================================

مولد محسن يتجنب تجاوز حدود Google Sheets API
"""

import sys
import os
from datetime import datetime, timedelta
import random
import time

# إضافة مسار المشروع
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sheets.manager import SheetsManager

class QuickDataGenerator:
    def __init__(self):
        """تهيئة مولد البيانات السريع"""
        
        self.sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
        
        # بيانات أساسية مبسطة
        self.projects = ["PRJ_2024_001", "PRJ_2024_002", "PRJ_2024_003", "PRJ_2024_004"]
        self.users = ["admin", "mohammed_supervisor", "fatma_warehouse", "ali_engineer"]
        self.operation_types = ["إضافة", "إخراج", "نقل", "تعديل"]
        
        # العناصر مع التصنيفات
        self.items = [
            # مواد البناء
            {"name": "أسمنت بورتلاندي CEM I 42.5", "category": "مواد البناء", "initial_qty": 200},
            {"name": "أسمنت أبيض CEM I 42.5", "category": "مواد البناء", "initial_qty": 150},
            {"name": "رمل البناء المغسول", "category": "مواد البناء", "initial_qty": 300},
            {"name": "حصى البناء المدرج", "category": "مواد البناء", "initial_qty": 250},
            {"name": "بلك خرساني 20x20x40", "category": "مواد البناء", "initial_qty": 500},
            
            # أدوات سباكة
            {"name": "أنابيب PVC قطر 110مم", "category": "أدوات سباكة", "initial_qty": 120},
            {"name": "صنابير مياه نحاس", "category": "أدوات سباكة", "initial_qty": 80},
            {"name": "خلاطات مياه حديثة", "category": "أدوات سباكة", "initial_qty": 60},
            {"name": "مضخات مياه 1 حصان", "category": "أدوات سباكة", "initial_qty": 25},
            {"name": "خزانات مياه بلاستيك", "category": "أدوات سباكة", "initial_qty": 40},
            
            # أدوات كهربائية
            {"name": "كابلات كهرباء 4مم", "category": "أدوات كهربائية", "initial_qty": 500},
            {"name": "مفاتيح كهرباء ذكية", "category": "أدوات كهربائية", "initial_qty": 100},
            {"name": "لوحات توزيع كهربائية", "category": "أدوات كهربائية", "initial_qty": 15},
            {"name": "مصابيح LED 20 واط", "category": "أدوات كهربائية", "initial_qty": 200},
            {"name": "مولدات كهرباء 10 كيلو واط", "category": "أدوات كهربائية", "initial_qty": 8},
            
            # أدوات عامة
            {"name": "مطارق بناء 500 جرام", "category": "أدوات عامة", "initial_qty": 50},
            {"name": "مثاقيب كهربائية", "category": "أدوات عامة", "initial_qty": 30},
            {"name": "سلالم ألومنيوم 3 متر", "category": "أدوات عامة", "initial_qty": 20},
            {"name": "عربات نقل المواد", "category": "أدوات عامة", "initial_qty": 15},
            {"name": "أقنعة وقاية صناعية", "category": "أدوات عامة", "initial_qty": 300}
        ]
        
        # تتبع الكميات
        self.current_quantities = {}
        for item in self.items:
            self.current_quantities[item["name"]] = item["initial_qty"]
        
    def connect(self):
        """الاتصال بـ Google Sheets"""
        if not self.sheets_manager.connect():
            print("❌ فشل في الاتصال!")
            return False
        print("✅ تم الاتصال بنجاح")
        return True
    
    def clear_and_setup_inventory(self):
        """مسح وإعداد المخزون"""
        
        try:
            print("📦 إعداد المخزون...")
            
            inventory_sheet = self.sheets_manager.spreadsheet.worksheet('Inventory')
            
            # مسح البيانات
            inventory_sheet.clear()
            
            # إضافة الرؤوس
            headers = ["اسم العنصر", "التصنيف", "الوحدة", "الكمية", "السعر", "القيمة الإجمالية", "تاريخ التحديث", "آخر مستخدم", "ملاحظات"]
            
            # إعداد بيانات المخزون
            inventory_data = [headers]
            
            for item in self.items:
                price = random.randint(10, 1000)  # سعر عشوائي
                qty = item["initial_qty"]
                total_value = qty * price
                
                row = [
                    item["name"],
                    item["category"],
                    "قطعة",
                    qty,
                    price,
                    total_value,
                    datetime.now().strftime("%Y-%m-%d"),
                    "admin",
                    "مخزون ابتدائي"
                ]
                inventory_data.append(row)
            
            # إضافة البيانات دفعة واحدة
            inventory_sheet.update('A1', inventory_data)
            print(f"✅ تم إعداد {len(self.items)} عنصر في المخزون")
            
        except Exception as e:
            print(f"❌ خطأ في إعداد المخزون: {e}")
            return False
        
        return True
    
    def generate_operations(self):
        """إنشاء العمليات دفعة واحدة"""
        
        try:
            print("🏗️ إنشاء عمليات المخزون...")
            
            activity_sheet = self.sheets_manager.spreadsheet.worksheet('Activity_Log_v2_20251108')
            
            # مسح البيانات
            activity_sheet.clear()
            
            # إضافة الرؤوس
            headers = ["التاريخ", "الوقت", "نوع العملية", "اسم العنصر", "التصنيف", 
                      "الكمية المضافة", "الكمية المخرجة", "الكمية السابقة", "الكمية الحالية", 
                      "اسم المستخدم", "رقم المشروع", "التفاصيل"]
            
            operations_data = [headers]
            
            # إنشاء 150 عملية
            start_date = datetime.now() - timedelta(days=60)
            
            for i in range(150):
                # تاريخ عشوائي
                operation_date = start_date + timedelta(
                    days=random.randint(0, 60),
                    hours=random.randint(7, 17),
                    minutes=random.randint(0, 59)
                )
                
                # اختيار عنصر عشوائي
                item = random.choice(self.items)
                item_name = item["name"]
                category = item["category"]
                
                # نوع العملية
                operation_type = random.choice(self.operation_types)
                
                # مستخدم ومشروع
                user = random.choice(self.users)
                project = random.choice(self.projects)
                
                # حساب الكميات
                previous_qty = self.current_quantities[item_name]
                added_qty = 0
                removed_qty = 0
                
                if operation_type == "إضافة":
                    added_qty = random.randint(10, 50)
                    self.current_quantities[item_name] += added_qty
                    details = f"شراء {added_qty} قطعة من {item_name}"
                    
                elif operation_type == "إخراج" and previous_qty > 0:
                    removed_qty = min(random.randint(1, 20), previous_qty)
                    self.current_quantities[item_name] -= removed_qty
                    details = f"استهلاك {removed_qty} قطعة في المشروع"
                    
                elif operation_type == "نقل" and previous_qty > 0:
                    removed_qty = min(random.randint(1, 15), previous_qty)
                    self.current_quantities[item_name] -= removed_qty
                    details = f"نقل {removed_qty} قطعة للمشروع {project}"
                    
                elif operation_type == "تعديل":
                    adjustment = random.randint(-10, 15)
                    if previous_qty + adjustment >= 0:
                        if adjustment > 0:
                            added_qty = adjustment
                        else:
                            removed_qty = abs(adjustment)
                        self.current_quantities[item_name] += adjustment
                        details = f"تصحيح مخزون بمقدار {adjustment:+}"
                    else:
                        continue
                else:
                    continue  # تخطي العمليات غير الصالحة
                
                current_qty = self.current_quantities[item_name]
                
                # إنشاء سجل العملية
                operation_row = [
                    operation_date.strftime("%Y-%m-%d"),
                    operation_date.strftime("%H:%M:%S"),
                    operation_type,
                    item_name,
                    category,
                    str(added_qty),
                    str(removed_qty),
                    str(previous_qty),
                    str(current_qty),
                    user,
                    project,
                    details
                ]
                
                operations_data.append(operation_row)
            
            # إضافة العمليات دفعة واحدة
            activity_sheet.update('A1', operations_data)
            print(f"✅ تم إنشاء {len(operations_data)-1} عملية")
            
        except Exception as e:
            print(f"❌ خطأ في إنشاء العمليات: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        return True
    
    def run(self):
        """تشغيل المولد"""
        
        print("🚀 بدء إنشاء البيانات التجريبية السريعة...")
        print("="*50)
        
        if not self.connect():
            return False
        
        if not self.clear_and_setup_inventory():
            return False
        
        # انتظار لتجنب تجاوز الحدود
        print("⏳ انتظار 10 ثوان...")
        time.sleep(10)
        
        if not self.generate_operations():
            return False
        
        print("\n" + "="*50)
        print("✅ تم إنشاء البيانات التجريبية بنجاح!")
        print("📊 الإحصائيات:")
        print(f"   • العناصر: {len(self.items)}")
        print(f"   • المشاريع: {len(self.projects)}")
        print(f"   • المستخدمين: {len(self.users)}")
        print(f"   • العمليات: ~150 عملية")
        print("\n🎮 يمكنك الآن اختبار:")
        print("   • فلاتر البحث")
        print("   • إحصائيات المخزون")
        print("   • تقارير العمليات")
        print("="*50)
        
        return True

def main():
    """الدالة الرئيسية"""
    
    generator = QuickDataGenerator()
    
    try:
        generator.run()
    except KeyboardInterrupt:
        print("\n⏹️ تم إيقاف العملية")
    except Exception as e:
        print(f"\n❌ خطأ: {e}")

if __name__ == "__main__":
    main()