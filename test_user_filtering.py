#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 اختبار النظام مع مستخدمين مختلفين
===================================

هذا سيختبر عرض البيانات حسب نوع المستخدم ومشروعه
"""

import sys
import os
import tkinter as tk

# إضافة مسار المشروع
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from new_activity_filter_system import NewActivityFilterSystem
from sheets.manager import SheetsManager

def test_user_filtering():
    """اختبار الفلترة حسب المستخدم"""
    
    print("🧪 اختبار عرض البيانات حسب المستخدم")
    print("="*50)
    
    # الاتصال بـ Google Sheets
    sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
    if not sheets_manager.connect():
        print("❌ فشل في الاتصال!")
        return
        
    print("✅ تم الاتصال بـ Google Sheets")
    
    # إنشاء نافذة جذر
    root = tk.Tk()
    root.withdraw()  # إخفاء النافذة
    
    # اختبار المدير (يرى كل شيء)
    print("\n👑 اختبار المدير (admin):")
    admin_user = {
        'username': 'admin',
        'user_type': 'admin',
        'project_id': ''
    }
    
    admin_system = NewActivityFilterSystem(
        parent=root, 
        sheets_manager=sheets_manager,
        current_user=admin_user
    )
    
    # محاكاة تحميل البيانات
    admin_system.load_operations_data()
    print(f"📊 المدير يرى: {len(admin_system.all_operations)} عملية")
    
    # اختبار مستخدم المشروع الأول
    print("\n👤 اختبار مستخدم المشروع الأول (PRJ_2024_001):")
    user1 = {
        'username': 'mohammed_prj1',
        'user_type': 'user',
        'project_id': 'PRJ_2024_001'
    }
    
    user1_system = NewActivityFilterSystem(
        parent=root, 
        sheets_manager=sheets_manager,
        current_user=user1
    )
    
    user1_system.load_operations_data()
    print(f"📊 المستخدم الأول يرى: {len(user1_system.all_operations)} عملية")
    
    # اختبار مستخدم المشروع الثاني
    print("\n👤 اختبار مستخدم المشروع الثاني (PRJ_2024_002):")
    user2 = {
        'username': 'fatma_prj2',
        'user_type': 'user',
        'project_id': 'PRJ_2024_002'
    }
    
    user2_system = NewActivityFilterSystem(
        parent=root, 
        sheets_manager=sheets_manager,
        current_user=user2
    )
    
    user2_system.load_operations_data()
    print(f"📊 المستخدم الثاني يرى: {len(user2_system.all_operations)} عملية")
    
    # اختبار مستخدم المشروع الثالث
    print("\n👤 اختبار مستخدم المشروع الثالث (PRJ_2024_003):")
    user3 = {
        'username': 'ali_prj3',
        'user_type': 'user',
        'project_id': 'PRJ_2024_003'
    }
    
    user3_system = NewActivityFilterSystem(
        parent=root, 
        sheets_manager=sheets_manager,
        current_user=user3
    )
    
    user3_system.load_operations_data()
    print(f"📊 المستخدم الثالث يرى: {len(user3_system.all_operations)} عملية")
    
    # اختبار مستخدم المشروع الرابع
    print("\n👤 اختبار مستخدم المشروع الرابع (PRJ_2024_004):")
    user4 = {
        'username': 'sara_prj4',
        'user_type': 'user',
        'project_id': 'PRJ_2024_004'
    }
    
    user4_system = NewActivityFilterSystem(
        parent=root, 
        sheets_manager=sheets_manager,
        current_user=user4
    )
    
    user4_system.load_operations_data()
    print(f"📊 المستخدم الرابع يرى: {len(user4_system.all_operations)} عملية")
    
    # تقرير الملخص
    print("\n" + "="*50)
    print("📊 ملخص اختبار الفلترة حسب المستخدم")
    print("="*50)
    
    total_admin = len(admin_system.all_operations)
    total_user1 = len(user1_system.all_operations)
    total_user2 = len(user2_system.all_operations)
    total_user3 = len(user3_system.all_operations)
    total_user4 = len(user4_system.all_operations)
    
    print(f"👑 المدير (جميع المشاريع): {total_admin} عملية")
    print(f"👤 المشروع الأول: {total_user1} عملية")
    print(f"👤 المشروع الثاني: {total_user2} عملية") 
    print(f"👤 المشروع الثالث: {total_user3} عملية")
    print(f"👤 المشروع الرابع: {total_user4} عملية")
    
    total_users = total_user1 + total_user2 + total_user3 + total_user4
    print(f"📈 إجمالي عمليات المستخدمين: {total_users}")
    
    if total_admin > 0 and total_users > 0:
        if total_users <= total_admin:
            print("✅ النظام يعمل بشكل صحيح - المستخدمون يرون أقل من أو يساوي إجمالي المدير")
        else:
            print("⚠️ قد تكون هناك مشكلة - المستخدمون يرون أكثر من المدير")
            
        if total_user1 != total_user2 or total_user2 != total_user3 or total_user3 != total_user4:
            print("✅ الفلترة تعمل - كل مستخدم يرى بيانات مختلفة")
        else:
            print("⚠️ قد تكون الفلترة لا تعمل - جميع المستخدمين يرون نفس البيانات")
    
    # عرض عينة من البيانات للمستخدم الأول
    if user1_system.all_operations:
        print(f"\n🔍 عينة من بيانات المشروع الأول:")
        for i, op in enumerate(user1_system.all_operations[:3]):
            project = op.get('رقم المشروع', 'غير محدد')
            item = op.get('اسم العنصر', 'غير محدد')
            operation = op.get('نوع العملية', 'غير محدد')
            print(f"   {i+1}. {operation} - {item} - {project}")
    
    print("\n🎮 لاختبار واجهة المستخدم:")
    print("1. شغل: python main_with_auth.py")
    print("2. سجل دخول بـ mohammed_prj1 / mohammed123")
    print("3. اضغط 'بحث في سجل العمليات'") 
    print("4. تأكد أن العنوان يظهر المشروع المحدد")
    print("5. تأكد أن البيانات تخص المشروع فقط")
    print("="*50)
    
    root.destroy()

def main():
    """الدالة الرئيسية"""
    
    try:
        test_user_filtering()
    except KeyboardInterrupt:
        print("\n⏹️ تم إيقاف الاختبار")
    except Exception as e:
        print(f"\n❌ خطأ في الاختبار: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()