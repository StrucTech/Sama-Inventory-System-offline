#!/usr/bin/env python3
"""
اختبار منطق الفلاتر فقط بدون واجهة
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def simulate_filter_logic():
    """محاكاة منطق الفلاتر"""
    
    print("🧪 اختبار منطق الفلاتر")
    print("=" * 50)
    
    # بيانات تجريبية
    all_operations = [
        {
            'التاريخ': '2024-01-15',
            'اسم العنصر': 'مسامير حديد 10مم',
            'التصنيف': 'مواد البناء',
            'اسم المستخدم': 'سارة محمد',
            'رقم المشروع': '102'
        },
        {
            'التاريخ': '2024-01-15',
            'اسم العنصر': 'أسمنت أبيض 50كغ',
            'التصنيف': 'مواد البناء',
            'اسم المستخدم': 'أحمد علي',
            'رقم المشروع': '103'
        },
        {
            'التاريخ': '2024-01-15',
            'اسم العنصر': 'مثقاب كهربائي',
            'التصنيف': 'أدوات',
            'اسم المستخدم': 'سارة محمد',
            'رقم المشروع': '102'
        },
        {
            'التاريخ': '2024-01-15',
            'اسم العنصر': 'طلاء أبيض 4لتر',
            'التصنيف': 'مواد التشطيب',
            'اسم المستخدم': 'محمد حسن',
            'رقم المشروع': '101'
        },
        {
            'التاريخ': '2024-01-15',
            'اسم العنصر': 'مفاتيح كهربائية',
            'التصنيف': 'كهربائيات',
            'اسم المستخدم': 'سارة محمد',
            'رقم المشروع': '102'
        }
    ]
    
    print(f"📊 إجمالي العمليات: {len(all_operations)}")
    
    # اختبار 1: بدون فلاتر
    print("\n🔍 اختبار 1: بدون فلاتر")
    filtered = all_operations.copy()
    print(f"النتيجة: {len(filtered)} عنصر")
    
    # اختبار 2: فلتر المستخدم
    print("\n🔍 اختبار 2: فلتر المستخدم = 'سارة محمد'")
    selected_user = 'سارة محمد'
    filtered = [
        op for op in all_operations 
        if op.get('اسم المستخدم', '').strip() == selected_user.strip()
    ]
    print(f"النتيجة: {len(filtered)} عنصر")
    for op in filtered:
        print(f"  - {op['اسم العنصر']} ({op['اسم المستخدم']})")
    
    # اختبار 3: فلتر المستخدم + المشروع
    print(f"\n🔍 اختبار 3: المستخدم = 'سارة محمد' + المشروع = '102'")
    selected_project = '102'
    filtered = [
        op for op in all_operations 
        if (op.get('اسم المستخدم', '').strip() == selected_user.strip() and
            op.get('رقم المشروع', '').strip() == selected_project.strip())
    ]
    print(f"النتيجة: {len(filtered)} عنصر")
    for op in filtered:
        print(f"  - {op['اسم العنصر']} (مشروع: {op['رقم المشروع']})")
    
    # اختبار 4: إضافة فلتر التصنيف
    print(f"\n🔍 اختبار 4: المستخدم + المشروع + التصنيف = 'أدوات'")
    selected_category = 'أدوات'
    filtered = [
        op for op in all_operations 
        if (op.get('اسم المستخدم', '').strip() == selected_user.strip() and
            op.get('رقم المشروع', '').strip() == selected_project.strip() and
            op.get('التصنيف', '').strip() == selected_category.strip())
    ]
    print(f"النتيجة: {len(filtered)} عنصر")
    for op in filtered:
        print(f"  - {op['اسم العنصر']} ({op['التصنيف']})")
    
    # اختبار 5: فلتر غير موجود
    print(f"\n🔍 اختبار 5: المستخدم + المشروع + التصنيف = 'غير موجود'")
    selected_category = 'غير موجود'
    filtered = [
        op for op in all_operations 
        if (op.get('اسم المستخدم', '').strip() == selected_user.strip() and
            op.get('رقم المشروع', '').strip() == selected_project.strip() and
            op.get('التصنيف', '').strip() == selected_category.strip())
    ]
    print(f"النتيجة: {len(filtered)} عنصر")
    
    # عرض التصنيفات المتاحة
    available_categories = set(op.get('التصنيف', '').strip() for op in all_operations if op.get('التصنيف', '').strip())
    print(f"التصنيفات المتاحة: {sorted(available_categories)}")
    
    # اختبار منطق UserSession
    print(f"\n🔒 اختبار منطق UserSession")
    
    from config.user_session import UserSession
    
    # مستخدم عادي
    user_session = UserSession()
    user_session.login("سارة محمد", 102, is_admin=False)
    
    print(f"نوع المستخدم: {'مدير' if user_session.is_admin else 'عادي'}")
    print(f"اسم المستخدم: {user_session.username}")
    print(f"رقم المشروع: {user_session.project_number}")
    
    # تطبيق منطق الفلترة للمستخدم العادي
    if not user_session.is_admin:
        auto_user = user_session.username
        auto_project = str(user_session.project_number)
        
        filtered = [
            op for op in all_operations 
            if (op.get('اسم المستخدم', '').strip() == auto_user.strip() and
                op.get('رقم المشروع', '').strip() == auto_project.strip())
        ]
        
        print(f"فلترة تلقائية للمستخدم العادي: {len(filtered)} عنصر")
        for op in filtered:
            print(f"  - {op['اسم العنصر']} ({op['التصنيف']})")
    
    print("\n" + "=" * 50)
    print("✅ انتهاء اختبار منطق الفلاتر")

if __name__ == "__main__":
    simulate_filter_logic()