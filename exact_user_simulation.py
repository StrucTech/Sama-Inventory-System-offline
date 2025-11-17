#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 EXACT USER EXPERIENCE SIMULATION
This will replicate EXACTLY what you do:
1. Run main_with_auth.py
2. Login with admin/admin123  
3. Click Activity Log button
4. Test filters and watch results
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import time
import threading

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def simulate_exact_user_experience():
    """Simulate the exact user experience step by step"""
    
    print("🎯 EXACT USER EXPERIENCE SIMULATION")
    print("="*60)
    print("This will do EXACTLY what you do:")
    print("1. Login with admin/admin123")
    print("2. Click 'بحث في سجل العمليات'") 
    print("3. Test filters and watch data changes")
    print("="*60)
    
    # Step 1: Import and run the main application
    print("📱 Step 1: Starting main_with_auth.py...")
    
    try:
        # Import the main modules
        from gui.login_window import LoginWindow
        from gui.main_window import MainWindow
        from sheets.manager import SheetsManager
        
        # Create root window
        root = tk.Tk()
        root.title("Inventory Management System")
        root.geometry("800x600")
        
        # Create login window
        print("🔐 Step 2: Creating login window...")
        login_window = LoginWindow(root)
        
        # Simulate automatic login with admin/admin123
        print("🤖 Step 3: Auto-filling credentials (admin/admin123)...")
        login_window.username_entry.delete(0, tk.END)
        login_window.username_entry.insert(0, "admin")
        login_window.password_entry.delete(0, tk.END) 
        login_window.password_entry.insert(0, "admin123")
        
        print("🔑 Step 4: Attempting login...")
        
        # Create a function to handle successful login
        def on_login_success():
            print("✅ Login successful!")
            
            # Connect to sheets
            print("🔌 Step 5: Connecting to Google Sheets...")
            sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
            
            if not sheets_manager.connect():
                print("❌ Failed to connect to Google Sheets!")
                return
                
            print("✅ Connected to Google Sheets successfully!")
            
            # Create main window
            print("🏠 Step 6: Creating main window...")
            main_window = MainWindow(root, sheets_manager)
            
            # Hide login and show main window
            login_window.destroy()
            root.deiconify()
            
            # Wait a moment for everything to load
            root.after(1000, lambda: test_activity_log_filters(main_window))
            
        def test_activity_log_filters(main_window):
            """Test the activity log filters exactly as user would"""
            print("🖱️ Step 7: Clicking 'بحث في سجل العمليات' button...")
            
            try:
                # Call the method that opens activity log
                main_window.open_filter_search_window()
                print("✅ Activity Log window opened!")
                
                # Wait for window to fully load
                root.after(2000, lambda: perform_filter_tests(main_window))
                
            except Exception as e:
                print(f"❌ Error opening activity log: {e}")
                import traceback
                traceback.print_exc()
                
        def perform_filter_tests(main_window):
            """Perform the actual filter tests"""
            print("🧪 Step 8: Testing filters and watching data changes...")
            
            try:
                # Find all windows
                windows = root.winfo_children()
                filter_window = None
                
                # Look for the activity log window
                for window in windows:
                    if hasattr(window, 'winfo_class') and window.winfo_class() == 'Toplevel':
                        filter_window = window
                        break
                        
                if not filter_window:
                    print("❌ Could not find activity log window!")
                    return
                    
                print("✅ Found activity log window!")
                
                # Find the filter components in the window
                def find_widget_by_text(parent, widget_type, text):
                    """Find widget by its text content"""
                    for child in parent.winfo_children():
                        if isinstance(child, widget_type):
                            try:
                                if hasattr(child, 'get') and text in str(child.get()):
                                    return child
                                elif hasattr(child, 'cget') and text in str(child.cget('text')):
                                    return child
                            except:
                                pass
                        # Recursively search children
                        result = find_widget_by_text(child, widget_type, text)
                        if result:
                            return result
                    return None
                
                def find_all_comboboxes(parent):
                    """Find all combobox widgets"""
                    comboboxes = []
                    for child in parent.winfo_children():
                        if isinstance(child, ttk.Combobox):
                            comboboxes.append(child)
                        comboboxes.extend(find_all_comboboxes(child))
                    return comboboxes
                
                def find_treeview(parent):
                    """Find the treeview widget"""
                    for child in parent.winfo_children():
                        if isinstance(child, ttk.Treeview):
                            return child
                        result = find_treeview(child)
                        if result:
                            return result
                    return None
                
                # Find the tree view (data display)
                tree = find_treeview(filter_window)
                if tree:
                    initial_count = len(tree.get_children())
                    print(f"📊 Initial data count in table: {initial_count} items")
                else:
                    print("❌ Could not find data table!")
                    return
                
                # Find all combo boxes
                combos = find_all_comboboxes(filter_window)
                print(f"🔍 Found {len(combos)} filter comboboxes")
                
                if len(combos) >= 2:  # Should have at least category and other filters
                    category_combo = combos[0]  # Assuming first is category
                    
                    # Test category filter
                    print("🧪 Testing category filter...")
                    
                    # Get available values
                    values = category_combo['values']
                    print(f"📋 Available categories: {values}")
                    
                    if len(values) > 1:
                        # Test with a specific category (not "الكل")
                        test_category = None
                        for val in values:
                            if val != "الكل" and val.strip():
                                test_category = val
                                break
                                
                        if test_category:
                            print(f"🔧 Setting category filter to: {test_category}")
                            
                            # Set the filter
                            category_combo.set(test_category)
                            
                            # Trigger the event
                            category_combo.event_generate('<<ComboboxSelected>>')
                            
                            # Wait for processing
                            def check_results():
                                filtered_count = len(tree.get_children())
                                print(f"📈 After filtering: {filtered_count} items displayed")
                                
                                if filtered_count != initial_count:
                                    print(f"✅ FILTER WORKING! Data changed: {initial_count} → {filtered_count}")
                                    
                                    # Show sample of filtered data
                                    if filtered_count > 0:
                                        first_item = tree.get_children()[0]
                                        values = tree.item(first_item)['values']
                                        print(f"📋 Sample filtered item: {values[:5] if len(values) > 5 else values}")
                                else:
                                    print(f"❌ FILTER NOT WORKING! Data unchanged: {initial_count} items")
                                
                                # Reset filter and test again
                                print("🔄 Resetting filter...")
                                category_combo.set("الكل")
                                category_combo.event_generate('<<ComboboxSelected>>')
                                
                                def check_reset():
                                    reset_count = len(tree.get_children())
                                    print(f"📈 After reset: {reset_count} items displayed")
                                    
                                    if reset_count == initial_count:
                                        print("✅ RESET WORKING! Data restored to original count")
                                    else:
                                        print(f"❌ RESET NOT WORKING! Expected {initial_count}, got {reset_count}")
                                    
                                    print("\n" + "="*60)
                                    print("🎯 SIMULATION COMPLETE!")
                                    print("📊 SUMMARY OF WHAT USER SEES:")
                                    print(f"   Initial: {initial_count} items")
                                    print(f"   Filtered: {filtered_count} items") 
                                    print(f"   Reset: {reset_count} items")
                                    
                                    if filtered_count != initial_count:
                                        print("✅ CONCLUSION: Filters ARE working correctly!")
                                    else:
                                        print("❌ CONCLUSION: Filters are NOT working!")
                                    print("="*60)
                                
                                root.after(1000, check_reset)
                            
                            root.after(1000, check_results)
                        else:
                            print("❌ No test categories found!")
                    else:
                        print("❌ No category values available!")
                else:
                    print("❌ Could not find enough filter comboboxes!")
                    
            except Exception as e:
                print(f"❌ Error during filter testing: {e}")
                import traceback
                traceback.print_exc()
        
        # Override the login method to automatically succeed
        original_login = login_window.login
        def auto_login():
            username = login_window.username_entry.get()
            password = login_window.password_entry.get()
            
            if username == "admin" and password == "admin123":
                on_login_success()
                return True
            else:
                return original_login()
                
        login_window.login = auto_login
        
        # Auto-trigger login after a moment
        root.after(500, auto_login)
        
        # Start the GUI
        print("🎮 Starting GUI simulation...")
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Simulation failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    simulate_exact_user_experience()