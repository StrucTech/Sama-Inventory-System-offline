"""
إصلاح وإعادة ضبط هيكل الشيتات
يقوم بإعادة إنشاء الشيتات بالهيكل الصحيح
"""

import os
import sys
import gspread

# إضافة مسار المشروع
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.settings import load_config

def fix_sheets_structure():
    """إصلاح هيكل الشيتات"""
    
    print("🔧 بدء إصلاح هيكل الشيتات...")
    print("=" * 50)
    
    # تحميل الإعدادات
    config = load_config()
    if not config:
        print("❌ فشل في تحميل الإعدادات")
        return False
    
    credentials_file = config.get("credentials_file", "config/credentials.json")
    spreadsheet_name = config.get("spreadsheet_name", "Inventory Management")
    
    try:
        # الاتصال بـ Google Sheets
        print("🔗 الاتصال بـ Google Sheets...")
        client = gspread.service_account(filename=credentials_file)
        spreadsheet = client.open(spreadsheet_name)
        
        # 1. إصلاح شيت المستخدمين
        print("\n1️⃣ إصلاح شيت المستخدمين...")
        fix_users_sheet(spreadsheet)
        
        # 2. إصلاح شيت المشاريع
        print("\n2️⃣ إصلاح شيت المشاريع...")
        fix_projects_sheet(spreadsheet)
        
        # 3. إصلاح شيت المخزون
        print("\n3️⃣ إصلاح شيت المخزون...")
        fix_inventory_sheet(spreadsheet)
        
        print("\n" + "=" * 50)
        print("✅ تم إصلاح جميع الشيتات بنجاح!")
        print("🚀 يمكنك الآن تشغيل التطبيق")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في إصلاح الشيتات: {e}")
        return False

def fix_users_sheet(spreadsheet):
    """إصلاح شيت المستخدمين"""
    try:
        # محاولة الحصول على الشيت أو إنشاؤه
        try:
            users_sheet = spreadsheet.worksheet("Users")
            print("📋 تم العثور على شيت المستخدمين الموجود")
            
            # حفظ البيانات الموجودة
            existing_data = []
            try:
                all_values = users_sheet.get_all_values()
                if len(all_values) > 1:  # إذا كان هناك بيانات غير العناوين
                    existing_data = all_values[1:]  # البيانات بدون العناوين
                    print(f"💾 تم حفظ {len(existing_data)} مستخدم موجود")
            except:
                print("⚠️ لا توجد بيانات موجودة أو هناك خطأ في قراءتها")
            
            # مسح الشيت وإعادة إنشاؤه
            users_sheet.clear()
            
        except gspread.WorksheetNotFound:
            print("📋 إنشاء شيت المستخدمين جديد...")
            users_sheet = spreadsheet.add_worksheet(title="Users", rows=1000, cols=8)
            existing_data = []
        
        # إضافة العناوين الصحيحة
        headers = [
            "اسم المستخدم",      # A
            "كلمة المرور",       # B  
            "نوع المستخدم",      # C
            "رقم التعريف",       # D
            "رقم المشروع",       # E
            "تاريخ الإنشاء",      # F
            "آخر تسجيل دخول",     # G
            "الحالة"            # H
        ]
        
        users_sheet.update("A1:H1", [headers])
        print(f"✅ تم إضافة العناوين: {', '.join(headers)}")
        
        # إعادة إضافة البيانات الموجودة (إذا وجدت)
        if existing_data:
            print("🔄 إعادة إضافة البيانات الموجودة...")
            row_num = 2
            for row in existing_data:
                if len(row) > 0 and row[0].strip():  # تأكد من وجود اسم مستخدم
                    # تحويل البيانات القديمة للهيكل الجديد
                    if len(row) >= 3:  # البيانات القديمة الأساسية
                        new_row = [
                            row[0] if len(row) > 0 else "",  # اسم المستخدم
                            row[1] if len(row) > 1 else "",  # كلمة المرور
                            row[2] if len(row) > 2 else "user",  # نوع المستخدم
                            f"USR_{row_num-1:03d}",  # رقم تعريف جديد
                            "",  # رقم المشروع (فارغ)
                            row[3] if len(row) > 3 else "",  # تاريخ الإنشاء
                            row[4] if len(row) > 4 else "",  # آخر تسجيل دخول
                            row[5] if len(row) > 5 else "نشط"  # الحالة
                        ]
                        
                        users_sheet.update(f"A{row_num}:H{row_num}", [new_row])
                        row_num += 1
            
            print(f"✅ تم إعادة إضافة {row_num-2} مستخدم")
        
    except Exception as e:
        print(f"❌ خطأ في إصلاح شيت المستخدمين: {e}")

def fix_projects_sheet(spreadsheet):
    """إصلاح شيت المشاريع"""
    try:
        # محاولة الحصول على الشيت أو إنشاؤه
        try:
            projects_sheet = spreadsheet.worksheet("Projects")
            print("📋 تم العثور على شيت المشاريع الموجود")
            
            # حفظ البيانات الموجودة
            existing_data = []
            try:
                all_values = projects_sheet.get_all_values()
                if len(all_values) > 1:  # إذا كان هناك بيانات غير العناوين
                    existing_data = all_values[1:]  # البيانات بدون العناوين
                    print(f"💾 تم حفظ {len(existing_data)} مشروع موجود")
            except:
                print("⚠️ لا توجد بيانات موجودة أو هناك خطأ في قراءتها")
            
            # مسح الشيت وإعادة إنشاؤه
            projects_sheet.clear()
            
        except gspread.WorksheetNotFound:
            print("📋 إنشاء شيت المشاريع جديد...")
            projects_sheet = spreadsheet.add_worksheet(title="Projects", rows=1000, cols=7)
            existing_data = []
        
        # إضافة العناوين الصحيحة
        headers = [
            "رقم المشروع",       # A
            "اسم المشروع",       # B
            "الوصف",            # C
            "حالة المشروع",      # D
            "تاريخ الإنشاء",      # E
            "تاريخ البدء",       # F
            "تاريخ الانتهاء"     # G
        ]
        
        projects_sheet.update("A1:G1", [headers])
        print(f"✅ تم إضافة العناوين: {', '.join(headers)}")
        
        # إعادة إضافة البيانات الموجودة (إذا وجدت)
        if existing_data:
            print("🔄 إعادة إضافة البيانات الموجودة...")
            row_num = 2
            for row in existing_data:
                if len(row) > 0 and row[0].strip():  # تأكد من وجود رقم مشروع
                    projects_sheet.update(f"A{row_num}:G{row_num}", [row[:7]])  # أول 7 أعمدة فقط
                    row_num += 1
            
            print(f"✅ تم إعادة إضافة {row_num-2} مشروع")
        
    except Exception as e:
        print(f"❌ خطأ في إصلاح شيت المشاريع: {e}")

def fix_inventory_sheet(spreadsheet):
    """إصلاح شيت المخزون"""
    try:
        # محاولة الحصول على الشيت أو إنشاؤه
        try:
            inventory_sheet = spreadsheet.worksheet("Inventory")
            print("📋 تم العثور على شيت المخزون الموجود")
            
            # حفظ البيانات الموجودة
            existing_data = []
            try:
                all_values = inventory_sheet.get_all_values()
                if len(all_values) > 1:  # إذا كان هناك بيانات غير العناوين
                    existing_data = all_values[1:]  # البيانات بدون العناوين
                    print(f"💾 تم حفظ {len(existing_data)} عنصر موجود")
            except:
                print("⚠️ لا توجد بيانات موجودة أو هناك خطأ في قراءتها")
            
            # مسح الشيت وإعادة إنشاؤه
            inventory_sheet.clear()
            
        except gspread.WorksheetNotFound:
            print("📋 إنشاء شيت المخزون جديد...")
            inventory_sheet = spreadsheet.add_worksheet(title="Inventory", rows=1000, cols=4)
            existing_data = []
        
        # إضافة العناوين الصحيحة
        headers = [
            "اسم العنصر",        # A
            "الكمية المتاحة",     # B
            "رقم المشروع",       # C
            "آخر تحديث"         # D
        ]
        
        inventory_sheet.update("A1:D1", [headers])
        print(f"✅ تم إضافة العناوين: {', '.join(headers)}")
        
        # إعادة إضافة البيانات الموجودة (إذا وجدت)
        if existing_data:
            print("🔄 إعادة إضافة البيانات الموجودة...")
            row_num = 2
            for row in existing_data:
                if len(row) > 0 and row[0].strip():  # تأكد من وجود اسم عنصر
                    # تحويل البيانات القديمة للهيكل الجديد
                    if len(row) >= 2:  # البيانات القديمة الأساسية
                        new_row = [
                            row[0] if len(row) > 0 else "",  # اسم العنصر
                            row[1] if len(row) > 1 else "0",  # الكمية
                            "",  # رقم المشروع (فارغ للبيانات القديمة)
                            row[2] if len(row) > 2 else ""  # آخر تحديث
                        ]
                        
                        inventory_sheet.update(f"A{row_num}:D{row_num}", [new_row])
                        row_num += 1
            
            print(f"✅ تم إعادة إضافة {row_num-2} عنصر")
        
    except Exception as e:
        print(f"❌ خطأ في إصلاح شيت المخزون: {e}")

if __name__ == "__main__":
    success = fix_sheets_structure()
    if success:
        print("\n🎉 تم إصلاح الشيتات بنجاح!")
        print("🚀 يمكنك الآن تشغيل التطبيق باستخدام:")
        print("   python main_with_auth.py")
        print("\n📋 هيكل الشيتات الجديد:")
        print("👥 Users: اسم المستخدم | كلمة المرور | نوع المستخدم | رقم التعريف | رقم المشروع | تاريخ الإنشاء | آخر تسجيل دخول | الحالة")
        print("📁 Projects: رقم المشروع | اسم المشروع | الوصف | حالة المشروع | تاريخ الإنشاء | تاريخ البدء | تاريخ الانتهاء")
        print("📦 Inventory: اسم العنصر | الكمية المتاحة | رقم المشروع | آخر تحديث")
    else:
        print("\n❌ فشل في إصلاح الشيتات - تحقق من الإعدادات والاتصال")
    
    input("\nاضغط Enter للخروج...")