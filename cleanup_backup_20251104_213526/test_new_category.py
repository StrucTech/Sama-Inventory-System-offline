#!/usr/bin/env python3
"""
Test the new category selection approach with Entry + Button.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from gui.add_item_dialog import AddItemDialog

class NewCategoryTest:
    """Test the new category selection approach."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("اختبار الحل الجديد - Entry + Button")
        self.root.geometry("600x500")
        
        # Sample existing items
        self.existing_items = [
            {"item_name": "مسامير حديد", "category": "أدوات معدنية"},
            {"item_name": "أسمنت أبيض", "category": "مواد البناء"},
            {"item_name": "كابل كهرباء", "category": "أدوات كهربائية"},
            {"item_name": "طلاء أحمر", "category": "دهانات ومواد التشطيب"},
            {"item_name": "براغي معدنية", "category": "أدوات معدنية"},
        ]
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup test UI."""
        # Title
        title_label = tk.Label(self.root, text="اختبار الحل الجديد للتصنيفات", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # Description
        desc_text = """
الحل الجديد يستخدم:
• Entry field للكتابة المباشرة
• زر "اختر من القائمة" لعرض التصنيفات الموجودة
• نافذة منفصلة لاختيار التصنيف
• تحقق صارم من البيانات
        """
        
        desc_label = tk.Label(self.root, text=desc_text, font=("Arial", 11), 
                             justify=tk.CENTER, bg="#f0f0f0")
        desc_label.pack(pady=20, padx=20, fill=tk.X)
        
        # Test info
        categories = list(set(item['category'] for item in self.existing_items))
        info_text = f"""
التصنيفات المتاحة ({len(categories)}):
{', '.join(categories)}

العناصر الموجودة: {len(self.existing_items)}
        """
        
        info_label = tk.Label(self.root, text=info_text, font=("Arial", 10), 
                             foreground="blue")
        info_label.pack(pady=10)
        
        # Test buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)
        
        # Test with existing items
        test_btn1 = tk.Button(btn_frame, 
                             text="اختبار مع عناصر موجودة", 
                             command=self.test_with_items,
                             font=("Arial", 12, "bold"),
                             bg="#4CAF50", fg="white",
                             width=20, height=2)
        test_btn1.pack(side=tk.LEFT, padx=10)
        
        # Test without items
        test_btn2 = tk.Button(btn_frame, 
                             text="اختبار بدون عناصر", 
                             command=self.test_without_items,
                             font=("Arial", 12, "bold"),
                             bg="#FF9800", fg="white",
                             width=20, height=2)
        test_btn2.pack(side=tk.LEFT, padx=10)
        
        # Instructions
        instructions = tk.Label(self.root, 
                               text="تعليمات الاختبار:\n" +
                                    "1. اضغط على أحد أزرار الاختبار\n" +
                                    "2. اختر 'إضافة عنصر جديد'\n" +
                                    "3. جرب كتابة تصنيف في الحقل مباشرة\n" +
                                    "4. جرب الضغط على 'اختر من القائمة'\n" +
                                    "5. تأكد من التحقق من البيانات",
                               font=("Arial", 10), foreground="gray",
                               justify=tk.CENTER)
        instructions.pack(pady=20)
        
        # Result display
        self.result_label = tk.Label(self.root, text="", font=("Arial", 12, "bold"))
        self.result_label.pack(pady=10)
        
        # Close button
        close_btn = tk.Button(self.root, text="إغلاق", 
                             command=self.root.quit,
                             font=("Arial", 12))
        close_btn.pack(pady=20)
    
    def test_with_items(self):
        """Test dialog with existing items."""
        print("🧪 اختبار مع عناصر موجودة...")
        print(f"التصنيفات المتاحة: {list(set(item['category'] for item in self.existing_items))}")
        
        try:
            dialog = AddItemDialog(self.root, self.existing_items)
            result = dialog.show()
            
            if result:
                item_name, category, quantity = result
                self.result_label.config(
                    text=f"✅ تم: {item_name} | {category} | {quantity}",
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
        """Test dialog without existing items."""
        print("🧪 اختبار بدون عناصر موجودة...")
        
        try:
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
    print("🔧 اختبار الحل الجديد للتصنيفات")
    print("=" * 50)
    
    test = NewCategoryTest()
    test.run()
    
    print("🎉 انتهى الاختبار")