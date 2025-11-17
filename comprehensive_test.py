#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار شامل للنظام مع مستخدم عادي
"""

from sheets.users_manager import UsersManager
from sheets.manager import SheetsManager
import time

def comprehensive_system_test():
    print("🚀 بداية الاختبار الشامل للنظام")
    
    # إنشاء مستخدم تجريبي
    print("\n👤 إنشاء مستخدم تجريبي...")
    users_manager = UsersManager('config/credentials.json', 'Inventory Management')
    
    if users_manager.connect():
        # إنشاء مستخدم جديد
        test_user_data = users_manager.create_user_with_project(
            username="test_user_fix",
            password="123456",
            project_id="PRJ_002"
        )
        
        if test_user_data:
            print(f"✅ تم إنشاء المستخدم: {test_user_data}")
            
            # اختبار تسجيل الدخول
            print("\n🔐 اختبار تسجيل الدخول...")
            login_result = users_manager.authenticate_user("test_user_fix", "123456")
            
            if login_result:
                print(f"✅ تسجيل دخول ناجح: {login_result}")
                
                # اختبار الوصول للعناصر
                print("\n📦 اختبار الوصول لعناصر المشروع...")
                sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
                
                if sheets_manager.connect():
                    sheets_manager.current_user = login_result['username']
                    
                    # جلب عناصر المشروع
                    project_items = sheets_manager.get_items_by_project(login_result['project_id'])
                    print(f"📋 عناصر المشروع {login_result['project_id']}: {len(project_items)}")
                    
                    for item in project_items:
                        print(f"  - {item['item_name']}: {item['quantity']} {item['unit']}")
                    
                    # اختبار إضافة عنصر جديد
                    print(f"\n➕ اختبار إضافة عنصر جديد للمشروع {login_result['project_id']}...")
                    success = sheets_manager.add_item(
                        item_name="عنصر اختبار النظام المحدث",
                        category="اختبار",
                        quantity=25,
                        project_id=login_result['project_id']
                    )
                    
                    if success:
                        print("✅ تم إضافة العنصر بنجاح!")
                        
                        # التحقق من الإضافة
                        time.sleep(2)  # انتظار قصير
                        updated_items = sheets_manager.get_items_by_project(login_result['project_id'])
                        print(f"📋 العناصر بعد الإضافة: {len(updated_items)}")
                        
                        for item in updated_items:
                            print(f"  - {item['item_name']}: {item['quantity']} {item['unit']}")
                    else:
                        print("❌ فشل في إضافة العنصر")
                        
                else:
                    print("❌ فشل في الاتصال بـ SheetsManager")
                    
            else:
                print("❌ فشل في تسجيل الدخول")
        else:
            print("❌ فشل في إنشاء المستخدم")
            
        # تنظيف - حذف المستخدم التجريبي
        print("\n🧹 تنظيف البيانات التجريبية...")
        users_manager.delete_user("test_user_fix")
        
    else:
        print("❌ فشل في الاتصال بـ UsersManager")
    
    print("\n🏁 انتهى الاختبار الشامل")

if __name__ == "__main__":
    comprehensive_system_test()