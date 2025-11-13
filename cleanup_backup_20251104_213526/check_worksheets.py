"""
سكريبت للتحقق من أسماء جميع الشيتات الموجودة في Google Sheets
"""

import sys
import os
import json

# إضافة مسار المشروع
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sheets.manager import SheetsManager
from config.settings import load_config

def check_worksheets():
    """فحص جميع الشيتات الموجودة"""
    print("🔍 فحص أسماء الشيتات في Google Sheets...")
    print("=" * 60)
    
    try:
        # تحميل الإعدادات
        config = load_config()
        if not config:
            print("❌ فشل في تحميل ملف الإعدادات")
            return False
            
        print(f"📊 اسم الجدول الرئيسي: {config.get('spreadsheet_name', 'غير محدد')}")
        print("=" * 60)
        
        # إنشاء مدير الشيتات
        manager = SheetsManager(
            credentials_file=config.get('credentials_file', ''),
            spreadsheet_name=config.get('spreadsheet_name', ''),
            worksheet_name=config.get('worksheet_name', 'Inventory')
        )
        
        # محاولة الاتصال
        if not manager.connect():
            print("❌ فشل في الاتصال بـ Google Sheets")
            return False
            
        print("✅ تم الاتصال بنجاح!")
        print("\n📋 قائمة جميع الشيتات الموجودة:")
        print("-" * 40)
        
        # الحصول على قائمة جميع الشيتات
        if manager.spreadsheet:
            worksheets = manager.spreadsheet.worksheets()
            
            if not worksheets:
                print("⚠️  لا توجد شيتات في الجدول")
                return True
                
            for i, sheet in enumerate(worksheets, 1):
                # معلومات أساسية عن الشيت
                title = sheet.title
                rows = sheet.row_count
                cols = sheet.col_count
                
                # تحديد نوع الشيت
                sheet_type = "غير محدد"
                if title == config.get('worksheet_name', 'Inventory'):
                    sheet_type = "شيت المخزون الرئيسي"
                elif title == config.get('activity_log_name', 'Activity_Log'):
                    sheet_type = "شيت سجل العمليات"
                elif title.lower() in ['inventory', 'main', 'stock']:
                    sheet_type = "شيت مخزون"
                elif title.lower() in ['log', 'activity', 'history']:
                    sheet_type = "شيت سجل"
                elif title.lower() in ['data', 'raw_data', 'backup']:
                    sheet_type = "شيت بيانات"
                
                print(f"{i:2}. 📄 {title}")
                print(f"    📝 النوع: {sheet_type}")
                print(f"    📏 الأبعاد: {rows} صف × {cols} عمود")
                
                # محاولة الحصول على عدد الصفوف التي تحتوي على بيانات
                try:
                    values = sheet.get_all_values()
                    data_rows = len([row for row in values if any(cell.strip() for cell in row)])
                    print(f"    📊 صفوف تحتوي على بيانات: {data_rows}")
                except Exception:
                    print(f"    📊 صفوف تحتوي على بيانات: غير متاح")
                
                print()
                
            print(f"📈 إجمالي عدد الشيتات: {len(worksheets)}")
            
            # عرض الشيتات المُعرّفة في التكوين
            print("\n🔧 الشيتات المُعرّفة في التكوين:")
            print("-" * 40)
            print(f"📄 شيت المخزون: {config.get('worksheet_name', 'Inventory')}")
            print(f"📄 شيت السجل: {config.get('activity_log_name', 'Activity_Log')}")
            
            # التحقق من وجود الشيتات المطلوبة
            worksheet_names = [sheet.title for sheet in worksheets]
            main_sheet = config.get('worksheet_name', 'Inventory')
            log_sheet = config.get('activity_log_name', 'Activity_Log')
            
            print("\n✅ حالة الشيتات المطلوبة:")
            print("-" * 40)
            if main_sheet in worksheet_names:
                print(f"✅ شيت المخزون '{main_sheet}' موجود")
            else:
                print(f"❌ شيت المخزون '{main_sheet}' غير موجود")
                
            if log_sheet in worksheet_names:
                print(f"✅ شيت السجل '{log_sheet}' موجود")  
            else:
                print(f"❌ شيت السجل '{log_sheet}' غير موجود")
                
        else:
            print("❌ فشل في الحصول على معلومات الجدول")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ حدث خطأ: {e}")
        return False

if __name__ == "__main__":
    success = check_worksheets()
    if success:
        print("\n🎉 تم فحص الشيتات بنجاح!")
    else:
        print("\n💥 فشل في فحص الشيتات!")
    
    input("\nاضغط Enter للخروج...")