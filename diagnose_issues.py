"""
اختبار سريع للتحقق من مشاكل تسجيل الدخول
"""

import os
import sys
import json
from pathlib import Path

print("🔍 فحص إعدادات النظام...")
print("=" * 50)

# فحص ملفات الإعداد
print("📁 فحص ملفات الإعداد:")

config_file = "config/config.json"
if os.path.exists(config_file):
    print(f"✅ {config_file} موجود")
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
        print(f"   📊 Spreadsheet: {config.get('spreadsheet_name', 'غير محدد')}")
else:
    print(f"❌ {config_file} مفقود")

credentials_file = "config/credentials.json"
if os.path.exists(credentials_file):
    print(f"✅ {credentials_file} موجود")
    # فحص حجم الملف
    size = os.path.getsize(credentials_file)
    print(f"   📏 حجم الملف: {size} bytes")
    if size < 100:
        print("   ⚠️ الملف صغير جداً - قد يكون فارغ أو غير صحيح")
else:
    print(f"❌ {credentials_file} مفقود")

update_file = "update_info.json"
if os.path.exists(update_file):
    print(f"✅ {update_file} موجود")
    with open(update_file, 'r', encoding='utf-8') as f:
        update_info = json.load(f)
        print(f"   🔖 الإصدار الحالي: {update_info.get('current_version', 'غير محدد')}")
        print(f"   🔗 رابط التحديث: {update_info.get('update_url', 'غير محدد')}")
else:
    print(f"❌ {update_file} مفقود")

print("\n" + "=" * 50)
print("🔧 فحص الاتصال...")

try:
    # فحص الاتصال بالإنترنت
    import requests
    response = requests.get("https://www.google.com", timeout=5)
    if response.status_code == 200:
        print("✅ الاتصال بالإنترنت يعمل")
    else:
        print("⚠️ مشكلة في الاتصال بالإنترنت")
except Exception as e:
    print(f"❌ فشل في الاتصال بالإنترنت: {e}")

try:
    # فحص Google Sheets API
    print("🔍 فحص Google Sheets API...")
    
    if os.path.exists("config/credentials.json"):
        # محاولة تحميل credentials
        import gspread
        from google.oauth2.service_account import Credentials
        
        creds = Credentials.from_service_account_file("config/credentials.json")
        client = gspread.authorize(creds)
        print("✅ تم تحميل Google credentials بنجاح")
        
        # محاولة الوصول للملف
        try:
            with open("config/config.json", 'r') as f:
                config = json.load(f)
            
            spreadsheet = client.open(config['spreadsheet_name'])
            print(f"✅ تم الاتصال بـ Google Sheet: {config['spreadsheet_name']}")
            
            # فحص الشيتس الموجودة
            worksheets = spreadsheet.worksheets()
            print(f"📋 الشيتس الموجودة: {[ws.title for ws in worksheets]}")
            
            # فحص شيت المستخدمين
            if 'Users' in [ws.title for ws in worksheets]:
                users_sheet = spreadsheet.worksheet('Users')
                users_data = users_sheet.get_all_values()
                print(f"👥 عدد المستخدمين المسجلين: {len(users_data) - 1}")  # -1 for header
                if len(users_data) > 1:
                    print("✅ يوجد مستخدمين في النظام")
                else:
                    print("⚠️ لا يوجد مستخدمين مسجلين")
            else:
                print("❌ شيت Users غير موجود")
                
        except Exception as e:
            print(f"❌ فشل في الوصول للـ Google Sheet: {e}")
            
    else:
        print("❌ ملف credentials.json غير موجود")
        
except ImportError as e:
    print(f"❌ مكتبة مفقودة: {e}")
except Exception as e:
    print(f"❌ خطأ في فحص Google Sheets: {e}")

print("\n" + "=" * 50)
print("📝 التوصيات:")

if not os.path.exists("config/credentials.json"):
    print("1. 🔑 أنشئ ملف credentials.json من Google Cloud Console")
    print("2. 📋 انسخ محتوى credentials_example.json وعدل البيانات")

print("3. 🔧 تأكد من أن Google Sheet مُشارك مع service account")
print("4. 📊 تأكد من وجود شيت 'Users' مع العمودين: username, password")
print("5. 👤 أضف مستخدم admin يدوياً في شيت Users")

input("\nاضغط Enter للخروج...")