"""
Configuration management for the Inventory Management System.
Handles loading and saving application settings.
"""

import json
import os
from typing import Dict, Any

CONFIG_FILE = "config/config.json"
DEFAULT_CONFIG = {
    "credentials_file": "config/credentials.json",
    "spreadsheet_name": "Inventory Management",
    "worksheet_name": "Inventory",
    "columns": {
        "item_name": "A",
        "quantity": "B", 
        "unit_price": "C",
        "total_value": "D",
        "last_updated": "E"
    },
    "window": {
        "width": 800,
        "height": 600
    }
}

# متغير للوصول السريع للإعدادات
SPREADSHEET_CONFIG = DEFAULT_CONFIG

def load_config() -> Dict[str, Any]:
    """
    Load configuration from config file.
    Creates default config file if it doesn't exist.
    
    Returns:
        Dict containing configuration settings
    """
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                # Merge with defaults in case new keys were added
                merged_config = {**DEFAULT_CONFIG, **config}
                return merged_config
        else:
            # Create config directory if it doesn't exist
            os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
            save_config(DEFAULT_CONFIG)
            return DEFAULT_CONFIG.copy()
    except Exception as e:
        print(f"Error loading config: {e}")
        return DEFAULT_CONFIG.copy()

def save_config(config: Dict[str, Any]) -> bool:
    """
    Save configuration to config file.
    
    Args:
        config: Dictionary containing configuration settings
        
    Returns:
        True if successful, False otherwise
    """
    try:
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False

def get_credentials_path() -> str:
    """
    Get the path to the Google Sheets API credentials file.
    
    Returns:
        Path to credentials file
    """
    config = load_config()
    return config.get("credentials_file", "config/credentials.json")