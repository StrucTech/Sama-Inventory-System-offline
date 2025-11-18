#!/usr/bin/env python3
"""
أداة تشخيص وإصلاح مشاكل Google Sheets API
"""

import os
import sys
import json
import gspread
from google.auth.exceptions import RefreshError
from google.oauth2.service_account import Credentials

def check_credentials_file():
    """التحقق من ملف بيانات الاعتماد"""
    
    print("🔍 فحص ملف بيانات الاعتماد...")
    print("-" * 40)
    
    credentials_path = "config/credentials.json"
    
    # التحقق من وجود الملف
    if not os.path.exists(credentials_path):
        print("❌ ملف credentials.json غير موجود!")
        print("📝 تحتاج إلى:")
        print("   1. إنشاء Service Account في Google Cloud Console")
        print("   2. تحميل ملف JSON")
        print("   3. وضعه في مجلد config باسم credentials.json")
        return False
    
    try:
        # قراءة وتحليل الملف
        with open(credentials_path, 'r', encoding='utf-8') as f:
            creds_data = json.load(f)
        
        print("✅ ملف credentials.json موجود")
        
        # التحقق من الحقول المطلوبة
        required_fields = [
            "type", "project_id", "private_key_id", 
            "private_key", "client_email", "client_id"
        ]
        
        missing_fields = []
        for field in required_fields:
            if field not in creds_data:
                missing_fields.append(field)
        
        if missing_fields:
            print(f"❌ حقول مفقودة: {missing_fields}")
            return False
        
        print("✅ جميع الحقول المطلوبة موجودة")
        
        # التحقق من نوع الخدمة
        if creds_data.get("type") != "service_account":
            print(f"❌ نوع بيانات الاعتماد خاطئ: {creds_data.get('type')}")
            print("   يجب أن يكون: service_account")
            return False
        
        print("✅ نوع بيانات الاعتماد صحيح")
        
        # معلومات إضافية
        print(f"\n📋 معلومات بيانات الاعتماد:")
        print(f"   📧 البريد الإلكتروني: {creds_data.get('client_email', 'غير محدد')}")
        print(f"   📁 المشروع: {creds_data.get('project_id', 'غير محدد')}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ خطأ في تنسيق JSON: {e}")
        return False
    except Exception as e:
        print(f"❌ خطأ في قراءة الملف: {e}")
        return False

def test_credentials_connection():
    """اختبار الاتصال بـ Google Sheets"""
    
    print("\n🔗 اختبار الاتصال بـ Google Sheets...")
    print("-" * 40)
    
    try:
        # محاولة إنشاء كائن gspread
        gc = gspread.service_account(filename="config/credentials.json")
        print("✅ تم إنشاء كائن gspread بنجاح")
        
        # اختبار الوصول لقائمة الملفات (لا يتطلب ملف محدد)
        try:
            # هذا لن يعطي خطأ JWT إذا كانت بيانات الاعتماد صحيحة
            print("🔍 اختبار صحة بيانات الاعتماد...")
            
            # محاولة الوصول لملف (سيعطي خطأ واضح إذا كانت المشكلة في الصلاحيات)
            sheets = gc.list_permissions("1BvyLiRm-test")  # ملف وهمي للاختبار
            
        except gspread.exceptions.APIError as api_error:
            if "JWT" in str(api_error) or "invalid_grant" in str(api_error):
                print("❌ مشكلة في بيانات الاعتماد (JWT signature)")
                return False
            elif "not found" in str(api_error) or "permission" in str(api_error):
                print("✅ بيانات الاعتماد صحيحة (مشكلة الصلاحية طبيعية)")
                return True
            else:
                print(f"⚠️ خطأ API آخر: {api_error}")
                return False
        except RefreshError as refresh_error:
            print(f"❌ مشكلة في تجديد الرمز المميز: {refresh_error}")
            return False
        except Exception as e:
            if "JWT" in str(e) or "invalid_grant" in str(e):
                print("❌ مشكلة في بيانات الاعتماد")
                return False
            else:
                print("✅ بيانات الاعتماد تبدو صحيحة")
                return True
            
        return True
        
    except Exception as e:
        print(f"❌ خطأ في إنشاء الاتصال: {e}")
        return False

def suggest_solutions():
    """اقتراح حلول للمشكلة"""
    
    print("\n💡 الحلول المقترحة:")
    print("=" * 40)
    
    solutions = [
        {
            "title": "1️⃣ إعادة إنشاء Service Account",
            "steps": [
                "اذهب إلى Google Cloud Console",
                "اختر مشروعك أو أنشئ مشروع جديد", 
                "اذهب إلى IAM & Admin > Service Accounts",
                "احذف Service Account القديم",
                "أنشئ Service Account جديد",
                "أنشئ مفتاح جديد (JSON)",
                "حمّل الملف واستبدل credentials.json"
            ]
        },
        {
            "title": "2️⃣ التحقق من تاريخ النظام", 
            "steps": [
                "تأكد من أن تاريخ ووقت النظام صحيح",
                "JWT tokens حساسة للوقت",
                "قم بمزامنة الوقت مع الخادم"
            ]
        },
        {
            "title": "3️⃣ إعادة تفعيل Google Sheets API",
            "steps": [
                "اذهب إلى Google Cloud Console", 
                "اذهب إلى APIs & Services > Library",
                "ابحث عن Google Sheets API",
                "تأكد من أنه مفعل",
                "إذا كان مفعل، قم بإلغاء تفعيله وإعادة تفعيله"
            ]
        },
        {
            "title": "4️⃣ التحقق من صلاحيات الملف",
            "steps": [
                "تأكد من أن ملف credentials.json قابل للقراءة",
                "تحقق من أن الملف غير تالف",
                "جرب نسخ الملف من مكان آخر"
            ]
        }
    ]
    
    for solution in solutions:
        print(f"\n🔧 {solution['title']}:")
        for i, step in enumerate(solution['steps'], 1):
            print(f"   {i}. {step}")

def create_test_credentials():
    """إنشاء ملف credentials تجريبي"""
    
    print(f"\n📝 إنشاء قالب credentials.json...")
    print("-" * 40)
    
    template = {
        "type": "service_account",
        "project_id": "your-project-id-here",
        "private_key_id": "your-private-key-id-here", 
        "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR-PRIVATE-KEY-HERE\n-----END PRIVATE KEY-----\n",
        "client_email": "your-service-account@your-project.iam.gserviceaccount.com",
        "client_id": "your-client-id-here",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
    }
    
    template_path = "config/credentials_template_new.json"
    
    try:
        with open(template_path, 'w', encoding='utf-8') as f:
            json.dump(template, f, indent=2, ensure_ascii=False)
        
        print(f"✅ تم إنشاء قالب في: {template_path}")
        print("📝 املأ القالب ببياناتك الحقيقية من Google Cloud Console")
        
    except Exception as e:
        print(f"❌ خطأ في إنشاء القالب: {e}")

def main():
    """الدالة الرئيسية"""
    
    print("🔧 أداة تشخيص مشاكل Google Sheets API")
    print("=" * 50)
    
    # فحص ملف بيانات الاعتماد
    credentials_ok = check_credentials_file()
    
    if credentials_ok:
        # اختبار الاتصال
        connection_ok = test_credentials_connection()
        
        if connection_ok:
            print("\n🎉 جميع الفحوصات نجحت!")
            print("✅ بيانات الاعتماد تبدو صحيحة")
        else:
            print("\n⚠️ مشكلة في الاتصال")
            suggest_solutions()
    else:
        print("\n❌ مشكلة في ملف بيانات الاعتماد")
        suggest_solutions()
        create_test_credentials()
    
    print(f"\n" + "=" * 50)
    print("📞 للمساعدة الإضافية، تواصل مع فريق الدعم")

if __name__ == "__main__":
    main()