#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار نافذة الفلاتر مع البيانات الفعلية من Google Sheets
"""

import tkinter as tk
from gui.filter_search_window import FilterSearchWindow
import gspread
import json
import os

class RealSheetsManager:
    """مدير حقيقي للشيتس مع البيانات الفعلية"""
    
    def __init__(self):
        try:
            # تحميل الإعدادات
            with open('config/config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # الاتصال بـ Google Sheets
            credentials_file = config.get('credentials_file', 'config/credentials.json')
            spreadsheet_name = config.get('spreadsheet_name', 'Inventory Management')
            
            self.gc = gspread.service_account(filename=credentials_file)
            self.spreadsheet = self.gc.open(spreadsheet_name)
            
            print("✅ تم الاتصال بـ Google Sheets")
            
        except Exception as e:
            print(f"❌ خطأ في الاتصال: {e}")
            self.gc = None
            self.spreadsheet = None
    
    def get_all_items_raw(self):
        """جلب جميع بيانات المخزون"""
        try:
            if not self.spreadsheet:
                return []
            
            # البحث عن ورقة المخزون
            worksheets = self.spreadsheet.worksheets()
            inventory_ws = None
            
            for ws in worksheets:
                if 'inventory' in ws.title.lower() or 'مخزون' in ws.title.lower():
                    inventory_ws = ws
                    break
            
            if not inventory_ws:
                print("❌ لم يتم العثور على ورقة المخزون")
                return []
            
            # جلب البيانات
            all_values = inventory_ws.get_all_values()
            
            # إرجاع البيانات بدون العناوين
            data = all_values[1:] if len(all_values) > 1 else []
            print(f"📦 تم جلب {len(data)} عنصر من المخزون")
            
            return data
            
        except Exception as e:
            print(f"❌ خطأ في جلب بيانات المخزون: {e}")
            return []
    
    def get_activity_log(self):
        """جلب سجل النشاط"""
        try:
            if not self.spreadsheet:
                return []
            
            # البحث عن ورقة النشاط
            worksheets = self.spreadsheet.worksheets()
            activity_ws = None
            
            for ws in worksheets:
                if any(word in ws.title.lower() for word in ['activity', 'نشاط', 'log']):
                    activity_ws = ws
                    break
            
            if not activity_ws:
                print("❌ لم يتم العثور على ورقة النشاط")
                return []
            
            # جلب البيانات
            all_values = activity_ws.get_all_values()
            
            # إرجاع البيانات بدون العناوين
            data = all_values[1:] if len(all_values) > 1 else []
            print(f"📊 تم جلب {len(data)} إدخال من سجل النشاط")
            
            return data
            
        except Exception as e:
            print(f"❌ خطأ في جلب سجل النشاط: {e}")
            return []

def test_real_filter_window():
    """اختبار نافذة الفلاتر مع البيانات الحقيقية"""
    root = tk.Tk()
    root.withdraw()  # إخفاء النافذة الرئيسية
    
    # إنشاء مدير الشيتس الحقيقي
    real_manager = RealSheetsManager()
    
    print("="*60)
    print("🧪 اختبار نافذة البحث مع البيانات الحقيقية")
    print("="*60)
    
    # عرض عينة من البيانات
    items = real_manager.get_all_items_raw()
    activity = real_manager.get_activity_log()
    
    print(f"\n📦 عينة من بيانات المخزون:")
    for i, item in enumerate(items[:3]):
        print(f"  {i+1}. {item}")
    
    print(f"\n📊 عينة من سجل النشاط:")
    for i, log in enumerate(activity[:3]):
        print(f"  {i+1}. {log}")
    
    # استخراج العناصر والتصنيفات الفريدة
    unique_items = set()
    unique_categories = set()
    
    for item in items:
        if len(item) >= 2:
            if item[0]:  # اسم العنصر
                unique_items.add(item[0])
            if item[1]:  # التصنيف
                unique_categories.add(item[1])
    
    print(f"\n🏷️ العناصر الفريدة ({len(unique_items)}):")
    for item_name in sorted(list(unique_items)):
        print(f"  - {item_name}")
    
    print(f"\n📂 التصنيفات الفريدة ({len(unique_categories)}):")
    for category in sorted(list(unique_categories)):
        print(f"  - {category}")
    
    # إنشاء نافذة البحث
    print(f"\n🔍 إنشاء نافذة البحث...")
    filter_window = FilterSearchWindow(root, real_manager)
    
    print(f"\n✅ النافذة جاهزة! جرب الفلاتر:")
    print(f"1. اختر تصنيف مثل: 'أدوات معدنية'")
    print(f"2. اختر عنصر مثل: 'مسامير اختبار'")
    print(f"3. جرب أيقونات التاريخ")
    print("="*60)
    
    # تشغيل التطبيق
    root.mainloop()

if __name__ == "__main__":
    test_real_filter_window()