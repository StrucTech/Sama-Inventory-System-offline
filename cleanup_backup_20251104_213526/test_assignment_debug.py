#!/usr/bin/env python3
"""
اختبار واجهة تعيين المستخدمين للمشاريع
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# إضافة المجلد الجذر للمسار
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.admin_projects_window import AdminProjectsWindow
from config.settings import load_config

def test_assignment_interface():
    """اختبار واجهة تعيين المستخدمين"""
    print("🧪 اختبار واجهة تعيين المستخدمين للمشاريع...")
    
    # تحميل الإعدادات
    config = load_config()
    
    # إنشاء نافذة جذر
    root = tk.Tk()
    root.title("اختبار واجهة التعيين")
    root.geometry("400x300")
    
    def open_admin_window():
        try:
            admin_window = AdminProjectsWindow(root, config)
            admin_window.show()
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في فتح واجهة الإدارة: {e}")
            import traceback
            traceback.print_exc()
    
    # زر لفتح واجهة الإدارة
    open_btn = ttk.Button(root, text="فتح واجهة إدارة المشاريع", 
                         command=open_admin_window)
    open_btn.pack(pady=20)
    
    # تعليمات
    instructions = tk.Text(root, height=10, wrap=tk.WORD)
    instructions.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    instructions.insert(tk.END, """تعليمات الاختبار:

1. اضغط على زر "فتح واجهة إدارة المشاريع"
2. انتقل إلى تبويب "تعيين مستخدمين"
3. اختر مستخدم من القائمة المنسدلة
4. اختر مشروع من القائمة المنسدلة
5. اضغط على "تعيين المستخدم للمشروع"

ملاحظة: سيظهر في Console معلومات DEBUG لمساعدة في حل المشكلة.
""")
    
    print("📋 جاهز للاختبار...")
    print("💡 افحص Console للرسائل التشخيصية")
    
    root.mainloop()

if __name__ == "__main__":
    test_assignment_interface()