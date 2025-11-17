"""
اختبار نافذة البحث بالفلاتر مع البيانات الجديدة
"""

import os
import sys
import tkinter as tk

# إضافة مسار المشروع
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_filter_functionality():
    """اختبار وظائف الفلاتر مع البيانات الجديدة"""
    
    print("🧪 اختبار وظائف الفلاتر...")
    
    try:
        from sheets.manager import SheetsManager
        from gui.filter_search_window import FilterSearchWindow
        
        # إنشاء SheetsManager
        sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
        
        if not sheets_manager.connect():
            print("❌ فشل في الاتصال")
            return False
        
        print("✅ تم الاتصال بـ Google Sheets")
        
        # اختبار تحميل البيانات
        print("\n📊 اختبار تحميل البيانات...")
        
        # اختبار بيانات المخزون
        inventory_data = sheets_manager.get_all_items_raw()
        print(f"📦 تم تحميل {len(inventory_data)} عنصر من المخزون")
        
        if inventory_data and len(inventory_data) > 0:
            print("📋 أول 3 عناصر:")
            for i, item in enumerate(inventory_data[:3]):
                if len(item) >= 4:
                    print(f"   {i+1}. {item[0]} - {item[1]} - مشروع: {item[3]}")
        
        # اختبار سجل النشاط
        activity_data = sheets_manager.get_activity_log()
        print(f"📋 تم تحميل {len(activity_data)} إدخال من سجل النشاط")
        
        # إنشاء نافذة الفلاتر للاختبار
        print("\n🔍 اختبار إنشاء نافذة الفلاتر...")
        
        root = tk.Tk()
        root.withdraw()  # إخفاء النافذة الرئيسية
        
        # إنشاء المستخدم التجريبي
        test_user = {
            'username': 'admin',
            'user_type': 'admin',
            'user_id': 'USR_001',
            'project_id': '',
            'project_name': ''
        }
        
        # إنشاء نافذة الفلاتر
        filter_window = FilterSearchWindow(root, sheets_manager, test_user)
        
        print("✅ تم إنشاء نافذة الفلاتر بنجاح")
        
        # اختبار تطبيق فلتر معين
        print("\n🎯 اختبار فلتر التصنيف...")
        
        # تطبيق فلتر للتصنيف "مواد البناء"
        filter_window.filter_vars['category'].set("مواد البناء")
        filter_window.apply_filters()
        
        building_results = len(filter_window.filtered_results)
        print(f"📊 نتائج فلتر 'مواد البناء': {building_results} عنصر")
        
        # اختبار فلتر آخر
        print("\n🎯 اختبار فلتر المشروع...")
        
        # مسح الفلتر السابق وتطبيق فلتر المشروع
        filter_window.filter_vars['category'].set("جميع التصنيفات")
        filter_window.filter_vars['project_id'].set("PRJ_001")
        filter_window.apply_filters()
        
        project_results = len(filter_window.filtered_results)
        print(f"📊 نتائج فلتر 'PRJ_001': {project_results} عنصر")
        
        # اختبار مسح الفلاتر
        print("\n🧹 اختبار مسح الفلاتر...")
        
        filter_window.clear_filters()
        all_results = len(filter_window.filtered_results)
        print(f"📊 جميع النتائج بعد مسح الفلاتر: {all_results} عنصر")
        
        # تنظيف
        root.destroy()
        
        print(f"\n✅ اكتمل الاختبار:")
        print(f"   - إجمالي العناصر: {all_results}")
        print(f"   - مواد البناء: {building_results}")
        print(f"   - مشروع PRJ_001: {project_results}")
        
        # التحقق من أن الفلاتر تعمل
        if building_results != all_results and project_results != all_results:
            print("🎉 الفلاتر تعمل بشكل صحيح!")
            return True
        else:
            print("⚠️ قد تكون هناك مشكلة في الفلاتر")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔬 اختبار وظائف الفلاتر مع البيانات الجديدة...")
    
    success = test_filter_functionality()
    
    if success:
        print("\n🎯 النتيجة: الفلاتر تعمل بشكل صحيح!")
        print("✅ يمكنك الآن استخدام نافذة البحث بالفلاتر بثقة")
    else:
        print("\n❌ النتيجة: قد تكون هناك مشكلة في الفلاتر")
        print("🔧 قد تحتاج لمزيد من التشخيص")