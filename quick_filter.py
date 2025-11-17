#!/usr/bin/env python3
"""
🚀 حل فوري ومباشر لتشغيل الفلاتر - النسخة البسيطة
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import messagebox
from gui.basic_filter_window import open_basic_filter_window
from sheets.manager import SheetsManager

def main():
    """الدالة الرئيسية المبسطة"""
    print("🔥 بدء النسخة المبسطة للفلاتر...")
    
    # إنشاء النافذة الرئيسية (مخفية)
    root = tk.Tk()
    root.withdraw()  # إخفاء النافذة الرئيسية
    
    try:
        # اتصال مباشر بـ Google Sheets
        print("🔗 جاري الاتصال بـ Google Sheets...")
        sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
        
        if not sheets_manager.connect():
            messagebox.showerror("خطأ", "فشل الاتصال بـ Google Sheets!")
            return
        
        # فحص البيانات
        data = sheets_manager.get_all_items_raw()
        print(f"✅ تم تحميل {len(data)} عنصر من قاعدة البيانات")
        
        # مستخدم افتراضي
        current_user = {'username': 'admin', 'user_type': 'admin'}
        print(f"👤 المستخدم: {current_user['username']}")
        
        # فتح نافذة الفلاتر مباشرة
        print("🎛️ فتح نافذة الفلاتر...")
        filter_window = open_basic_filter_window(root, sheets_manager, current_user)
        
        if filter_window:
            print("🎉 نجح! نافذة الفلاتر مفتوحة ومجهزة للاستخدام!")
            
            messagebox.showinfo("نجح! 🔥", 
                f"تم فتح نافذة الفلاتر بنجاح!\\n\\n"
                f"✨ الميزات المتاحة:\\n"
                f"• فلتر التصنيف (Category)\\n"
                f"• فلتر المشروع (Project)\\n"
                f"• أزرار المسح والتحديث\\n"
                f"• تحديث فوري للبيانات\\n\\n"
                f"🎯 جرب الفلاتر الآن وراقب النتائج!")
            
            # بدء حلقة الأحداث
            root.mainloop()
            
        else:
            messagebox.showerror("خطأ", "فشل في إنشاء نافذة الفلاتر!")
            
    except Exception as e:
        print(f"❌ خطأ: {e}")
        import traceback
        traceback.print_exc()
        messagebox.showerror("خطأ", f"حدث خطأ غير متوقع:\\n{str(e)}")
    
    finally:
        try:
            root.destroy()
        except:
            pass

if __name__ == "__main__":
    main()