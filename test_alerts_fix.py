#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
اختبار سريع للتأكد من إصلاح مشكلة الصفوف الفارغة في جداول التنبيهات
"""

print("🧪 اختبار إصلاح جداول التنبيهات...")
print("=" * 50)

try:
    # استيراد النظام
    import sys
    import os
    sys.path.append('src')
    
    from PyQt6.QtWidgets import QApplication
    from main_window import MainWindow
    
    # إنشاء تطبيق وهمي للاختبار
    app = QApplication([])
    
    # اختبار مع مشروع تجريبي
    test_projects = ["مخزن_المواد_الغذائية", "pepsi", "cocacola"]
    
    for project in test_projects:
        print(f"\n📦 اختبار المشروع: {project}")
        
        # التحقق من وجود الملف
        project_file = os.path.join("projects", f"{project}_Transactions.xlsx")
        if not os.path.exists(project_file):
            print(f"   ⚠️  ملف المشروع غير موجود: {project_file}")
            continue
        
        try:
            # إنشاء نافذة للاختبار
            window = MainWindow(project)
            
            # اختبار دوال التحديث
            print(f"   🔄 تحديث التنبيهات...")
            window.clear_alert_tables()
            window.update_low_stock_alerts()
            window.update_expiry_alerts()
            
            # فحص عدد الصفوف
            low_stock_rows = window.low_stock_table.rowCount()
            expiry_rows = window.expiry_table.rowCount()
            
            print(f"   📊 جدول المخزون المنخفض: {low_stock_rows} صف")
            print(f"   ⏰ جدول انتهاء الصلاحية: {expiry_rows} صف")
            
            # فحص محتوى الصفوف الأولى
            if low_stock_rows > 0:
                first_item = window.low_stock_table.item(0, 0)
                if first_item and first_item.text().strip():
                    print(f"   ✅ أول عنصر في المخزون المنخفض: {first_item.text()}")
                else:
                    print(f"   ❌ الصف الأول في المخزون المنخفض فارغ!")
            
            if expiry_rows > 0:
                first_expiry = window.expiry_table.item(0, 0)
                if first_expiry and first_expiry.text().strip():
                    print(f"   ✅ أول عنصر في تنبيهات الصلاحية: {first_expiry.text()}")
                else:
                    print(f"   ❌ الصف الأول في تنبيهات الصلاحية فارغ!")
            
        except Exception as e:
            print(f"   ❌ خطأ في اختبار المشروع {project}: {e}")
    
    print("\n" + "=" * 50)
    print("✅ انتهى الاختبار!")
    print("📋 إذا ظهرت رسائل '✅' فالإصلاح نجح")
    print("⚠️  إذا ظهرت رسائل '❌' فما زالت هناك مشكلة")

except Exception as e:
    print(f"❌ خطأ عام في الاختبار: {e}")
    print("تأكد من أن جميع المكتبات مثبتة بشكل صحيح")

print("\n🚀 يمكنك الآن تشغيل البرنامج: python main.py")