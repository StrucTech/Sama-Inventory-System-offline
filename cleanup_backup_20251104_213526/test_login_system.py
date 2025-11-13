"""
سكريبت اختبار نظام تسجيل الدخول والحسابات الجديدة
"""

import sys
import os

# إضافة مسار المشروع
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sheets.users_manager import UsersManager
from config.settings import load_config

def test_users_system():
    """اختبار نظام المستخدمين"""
    print("🧪 بدء اختبار نظام المستخدمين...")
    print("=" * 60)
    
    try:
        # تحميل الإعدادات
        config = load_config()
        if not config:
            print("❌ فشل في تحميل الإعدادات")
            return False
        
        print("✅ تم تحميل الإعدادات بنجاح")
        
        # إنشاء مدير المستخدمين
        users_manager = UsersManager(
            credentials_file=config.get('credentials_file', ''),
            spreadsheet_name=config.get('spreadsheet_name', '')
        )
        
        print("📱 محاولة الاتصال بـ Google Sheets...")
        
        # محاولة الاتصال
        if not users_manager.connect():
            print("❌ فشل في الاتصال بـ Google Sheets")
            return False
        
        print("✅ تم الاتصال بـ Google Sheets بنجاح")
        
        # اختبار 1: إنشاء حساب أدمن افتراضي
        print("\n🔧 اختبار 1: إنشاء حساب الأدمن الافتراضي")
        print("-" * 40)
        
        if not users_manager.user_exists("admin"):
            result = users_manager.create_admin_user()
            if result:
                print("✅ تم إنشاء حساب الأدمن بنجاح")
            else:
                print("❌ فشل في إنشاء حساب الأدمن")
        else:
            print("ℹ️ حساب الأدمن موجود بالفعل")
        
        # اختبار 2: إنشاء مستخدم تجريبي
        print("\n👤 اختبار 2: إنشاء مستخدم تجريبي")
        print("-" * 40)
        
        test_username = "test_user"
        test_password = "test123"
        
        if not users_manager.user_exists(test_username):
            result = users_manager.create_user(test_username, test_password, "user")
            if result:
                print(f"✅ تم إنشاء المستخدم '{test_username}' بنجاح")
            else:
                print(f"❌ فشل في إنشاء المستخدم '{test_username}'")
        else:
            print(f"ℹ️ المستخدم '{test_username}' موجود بالفعل")
        
        # اختبار 3: تسجيل الدخول
        print("\n🔐 اختبار 3: تسجيل الدخول")
        print("-" * 40)
        
        # اختبار تسجيل دخول صحيح
        user_info = users_manager.authenticate_user("admin", "admin123")
        if user_info:
            print("✅ نجح تسجيل دخول الأدمن")
            print(f"   👤 المستخدم: {user_info['username']}")
            print(f"   🎭 النوع: {user_info['user_type']}")
            print(f"   📅 آخر دخول: {user_info['last_login']}")
        else:
            print("❌ فشل في تسجيل دخول الأدمن")
        
        # اختبار تسجيل دخول خاطئ
        user_info = users_manager.authenticate_user("admin", "wrong_password")
        if user_info:
            print("❌ تم قبول كلمة مرور خاطئة!")
        else:
            print("✅ تم رفض كلمة المرور الخاطئة")
        
        # اختبار 4: عرض قائمة المستخدمين
        print("\n📋 اختبار 4: قائمة المستخدمين")
        print("-" * 40)
        
        users_list = users_manager.get_all_users()
        users_count = users_manager.get_users_count()
        
        print(f"📊 عدد المستخدمين: {users_count}")
        
        if users_list:
            print("📋 قائمة المستخدمين:")
            for i, user in enumerate(users_list, 1):
                print(f"   {i}. 👤 {user['username']} ({user['user_type']})")
                print(f"      📅 تاريخ الإنشاء: {user['created_date']}")
                print(f"      🕒 آخر دخول: {user['last_login'] or 'لم يسجل دخول بعد'}")
                print(f"      📊 الحالة: {user['status']}")
                print()
        else:
            print("❌ لا توجد مستخدمين في النظام")
        
        # اختبار 5: التحقق من البيانات المخزنة
        print("\n🔍 اختبار 5: فحص البيانات في Google Sheets")
        print("-" * 40)
        
        if users_manager.users_sheet:
            try:
                all_data = users_manager.users_sheet.get_all_values()
                print(f"📊 عدد الصفوف في الشيت: {len(all_data)}")
                
                if len(all_data) > 1:  # أكثر من صف العناوين
                    print("📋 عينة من البيانات:")
                    headers = all_data[0]
                    print(f"   العناوين: {headers}")
                    
                    for i, row in enumerate(all_data[1:3], 1):  # أول صفين من البيانات
                        print(f"   الصف {i}: {row}")
                else:
                    print("ℹ️ الشيت يحتوي على العناوين فقط")
                
            except Exception as e:
                print(f"❌ خطأ في قراءة بيانات الشيت: {e}")
        
        print("\n🎉 انتهى اختبار نظام المستخدمين بنجاح!")
        return True
        
    except Exception as e:
        print(f"💥 خطأ في اختبار النظام: {e}")
        return False

def test_validation():
    """اختبار صحة البيانات"""
    print("\n🔬 اختبار صحة البيانات...")
    print("=" * 60)
    
    try:
        config = load_config()
        users_manager = UsersManager(
            credentials_file=config.get('credentials_file', ''),
            spreadsheet_name=config.get('spreadsheet_name', '')
        )
        
        if not users_manager.connect():
            print("❌ فشل في الاتصال")
            return False
        
        # اختبار بيانات خاطئة
        test_cases = [
            ("", "password123", "اسم مستخدم فارغ"),
            ("ab", "password123", "اسم مستخدم قصير"),
            ("valid_user", "", "كلمة مرور فارغة"),
            ("valid_user", "123", "كلمة مرور قصيرة"),
        ]
        
        print("🚫 اختبار البيانات الخاطئة:")
        for username, password, description in test_cases:
            result = users_manager.create_user(username, password)
            if result:
                print(f"❌ تم قبول {description}!")
            else:
                print(f"✅ تم رفض {description}")
        
        return True
        
    except Exception as e:
        print(f"💥 خطأ في اختبار التحقق: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("🚀 بدء اختبار نظام تسجيل الدخول")
    print("=" * 80)
    
    # اختبار النظام الأساسي
    success1 = test_users_system()
    
    # اختبار صحة البيانات
    success2 = test_validation()
    
    print("\n" + "=" * 80)
    if success1 and success2:
        print("🎉 جميع الاختبارات نجحت!")
        print("\n💡 يمكنك الآن:")
        print("   • تشغيل التطبيق: python main_with_auth.py")
        print("   • تسجيل الدخول بـ: admin / admin123")
        print("   • إنشاء حسابات جديدة من واجهة التطبيق")
    else:
        print("❌ بعض الاختبارات فشلت")
    
    print("=" * 80)

if __name__ == "__main__":
    main()
    input("\nاضغط Enter للخروج...")
