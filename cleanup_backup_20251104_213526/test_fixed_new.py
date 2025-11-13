#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار النسخة المحدثة من add_item_dialog
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# إضافة المجلد للمسار
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fixed_add_item_dialog import FixedAddItemDialog

class MockSheetsManager:
    """محاكي لمدير الشيتات للاختبار"""
    
    def __init__(self):
        # بيانات وهمية للاختبار
        self.mock_data = [
            ["أسمنت", "مواد بناء", "100", "مشروع 1", "2024-01-01"],
            ["حديد", "مواد بناء", "50", "مشروع 2", "2024-01-02"],
            ["طوب", "مواد بناء", "200", "مشروع 1", "2024-01-03"],
            ["دهان", "تشطيبات", "30", "مشروع 3", "2024-01-04"],
            ["بلاط", "تشطيبات", "75", "مشروع 2", "2024-01-05"],
        ]
    
    def get_all_items(self):
        """إرجاع جميع العناصر"""
        print("📊 Mock: جلب البيانات الوهمية")
        return self.mock_data
    
    def add_item(self, name, category, quantity):
        """إضافة عنصر جديد"""
        print(f"✅ Mock: إضافة عنصر - الاسم: {name}, التصنيف: {category}, الكمية: {quantity}")
        
        # إضافة للبيانات الوهمية
        new_item = [name, category, str(quantity), "مشروع جديد", "2024-01-06"]
        self.mock_data.append(new_item)
        
        return True  # محاكاة النجاح

def test_dialog():
    """اختبار النافذة"""
    print("🚀 بدء اختبار النافذة المحدثة")
    
    # إنشاء النافذة الرئيسية
    root = tk.Tk()
    root.title("اختبار النافذة المحدثة")
    root.geometry("400x300")
    
    # مدير الشيتات الوهمي
    mock_manager = MockSheetsManager()
    
    # زر لفتح النافذة
    def open_dialog():
        print("📂 فتح نافذة الإضافة...")
        dialog = FixedAddItemDialog(root, mock_manager)
        print(f"🔄 نتيجة النافذة: {dialog.result}")
    
    open_btn = ttk.Button(root, text="فتح نافذة إضافة عنصر", command=open_dialog)
    open_btn.pack(expand=True)
    
    # زر للخروج
    quit_btn = ttk.Button(root, text="خروج", command=root.quit)
    quit_btn.pack(pady=10)
    
    print("✅ جاهز للاختبار")
    root.mainloop()

if __name__ == "__main__":
    test_dialog()