#!/usr/bin/env python3
"""
اختبار تعيين المستخدمين للمشاريع
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

def test_user_assignment():
    """اختبار تعيين المستخدم للمشروع"""
    print("🧪 اختبار تعيين المستخدم للمشروع")
    print("=" * 50)
    
    try:
        from sheets.users_manager import UsersManager
        
        # إعداد المدير
        config = {
            "credentials_file": "config/credentials.json",
            "spreadsheet_name": "Inventory Management"
        }
        
        users_manager = UsersManager(
            config["credentials_file"],
            config["spreadsheet_name"]
        )
        
        print("📡 محاولة الاتصال...")
        if not users_manager.connect():
            print("❌ فشل الاتصال")
            return
        
        print("✅ تم الاتصال بنجاح")
        
        # الحصول على قائمة المستخدمين
        print("📋 جلب قائمة المستخدمين...")
        users = users_manager.get_all_users()
        
        if not users:
            print("❌ لا توجد مستخدمين")
            return
        
        print(f"✅ تم العثور على {len(users)} مستخدم")
        
        # عرض المستخدمين
        print("\n👥 المستخدمين المتاحين:")
        for i, user in enumerate(users[:5], 1):  # عرض أول 5 فقط
            print(f"{i}. {user['username']} (ID: {user['user_id']}) - مشروع: {user.get('project_id', 'لا يوجد')}")
        
        # اختبار تعيين مستخدم
        if len(users) > 0:
            test_user = users[0]
            test_project_id = "TEST_PROJECT"
            
            print(f"\n🎯 اختبار تعيين المستخدم '{test_user['username']}' للمشروع '{test_project_id}'...")
            
            result = users_manager.assign_user_to_project(test_user['user_id'], test_project_id)
            
            if result:
                print("✅ تم التعيين بنجاح!")
                
                # التحقق من التحديث
                print("🔍 التحقق من التحديث...")
                updated_user = users_manager.get_user_by_id(test_user['user_id'])
                
                if updated_user and updated_user.get('project_id') == test_project_id:
                    print("✅ تم التحديث بنجاح في الشيت!")
                else:
                    print("❌ التحديث لم يظهر في الشيت")
                    print(f"المشروع المحدث: {updated_user.get('project_id') if updated_user else 'المستخدم غير موجود'}")
            else:
                print("❌ فشل التعيين")
        
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_user_assignment()