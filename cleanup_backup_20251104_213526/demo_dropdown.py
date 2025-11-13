#!/usr/bin/env python3
"""
Demo script to showcase the dropdown feature.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from gui.add_item_dialog import AddItemDialog
from sheets.manager import SheetsManager
from config.settings import load_config

class DropdownDemo:
    """Demo class for testing the dropdown feature."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("عرض توضيحي - ميزة Dropdown للعناصر")
        self.root.geometry("400x300")
        self.existing_items = []
        self.load_existing_items()
        self.setup_ui()
    
    def load_existing_items(self):
        """Load existing items from Google Sheets."""
        try:
            config = load_config()
            if config:
                sheets_manager = SheetsManager(
                    config.get('credentials_path', 'config/credentials.json'),
                    config.get('spreadsheet_name', 'Inventory Management'),
                    config.get('inventory_worksheet', 'Inventory')
                )
                
                if sheets_manager.connect():
                    self.existing_items = sheets_manager.get_all_items()
                    print(f"✅ تم تحميل {len(self.existing_items)} عنصر من Google Sheets")
                else:
                    print("❌ فشل في الاتصال بـ Google Sheets")
            else:
                print("❌ فشل في تحميل الإعدادات")
        except Exception as e:
            print(f"❌ خطأ في تحميل البيانات: {e}")
    
    def setup_ui(self):
        """Setup the demo UI."""
        # Title
        title_label = tk.Label(self.root, text="عرض توضيحي - ميزة Dropdown للعناصر", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # Info
        info_text = f"""
تم تحميل {len(self.existing_items)} عنصر من المخزون

اضغط على الزر أدناه لفتح نافذة إضافة العناصر الجديدة
التي تتضمن:

• اختيار عنصر موجود من القائمة المنسدلة
• إضافة عنصر جديد مع تصنيفات متاحة
        """
        
        info_label = tk.Label(self.root, text=info_text, font=("Arial", 11), 
                             justify=tk.CENTER)
        info_label.pack(pady=20)
        
        # Test button
        test_btn = tk.Button(self.root, text="اختبار نافذة إضافة العناصر", 
                            command=self.test_dialog,
                            font=("Arial", 14, "bold"),
                            bg="#4CAF50", fg="white",
                            width=25, height=2)
        test_btn.pack(pady=20)
        
        # Result label
        self.result_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)
        
        # Close button
        close_btn = tk.Button(self.root, text="إغلاق", 
                             command=self.root.quit,
                             font=("Arial", 12))
        close_btn.pack(pady=10)
    
    def test_dialog(self):
        """Test the add item dialog."""
        try:
            dialog = AddItemDialog(self.root, self.existing_items)
            result = dialog.show()
            
            if result:
                item_name, category, quantity = result
                self.result_label.config(
                    text=f"✅ تم اختيار: {item_name} | {category} | {quantity}",
                    fg="green"
                )
                print(f"النتيجة: {item_name} - {category} - {quantity}")
            else:
                self.result_label.config(text="❌ تم الإلغاء", fg="red")
                
        except Exception as e:
            self.result_label.config(text=f"❌ خطأ: {e}", fg="red")
            print(f"خطأ: {e}")
    
    def run(self):
        """Run the demo."""
        self.root.mainloop()

if __name__ == "__main__":
    print("🎮 عرض توضيحي لميزة Dropdown للعناصر")
    print("=" * 50)
    
    demo = DropdownDemo()
    demo.run()
    
    print("🔚 انتهى العرض التوضيحي")