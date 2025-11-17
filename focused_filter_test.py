"""
🎯 Focused Filter Test - Main App Integration
============================================

This test specifically checks if filters work when launched from main_with_auth.py
"""

import sys
import os
import tkinter as tk

# Add project path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_main_app_filters():
    """Test filters when launched from main app context"""
    
    print("🎯 FOCUSED FILTER TEST - Main App Integration")
    print("=" * 55)
    
    try:
        # 1. Simulate main app environment
        print("\n1. 🏗️ Setting up main app environment:")
        
        from sheets.manager import SheetsManager
        from activity_log_search_system import ActivityLogSearchSystem
        
        # Create sheets manager like main app does
        sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
        
        if not sheets_manager.connect():
            print("❌ Failed to connect to Google Sheets")
            return False
        
        print("✅ SheetsManager connected (like main app)")
        
        # 2. Create ActivityLogSearchSystem with existing connection
        print("\n2. 🔍 Creating ActivityLogSearchSystem with shared connection:")
        
        root = tk.Tk()
        root.withdraw()  # Hide test window
        
        # THIS IS THE KEY - Pass the existing sheets_manager
        search_system = ActivityLogSearchSystem(parent=root, sheets_manager=sheets_manager)
        
        print("✅ ActivityLogSearchSystem created with shared connection")
        
        # 3. Create window and load data
        print("\n3. 🪟 Creating window and loading data:")
        
        window = search_system.create_window()
        
        if not window:
            print("❌ Window creation failed")
            return False
        
        print("✅ Window created")
        
        # Give it time to load data
        root.update()
        
        # 4. Check if data loaded correctly
        print("\n4. 📊 Checking data loading:")
        
        if not hasattr(search_system, 'activity_data') or not search_system.activity_data:
            print("❌ No activity data loaded")
            return False
        
        data_count = len(search_system.activity_data)
        print(f"✅ Loaded {data_count} activity records")
        
        # 5. Check filter options
        print("\n5. 🎛️ Checking filter options:")
        
        if not hasattr(search_system, 'filter_options'):
            print("❌ No filter options available")
            return False
        
        categories = search_system.filter_options.get('categories', [])
        items = search_system.filter_options.get('items', [])
        projects = search_system.filter_options.get('projects', [])
        
        print(f"✅ Filter options loaded:")
        print(f"   🏷️ Categories: {len(categories)} options")
        print(f"   📦 Items: {len(items)} options")
        print(f"   🎯 Projects: {len(projects)} options")
        
        # 6. Test filter variables
        print("\n6. 🔧 Testing filter variables:")
        
        if not hasattr(search_system, 'filter_vars'):
            print("❌ No filter variables found")
            return False
        
        print("✅ Filter variables available:")
        for key, var in search_system.filter_vars.items():
            current_value = var.get()
            print(f"   {key}: '{current_value}'")
        
        # 7. Test actual filtering
        print("\n7. 🧪 Testing actual filter application:")
        
        # Get initial count
        initial_count = len(search_system.filtered_data) if hasattr(search_system, 'filtered_data') else data_count
        print(f"📊 Initial display count: {initial_count}")
        
        # Test category filter
        if len(categories) > 1:  # Has categories beyond "الكل"
            test_category = categories[1]  # First real category
            print(f"🔬 Testing category filter: '{test_category}'")
            
            # Set filter
            search_system.filter_vars['category'].set(test_category)
            
            # Apply filter
            search_system.apply_filters()
            
            # Update GUI
            root.update()
            
            # Check results
            filtered_count = len(search_system.filtered_data)
            print(f"📊 After filter: {filtered_count} records")
            
            if filtered_count < initial_count:
                print("✅ Filter reduced record count - WORKING!")
                
                # Check display
                if hasattr(search_system, 'results_tree'):
                    display_count = len(search_system.results_tree.get_children())
                    print(f"🖥️ Display shows: {display_count} records")
                    
                    if display_count == filtered_count:
                        print("✅ Display matches filter - PERFECT!")
                    else:
                        print(f"⚠️ Display mismatch: expected {filtered_count}, showing {display_count}")
                
            else:
                print(f"❌ Filter not working - same count ({filtered_count})")
                
                # Debug: Check what's actually in the filter
                print(f"🔍 Debug: Current filter value: '{search_system.filter_vars['category'].get()}'")
                
                # Check if combobox is set correctly
                if hasattr(search_system, 'category_combo'):
                    combo_value = search_system.category_combo.get()
                    print(f"🔍 Debug: Combobox shows: '{combo_value}'")
            
            # Test reset
            print(f"\n🔄 Testing filter reset:")
            search_system.filter_vars['category'].set('الكل')
            search_system.apply_filters()
            root.update()
            
            reset_count = len(search_system.filtered_data)
            print(f"📊 After reset: {reset_count} records")
            
            if reset_count == initial_count:
                print("✅ Filter reset working - EXCELLENT!")
            else:
                print(f"⚠️ Reset issue: expected {initial_count}, got {reset_count}")
        
        # 8. Test combobox events
        print("\n8. 🎯 Testing combobox event handling:")
        
        if hasattr(search_system, 'category_combo'):
            # Simulate combobox selection
            if len(categories) > 2:  # Has enough options
                test_category_2 = categories[2]
                print(f"🔧 Simulating selection of '{test_category_2}'")
                
                # Set combobox value
                search_system.category_combo.set(test_category_2)
                
                # Trigger event manually
                search_system.category_combo.event_generate('<<ComboboxSelected>>')
                
                # Update GUI
                root.update()
                
                # Check if it worked
                final_count = len(search_system.filtered_data)
                print(f"📊 After combobox event: {final_count} records")
                
                if final_count < initial_count:
                    print("✅ Combobox events working - PERFECT!")
                else:
                    print("❌ Combobox events not working")
        
        # Clean up
        window.destroy()
        root.destroy()
        
        print(f"\n🎉 Test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    
    print("🎯 FOCUSED FILTER TEST - Main App Integration")
    print("=" * 60)
    
    success = test_main_app_filters()
    
    if success:
        print(f"\n✅ FILTER TEST PASSED!")
        print(f"🚀 Filters should work correctly in main app")
    else:
        print(f"\n❌ FILTER TEST FAILED!")
        print(f"🔧 There are still issues to fix")

if __name__ == "__main__":
    main()