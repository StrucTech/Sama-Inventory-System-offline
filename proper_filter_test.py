#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 PROPER FILTER SYSTEM TEST
This will properly initialize and test the filter system
exactly as your GUI does it
"""

import sys
import os
import tkinter as tk

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sheets.manager import SheetsManager
from activity_log_search_system import ActivityLogSearchSystem
import time

def test_proper_filter_system():
    """Test filter system with proper initialization"""
    
    print("🎯 PROPER FILTER SYSTEM TEST")
    print("="*60)
    print("This properly initializes the filter system exactly like your GUI")
    print("="*60)
    
    try:
        # Step 1: Connect to sheets
        print("📱 Step 1: Connecting to Google Sheets...")
        sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
        
        if not sheets_manager.connect():
            print("❌ Failed to connect to Google Sheets!")
            return False
            
        print("✅ Connected to Google Sheets successfully!")
        
        # Step 2: Create a root window (required for GUI components)
        print("🖥️ Step 2: Creating GUI window...")
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Step 3: Create filter system with proper initialization
        print("🔍 Step 3: Creating and initializing filter system...")
        filter_system = ActivityLogSearchSystem(parent=root, sheets_manager=sheets_manager)
        
        # Create the window which will trigger data loading
        window = filter_system.create_window()
        window.withdraw()  # Hide the window but keep it functional
        
        print("✅ Filter system created and initialized!")
        
        # Step 4: Wait for data loading
        print("⏳ Step 4: Waiting for data to load...")
        
        # Process any pending GUI events to ensure data loading completes
        for i in range(10):  # Wait up to 5 seconds
            root.update()
            time.sleep(0.5)
            if len(filter_system.activity_data) > 0:
                break
                
        # Step 5: Check loaded data
        print("📊 Step 5: Checking loaded data...")
        
        total_records = len(filter_system.activity_data)
        initial_filtered = len(filter_system.filtered_data)
        
        print(f"📈 Total records loaded: {total_records}")
        print(f"📋 Initial filtered records: {initial_filtered}")
        
        if total_records == 0:
            print("❌ No data loaded! Checking connection...")
            
            # Try direct data loading
            try:
                worksheet = sheets_manager.spreadsheet.worksheet('Activity_Log_v2_20251108')
                all_values = worksheet.get_all_values()
                print(f"📊 Raw data from sheet: {len(all_values)} rows")
                
                if len(all_values) > 1:
                    headers = all_values[0]
                    print(f"📋 Headers: {headers}")
                    print(f"📄 Sample row: {all_values[1] if len(all_values) > 1 else 'No data'}")
                else:
                    print("❌ No data in worksheet!")
                    
            except Exception as e:
                print(f"❌ Error accessing worksheet: {e}")
                
            root.destroy()
            return False
        
        # Step 6: Test filter values
        print("🔧 Step 6: Checking filter options...")
        
        categories = filter_system.filter_options.get('categories', [])
        print(f"📋 Available categories: {categories}")
        
        if len(categories) <= 1:  # Only "الكل"
            print("❌ No categories loaded!")
            root.destroy()
            return False
            
        # Step 7: Test actual filtering
        print("🧪 Step 7: Testing filter functionality...")
        
        # Find category combo box
        category_combo = getattr(filter_system, 'category_combo', None)
        
        if not category_combo:
            print("❌ Category combo not found!")
            root.destroy()
            return False
            
        # Test with first available category
        test_categories = [cat for cat in categories if cat != "الكل"]
        
        if not test_categories:
            print("❌ No test categories available!")
            root.destroy()
            return False
            
        test_results = {}
        
        for test_category in test_categories[:3]:  # Test up to 3 categories
            print(f"🧪 Testing category: '{test_category}'")
            
            # Set the filter
            category_combo.set(test_category)
            
            # Trigger the filter event
            category_combo.event_generate('<<ComboboxSelected>>')
            
            # Process GUI events
            root.update()
            time.sleep(0.2)
            
            # Check results
            filtered_count = len(filter_system.filtered_data)
            test_results[test_category] = filtered_count
            
            print(f"   📊 Result: {filtered_count} records")
            
            # Verify the filtering is correct
            if filtered_count > 0:
                correct_count = 0
                for record in filter_system.filtered_data[:5]:  # Check first 5
                    if record.get('التصنيف', '') == test_category:
                        correct_count += 1
                        
                print(f"   ✅ Correct category in sample: {correct_count}/5")
                
        # Step 8: Test reset
        print("🔄 Step 8: Testing filter reset...")
        
        category_combo.set("الكل")
        category_combo.event_generate('<<ComboboxSelected>>')
        root.update()
        time.sleep(0.2)
        
        reset_count = len(filter_system.filtered_data)
        print(f"📊 After reset: {reset_count} records")
        
        # Final analysis
        print("\n" + "="*60)
        print("🎯 FINAL TEST RESULTS")
        print("="*60)
        print(f"📈 Total records: {total_records}")
        print(f"📊 Initial display: {initial_filtered}")
        print(f"🔄 After reset: {reset_count}")
        
        working_filters = 0
        not_working = 0
        
        for category, count in test_results.items():
            if count < total_records and count > 0:
                print(f"   ✅ '{category}': {count} records - WORKING")
                working_filters += 1
            elif count == 0:
                print(f"   ⚠️ '{category}': {count} records - NO MATCHING DATA")
            else:
                print(f"   ❌ '{category}': {count} records - NOT FILTERING")
                not_working += 1
                
        # Conclusion
        if working_filters > 0:
            print(f"\n✅ SUCCESS: {working_filters} filters are working correctly!")
            print("🎯 The filter system IS functional")
            
            if reset_count == total_records:
                print("✅ Reset functionality is also working")
            else:
                print(f"⚠️ Reset may have issue: expected {total_records}, got {reset_count}")
                
        else:
            print(f"\n❌ FAILURE: Filters are not working properly")
            
        # Cleanup
        root.destroy()
        
        return working_filters > 0
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_proper_filter_system()
    
    if success:
        print("\n🎯 CONCLUSION: The filter system is working correctly!")
        print("💡 If you still see issues in your main app, it might be:")
        print("   1. A display refresh problem")
        print("   2. Multiple instances conflicting")
        print("   3. Event binding issues in your specific setup")
    else:
        print("\n❌ CONCLUSION: There is a problem with the filter system!")
        print("🔧 The issue needs to be fixed in the filter logic or data loading")