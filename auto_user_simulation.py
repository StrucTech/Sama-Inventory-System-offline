#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 AUTOMATIC USER SIMULATION
This script will automatically:
1. Login with admin/admin123
2. Navigate to Activity Log page
3. Test filters and watch displayed data
4. Report exactly what the user sees
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import MainWindow
from sheets.manager import SheetsManager

class AutoUserSimulation:
    def __init__(self):
        self.main_window = None
        self.filter_window = None
        self.test_results = []
        
    def log_result(self, message):
        """Log test results"""
        print(f"🤖 {message}")
        self.test_results.append(message)
        
    def simulate_login(self):
        """Simulate user login with admin/admin123"""
        self.log_result("=== STARTING AUTO USER SIMULATION ===")
        self.log_result("Step 1: Launching main application...")
        
        # Create main window
        root = tk.Tk()
        root.withdraw()  # Hide root initially
        
        # Initialize sheets manager
        sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
        if not sheets_manager.connect():
            self.log_result("❌ Failed to connect to Google Sheets!")
            return False
            
        self.log_result("✅ Connected to Google Sheets")
        
        # Create main window instance
        self.main_window = MainWindow(root, sheets_manager)
        
        # Simulate login
        self.log_result("Step 2: Simulating login with admin/admin123...")
        
        # Set login credentials programmatically
        if hasattr(self.main_window, 'username_var'):
            self.main_window.username_var.set("admin")
        if hasattr(self.main_window, 'password_var'):
            self.main_window.password_var.set("admin123")
            
        # Attempt login
        try:
            # Call login method if it exists
            if hasattr(self.main_window, 'login'):
                result = self.main_window.login()
                if result:
                    self.log_result("✅ Login successful!")
                else:
                    self.log_result("❌ Login failed!")
                    return False
            else:
                self.log_result("✅ Skipping login (direct access)")
        except Exception as e:
            self.log_result(f"⚠️ Login simulation: {e}")
            
        return True
        
    def simulate_activity_log_navigation(self):
        """Simulate clicking on Activity Log button"""
        self.log_result("Step 3: Navigating to Activity Log page...")
        
        try:
            # Find and simulate clicking the activity log button
            if hasattr(self.main_window, 'open_filter_search_window'):
                self.log_result("🖱️ Simulating click on 'بحث في سجل العمليات' button...")
                
                # Call the method that opens filter window
                self.main_window.open_filter_search_window()
                self.log_result("✅ Activity Log page opened!")
                return True
            else:
                self.log_result("❌ Could not find activity log method!")
                return False
                
        except Exception as e:
            self.log_result(f"❌ Error opening activity log: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    def simulate_filter_testing(self):
        """Simulate testing filters and watching data changes"""
        self.log_result("Step 4: Testing filters and watching displayed data...")
        
        # Wait a moment for the window to fully load
        time.sleep(2)
        
        try:
            # Import the activity log system to test directly
            from activity_log_search_system import ActivityLogSearchSystem
            
            # Create filter system with shared connection
            if hasattr(self.main_window, 'sheets_manager'):
                sheets_manager = self.main_window.sheets_manager
            else:
                sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
                sheets_manager.connect()
                
            self.log_result("🔄 Creating filter system...")
            filter_system = ActivityLogSearchSystem(sheets_manager=sheets_manager)
            
            # Wait for initialization
            time.sleep(1)
            
            # Check initial data count
            initial_count = len(filter_system.filtered_data) if hasattr(filter_system, 'filtered_data') else 0
            self.log_result(f"📊 Initial data count: {initial_count}")
            
            # Test different filters
            test_filters = [
                ("التصنيف", "أدوات سباكة"),
                ("التصنيف", "مواد البناء"),
                ("التصنيف", "أدوات عامة"),
                ("اسم المستخدم", "admin"),
                ("نوع العملية", "إضافة")
            ]
            
            for filter_type, filter_value in test_filters:
                self.log_result(f"\n🧪 Testing filter: {filter_type} = {filter_value}")
                
                # Get the appropriate combobox and set value
                if hasattr(filter_system, 'category_combo') and filter_type == "التصنيف":
                    combo = filter_system.category_combo
                elif hasattr(filter_system, 'user_combo') and filter_type == "اسم المستخدم":
                    combo = filter_system.user_combo
                elif hasattr(filter_system, 'operation_combo') and filter_type == "نوع العملية":
                    # Check if operation combo exists
                    combo = getattr(filter_system, 'operation_combo', None)
                else:
                    self.log_result(f"⚠️ Filter type {filter_type} not found")
                    continue
                    
                if combo:
                    # Set the filter value
                    combo.set(filter_value)
                    self.log_result(f"🔧 Set {filter_type} to: {filter_value}")
                    
                    # Trigger filter application
                    filter_system.apply_filters()
                    
                    # Wait for processing
                    time.sleep(0.5)
                    
                    # Check results
                    if hasattr(filter_system, 'filtered_data'):
                        filtered_count = len(filter_system.filtered_data)
                        self.log_result(f"📈 Results: {filtered_count} items")
                        
                        # Check what's actually displayed
                        if hasattr(filter_system, 'tree') and filter_system.tree:
                            displayed_count = len(filter_system.tree.get_children())
                            self.log_result(f"👁️ Displayed in table: {displayed_count} items")
                            
                            if displayed_count != filtered_count:
                                self.log_result(f"⚠️ MISMATCH: Filtered {filtered_count} but displaying {displayed_count}")
                            else:
                                self.log_result(f"✅ MATCH: Filter and display consistent")
                                
                            # Show sample of displayed data
                            if displayed_count > 0:
                                first_item = filter_system.tree.get_children()[0]
                                values = filter_system.tree.item(first_item)['values']
                                self.log_result(f"📋 First displayed item: {values[:3] if len(values) > 3 else values}")
                        else:
                            self.log_result("⚠️ No tree widget found for display verification")
                    else:
                        self.log_result("⚠️ No filtered_data attribute found")
                        
                    # Reset filter
                    combo.set("الكل")
                    filter_system.apply_filters()
                    time.sleep(0.5)
                    
                    if hasattr(filter_system, 'filtered_data'):
                        reset_count = len(filter_system.filtered_data)
                        self.log_result(f"🔄 After reset: {reset_count} items")
                else:
                    self.log_result(f"❌ Could not find combo for {filter_type}")
                    
        except Exception as e:
            self.log_result(f"❌ Error during filter testing: {e}")
            import traceback
            traceback.print_exc()
            
    def run_simulation(self):
        """Run the complete simulation"""
        print("🎯 STARTING AUTOMATIC USER SIMULATION")
        print("=" * 50)
        
        # Step 1: Login
        if not self.simulate_login():
            return False
            
        # Step 2: Navigate to Activity Log
        if not self.simulate_activity_log_navigation():
            return False
            
        # Step 3: Test filters
        self.simulate_filter_testing()
        
        # Summary
        self.log_result("\n" + "=" * 50)
        self.log_result("🎯 SIMULATION COMPLETED")
        self.log_result("📊 Summary of what the user would see:")
        
        for result in self.test_results[-10:]:  # Last 10 results
            if "Results:" in result or "Displayed:" in result or "MATCH:" in result or "MISMATCH:" in result:
                print(f"   {result}")
                
        return True

def main():
    """Main function to run the simulation"""
    simulator = AutoUserSimulation()
    
    try:
        success = simulator.run_simulation()
        if success:
            print("\n✅ Simulation completed successfully!")
        else:
            print("\n❌ Simulation failed!")
            
    except Exception as e:
        print(f"\n❌ Simulation error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()