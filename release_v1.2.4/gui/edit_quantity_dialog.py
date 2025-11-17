"""
Edit quantity dialog for the Inventory Management System.
Allows users to edit the quantity of existing inventory items.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Dict, Any
from localization import get_text

class EditQuantityDialog:
    """Dialog for editing item quantities."""
    
    def __init__(self, parent, item: Dict[str, Any]):
        """
        Initialize the edit quantity dialog.
        
        Args:
            parent: Parent window
            item: Item data to edit
        """
        self.parent = parent
        self.item = item
        self.result = None
        self.dialog = None
        
    def show(self) -> Optional[int]:
        """
        Show the dialog and return the result.
        
        Returns:
            New quantity value or None if cancelled
        """
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title(get_text("edit_quantity_title"))
        self.dialog.geometry("550x450")  # حجم أكبر
        self.dialog.resizable(False, False)
        
        # Make dialog modal
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        self.setup_ui()
        
        # Wait for dialog to close
        self.dialog.wait_window()
        
        return self.result
        
    def setup_ui(self):
        """Set up the user interface."""
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text=get_text("edit_item_quantity"), 
                               font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Item info frame
        info_frame = ttk.LabelFrame(main_frame, text=get_text("item_info"), padding="15")
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Item details
        ttk.Label(info_frame, text=get_text("item_label", self.item['item_name']), 
                 font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=2)
        ttk.Label(info_frame, text=get_text("current_quantity", int(self.item['quantity'])), 
                 font=("Arial", 10)).pack(anchor=tk.W, pady=2)
        
        # Edit frame
        edit_frame = ttk.Frame(main_frame)
        edit_frame.pack(fill=tk.X, pady=(0, 20))
        
        # New quantity
        ttk.Label(edit_frame, text=get_text("new_quantity"), font=("Arial", 11)).pack(anchor=tk.W, pady=(0, 5))
        self.quantity_entry = ttk.Entry(edit_frame, width=25, font=("Arial", 14), justify="center")
        self.quantity_entry.pack(fill=tk.X, pady=(0, 10))
        self.quantity_entry.insert(0, str(self.item['quantity']))
        self.quantity_entry.select_range(0, tk.END)
        self.quantity_entry.focus()
        
        # Preview frame
        preview_frame = ttk.LabelFrame(main_frame, text=get_text("preview"), padding="15")
        preview_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.quantity_preview_label = ttk.Label(preview_frame, 
                                               text=get_text("new_quantity") + f" {self.item['quantity']}", 
                                               font=("Arial", 12, "bold"))
        self.quantity_preview_label.pack()
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Cancel button (left side) - أكبر وأوضح
        cancel_btn = tk.Button(buttons_frame, 
                              text=get_text("cancel"), 
                              command=self.cancel,
                              font=("Arial", 14, "bold"),
                              bg="#f44336", 
                              fg="white", 
                              width=18, 
                              height=3,
                              relief="raised",
                              bd=4,
                              cursor="hand2")
        cancel_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # Update button (right side) - أكبر وأوضح
        update_btn = tk.Button(buttons_frame, 
                              text=get_text("update"), 
                              command=self.update_quantity,
                              font=("Arial", 14, "bold"),
                              bg="#4CAF50", 
                              fg="white", 
                              width=18, 
                              height=3,
                              relief="raised",
                              bd=4,
                              cursor="hand2")
        update_btn.pack(side=tk.RIGHT, padx=(15, 0))
        
        # Bind events for real-time calculation
        self.quantity_entry.bind("<KeyRelease>", self.update_preview)
        
        # Bind Enter key to update
        self.dialog.bind("<Return>", lambda e: self.update_quantity())
        self.dialog.bind("<Escape>", lambda e: self.cancel())
        
        # Initial preview update
        self.update_preview()
        
    def update_preview(self, event=None):
        """Update the quantity preview."""
        try:
            quantity = int(self.quantity_entry.get() or "0")
            self.quantity_preview_label.config(text=get_text("new_quantity") + f" {quantity}")
        except ValueError:
            current_quantity = int(self.item['quantity'])
            self.quantity_preview_label.config(text=get_text("new_quantity") + f" {current_quantity}")
            
    def update_quantity(self):
        """Update the quantity and close the dialog."""
        # Get new quantity
        quantity_str = self.quantity_entry.get().strip()
        
        # Validate input
        try:
            quantity = int(quantity_str)
            if quantity < 0:
                raise ValueError("Quantity must be non-negative")
        except ValueError:
            messagebox.showerror(get_text("error"), get_text("enter_valid_quantity"))
            self.quantity_entry.focus()
            return
            
        # Check if quantity actually changed
        if quantity == self.item['quantity']:
            messagebox.showinfo(get_text("no_change"), get_text("quantity_same"))
            return
            
        # Set result and close dialog
        self.result = quantity
        self.dialog.destroy()
        
    def cancel(self):
        """Cancel and close the dialog."""
        self.result = None
        self.dialog.destroy()