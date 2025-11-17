"""
مسح البيانات من جميع الشيتات وإضافة بيانات جديدة منظمة
لحل مشكلة الفلاتر التي لا تعمل
"""

import os
import sys
from datetime import datetime, timedelta
import random

# إضافة مسار المشروع
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sheets.manager import SheetsManager
from sheets.users_manager import UsersManager  
from sheets.projects_manager import ProjectsManager

def clear_and_populate_sheets():
    """مسح الشيتات وإضافة بيانات جديدة منظمة"""
    
    print("🧹 بدء مسح الشيتات وإضافة بيانات جديدة...")
    
    # التأكد من وجود ملف الاعتماد
    if not os.path.exists('config/credentials.json'):
        print("❌ ملف credentials.json غير موجود")
        return False
    
    try:
        # إنشاء المديرين
        sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
        users_manager = UsersManager('config/credentials.json', 'Inventory Management')
        projects_manager = ProjectsManager('config/credentials.json', 'Inventory Management')
        
        print("📡 الاتصال بـ Google Sheets...")
        
        if not sheets_manager.connect():
            print("❌ فشل في الاتصال بـ SheetsManager")
            return False
            
        if not users_manager.connect():
            print("❌ فشل في الاتصال بـ UsersManager")
            return False
            
        if not projects_manager.connect():
            print("❌ فشل في الاتصال بـ ProjectsManager")
            return False
            
        print("✅ تم الاتصال بنجاح")
        
        # 1. مسح وإعداد شيت المخزون
        print("\n📦 مسح وإعداد شيت المخزون...")
        clear_inventory_sheet(sheets_manager)
        
        # 2. مسح وإعداد شيت المشاريع  
        print("\n📋 مسح وإعداد شيت المشاريع...")
        clear_projects_sheet(projects_manager)
        
        # 3. مسح وإعداد شيت المستخدمين
        print("\n👥 مسح وإعداد شيت المستخدمين...")
        clear_users_sheet(users_manager)
        
        # 4. إضافة بيانات جديدة منظمة
        print("\n✨ إضافة بيانات جديدة منظمة...")
        populate_with_organized_data(sheets_manager, users_manager, projects_manager)
        
        print("\n🎉 تم مسح الشيتات وإضافة البيانات الجديدة بنجاح!")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في العملية: {e}")
        import traceback
        traceback.print_exc()
        return False

def clear_inventory_sheet(sheets_manager):
    """مسح شيت المخزون مع ترك الرؤوس"""
    try:
        worksheet = sheets_manager.worksheet
        
        # الحصول على جميع البيانات
        all_values = worksheet.get_all_values()
        
        if len(all_values) > 1:  # إذا كان هناك بيانات غير الرؤوس
            # مسح جميع البيانات ما عدا الصف الأول (الرؤوس)
            range_to_clear = f"A2:Z{len(all_values)}"
            worksheet.batch_clear([range_to_clear])
            print(f"   ✅ تم مسح {len(all_values)-1} صف من شيت المخزون")
            
            # التأكد من الرؤوس الصحيحة (متطابقة مع SheetsManager)
            correct_headers = ["اسم العنصر", "التصنيف", "الكمية المتاحة", "رقم المشروع", "آخر تحديث"]
            worksheet.update('A1:E1', [correct_headers])
            print("   ✅ تم تحديث رؤوس شيت المخزون")
        else:
            print("   ℹ️ شيت المخزون فارغ")
            
    except Exception as e:
        print(f"   ❌ خطأ في مسح شيت المخزون: {e}")

def clear_projects_sheet(projects_manager):
    """مسح شيت المشاريع مع ترك الرؤوس"""
    try:
        worksheet = projects_manager.projects_sheet
        
        # الحصول على جميع البيانات
        all_values = worksheet.get_all_values()
        
        if len(all_values) > 1:  # إذا كان هناك بيانات غير الرؤوس
            # مسح جميع البيانات ما عدا الصف الأول (الرؤوس)
            range_to_clear = f"A2:Z{len(all_values)}"
            worksheet.batch_clear([range_to_clear])
            print(f"   ✅ تم مسح {len(all_values)-1} صف من شيت المشاريع")
            
            # التأكد من الرؤوس الصحيحة
            correct_headers = ["رقم المشروع", "اسم المشروع", "الوصف", "تاريخ البداية", "تاريخ النهاية", "الحالة", "الميزانية", "تاريخ الإنشاء"]
            worksheet.update('A1:H1', [correct_headers])
            print("   ✅ تم تحديث رؤوس شيت المشاريع")
        else:
            print("   ℹ️ شيت المشاريع فارغ")
            
    except Exception as e:
        print(f"   ❌ خطأ في مسح شيت المشاريع: {e}")

def clear_users_sheet(users_manager):
    """مسح شيت المستخدمين مع ترك الرؤوس"""
    try:
        worksheet = users_manager.users_sheet
        
        # الحصول على جميع البيانات
        all_values = worksheet.get_all_values()
        
        if len(all_values) > 1:  # إذا كان هناك بيانات غير الرؤوس
            # مسح جميع البيانات ما عدا الصف الأول (الرؤوس)
            range_to_clear = f"A2:Z{len(all_values)}"
            worksheet.batch_clear([range_to_clear])
            print(f"   ✅ تم مسح {len(all_values)-1} صف من شيت المستخدمين")
            
            # التأكد من الرؤوس الصحيحة
            correct_headers = ["اسم المستخدم", "كلمة المرور", "نوع المستخدم", "رقم التعريف", "رقم المشروع", "اسم المشروع", "الحالة", "تاريخ الإنشاء", "آخر تسجيل دخول"]
            worksheet.update('A1:I1', [correct_headers])
            print("   ✅ تم تحديث رؤوس شيت المستخدمين")
        else:
            print("   ℹ️ شيت المستخدمين فارغ")
            
    except Exception as e:
        print(f"   ❌ خطأ في مسح شيت المستخدمين: {e}")

def populate_with_organized_data(sheets_manager, users_manager, projects_manager):
    """إضافة بيانات منظمة وجديدة للاختبار"""
    
    # 1. إضافة المشاريع أولاً
    print("   📋 إضافة مشاريع جديدة...")
    projects_data = [
        ["PRJ_001", "مشروع البناء الأول", "بناء مجمع سكني", "2025-01-01", "2025-12-31", "نشط", "1000000", datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
        ["PRJ_002", "مشروع الكهرباء", "تمديدات كهربائية", "2025-02-01", "2025-08-31", "نشط", "500000", datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
        ["PRJ_003", "مشروع السباكة", "أعمال السباكة", "2025-03-01", "2025-09-30", "مكتمل", "300000", datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
    ]
    
    try:
        projects_manager.projects_sheet.update('A2:H4', projects_data)
        print(f"   ✅ تم إضافة {len(projects_data)} مشروع")
    except Exception as e:
        print(f"   ❌ خطأ في إضافة المشاريع: {e}")
    
    # 2. إضافة المستخدمين  
    print("   👥 إضافة مستخدمين جدد...")
    users_data = [
        ["admin", "admin123", "admin", "USR_001", "", "", "نشط", datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ""],
        ["محمد_أحمد", "pass123", "user", "USR_002", "PRJ_001", "مشروع البناء الأول", "نشط", datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ""],
        ["سارة_علي", "pass456", "user", "USR_003", "PRJ_002", "مشروع الكهرباء", "نشط", datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ""],
        ["أحمد_محمود", "pass789", "user", "USR_004", "PRJ_003", "مشروع السباكة", "نشط", datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ""]
    ]
    
    try:
        users_manager.users_sheet.update('A2:I5', users_data)
        print(f"   ✅ تم إضافة {len(users_data)} مستخدم")
    except Exception as e:
        print(f"   ❌ خطأ في إضافة المستخدمين: {e}")
    
    # 3. إضافة عناصر المخزون مع بيانات متنوعة للفلترة
    print("   📦 إضافة عناصر مخزون متنوعة...")
    
    # عناصر مختلفة بتصنيفات وتواريخ مختلفة
    today = datetime.now()
    inventory_data = []
    
    # مواد البناء - مشروع 1
    building_items = [
        ["أسمنت", "مواد البناء", "50", "PRJ_001", (today - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')],
        ["حديد تسليح 12مم", "مواد البناء", "100", "PRJ_001", (today - timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S')],
        ["طوب أحمر", "مواد البناء", "1000", "PRJ_001", (today - timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S')],
        ["رمل", "مواد البناء", "200", "PRJ_001", (today - timedelta(days=4)).strftime('%Y-%m-%d %H:%M:%S')],
    ]
    
    # أدوات كهربائية - مشروع 2
    electrical_items = [
        ["كابل كهربائي 2.5مم", "أدوات كهربائية", "500", "PRJ_002", (today - timedelta(days=5)).strftime('%Y-%m-%d %H:%M:%S')],
        ["مفاتيح كهربائية", "أدوات كهربائية", "20", "PRJ_002", (today - timedelta(days=6)).strftime('%Y-%m-%d %H:%M:%S')],
        ["لمبات LED", "أدوات كهربائية", "30", "PRJ_002", (today - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')],
        ["قاطع كهربائي", "أدوات كهربائية", "15", "PRJ_002", today.strftime('%Y-%m-%d %H:%M:%S')],
    ]
    
    # أدوات سباكة - مشروع 3  
    plumbing_items = [
        ["أنابيب PVC", "أدوات سباكة", "80", "PRJ_003", (today - timedelta(days=8)).strftime('%Y-%m-%d %H:%M:%S')],
        ["صنابير مياه", "أدوات سباكة", "25", "PRJ_003", (today - timedelta(days=9)).strftime('%Y-%m-%d %H:%M:%S')],
        ["مضخة مياه", "أدوات سباكة", "2", "PRJ_003", (today - timedelta(days=10)).strftime('%Y-%m-%d %H:%M:%S')],
        ["خزان مياه", "أدوات سباكة", "5", "PRJ_003", (today - timedelta(days=11)).strftime('%Y-%m-%d %H:%M:%S')],
    ]
    
    # أدوات عامة - بدون مشروع
    general_items = [
        ["مطرقة", "أدوات عامة", "10", "", (today - timedelta(days=12)).strftime('%Y-%m-%d %H:%M:%S')],
        ["مفك براغي", "أدوات عامة", "15", "", (today - timedelta(days=13)).strftime('%Y-%m-%d %H:%M:%S')],
        ["شريط قياس", "أدوات عامة", "8", "", (today - timedelta(days=14)).strftime('%Y-%m-%d %H:%M:%S')],
    ]
    
    # دمج جميع العناصر
    inventory_data = building_items + electrical_items + plumbing_items + general_items
    
    try:
        # إضافة البيانات على دفعات
        start_row = 2
        for i in range(0, len(inventory_data), 10):  # إضافة 10 عناصر في كل مرة
            batch = inventory_data[i:i+10]
            end_row = start_row + len(batch) - 1
            range_name = f"A{start_row}:E{end_row}"
            sheets_manager.worksheet.update(range_name, batch)
            start_row = end_row + 1
            
        print(f"   ✅ تم إضافة {len(inventory_data)} عنصر مخزون")
        print("      - 4 عناصر مواد بناء (PRJ_001)")
        print("      - 4 عناصر أدوات كهربائية (PRJ_002)")  
        print("      - 4 عناصر أدوات سباكة (PRJ_003)")
        print("      - 3 عناصر أدوات عامة (بدون مشروع)")
        
    except Exception as e:
        print(f"   ❌ خطأ في إضافة المخزون: {e}")

if __name__ == "__main__":
    print("🧹 مسح وإعادة تنظيم البيانات للاختبار...")
    
    confirm = input("⚠️ هل أنت متأكد من حذف جميع البيانات؟ (اكتب 'نعم' للمتابعة): ")
    
    if confirm.lower() in ['نعم', 'yes', 'y']:
        success = clear_and_populate_sheets()
        if success:
            print("\n✅ تم الانتهاء بنجاح! يمكنك الآن اختبار الفلاتر.")
            print("📋 البيانات الجديدة:")
            print("   - 3 مشاريع (PRJ_001, PRJ_002, PRJ_003)")
            print("   - 4 مستخدمين (1 مدير، 3 مستخدمين عاديين)")
            print("   - 15 عنصر مخزون بتصنيفات ومشاريع مختلفة")
            print("   - تواريخ متنوعة من آخر 14 يوم")
        else:
            print("\n❌ فشلت العملية!")
    else:
        print("❌ تم إلغاء العملية")