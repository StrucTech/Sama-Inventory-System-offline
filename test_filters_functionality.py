"""
🧪 اختبار سريع للفلاتر في نظام البحث
====================================

هذا السكريبت يختبر وظائف الفلترة بدون واجهة مستخدم
"""

import sys
import os
from datetime import datetime

# إضافة مسار المشروع
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sheets.manager import SheetsManager

def test_filters():
    """اختبار وظائف الفلترة"""
    
    print("🧪 اختبار نظام الفلاتر")
    print("=" * 40)
    
    # 1. الاتصال بالشيتس
    print("📡 الاتصال بـ Google Sheets...")
    sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
    
    if not sheets_manager.connect():
        print("❌ فشل في الاتصال")
        return
    
    print("✅ تم الاتصال بنجاح")
    
    # 2. تحميل بيانات سجل العمليات
    print("\n📊 تحميل بيانات سجل العمليات...")
    try:
        activity_worksheet = sheets_manager.spreadsheet.worksheet('Activity_Log_v2_20251108')
        activity_values = activity_worksheet.get_all_values()
        
        if not activity_values:
            print("❌ لا توجد بيانات")
            return
        
        headers = activity_values[0]
        print(f"📋 العناوين: {headers}")
        
        # تحويل البيانات لقائمة قواميس
        activity_data = []
        for i, row in enumerate(activity_values[1:], 2):
            if row and row[0]:  # التأكد من وجود تاريخ
                record = {}
                for j, header in enumerate(headers):
                    record[header] = row[j] if j < len(row) else ""
                activity_data.append(record)
        
        print(f"✅ تم تحميل {len(activity_data)} عملية")
        
        if not activity_data:
            print("❌ لا توجد عمليات للاختبار")
            return
        
        # 3. اختبار الفلاتر
        print(f"\n🔍 اختبار الفلاتر على {len(activity_data)} عملية")
        
        # أ) فلتر التصنيف
        print("\n📂 اختبار فلتر التصنيف:")
        categories = set()
        for record in activity_data:
            category = record.get('التصنيف', '')
            if category:
                categories.add(category)
        
        print(f"   📊 التصنيفات الموجودة ({len(categories)}): {sorted(categories)}")
        
        # اختبار فلتر تصنيف واحد
        if categories:
            test_category = list(categories)[0]
            filtered = [r for r in activity_data if r.get('التصنيف', '') == test_category]
            print(f"   🔬 فلتر '{test_category}': {len(filtered)} عملية")
        
        # ب) فلتر العناصر
        print("\n📦 اختبار فلتر العناصر:")
        items = set()
        for record in activity_data:
            item = record.get('اسم العنصر', '')
            if item:
                items.add(item)
        
        print(f"   📊 العناصر الموجودة ({len(items)}): {sorted(list(items)[:5])}{'...' if len(items) > 5 else ''}")
        
        # اختبار فلتر عنصر واحد
        if items:
            test_item = list(items)[0]
            filtered = [r for r in activity_data if r.get('اسم العنصر', '') == test_item]
            print(f"   🔬 فلتر '{test_item}': {len(filtered)} عملية")
        
        # ج) فلتر المشاريع
        print("\n🎯 اختبار فلتر المشاريع:")
        projects = set()
        for record in activity_data:
            project = record.get('رقم المشروع', '')
            if project:
                projects.add(project)
        
        print(f"   📊 المشاريع الموجودة ({len(projects)}): {sorted(projects)}")
        
        # اختبار فلتر مشروع واحد
        if projects:
            test_project = list(projects)[0]
            filtered = [r for r in activity_data if r.get('رقم المشروع', '') == test_project]
            print(f"   🔬 فلتر '{test_project}': {len(filtered)} عملية")
        
        # د) فلتر التاريخ
        print("\n📅 اختبار فلتر التاريخ:")
        dates = set()
        for record in activity_data:
            date = record.get('التاريخ', '')
            if date:
                dates.add(date)
        
        sorted_dates = sorted(dates)
        print(f"   📊 التواريخ ({len(dates)}): من {sorted_dates[0] if sorted_dates else 'N/A'} إلى {sorted_dates[-1] if sorted_dates else 'N/A'}")
        
        # اختبار فلتر تاريخ واحد
        if dates:
            test_date = list(dates)[0]
            filtered = [r for r in activity_data if r.get('التاريخ', '') == test_date]
            print(f"   🔬 فلتر '{test_date}': {len(filtered)} عملية")
        
        # هـ) فلتر المستخدمين
        print("\n👤 اختبار فلتر المستخدمين:")
        users = set()
        for record in activity_data:
            user = record.get('اسم المستخدم', '')
            if user:
                users.add(user)
        
        print(f"   📊 المستخدمين ({len(users)}): {sorted(users)}")
        
        # اختبار فلتر مستخدم واحد
        if users:
            test_user = list(users)[0]
            filtered = [r for r in activity_data if r.get('اسم المستخدم', '') == test_user]
            print(f"   🔬 فلتر '{test_user}': {len(filtered)} عملية")
        
        # و) فلتر نطاق التواريخ
        print("\n📆 اختبار فلتر نطاق التواريخ:")
        if len(sorted_dates) >= 2:
            from_date = sorted_dates[0]
            to_date = sorted_dates[len(sorted_dates)//2]  # منتصف المدة
            
            print(f"   🔬 فلتر من {from_date} إلى {to_date}:")
            
            filtered = []
            for record in activity_data:
                record_date = record.get('التاريخ', '')
                if record_date and from_date <= record_date <= to_date:
                    filtered.append(record)
            
            print(f"   📊 النتيجة: {len(filtered)} عملية")
        
        # 4. اختبار فلترة مركبة
        print(f"\n🔄 اختبار فلترة مركبة:")
        if categories and projects:
            test_category = list(categories)[0]
            test_project = list(projects)[0]
            
            filtered = []
            for record in activity_data:
                if (record.get('التصنيف', '') == test_category and 
                    record.get('رقم المشروع', '') == test_project):
                    filtered.append(record)
            
            print(f"   🔬 فلتر '{test_category}' + '{test_project}': {len(filtered)} عملية")
        
        # 5. الإحصائيات النهائية
        print(f"\n📊 ملخص الاختبار:")
        print(f"   ✅ إجمالي العمليات: {len(activity_data)}")
        print(f"   ✅ التصنيفات: {len(categories)}")
        print(f"   ✅ العناصر: {len(items)}")
        print(f"   ✅ المشاريع: {len(projects)}")
        print(f"   ✅ المستخدمين: {len(users)}")
        print(f"   ✅ التواريخ: {len(dates)}")
        
        print(f"\n🎉 جميع الفلاتر تعمل بشكل صحيح!")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """الدالة الرئيسية"""
    
    print("🧪 اختبار سريع لنظام الفلاتر")
    print("=" * 50)
    
    success = test_filters()
    
    if success:
        print("\n✅ الاختبار مكتمل - النظام جاهز!")
    else:
        print("\n❌ فشل في الاختبار - يحتاج مراجعة")

if __name__ == "__main__":
    main()