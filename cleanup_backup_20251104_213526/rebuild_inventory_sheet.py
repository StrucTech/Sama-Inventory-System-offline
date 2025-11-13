#!/usr/bin/env python3
"""
Script to rebuild the inventory sheet with the new category column.
This will delete the existing inventory sheet and create a new one with proper headers.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sheets.manager import SheetsManager
from config.settings import load_config
import gspread
from google.auth import default

def rebuild_inventory_sheet():
    """Delete and rebuild the inventory sheet with new structure."""
    print("🔄 إعادة بناء شيت المخزن مع التصنيفات...")
    
    try:
        # Load configuration
        config = load_config()
        if not config:
            print("❌ خطأ في تحميل الإعدادات")
            return False
        
        # Initialize Google Sheets client directly
        print("🔗 الاتصال بـ Google Sheets...")
        
        # Load credentials
        credentials_path = config.get('credentials_path', 'config/credentials.json')
        gc = gspread.service_account(filename=credentials_path)
        
        # Open the spreadsheet
        spreadsheet_name = config.get('spreadsheet_name', 'Inventory Management')
        spreadsheet = gc.open(spreadsheet_name)
        
        print(f"📊 فتح جدول البيانات: {spreadsheet_name}")
        
        # Check if inventory worksheet exists and delete it
        worksheet_name = config.get('inventory_worksheet', 'Inventory')
        
        try:
            existing_worksheet = spreadsheet.worksheet(worksheet_name)
            print(f"🗑️ حذف الشيت الموجود: {worksheet_name}")
            spreadsheet.del_worksheet(existing_worksheet)
            print("✅ تم حذف الشيت القديم بنجاح")
        except gspread.WorksheetNotFound:
            print(f"ℹ️ الشيت {worksheet_name} غير موجود، سيتم إنشاؤه من جديد")
        
        # Create new worksheet with proper structure
        print(f"➕ إنشاء شيت جديد: {worksheet_name}")
        new_worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows=1000, cols=10)
        
        # Set up the new headers
        headers = ["اسم العنصر", "التصنيف", "الكمية المتاحة", "رقم المشروع", "آخر تحديث"]
        print("📝 إعداد العناوين الجديدة...")
        new_worksheet.update(range_name="A1:E1", values=[headers])
        
        # Format headers
        print("🎨 تنسيق العناوين...")
        new_worksheet.format("A1:E1", {
            "backgroundColor": {"red": 0.8, "green": 0.8, "blue": 0.8},
            "textFormat": {"bold": True, "fontSize": 12},
            "horizontalAlignment": "CENTER"
        })
        
        print("✅ تم إعادة بناء شيت المخزن بنجاح!")
        print("\n📋 الهيكل الجديد:")
        print("العمود A: اسم العنصر")
        print("العمود B: التصنيف ⭐ جديد")
        print("العمود C: الكمية المتاحة")
        print("العمود D: رقم المشروع")
        print("العمود E: آخر تحديث")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في إعادة بناء الشيت: {e}")
        return False

def add_sample_data():
    """Add some sample data with categories to test the new structure."""
    print("\n➕ إضافة بيانات تجريبية...")
    
    try:
        # Initialize sheets manager with new structure
        config = load_config()
        sheets_manager = SheetsManager(config)
        
        if not sheets_manager.initialize():
            print("❌ فشل في تهيئة مدير الجداول")
            return False
        
        # Sample items with categories
        sample_items = [
            ("مسامير حديد 3 سم", "أدوات معدنية", 500, "PROJ001"),
            ("أسمنت أبيض كيس 50 كيلو", "مواد البناء", 20, "PROJ001"),
            ("كابل كهرباء 2.5 مم", "أدوات كهربائية", 100, "PROJ002"),
            ("طلاء أحمر لتر", "دهانات ومواد التشطيب", 15, "PROJ002"),
            ("براغي معدنية 5 سم", "أدوات معدنية", 200, "PROJ001"),
        ]
        
        for item_name, category, quantity, project_id in sample_items:
            try:
                success = sheets_manager.add_item(item_name, category, quantity, project_id)
                if success:
                    print(f"✅ تمت الإضافة: {item_name} | {category}")
                else:
                    print(f"❌ فشل في إضافة: {item_name}")
            except Exception as e:
                print(f"❌ خطأ في إضافة {item_name}: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في إضافة البيانات التجريبية: {e}")
        return False

if __name__ == "__main__":
    print("🔧 أداة إعادة بناء شيت المخزن مع التصنيفات")
    print("=" * 60)
    
    # Ask for confirmation
    print("⚠️ تحذير: هذه العملية ستحذف شيت المخزن الحالي وتُعيد بناءه!")
    confirm = input("هل أنت متأكد؟ اكتب 'نعم' للمتابعة: ")
    
    if confirm.lower() in ['نعم', 'yes', 'y']:
        print("\n🚀 بدء إعادة البناء...")
        
        # Rebuild the sheet
        if rebuild_inventory_sheet():
            print("\n🎯 هل تريد إضافة بيانات تجريبية؟")
            add_sample = input("اكتب 'نعم' لإضافة عناصر تجريبية: ")
            
            if add_sample.lower() in ['نعم', 'yes', 'y']:
                add_sample_data()
            
            print("\n🎉 تمت العملية بنجاح!")
            print("💡 يمكنك الآن تشغيل التطبيق وستجد عمود التصنيف")
            print("🚀 شغّل: python main_with_auth.py")
        else:
            print("\n❌ فشلت العملية")
    else:
        print("❌ تم إلغاء العملية")