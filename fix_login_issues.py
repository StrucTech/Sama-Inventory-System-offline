"""
إصلاح سريع لمشاكل Google Sheets وتسجيل الدخول
"""

import os
import sys
import json
import gspread
from google.oauth2.service_account import Credentials

def fix_google_sheets():
    """إصلاح مشاكل Google Sheets"""
    print("🔧 إصلاح Google Sheets...")
    
    # التأكد من الـ scopes الصحيحة
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    try:
        # تحميل credentials مع الـ scopes الصحيحة
        creds = Credentials.from_service_account_file(
            "config/credentials.json",
            scopes=SCOPES
        )
        
        client = gspread.authorize(creds)
        print("✅ تم الاتصال بـ Google Sheets بنجاح")
        
        # فتح أو إنشاء الـ spreadsheet
        try:
            spreadsheet = client.open("Inventory Management")
            print("✅ تم فتح Inventory Management")
        except gspread.SpreadsheetNotFound:
            print("📊 إنشاء Inventory Management جديد...")
            spreadsheet = client.create("Inventory Management")
            print("✅ تم إنشاء Inventory Management")
        
        # التأكد من وجود شيت Users
        try:
            users_sheet = spreadsheet.worksheet("Users")
            print("✅ شيت Users موجود")
        except gspread.WorksheetNotFound:
            print("👥 إنشاء شيت Users...")
            users_sheet = spreadsheet.add_worksheet(title="Users", rows="100", cols="10")
            
            # إضافة العناوين
            users_sheet.update('A1:C1', [['username', 'password', 'role']])
            
            # إضافة مستخدم admin افتراضي
            users_sheet.update('A2:C2', [['admin', 'admin123', 'admin']])
            
            print("✅ تم إنشاء شيت Users مع مستخدم admin")
        
        # فحص البيانات الموجودة
        users_data = users_sheet.get_all_values()
        if len(users_data) <= 1:
            # لا يوجد مستخدمين، إضافة admin
            users_sheet.update('A2:C2', [['admin', 'admin123', 'admin']])
            print("✅ تم إضافة مستخدم admin افتراضي")
        else:
            print(f"👥 يوجد {len(users_data) - 1} مستخدمين في النظام")
            
        # التأكد من شيت Inventory
        try:
            inventory_sheet = spreadsheet.worksheet("Inventory")
            print("✅ شيت Inventory موجود")
        except gspread.WorksheetNotFound:
            print("📦 إنشاء شيت Inventory...")
            inventory_sheet = spreadsheet.add_worksheet(title="Inventory", rows="1000", cols="10")
            
            # إضافة العناوين
            inventory_sheet.update('A1:E1', [['Item Name', 'Quantity', 'Unit Price', 'Total Value', 'Last Updated']])
            
            print("✅ تم إنشاء شيت Inventory")
            
        return True
        
    except Exception as e:
        print(f"❌ خطأ في إصلاح Google Sheets: {e}")
        return False

def create_sample_config():
    """إنشاء ملف config نموذجي"""
    print("📋 إنشاء ملف config محسن...")
    
    config = {
        "credentials_file": "config/credentials.json",
        "spreadsheet_name": "Inventory Management",
        "worksheet_name": "Inventory",
        "users_sheet": "Users",
        "activity_log_sheet": "Activity_Log",
        "google_scopes": [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ],
        "columns": {
            "item_name": "A",
            "quantity": "B", 
            "unit_price": "C",
            "total_value": "D",
            "last_updated": "E"
        },
        "window": {
            "width": 1000,
            "height": 700
        },
        "theme": "luxury"
    }
    
    with open("config/config.json", 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
    
    print("✅ تم إنشاء ملف config محسن")

def main():
    print("🚀 إصلاح مشاكل النظام...")
    print("=" * 50)
    
    # إصلاح ملف config
    create_sample_config()
    
    # إصلاح Google Sheets
    if os.path.exists("config/credentials.json"):
        if fix_google_sheets():
            print("\n🎉 تم إصلاح جميع المشاكل!")
            print("\n📋 الآن يمكنك:")
            print("1. تسجيل الدخول باستخدام:")
            print("   👤 اسم المستخدم: admin")
            print("   🔑 كلمة المرور: admin123")
            print("\n2. أو إنشاء حساب جديد من البرنامج")
            print("\n3. النظام سيتحقق من التحديثات تلقائياً")
        else:
            print("\n⚠️ فشل في إصلاح Google Sheets")
            print("تأكد من:")
            print("1. صحة ملف credentials.json")
            print("2. تفعيل Google Sheets API")
            print("3. صلاحيات service account")
    else:
        print("\n❌ ملف credentials.json غير موجود")
        print("يرجى نسخ معلومات service account من Google Cloud Console")
    
    input("\nاضغط Enter للخروج...")

if __name__ == "__main__":
    main()