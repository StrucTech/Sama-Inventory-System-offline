"""
Script to show exactly which spreadsheet the app is using and add a test item
"""

from sheets.manager import SheetsManager
from config.settings import load_config
import datetime

def main():
    print("Finding your exact spreadsheet...")
    
    config = load_config()
    manager = SheetsManager(
        credentials_file=config["credentials_file"],
        spreadsheet_name=config["spreadsheet_name"],
        worksheet_name=config["worksheet_name"]
    )
    
    if manager.connect():
        # Get spreadsheet info
        spreadsheet_id = manager.spreadsheet.id
        spreadsheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}"
        
        print(f"📊 Spreadsheet Name: '{manager.spreadsheet.title}'")
        print(f"📝 Worksheet Name: '{manager.worksheet.title}'")
        print(f"🔗 Direct URL: {spreadsheet_url}")
        print(f"📧 Service Account Email: Check your credentials.json for the 'client_email' field")
        
        print("\n" + "="*60)
        print("IMPORTANT: Make sure you:")
        print("1. Open this exact URL in your browser")
        print("2. Look for the 'Inventory' tab at the bottom")
        print("3. Check that the spreadsheet is shared with your service account email")
        print("="*60)
        
        # Add a timestamp test item to make it obvious
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        test_item_name = f"TEST ITEM - {timestamp}"
        
        print(f"\n🧪 Adding test item: '{test_item_name}'")
        
        if manager.add_item(test_item_name, 99, 1.50):
            print("✅ Test item added successfully!")
            print(f"💡 Look for '{test_item_name}' in your spreadsheet")
        else:
            print("❌ Failed to add test item")
            
        # Show current contents
        print("\n📋 Current spreadsheet contents:")
        all_values = manager.worksheet.get_all_values()
        for i, row in enumerate(all_values, 1):
            print(f"Row {i}: {row}")
            
    else:
        print("❌ Failed to connect to Google Sheets")

if __name__ == "__main__":
    main()