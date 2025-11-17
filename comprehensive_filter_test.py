#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 DIRECT FILTER TESTING - COMPREHENSIVE
This will test exactly what happens when you use filters in your app
by directly calling the same methods your GUI calls
"""

import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sheets.manager import SheetsManager
from activity_log_search_system import ActivityLogSearchSystem
import time

def test_filter_functionality_directly():
    """Test the filter functionality exactly as the GUI would call it"""
    
    print("🎯 DIRECT FILTER FUNCTIONALITY TEST")
    print("="*60)
    print("This tests the EXACT same code your GUI calls when you:")
    print("1. Open Activity Log page")
    print("2. Change a filter")
    print("3. Watch the data change")
    print("="*60)
    
    try:
        # Step 1: Connect to sheets (same as your app)
        print("📱 Step 1: Connecting to Google Sheets...")
        sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
        
        if not sheets_manager.connect():
            print("❌ Failed to connect to Google Sheets!")
            return False
            
        print("✅ Connected to Google Sheets successfully!")
        
        # Step 2: Create ActivityLogSearchSystem (same as clicking button in your app)
        print("🔍 Step 2: Creating Activity Log Search System...")
        
        # This is EXACTLY what happens when you click "بحث في سجل العمليات" 
        filter_system = ActivityLogSearchSystem(sheets_manager=sheets_manager)
        
        print("✅ Activity Log Search System created!")
        
        # Step 3: Wait for initialization (same as GUI loading)
        print("⏳ Step 3: Waiting for data to load...")
        time.sleep(2)  # Give time for data loading
        
        # Step 4: Check what data is loaded
        print("📊 Step 4: Checking loaded data...")
        
        if hasattr(filter_system, 'activity_data'):
            total_records = len(filter_system.activity_data)
            print(f"📈 Total records loaded: {total_records}")
        else:
            print("❌ No activity_data found!")
            return False
            
        if hasattr(filter_system, 'filtered_data'):
            initial_filtered = len(filter_system.filtered_data) 
            print(f"📋 Initial filtered records: {initial_filtered}")
        else:
            print("❌ No filtered_data found!")
            return False
            
        # Step 5: Check available filter values  
        print("🔧 Step 5: Checking available filter values...")
        
        # Check what categories are available (same as combobox population)
        categories = set()
        for record in filter_system.activity_data:
            cat = record.get('التصنيف', '').strip()
            if cat:
                categories.add(cat)
                
        categories = sorted(categories)
        print(f"📋 Available categories: {categories}")
        
        if not categories:
            print("❌ No categories found in data!")
            return False
            
        # Step 6: Test filter application (same as selecting from combobox)
        print("🧪 Step 6: Testing filter application...")
        
        test_category = categories[0]  # Pick first category
        print(f"🔧 Testing with category: '{test_category}'")
        
        # Apply filter - this is EXACTLY what happens when you select from dropdown
        print("⚙️ Applying filter...")
        
        # Set the filter (same as combobox selection)
        if hasattr(filter_system, 'filters'):
            filter_system.filters['category'] = test_category
        
        # Apply the filter (same as combobox event)
        filter_system.apply_filters()
        
        # Check results
        if hasattr(filter_system, 'filtered_data'):
            filtered_count = len(filter_system.filtered_data)
            print(f"📊 Results after filtering: {filtered_count} records")
            
            if filtered_count < total_records:
                print(f"✅ FILTER WORKING! Reduced from {total_records} to {filtered_count}")
                
                # Show sample of filtered data
                if filtered_count > 0:
                    sample = filter_system.filtered_data[0]
                    print(f"📋 Sample filtered record category: '{sample.get('التصنيف', 'N/A')}'")
                    
                    # Verify all filtered records have the correct category
                    correct_category_count = 0
                    for record in filter_system.filtered_data:
                        if record.get('التصنيف', '') == test_category:
                            correct_category_count += 1
                            
                    print(f"✅ Records with correct category: {correct_category_count}/{filtered_count}")
                    
                    if correct_category_count == filtered_count:
                        print("✅ ALL FILTERED RECORDS ARE CORRECT!")
                    else:
                        print("❌ Some filtered records have wrong category!")
                        
            else:
                print(f"❌ FILTER NOT WORKING! Still showing {filtered_count} records")
                
        # Step 7: Test filter reset (same as selecting "الكل")
        print("🔄 Step 7: Testing filter reset...")
        
        if hasattr(filter_system, 'filters'):
            filter_system.filters['category'] = 'الكل'
            
        filter_system.apply_filters()
        
        if hasattr(filter_system, 'filtered_data'):
            reset_count = len(filter_system.filtered_data)
            print(f"📊 Records after reset: {reset_count}")
            
            if reset_count == total_records:
                print("✅ RESET WORKING! All records restored")
            else:
                print(f"❌ RESET NOT WORKING! Expected {total_records}, got {reset_count}")
                
        # Step 8: Test multiple filters
        print("🧪 Step 8: Testing multiple categories...")
        
        test_results = {}
        
        for category in categories[:3]:  # Test first 3 categories
            if hasattr(filter_system, 'filters'):
                filter_system.filters['category'] = category
            filter_system.apply_filters()
            
            if hasattr(filter_system, 'filtered_data'):
                count = len(filter_system.filtered_data)
                test_results[category] = count
                print(f"   📊 '{category}': {count} records")
                
        # Final summary
        print("\n" + "="*60)
        print("🎯 FINAL TEST RESULTS")
        print("="*60)
        print(f"📈 Total records in database: {total_records}")
        print("📊 Filter test results:")
        
        working_filters = 0
        for category, count in test_results.items():
            if count < total_records and count > 0:
                print(f"   ✅ '{category}': {count} records - WORKING")
                working_filters += 1
            elif count == 0:
                print(f"   ⚠️ '{category}': {count} records - NO DATA")  
            else:
                print(f"   ❌ '{category}': {count} records - NOT FILTERING")
                
        if working_filters > 0:
            print(f"\n✅ CONCLUSION: Filters ARE WORKING! ({working_filters} working)")
            print("🔍 If you're not seeing changes in your GUI, the issue is in the display update, not the filtering logic.")
        else:
            print(f"\n❌ CONCLUSION: Filters are NOT WORKING!")
            
        print("="*60)
        
        return working_filters > 0
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_filter_functionality_directly()
    
    if success:
        print("\n🎯 The filter logic is working correctly!")
        print("💡 If you don't see changes in your GUI, the problem is likely:")
        print("   1. Display not refreshing properly")
        print("   2. Combobox events not firing") 
        print("   3. Data not being passed to display correctly")
    else:
        print("\n❌ There is a problem with the filter logic itself!")