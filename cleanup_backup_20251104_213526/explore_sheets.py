#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
فحص شامل لـ Google Sheets لاكتشاف البيانات
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import gspread
import json

def explore_sheets():
    """استكشاف شامل لـ Google Sheets"""
    
    try:
        # تحميل الإعدادات
        with open('config/config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print("📋 إعدادات الملف:")
        for key, value in config.items():
            if 'key' not in key.lower() and 'secret' not in key.lower():
                print(f"  {key}: {value}")
        
        # الاتصال المباشر
        credentials_file = config.get('credentials_file', 'config/credentials.json')
        
        # التحقق من وجود ملف الاعتماد
        if not os.path.exists(credentials_file):
            print(f"❌ ملف الاعتماد غير موجود: {credentials_file}")
            return
        
        print(f"✅ ملف الاعتماد موجود: {credentials_file}")
        
        # إنشاء العميل
        gc = gspread.service_account(filename=credentials_file)
        print("✅ تم إنشاء عميل Google Sheets")
        
        # الحصول على قائمة الملفات
        print("\n📂 الملفات المتاحة:")
        all_sheets = gc.openall()
        for i, sheet in enumerate(all_sheets[:10]):  # أول 10 ملفات
            print(f"  {i+1}. {sheet.title}")
        
        # محاولة فتح الملف المحدد
        spreadsheet_name = config.get('spreadsheet_name', 'Inventory Management')
        print(f"\n🎯 محاولة فتح الملف: '{spreadsheet_name}'")
        
        try:
            spreadsheet = gc.open(spreadsheet_name)
            print(f"✅ تم فتح الملف بنجاح!")
            
            # عرض أوراق العمل
            print(f"\n📑 أوراق العمل في '{spreadsheet_name}':")
            worksheets = spreadsheet.worksheets()
            for i, ws in enumerate(worksheets):
                print(f"  {i+1}. {ws.title} ({ws.row_count} صف × {ws.col_count} عمود)")
            
            # فحص أول ورقة عمل
            if worksheets:
                first_ws = worksheets[0]
                print(f"\n🔍 فحص الورقة الأولى: '{first_ws.title}'")
                
                # جلب البيانات
                all_values = first_ws.get_all_values()
                print(f"عدد الصفوف المملوءة: {len(all_values)}")
                
                if all_values:
                    print("\n📋 أول 5 صفوف:")
                    for i, row in enumerate(all_values[:5]):
                        print(f"  صف {i+1}: {row}")
            
            # البحث عن ورقة المخزون
            inventory_sheets = [ws for ws in worksheets if 'inventory' in ws.title.lower() or 'مخزون' in ws.title.lower()]
            if inventory_sheets:
                print(f"\n📦 وجدت ورقة المخزون: '{inventory_sheets[0].title}'")
                inv_ws = inventory_sheets[0]
                inv_data = inv_ws.get_all_values()
                print(f"عدد صفوف المخزون: {len(inv_data)}")
                
                if inv_data:
                    print("\n📋 بيانات المخزون (أول 3 صفوف):")
                    for i, row in enumerate(inv_data[:3]):
                        print(f"  صف {i+1}: {row}")
            
            # البحث عن ورقة النشاط
            activity_sheets = [ws for ws in worksheets if 'activity' in ws.title.lower() or 'نشاط' in ws.title.lower() or 'log' in ws.title.lower()]
            if activity_sheets:
                print(f"\n📊 وجدت ورقة النشاط: '{activity_sheets[0].title}'")
                act_ws = activity_sheets[0]
                act_data = act_ws.get_all_values()
                print(f"عدد صفوف النشاط: {len(act_data)}")
                
                if act_data:
                    print("\n📋 بيانات النشاط (أول 3 صفوف):")
                    for i, row in enumerate(act_data[:3]):
                        print(f"  صف {i+1}: {row}")
                        
        except Exception as e:
            print(f"❌ فشل في فتح الملف '{spreadsheet_name}': {e}")
            
            # اقتراح ملفات بديلة
            print("\n💡 ربما تقصد أحد هذه الملفات:")
            for sheet in all_sheets[:5]:
                if any(word in sheet.title.lower() for word in ['inventory', 'مخزون', 'stock']):
                    print(f"  ✨ {sheet.title}")
        
    except Exception as e:
        print(f"❌ خطأ عام: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    explore_sheets()