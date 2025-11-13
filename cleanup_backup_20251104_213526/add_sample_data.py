"""
سكريبت لإضافة بيانات تجريبية للنظام
يقوم بإضافة عناصر تجريبية لاختبار النظام الجديد
"""

from sheets.manager import SheetsManager
from config.settings import load_config

def main():
    print("📦 إضافة بيانات تجريبية للمخزون...")
    print("=" * 50)
    
    config = load_config()
    manager = SheetsManager(
        credentials_file=config["credentials_file"],
        spreadsheet_name=config["spreadsheet_name"],
        worksheet_name=config["worksheet_name"]
    )
    
    if manager.connect():
        print(f"✓ متصل بالجدول: '{config['spreadsheet_name']}'")
        
        # بيانات تجريبية
        sample_items = [
            {"name": "لابتوب ديل", "quantity": 15},
            {"name": "ماوس لوجيتك", "quantity": 50},
            {"name": "كيبورد ميكانيكي", "quantity": 25},
            {"name": "شاشة سامسونج 24 انش", "quantity": 8},
            {"name": "طابعة HP LaserJet", "quantity": 3},
            {"name": "هاتف آيفون 15", "quantity": 12},
            {"name": "تابلت iPad", "quantity": 6},
            {"name": "سماعات AirPods", "quantity": 30},
            {"name": "كاميرا كانون", "quantity": 4},
            {"name": "هارد ديسك خارجي 1TB", "quantity": 20}
        ]
        
        print(f"\n📝 إضافة {len(sample_items)} عنصر تجريبي...")
        
        success_count = 0
        for item in sample_items:
            try:
                if manager.add_item(item["name"], item["quantity"]):
                    print(f"✓ تم إضافة: {item['name']} (الكمية: {item['quantity']})")
                    success_count += 1
                else:
                    print(f"✗ فشل في إضافة: {item['name']}")
            except Exception as e:
                print(f"✗ خطأ في إضافة {item['name']}: {e}")
        
        print(f"\n📊 النتائج:")
        print(f"✅ تم إضافة {success_count} عنصر بنجاح")
        print(f"❌ فشل في إضافة {len(sample_items) - success_count} عنصر")
        
        # التحقق من البيانات المضافة
        print(f"\n🔍 التحقق من المخزون:")
        items = manager.get_all_items()
        print(f"📦 إجمالي العناصر في المخزون: {len(items)}")
        
        if items:
            print("\n📋 قائمة العناصر:")
            for item in items:
                print(f"  • {item['item_name']}: {int(item['quantity'])} قطعة")
        
        # عرض رابط الجدول
        spreadsheet_id = manager.spreadsheet.id
        spreadsheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}"
        print(f"\n🔗 رابط الجدول: {spreadsheet_url}")
        
        print(f"\n🎉 تم إنشاء بيانات تجريبية بنجاح!")
        print(f"💡 يمكنك الآن تجربة النظام باستخدام البيانات المضافة")
        
    else:
        print("❌ فشل في الاتصال بجداول جوجل")

if __name__ == "__main__":
    main()