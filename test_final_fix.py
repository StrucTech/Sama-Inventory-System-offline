#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
اختبار نهائي لإصلاح مشكلة الصفوف الفارغة في جداول التنبيهات
"""

print("🔎 اختبار نهائي لإصلاح الصفوف الفارغة...")
print("=" * 50)

try:
    import sys
    import os
    import time
    sys.path.append('src')
    
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import QTimer
    from main_window import MainWindow
    
    # إنشاء تطبيق وهمي
    app = QApplication([])
    
    # اختبار مع مشروع به بيانات كثيرة
    test_project = "مخزن_المواد_الغذائية"
    
    print(f"📦 اختبار المشروع: {test_project}")
    
    # التحقق من وجود الملف
    project_file = os.path.join("projects", f"{test_project}_Transactions.xlsx")
    if not os.path.exists(project_file):
        print(f"❌ ملف المشروع غير موجود!")
        exit(1)
    
    # إنشاء النافذة
    print("🔧 إنشاء النافذة الرئيسية...")
    window = MainWindow(test_project)
    
    # اختبار حالة الجداول عند الإنشاء
    print("⏱️  اختبار حالة الجداول الأولية...")
    
    def check_tables():
        print("🔍 فحص الجداول...")
        
        # فحص جدول المخزون المنخفض
        low_rows = window.low_stock_table.rowCount()
        print(f"📊 جدول المخزون المنخفض: {low_rows} صف")
        
        if low_rows > 0:
            for row in range(min(3, low_rows)):  # فحص أول 3 صفوف
                first_cell = window.low_stock_table.item(row, 0)
                if first_cell:
                    text = first_cell.text().strip()
                    print(f"   الصف {row + 1}: '{text}'")
                    if not text or text == "":
                        print(f"   ⚠️  الصف {row + 1} فارغ!")
                else:
                    print(f"   ❌ الصف {row + 1} لا يحتوي على بيانات!")
        
        # فحص جدول انتهاء الصلاحية
        expiry_rows = window.expiry_table.rowCount()
        print(f"⏰ جدول انتهاء الصلاحية: {expiry_rows} صف")
        
        if expiry_rows > 0:
            for row in range(min(3, expiry_rows)):  # فحص أول 3 صفوف
                first_cell = window.expiry_table.item(row, 0)
                if first_cell:
                    text = first_cell.text().strip()
                    print(f"   الصف {row + 1}: '{text}'")
                    if not text or text == "":
                        print(f"   ⚠️  الصف {row + 1} فارغ!")
                else:
                    print(f"   ❌ الصف {row + 1} لا يحتوي على بيانات!")
        
        print("\n📋 خلاصة النتائج:")
        if low_rows > 0 and expiry_rows > 0:
            print("✅ الجداول تحتوي على بيانات")
        else:
            print("⚠️  بعض الجداول فارغة")
    
    # فحص فوري
    check_tables()
    
    # انتظار قليل للتحديث
    print("\n⏳ انتظار التحديث الأوتوماتيكي...")
    
    def delayed_check():
        print("\n🔄 فحص بعد التحديث:")
        check_tables()
        
        print("\n" + "=" * 50)
        print("✅ انتهى الاختبار!")
        print("📝 إذا رأيت صفوف فارغة، فما زالت المشكلة موجودة")
        print("✅ إذا كانت جميع الصفوف تحتوي على بيانات، فتم حل المشكلة")
        
        app.quit()
    
    # فحص بعد تأخير
    QTimer.singleShot(1000, delayed_check)
    
    # تشغيل التطبيق لفترة قصيرة
    QTimer.singleShot(2000, app.quit)
    app.exec()

except Exception as e:
    print(f"❌ خطأ في الاختبار: {e}")
    import traceback
    traceback.print_exc()

print("\n🚀 يمكنك الآن تشغيل البرنامج للتأكد: python main.py")