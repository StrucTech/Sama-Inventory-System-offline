"""
Setup script for the Inventory Management System.
Helps users verify their setup and test the connection.
"""

import os
import sys
import json
from pathlib import Path

def check_requirements():
    """Check if all required packages are installed."""
    print("Checking Python packages...")
    
    required_packages = [
        'gspread',
        'google.auth',
        'google_auth_oauthlib',
        'google_auth_httplib2'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("All required packages are installed!")
    return True

def check_config():
    """Check if configuration files exist."""
    print("\nChecking configuration files...")
    
    config_file = Path("config/config.json")
    credentials_file = Path("config/credentials.json")
    
    if not config_file.exists():
        print("✗ config/config.json - MISSING")
        return False
    else:
        print("✓ config/config.json")
    
    if not credentials_file.exists():
        print("✗ config/credentials.json - MISSING")
        print("  Please copy your Google Sheets API credentials to this file.")
        print("  See config/credentials_template.json for the expected format.")
        return False
    else:
        print("✓ config/credentials.json")
    
    return True

def validate_credentials():
    """Validate the credentials file format."""
    print("\nValidating credentials file...")
    
    try:
        with open("config/credentials.json", "r") as f:
            creds = json.load(f)
        
        required_fields = [
            "type", "project_id", "private_key", "client_email"
        ]
        
        for field in required_fields:
            if field not in creds:
                print(f"✗ Missing required field: {field}")
                return False
        
        if creds.get("type") != "service_account":
            print("✗ Invalid credential type. Expected 'service_account'")
            return False
        
        print("✓ Credentials file format is valid")
        return True
        
    except json.JSONDecodeError:
        print("✗ Invalid JSON format in credentials file")
        return False
    except FileNotFoundError:
        print("✗ Credentials file not found")
        return False

def test_connection():
    """Test connection to Google Sheets."""
    print("\nTesting Google Sheets connection...")
    
    try:
        from sheets.manager import SheetsManager
        from config.settings import load_config
        
        config = load_config()
        
        manager = SheetsManager(
            credentials_file=config["credentials_file"],
            spreadsheet_name=config["spreadsheet_name"],
            worksheet_name=config["worksheet_name"]
        )
        
        if manager.connect():
            print("✓ Successfully connected to Google Sheets!")
            
            # Try to get data
            items = manager.get_all_items()
            print(f"✓ Found {len(items)} items in the spreadsheet")
            
            return True
        else:
            print("✗ Failed to connect to Google Sheets")
            return False
            
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False

def main():
    """Main setup verification function."""
    print("Inventory Management System - Setup Verification")
    print("=" * 50)
    
    success = True
    
    # Check requirements
    if not check_requirements():
        success = False
    
    # Check config files
    if not check_config():
        success = False
    
    # Validate credentials if file exists
    if Path("config/credentials.json").exists():
        if not validate_credentials():
            success = False
    
    # Test connection if everything looks good so far
    if success:
        if not test_connection():
            success = False
    
    print("\n" + "=" * 50)
    
    if success:
        print("✓ Setup verification completed successfully!")
        print("You can now run the application with: python main.py")
    else:
        print("✗ Setup verification failed!")
        print("Please fix the issues above before running the application.")
        
        print("\nSetup steps:")
        print("1. Install packages: pip install -r requirements.txt")
        print("2. Get Google Sheets API credentials and save as config/credentials.json")
        print("3. Update config/config.json with your spreadsheet name")
        print("4. Share your spreadsheet with the service account email")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)