"""
Outbound dialog for the Inventory Management System.
Allows warehouse managers to process outbound items.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Dict, Any, Tuple
from localization import get_text

class OutboundDialog:
    """Dialog for processing outbound items."""
    
    def __init__(self, parent, item: Dict[str, Any]):
        """
        Initialize the outbound dialog.
        
        Args:
            parent: Parent window
            item: Item data for outbound processing
        """
        self.parent = parent
        self.item = item
        self.result = None
        self.dialog = None
        
    def show(self) -> Optional[Tuple[int, str]]:
        """
        Show the dialog and return the result.
        
        Returns:
            Tuple of (outbound_quantity, recipient_name) or None if cancelled
        """
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title(get_text("outbound_title"))
        self.dialog.geometry("600x500")  # حجم أكبر
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
        title_label = ttk.Label(main_frame, text=get_text("outbound_item_title"), 
                               font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Item info frame
        info_frame = ttk.LabelFrame(main_frame, text=get_text("item_info"), padding="15")
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Item details
        ttk.Label(info_frame, text=get_text("item_label", self.item['item_name']), 
                 font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=2)
        ttk.Label(info_frame, text=get_text("available_quantity", int(self.item['quantity'])), 
                 font=("Arial", 10)).pack(anchor=tk.W, pady=2)
        
        # Outbound form frame
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Outbound quantity
        ttk.Label(form_frame, text=get_text("outbound_quantity_label"), 
                 font=("Arial", 11)).pack(anchor=tk.W, pady=(0, 5))
        self.quantity_entry = ttk.Entry(form_frame, width=25, font=("Arial", 12), justify="center")
        self.quantity_entry.pack(fill=tk.X, pady=(0, 15))
        self.quantity_entry.focus()
        
        # Recipient name
        ttk.Label(form_frame, text=get_text("recipient_name_label"), 
                 font=("Arial", 11)).pack(anchor=tk.W, pady=(0, 5))
        self.recipient_entry = ttk.Entry(form_frame, width=25, font=("Arial", 12))
        self.recipient_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Preview frame
        preview_frame = ttk.LabelFrame(main_frame, text=get_text("preview"), padding="15")
        preview_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.remaining_label = ttk.Label(preview_frame, 
                                        text=get_text("remaining_quantity", int(self.item['quantity'])), 
                                        font=("Arial", 12, "bold"))
        self.remaining_label.pack()
        
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
        
        # Outbound button (right side) - أكبر وأوضح
        outbound_btn = tk.Button(buttons_frame, 
                                text=get_text("outbound"), 
                                command=self.process_outbound,
                                font=("Arial", 14, "bold"),
                                bg="#4CAF50", 
                                fg="white", 
                                width=18, 
                                height=3,
                                relief="raised",
                                bd=4,
                                cursor="hand2")
        outbound_btn.pack(side=tk.RIGHT, padx=(15, 0))
        
        # Bind events for real-time calculation
        self.quantity_entry.bind("<KeyRelease>", self.update_preview)
        
        # Bind Enter key to process outbound
        self.dialog.bind("<Return>", lambda e: self.process_outbound())
        self.dialog.bind("<Escape>", lambda e: self.cancel())
        
    def update_preview(self, event=None):
        """Update the remaining quantity preview."""
        try:
            outbound_quantity = int(self.quantity_entry.get() or "0")
            available_quantity = int(self.item['quantity'])
            remaining_quantity = available_quantity - outbound_quantity
            
            if remaining_quantity < 0:
                self.remaining_label.config(
                    text=get_text("remaining_quantity", remaining_quantity), 
                    foreground="red"
                )
            else:
                self.remaining_label.config(
                    text=get_text("remaining_quantity", remaining_quantity), 
                    foreground="green"
                )
        except ValueError:
            self.remaining_label.config(
                text=get_text("remaining_quantity", int(self.item['quantity'])), 
                foreground="black"
            )
            
    def process_outbound(self):
        """Process the outbound operation and close the dialog."""
        # Get values
        quantity_str = self.quantity_entry.get().strip()
        recipient_name = self.recipient_entry.get().strip()
        
        # Validate inputs
        if not quantity_str:
            messagebox.showerror(get_text("error"), get_text("enter_outbound_quantity"))
            self.quantity_entry.focus()
            return
            
        try:
            outbound_quantity = int(quantity_str)
            if outbound_quantity <= 0:
                raise ValueError("Quantity must be positive")
        except ValueError:
            messagebox.showerror(get_text("error"), get_text("enter_valid_quantity"))
            self.quantity_entry.focus()
            return
            
        if not recipient_name:
            messagebox.showerror(get_text("error"), get_text("enter_recipient_name"))
            self.recipient_entry.focus()
            return
            
        # Check if there's enough quantity
        if outbound_quantity > self.item['quantity']:
            messagebox.showerror(get_text("error"), get_text("insufficient_quantity"))
            self.quantity_entry.focus()
            return
            
        # Set result and close dialog
        self.result = (outbound_quantity, recipient_name)
        self.dialog.destroy()
        
    def cancel(self):
        """Cancel and close the dialog."""
        self.result = None
        self.dialog.destroy()