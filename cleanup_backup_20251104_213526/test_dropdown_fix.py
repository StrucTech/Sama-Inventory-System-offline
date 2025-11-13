#!/usr/bin/env python3
"""
Quick test for the dropdown opening fix.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import ttk

class DropdownFixTest:
    """Test the dropdown fix."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("اختبار فتح Dropdown التصنيف")
        self.root.geometry("600x400")
        
        # Test categories
        self.categories = ["أدوات معدنية", "مواد البناء", "أدوات كهربائية", "دهانات"]
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup test UI."""
        # Title
        title_label = tk.Label(self.root, text="اختبار فتح Dropdown التصنيف", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # Info
        info_label = tk.Label(self.root, 
                             text="اختبر طرق فتح القائمة المنسدلة:\n• النقر على الحقل\n• النقر على الزر\n• مفاتيح الأسهم",
                             font=("Arial", 12), justify=tk.CENTER)
        info_label.pack(pady=10)
        
        # Test frame
        test_frame = ttk.LabelFrame(self.root, text="اختبار Combobox", padding="20")
        test_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Method 1: Simple combobox
        ttk.Label(test_frame, text="طريقة 1 - Combobox عادي:", font=("Arial", 11)).pack(anchor=tk.W, pady=5)
        self.combo1 = ttk.Combobox(test_frame, values=self.categories, state="normal", width=40)
        self.combo1.pack(pady=5)
        self.combo1.set("اختر أو اكتب تصنيف...")
        
        # Method 2: With manual button
        ttk.Label(test_frame, text="طريقة 2 - مع زر فتح:", font=("Arial", 11)).pack(anchor=tk.W, pady=(20,5))
        
        combo_frame = tk.Frame(test_frame)
        combo_frame.pack(pady=5)
        
        self.combo2 = ttk.Combobox(combo_frame, values=self.categories, state="normal", width=35)
        self.combo2.pack(side=tk.LEFT, padx=(0, 5))
        self.combo2.set("اختر أو اكتب تصنيف...")
        
        # Manual dropdown button
        dropdown_btn = tk.Button(combo_frame, text="▼", 
                                command=self.open_dropdown,
                                font=("Arial", 10), width=3)
        dropdown_btn.pack(side=tk.LEFT)
        
        # Method 3: With events
        ttk.Label(test_frame, text="طريقة 3 - مع Events:", font=("Arial", 11)).pack(anchor=tk.W, pady=(20,5))
        self.combo3 = ttk.Combobox(test_frame, values=self.categories, state="normal", width=40)
        self.combo3.pack(pady=5)
        self.combo3.set("اختر أو اكتب تصنيف...")
        
        # Bind events
        self.combo3.bind('<Button-1>', self.on_click)
        self.combo3.bind('<FocusIn>', self.on_focus)
        
        # Test buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)
        
        test_btn1 = tk.Button(btn_frame, text="اختبار الطريقة 1", 
                             command=lambda: self.test_combo(self.combo1, "1"),
                             font=("Arial", 10))
        test_btn1.pack(side=tk.LEFT, padx=5)
        
        test_btn2 = tk.Button(btn_frame, text="اختبار الطريقة 2", 
                             command=lambda: self.test_combo(self.combo2, "2"),
                             font=("Arial", 10))
        test_btn2.pack(side=tk.LEFT, padx=5)
        
        test_btn3 = tk.Button(btn_frame, text="اختبار الطريقة 3", 
                             command=lambda: self.test_combo(self.combo3, "3"),
                             font=("Arial", 10))
        test_btn3.pack(side=tk.LEFT, padx=5)
        
        # Result
        self.result_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)
        
        # Close
        close_btn = tk.Button(self.root, text="إغلاق", command=self.root.quit)
        close_btn.pack(pady=10)
    
    def open_dropdown(self):
        """Open dropdown for combo2."""
        try:
            # Clear placeholder
            if "اختر" in self.combo2.get():
                self.combo2.set("")
            
            # Try to open
            self.combo2.focus_set()
            self.combo2.tk.call("ttk::combobox::Post", self.combo2)
            print("✅ تم فتح dropdown بنجاح")
        except Exception as e:
            print(f"❌ فشل في فتح dropdown: {e}")
    
    def on_click(self, event):
        """Handle click on combo3."""
        try:
            if "اختر" in self.combo3.get():
                self.combo3.set("")
            self.combo3.tk.call("ttk::combobox::Post", self.combo3)
            print("✅ تم فتح dropdown عند النقر")
        except Exception as e:
            print(f"❌ فشل في فتح dropdown عند النقر: {e}")
    
    def on_focus(self, event):
        """Handle focus on combo3."""
        if "اختر" in self.combo3.get():
            self.combo3.set("")
    
    def test_combo(self, combo, method):
        """Test combo value."""
        value = combo.get().strip()
        self.result_label.config(text=f"الطريقة {method}: '{value}'")
        print(f"طريقة {method}: {value}")
    
    def run(self):
        """Run the test."""
        self.root.mainloop()

if __name__ == "__main__":
    print("🔧 اختبار إصلاح فتح Dropdown")
    print("=" * 40)
    
    test = DropdownFixTest()
    test.run()
    
    print("🔚 انتهى الاختبار")