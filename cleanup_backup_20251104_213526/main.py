"""
Inventory Management System - Main Application
A desktop application for managing inventory using Google Sheets as the data store.
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import MainWindow
from config.settings import load_config, save_config
from localization import get_text

def main():
    """Main entry point of the application."""
    try:
        # Load configuration
        config = load_config()
        
        # Create and run the main application window
        root = tk.Tk()
        app = MainWindow(root, config)
        
        # Set window properties
        root.title(get_text("app_title"))
        root.geometry("800x600")
        root.minsize(600, 400)
        
        # Center the window
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Start the application
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start application: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()