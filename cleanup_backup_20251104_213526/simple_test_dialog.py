#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار مبسط للـ add item dialog مع تشخيص مفصل
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class SimpleAddItemDialog:
    def __init__(self, parent=None):
        self.dialog = tk.Toplevel(parent) if parent else tk.Tk()
        self.dialog.title("اختبار إضافة عنصر")
        self.dialog.geometry("500x400")
        self.dialog.resizable(True, True)
        
        self.result = None
        self.mode_var = tk.StringVar(value="")
        
        # ربط تغيير المتغير
        self.mode_var.trace_add("write", self.on_mode_change_trace)
        
        self.setup_ui()
        
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        print("🔧 بدء إعداد الواجهة")
        
        # الإطار الرئيسي
        self.main_frame = ttk.Frame(self.dialog, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # العنوان
        title = ttk.Label(self.main_frame, text="اختبار إضافة عنصر", 
                         font=("Arial", 16, "bold"))
        title.pack(pady=(0, 20))
        
        # إطار أزرار الاختيار
        mode_frame = ttk.LabelFrame(self.main_frame, text="اختر الطريقة", padding="15")
        mode_frame.pack(fill=tk.X, pady=(0, 20))
        
        # أزرار الاختيار
        existing_radio = ttk.Radiobutton(mode_frame, text="عنصر موجود", 
                                        variable=self.mode_var, value="existing")
        existing_radio.pack(anchor=tk.W, pady=5)
        
        new_radio = ttk.Radiobutton(mode_frame, text="عنصر جديد", 
                                   variable=self.mode_var, value="new")
        new_radio.pack(anchor=tk.W, pady=5)
        
        # إطار المحتوى
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # إطار الأزرار
        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame.pack(fill=tk.X)
        
        # زر الإلغاء
        cancel_btn = ttk.Button(buttons_frame, text="إلغاء", command=self.cancel)
        cancel_btn.pack(side=tk.LEFT)
        
        # زر الإضافة (مخفي في البداية)
        self.add_btn = ttk.Button(buttons_frame, text="إضافة", command=self.add_item)
        # لا نضعه في البداية
        
        # عرض الرسالة الأولية
        self.show_initial_message()
        
        print("✅ انتهى إعداد الواجهة")
    
    def on_mode_change_trace(self, *args):
        """معالج تغيير الوضع مع trace"""
        mode = self.mode_var.get()
        print(f"🎯 تم استدعاء trace، الوضع الجديد: '{mode}'")
        
        if mode:
            print(f"📋 بدء تغيير الواجهة للوضع: {mode}")
            self.update_content_ui(mode)
        else:
            print("⚠️ لا يوجد وضع محدد")
    
    def update_content_ui(self, mode):
        """تحديث واجهة المحتوى"""
        print(f"🔄 تحديث المحتوى للوضع: {mode}")
        
        # مسح المحتوى الحالي
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            print("🗑️ تم حذف widget")
        
        if mode == "existing":
            print("📝 إنشاء واجهة العناصر الموجودة")
            self.create_existing_ui()
        elif mode == "new":
            print("➕ إنشاء واجهة العنصر الجديد")
            self.create_new_ui()
        
        # إظهار زر الإضافة
        print("👆 إظهار زر الإضافة")
        self.add_btn.pack(side=tk.RIGHT)
    
    def create_existing_ui(self):
        """إنشاء واجهة العناصر الموجودة"""
        frame = ttk.LabelFrame(self.content_frame, text="اختيار عنصر موجود", padding="15")
        frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(frame, text="اسم العنصر:").grid(row=0, column=0, sticky=tk.W, pady=5)
        combobox = ttk.Combobox(frame, values=["عنصر 1", "عنصر 2", "عنصر 3"])
        combobox.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        ttk.Label(frame, text="الكمية:").grid(row=1, column=0, sticky=tk.W, pady=5)
        quantity_entry = ttk.Entry(frame)
        quantity_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        frame.columnconfigure(1, weight=1)
        print("✅ تم إنشاء واجهة العناصر الموجودة")
    
    def create_new_ui(self):
        """إنشاء واجهة العنصر الجديد"""
        frame = ttk.LabelFrame(self.content_frame, text="إضافة عنصر جديد", padding="15")
        frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(frame, text="اسم العنصر:").grid(row=0, column=0, sticky=tk.W, pady=5)
        name_entry = ttk.Entry(frame)
        name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        ttk.Label(frame, text="التصنيف:").grid(row=1, column=0, sticky=tk.W, pady=5)
        category_entry = ttk.Entry(frame)
        category_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        ttk.Label(frame, text="الكمية:").grid(row=2, column=0, sticky=tk.W, pady=5)
        quantity_entry = ttk.Entry(frame)
        quantity_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        frame.columnconfigure(1, weight=1)
        print("✅ تم إنشاء واجهة العنصر الجديد")
    
    def show_initial_message(self):
        """عرض الرسالة الأولية"""
        label = ttk.Label(self.content_frame, 
                         text="يرجى اختيار طريقة الإضافة من الأعلى", 
                         font=("Arial", 12), 
                         foreground="gray")
        label.pack(expand=True)
        print("📝 تم عرض الرسالة الأولية")
    
    def add_item(self):
        """إضافة العنصر"""
        mode = self.mode_var.get()
        print(f"✅ تم النقر على إضافة، الوضع: {mode}")
        messagebox.showinfo("نجح", f"تم اختيار الوضع: {mode}")
    
    def cancel(self):
        """إلغاء"""
        print("❌ تم النقر على إلغاء")
        self.dialog.destroy()

if __name__ == "__main__":
    print("🚀 بدء تشغيل الاختبار")
    
    # إنشاء النافذة
    dialog = SimpleAddItemDialog()
    
    # تشغيل التطبيق
    dialog.dialog.mainloop()
    
    print("🏁 انتهى الاختبار")