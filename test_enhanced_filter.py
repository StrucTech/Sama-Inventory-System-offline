"""
اختبار النافذة المحسّنة للفلاتر مع أعمدة الكمية الجديدة
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.enhanced_filter_window import AdvancedFilterWindow
from sheets.manager import SheetsManager
import tkinter as tk

def test_enhanced_filter():
    """اختبار النافذة المحسّنة"""
    
    print("🚀 بدء اختبار النافذة المحسّنة...")
    
    # إنشاء النافذة الجذر (مخفية)
    root = tk.Tk()
    root.withdraw()
    
    try:
        # إنشاء مدير Google Sheets
        sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
        
        if not sheets_manager.connect():
            print("❌ فشل في الاتصال بـ Google Sheets")
            return False
        
        print("✅ تم الاتصال بـ Google Sheets بنجاح")
        
        # إنشاء النافذة المحسّنة
        filter_window = AdvancedFilterWindow(sheets_manager)
        
        print("📊 النافذة جاهزة للاختبار")
        print("🔍 يمكنك الآن اختبار:")
        print("  - عرض جميع أعمدة الكمية (ابتدائية، داخلة، خارجة، متبقية)")
        print("  - الإحصائيات السريعة في أعلى النافذة")
        print("  - الفلاتر المختلفة للبيانات")
        print("  - الألوان المختلفة للصفوف حسب الكمية المتبقية")
        
        # تشغيل النافذة
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار النافذة: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        try:
            root.destroy()
        except:
            pass

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 اختبار النافذة المحسّنة للفلاتر")
    print("=" * 60)
    
    success = test_enhanced_filter()
    
    if success:
        print("\n✅ انتهى الاختبار بنجاح")
    else:
        print("\n❌ فشل الاختبار")