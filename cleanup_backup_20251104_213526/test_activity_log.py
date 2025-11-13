"""
اختبار سجل الأنشطة عن طريق إضافة عنصر تجريبي
"""

from sheets.manager import SheetsManager
from config.settings import load_config

def main():
    print("اختبار سجل الأنشطة...")
    
    config = load_config()
    manager = SheetsManager(
        credentials_file=config["credentials_file"],
        spreadsheet_name=config["spreadsheet_name"],
        worksheet_name=config["worksheet_name"]
    )
    
    if manager.connect():
        print("✓ متصل بجداول جوجل")
        
        # إضافة عنصر تجريبي
        print("\n🧪 إضافة عنصر تجريبي...")
        if manager.add_item("عنصر تجريبي - اختبار السجل", 5, 10.50):
            print("✓ تم إضافة العنصر التجريبي")
        else:
            print("✗ فشل في إضافة العنصر")
            
        # عرض المخزون الحالي
        print("\n📦 المخزون الحالي:")
        items = manager.get_all_items()
        for item in items:
            print(f"  - {item['item_name']}: {item['quantity']} (سعر: {item['unit_price']} ر.س)")
            
        # عرض سجل الأنشطة
        print("\n📋 سجل الأنشطة:")
        if manager.activity_log:
            activities = manager.activity_log.get_all_values()
            for i, row in enumerate(activities):
                if i == 0:  # تخطي العناوين
                    continue
                if len(row) >= 4:
                    print(f"  {row[0]} - {row[1]}: {row[2]} ({row[3]})")
                    
    else:
        print("فشل في الاتصال")

if __name__ == "__main__":
    main()