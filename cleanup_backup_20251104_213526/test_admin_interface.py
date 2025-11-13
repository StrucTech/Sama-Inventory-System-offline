#!/usr/bin/env python3
"""
اختبار واجهة إدارة المشاريع
"""

import tkinter as tk
from gui.admin_projects_window import AdminProjectsWindow
from config.settings import SPREADSHEET_CONFIG

def test_admin_interface():
    """اختبار واجهة الإدارة"""
    print("🧪 اختبار واجهة إدارة المشاريع...")
    
    # إنشاء نافذة جذر
    root = tk.Tk()
    root.withdraw()  # إخفاء النافذة الجذر
    
    try:
        # إنشاء واجهة الإدارة
        admin_window = AdminProjectsWindow(root, SPREADSHEET_CONFIG)
        
        print("✅ تم إنشاء واجهة الإدارة بنجاح")
        
        # عرض النافذة
        admin_window.show()
        
        print("📋 النوافذ متاحة:")
        print("  - نافذة إنشاء مشروع جديد")
        print("  - نافذة ربط المستخدمين بالمشاريع")
        print("  - عرض البيانات في جداول")
        
        # تشغيل النافذة
        root.mainloop()
        
    except Exception as e:
        print(f"❌ خطأ في اختبار واجهة الإدارة: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_admin_interface()