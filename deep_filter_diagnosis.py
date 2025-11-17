"""
🔍 Filter System Deep Diagnostic Tool
====================================

This will help us identify exactly why filters aren't working in the main app
"""

import sys
import os
import tkinter as tk
from tkinter import ttk

# Add project path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sheets.manager import SheetsManager

def diagnose_filter_issue():
    """Deep diagnosis of filter system"""
    
    print("🔍 DEEP FILTER DIAGNOSIS")
    print("=" * 40)
    
    try:
        # 1. Test Google Sheets connection
        print("\n1. 📡 Testing Google Sheets Connection:")
        sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
        
        if not sheets_manager.connect():
            print("❌ Google Sheets connection failed")
            return False
        
        print("✅ Google Sheets connected successfully")
        
        # 2. Load activity log data
        print("\n2. 📊 Loading Activity Log Data:")
        try:
            activity_worksheet = sheets_manager.spreadsheet.worksheet('Activity_Log_v2_20251108')
            activity_values = activity_worksheet.get_all_values()
            
            if not activity_values:
                print("❌ No data in Activity_Log_v2_20251108")
                return False
            
            print(f"✅ Loaded {len(activity_values)} rows")
            
            headers = activity_values[0]
            print(f"📋 Headers: {headers}")
            
            # Convert to records
            records = []
            for row in activity_values[1:]:
                if row and row[0]:  # Has date
                    record = {}
                    for i, header in enumerate(headers):
                        record[header] = row[i] if i < len(row) else ""
                    records.append(record)
            
            print(f"✅ Converted {len(records)} records")
            
        except Exception as e:
            print(f"❌ Error loading activity log: {e}")
            return False
        
        # 3. Test filter creation
        print("\n3. 🎯 Testing Filter Creation:")
        
        # Collect unique values for filters
        categories = set(['الكل'])
        items = set(['الكل'])
        projects = set(['الكل'])
        users = set(['الكل'])
        dates = set(['الكل'])
        
        for record in records:
            if record.get('التصنيف'):
                categories.add(record['التصنيف'])
            if record.get('اسم العنصر'):
                items.add(record['اسم العنصر'])
            if record.get('رقم المشروع'):
                projects.add(record['رقم المشروع'])
            if record.get('اسم المستخدم'):
                users.add(record['اسم المستخدم'])
            if record.get('التاريخ'):
                dates.add(record['التاريخ'])
        
        print(f"📊 Filter Options Available:")
        print(f"   🏷️ Categories: {len(categories)-1} ({sorted(list(categories))[1:3]}...)")
        print(f"   📦 Items: {len(items)-1}")
        print(f"   🎯 Projects: {len(projects)-1} ({sorted(list(projects))[1:]})")
        print(f"   👤 Users: {len(users)-1} ({sorted(list(users))[1:]})")
        print(f"   📅 Dates: {len(dates)-1}")
        
        # 4. Test actual filtering
        print("\n4. 🔬 Testing Manual Filter Logic:")
        
        # Test category filter
        if len(categories) > 1:
            test_category = sorted(list(categories))[1]  # First non-"الكل" category
            filtered_records = []
            
            print(f"🧪 Testing filter: Category = '{test_category}'")
            
            for record in records:
                if record.get('التصنيف', '') == test_category:
                    filtered_records.append(record)
            
            print(f"   📊 Results: {len(filtered_records)} out of {len(records)} records")
            
            if filtered_records:
                print(f"   ✅ Sample result: {filtered_records[0]['التاريخ']} - {filtered_records[0]['اسم العنصر']}")
            else:
                print(f"   ❌ No results for category '{test_category}'")
                
                # Debug: Check what categories actually exist
                print(f"   🔍 Debug: Checking actual categories in data...")
                actual_categories = {}
                for record in records:
                    cat = record.get('التصنيف', '')
                    if cat:
                        actual_categories[cat] = actual_categories.get(cat, 0) + 1
                
                print(f"   📋 Actual categories found:")
                for cat, count in actual_categories.items():
                    print(f"      '{cat}': {count} records")
        
        # 5. Test ActivityLogSearchSystem directly
        print("\n5. 🔍 Testing ActivityLogSearchSystem:")
        
        try:
            from activity_log_search_system import ActivityLogSearchSystem
            
            # Create a test root window
            root = tk.Tk()
            root.withdraw()  # Hide it
            
            # Create the system
            search_system = ActivityLogSearchSystem(parent=root)
            
            print("✅ ActivityLogSearchSystem created")
            
            # Create the window (this loads data)
            window = search_system.create_window()
            
            if window:
                print("✅ Window created")
                
                # Check if data loaded
                if hasattr(search_system, 'activity_data') and search_system.activity_data:
                    print(f"✅ Data loaded: {len(search_system.activity_data)} records")
                    
                    # Check filter variables
                    if hasattr(search_system, 'filter_vars'):
                        print(f"📋 Filter variables:")
                        for key, var in search_system.filter_vars.items():
                            print(f"   {key}: '{var.get()}'")
                        
                        # Test changing a filter variable
                        if 'category' in search_system.filter_vars and len(categories) > 1:
                            test_category = sorted(list(categories))[1]
                            
                            print(f"\n🔧 Testing filter change to '{test_category}':")
                            
                            # Set the filter
                            search_system.filter_vars['category'].set(test_category)
                            
                            # Apply filters
                            search_system.apply_filters()
                            
                            # Check results
                            filtered_count = len(search_system.filtered_data)
                            print(f"   📊 Filtered results: {filtered_count}")
                            
                            # Check if display updated
                            if hasattr(search_system, 'results_tree'):
                                display_count = len(search_system.results_tree.get_children())
                                print(f"   🖥️ Display count: {display_count}")
                                
                                if display_count == filtered_count:
                                    print(f"   ✅ Display matches filter results")
                                else:
                                    print(f"   ❌ Display mismatch! Expected {filtered_count}, showing {display_count}")
                            
                            # Reset filter
                            search_system.filter_vars['category'].set('الكل')
                            search_system.apply_filters()
                            
                            reset_count = len(search_system.filtered_data)
                            print(f"   🔄 After reset: {reset_count} (should be {len(records)})")
                    
                else:
                    print("❌ No data loaded in ActivityLogSearchSystem")
                
                # Clean up
                window.destroy()
            else:
                print("❌ Window creation failed")
            
            root.destroy()
            
        except Exception as e:
            print(f"❌ Error testing ActivityLogSearchSystem: {e}")
            import traceback
            traceback.print_exc()
        
        # 6. Test GUI elements
        print("\n6. 🎛️ Testing GUI Filter Elements:")
        
        try:
            root = tk.Tk()
            root.title("Filter Element Test")
            root.geometry("600x200")
            
            # Create test variables
            test_category_var = tk.StringVar(value="الكل")
            
            # Create combobox
            test_combo = ttk.Combobox(root, textvariable=test_category_var, 
                                    values=sorted(list(categories)), state="readonly")
            test_combo.pack(pady=20)
            
            # Create test button
            def test_filter_change():
                current_value = test_category_var.get()
                print(f"🔧 Manual test: Filter changed to '{current_value}'")
                
                # Test filtering logic
                filtered = [r for r in records if r.get('التصنيف', '') == current_value or current_value == 'الكل']
                print(f"   📊 Would show {len(filtered)} records")
            
            test_button = tk.Button(root, text="Test Current Filter", command=test_filter_change)
            test_button.pack(pady=10)
            
            # Bind change event
            def on_combo_change(event=None):
                new_value = test_category_var.get()
                print(f"🎯 Combo changed to: '{new_value}'")
                test_filter_change()
            
            test_combo.bind('<<ComboboxSelected>>', on_combo_change)
            
            tk.Label(root, text="Select different categories to test filtering logic", 
                    font=("Arial", 12)).pack(pady=10)
            
            # Run for a few seconds then close
            root.after(8000, root.destroy)  # Auto close after 8 seconds
            root.mainloop()
            
        except Exception as e:
            print(f"❌ Error in GUI test: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Diagnosis failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main diagnostic function"""
    
    print("🔍 FILTER SYSTEM DEEP DIAGNOSIS")
    print("=" * 50)
    
    success = diagnose_filter_issue()
    
    if success:
        print(f"\n✅ Diagnosis completed")
        print(f"📋 Check the output above for any issues found")
    else:
        print(f"\n❌ Diagnosis failed")
        print(f"🔧 There are critical issues that need fixing")

if __name__ == "__main__":
    main()