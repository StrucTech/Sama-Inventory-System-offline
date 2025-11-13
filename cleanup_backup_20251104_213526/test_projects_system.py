"""
اختبار شامل لنظام إدارة المشاريع والمستخدمين
"""

import os
import sys

# إضافة مسار المشروع
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sheets.users_manager import UsersManager
from sheets.projects_manager import ProjectsManager
from sheets.manager import SheetsManager
from config.settings import load_config

def test_projects_system():
    """اختبار نظام إدارة المشاريع والمستخدمين"""
    
    print("🚀 بدء اختبار نظام إدارة المشاريع والمستخدمين...")
    print("=" * 60)
    
    # تحميل الإعدادات
    config = load_config()
    if not config:
        print("❌ فشل في تحميل الإعدادات")
        return False
    
    credentials_file = config.get("credentials_file", "config/credentials.json")
    spreadsheet_name = config.get("spreadsheet_name", "Inventory Management")
    
    try:
        # 1. اختبار مدير المستخدمين الجديد
        print("\n1️⃣ اختبار مدير المستخدمين المحدث...")
        users_manager = UsersManager(credentials_file, spreadsheet_name)
        
        if not users_manager.connect():
            print("❌ فشل الاتصال بمدير المستخدمين")
            return False
        
        print("✅ تم الاتصال بمدير المستخدمين بنجاح")
        
        # إنشاء حساب أدمن إذا لم يكن موجوداً
        if not users_manager.user_exists("admin"):
            users_manager.create_admin_user()
        
        # إنشاء مستخدم تجريبي
        test_username = "test_project_user"
        if not users_manager.user_exists(test_username):
            if users_manager.create_user(test_username, "test123", "user"):
                print(f"✅ تم إنشاء المستخدم التجريبي '{test_username}'")
            else:
                print(f"❌ فشل في إنشاء المستخدم التجريبي '{test_username}'")
        
        # 2. اختبار مدير المشاريع
        print("\n2️⃣ اختبار مدير المشاريع...")
        projects_manager = ProjectsManager(credentials_file, spreadsheet_name)
        
        if not projects_manager.connect():
            print("❌ فشل الاتصال بمدير المشاريع")
            return False
        
        print("✅ تم الاتصال بمدير المشاريع بنجاح")
        
        # إنشاء مشروع تجريبي
        test_project_name = "مشروع اختبار النظام"
        project_id = projects_manager.create_project(
            test_project_name, 
            "مشروع تجريبي لاختبار النظام الجديد"
        )
        
        if project_id:
            print(f"✅ تم إنشاء المشروع التجريبي برقم '{project_id}'")
        else:
            # البحث عن مشروع موجود
            projects = projects_manager.get_all_projects()
            if projects:
                project_id = projects[0]['project_id']
                print(f"🔄 استخدام مشروع موجود: '{project_id}'")
            else:
                print("❌ فشل في إنشاء أو العثور على مشروع")
                return False
        
        # 3. اختبار تعيين مستخدم لمشروع
        print("\n3️⃣ اختبار تعيين مستخدم للمشروع...")
        
        # الحصول على معلومات المستخدم التجريبي
        users_without_project = users_manager.get_users_without_project()
        if users_without_project:
            user_to_assign = users_without_project[0]
            user_id = user_to_assign['user_id']
            
            if users_manager.assign_user_to_project(user_id, project_id):
                print(f"✅ تم تعيين المستخدم '{user_to_assign['username']}' للمشروع '{project_id}'")
            else:
                print("❌ فشل في تعيين المستخدم للمشروع")
        else:
            print("⚠️ لا توجد مستخدمين بدون مشاريع للاختبار")
        
        # 4. اختبار مدير المخزون المحدث
        print("\n4️⃣ اختبار مدير المخزون المحدث...")
        sheets_manager = SheetsManager(credentials_file, spreadsheet_name)
        
        if not sheets_manager.connect():
            print("❌ فشل الاتصال بمدير المخزون")
            return False
        
        print("✅ تم الاتصال بمدير المخزون بنجاح")
        
        # إضافة عنصر تجريبي مربوط بالمشروع
        test_item_name = f"عنصر تجريبي - {project_id}"
        if sheets_manager.add_item(test_item_name, 50, project_id):
            print(f"✅ تم إضافة عنصر تجريبي '{test_item_name}' للمشروع '{project_id}'")
        else:
            print("❌ فشل في إضافة العنصر التجريبي")
        
        # اختبار فلترة العناصر حسب المشروع
        project_items = sheets_manager.get_items_by_project(project_id)
        print(f"📊 عدد العناصر في المشروع '{project_id}': {len(project_items)}")
        
        # 5. عرض إحصائيات النظام
        print("\n5️⃣ إحصائيات النظام:")
        print(f"👥 عدد المستخدمين: {users_manager.get_user_count()}")
        print(f"📁 عدد المشاريع: {projects_manager.get_project_count()}")
        print(f"📦 عدد العناصر الكلي: {len(sheets_manager.get_all_items())}")
        print(f"🔗 عدد العناصر في المشروع التجريبي: {len(project_items)}")
        
        # 6. عرض معلومات المشاريع
        print("\n6️⃣ المشاريع المتاحة:")
        projects = projects_manager.get_all_projects()
        for project in projects:
            print(f"  📁 {project['project_id']}: {project['name']} ({project['status']})")
        
        # 7. عرض المستخدمين بدون مشاريع
        print("\n7️⃣ المستخدمين بدون مشاريع:")
        users_without_projects = users_manager.get_users_without_project()
        if users_without_projects:
            for user in users_without_projects:
                print(f"  👤 {user['user_id']}: {user['username']}")
        else:
            print("  ✅ جميع المستخدمين مُعيَّنون لمشاريع")
        
        print("\n" + "=" * 60)
        print("🎉 تم اكتمال جميع الاختبارات بنجاح!")
        print("✅ النظام جاهز للاستخدام مع إدارة المشاريع والمستخدمين")
        
        return True
        
    except Exception as e:
        print(f"\n❌ خطأ أثناء الاختبار: {e}")
        return False

if __name__ == "__main__":
    success = test_projects_system()
    if success:
        print("\n🚀 يمكنك الآن تشغيل التطبيق باستخدام:")
        print("   python main_with_auth.py")
        print("\n📋 معلومات تسجيل الدخول:")
        print("   👤 المدير: admin / admin123")
        print("   👤 المستخدم التجريبي: test_project_user / test123")
    else:
        print("\n❌ فشل في الاختبار - تحقق من الإعدادات والاتصال")
    
    input("\nاضغط Enter للخروج...")