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
        
        # Sample existing items
        self.existing_items = [
            {"item_name": "مسامير حديد", "category": "أدوات معدنية"},
            {"item_name": "أسمنت أبيض", "category": "مواد البناء"},
            {"item_name": "كابل كهرباء", "category": "أدوات كهربائية"},
            {"item_name": "طلاء أحمر", "category": "دهانات ومواد التشطيب"},
        ]
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup test UI."""
        # Title
        title_label = tk.Label(self.root, text="اختبار الحوار المصحح", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # Description
        desc_text = """
الإصلاحات المطبقة:
✅ إجبار المستخدم على اختيار وضع الإضافة
✅ عدم إظهار محتوى قبل الاختيار
✅ تحقق صارم من اختيار الوضع قبل الإضافة
✅ رسائل خطأ واضحة
        """
        
        desc_label = tk.Label(self.root, text=desc_text, font=("Arial", 11), 
                             justify=tk.CENTER, bg="#e8f5e8")
        desc_label.pack(pady=20, padx=20, fill=tk.X)
        
        # Test scenarios
        scenarios_text = """
سيناريوهات الاختبار:
1. محاولة الإضافة بدون اختيار وضع → يجب أن تظهر رسالة خطأ
2. اختيار "عنصر جديد" ومحاولة الإضافة بتصنيف فارغ → خطأ
3. اختيار "عنصر موجود" والإضافة بشكل صحيح → نجاح
4. اختيار "عنصر جديد" والإضافة بشكل صحيح → نجاح
        """
        
        scenarios_label = tk.Label(self.root, text=scenarios_text, font=("Arial", 10), 
                                  foreground="blue", justify=tk.LEFT)
        scenarios_label.pack(pady=10, padx=20)
        
        # Test button
        test_btn = tk.Button(self.root, 
                            text="اختبار الحوار المصحح", 
                            command=self.test_dialog,
                            font=("Arial", 14, "bold"),
                            bg="#4CAF50", fg="white",
                            width=25, height=2)
        test_btn.pack(pady=20)
        
        # Instructions
        instructions = tk.Label(self.root, 
                               text="تعليمات:\n" +
                                    "1. اضغط الزر أعلاه\n" +
                                    "2. جرب الضغط على 'إضافة' بدون اختيار وضع\n" +
                                    "3. جرب اختيار وضع وإضافة عنصر\n" +
                                    "4. تأكد من رسائل الخطأ",
                               font=("Arial", 10), foreground="gray",
                               justify=tk.CENTER)
        instructions.pack(pady=10)
        
        # Result display
        self.result_label = tk.Label(self.root, text="", font=("Arial", 12, "bold"))
        self.result_label.pack(pady=10)
        
        # Close button
        close_btn = tk.Button(self.root, text="إغلاق", 
                             command=self.root.quit,
                             font=("Arial", 12))
        close_btn.pack(pady=20)
    
    def test_dialog(self):
        """Test the dialog."""
        print("🧪 اختبار الحوار المصحح...")
        
        try:
            dialog = AddItemDialog(self.root, self.existing_items)
            result = dialog.show()
            
            if result:
                item_name, category, quantity = result
                self.result_label.config(
                    text=f"✅ نجح: {item_name} | {category} | {quantity}",
                    fg="green"
                )
                print(f"✅ النتيجة: {item_name} - {category} - {quantity}")
            else:
                self.result_label.config(text="❌ تم الإلغاء", fg="orange")
                print("❌ تم إلغاء العملية")
                
        except Exception as e:
            self.result_label.config(text=f"❌ خطأ: {e}", fg="red")
            print(f"❌ خطأ: {e}")
    
    def run(self):
        """Run the test."""
        self.root.mainloop()

if __name__ == "__main__":
    print("🔧 اختبار الحوار المصحح")
    print("=" * 40)
    
    test = FixedDialogTest()
    test.run()
    
    print("🎉 انتهى الاختبار")