#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 اختبار إنشاء مستخدم جديد مع رقم التعريف
===============================================

هذا الملف سيختبر إنشاء مستخدم جديد والتأكد من إنشاء رقم التعريف تلقائياً
"""

import sys
import os
import random

# إضافة مسار المشروع
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sheets.users_manager import UsersManager

def test_user_creation_with_id():
    """اختبار إنشاء مستخدم جديد مع رقم التعريف"""
    
    print("🧪 اختبار إنشاء مستخدم جديد مع رقم التعريف")
    print("="*50)
    
    # إنشاء مدير المستخدمين
    users_manager = UsersManager('config/credentials.json', 'Inventory Management')
    
    if not users_manager.connect():
        print("❌ فشل في الاتصال بـ Google Sheets!")
        return False
    
    print("✅ تم الاتصال بـ Google Sheets بنجاح")
    
    # إنشاء مستخدم تجريبي جديد
    test_number = random.randint(100, 999)
    test_username = f"test_user_{test_number}"
    test_password = f"test{test_number}"
    test_project = "PRJ_2024_001"
    
    print(f"\n👤 إنشاء مستخدم تجريبي:")
    print(f"   المستخدم: {test_username}")
    print(f"   كلمة المرور: {test_password}")
    print(f"   المشروع: {test_project}")
    
    # إنشاء المستخدم
    result = users_manager.create_user_with_project(
        username=test_username,
        password=test_password,
        user_type="user",
        project_id=test_project
    )
    
    if result:
        print("✅ تم إنشاء المستخدم بنجاح!")
        
        # التحقق من وجود رقم التعريف
        print("\n🔍 التحقق من رقم التعريف...")
        
        # تسجيل دخول للحصول على معلومات المستخدم
        user_info = users_manager.authenticate_user(test_username, test_password)
        
        if user_info:
            user_id = user_info.get('user_id', '')
            
            if user_id:
                print(f"✅ رقم التعريف تم إنشاؤه: {user_id}")
                print(f"📊 طول رقم التعريف: {len(user_id)} أحرف")
                
                # عرض جميع معلومات المستخدم
                print(f"\n📋 معلومات المستخدم الكاملة:")
                print(f"   🆔 رقم التعريف: {user_info.get('user_id', 'غير محدد')}")
                print(f"   👤 اسم المستخدم: {user_info.get('username', 'غير محدد')}")
                print(f"   🏷️ نوع المستخدم: {user_info.get('user_type', 'غير محدد')}")
                print(f"   🏗️ رقم المشروع: {user_info.get('project_id', 'غير محدد')}")
                print(f"   📅 تاريخ الإنشاء: {user_info.get('created_date', 'غير محدد')}")
                print(f"   ⏰ آخر دخول: {user_info.get('last_login', 'غير محدد')}")
                print(f"   📊 الحالة: {user_info.get('status', 'غير محدد')}")
                
                return True
            else:
                print("❌ رقم التعريف لم يتم إنشاؤه!")
                return False
        else:
            print("❌ فشل في الحصول على معلومات المستخدم!")
            return False
    else:
        print("❌ فشل في إنشاء المستخدم!")
        return False

def test_multiple_users():
    """اختبار إنشاء عدة مستخدمين والتأكد من أرقام التعريف المختلفة"""
    
    print("\n🔄 اختبار إنشاء عدة مستخدمين...")
    print("="*50)
    
    users_manager = UsersManager('config/credentials.json', 'Inventory Management')
    
    if not users_manager.connect():
        print("❌ فشل في الاتصال!")
        return False
    
    created_users = []
    user_ids = set()
    
    # إنشاء 3 مستخدمين تجريبيين
    for i in range(1, 4):
        test_number = random.randint(1000, 9999)
        test_username = f"multi_test_{test_number}"
        test_password = f"pass{test_number}"
        test_project = f"PRJ_2024_00{i}"
        
        print(f"\n👤 إنشاء المستخدم {i}: {test_username}")
        
        result = users_manager.create_user_with_project(
            username=test_username,
            password=test_password,
            user_type="user",
            project_id=test_project
        )
        
        if result:
            # الحصول على معلومات المستخدم
            user_info = users_manager.authenticate_user(test_username, test_password)
            
            if user_info:
                user_id = user_info.get('user_id', '')
                if user_id:
                    created_users.append({
                        'username': test_username,
                        'user_id': user_id,
                        'project': test_project
                    })
                    user_ids.add(user_id)
                    print(f"   ✅ رقم التعريف: {user_id}")
                else:
                    print(f"   ❌ لا يوجد رقم تعريف!")
            else:
                print(f"   ❌ فشل في الحصول على المعلومات!")
        else:
            print(f"   ❌ فشل في الإنشاء!")
    
    # التحقق من فرادة أرقام التعريف
    print(f"\n📊 نتائج اختبار الفرادة:")
    print(f"   المستخدمون المُنشأون: {len(created_users)}")
    print(f"   أرقام التعريف المختلفة: {len(user_ids)}")
    
    if len(created_users) > 0 and len(user_ids) == len(created_users):
        print("✅ جميع أرقام التعريف فريدة!")
        
        print("\n📋 ملخص المستخدمين المُنشأين:")
        for user in created_users:
            print(f"   👤 {user['username']} | ID: {user['user_id']} | المشروع: {user['project']}")
            
        return True
    else:
        print("❌ هناك أرقام تعريف مكررة!")
        return False

def main():
    """الدالة الرئيسية"""
    
    try:
        print("🚀 بدء اختبار إنشاء المستخدمين مع أرقام التعريف")
        print("="*60)
        
        # اختبار إنشاء مستخدم واحد
        success1 = test_user_creation_with_id()
        
        # اختبار إنشاء عدة مستخدمين
        success2 = test_multiple_users()
        
        print("\n" + "="*60)
        print("📊 ملخص نتائج الاختبار")
        print("="*60)
        
        if success1:
            print("✅ اختبار المستخدم الواحد: نجح")
        else:
            print("❌ اختبار المستخدم الواحد: فشل")
            
        if success2:
            print("✅ اختبار المستخدمين المتعددين: نجح")
        else:
            print("❌ اختبار المستخدمين المتعددين: فشل")
        
        if success1 and success2:
            print("\n🎉 جميع الاختبارات نجحت! أرقام التعريف تعمل بشكل صحيح")
        else:
            print("\n⚠️ بعض الاختبارات فشلت - تحقق من الكود")
        
        print("\n💡 لاختبار النظام:")
        print("1. شغل python main_with_auth.py")
        print("2. أنشئ حساب جديد")
        print("3. تأكد من أن رقم التعريف يظهر في ملف تعريف المستخدم")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n⏹️ تم إيقاف الاختبار")
    except Exception as e:
        print(f"\n❌ خطأ في الاختبار: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()