#!/usr/bin/env python3
"""
اختبار الفلاتر مع البيانات الحقيقية من Google Sheets
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_real_filters():
    """اختبار الفلاتر مع البيانات الحقيقية"""
    
    print("🧪 اختبار الفلاتر مع البيانات الحقيقية")
    print("=" * 50)
    
    from sheets.manager import SheetsManager
    from config.user_session import UserSession
    
    # الاتصال بـ Google Sheets
    sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
    
    if not sheets_manager.connect():
        print("❌ فشل في الاتصال بـ Google Sheets")
        return
    
    print("✅ تم الاتصال بـ Google Sheets")
    
    try:
        # الحصول على بيانات Activity Log
        activity_sheet = sheets_manager.spreadsheet.worksheet('Activity_Log_v2_20251108')
        all_values = activity_sheet.get_all_values()
        
        if not all_values:
            print("❌ لا توجد بيانات في شيت العمليات")
            return
        
        headers = all_values[0]
        print(f"📋 الأعمدة: {headers}")
        print(f"📊 عدد الصفوف: {len(all_values)}")
        
        # تحويل البيانات إلى قائمة dictionaries
        operations = []
        for i, row in enumerate(all_values[1:], start=2):
            if row and len(row) >= 5 and row[0]:
                operation = {}
                for j, header in enumerate(headers):
                    if j < len(row):
                        operation[header] = row[j].strip()
                    else:
                        operation[header] = ""
                operations.append(operation)
        
        print(f"📈 تم تحميل {len(operations)} عملية")
        
        # جمع إحصائيات
        users = set(op.get('اسم المستخدم', '') for op in operations if op.get('اسم المستخدم', ''))
        projects = set(op.get('رقم المشروع', '') for op in operations if op.get('رقم المشروع', ''))
        categories = set(op.get('التصنيف', '') for op in operations if op.get('التصنيف', ''))
        
        print(f"👥 المستخدمون ({len(users)}): {sorted(users)}")
        print(f"🏢 المشاريع ({len(projects)}): {sorted(projects)}")
        print(f"📦 التصنيفات ({len(categories)}): {sorted(categories)}")
        
        # اختبار فلتر المستخدم
        if users:
            test_user = list(users)[0]
            print(f"\n🔍 اختبار فلتر المستخدم: '{test_user}'")
            
            user_operations = [
                op for op in operations 
                if op.get('اسم المستخدم', '').strip() == test_user.strip()
            ]
            
            print(f"📊 عمليات المستخدم: {len(user_operations)} من أصل {len(operations)}")
            
            if user_operations:
                print("📋 عينة من العمليات:")
                for i, op in enumerate(user_operations[:3], 1):
                    print(f"  {i}. {op.get('اسم العنصر', '')} - {op.get('التصنيف', '')}")
        
        # اختبار فلتر المشروع
        if projects:
            test_project = list(projects)[0]
            print(f"\n🔍 اختبار فلتر المشروع: '{test_project}'")
            
            project_operations = [
                op for op in operations 
                if op.get('رقم المشروع', '').strip() == test_project.strip()
            ]
            
            print(f"📊 عمليات المشروع: {len(project_operations)} من أصل {len(operations)}")
        
        # اختبار فلتر التصنيف
        if categories:
            test_category = list(categories)[0]
            print(f"\n🔍 اختبار فلتر التصنيف: '{test_category}'")
            
            category_operations = [
                op for op in operations 
                if op.get('التصنيف', '').strip() == test_category.strip()
            ]
            
            print(f"📊 عمليات التصنيف: {len(category_operations)} من أصل {len(operations)}")
        
        # اختبار مجموع الفلاتر (محاكاة المستخدم العادي)
        print(f"\n🔒 اختبار مجموع الفلاتر (محاكاة مستخدم عادي)")
        
        if users and projects:
            test_user = list(users)[0]
            test_project = list(projects)[0]
            
            # العثور على مستخدم ومشروع متطابقين
            user_project_ops = [
                op for op in operations 
                if (op.get('اسم المستخدم', '').strip() == test_user.strip() and
                    op.get('رقم المشروع', '').strip() == test_project.strip())
            ]
            
            if user_project_ops:
                print(f"👤 المستخدم: {test_user}")
                print(f"🏢 المشروع: {test_project}")
                print(f"📊 العمليات المطابقة: {len(user_project_ops)}")
                
                # اختبار فلتر التصنيف الإضافي
                if categories:
                    test_category = list(categories)[0]
                    
                    filtered_ops = [
                        op for op in user_project_ops 
                        if op.get('التصنيف', '').strip() == test_category.strip()
                    ]
                    
                    print(f"📦 مع التصنيف '{test_category}': {len(filtered_ops)} عملية")
            else:
                print("⚠️ لا توجد عمليات تطابق المستخدم والمشروع المختبر")
        
        # إنشاء مستخدم وهمي لاختبار نظام UserSession
        print(f"\n🎭 اختبار نظام UserSession")
        
        if users and projects:
            # أخذ أول مستخدم ومشروع للاختبار
            real_user = list(users)[0]
            real_project = list(projects)[0] if projects else '101'
            
            user_session = UserSession()
            user_session.login(real_user, real_project, is_admin=False)
            
            print(f"👤 مستخدم الاختبار: {real_user}")
            print(f"🏢 مشروع الاختبار: {real_project}")
            
            # تطبيق منطق الفلترة
            filtered_for_user = [
                op for op in operations 
                if (op.get('اسم المستخدم', '').strip() == user_session.username and
                    op.get('رقم المشروع', '').strip() == str(user_session.project_number))
            ]
            
            print(f"📊 البيانات المرئية للمستخدم العادي: {len(filtered_for_user)} من أصل {len(operations)}")
            
            if filtered_for_user:
                print("📋 عينة من العمليات المرئية:")
                for i, op in enumerate(filtered_for_user[:5], 1):
                    print(f"  {i}. {op.get('التاريخ', '')} - {op.get('اسم العنصر', '')}")
        
        print(f"\n✅ اكتمل اختبار الفلاتر بنجاح")
        
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {e}")
        import traceback
        traceback.print_exc()
    
    print("=" * 50)

if __name__ == "__main__":
    test_real_filters()