"""
نسخة عربية من نظام إدارة المخزون
تطبيق سطح مكتب لإدارة المخزون باستخدام جداول جوجل
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# إضافة المجلد الحالي إلى مسار Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import MainWindow
from config.settings import load_config, save_config
from localization import get_text

def main():
    """نقطة البداية الرئيسية للتطبيق."""
    try:
        # تحميل الإعدادات
        config = load_config()
        
        # إنشاء وتشغيل نافذة التطبيق الرئيسية
        root = tk.Tk()
        app = MainWindow(root, config)
        
        # ضبط خصائص النافذة
        root.title(get_text("app_title"))
        root.geometry("800x600")
        root.minsize(600, 400)
        
        # توسيط النافذة
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f"{width}x{height}+{x}+{y}")
        
        # بدء التطبيق
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror(get_text("error"), f"فشل في بدء التطبيق: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()