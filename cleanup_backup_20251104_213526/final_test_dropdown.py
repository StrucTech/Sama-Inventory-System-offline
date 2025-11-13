#!/usr/bin/env python3
"""
Final test for the fixed category dropdown functionality.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from gui.add_item_dialog import AddItemDialog

class FinalDropdownTest:
    """Final test class for the dropdown feature."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("اختبار نهائي - Dropdown التصنيف")
        self.root.geometry("600x500")
        
        # Simulate existing items data
        self.existing_items = [
            {"item_name": "مسامير حديد", "category": "أدوات معدنية"},
            {"item_name": "أسمنت أبيض", "category": "مواد البناء"},
            {"item_name": "كابل كهرباء", "category": "أدوات كهربائية"},
            {"item_name": "طلاء أحمر", "category": "دهانات ومواد التشطيب"},
        ]
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the test UI."""
        # Title
        title_label = tk.Label(self.root, text="اختبار نهائي - نافذة إضافة العناصر", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # Test info
        info_text = f"""
تم إصلاح مشكلة dropdown التصنيف!

العناصر الموجودة: {len(self.existing_items)}
التصنيفات المتاحة: {len(set(item['category'] for item in self.existing_items))}

الاختبارات المطلوبة:
✅ تجربة وضع "اختيار عنصر موجود"
✅ تجربة وضع "إضافة عنصر جديد"
✅ اختبار dropdown التصنيف في الوضع الجديد
✅ كتابة تصنيف جديد
        """
        
        info_label = tk.Label(self.root, text=info_text, font=("Arial", 11), 
                             justify=tk.CENTER, bg="#f0f0f0")
        info_label.pack(pady=20, padx=20, fill=tk.X)
        
        # Test buttons frame
        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(pady=20)
        
        # Test with existing items
        test_with_items_btn = tk.Button(buttons_frame, 
                                       text="اختبار مع عناصر موجودة", 
                                       command=self.test_with_existing_items,
                                       font=("Arial", 12, "bold"),
                                       bg="#4CAF50", fg="white",
                                       width=20, height=2)
        test_with_items_btn.pack(side=tk.LEFT, padx=10)
        
        # Test without items
        test_empty_btn = tk.Button(buttons_frame, 
                                  text="اختبار بدون عناصر", 
                                  command=self.test_without_items,
                                  font=("Arial", 12, "bold"),
                                  bg="#2196F3", fg="white",
                                  width=20, height=2)
        test_empty_btn.pack(side=tk.LEFT, padx=10)
        
        # Result display
        self.result_label = tk.Label(self.root, text="", font=("Arial", 12, "bold"))
        self.result_label.pack(pady=20)
        
        # Instructions
        instructions = tk.Label(self.root, 
                               text="تعليمات الاختبار:\n" +
                                    "1. اضغط على أحد أزرار الاختبار\n" +
                                    "2. جرب التبديل بين الوضعين\n" +
                                    "3. في وضع 'عنصر جديد'، اختبر dropdown التصنيف\n" +
                                    "4. جرب كتابة تصنيف جديد",
                               font=("Arial", 10), foreground="gray",
                               justify=tk.CENTER)
        instructions.pack(pady=10)
        
        # Close button
        close_btn = tk.Button(self.root, text="إغلاق الاختبار", 
                             command=self.root.quit,
                             font=("Arial", 12))
        close_btn.pack(pady=20)
    
    def test_with_existing_items(self):
        """Test with existing items."""
        try:
            print("🧪 اختبار مع عناصر موجودة...")
            dialog = AddItemDialog(self.root, self.existing_items)
            result = dialog.show()
            
            if result:
                item_name, category, quantity = result
                self.result_label.config(
                    text=f"✅ النتيجة: {item_name} | {category} | {quantity}",
                    fg="green"
                )
                print(f"✅ النتيجة: {item_name} - {category} - {quantity}")
            else:
                self.result_label.config(text="❌ تم الإلغاء", fg="orange")
                print("❌ تم إلغاء العملية")
                
        except Exception as e:
            self.result_label.config(text=f"❌ خطأ: {e}", fg="red")
            print(f"❌ خطأ: {e}")
    
    def test_without_items(self):
        """Test without existing items."""
        try:
            print("🧪 اختبار بدون عناصر موجودة...")
            dialog = AddItemDialog(self.root, [])
            result = dialog.show()
            
            if result:
                item_name, category, quantity = result
                self.result_label.config(
                    text=f"✅ عنصر جديد: {item_name} | {category} | {quantity}",
                    fg="green"
                )
                print(f"✅ عنصر جديد: {item_name} - {category} - {quantity}")
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
    print("🔧 الاختبار النهائي لإصلاح dropdown التصنيف")
    print("=" * 60)
    
    test = FinalDropdownTest()
    test.run()
    
    print("🎉 انتهى الاختبار النهائي")