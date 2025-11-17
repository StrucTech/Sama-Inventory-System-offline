"""
🔍 Debug Filter System Test
===========================
This test will help us understand exactly what's happening with the filters
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Add project path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sheets.manager import SheetsManager

class FilterDebugTest:
    def __init__(self):
        """Initialize the filter debug test"""
        self.window = tk.Tk()
        self.window.title("🔍 Filter Debug Test")
        self.window.geometry("800x600")
        
        self.sheets_manager = None
        self.activity_data = []
        self.filtered_data = []
        
        # Filter variables
        self.filter_vars = {
            'category': tk.StringVar(value="الكل"),
            'item': tk.StringVar(value="الكل"),
            'project': tk.StringVar(value="الكل")
        }
        
        self.create_interface()
        self.load_data()
    
    def create_interface(self):
        """Create the interface"""
        
        # Title
        title_label = tk.Label(self.window, text="🔍 Filter Debug Test", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Status label
        self.status_label = tk.Label(self.window, text="Ready", 
                                   font=("Arial", 12))
        self.status_label.pack(pady=5)
        
        # Filters frame
        filters_frame = tk.LabelFrame(self.window, text="Filters", 
                                    font=("Arial", 12, "bold"))
        filters_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Create filter controls
        filter_row = tk.Frame(filters_frame)
        filter_row.pack(fill=tk.X, padx=10, pady=10)
        
        # Category filter
        tk.Label(filter_row, text="Category:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        self.category_combo = ttk.Combobox(filter_row, textvariable=self.filter_vars['category'],
                                         width=15, state="readonly")
        self.category_combo.pack(side=tk.LEFT, padx=5)
        self.category_combo.bind('<<ComboboxSelected>>', self.on_filter_change)
        
        # Item filter  
        tk.Label(filter_row, text="Item:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        self.item_combo = ttk.Combobox(filter_row, textvariable=self.filter_vars['item'],
                                     width=20, state="readonly")
        self.item_combo.pack(side=tk.LEFT, padx=5)
        self.item_combo.bind('<<ComboboxSelected>>', self.on_filter_change)
        
        # Project filter
        tk.Label(filter_row, text="Project:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        self.project_combo = ttk.Combobox(filter_row, textvariable=self.filter_vars['project'],
                                        width=15, state="readonly")
        self.project_combo.pack(side=tk.LEFT, padx=5)
        self.project_combo.bind('<<ComboboxSelected>>', self.on_filter_change)
        
        # Test button
        test_btn = tk.Button(filter_row, text="Manual Test", command=self.manual_test,
                           bg="#27ae60", fg="white", font=("Arial", 10, "bold"))
        test_btn.pack(side=tk.LEFT, padx=10)
        
        # Clear button
        clear_btn = tk.Button(filter_row, text="Clear Filters", command=self.clear_filters,
                            bg="#e74c3c", fg="white", font=("Arial", 10, "bold"))
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Results frame
        results_frame = tk.LabelFrame(self.window, text="Results", 
                                    font=("Arial", 12, "bold"))
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create treeview
        columns = ('Date', 'Operation', 'Item', 'Category', 'Quantity', 'Project')
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.results_tree.heading(col, text=col, anchor='center')
            self.results_tree.column(col, width=120, anchor='center')
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        h_scrollbar = ttk.Scrollbar(results_frame, orient=tk.HORIZONTAL, command=self.results_tree.xview)
        
        self.results_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack everything
        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Info label
        self.info_label = tk.Label(self.window, text="No data loaded", 
                                 font=("Arial", 10))
        self.info_label.pack(pady=5)
    
    def load_data(self):
        """Load data from Google Sheets"""
        
        print("🔄 Loading data...")
        self.status_label.config(text="Loading data from Google Sheets...")
        self.window.update()
        
        try:
            # Connect to sheets
            self.sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
            
            if not self.sheets_manager.connect():
                print("❌ Failed to connect to Google Sheets")
                self.status_label.config(text="Failed to connect to Google Sheets")
                return
            
            print("✅ Connected to Google Sheets")
            
            # Load activity log data
            activity_worksheet = self.sheets_manager.spreadsheet.worksheet('Activity_Log_v2_20251108')
            activity_values = activity_worksheet.get_all_values()
            
            if not activity_values:
                print("❌ No data in Activity_Log_v2_20251108")
                self.status_label.config(text="No data found")
                return
            
            # Process data
            headers = activity_values[0]
            print(f"📋 Headers: {headers}")
            
            self.activity_data = []
            for i, row in enumerate(activity_values[1:], 2):
                if row and row[0]:  # Check if date exists
                    record = {}
                    for j, header in enumerate(headers):
                        record[header] = row[j] if j < len(row) else ""
                    self.activity_data.append(record)
            
            print(f"✅ Loaded {len(self.activity_data)} records")
            self.status_label.config(text=f"Loaded {len(self.activity_data)} records")
            
            # Setup filter options
            self.setup_filter_options()
            
            # Display all data initially
            self.apply_filters()
            
        except Exception as e:
            error_msg = f"❌ Error loading data: {str(e)}"
            print(error_msg)
            import traceback
            traceback.print_exc()
            self.status_label.config(text=error_msg)
    
    def setup_filter_options(self):
        """Setup filter dropdown options"""
        
        print("🔧 Setting up filter options...")
        
        # Collect unique values
        categories = set(['الكل'])
        items = set(['الكل'])  
        projects = set(['الكل'])
        
        for record in self.activity_data:
            category = record.get('التصنيف', '')
            item = record.get('اسم العنصر', '')
            project = record.get('رقم المشروع', '')
            
            if category:
                categories.add(category)
            if item:
                items.add(item)
            if project:
                projects.add(project)
        
        # Update comboboxes
        self.category_combo['values'] = sorted(list(categories))
        self.item_combo['values'] = sorted(list(items))
        self.project_combo['values'] = sorted(list(projects))
        
        print(f"📊 Filter options setup:")
        print(f"   Categories: {len(categories)-1}")
        print(f"   Items: {len(items)-1}")
        print(f"   Projects: {len(projects)-1}")
    
    def on_filter_change(self, event=None):
        """Called when any filter changes"""
        
        print(f"🔄 Filter changed! Current values:")
        print(f"   Category: {self.filter_vars['category'].get()}")
        print(f"   Item: {self.filter_vars['item'].get()}")
        print(f"   Project: {self.filter_vars['project'].get()}")
        
        self.apply_filters()
    
    def apply_filters(self):
        """Apply current filters to data"""
        
        print(f"\\n🔍 Applying filters...")
        
        # Get current filter values
        category_filter = self.filter_vars['category'].get()
        item_filter = self.filter_vars['item'].get()
        project_filter = self.filter_vars['project'].get()
        
        print(f"📋 Filter values:")
        print(f"   Category: '{category_filter}'")
        print(f"   Item: '{item_filter}'")
        print(f"   Project: '{project_filter}'")
        
        # Apply filters
        self.filtered_data = []
        
        for record in self.activity_data:
            include = True
            
            # Category filter
            if category_filter != "الكل":
                if record.get('التصنيف', '') != category_filter:
                    include = False
            
            # Item filter
            if item_filter != "الكل":
                if record.get('اسم العنصر', '') != item_filter:
                    include = False
            
            # Project filter
            if project_filter != "الكل":
                if record.get('رقم المشروع', '') != project_filter:
                    include = False
            
            if include:
                self.filtered_data.append(record)
        
        print(f"📊 Filtering result: {len(self.filtered_data)} out of {len(self.activity_data)} records")
        
        # Update display
        self.display_results()
    
    def display_results(self):
        """Display filtered results"""
        
        print(f"🖥️ Displaying {len(self.filtered_data)} results...")
        
        # Clear existing items
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        print("🗑️ Cleared existing items from tree")
        
        # Add filtered results
        for i, record in enumerate(self.filtered_data):
            
            # Get quantity info
            added_qty = record.get('الكمية المضافة', '0')
            removed_qty = record.get('الكمية المخرجة', '0')
            
            if added_qty != '0':
                quantity = f"+{added_qty}"
            elif removed_qty != '0':
                quantity = f"-{removed_qty}"
            else:
                quantity = "0"
            
            values = (
                record.get('التاريخ', ''),
                record.get('نوع العملية', ''),
                record.get('اسم العنصر', ''),
                record.get('التصنيف', ''),
                quantity,
                record.get('رقم المشروع', '')
            )
            
            self.results_tree.insert("", "end", values=values)
            
            if i < 3:  # Print first 3 for debugging
                print(f"   Added record {i+1}: {values}")
        
        print(f"✅ Added {len(self.filtered_data)} records to tree")
        
        # Update info label
        self.info_label.config(text=f"Showing {len(self.filtered_data)} of {len(self.activity_data)} records")
        
        # Force update
        self.window.update_idletasks()
        print("🔄 UI updated")
    
    def clear_filters(self):
        """Clear all filters"""
        
        print("🗑️ Clearing all filters...")
        
        self.filter_vars['category'].set("الكل")
        self.filter_vars['item'].set("الكل")
        self.filter_vars['project'].set("الكل")
        
        # Update combobox displays
        self.category_combo.set("الكل")
        self.item_combo.set("الكل")
        self.project_combo.set("الكل")
        
        self.apply_filters()
        
        print("✅ All filters cleared")
    
    def manual_test(self):
        """Manual test button"""
        
        print("🧪 Manual test triggered!")
        
        # Set a specific filter for testing
        self.filter_vars['category'].set('مواد البناء')
        self.category_combo.set('مواد البناء')
        
        print("Set category filter to 'مواد البناء'")
        self.apply_filters()
    
    def run(self):
        """Run the test window"""
        print("🚀 Starting filter debug test...")
        self.window.mainloop()

def main():
    """Main function"""
    
    print("🔍 Filter Debug Test")
    print("=" * 40)
    
    test = FilterDebugTest()
    test.run()

if __name__ == "__main__":
    main()