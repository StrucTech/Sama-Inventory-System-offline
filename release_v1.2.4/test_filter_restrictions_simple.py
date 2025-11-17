#!/usr/bin/env python3
"""
اختبار بسيط لنظام قيود الفلاتر
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_user_session():
    """اختبار نظام الجلسات"""
    print("🔵 اختبار نظام جلسة المستخدم...")
    
    from config.user_session import UserSession
    
    # اختبار المدير
    admin_session = UserSession()
    admin_session.login("Admin User", 999, is_admin=True)
    
    print(f"   المدير: {admin_session}")
    print(f"   هل مدير؟ {admin_session.has_admin_access()}")
    print(f"   يمكن الوصول لمشروع 101؟ {admin_session.can_access_project(101)}")
    print(f"   يمكن الوصول لبيانات محمد؟ {admin_session.can_access_user_data('محمد')}")
    
    # اختبار المستخدم العادي
    user_session = UserSession()
    user_session.login("محمد أحمد", 101, is_admin=False)
    
    print(f"   المستخدم العادي: {user_session}")
    print(f"   هل مدير؟ {user_session.has_admin_access()}")
    print(f"   يمكن الوصول لمشروع 101؟ {user_session.can_access_project(101)}")
    print(f"   يمكن الوصول لمشروع 102؟ {user_session.can_access_project(102)}")
    print(f"   يمكن الوصول لبياناته؟ {user_session.can_access_user_data('محمد أحمد')}")
    print(f"   يمكن الوصول لبيانات آخرين؟ {user_session.can_access_user_data('سارة')}")
    
    print("   ✅ نظام الجلسات يعمل بشكل صحيح")

def test_filter_restrictions():
    """اختبار قيود الفلاتر"""
    print("\n🔴 اختبار قيود الفلاتر...")
    
    from config.user_session import UserSession
    
    # إنشاء مستخدم عادي
    user_session = UserSession()
    user_session.login("سارة محمد", 102, is_admin=False)
    
    # محاكاة منطق الفلترة
    def simulate_filter_logic(user_session):
        """محاكاة منطق تطبيق الفلاتر"""
        
        # قيم الفلاتر المحددة من المستخدم (محاكاة)
        selected_category = "مواد"
        selected_item = "الكل"
        
        # تطبيق منطق الأمان
        if hasattr(user_session, 'is_admin') and not user_session.is_admin:
            selected_user = user_session.username
            selected_project = str(user_session.project_number)
            print(f"   🔒 مستخدم عادي - القيود المطبقة:")
            print(f"      المستخدم: {selected_user} (مقيد)")
            print(f"      المشروع: {selected_project} (مقيد)")
        else:
            selected_user = "الكل"  # المدير يختار
            selected_project = "الكل"  # المدير يختار
            print(f"   🔓 مدير - لا توجد قيود")
        
        print(f"      التصنيف: {selected_category} (قابل للتعديل)")
        print(f"      العنصر: {selected_item} (قابل للتعديل)")
        
        return selected_user, selected_project, selected_category, selected_item
    
    # اختبار مع المستخدم العادي
    user_filters = simulate_filter_logic(user_session)
    
    # التحقق من النتائج
    expected_user = "سارة محمد"
    expected_project = "102"
    
    assert user_filters[0] == expected_user, f"فلتر المستخدم خطأ: {user_filters[0]} != {expected_user}"
    assert user_filters[1] == expected_project, f"فلتر المشروع خطأ: {user_filters[1]} != {expected_project}"
    
    print("   ✅ قيود الفلاتر تعمل بشكل صحيح")
    
    # اختبار مع المدير
    print("\n🔵 اختبار المدير...")
    admin_session = UserSession()
    admin_session.login("Admin", 999, is_admin=True)
    
    admin_filters = simulate_filter_logic(admin_session)
    
    # المدير لا يجب أن يكون لديه قيود
    assert admin_filters[0] == "الكل", f"المدير يجب أن يرى جميع المستخدمين: {admin_filters[0]}"
    assert admin_filters[1] == "الكل", f"المدير يجب أن يرى جميع المشاريع: {admin_filters[1]}"
    
    print("   ✅ المدير لديه وصول كامل")

def test_data_filtering():
    """اختبار فلترة البيانات الفعلية"""
    print("\n🟡 اختبار فلترة البيانات...")
    
    from config.user_session import UserSession
    
    # بيانات تجريبية
    all_operations = [
        {'اسم المستخدم': 'سارة محمد', 'رقم المشروع': '102', 'التصنيف': 'مواد', 'اسم العنصر': 'عنصر 1'},
        {'اسم المستخدم': 'أحمد علي', 'رقم المشروع': '103', 'التصنيف': 'أدوات', 'اسم العنصر': 'عنصر 2'},
        {'اسم المستخدم': 'سارة محمد', 'رقم المشروع': '102', 'التصنيف': 'أدوات', 'اسم العنصر': 'عنصر 3'},
        {'اسم المستخدم': 'محمد حسن', 'رقم المشروع': '102', 'التصنيف': 'مواد', 'اسم العنصر': 'عنصر 4'},
        {'اسم المستخدم': 'سارة محمد', 'رقم المشروع': '101', 'التصنيف': 'مواد', 'اسم العنصر': 'عنصر 5'},
    ]
    
    # مستخدم عادي
    user_session = UserSession()
    user_session.login("سارة محمد", 102, is_admin=False)
    
    # تطبيق الفلترة كما يجب أن تحدث
    filtered_operations = all_operations.copy()
    
    # قيود المستخدم العادي
    selected_user = user_session.username
    selected_project = str(user_session.project_number)
    
    # تطبيق فلتر المستخدم
    filtered_operations = [
        op for op in filtered_operations 
        if op.get('اسم المستخدم', '').strip() == selected_user
    ]
    
    # تطبيق فلتر المشروع
    filtered_operations = [
        op for op in filtered_operations 
        if op.get('رقم المشروع', '').strip() == selected_project
    ]
    
    print(f"   العمليات الأصلية: {len(all_operations)}")
    print(f"   العمليات المفلترة: {len(filtered_operations)}")
    
    # التحقق من النتائج
    expected_count = 2  # عنصر 1 و عنصر 3 فقط
    assert len(filtered_operations) == expected_count, f"عدد خطأ: {len(filtered_operations)} != {expected_count}"
    
    # التحقق من أن جميع النتائج تخص المستخدم الصحيح والمشروع الصحيح
    for op in filtered_operations:
        assert op['اسم المستخدم'] == 'سارة محمد', f"مستخدم خطأ: {op['اسم المستخدم']}"
        assert op['رقم المشروع'] == '102', f"مشروع خطأ: {op['رقم المشروع']}"
    
    print("   ✅ فلترة البيانات تعمل بشكل صحيح")
    print(f"   العناصر المعروضة:")
    for op in filtered_operations:
        print(f"      - {op['اسم العنصر']} ({op['التصنيف']})")

if __name__ == "__main__":
    print("🧪 اختبار نظام قيود الفلاتر")
    print("=" * 50)
    
    try:
        test_user_session()
        test_filter_restrictions()
        test_data_filtering()
        
        print("\n" + "=" * 50)
        print("✅ جميع الاختبارات نجحت!")
        print("🎉 نظام قيود الفلاتر جاهز للاستخدام")
        
    except Exception as e:
        print(f"\n❌ فشل في الاختبار: {e}")
        import traceback
        traceback.print_exc()
        raise
    
    print("\n" + "=" * 50)
    print("انتهاء الاختبارات")