#!/usr/bin/env python3
"""
حل مؤقت سريع - إعادة إنشاء ملف credentials من القالب
"""

import os
import json
import shutil
from datetime import datetime

def try_restore_from_example():
    """محاولة استخدام ملف المثال إذا كان متوفراً"""
    
    print("🔄 محاولة استعادة من ملف المثال...")
    
    example_path = "config/credentials_example.json"
    credentials_path = "config/credentials.json" 
    
    if os.path.exists(example_path):
        try:
            # قراءة ملف المثال
            with open(example_path, 'r', encoding='utf-8') as f:
                example_data = json.load(f)
            
            print("✅ تم العثور على ملف المثال")
            
            # التحقق من أنه ليس مجرد قالب فارغ
            if ("your-project-id" in str(example_data) or 
                "example" in str(example_data).lower() or
                len(example_data.get("private_key", "")) < 100):
                print("⚠️ ملف المثال يحتوي على بيانات وهمية")
                return False
            
            # نسخ ملف المثال
            shutil.copy2(example_path, credentials_path)
            print("✅ تم نسخ ملف المثال إلى credentials.json")
            return True
            
        except Exception as e:
            print(f"❌ خطأ في نسخ ملف المثال: {e}")
            return False
    
    print("❌ لم يتم العثور على ملف مثال صحيح")
    return False

def try_fix_current_credentials():
    """محاولة إصلاح ملف الإعدادات الحالي"""
    
    print("\n🔧 محاولة إصلاح الملف الحالي...")
    
    credentials_path = "config/credentials.json"
    
    if not os.path.exists(credentials_path):
        print("❌ ملف credentials.json غير موجود")
        return False
    
    try:
        # قراءة الملف
        with open(credentials_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # التحقق من وجود مشاكل شائعة
        issues_found = []
        
        # مشكلة في نهايات الأسطر
        if '\r\n' in content:
            content = content.replace('\r\n', '\n')
            issues_found.append("إصلاح نهايات الأسطر")
        
        # مشكلة في التشفير
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            print(f"❌ مشكلة في تنسيق JSON: {e}")
            return False
        
        # التحقق من المفتاح الخاص
        if "private_key" in data:
            private_key = data["private_key"]
            
            # إصلاح مشاكل شائعة في المفتاح الخاص
            if not private_key.startswith("-----BEGIN PRIVATE KEY-----"):
                print("⚠️ تنسيق المفتاح الخاص غير صحيح")
                return False
            
            # إصلاح escape sequences
            if "\\n" in private_key:
                private_key = private_key.replace("\\n", "\n")
                data["private_key"] = private_key
                issues_found.append("إصلاح تنسيق المفتاح الخاص")
        
        # حفظ الملف المُصحح
        if issues_found:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"{credentials_path}.backup_{timestamp}"
            shutil.copy2(credentials_path, backup_path)
            
            with open(credentials_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ تم إصلاح المشاكل: {', '.join(issues_found)}")
            print(f"📁 نسخة احتياطية: {backup_path}")
            return True
        else:
            print("ℹ️ لم يتم العثور على مشاكل واضحة في الملف")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في إصلاح الملف: {e}")
        return False

def regenerate_credentials_template():
    """إنشاء قالب جديد محدث"""
    
    print("\n📝 إنشاء قالب محدث...")
    
    template = {
        "type": "service_account",
        "project_id": "",
        "private_key_id": "",
        "private_key": "",
        "client_email": "",
        "client_id": "",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": ""
    }
    
    template_path = "config/credentials_template_updated.json"
    
    try:
        with open(template_path, 'w', encoding='utf-8') as f:
            json.dump(template, f, indent=2, ensure_ascii=False)
        
        print(f"✅ تم إنشاء قالب محدث: {template_path}")
        
        instructions = """
# تعليمات ملء القالب:

1. اذهب إلى: https://console.cloud.google.com
2. اختر مشروعك أو أنشئ مشروع جديد
3. اذهب إلى IAM & Admin > Service Accounts  
4. اضغط Create Service Account
5. اكتب اسم الحساب واضغط Create
6. اضغط Keys > Add Key > Create new key
7. اختر JSON واضغط Create
8. افتح الملف المُحمّل
9. انسخ جميع المحتويات إلى credentials.json
10. احذف الملف المُحمّل من Downloads

⚠️ مهم: تأكد من مشاركة Google Sheet مع البريد الإلكتروني الموجود في client_email
"""
        
        instructions_file = "HOW_TO_SETUP_CREDENTIALS.txt"
        with open(instructions_file, 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        print(f"📖 تم إنشاء التعليمات: {instructions_file}")
        
    except Exception as e:
        print(f"❌ خطأ في إنشاء القالب: {e}")

def main():
    """الدالة الرئيسية للحل المؤقت"""
    
    print("⚡ حل مؤقت سريع لمشكلة JWT")
    print("=" * 40)
    
    # 1. محاولة الاستعادة من ملف المثال
    restored = try_restore_from_example()
    
    if not restored:
        # 2. محاولة إصلاح الملف الحالي
        fixed = try_fix_current_credentials()
        
        if not fixed:
            # 3. إنشاء قالب جديد
            regenerate_credentials_template()
    
    print(f"\n" + "=" * 40)
    print("📋 الخطوات التالية:")
    
    if restored or try_fix_current_credentials():
        print("1️⃣ جرب تشغيل البرنامج الآن")
        print("2️⃣ إذا استمرت المشكلة، أنشئ Service Account جديد")
    else:
        print("1️⃣ أنشئ Service Account جديد في Google Cloud Console")
        print("2️⃣ حمّل ملف JSON الجديد")
        print("3️⃣ استبدل credentials.json بالملف الجديد")
    
    print("4️⃣ تأكد من مشاركة Google Sheet مع Service Account")

if __name__ == "__main__":
    main()