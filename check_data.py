from sheets.manager import SheetsManager

def check_data():
    sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
    if sheets_manager.connect():
        worksheet = sheets_manager.worksheet
        all_values = worksheet.get_all_values()
        
        print('📋 العناوين:')
        headers = all_values[0] if all_values else []
        for i, header in enumerate(headers, 1):
            print(f'  {i}. {header}')
        
        print(f'\n📊 عدد الأعمدة: {len(headers)}')
        print(f'📊 عدد الصفوف: {len(all_values)}')
        
        if len(all_values) > 1:
            print('\n🔍 عينة من البيانات الفعلية:')
            for i, row in enumerate(all_values[1:4], 1):
                print(f'صف {i}:')
                for j, cell in enumerate(row):
                    if j < len(headers):
                        print(f'  {headers[j]}: "{cell}"')
                print()
            
            # فحص مشكلة الأرقام
            print('\n🔍 فحص البيانات الرقمية:')
            for i, row in enumerate(all_values[1:6], 1):
                if len(row) >= 6:
                    print(f'العنصر {i}: {row[0]}')
                    print(f'  ابتدائية: "{row[2]}" (نوع: {type(row[2])})')
                    print(f'  داخلة: "{row[3]}" (نوع: {type(row[3])})')
                    print(f'  خارجة: "{row[4]}" (نوع: {type(row[4])})')
                    print(f'  متبقية: "{row[5]}" (نوع: {type(row[5])})')
                    print()

if __name__ == "__main__":
    check_data()