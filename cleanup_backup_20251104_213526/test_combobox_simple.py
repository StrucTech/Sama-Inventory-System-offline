#!/usr/bin/env python3
"""
اختبار مباشر لمشكلة تعيين المستخدمين
"""

import tkinter as tk
from tkinter import ttk, messagebox

def test_combobox_selection():
    """اختبار بسيط للـ Combobox"""
    root = tk.Tk()
    root.title("اختبار Combobox")
    root.geometry("400x300")
    
    # متغيرات
    user_var = tk.StringVar()
    project_var = tk.StringVar()
    
    # بيانات تجريبية
    users = ["أحمد محمد (USR_001)", "فاطمة علي (USR_002)", "محمد سالم (USR_003)"]
    projects = ["مشروع التطوير (PRJ_001)", "مشروع التسويق (PRJ_002)", "مشروع البحث (PRJ_003)"]
    
    # واجهة
    ttk.Label(root, text="اختر المستخدم:").pack(pady=10)
    user_combo = ttk.Combobox(root, textvariable=user_var, values=users, state="readonly")
    user_combo.pack(pady=5)
    user_combo.current(0)  # اختيار افتراضي
    
    ttk.Label(root, text="اختر المشروع:").pack(pady=10)
    project_combo = ttk.Combobox(root, textvariable=project_var, values=projects, state="readonly")
    project_combo.pack(pady=5)
    project_combo.current(0)  # اختيار افتراضي
    
    def test_assignment():
        user_selection = user_var.get()
        project_selection = project_var.get()
        
        print(f"User: '{user_selection}'")
        print(f"Project: '{project_selection}'")
        
        if not user_selection or not project_selection:
            messagebox.showerror("خطأ", "يرجى اختيار المستخدم والمشروع")
            return
        
        # استخراج المعرفات
        try:
            user_id = user_selection.split('(')[-1].split(')')[0].strip()
            project_id = project_selection.split('(')[-1].split(')')[0].strip()
            
            messagebox.showinfo("نجح", f"تم اختيار:\nالمستخدم: {user_id}\nالمشروع: {project_id}")
            
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في المعالجة: {e}")
    
    ttk.Button(root, text="اختبار التعيين", command=test_assignment).pack(pady=20)
    
    # تعليمات
    instructions = tk.Text(root, height=6, wrap=tk.WORD)
    instructions.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    instructions.insert(tk.END, """تعليمات:
1. اختر مستخدم من القائمة الأولى
2. اختر مشروع من القائمة الثانية  
3. اضغط على "اختبار التعيين"

يجب أن ترى رسالة نجح مع المعرفات المستخرجة.
""")
    
    root.mainloop()

if __name__ == "__main__":
    test_combobox_selection()