#!/usr/bin/env python3
"""
Add sample inventory items with categories for testing.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sheets.manager import SheetsManager
from config.settings import load_config

def add_sample_items():
    """Add sample items with categories."""
    print("➕ إضافة عناصر تجريبية مع التصنيفات...")
    
    try:
        # Load config and initialize sheets manager
        config = load_config()
        if not config:
            print("❌ خطأ في تحميل الإعدادات")
            return
            
        sheets_manager = SheetsManager(
            config, 
            config.get('spreadsheet_name', 'Inventory Management')
        )
        
        if not sheets_manager.initialize():
            print("❌ فشل في تهيئة مدير الجداول")
            return
        
        # Sample items with different categories
        sample_items = [
            ("مسامير حديد 3 سم", "أدوات معدنية", 500, "PROJ001"),
            ("أسمنت أبيض كيس 50 كيلو", "مواد البناء", 20, "PROJ001"),
            ("كابل كهرباء 2.5 مم", "أدوات كهربائية", 100, "PROJ002"),
            ("طلاء أحمر لتر واحد", "دهانات ومواد التشطيب", 15, "PROJ002"),
            ("براغي معدنية 5 سم", "أدوات معدنية", 200, "PROJ001"),
            ("رمل بناء متر مكعب", "مواد البناء", 10, "PROJ003"),
            ("مفتاح كهرباء", "أدوات كهربائية", 50, "PROJ002"),
            ("ورنيش شفاف", "دهانات ومواد التشطيب", 8, "PROJ003"),
        ]
        
        print(f"🔄 إضافة {len(sample_items)} عنصر تجريبي...")
        
        success_count = 0
        for item_name, category, quantity, project_id in sample_items:
            try:
                success = sheets_manager.add_item(item_name, category, quantity, project_id)
                if success:
                    print(f"✅ {item_name} | {category}")
                    success_count += 1
                else:
                    print(f"❌ فشل في إضافة: {item_name}")
            except Exception as e:
                print(f"❌ خطأ في {item_name}: {e}")
        
        print(f"\n🎉 تمت إضافة {success_count} عنصر من أصل {len(sample_items)}")
        
        if success_count > 0:
            print("\n📊 التصنيفات المضافة:")
            categories = list(set([item[1] for item in sample_items]))
            for category in categories:
                items_in_category = [item for item in sample_items if item[1] == category]
                print(f"  📦 {category}: {len(items_in_category)} عنصر")
        
    except Exception as e:
        print(f"❌ خطأ عام: {e}")

if __name__ == "__main__":
    print("🧪 إضافة بيانات تجريبية للمخزون")
    print("=" * 50)
    add_sample_items()
    print("\n💡 شغّل التطبيق الآن لرؤية البيانات مع التصنيفات!")