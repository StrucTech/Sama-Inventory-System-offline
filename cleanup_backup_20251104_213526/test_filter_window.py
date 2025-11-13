#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار سريع لنافذة البحث بالفلاتر الجديدة
"""

import tkinter as tk
from gui.filter_search_window import FilterSearchWindow

# محاكاة مدير الشيتس للاختبار
class MockSheetsManager:
    def get_all_items_raw(self):
        return [
            ["كمبيوتر محمول", "أجهزة كمبيوتر", "10", "مشروع أ", "2024-11-01"],
            ["ماوس", "أجهزة طرفية", "25", "مشروع ب", "2024-11-02"],
            ["كيبورد", "أجهزة طرفية", "15", "مشروع أ", "2024-11-03"],
            ["شاشة", "أجهزة كمبيوتر", "8", "مشروع ج", "2024-11-04"],
        ]
    
    def get_activity_log(self):
        return [
            ["2024-11-01 10:00", "إضافة", "كمبيوتر محمول", "10", "أحمد", "إضافة أجهزة جديدة"],
            ["2024-11-02 11:00", "إخراج", "ماوس", "5", "سارة", "توزيع على فريق التطوير"],
            ["2024-11-03 12:00", "إضافة", "كيبورد", "15", "محمد", "شراء جديد"],
            ["2024-11-04 13:00", "تعديل", "شاشة", "8", "فاطمة", "تحديث الكمية"],
        ]

def test_filter_window():
    """اختبار نافذة البحث بالفلاتر"""
    root = tk.Tk()
    root.withdraw()  # إخفاء النافذة الرئيسية
    
    mock_manager = MockSheetsManager()
    
    # إنشاء نافذة البحث
    filter_window = FilterSearchWindow(root, mock_manager)
    
    print("✅ تم إنشاء نافذة البحث بنجاح")
    
    # تشغيل التطبيق
    root.mainloop()

if __name__ == "__main__":
    test_filter_window()