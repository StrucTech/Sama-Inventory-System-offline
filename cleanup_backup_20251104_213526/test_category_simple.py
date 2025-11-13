#!/usr/bin/env python3
"""
Simple test for the category feature without GUI.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sheets.manager import SheetsManager
from config.settings import load_config

def test_categories():
    """Test category functionality directly."""
    print("🧪 اختبار ميزة التصنيفات...")
    
    try:
        # Load configuration
        config = load_config()
        if not config:
            print("❌ خطأ في تحميل الإعدادات")
            return False
            
        # Initialize sheets manager
        sheets_manager = SheetsManager(
            config.get('credentials_path', 'config/credentials.json'),
            config.get('spreadsheet_name', 'Inventory Management'),
            config.get('inventory_worksheet', 'Inventory')
        )
        
        if not sheets_manager.connect():
            print("❌ فشل في الاتصال بـ Google Sheets")
            return False
            
        print("✅ تم الاتصال بـ Google Sheets بنجاح")
        
        # Add one test item with category
        test_item = ("مسامير اختبار", "أدوات معدنية", 100, "TEST001")
        
        print(f"➕ إضافة عنصر تجريبي: {test_item[0]} | {test_item[1]}")
        
        success = sheets_manager.add_item(
            test_item[0],  # item_name
            test_item[1],  # category  
            test_item[2],  # quantity
            test_item[3]   # project_id
        )
        
        if success:
            print("✅ تمت إضافة العنصر بنجاح")
            
            # Get all items to verify structure
            print("📋 استرجاع البيانات للتحقق من البنية...")
            items = sheets_manager.get_all_items()
            
            if items:
                print(f"📊 تم العثور على {len(items)} عنصر")
                print("\nالبنية:")
                for item in items:
                    print(f"  العنصر: {item.get('item_name', 'N/A')}")
                    print(f"  التصنيف: {item.get('category', 'غير محدد')}")
                    print(f"  الكمية: {item.get('quantity', 0)}")
                    print(f"  المشروع: {item.get('project_id', 'N/A')}")
                    print(f"  آخر تحديث: {item.get('last_updated', 'N/A')}")
                    print("  ---")
                
                return True
            else:
                print("❌ لم يتم العثور على عناصر")
                return False
        else:
            print("❌ فشل في إضافة العنصر")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {e}")
        return False

if __name__ == "__main__":
    print("🔧 اختبار سريع لميزة التصنيفات")
    print("=" * 40)
    
    if test_categories():
        print("\n🎉 الاختبار نجح! عمود التصنيف يعمل بشكل صحيح")
        print("💡 يمكنك الآن تشغيل التطبيق: python main_with_auth.py")
    else:
        print("\n❌ فشل الاختبار")