"""
🗑️ مسح البيانات الحالية وإعادة تعبئة بيانات اختبار مترابطة
================================================================

هذا السكريبت سيقوم بـ:
1. مسح جميع البيانات في الشيتات (مع الاحتفاظ بالرؤوس)
2. إنشاء بيانات اختبار مترابطة ومنطقية
3. ملء الشيتات بالبيانات الجديدة
"""

import sys
import os
from datetime import datetime, timedelta
import random

# إضافة مسار المشروع
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sheets.manager import SheetsManager

class DataResetAndPopulator:
    def __init__(self):
        """تهيئة أداة إعادة تعيين البيانات"""
        self.sheets_manager = None
        
    def connect_to_sheets(self):
        """الاتصال بـ Google Sheets"""
        try:
            print("📡 جاري الاتصال بـ Google Sheets...")
            
            self.sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
            
            if not self.sheets_manager.connect():
                print("❌ فشل في الاتصال بـ Google Sheets")
                return False
            
            print("✅ تم الاتصال بـ Google Sheets بنجاح")
            return True
            
        except Exception as e:
            print(f"❌ خطأ في الاتصال: {str(e)}")
            return False
    
    def clear_all_data(self):
        """مسح جميع البيانات مع الاحتفاظ بالرؤوس"""
        
        try:
            print("\n🗑️ بدء عملية مسح البيانات...")
            
            # 1. مسح بيانات المخزون الرئيسي
            print("📊 مسح بيانات المخزون الرئيسي...")
            worksheet = self.sheets_manager.worksheet
            
            # الحصول على البيانات الحالية
            all_values = worksheet.get_all_values()
            if len(all_values) > 1:
                # مسح جميع البيانات ما عدا الرؤوس (الصف الأول)
                num_rows = len(all_values)
                if num_rows > 1:
                    worksheet.delete_rows(2, num_rows)
                print(f"   ✅ تم مسح {num_rows - 1} صف من المخزون الرئيسي")
            
            # 2. مسح بيانات سجل النشاط
            print("⚡ مسح بيانات سجل النشاط...")
            try:
                activity_worksheet = self.sheets_manager.spreadsheet.worksheet('activity_log')
                activity_values = activity_worksheet.get_all_values()
                if len(activity_values) > 1:
                    num_activity_rows = len(activity_values)
                    if num_activity_rows > 1:
                        activity_worksheet.delete_rows(2, num_activity_rows)
                    print(f"   ✅ تم مسح {num_activity_rows - 1} صف من سجل النشاط العادي")
            except Exception as e:
                print(f"   ⚠️ لا يوجد سجل نشاط عادي أو خطأ: {e}")
            
            # 3. مسح بيانات Activity_Log_v2_20251108
            print("📋 مسح بيانات Activity_Log_v2_20251108...")
            try:
                activity_v2_worksheet = self.sheets_manager.spreadsheet.worksheet('Activity_Log_v2_20251108')
                activity_v2_values = activity_v2_worksheet.get_all_values()
                if len(activity_v2_values) > 1:
                    num_v2_rows = len(activity_v2_values)
                    if num_v2_rows > 1:
                        activity_v2_worksheet.delete_rows(2, num_v2_rows)
                    print(f"   ✅ تم مسح {num_v2_rows - 1} صف من Activity_Log_v2_20251108")
            except Exception as e:
                print(f"   ⚠️ لا يوجد Activity_Log_v2_20251108 أو خطأ: {e}")
            
            # 4. مسح بيانات المستخدمين (إن وجدت)
            print("👥 مسح بيانات المستخدمين...")
            try:
                users_worksheet = self.sheets_manager.spreadsheet.worksheet('users')
                users_values = users_worksheet.get_all_values()
                if len(users_values) > 1:
                    num_users_rows = len(users_values)
                    if num_users_rows > 1:
                        users_worksheet.delete_rows(2, num_users_rows)
                    print(f"   ✅ تم مسح {num_users_rows - 1} صف من المستخدمين")
            except Exception as e:
                print(f"   ⚠️ لا يوجد شيت مستخدمين أو خطأ: {e}")
            
            print("✅ تم الانتهاء من مسح جميع البيانات")
            return True
            
        except Exception as e:
            print(f"❌ خطأ في مسح البيانات: {str(e)}")
            return False
    
    def populate_test_data(self):
        """تعبئة بيانات اختبار مترابطة ومنطقية"""
        
        try:
            print("\n📊 بدء تعبئة بيانات اختبار مترابطة...")
            
            # بيانات المشاريع
            projects = ['PRJ_2024_001', 'PRJ_2024_002', 'PRJ_2024_003']
            
            # بيانات العناصر المترابطة
            inventory_items = [
                # مواد البناء
                {'name': 'أسمنت أبيض CEM I 42.5', 'category': 'مواد البناء', 'initial': 500, 'project': projects[0]},
                {'name': 'أسمنت رمادي CEM II 32.5', 'category': 'مواد البناء', 'initial': 800, 'project': projects[0]},
                {'name': 'رمل خشن مغسول', 'category': 'مواد البناء', 'initial': 1000, 'project': projects[1]},
                {'name': 'زلط حجم 2 سم', 'category': 'مواد البناء', 'initial': 750, 'project': projects[1]},
                {'name': 'طوب أحمر 25×12×6', 'category': 'مواد البناء', 'initial': 2000, 'project': projects[2]},
                
                # أدوات كهربائية
                {'name': 'كابل كهرباء 2.5 مم²', 'category': 'أدوات كهربائية', 'initial': 300, 'project': projects[0]},
                {'name': 'كابل كهرباء 4 مم²', 'category': 'أدوات كهربائية', 'initial': 200, 'project': projects[0]},
                {'name': 'مفاتيح كهرباء مودرن', 'category': 'أدوات كهربائية', 'initial': 150, 'project': projects[1]},
                {'name': 'أفياش كهرباء ثلاثية', 'category': 'أدوات كهربائية', 'initial': 100, 'project': projects[1]},
                {'name': 'قواطع كهرباء 25A', 'category': 'أدوات كهربائية', 'initial': 50, 'project': projects[2]},
                
                # أدوات سباكة
                {'name': 'أنابيب PVC قطر 110 مم', 'category': 'أدوات سباكة', 'initial': 200, 'project': projects[0]},
                {'name': 'أنابيب PVC قطر 75 مم', 'category': 'أدوات سباكة', 'initial': 150, 'project': projects[1]},
                {'name': 'صنابير مياه نحاس', 'category': 'أدوات سباكة', 'initial': 80, 'project': projects[2]},
                {'name': 'خلاطات مياه حديثة', 'category': 'أدوات سباكة', 'initial': 60, 'project': projects[2]},
                
                # أدوات عامة
                {'name': 'مفك براغي كهربائي', 'category': 'أدوات عامة', 'initial': 25, 'project': projects[0]},
                {'name': 'شريط قياس 5 متر', 'category': 'أدوات عامة', 'initial': 30, 'project': projects[1]},
                {'name': 'مطرقة 500 جرام', 'category': 'أدوات عامة', 'initial': 20, 'project': projects[2]},
                {'name': 'منشار يدوي 60 سم', 'category': 'أدوات عامة', 'initial': 15, 'project': projects[0]}
            ]
            
            # 1. تعبئة بيانات المخزون الرئيسي
            self.populate_inventory_data(inventory_items)
            
            # 2. تعبئة بيانات سجل العمليات
            self.populate_activity_log(inventory_items, projects)
            
            # 3. تعبئة بيانات المستخدمين (اختياري)
            self.populate_users_data()
            
            print("✅ تم الانتهاء من تعبئة جميع البيانات بنجاح")
            return True
            
        except Exception as e:
            print(f"❌ خطأ في تعبئة البيانات: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def populate_inventory_data(self, items):
        """تعبئة بيانات المخزون الرئيسي"""
        
        print("📦 تعبئة بيانات المخزون الرئيسي...")
        
        worksheet = self.sheets_manager.worksheet
        
        # تحضير البيانات للإدراج
        rows_to_insert = []
        
        for item in items:
            # حساب العمليات العشوائية لكل عنصر
            incoming = random.randint(0, int(item['initial'] * 0.3))  # 0-30% من الكمية الأولية
            outgoing = random.randint(0, int(item['initial'] * 0.2))   # 0-20% من الكمية الأولية
            remaining = item['initial'] + incoming - outgoing
            
            # تاريخ عشوائي خلال الشهر الماضي
            days_ago = random.randint(1, 30)
            last_updated = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d %H:%M:%S")
            
            row = [
                item['name'],           # اسم العنصر
                item['category'],       # التصنيف
                item['initial'],        # الكمية الابتدائية
                incoming,               # الكمية الداخلة
                outgoing,               # الكمية الخارجة
                remaining,              # الكمية المتبقية
                item['project'],        # رقم المشروع
                last_updated            # آخر تحديث
            ]
            
            rows_to_insert.append(row)
        
        # إدراج جميع الصفوف دفعة واحدة
        if rows_to_insert:
            range_name = f"A2:H{len(rows_to_insert) + 1}"
            worksheet.update(range_name, rows_to_insert)
            print(f"   ✅ تم إضافة {len(rows_to_insert)} عنصر للمخزون")
        
        return rows_to_insert
    
    def populate_activity_log(self, items, projects):
        """تعبئة سجل العمليات المترابط"""
        
        print("⚡ تعبئة سجل العمليات...")
        
        try:
            # محاولة الوصول للشيت الصحيح
            activity_worksheet = self.sheets_manager.spreadsheet.worksheet('Activity_Log_v2_20251108')
            
            # إنشاء عمليات مترابطة
            operations = []
            users = ['ahmed_manager', 'fatma_supervisor', 'mohamed_worker', 'admin']
            operation_types = ['إضافة', 'إخراج', 'تعديل', 'نقل']
            
            base_date = datetime.now() - timedelta(days=60)  # ابدأ من 60 يوم مضت
            
            for day in range(60):  # إنشاء عمليات لـ 60 يوم
                current_date = base_date + timedelta(days=day)
                
                # عدد العمليات يومياً (1-5 عمليات)
                daily_operations = random.randint(1, 5)
                
                for _ in range(daily_operations):
                    item = random.choice(items)
                    operation_type = random.choice(operation_types)
                    user = random.choice(users)
                    
                    # تحديد الكميات حسب نوع العملية
                    if operation_type == 'إضافة':
                        added_qty = random.randint(10, 100)
                        removed_qty = 0
                        details = f"إضافة {added_qty} وحدة من {item['name']} للمشروع {item['project']}"
                    elif operation_type == 'إخراج':
                        added_qty = 0
                        removed_qty = random.randint(5, 50)
                        details = f"إخراج {removed_qty} وحدة من {item['name']} للمشروع {item['project']}"
                    elif operation_type == 'تعديل':
                        added_qty = random.randint(0, 20)
                        removed_qty = random.randint(0, 15)
                        details = f"تعديل كمية {item['name']} - إضافة {added_qty} وإخراج {removed_qty}"
                    else:  # نقل
                        transferred_qty = random.randint(5, 30)
                        source_project = item['project']
                        target_project = random.choice([p for p in projects if p != source_project])
                        added_qty = 0
                        removed_qty = transferred_qty
                        details = f"نقل {transferred_qty} وحدة من {item['name']} من {source_project} إلى {target_project}"
                    
                    # تحديد الكميات السابقة والحالية بشكل منطقي
                    previous_qty = random.randint(50, 500)
                    current_qty = previous_qty + added_qty - removed_qty
                    
                    # تأكد من أن الكمية الحالية لا تصبح سالبة
                    if current_qty < 0:
                        current_qty = 0
                        removed_qty = previous_qty  # عدل الكمية المخرجة
                    
                    operation_time = current_date.replace(
                        hour=random.randint(8, 17),  # ساعات العمل
                        minute=random.randint(0, 59),
                        second=random.randint(0, 59)
                    )
                    
                    operation_row = [
                        operation_time.strftime("%Y-%m-%d"),      # التاريخ
                        operation_time.strftime("%H:%M:%S"),      # الوقت
                        operation_type,                           # نوع العملية
                        item['name'],                            # اسم العنصر
                        item['category'],                        # التصنيف
                        added_qty,                               # الكمية المضافة
                        removed_qty,                             # الكمية المخرجة
                        previous_qty,                            # الكمية السابقة
                        current_qty,                             # الكمية الحالية
                        user,                                    # اسم المستخدم
                        item['project'],                         # رقم المشروع
                        details                                  # التفاصيل
                    ]
                    
                    operations.append(operation_row)
            
            # ترتيب العمليات حسب التاريخ والوقت
            operations.sort(key=lambda x: f"{x[0]} {x[1]}")
            
            # إدراج العمليات في الشيت
            if operations:
                range_name = f"A2:L{len(operations) + 1}"
                activity_worksheet.update(range_name, operations)
                print(f"   ✅ تم إضافة {len(operations)} عملية لسجل النشاط")
                
                # إحصائيات سريعة
                total_added = sum(op[5] for op in operations)  # الكمية المضافة
                total_removed = sum(op[6] for op in operations)  # الكمية المخرجة
                print(f"   📊 إجمالي الإضافات: {total_added:,}")
                print(f"   📊 إجمالي الإخراجات: {total_removed:,}")
                print(f"   📊 صافي التغيير: {total_added - total_removed:,}")
            
        except Exception as e:
            print(f"   ⚠️ خطأ في إنشاء سجل العمليات: {e}")
    
    def populate_users_data(self):
        """تعبئة بيانات المستخدمين"""
        
        print("👥 تعبئة بيانات المستخدمين...")
        
        try:
            users_worksheet = self.sheets_manager.spreadsheet.worksheet('users')
            
            users_data = [
                ['admin', 'المدير العام', 'admin', '', 'نشط', datetime.now().strftime("%Y-%m-%d")],
                ['ahmed_manager', 'أحمد محمد', 'manager', 'PRJ_2024_001', 'نشط', datetime.now().strftime("%Y-%m-%d")],
                ['fatma_supervisor', 'فاطمة علي', 'supervisor', 'PRJ_2024_002', 'نشط', datetime.now().strftime("%Y-%m-%d")],
                ['mohamed_worker', 'محمد عبدالله', 'user', 'PRJ_2024_003', 'نشط', datetime.now().strftime("%Y-%m-%d")],
                ['sara_assistant', 'سارة أحمد', 'user', 'PRJ_2024_001', 'نشط', datetime.now().strftime("%Y-%m-%d")]
            ]
            
            if users_data:
                range_name = f"A2:F{len(users_data) + 1}"
                users_worksheet.update(range_name, users_data)
                print(f"   ✅ تم إضافة {len(users_data)} مستخدم")
            
        except Exception as e:
            print(f"   ⚠️ خطأ في إنشاء بيانات المستخدمين: {e}")
    
    def generate_summary_report(self):
        """إنشاء تقرير ملخص للبيانات الجديدة"""
        
        print("\n📋 تقرير ملخص البيانات الجديدة:")
        print("=" * 50)
        
        try:
            # إحصائيات المخزون
            worksheet = self.sheets_manager.worksheet
            inventory_data = worksheet.get_all_values()
            
            if len(inventory_data) > 1:
                inventory_count = len(inventory_data) - 1
                
                # حساب الإحصائيات
                total_initial = 0
                total_incoming = 0
                total_outgoing = 0
                total_remaining = 0
                
                categories = set()
                projects = set()
                
                for row in inventory_data[1:]:
                    if len(row) >= 8:
                        try:
                            total_initial += int(row[2]) if row[2].isdigit() else 0
                            total_incoming += int(row[3]) if row[3].isdigit() else 0
                            total_outgoing += int(row[4]) if row[4].isdigit() else 0
                            total_remaining += int(row[5]) if row[5].isdigit() else 0
                            
                            categories.add(row[1])
                            projects.add(row[6])
                        except (ValueError, IndexError):
                            pass
                
                print(f"📦 المخزون: {inventory_count} عنصر")
                print(f"🏷️ التصنيفات: {len(categories)} ({', '.join(sorted(categories))})")
                print(f"🎯 المشاريع: {len(projects)} ({', '.join(sorted(projects))})")
                print(f"📊 الكمية الابتدائية: {total_initial:,}")
                print(f"📥 إجمالي الداخل: {total_incoming:,}")
                print(f"📤 إجمالي الخارج: {total_outgoing:,}")
                print(f"📦 الكمية المتبقية: {total_remaining:,}")
            
            # إحصائيات العمليات
            try:
                activity_worksheet = self.sheets_manager.spreadsheet.worksheet('Activity_Log_v2_20251108')
                activity_data = activity_worksheet.get_all_values()
                
                if len(activity_data) > 1:
                    operations_count = len(activity_data) - 1
                    print(f"⚡ العمليات المسجلة: {operations_count:,}")
                    
                    # تحليل أنواع العمليات
                    operation_types = {}
                    for row in activity_data[1:]:
                        if len(row) >= 3:
                            op_type = row[2]
                            operation_types[op_type] = operation_types.get(op_type, 0) + 1
                    
                    for op_type, count in operation_types.items():
                        print(f"   {op_type}: {count} عملية")
                
            except Exception as e:
                print(f"⚠️ لا توجد بيانات عمليات: {e}")
            
            print("\n✅ تم إنشاء قاعدة بيانات اختبار مترابطة وجاهزة للاختبار!")
            print("🚀 يمكنك الآن اختبار جميع وظائف البرنامج بثقة")
            
        except Exception as e:
            print(f"❌ خطأ في إنشاء التقرير: {e}")
    
    def run(self):
        """تشغيل عملية إعادة التعيين الكاملة"""
        
        print("🗑️ بدء عملية إعادة تعيين البيانات الكاملة")
        print("=" * 60)
        
        # 1. الاتصال
        if not self.connect_to_sheets():
            return False
        
        # 2. تأكيد من المستخدم
        print("\n⚠️ تحذير: هذه العملية ستقوم بـ:")
        print("   • مسح جميع البيانات الحالية")
        print("   • الاحتفاظ بالرؤوس فقط")
        print("   • إنشاء بيانات اختبار جديدة مترابطة")
        
        confirm = input("\n❓ هل أنت متأكد من المتابعة؟ (اكتب 'نعم' للمتابعة): ")
        
        if confirm.lower() not in ['نعم', 'yes', 'y']:
            print("❌ تم إلغاء العملية")
            return False
        
        # 3. مسح البيانات
        if not self.clear_all_data():
            return False
        
        # 4. تعبئة بيانات جديدة
        if not self.populate_test_data():
            return False
        
        # 5. إنشاء تقرير
        self.generate_summary_report()
        
        return True


def main():
    """الدالة الرئيسية"""
    
    print("🗑️🔄 أداة إعادة تعيين وتعبئة بيانات الاختبار")
    print("=" * 60)
    
    try:
        resetter = DataResetAndPopulator()
        success = resetter.run()
        
        if success:
            print("\n🎉 تمت العملية بنجاح!")
            print("💡 يمكنك الآن تشغيل البرنامج واختبار جميع الوظائف")
        else:
            print("\n❌ فشلت العملية!")
            
    except KeyboardInterrupt:
        print("\n⚠️ تم إيقاف العملية بواسطة المستخدم")
    except Exception as e:
        print(f"\n💥 خطأ غير متوقع: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()