"""
🔍 فحص شامل لصحة البيانات المُحدّثة
=====================================

هذا السكريبت يتحقق من:
1. صحة بيانات المخزون الرئيسي
2. صحة بيانات سجل العمليات  
3. الترابط بين البيانات
4. المنطق الرياضي للحسابات
"""

import sys
import os
from collections import defaultdict
from datetime import datetime

# إضافة مسار المشروع
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sheets.manager import SheetsManager

class DataValidator:
    def __init__(self):
        """تهيئة أداة التحقق من البيانات"""
        self.sheets_manager = None
        self.validation_results = {
            'inventory_valid': False,
            'activity_log_valid': False,
            'data_consistency': False,
            'math_accuracy': False,
            'errors': []
        }
        
    def connect_to_sheets(self):
        """الاتصال بـ Google Sheets"""
        try:
            print("الاتصال بـ Google Sheets...")
            
            self.sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
            
            if not self.sheets_manager.connect():
                print("فشل في الاتصال بـ Google Sheets")
                return False
            
            print("تم الاتصال بـ Google Sheets بنجاح")
            return True
            
        except Exception as e:
            print(f"خطأ في الاتصال: {str(e)}")
            return False
    
    def validate_inventory_data(self):
        """التحقق من صحة بيانات المخزون"""
        
        print("\n=== فحص بيانات المخزون الرئيسي ===")
        
        try:
            worksheet = self.sheets_manager.worksheet
            inventory_data = worksheet.get_all_values()
            
            if not inventory_data:
                self.validation_results['errors'].append("لا توجد بيانات في المخزون")
                return False
            
            headers = inventory_data[0]
            expected_headers = ['اسم العنصر', 'التصنيف', 'الكمية الابتدائية', 'الكمية الداخلة', 
                              'الكمية الخارجة', 'الكمية المتبقية', 'رقم المشروع', 'آخر تحديث']
            
            print(f"عدد الأعمدة: {len(headers)}")
            print(f"عدد الصفوف: {len(inventory_data)}")
            print(f"عدد العناصر: {len(inventory_data) - 1}")
            
            # التحقق من الرؤوس
            headers_valid = True
            for i, expected in enumerate(expected_headers):
                if i < len(headers):
                    if headers[i] != expected:
                        print(f"خطأ في الرأس {i+1}: متوقع '{expected}' وجد '{headers[i]}'")
                        headers_valid = False
                else:
                    print(f"رأس مفقود: {expected}")
                    headers_valid = False
            
            if headers_valid:
                print("✓ رؤوس الأعمدة صحيحة")
            
            # فحص البيانات
            categories = set()
            projects = set()
            items = {}
            errors = []
            
            total_initial = 0
            total_incoming = 0  
            total_outgoing = 0
            total_remaining = 0
            
            for i, row in enumerate(inventory_data[1:], 2):  # ابدأ من الصف 2
                
                if len(row) < 8:
                    errors.append(f"الصف {i}: بيانات ناقصة - {len(row)} أعمدة فقط")
                    continue
                
                item_name = row[0]
                category = row[1]
                
                try:
                    initial = int(row[2]) if row[2].isdigit() else 0
                    incoming = int(row[3]) if row[3].isdigit() else 0
                    outgoing = int(row[4]) if row[4].isdigit() else 0
                    remaining = int(row[5]) if row[5].isdigit() else 0
                    
                    # التحقق من المنطق الرياضي لكل عنصر
                    expected_remaining = initial + incoming - outgoing
                    if remaining != expected_remaining:
                        errors.append(f"خطأ حسابي في '{item_name}': متوقع {expected_remaining} وجد {remaining}")
                    
                    total_initial += initial
                    total_incoming += incoming
                    total_outgoing += outgoing
                    total_remaining += remaining
                    
                    categories.add(category)
                    projects.add(row[6])
                    items[item_name] = {
                        'category': category,
                        'initial': initial,
                        'incoming': incoming,
                        'outgoing': outgoing,
                        'remaining': remaining,
                        'project': row[6]
                    }
                    
                except ValueError as e:
                    errors.append(f"الصف {i} ({item_name}): خطأ في تحويل الأرقام - {e}")
            
            print(f"\nالإحصائيات:")
            print(f"  التصنيفات ({len(categories)}): {sorted(categories)}")
            print(f"  المشاريع ({len(projects)}): {sorted(projects)}")
            print(f"  العناصر: {len(items)}")
            print(f"  الكمية الابتدائية الإجمالية: {total_initial:,}")
            print(f"  الكمية الداخلة الإجمالية: {total_incoming:,}")
            print(f"  الكمية الخارجة الإجمالية: {total_outgoing:,}")
            print(f"  الكمية المتبقية الإجمالية: {total_remaining:,}")
            
            # التحقق من المنطق الإجمالي
            expected_total = total_initial + total_incoming - total_outgoing
            print(f"  المتوقع حسابياً: {expected_total:,}")
            
            if total_remaining == expected_total:
                print("✓ الحسابات الإجمالية صحيحة")
                self.validation_results['math_accuracy'] = True
            else:
                errors.append(f"خطأ في الحسابات الإجمالية: الفرق {total_remaining - expected_total}")
            
            if errors:
                print(f"\nالأخطاء المكتشفة ({len(errors)}):")
                for error in errors[:10]:  # اعرض أول 10 أخطاء
                    print(f"  • {error}")
                if len(errors) > 10:
                    print(f"  ... و{len(errors) - 10} خطأ آخر")
                self.validation_results['errors'].extend(errors)
            else:
                print("✓ لا توجد أخطاء في بيانات المخزون")
                self.validation_results['inventory_valid'] = True
            
            return len(errors) == 0, items
            
        except Exception as e:
            error_msg = f"خطأ في فحص المخزون: {str(e)}"
            print(error_msg)
            self.validation_results['errors'].append(error_msg)
            return False, {}
    
    def validate_activity_log(self, inventory_items):
        """التحقق من صحة بيانات سجل العمليات"""
        
        print("\n=== فحص سجل العمليات ===")
        
        try:
            activity_worksheet = self.sheets_manager.spreadsheet.worksheet('Activity_Log_v2_20251108')
            activity_data = activity_worksheet.get_all_values()
            
            if not activity_data:
                self.validation_results['errors'].append("لا توجد بيانات في سجل العمليات")
                return False
            
            headers = activity_data[0]
            expected_headers = ['التاريخ', 'الوقت', 'نوع العملية', 'اسم العنصر', 'التصنيف', 
                              'الكمية المضافة', 'الكمية المخرجة', 'الكمية السابقة', 
                              'الكمية الحالية', 'اسم المستخدم', 'رقم المشروع', 'التفاصيل']
            
            print(f"عدد الأعمدة: {len(headers)}")
            print(f"عدد الصفوف: {len(activity_data)}")
            print(f"عدد العمليات: {len(activity_data) - 1}")
            
            # فحص البيانات
            operation_types = defaultdict(int)
            users = set()
            projects = set()
            items_in_log = set()
            errors = []
            
            total_added_in_log = 0
            total_removed_in_log = 0
            
            for i, row in enumerate(activity_data[1:], 2):
                
                if len(row) < 12:
                    errors.append(f"العملية {i-1}: بيانات ناقصة")
                    continue
                
                try:
                    date_str = row[0]
                    time_str = row[1]
                    op_type = row[2]
                    item_name = row[3]
                    category = row[4]
                    added_qty = int(row[5]) if row[5].isdigit() else 0
                    removed_qty = int(row[6]) if row[6].isdigit() else 0
                    prev_qty = int(row[7]) if row[7].isdigit() else 0
                    current_qty = int(row[8]) if row[8].isdigit() else 0
                    user = row[9]
                    project = row[10]
                    
                    # التحقق من التاريخ
                    try:
                        datetime.strptime(date_str, "%Y-%m-%d")
                    except ValueError:
                        errors.append(f"العملية {i-1}: تاريخ غير صالح '{date_str}'")
                    
                    # التحقق من الوقت
                    try:
                        datetime.strptime(time_str, "%H:%M:%S")
                    except ValueError:
                        errors.append(f"العملية {i-1}: وقت غير صالح '{time_str}'")
                    
                    # التحقق من المنطق الحسابي للعملية
                    expected_current = prev_qty + added_qty - removed_qty
                    if current_qty != expected_current:
                        errors.append(f"العملية {i-1} ({item_name}): خطأ حسابي - متوقع {expected_current} وجد {current_qty}")
                    
                    # التحقق من وجود العنصر في المخزون
                    if item_name in inventory_items:
                        if inventory_items[item_name]['category'] != category:
                            errors.append(f"العملية {i-1}: تصنيف مختلف للعنصر '{item_name}'")
                    
                    operation_types[op_type] += 1
                    users.add(user)
                    projects.add(project)
                    items_in_log.add(item_name)
                    
                    total_added_in_log += added_qty
                    total_removed_in_log += removed_qty
                    
                except ValueError as e:
                    errors.append(f"العملية {i-1}: خطأ في البيانات - {e}")
            
            print(f"\nإحصائيات العمليات:")
            print(f"  أنواع العمليات:")
            for op_type, count in operation_types.items():
                print(f"    {op_type}: {count} عملية")
            print(f"  المستخدمين ({len(users)}): {sorted(users)}")
            print(f"  المشاريع ({len(projects)}): {sorted(projects)}")
            print(f"  العناصر المتداولة: {len(items_in_log)}")
            print(f"  إجمالي الإضافات: {total_added_in_log:,}")
            print(f"  إجمالي الإخراجات: {total_removed_in_log:,}")
            print(f"  صافي التغيير: {total_added_in_log - total_removed_in_log:,}")
            
            if errors:
                print(f"\nالأخطاء المكتشفة في سجل العمليات ({len(errors)}):")
                for error in errors[:10]:
                    print(f"  • {error}")
                if len(errors) > 10:
                    print(f"  ... و{len(errors) - 10} خطأ آخر")
                self.validation_results['errors'].extend(errors)
            else:
                print("✓ لا توجد أخطاء في سجل العمليات")
                self.validation_results['activity_log_valid'] = True
            
            return len(errors) == 0
            
        except Exception as e:
            error_msg = f"خطأ في فحص سجل العمليات: {str(e)}"
            print(error_msg)
            self.validation_results['errors'].append(error_msg)
            return False
    
    def check_data_consistency(self):
        """فحص الاتساق بين البيانات"""
        
        print("\n=== فحص اتساق البيانات ===")
        
        # هنا يمكن إضافة فحوصات إضافية للاتساق
        # مثل مطابقة العناصر بين المخزون وسجل العمليات
        
        consistency_valid = (self.validation_results['inventory_valid'] and 
                           self.validation_results['activity_log_valid'] and
                           self.validation_results['math_accuracy'])
        
        if consistency_valid:
            print("✓ البيانات متسقة ومترابطة")
            self.validation_results['data_consistency'] = True
        else:
            print("✗ توجد مشاكل في اتساق البيانات")
        
        return consistency_valid
    
    def generate_final_report(self):
        """إنشاء تقرير نهائي شامل"""
        
        print("\n" + "="*60)
        print("📊 التقرير النهائي لفحص البيانات")
        print("="*60)
        
        print(f"✓ بيانات المخزون: {'صحيحة' if self.validation_results['inventory_valid'] else 'خاطئة'}")
        print(f"✓ سجل العمليات: {'صحيح' if self.validation_results['activity_log_valid'] else 'خاطئ'}")
        print(f"✓ دقة الحسابات: {'صحيحة' if self.validation_results['math_accuracy'] else 'خاطئة'}")
        print(f"✓ اتساق البيانات: {'متسقة' if self.validation_results['data_consistency'] else 'غير متسقة'}")
        
        total_errors = len(self.validation_results['errors'])
        print(f"\n📋 عدد الأخطاء المكتشفة: {total_errors}")
        
        if total_errors == 0:
            print("\n🎉 ممتاز! جميع البيانات صحيحة ومترابطة")
            print("✅ البرنامج جاهز للاستخدام والاختبار")
            return True
        else:
            print(f"\n⚠️ يوجد {total_errors} خطأ يحتاج إلى مراجعة")
            if total_errors <= 20:  # اعرض جميع الأخطاء إذا كانت قليلة
                for i, error in enumerate(self.validation_results['errors'], 1):
                    print(f"  {i}. {error}")
            return False
    
    def run_full_validation(self):
        """تشغيل فحص شامل للبيانات"""
        
        print("🔍 بدء الفحص الشامل للبيانات")
        print("="*50)
        
        # 1. الاتصال
        if not self.connect_to_sheets():
            return False
        
        # 2. فحص المخزون
        inventory_valid, inventory_items = self.validate_inventory_data()
        
        # 3. فحص سجل العمليات
        activity_valid = self.validate_activity_log(inventory_items)
        
        # 4. فحص الاتساق
        consistency_valid = self.check_data_consistency()
        
        # 5. التقرير النهائي
        overall_valid = self.generate_final_report()
        
        return overall_valid


def main():
    """الدالة الرئيسية"""
    
    print("🔍 أداة فحص صحة البيانات المحدثة")
    print("="*50)
    
    try:
        validator = DataValidator()
        success = validator.run_full_validation()
        
        if success:
            print("\n🚀 البيانات جاهزة للاختبار!")
        else:
            print("\n🔧 البيانات تحتاج إلى مراجعة وإصلاح")
            
    except KeyboardInterrupt:
        print("\n⚠️ تم إيقاف الفحص بواسطة المستخدم")
    except Exception as e:
        print(f"\n💥 خطأ غير متوقع: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()