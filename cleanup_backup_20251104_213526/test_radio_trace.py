#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار بسيط للتأكد من عمل trace مع radio buttons
"""

import tkinter as tk
from tkinter import ttk

def on_mode_change(*args):
    """Test function to handle mode change."""
    print(f"🔄 تغيير الوضع إلى: {mode_var.get()}")
    
    # Clear content frame
    for widget in content_frame.winfo_children():
        widget.destroy()
    
    mode = mode_var.get()
    if mode == "existing":
        label = ttk.Label(content_frame, text="✅ واجهة العناصر الموجودة", 
                         font=("Arial", 14, "bold"), foreground="green")
        label.pack(pady=20)
    elif mode == "new":
        label = ttk.Label(content_frame, text="➕ واجهة العنصر الجديد", 
                         font=("Arial", 14, "bold"), foreground="blue")
        label.pack(pady=20)
    else:
        label = ttk.Label(content_frame, text="⚠️ يرجى الاختيار", 
                         font=("Arial", 14), foreground="gray")
        label.pack(pady=20)

# إنشاء النافذة الرئيسية
root = tk.Tk()
root.title("اختبار Radio Buttons")
root.geometry("400x300")

# إعداد المتغير مع trace
mode_var = tk.StringVar(value="")
mode_var.trace_add("write", on_mode_change)

# إطار أزرار الاختيار
radio_frame = ttk.LabelFrame(root, text="اختر الوضع", padding="10")
radio_frame.pack(fill=tk.X, padx=10, pady=10)

# أزرار الاختيار
existing_radio = ttk.Radiobutton(radio_frame, text="اختيار عنصر موجود", 
                                variable=mode_var, value="existing")
existing_radio.pack(anchor=tk.W, pady=5)

new_radio = ttk.Radiobutton(radio_frame, text="إضافة عنصر جديد", 
                           variable=mode_var, value="new")
new_radio.pack(anchor=tk.W, pady=5)

# إطار المحتوى
content_frame = ttk.Frame(root)
content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# عرض الرسالة الأولية
on_mode_change()

# تشغيل التطبيق
root.mainloop()