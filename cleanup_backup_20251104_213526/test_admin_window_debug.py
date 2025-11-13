#!/usr/bin/env python3
"""
اختبار تشخيص مشكلة فتح نافذة الإدارة
"""

import sys
import os
import traceback

# إضافة المجلد الجذر للمسار
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_admin_window_import():
    """اختبار استيراد نافذة الإدارة"""
    print("🔍 تشخيص مشكلة فتح نافذة الإدارة...")
    print("=" * 50)
    
    try:
        print("1. اختبار استيراد AdminProjectsWindow...")
        from gui.admin_projects_window import AdminProjectsWindow
        print("   ✅ تم استيراد AdminProjectsWindow بنجاح")
        
        print("2. اختبار استيراد الإعدادات...")
        from config.settings import load_config
        config = load_config()
        print("   ✅ تم تحميل الإعدادات بنجاح")
        
        print("3. اختبار إنشاء نافذة جذر...")
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # إخفاء النافذة الجذر
        print("   ✅ تم إنشاء النافذة الجذر بنجاح")
        
        print("4. اختبار إنشاء AdminProjectsWindow...")
        admin_window = AdminProjectsWindow(root, config)
        print("   ✅ تم إنشاء AdminProjectsWindow بنجاح")
        
        print("5. اختبار فتح النافذة...")
        admin_window.show()
        print("   ✅ تم فتح النافذة بنجاح")
        
        print("\n🎉 جميع الاختبارات نجحت!")
        print("المشكلة قد تكون في:")
        print("  - ملف credentials.json")
        print("  - اتصال الإنترنت")
        print("  - إعدادات Google Sheets")
        
        # إغلاق النافذة بعد 3 ثوان
        root.after(3000, root.destroy)
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"\n❌ خطأ في الاختبار: {e}")
        print("\n📋 تفاصيل الخطأ:")
        traceback.print_exc()
        
        print("\n💡 حلول محتملة:")
        print("  1. تأكد من وجود ملف credentials.json")
        print("  2. تحقق من اتصال الإنترنت")
        print("  3. تأكد من صحة إعدادات Google Sheets")
        print("  4. أعد تشغيل النظام")
        
        return False

if __name__ == "__main__":
    test_admin_window_import()