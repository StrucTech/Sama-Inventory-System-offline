"""
سكريبت اختبار لسجل الأنشطة - يعرض جميع العمليات المسجلة
"""

from sheets.manager import SheetsManager
from config.settings import load_config

def main():
    print("عرض سجل الأنشطة...")
    
    config = load_config()
    manager = SheetsManager(
        credentials_file=config["credentials_file"],
        spreadsheet_name=config["spreadsheet_name"],
        worksheet_name=config["worksheet_name"]
    )
    
    if manager.connect():
        print(f"✓ متصل بالجدول: '{config['spreadsheet_name']}'")
        
        # عرض سجل الأنشطة
        try:
            if manager.activity_log:
                print(f"\n📋 سجل الأنشطة (Activity_Log):")
                print("=" * 80)
                
                all_activities = manager.activity_log.get_all_values()
                
                if len(all_activities) <= 1:
                    print("لا توجد أنشطة مسجلة بعد")
                else:
                    # طباعة الصفوف
                    for i, row in enumerate(all_activities):
                        if i == 0:  # العناوين
                            print(f"{'التاريخ والوقت':<20} {'العملية':<10} {'العنصر':<15} {'التفاصيل':<30} {'الكمية القديمة':<12} {'الكمية الجديدة':<12}")
                            print("-" * 120)
                        else:
                            timestamp = row[0] if len(row) > 0 else ""
                            operation = row[1] if len(row) > 1 else ""
                            item_name = row[2] if len(row) > 2 else ""
                            details = row[3] if len(row) > 3 else ""
                            old_qty = row[4] if len(row) > 4 else ""
                            new_qty = row[5] if len(row) > 5 else ""
                            
                            print(f"{timestamp:<20} {operation:<10} {item_name:<15} {details:<30} {old_qty:<12} {new_qty:<12}")
                
                # عرض الرابط المباشر لشيت سجل الأنشطة
                spreadsheet_id = manager.spreadsheet.id
                activity_sheet_id = manager.activity_log.id
                activity_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit#gid={activity_sheet_id}"
                
                print(f"\n🔗 رابط مباشر لسجل الأنشطة:")
                print(activity_url)
                print("\nملاحظة: هذا الشيت مخفي في التطبيق ولكن يمكن الوصول إليه مباشرة من جداول جوجل")
                
            else:
                print("لم يتم العثور على شيت سجل الأنشطة")
                
        except Exception as e:
            print(f"خطأ في قراءة سجل الأنشطة: {e}")
            
    else:
        print("فشل في الاتصال بجداول جوجل")

if __name__ == "__main__":
    main()