#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏗️ مولد البيانات التجريبية لنظام إدارة المخزون
==============================================

هذا المولد سيقوم بـ:
1. مسح جميع البيانات الموجودة (الاحتفاظ بالرؤوس)
2. إنشاء بيانات تجريبية واقعية لعمليات المخزون
3. محاكاة عمليات مختلفة (إضافة، إخراج، نقل، تعديل)
4. ربط العمليات بمشاريع مختلفة
5. حسابات واقعية للكميات
"""

import sys
import os
from datetime import datetime, timedelta
import random

# إضافة مسار المشروع
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sheets.manager import SheetsManager

class InventoryDataGenerator:
    def __init__(self):
        """تهيئة مولد البيانات التجريبية"""
        
        # الاتصال بـ Google Sheets
        self.sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
        
        # بيانات المشاريع
        self.projects = [
            {"id": "PRJ_2024_001", "name": "مجمع سكني الواحة"},
            {"id": "PRJ_2024_002", "name": "مول تجاري النخيل"},
            {"id": "PRJ_2024_003", "name": "مصنع الإلكترونيات الحديث"},
            {"id": "PRJ_2024_004", "name": "مدرسة المستقبل التقنية"},
            {"id": "PRJ_2024_005", "name": "مستشفى النور الطبي"}
        ]
        
        # المستخدمين
        self.users = [
            {"username": "admin", "name": "أحمد المدير"},
            {"username": "mohammed_supervisor", "name": "محمد المشرف"},
            {"username": "fatma_warehouse", "name": "فاطمة أمين المخزن"},
            {"username": "ali_engineer", "name": "علي المهندس"},
            {"username": "sara_coordinator", "name": "سارة المنسقة"}
        ]
        
        # العناصر والمواد
        self.inventory_items = {
            "مواد البناء": [
                {"name": "أسمنت بورتلاندي CEM I 42.5", "unit": "كيس 50كيلو", "base_price": 45},
                {"name": "أسمنت أبيض CEM I 42.5", "unit": "كيس 50كيلو", "base_price": 85},
                {"name": "رمل البناء المغسول", "unit": "متر مكعب", "base_price": 120},
                {"name": "حصى البناء المدرج", "unit": "متر مكعب", "base_price": 150},
                {"name": "بلك خرساني 20x20x40", "unit": "قطعة", "base_price": 3.5},
                {"name": "طوب أحمر 24x12x6", "unit": "قطعة", "base_price": 1.2}
            ],
            "أدوات سباكة": [
                {"name": "أنابيب PVC قطر 110مم", "unit": "متر", "base_price": 25},
                {"name": "صنابير مياه نحاس", "unit": "قطعة", "base_price": 150},
                {"name": "خلاطات مياه حديثة", "unit": "قطعة", "base_price": 320},
                {"name": "مضخات مياه 1 حصان", "unit": "قطعة", "base_price": 850},
                {"name": "خزانات مياه بلاستيك 1000لتر", "unit": "قطعة", "base_price": 450}
            ],
            "أدوات كهربائية": [
                {"name": "كابلات كهرباء 4مم", "unit": "متر", "base_price": 12},
                {"name": "مفاتيح كهرباء ذكية", "unit": "قطعة", "base_price": 85},
                {"name": "لوحات توزيع كهربائية", "unit": "قطعة", "base_price": 650},
                {"name": "مصابيح LED 20 واط", "unit": "قطعة", "base_price": 45},
                {"name": "مولدات كهرباء 10 كيلو واط", "unit": "قطعة", "base_price": 12000}
            ],
            "أدوات عامة": [
                {"name": "مطارق بناء 500 جرام", "unit": "قطعة", "base_price": 35},
                {"name": "مثاقيب كهربائية", "unit": "قطعة", "base_price": 280},
                {"name": "سلالم ألومنيوم 3 متر", "unit": "قطعة", "base_price": 420},
                {"name": "عربات نقل المواد", "unit": "قطعة", "base_price": 180},
                {"name": "أقنعة وقاية صناعية", "unit": "قطعة", "base_price": 8}
            ]
        }
        
        # أنواع العمليات
        self.operation_types = ["إضافة", "إخراج", "نقل", "تعديل", "جرد"]
        
        # تتبع الكميات الحالية لكل عنصر
        self.current_quantities = {}
        
    def connect_to_sheets(self):
        """الاتصال بـ Google Sheets"""
        
        if not self.sheets_manager.connect():
            print("❌ فشل في الاتصال بـ Google Sheets!")
            return False
            
        print("✅ تم الاتصال بـ Google Sheets بنجاح")
        return True
    
    def clear_existing_data(self):
        """مسح البيانات الموجودة مع الاحتفاظ بالرؤوس"""
        
        try:
            print("🗑️ جاري مسح البيانات الموجودة...")
            
            # مسح بيانات المخزون
            inventory_sheet = self.sheets_manager.spreadsheet.worksheet('Inventory')
            all_values = inventory_sheet.get_all_values()
            
            if len(all_values) > 1:
                # الاحتفاظ بالرؤوس فقط
                headers = all_values[0]
                inventory_sheet.clear()
                inventory_sheet.append_row(headers)
                print(f"✅ تم مسح {len(all_values)-1} صف من المخزون")
            
            # مسح بيانات سجل العمليات
            activity_sheet = self.sheets_manager.spreadsheet.worksheet('Activity_Log_v2_20251108')
            all_values = activity_sheet.get_all_values()
            
            if len(all_values) > 1:
                # الاحتفاظ بالرؤوس فقط
                headers = all_values[0]
                activity_sheet.clear()
                activity_sheet.append_row(headers)
                print(f"✅ تم مسح {len(all_values)-1} صف من سجل العمليات")
                
            print("🆕 تم مسح جميع البيانات مع الاحتفاظ بالرؤوس")
            
        except Exception as e:
            print(f"❌ خطأ في مسح البيانات: {e}")
            return False
            
        return True
    
    def initialize_inventory(self):
        """تهيئة المخزون بكميات ابتدائية"""
        
        try:
            print("📦 جاري تهيئة المخزون بكميات ابتدائية...")
            
            inventory_sheet = self.sheets_manager.spreadsheet.worksheet('Inventory')
            
            for category, items in self.inventory_items.items():
                for item in items:
                    # كمية ابتدائية عشوائية واقعية
                    initial_qty = random.randint(50, 500)
                    self.current_quantities[item["name"]] = initial_qty
                    
                    # إضافة العنصر للمخزون
                    row_data = [
                        item["name"],           # اسم العنصر
                        category,               # التصنيف  
                        item["unit"],           # الوحدة
                        initial_qty,            # الكمية
                        item["base_price"],     # السعر
                        initial_qty * item["base_price"], # القيمة الإجمالية
                        datetime.now().strftime("%Y-%m-%d"), # تاريخ آخر تحديث
                        "admin",                # آخر مستخدم
                        "تهيئة أولية للمخزون"  # ملاحظات
                    ]
                    
                    inventory_sheet.append_row(row_data)
                    
            print(f"✅ تم تهيئة {len(self.current_quantities)} عنصر في المخزون")
            
        except Exception as e:
            print(f"❌ خطأ في تهيئة المخزون: {e}")
            return False
            
        return True
    
    def generate_realistic_operations(self, num_operations=200):
        """إنشاء عمليات واقعية للمخزون"""
        
        try:
            print(f"🏗️ جاري إنشاء {num_operations} عملية واقعية...")
            
            activity_sheet = self.sheets_manager.spreadsheet.worksheet('Activity_Log_v2_20251108')
            
            # قائمة جميع العناصر
            all_items = []
            for category, items in self.inventory_items.items():
                for item in items:
                    all_items.append({**item, "category": category})
            
            # تاريخ البداية (قبل 3 أشهر)
            start_date = datetime.now() - timedelta(days=90)
            
            for i in range(num_operations):
                # اختيار تاريخ ووقت عشوائي
                operation_date = start_date + timedelta(
                    days=random.randint(0, 90),
                    hours=random.randint(6, 18),
                    minutes=random.randint(0, 59)
                )
                
                # اختيار عنصر عشوائي
                item = random.choice(all_items)
                item_name = item["name"]
                category = item["category"]
                
                # اختيار نوع العملية بناءً على احتمالات واقعية
                operation_weights = [40, 25, 15, 15, 5]  # إضافة، إخراج، نقل، تعديل، جرد
                operation_type = random.choices(self.operation_types, weights=operation_weights)[0]
                
                # اختيار مستخدم ومشروع
                user = random.choice(self.users)
                project = random.choice(self.projects)
                
                # الكمية الحالية للعنصر
                current_qty = self.current_quantities.get(item_name, 0)
                
                # حساب الكميات حسب نوع العملية
                added_qty = 0
                removed_qty = 0
                previous_qty = current_qty
                
                if operation_type == "إضافة":
                    # إضافة كمية جديدة
                    added_qty = random.randint(10, 100)
                    current_qty += added_qty
                    details = f"شراء {added_qty} {item['unit']} من {item_name} للمشروع {project['name']}"
                    
                elif operation_type == "إخراج":
                    # إخراج كمية (لا تتجاوز المتاح)
                    if current_qty > 0:
                        removed_qty = min(random.randint(1, 50), current_qty)
                        current_qty -= removed_qty
                        details = f"استهلاك {removed_qty} {item['unit']} من {item_name} في {project['name']}"
                    else:
                        continue  # تخطي إذا لم تكن هناك كمية متاحة
                        
                elif operation_type == "نقل":
                    # نقل كمية بين مشاريع
                    if current_qty > 0:
                        transferred_qty = min(random.randint(1, 30), current_qty)
                        removed_qty = transferred_qty
                        current_qty -= transferred_qty
                        
                        # إضافة عملية النقل للمشروع الآخر
                        target_project = random.choice([p for p in self.projects if p != project])
                        details = f"نقل {transferred_qty} {item['unit']} من {item_name} من {project['name']} إلى {target_project['name']}"
                    else:
                        continue
                        
                elif operation_type == "تعديل":
                    # تعديل في الكمية (تصحيح خطأ)
                    adjustment = random.randint(-20, 30)
                    if current_qty + adjustment >= 0:
                        if adjustment > 0:
                            added_qty = adjustment
                        else:
                            removed_qty = abs(adjustment)
                        current_qty += adjustment
                        details = f"تصحيح مخزون {item_name} - تعديل بمقدار {adjustment:+} {item['unit']}"
                    else:
                        continue
                        
                elif operation_type == "جرد":
                    # عملية جرد (بدون تغيير في الكمية)
                    details = f"جرد دوري لمخزون {item_name} في {project['name']}"
                
                # تحديث الكمية الحالية
                self.current_quantities[item_name] = current_qty
                
                # إنشاء سجل العملية
                operation_row = [
                    operation_date.strftime("%Y-%m-%d"),    # التاريخ
                    operation_date.strftime("%H:%M:%S"),    # الوقت
                    operation_type,                         # نوع العملية
                    item_name,                              # اسم العنصر
                    category,                               # التصنيف
                    str(added_qty),                         # الكمية المضافة
                    str(removed_qty),                       # الكمية المخرجة
                    str(previous_qty),                      # الكمية السابقة
                    str(current_qty),                       # الكمية الحالية
                    user["username"],                       # اسم المستخدم
                    project["id"],                          # رقم المشروع
                    details                                 # التفاصيل
                ]
                
                activity_sheet.append_row(operation_row)
                
                # طباعة تقدم العملية
                if (i + 1) % 20 == 0:
                    print(f"📊 تم إنشاء {i + 1} عملية...")
                    
            print(f"✅ تم إنشاء {num_operations} عملية واقعية بنجاح!")
            
        except Exception as e:
            print(f"❌ خطأ في إنشاء العمليات: {e}")
            import traceback
            traceback.print_exc()
            return False
            
        return True
    
    def update_final_inventory(self):
        """تحديث المخزون النهائي بناءً على العمليات"""
        
        try:
            print("🔄 جاري تحديث المخزون النهائي...")
            
            inventory_sheet = self.sheets_manager.spreadsheet.worksheet('Inventory')
            all_rows = inventory_sheet.get_all_values()
            
            if len(all_rows) > 1:
                headers = all_rows[0]
                
                # تحديث كل صف
                for i, row in enumerate(all_rows[1:], 2):
                    item_name = row[0]  # اسم العنصر
                    
                    if item_name in self.current_quantities:
                        final_qty = self.current_quantities[item_name]
                        unit_price = float(row[4]) if row[4] else 0
                        total_value = final_qty * unit_price
                        
                        # تحديث الصف
                        inventory_sheet.update_cell(i, 4, final_qty)        # الكمية
                        inventory_sheet.update_cell(i, 6, total_value)      # القيمة الإجمالية
                        inventory_sheet.update_cell(i, 7, datetime.now().strftime("%Y-%m-%d"))  # تاريخ التحديث
                        
            print("✅ تم تحديث المخزون النهائي بنجاح!")
            
        except Exception as e:
            print(f"❌ خطأ في تحديث المخزون: {e}")
            return False
            
        return True
    
    def generate_summary_report(self):
        """إنشاء تقرير ملخص للبيانات المُولدة"""
        
        print("\n" + "="*60)
        print("📊 ملخص البيانات التجريبية المُولدة")
        print("="*60)
        
        # إحصائيات المشاريع
        print(f"🏗️ المشاريع: {len(self.projects)}")
        for project in self.projects:
            print(f"   • {project['id']}: {project['name']}")
        
        # إحصائيات المستخدمين
        print(f"\n👥 المستخدمون: {len(self.users)}")
        for user in self.users:
            print(f"   • {user['username']}: {user['name']}")
        
        # إحصائيات المواد
        total_items = sum(len(items) for items in self.inventory_items.values())
        print(f"\n📦 إجمالي العناصر: {total_items}")
        
        for category, items in self.inventory_items.items():
            print(f"\n🏷️ {category}: {len(items)} عنصر")
            total_qty = 0
            total_value = 0
            
            for item in items:
                item_name = item["name"]
                qty = self.current_quantities.get(item_name, 0)
                value = qty * item["base_price"]
                total_qty += qty
                total_value += value
                
                print(f"   • {item_name}: {qty} {item['unit']} (قيمة: {value:,.0f})")
            
            print(f"   📊 إجمالي الفئة: {total_qty} قطعة بقيمة {total_value:,.0f}")
        
        print("\n" + "="*60)
        print("✅ تم إنشاء البيانات التجريبية بنجاح!")
        print("🎮 يمكنك الآن اختبار البرنامج مع بيانات واقعية")
        print("="*60)
    
    def run_full_generation(self):
        """تشغيل عملية إنشاء البيانات الكاملة"""
        
        print("🚀 بدء إنشاء البيانات التجريبية...")
        print("="*50)
        
        # الخطوة 1: الاتصال
        if not self.connect_to_sheets():
            return False
        
        # الخطوة 2: مسح البيانات الموجودة
        if not self.clear_existing_data():
            return False
        
        # الخطوة 3: تهيئة المخزون
        if not self.initialize_inventory():
            return False
        
        # الخطوة 4: إنشاء العمليات
        if not self.generate_realistic_operations(250):
            return False
        
        # الخطوة 5: تحديث المخزون النهائي
        if not self.update_final_inventory():
            return False
        
        # الخطوة 6: تقرير الملخص
        self.generate_summary_report()
        
        return True

def main():
    """الدالة الرئيسية"""
    
    generator = InventoryDataGenerator()
    
    try:
        success = generator.run_full_generation()
        
        if success:
            print("\n🎉 تم إنشاء البيانات التجريبية بنجاح!")
            print("💡 يمكنك الآن تشغيل البرنامج واختبار:")
            print("   • فلاتر العمليات")
            print("   • إحصائيات المشاريع")
            print("   • تقارير المخزون")
            print("   • عمليات الإدخال والإخراج")
        else:
            print("\n❌ فشل في إنشاء البيانات التجريبية!")
            
    except KeyboardInterrupt:
        print("\n⏹️ تم إيقاف العملية بواسطة المستخدم")
    except Exception as e:
        print(f"\n❌ خطأ غير متوقع: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()