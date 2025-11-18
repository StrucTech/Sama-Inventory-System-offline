#!/usr/bin/env python3
"""
حل سريع لمشكلة Invalid JWT Signature
"""

import os
import sys
import json
import shutil
from datetime import datetime

def backup_current_credentials():
    """عمل نسخة احتياطية من الملف الحالي"""
    
    credentials_path = "config/credentials.json"
    
    if os.path.exists(credentials_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"config/credentials_backup_{timestamp}.json"
        
        try:
            shutil.copy2(credentials_path, backup_path)
            print(f"✅ تم إنشاء نسخة احتياطية: {backup_path}")
            return backup_path
        except Exception as e:
            print(f"⚠️ لم يتم إنشاء النسخة الاحتياطية: {e}")
            return None
    
    return None

def check_system_time():
    """التحقق من توقيت النظام"""
    
    print("\n🕐 فحص توقيت النظام...")
    print("-" * 30)
    
    import requests
    from datetime import datetime, timezone
    
    try:
        # الحصول على التوقيت من خادم خارجي
        response = requests.get("http://worldtimeapi.org/api/timezone/Etc/UTC", timeout=5)
        if response.status_code == 200:
            data = response.json()
            server_time = datetime.fromisoformat(data['datetime'].replace('Z', '+00:00'))
            local_time = datetime.now(timezone.utc)
            
            time_diff = abs((server_time - local_time).total_seconds())
            
            print(f"📅 وقت النظام: {local_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
            print(f"🌍 وقت الخادم: {server_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
            print(f"⏱️ الفرق: {time_diff:.1f} ثانية")
            
            if time_diff > 300:  # أكثر من 5 دقائق
                print("❌ الفرق في التوقيت كبير! هذا قد يسبب مشكلة JWT")
                print("🔧 احرص على مزامنة وقت النظام")
                return False
            else:
                print("✅ توقيت النظام صحيح")
                return True
                
    except Exception as e:
        print(f"⚠️ لم يتم التحقق من التوقيت: {e}")
        return None

def create_new_credentials_guide():
    """إنشاء دليل مفصل لإنشاء credentials جديد"""
    
    guide = """
# 🔧 دليل إنشاء Google Service Account جديد

## الخطوات:

### 1️⃣ الذهاب إلى Google Cloud Console:
   🌐 https://console.cloud.google.com

### 2️⃣ اختيار أو إنشاء مشروع:
   • إذا لم يكن لديك مشروع: اضغط "Create Project"
   • إذا كان لديك مشروع: اختره من القائمة العلوية

### 3️⃣ تفعيل Google Sheets API:
   • اذهب إلى "APIs & Services" > "Library"
   • ابحث عن "Google Sheets API"
   • اضغط عليه ثم "Enable"

### 4️⃣ إنشاء Service Account:
   • اذهب إلى "IAM & Admin" > "Service Accounts"
   • اضغط "Create Service Account"
   • اكتب اسم للحساب (مثل: inventory-service)
   • اضغط "Create and Continue"

### 5️⃣ إضافة صلاحيات (اختياري):
   • يمكنك تخطي هذه الخطوة
   • اضغط "Continue" ثم "Done"

### 6️⃣ إنشاء مفتاح JSON:
   • في قائمة Service Accounts، اضغط على الحساب المُنشأ
   • اذهب إلى تبويب "Keys"
   • اضغط "Add Key" > "Create new key"
   • اختر "JSON"
   • اضغط "Create"
   • سيتم تحميل ملف JSON

### 7️⃣ استبدال الملف:
   • احذف الملف القديم: config/credentials.json
   • انسخ الملف الجديد إلى: config/credentials.json
   • تأكد من الاسم صحيح

### 8️⃣ مشاركة Google Sheet:
   • افتح Google Sheet الخاص بك
   • اضغط "Share"
   • أضف البريد الإلكتروني للـ Service Account
   • (ستجده في الملف JSON تحت "client_email")
   • أعطه صلاحية "Editor"

## ⚠️ نصائح مهمة:
   • احتفظ بالملف في مكان آمن
   • لا تشاركه مع أحد
   • تأكد من أن توقيت النظام صحيح
   • إذا كان عندك VPN، جرب إيقافه مؤقتاً
"""

    guide_file = "GOOGLE_CREDENTIALS_GUIDE.md"
    
    try:
        with open(guide_file, 'w', encoding='utf-8') as f:
            f.write(guide)
        
        print(f"\n📖 تم إنشاء دليل مفصل: {guide_file}")
        print("🔍 اقرأ الدليل لإنشاء Service Account جديد")
        
    except Exception as e:
        print(f"❌ خطأ في إنشاء الدليل: {e}")

def quick_fix_suggestions():
    """اقتراحات الحل السريع"""
    
    print("\n🚀 حلول سريعة:")
    print("=" * 40)
    
    print("1️⃣ أسرع حل - إنشاء Service Account جديد:")
    print("   • اذهب إلى Google Cloud Console")
    print("   • أنشئ Service Account جديد")
    print("   • حمّل ملف JSON جديد")
    print("   • استبدل credentials.json")
    
    print("\n2️⃣ حل مؤقت - تحديث الوقت:")
    print("   • افتح إعدادات Windows")
    print("   • اذهب إلى Time & Language")
    print("   • اضغط 'Sync now'")
    
    print("\n3️⃣ حل تجريبي - إعادة تشغيل:")
    print("   • أعد تشغيل الكمبيوتر")
    print("   • شغّل البرنامج مرة أخرى")
    
    print("\n🎯 الأسباب الشائعة:")
    print("   ❌ ملف credentials منتهي الصلاحية")
    print("   ❌ توقيت النظام غير صحيح") 
    print("   ❌ مشكلة في الشبكة أو VPN")
    print("   ❌ ملف credentials تالف")

def main():
    """الدالة الرئيسية"""
    
    print("🔧 حل مشكلة Invalid JWT Signature")
    print("=" * 50)
    
    # نسخة احتياطية
    backup_file = backup_current_credentials()
    
    # فحص التوقيت
    time_ok = check_system_time()
    
    # الحلول المقترحة
    quick_fix_suggestions()
    
    # إنشاء دليل مفصل
    create_new_credentials_guide()
    
    print(f"\n" + "=" * 50)
    print("💡 الخطوة التالية:")
    print("   🔄 أنشئ Service Account جديد في Google Cloud Console")
    print("   📁 استبدل ملف credentials.json")
    print("   🚀 شغّل البرنامج مرة أخرى")

if __name__ == "__main__":
    main()