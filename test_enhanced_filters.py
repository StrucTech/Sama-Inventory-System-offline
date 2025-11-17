#!/usr/bin/env python3
"""
اختبار سريع لنظام الفلاتر المحسن
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_filter_system():
    """اختبار نظام الفلاتر مع بيانات تجريبية"""
    
    print("🧪 اختبار نظام الفلاتر المحسن")
    print("=" * 50)
    
    from config.user_session import UserSession
    from new_activity_filter_system import NewActivityFilterSystem
    import tkinter as tk
    
    # إنشاء بيانات تجريبية
    sample_operations = [
        {
            'التاريخ': '2024-01-15',
            'الوقت': '10:30',
            'نوع العملية': 'إدخال',
            'اسم العنصر': 'مسامير حديد 10مم',
            'التصنيف': 'مواد البناء',
            'الكمية المضافة': '100',
            'الكمية المخرجة': '0',
            'اسم المستخدم': 'سارة محمد',
            'رقم المشروع': '102'
        },
        {
            'التاريخ': '2024-01-15',
            'الوقت': '11:00', 
            'نوع العملية': 'سحب',
            'اسم العنصر': 'أسمنت أبيض 50كغ',
            'التصنيف': 'مواد البناء',
            'الكمية المضافة': '0',
            'الكمية المخرجة': '5',
            'اسم المستخدم': 'أحمد علي',
            'رقم المشروع': '103'
        },
        {
            'التاريخ': '2024-01-15',
            'الوقت': '12:15',
            'نوع العملية': 'تعديل',
            'اسم العنصر': 'مثقاب كهربائي',
            'التصنيف': 'أدوات',
            'الكمية المضافة': '2',
            'الكمية المخرجة': '0',
            'اسم المستخدم': 'سارة محمد',
            'رقم المشروع': '102'
        },
        {
            'التاريخ': '2024-01-15',
            'الوقت': '14:30',
            'نوع العملية': 'سحب',
            'اسم العنصر': 'طلاء أبيض 4لتر',
            'التصنيف': 'مواد التشطيب',
            'الكمية المضافة': '0',
            'الكمية المخرجة': '3',
            'اسم المستخدم': 'محمد حسن',
            'رقم المشروع': '101'
        },
        {
            'التاريخ': '2024-01-15',
            'الوقت': '15:45',
            'نوع العملية': 'إدخال',
            'اسم العنصر': 'مفاتيح كهربائية',
            'التصنيف': 'كهربائيات',
            'الكمية المضافة': '20',
            'الكمية المخرجة': '0',
            'اسم المستخدم': 'سارة محمد',
            'رقم المشروع': '102'
        }
    ]
    
    # اختبار مع مستخدم عادي
    print("🔴 اختبار المستخدم العادي...")
    user_session = UserSession()
    user_session.login("سارة محمد", 102, is_admin=False)
    
    # إنشاء نظام فلاتر وهمي
    root = tk.Tk()
    root.withdraw()  # إخفاء النافذة
    
    try:
        # إنشاء كائن النظام
        filter_system = NewActivityFilterSystem(root, None, user_session.username)
        filter_system.user_session = user_session
        
        # إضافة البيانات التجريبية
        filter_system.all_operations = sample_operations
        
        # إعداد الفلاتر المتاحة
        filter_system.available_categories = set()
        filter_system.available_users = set()
        filter_system.available_projects = set()
        filter_system.available_items = set()
        
        for op in sample_operations:
            filter_system.available_categories.add(op.get('التصنيف', ''))
            filter_system.available_users.add(op.get('اسم المستخدم', ''))
            filter_system.available_projects.add(op.get('رقم المشروع', ''))
            filter_system.available_items.add(op.get('اسم العنصر', ''))
        
        # اختبار تطبيق الفلاتر مباشرة
        print(f"📊 البيانات الأصلية: {len(filter_system.all_operations)} عنصر")
        
        # محاكاة فلاتر
        filter_system.filter_combos = {
            'category': type('Combo', (), {'get': lambda: 'الكل'}),
            'user': type('Combo', (), {'get': lambda: 'الكل'}),
            'project': type('Combo', (), {'get': lambda: 'الكل'}),
            'item': type('Combo', (), {'get': lambda: 'الكل'})
        }
        
        # تطبيق الفلاتر
        filter_system.apply_filters()
        
        # فحص النتائج
        expected_count = len([op for op in sample_operations 
                            if op.get('اسم المستخدم') == 'سارة محمد' 
                            and op.get('رقم المشروع') == '102'])
        
        actual_count = len(filter_system.displayed_operations)
        
        print(f"📈 النتيجة المتوقعة: {expected_count}")
        print(f"📉 النتيجة الفعلية: {actual_count}")
        
        if actual_count == expected_count:
            print("✅ المستخدم العادي - الفلاتر تعمل بشكل صحيح!")
        else:
            print("❌ المستخدم العادي - مشكلة في الفلاتر!")
            
        # اختبار فلتر التصنيف
        print("\n🔍 اختبار فلتر التصنيف...")
        filter_system.filter_combos['category'] = type('Combo', (), {'get': lambda: 'أدوات'})
        
        filter_system.apply_filters()
        
        tools_count = len([op for op in sample_operations 
                          if op.get('اسم المستخدم') == 'سارة محمد' 
                          and op.get('رقم المشروع') == '102'
                          and op.get('التصنيف') == 'أدوات'])
        
        actual_tools_count = len(filter_system.displayed_operations)
        
        print(f"📈 المتوقع (أدوات): {tools_count}")
        print(f"📉 الفعلي (أدوات): {actual_tools_count}")
        
        if actual_tools_count == tools_count:
            print("✅ فلتر التصنيف يعمل بشكل صحيح!")
        else:
            print("❌ مشكلة في فلتر التصنيف!")
            
    finally:
        root.destroy()
    
    print("\n" + "=" * 50)
    print("انتهاء الاختبار")

if __name__ == "__main__":
    test_filter_system()