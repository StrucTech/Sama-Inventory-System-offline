"""
Add item dialog for the Inventory Management System.
Allows users to select existing items or add new ones with categories.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Tuple, List, Dict, Any
from localization import get_text

class AddItemDialog:
    """Dialog for adding inventory items with existing item selection."""
    
    def __init__(self, parent, existing_items: List[Dict[str, Any]] = None):
        """
        Initialize the add item dialog.
        
        Args:
            parent: Parent window
            existing_items: List of existing items with their categories
        """
        self.parent = parent
        self.result = None
        self.dialog = None
        self.existing_items = existing_items or []
        self.is_new_item_mode = False
        
        # Extract unique items and categories
        self.unique_items = {}  # item_name -> category
        self.unique_categories = set()
        
        for item in self.existing_items:
            item_name = item.get('item_name', '')
            category = item.get('category', '')
            if item_name and item_name not in self.unique_items:
                self.unique_items[item_name] = category
            if category:
                self.unique_categories.add(category)
        
        self.unique_categories = sorted(list(self.unique_categories))
        
    def show(self) -> Optional[Tuple[str, str, int]]:
        """
        Show the dialog and return the result.
        
        Returns:
            Tuple of (item_name, category, quantity) or None if cancelled
        """
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("إضافة عنصر للمخزون")
        self.dialog.geometry("700x600")  # حجم أكبر لاستيعاب العناصر الجديدة
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
        self.main_frame = ttk.Frame(self.dialog, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(self.main_frame, text="إضافة عنصر للمخزون", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Mode selection frame
        mode_frame = ttk.LabelFrame(self.main_frame, text="اختر طريقة الإضافة", padding="15")
        mode_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Radio buttons for mode selection
        self.mode_var = tk.StringVar(value="")  # لا يوجد اختيار افتراضي
        
        print("🎛️ إعداد أزرار الاختيار")  # تشخيص
        
        # دوال للنقر على الأزرار
        def on_existing_click():
            print("📻 تم النقر على: عنصر موجود")
            self.mode_var.set("existing")
            self.on_mode_change()
        
        def on_new_click():
            print("📻 تم النقر على: عنصر جديد")
            self.mode_var.set("new")
            self.on_mode_change()
        
        existing_radio = ttk.Radiobutton(mode_frame, text="اختيار عنصر موجود", 
                                        variable=self.mode_var, value="existing",
                                        command=on_existing_click)
        existing_radio.pack(anchor=tk.W, pady=5)
        
        new_radio = ttk.Radiobutton(mode_frame, text="إضافة عنصر جديد", 
                                   variable=self.mode_var, value="new",
                                   command=on_new_click)
        new_radio.pack(anchor=tk.W, pady=5)
        
        # Content frame that changes based on mode
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Initially show message to select mode
        self.setup_selection_prompt()
        
        # Buttons frame
        self.buttons_frame = ttk.Frame(self.main_frame)
        self.buttons_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Cancel button
        cancel_btn = tk.Button(self.buttons_frame, 
                              text="إلغاء", 
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
        
        # Add button (initially hidden)
        self.add_btn = tk.Button(self.buttons_frame, 
                                text="إضافة", 
                                command=self.add_item,
                                font=("Arial", 14, "bold"),
                                bg="#4CAF50", 
                                fg="white", 
                                width=18, 
                                height=3,
                                relief="raised",
                                bd=4,
                                cursor="hand2")
        # Don't pack initially - will be shown when mode is selected
        
        # Bind Enter key to add item
        self.dialog.bind("<Return>", lambda e: self.add_item())
        self.dialog.bind("<Escape>", lambda e: self.cancel())
        
    def setup_selection_prompt(self):
        """Setup prompt to select mode."""
        prompt_frame = ttk.LabelFrame(self.content_frame, text="يرجى الاختيار", padding="20")
        prompt_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        prompt_label = ttk.Label(prompt_frame, 
                                text="يرجى اختيار طريقة الإضافة أعلاه:\n\n• اختيار عنصر موجود: لإضافة كمية لعنصر موجود\n• إضافة عنصر جديد: لإضافة عنصر جديد للمخزون",
                                font=("Arial", 12), justify=tk.CENTER)
        prompt_label.pack(expand=True)
        
        # Hide add button
        if hasattr(self, 'add_btn'):
            self.add_btn.pack_forget()
        
    def on_mode_change(self):
        """Handle mode change between existing and new item."""
        print(f"🔄 تغيير الوضع إلى: {self.mode_var.get()}")  # تشخيص
        
        # Clear the content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Setup UI based on selected mode
        mode = self.mode_var.get()
        print(f"🎯 الوضع المختار: {mode}")  # تشخيص
        
        if mode == "existing":
            print("📋 إعداد واجهة العناصر الموجودة")  # تشخيص
            self.is_new_item_mode = False
            self.setup_existing_items_ui()
        elif mode == "new":
            print("➕ إعداد واجهة العنصر الجديد")  # تشخيص
            self.is_new_item_mode = True
            self.setup_new_item_ui()
        else:
            print("❓ لا يوجد اختيار - إظهار رسالة الاختيار")  # تشخيص
            # No selection yet
            self.setup_selection_prompt()
            
    def setup_existing_items_ui(self):
        """Setup UI for selecting existing items."""
        if not self.unique_items:
            # No existing items
            no_items_label = ttk.Label(self.content_frame, 
                                      text="لا توجد عناصر موجودة، يرجى اختيار 'إضافة عنصر جديد'",
                                      font=("Arial", 12))
            no_items_label.pack(pady=20)
            return
            
        # Form frame for existing items
        form_frame = ttk.LabelFrame(self.content_frame, text="اختيار عنصر موجود", padding="15")
        form_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Item selection dropdown
        ttk.Label(form_frame, text="اختر العنصر:", font=("Arial", 11)).grid(row=0, column=0, sticky=tk.W, pady=8)
        self.item_combobox = ttk.Combobox(form_frame, width=35, font=("Arial", 12))
        self.item_combobox['values'] = list(self.unique_items.keys())
        self.item_combobox.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=8, padx=(10, 0))
        self.item_combobox.bind('<<ComboboxSelected>>', self.on_item_selected)
        
        # Category display (read-only)
        ttk.Label(form_frame, text="التصنيف:", font=("Arial", 11)).grid(row=1, column=0, sticky=tk.W, pady=8)
        self.category_display = ttk.Label(form_frame, text="", font=("Arial", 12), 
                                         background="white", relief="sunken")
        self.category_display.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=8, padx=(10, 0))
        
        # Quantity
        ttk.Label(form_frame, text="الكمية:", font=("Arial", 11)).grid(row=2, column=0, sticky=tk.W, pady=8)
        self.quantity_entry = ttk.Entry(form_frame, width=35, font=("Arial", 12))
        self.quantity_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=8, padx=(10, 0))
        self.quantity_entry.focus()
        
        # Configure column weight
        form_frame.columnconfigure(1, weight=1)
        
        # Show add button
        if hasattr(self, 'add_btn'):
            self.add_btn.pack(side=tk.RIGHT, padx=(15, 0))
        
    def setup_new_item_ui(self):
        """Setup UI for adding new items."""
        # Form frame for new items
        form_frame = ttk.LabelFrame(self.content_frame, text="إضافة عنصر جديد", padding="15")
        form_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Item name
        ttk.Label(form_frame, text="اسم العنصر:", font=("Arial", 11)).grid(row=0, column=0, sticky=tk.W, pady=8)
        self.new_item_name_entry = ttk.Entry(form_frame, width=35, font=("Arial", 12))
        self.new_item_name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=8, padx=(10, 0))
        self.new_item_name_entry.focus()
        
        # Category selection - using Entry + Button approach
        ttk.Label(form_frame, text="التصنيف:", font=("Arial", 11)).grid(row=1, column=0, sticky=tk.W, pady=8)
        
        # Category entry field
        self.new_category_entry = ttk.Entry(form_frame, width=30, font=("Arial", 12))
        self.new_category_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=8, padx=(10, 0))
        self.new_category_entry.insert(0, "اكتب تصنيف جديد...")
        self.new_category_entry.bind('<FocusIn>', self.on_category_entry_focus)
        self.new_category_entry.bind('<FocusOut>', self.on_category_entry_unfocus)
        
        # Category selection button
        category_btn = tk.Button(form_frame, text="اختر من القائمة", 
                               command=self.show_category_list,
                               font=("Arial", 9), bg="#2196F3", fg="white")
        category_btn.grid(row=1, column=2, pady=8, padx=(5, 0))
        
        # Category help label
        help_label = ttk.Label(form_frame, text="اكتب تصنيف جديد أو اضغط 'اختر من القائمة' لاختيار موجود", 
                              font=("Arial", 9), foreground="gray")
        help_label.grid(row=2, column=1, columnspan=2, sticky=tk.W, padx=(10, 0))
        
        # Quantity
        ttk.Label(form_frame, text="الكمية:", font=("Arial", 11)).grid(row=3, column=0, sticky=tk.W, pady=8)
        self.quantity_entry = ttk.Entry(form_frame, width=35, font=("Arial", 12))
        self.quantity_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=8, padx=(10, 0))
        
        # Configure column weight
        form_frame.columnconfigure(1, weight=1)
        
        # Show add button
        if hasattr(self, 'add_btn'):
            self.add_btn.pack(side=tk.RIGHT, padx=(15, 0))
        
    def on_item_selected(self, event=None):
        """Handle item selection from dropdown."""
        selected_item = self.item_combobox.get()
        if selected_item in self.unique_items:
            category = self.unique_items[selected_item]
            self.category_display.config(text=category)
    
    def on_category_entry_focus(self, event=None):
        """Handle focus in category entry."""
        if self.new_category_entry.get() == "اكتب تصنيف جديد...":
            self.new_category_entry.delete(0, tk.END)
    
    def on_category_entry_unfocus(self, event=None):
        """Handle focus out of category entry."""
        if not self.new_category_entry.get().strip():
            self.new_category_entry.insert(0, "اكتب تصنيف جديد...")
    
    def show_category_list(self):
        """Show category selection dialog."""
        if not self.unique_categories:
            messagebox.showinfo("لا توجد تصنيفات", "لا توجد تصنيفات محفوظة. يمكنك كتابة تصنيف جديد.")
            self.new_category_entry.focus()
            return
        
        # Create category selection window
        category_window = tk.Toplevel(self.dialog)
        category_window.title("اختيار التصنيف")
        category_window.geometry("400x300")
        category_window.transient(self.dialog)
        category_window.grab_set()
        
        # Center the window
        category_window.update_idletasks()
        x = (category_window.winfo_screenwidth() // 2) - (category_window.winfo_width() // 2)
        y = (category_window.winfo_screenheight() // 2) - (category_window.winfo_height() // 2)
        category_window.geometry(f"+{x}+{y}")
        
        # Title
        title_label = tk.Label(category_window, text="اختر التصنيف", 
                              font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Listbox with categories
        list_frame = tk.Frame(category_window)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        category_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, 
                                     font=("Arial", 12))
        category_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=category_listbox.yview)
        
        # Add categories to listbox
        for category in sorted(self.unique_categories):
            category_listbox.insert(tk.END, category)
        
        # Buttons
        btn_frame = tk.Frame(category_window)
        btn_frame.pack(pady=10)
        
        def select_category():
            selection = category_listbox.curselection()
            if selection:
                selected_category = category_listbox.get(selection[0])
                self.new_category_entry.delete(0, tk.END)
                self.new_category_entry.insert(0, selected_category)
                category_window.destroy()
            else:
                messagebox.showwarning("لم يتم اختيار تصنيف", "يرجى اختيار تصنيف من القائمة")
        
        def cancel_selection():
            category_window.destroy()
        
        select_btn = tk.Button(btn_frame, text="اختيار", command=select_category,
                              font=("Arial", 12), bg="#4CAF50", fg="white")
        select_btn.pack(side=tk.LEFT, padx=10)
        
        cancel_btn = tk.Button(btn_frame, text="إلغاء", command=cancel_selection,
                              font=("Arial", 12))
        cancel_btn.pack(side=tk.LEFT, padx=10)
        
        # Double click to select
        category_listbox.bind('<Double-Button-1>', lambda e: select_category())
            
    def add_item(self):
        """Add the item and close the dialog."""
        # Check if mode is selected
        mode = self.mode_var.get()
        if not mode:
            messagebox.showerror("خطأ", "يرجى اختيار طريقة الإضافة أولاً:\n• اختيار عنصر موجود\n• إضافة عنصر جديد")
            return
            
        if mode == "new":
            # New item mode
            if not hasattr(self, 'new_item_name_entry'):
                messagebox.showerror("خطأ", "يرجى اختيار 'إضافة عنصر جديد' أولاً")
                return
                
            item_name = self.new_item_name_entry.get().strip()
            category = self.new_category_entry.get().strip()
            quantity_str = self.quantity_entry.get().strip()
            
            # Validate inputs
            if not item_name:
                messagebox.showerror("خطأ", "يرجى إدخال اسم العنصر")
                self.new_item_name_entry.focus()
                return
                
            if not category or category == "اكتب تصنيف جديد...":
                messagebox.showerror("خطأ", "يرجى إدخال تصنيف للعنصر أو اختيار من القائمة")
                self.new_category_entry.focus()
                return
        elif mode == "existing":
            # Existing item mode
            if not hasattr(self, 'item_combobox'):
                messagebox.showerror("خطأ", "يرجى اختيار 'اختيار عنصر موجود' أولاً")
                return
                
            item_name = self.item_combobox.get().strip()
            category = self.category_display.cget("text")
            quantity_str = self.quantity_entry.get().strip()
            
            # Validate inputs
            if not item_name:
                messagebox.showerror("خطأ", "يرجى اختيار عنصر")
                self.item_combobox.focus()
                return
        else:
            messagebox.showerror("خطأ", "يرجى اختيار طريقة الإضافة")
            return
                
        # Validate quantity for both modes
        try:
            quantity = int(quantity_str)
            if quantity < 0:
                raise ValueError("Quantity must be non-negative")
        except ValueError:
            messagebox.showerror("خطأ", "يرجى إدخال كمية صحيحة (رقم موجب)")
            if hasattr(self, 'quantity_entry'):
                self.quantity_entry.focus()
            return
            
        # Set result and close dialog
        self.result = (item_name, category, quantity)
        self.dialog.destroy()
        
    def cancel(self):
        """Cancel and close the dialog."""
        self.result = None
        self.dialog.destroy()