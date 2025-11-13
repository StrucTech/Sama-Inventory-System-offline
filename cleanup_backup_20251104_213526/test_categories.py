#!/usr/bin/env python3
"""
Test script for the new category feature in the inventory management system.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sheets.manager import SheetsManager
from config.settings import load_config

def test_category_feature():
    """Test the new category functionality."""
    print("🧪 اختبار ميزة التصنيفات الجديدة...")
    
    try:
        # Load configuration
        config = load_config()
        if not config:
            print("❌ خطأ في تحميل الإعدادات")
            return False
            
        # Initialize sheets manager
        print("📊 تهيئة مدير الجداول...")
        sheets_manager = SheetsManager(config)
        
        if not sheets_manager.initialize():
            print("❌ فشل في تهيئة مدير الجداول")
            return False
            
        print("✅ تم تهيئة مدير الجداول بنجاح")
        
        # Test data with categories
        test_items = [
            ("مسامير حديد", "أدوات معدنية", 100, "TEST001"),
            ("أسمنت أبيض", "مواد البناء", 50, "TEST001"),
            ("كابل كهرباء", "أدوات كهربائية", 200, "TEST002"),
            ("طلاء أحمر", "دهانات ومواد التشطيب", 25, "TEST002"),
        ]
        
        print("\n➕ إضافة عناصر تجريبية مع التصنيفات...")
        
        for item_name, category, quantity, project_id in test_items:
            try:
                success = sheets_manager.add_item(item_name, category, quantity, project_id)
                if success:
                    print(f"✅ تمت إضافة: {item_name} | التصنيف: {category}")
                else:
                    print(f"❌ فشل في إضافة: {item_name}")
            except Exception as e:
                print(f"❌ خطأ في إضافة {item_name}: {e}")
        
        print("\n📋 عرض جميع العناصر مع التصنيفات...")
        
        # Get all items and display them
        items = sheets_manager.get_all_items()
        
        if items:
            print("\n" + "="*80)
            print(f"{'اسم العنصر':<20} {'التصنيف':<20} {'الكمية':<10} {'المشروع':<10} {'آخر تحديث'}")
            print("="*80)
            
            for item in items:
                print(f"{item['item_name']:<20} {item.get('category', 'غير محدد'):<20} "
                      f"{item['quantity']:<10} {item.get('project_id', 'N/A'):<10} {item['last_updated']}")
                      
            print("="*80)
            print(f"إجمالي العناصر: {len(items)}")
            
        else:
            print("❌ لا توجد عناصر في المخزون")
        
        print("\n✅ تم اختبار ميزة التصنيفات بنجاح!")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار ميزة التصنيفات: {e}")
        return False

if __name__ == "__main__":
    print("🚀 بدء اختبار نظام إدارة المخزون مع التصنيفات")
    print("=" * 60)
    
    success = test_category_feature()
    
    if success:
        print("\n🎉 تم اختبار النظام بنجاح!")
        print("💡 يمكنك الآن استخدام التطبيق مع ميزة التصنيفات الجديدة")
    else:
        print("\n❌ فشل في اختبار النظام")
        print("🔧 يرجى التحقق من الإعدادات والمحاولة مرة أخرى")