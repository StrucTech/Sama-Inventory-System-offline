#!/usr/bin/env python3
"""
Quick test for the category combobox functionality.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import ttk

class ComboboxTest:
    """Test class for category combobox."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("اختبار Combobox التصنيف")
        self.root.geometry("500x400")
        self.setup_ui()
    
    def setup_ui(self):
        """Setup test UI."""
        # Title
        title_label = tk.Label(self.root, text="اختبار Combobox التصنيف", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # Test categories
        test_categories = [
            "أدوات معدنية",
            "مواد البناء", 
            "أدوات كهربائية",
            "دهانات ومواد التشطيب"
        ]
        
        # Instructions
        instructions = tk.Label(self.root, 
                               text="جرب الآتي:\n• اضغط على السهم لفتح القائمة\n• اختر تصنيف موجود\n• أو اكتب تصنيف جديد",
                               font=("Arial", 12), justify=tk.CENTER)
        instructions.pack(pady=20)
        
        # Frame for combobox
        combo_frame = ttk.LabelFrame(self.root, text="التصنيف", padding="20")
        combo_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Category combobox - exactly like in the dialog
        self.category_combobox = ttk.Combobox(combo_frame, width=40, font=("Arial", 12), state="normal")
        self.category_combobox['values'] = test_categories
        self.category_combobox.pack(pady=10)
        
        # Enable typing and dropdown functionality
        self.category_combobox.bind('<Button-1>', self.on_category_click)
        self.category_combobox.bind('<KeyPress>', self.on_category_type)
        self.category_combobox.bind('<<ComboboxSelected>>', self.on_selection)
        
        # Help text
        help_text = tk.Label(combo_frame, text="اختر من القائمة أو اكتب تصنيف جديد", 
                            font=("Arial", 10), foreground="gray")
        help_text.pack()
        
        # Result display
        self.result_label = tk.Label(self.root, text="النتيجة: ", 
                                    font=("Arial", 12, "bold"))
        self.result_label.pack(pady=20)
        
        # Test button
        test_btn = tk.Button(self.root, text="اختبار القيمة المختارة", 
                            command=self.test_value,
                            font=("Arial", 12), bg="#4CAF50", fg="white")
        test_btn.pack(pady=10)
        
        # Close button
        close_btn = tk.Button(self.root, text="إغلاق", 
                             command=self.root.quit,
                             font=("Arial", 12))
        close_btn.pack(pady=10)
        
        # Focus on combobox
        self.category_combobox.focus()
    
    def on_category_click(self, event=None):
        """Handle category combobox click to show dropdown."""
        print("🖱️ تم النقر على الـ combobox")
        self.category_combobox.event_generate('<Down>')
        return None
    
    def on_category_type(self, event=None):
        """Handle typing in category combobox."""
        print(f"⌨️ تم الضغط على: {event.char if event else 'N/A'}")
        return None
    
    def on_selection(self, event=None):
        """Handle selection from dropdown."""
        selected = self.category_combobox.get()
        print(f"✅ تم اختيار: {selected}")
        self.result_label.config(text=f"تم اختيار: {selected}")
    
    def test_value(self):
        """Test the current value."""
        value = self.category_combobox.get().strip()
        if value:
            self.result_label.config(text=f"القيمة الحالية: '{value}'", fg="green")
            print(f"📋 القيمة المختبرة: '{value}'")
        else:
            self.result_label.config(text="لا توجد قيمة", fg="red")
            print("❌ لا توجد قيمة")
    
    def run(self):
        """Run the test."""
        self.root.mainloop()

if __name__ == "__main__":
    print("🧪 اختبار Combobox التصنيف")
    print("=" * 40)
    
    test = ComboboxTest()
    test.run()
    
    print("🔚 انتهى الاختبار")