#!/usr/bin/env python3
"""
Test script for the new dropdown feature with existing items.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sheets.manager import SheetsManager
from config.settings import load_config

def test_dropdown_feature():
    """Test the dropdown functionality by adding items and verifying structure."""
    print("🧪 اختبار ميزة dropdown للعناصر الموجودة...")
    
    try:
        # Initialize sheets manager
        config = load_config()
        if not config:
            print("❌ خطأ في تحميل الإعدادات")
            return False
            
        sheets_manager = SheetsManager(
            config.get('credentials_path', 'config/credentials.json'),
            config.get('spreadsheet_name', 'Inventory Management'),
            config.get('inventory_worksheet', 'Inventory')
        )
        
        if not sheets_manager.connect():
            print("❌ فشل في الاتصال بـ Google Sheets")
            return False
            
        print("✅ تم الاتصال بـ Google Sheets بنجاح")
        
        # Add some test items if they don't exist
        test_items = [
            ("مسامير حديد 5 سم", "أدوات معدنية", 150, "PROJ001"),
            ("أسمنت رمادي", "مواد البناء", 30, "PROJ002"),
            ("كابل كهرباء 4 مم", "أدوات كهربائية", 80, "PROJ001"),
            ("طلاء أزرق", "دهانات ومواد التشطيب", 12, "PROJ003"),
            ("براغي معدنية", "أدوات معدنية", 250, "PROJ002"),
        ]
        
        print("\n➕ إضافة عناصر اختبارية...")
        for item_name, category, quantity, project_id in test_items:
            try:
                success = sheets_manager.add_item(item_name, category, quantity, project_id)
                if success:
                    print(f"✅ {item_name} | {category}")
                else:
                    print(f"⚠️ العنصر موجود: {item_name}")
            except Exception as e:
                print(f"❌ خطأ في {item_name}: {e}")
        
        # Get all items to test dropdown data
        print("\n📋 جلب العناصر الموجودة...")
        all_items = sheets_manager.get_all_items()
        
        if all_items:
            print(f"📊 تم العثور على {len(all_items)} عنصر")
            
            # Test dropdown data structure
            unique_items = {}
            unique_categories = set()
            
            for item in all_items:
                item_name = item.get('item_name', '')
                category = item.get('category', '')
                if item_name and item_name not in unique_items:
                    unique_items[item_name] = category
                if category:
                    unique_categories.add(category)
            
            print(f"\n🔽 العناصر الفريدة للـ dropdown: {len(unique_items)}")
            for item_name, category in list(unique_items.items())[:5]:  # Show first 5
                print(f"  • {item_name} → {category}")
            if len(unique_items) > 5:
                print(f"  ... و {len(unique_items) - 5} عنصر آخر")
                
            print(f"\n📦 التصنيفات المتاحة: {len(unique_categories)}")
            for category in sorted(unique_categories):
                print(f"  • {category}")
                
            print("\n✅ بيانات dropdown جاهزة!")
            print("💡 يمكنك الآن تشغيل التطبيق واختبار:")
            print("   1. اختيار عنصر موجود من القائمة")
            print("   2. إضافة عنصر جديد مع تصنيف جديد أو موجود")
            
            return True
        else:
            print("❌ لا توجد عناصر في المخزون")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {e}")
        return False

if __name__ == "__main__":
    print("🔧 اختبار ميزة dropdown للعناصر الموجودة")
    print("=" * 50)
    
    if test_dropdown_feature():
        print(f"\n🎉 الاختبار نجح!")
        print("🚀 شغّل التطبيق الآن: python main_with_auth.py")
        print("💡 جرب الضغط على 'إضافة عنصر' لرؤية الميزات الجديدة")
    else:
        print("\n❌ فشل الاختبار")