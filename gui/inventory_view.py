"""
Inventory view component - displays inventory items in a table format.
"""

import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Any, Callable, Optional
from localization import get_text

# Luxury color scheme for inventory view
LUXURY_INVENTORY_COLORS = {
    'bg_main': '#1A1A2E',          # خلفية رئيسية داكنة
    'bg_card': '#2A2A3E',          # خلفية البطاقات
    'accent': '#DAA520',           # ذهبي
    'accent_hover': '#FFD700',     # ذهبي فاتح
    'text_primary': '#F5F5F5',     # نص أساسي
    'text_secondary': '#B8B8B8',   # نص ثانوي
    'border': '#FFD700',           # حدود ذهبية
    'selected': '#8B4513',         # بني ذهبي للاختيار
    'selected_text': '#FFD700'     # نص مختار ذهبي
}

class InventoryView(ttk.Frame):
    """Widget for displaying inventory items in a table."""
    
    def __init__(self, parent, selection_callback: Callable[[bool], None]):
        """
        Initialize the inventory view.
        
        Args:
            parent: Parent widget
            selection_callback: Function to call when selection changes
        """
        super().__init__(parent)
        self.selection_callback = selection_callback
        self.current_data = []  # Store current data for reference
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface with luxury styling."""
        # Configure the frame with luxury background
        self.configure(style='Luxury.TFrame')
        
        # Configure luxury treeview style
        style = ttk.Style()
        
        # Configure the luxury treeview theme
        style.theme_use('default')
        
        # Configure treeview colors
        style.configure("Luxury.Treeview",
                       background=LUXURY_INVENTORY_COLORS['bg_card'],
                       foreground=LUXURY_INVENTORY_COLORS['text_primary'],
                       fieldbackground=LUXURY_INVENTORY_COLORS['bg_card'],
                       borderwidth=2,
                       relief="solid")
        
        style.map("Luxury.Treeview",
                 background=[('selected', LUXURY_INVENTORY_COLORS['selected'])],
                 foreground=[('selected', LUXURY_INVENTORY_COLORS['selected_text'])])
        
        # Configure treeview heading style
        style.configure("Luxury.Treeview.Heading",
                       background=LUXURY_INVENTORY_COLORS['accent'],
                       foreground=LUXURY_INVENTORY_COLORS['bg_main'],
                       font=('Tahoma', 11, 'bold'),
                       relief="raised",
                       borderwidth=2)
        
        style.map("Luxury.Treeview.Heading",
                 background=[('active', LUXURY_INVENTORY_COLORS['accent_hover'])])
        
        # Configure scrollbar style
        style.configure("Luxury.Vertical.TScrollbar",
                       background=LUXURY_INVENTORY_COLORS['bg_card'],
                       troughcolor=LUXURY_INVENTORY_COLORS['bg_main'],
                       bordercolor=LUXURY_INVENTORY_COLORS['accent'],
                       arrowcolor=LUXURY_INVENTORY_COLORS['accent'],
                       darkcolor=LUXURY_INVENTORY_COLORS['accent'],
                       lightcolor=LUXURY_INVENTORY_COLORS['accent_hover'])
        
        style.configure("Luxury.Horizontal.TScrollbar",
                       background=LUXURY_INVENTORY_COLORS['bg_card'],
                       troughcolor=LUXURY_INVENTORY_COLORS['bg_main'],
                       bordercolor=LUXURY_INVENTORY_COLORS['accent'],
                       arrowcolor=LUXURY_INVENTORY_COLORS['accent'],
                       darkcolor=LUXURY_INVENTORY_COLORS['accent'],
                       lightcolor=LUXURY_INVENTORY_COLORS['accent_hover'])
        
        # Create treeview with luxury style
        columns = ("item_name", "category", "quantity", "project_id", "last_updated")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15,
                                style="Luxury.Treeview")
        
        # Configure columns with luxury headers
        self.tree.heading("item_name", text="🏷️ " + get_text("item_name"))
        self.tree.heading("category", text="📁 التصنيف")
        self.tree.heading("quantity", text="📦 " + get_text("quantity"))
        self.tree.heading("project_id", text="🏗️ رقم المشروع")
        self.tree.heading("last_updated", text="🕐 " + get_text("last_updated"))
        
        # Configure column widths
        self.tree.column("item_name", width=200, anchor="w")
        self.tree.column("category", width=150, anchor="center")
        self.tree.column("quantity", width=120, anchor="center")
        self.tree.column("project_id", width=100, anchor="center")
        self.tree.column("last_updated", width=180, anchor="center")
        
        # Create luxury scrollbars
        v_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview,
                                   style="Luxury.Vertical.TScrollbar")
        h_scrollbar = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview,
                                   style="Luxury.Horizontal.TScrollbar")
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Configure grid weights
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_selection_change)
        
        # Bind double-click event
        self.tree.bind("<Double-1>", self.on_double_click)
        
    def update_data(self, data: List[Dict[str, Any]]):
        """
        Update the displayed data.
        
        Args:
            data: List of inventory items
        """
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Store data for reference
        self.current_data = data
        
        # Add new items
        for i, item in enumerate(data):
            values = (
                item.get("item_name", ""),
                item.get("category", ""),
                int(item.get("quantity", 0)),
                item.get("project_id", ""),
                item.get("last_updated", "")
            )
            
            # Insert item with row number as tag for reference
            item_id = self.tree.insert("", "end", values=values, tags=(str(i),))
            
    def get_selected_item(self) -> Optional[Dict[str, Any]]:
        """
        Get the currently selected item.
        
        Returns:
            Selected item data or None if no selection
        """
        selection = self.tree.selection()
        if not selection:
            return None
            
        item_id = selection[0]
        
        # Get the item index from tags
        try:
            tags = self.tree.item(item_id, "tags")
            if tags and self.current_data:
                item_index = int(tags[0])
                if 0 <= item_index < len(self.current_data):
                    return self.current_data[item_index]
        except (ValueError, IndexError):
            pass
            
        return None
        
    def on_selection_change(self, event):
        """Handle selection change event."""
        has_selection = bool(self.tree.selection())
        self.selection_callback(has_selection)
        
    def on_double_click(self, event):
        """Handle double-click event."""
        # Double-click could trigger edit mode in the future
        pass