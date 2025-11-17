#!/usr/bin/env python3
"""
اختبار قيود الفلاتر للمستخدمين العاديين
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from config.user_session import UserSession
from new_activity_filter_system import NewActivityFilterSystem

def test_admin_user():
    """اختبار المدير - يجب أن يكون لديه وصول كامل للفلاتر"""
    print("🔵 اختبار المدير...")
    
    # إنشاء جلسة مدير
    admin_session = UserSession()
    admin_session.login("Admin User", 999, is_admin=True)
    
    # إنشاء النافذة
    root = tk.Tk()
    root.withdraw()  # إخفاء النافذة الرئيسية
    
    try:
        filter_window = NewActivityFilterSystem(root, None, admin_session.username)
        filter_window.user_session = admin_session
        
        # التحقق من حالة الفلاتر
        user_combo = filter_window.filter_combos['user']
        project_combo = filter_window.filter_combos['project']
        
        print(f"   فلتر المستخدم - الحالة: {user_combo['state']}")
        print(f"   فلتر المشروع - الحالة: {project_combo['state']}")
        
        # يجب أن تكون الفلاتر مفعلة للمدير
        assert user_combo['state'] != 'disabled', "فلتر المستخدم يجب أن يكون مفعلاً للمدير"
        assert project_combo['state'] != 'disabled', "فلتر المشروع يجب أن يكون مفعلاً للمدير"
        
        print("   ✅ المدير لديه وصول كامل للفلاتر")
        
    finally:
        root.destroy()

def test_regular_user():
    """اختبار المستخدم العادي - يجب أن تكون الفلاتر مقيدة"""
    print("\n🔴 اختبار المستخدم العادي...")
    
    # إنشاء جلسة مستخدم عادي
    user_session = UserSession()
    user_session.login("محمد أحمد", 101, is_admin=False)
    
    # إنشاء النافذة
    root = tk.Tk()
    root.withdraw()  # إخفاء النافذة الرئيسية
    
    try:
        filter_window = NewActivityFilterSystem(root, user_session)
        
        # التحقق من حالة الفلاتر
        user_combo = filter_window.filter_combos['user']
        project_combo = filter_window.filter_combos['project']
        category_combo = filter_window.filter_combos['category']
        item_combo = filter_window.filter_combos['item']
        
        print(f"   فلتر المستخدم - الحالة: {user_combo['state']}, القيمة: {user_combo.get()}")
        print(f"   فلتر المشروع - الحالة: {project_combo['state']}, القيمة: {project_combo.get()}")
        print(f"   فلتر التصنيف - الحالة: {category_combo['state']}")
        print(f"   فلتر العنصر - الحالة: {item_combo['state']}")
        
        # التحقق من القيود
        assert user_combo['state'] == 'disabled', "فلتر المستخدم يجب أن يكون معطلاً للمستخدم العادي"
        assert project_combo['state'] == 'disabled', "فلتر المشروع يجب أن يكون معطلاً للمستخدم العادي"
        assert user_combo.get() == "محمد أحمد", "فلتر المستخدم يجب أن يكون محدد على اسم المستخدم"
        assert project_combo.get() == "101", "فلتر المشروع يجب أن يكون محدد على رقم مشروع المستخدم"
        
        # فلاتر التصنيف والعنصر يجب أن تبقى مفعلة
        assert category_combo['state'] != 'disabled', "فلتر التصنيف يجب أن يبقى مفعلاً"
        assert item_combo['state'] != 'disabled', "فلتر العنصر يجب أن يبقى مفعلاً"
        
        print("   ✅ الفلاتر مقيدة بشكل صحيح للمستخدم العادي")
        
        # اختبار تطبيق الفلاتر
        print("   🔄 اختبار تطبيق الفلاتر...")
        filter_window.apply_filters()
        
        print("   ✅ تم تطبيق الفلاتر بنجاح")
        
    finally:
        root.destroy()

def test_filter_logic():
    """اختبار منطق الفلترة للمستخدم العادي"""
    print("\n🟡 اختبار منطق الفلترة...")
    
    # إنشاء جلسة مستخدم عادي
    user_session = UserSession()
    user_session.login("سارة محمد", 102, is_admin=False)
    
    # إنشاء النافذة
    root = tk.Tk()
    root.withdraw()
    
    try:
        filter_window = NewActivityFilterSystem(root, user_session)
        
        # محاكاة بعض العمليات
        filter_window.all_operations = [
            {
                'اسم المستخدم': 'سارة محمد',
                'رقم المشروع': '102',
                'التصنيف': 'مواد',
                'اسم العنصر': 'عنصر 1'
            },
            {
                'اسم المستخدم': 'أحمد علي',
                'رقم المشروع': '103',
                'التصنيف': 'أدوات',
                'اسم العنصر': 'عنصر 2'
            },
            {
                'اسم المستخدم': 'سارة محمد',
                'رقم المشروع': '102',
                'التصنيف': 'أدوات',
                'اسم العنصر': 'عنصر 3'
            }
        ]
        
        # تطبيق الفلاتر
        filter_window.apply_filters()
        
        # يجب أن تظهر فقط العمليات الخاصة بالمستخدم الحالي ومشروعه
        displayed_count = len(filter_window.displayed_operations)
        expected_count = 2  # عنصران لسارة محمد في مشروع 102
        
        print(f"   العمليات المعروضة: {displayed_count}")
        print(f"   العمليات المتوقعة: {expected_count}")
        
        assert displayed_count == expected_count, f"عدد العمليات المعروضة غير صحيح: {displayed_count} بدلاً من {expected_count}"
        
        # التحقق من أن جميع العمليات المعروضة تخص المستخدم الحالي
        for operation in filter_window.displayed_operations:
            assert operation['اسم المستخدم'] == 'سارة محمد', f"عملية تخص مستخدم آخر: {operation['اسم المستخدم']}"
            assert operation['رقم المشروع'] == '102', f"عملية تخص مشروع آخر: {operation['رقم المشروع']}"
        
        print("   ✅ منطق الفلترة يعمل بشكل صحيح")
        
    finally:
        root.destroy()

if __name__ == "__main__":
    print("🧪 اختبار قيود الفلاتر للمستخدمين العاديين")
    print("=" * 50)
    
    try:
        test_admin_user()
        test_regular_user()
        test_filter_logic()
        
        print("\n✅ جميع الاختبارات نجحت!")
        print("🎉 نظام قيود الفلاتر يعمل بشكل مثالي")
        
    except Exception as e:
        print(f"\n❌ فشل في الاختبار: {e}")
        raise
    
    print("\n" + "=" * 50)
    print("انتهاء الاختبارات")