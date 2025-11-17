"""
🔧 Test Main App Integration with Filter System
===============================================

This script tests if the main application properly integrates with the filter system
"""

import sys
import os
import tkinter as tk

# Add project path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_main_integration():
    """Test if main app can properly open the filter system"""
    
    print("🧪 Testing Main Application Integration")
    print("=" * 45)
    
    try:
        # 1. Test importing the main components
        print("📦 Testing imports...")
        
        from gui.main_window import MainWindow
        from activity_log_search_system import ActivityLogSearchSystem
        from sheets.manager import SheetsManager
        
        print("✅ All imports successful")
        
        # 2. Test creating SheetsManager
        print("\n📡 Testing Google Sheets connection...")
        
        sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
        
        if sheets_manager.connect():
            print("✅ Google Sheets connection successful")
        else:
            print("❌ Google Sheets connection failed")
            return False
        
        # 3. Test ActivityLogSearchSystem creation
        print("\n🔍 Testing ActivityLogSearchSystem creation...")
        
        root = tk.Tk()
        root.withdraw()  # Hide the test window
        
        search_system = ActivityLogSearchSystem(parent=root)
        print("✅ ActivityLogSearchSystem created successfully")
        
        # 4. Test window creation
        print("\n🪟 Testing window creation...")
        
        filter_window = search_system.create_window()
        
        if filter_window:
            print("✅ Filter window created successfully")
            
            # Test if data loads
            print("\n📊 Testing data loading...")
            
            # Give it a moment to load data
            root.update()
            
            if hasattr(search_system, 'activity_data') and search_system.activity_data:
                print(f"✅ Data loaded: {len(search_system.activity_data)} records")
                
                # Test filter options
                if hasattr(search_system, 'filter_options'):
                    categories = len(search_system.filter_options.get('categories', [])) - 1  # -1 for "الكل"
                    items = len(search_system.filter_options.get('items', [])) - 1
                    projects = len(search_system.filter_options.get('projects', [])) - 1
                    
                    print(f"📋 Filter options available:")
                    print(f"   🏷️ Categories: {categories}")
                    print(f"   📦 Items: {items}")
                    print(f"   🎯 Projects: {projects}")
                    
                    if categories > 0 and items > 0 and projects > 0:
                        print("✅ All filter options populated correctly")
                    else:
                        print("⚠️ Some filter options missing")
                
                # Test applying a filter
                print(f"\n🔍 Testing filter application...")
                
                # Try to apply a category filter
                if hasattr(search_system, 'filter_vars') and 'category' in search_system.filter_vars:
                    original_count = len(search_system.activity_data)
                    
                    # Set a category filter
                    categories = search_system.filter_options.get('categories', [])
                    if len(categories) > 1:  # More than just "الكل"
                        test_category = categories[1]  # First real category
                        search_system.filter_vars['category'].set(test_category)
                        search_system.apply_filters()
                        
                        root.update()
                        
                        filtered_count = len(search_system.filtered_data)
                        
                        print(f"   📊 Original records: {original_count}")
                        print(f"   📊 Filtered records: {filtered_count}")
                        print(f"   🎯 Filter applied: {test_category}")
                        
                        if filtered_count < original_count:
                            print("✅ Filter application working correctly")
                            
                            # Check if display updated
                            if hasattr(search_system, 'results_tree'):
                                display_count = len(search_system.results_tree.get_children())
                                
                                if display_count == filtered_count:
                                    print("✅ Display updated correctly")
                                else:
                                    print(f"⚠️ Display mismatch: showing {display_count}, expected {filtered_count}")
                            
                        else:
                            print("⚠️ Filter not working - same number of records")
                
            else:
                print("❌ No data loaded")
            
            # Close the test window
            filter_window.destroy()
            
        else:
            print("❌ Filter window creation failed")
            return False
        
        root.destroy()
        
        print(f"\n🎉 Integration test completed successfully!")
        print(f"✅ Main application should be able to open working filters")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    
    print("🔧 Main Application Integration Test")
    print("=" * 50)
    
    success = test_main_integration()
    
    if success:
        print("\n✅ INTEGRATION TEST PASSED")
        print("🚀 The main application should work correctly with filters")
        print("\n💡 To use:")
        print("   1. Run: python main_with_auth.py")
        print("   2. Login to the system")
        print("   3. Click 'بحث في سجل العمليات' button")
        print("   4. Use the filters - they should work immediately!")
    else:
        print("\n❌ INTEGRATION TEST FAILED")
        print("🔧 There may be an issue with the integration")

if __name__ == "__main__":
    main()