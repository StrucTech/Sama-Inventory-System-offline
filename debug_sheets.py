"""
Debug script to check what's in the Google Sheets
"""

from sheets.manager import SheetsManager
from config.settings import load_config

def main():
    print("Debugging Google Sheets content...")
    
    config = load_config()
    manager = SheetsManager(
        credentials_file=config["credentials_file"],
        spreadsheet_name=config["spreadsheet_name"],
        worksheet_name=config["worksheet_name"]
    )
    
    if manager.connect():
        print(f"✓ Connected to spreadsheet: '{config['spreadsheet_name']}'")
        print(f"✓ Using worksheet: '{config['worksheet_name']}'")
        
        # Get all values from the worksheet
        try:
            all_values = manager.worksheet.get_all_values()
            print(f"\nTotal rows in worksheet: {len(all_values)}")
            
            for i, row in enumerate(all_values, 1):
                print(f"Row {i}: {row}")
                
            print(f"\nItems found by get_all_items(): {len(manager.get_all_items())}")
            
            items = manager.get_all_items()
            for item in items:
                print(f"Item: {item}")
                
        except Exception as e:
            print(f"Error reading data: {e}")
            
        # Check worksheet properties
        print(f"\nWorksheet title: {manager.worksheet.title}")
        print(f"Worksheet ID: {manager.worksheet.id}")
        print(f"Spreadsheet URL: https://docs.google.com/spreadsheets/d/{manager.spreadsheet.id}")
        
    else:
        print("Failed to connect to Google Sheets")

if __name__ == "__main__":
    main()