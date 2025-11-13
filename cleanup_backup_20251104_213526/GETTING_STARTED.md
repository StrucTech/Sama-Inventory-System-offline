# Getting Started with Inventory Management System

## Quick Setup Guide

Your Python inventory management application is ready! Follow these steps to get started:

### 1. Google Sheets API Setup (Required)

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Create a new project** or select an existing one
3. **Enable the Google Sheets API**:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Sheets API"
   - Click "Enable"
4. **Create a service account**:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "Service Account"
   - Fill in the service account details
   - Click "Create and Continue"
   - Skip granting users access (click "Done")
5. **Generate credentials**:
   - Click on your service account email
   - Go to "Keys" tab
   - Click "Add Key" > "Create new key"
   - Choose "JSON" format
   - Download the file

### 2. Install Credentials

1. **Copy the downloaded JSON file** to `config/credentials.json`
2. **Note the service account email** from the JSON file (it looks like: `your-service@project-id.iam.gserviceaccount.com`)

### 3. Set Up Google Sheets

1. **Create a new Google Sheets document** or use an existing one
2. **Share the document** with the service account email:
   - Click "Share" in your Google Sheets
   - Add the service account email
   - Give it "Editor" permissions
3. **Note your spreadsheet name** (you'll need this for configuration)

### 4. Configure the Application

1. **Edit `config/config.json`**:
   ```json
   {
       "spreadsheet_name": "Your Actual Spreadsheet Name Here",
       "worksheet_name": "Inventory"
   }
   ```

### 5. Verify Setup

Run the setup verification script:
```bash
python setup_check.py
```

This will check if everything is configured correctly.

### 6. Run the Application

```bash
python main.py
```

## What the Application Does

- **View Inventory**: Shows all items in a table format
- **Add Items**: Add new inventory items with name, quantity, and price
- **Edit Quantities**: Update quantities of existing items
- **Remove Items**: Delete items from inventory
- **Auto-sync**: All changes sync with your Google Sheets in real-time

## Troubleshooting

**"Connection failed"**: 
- Check your internet connection
- Verify credentials.json is valid
- Make sure the spreadsheet is shared with the service account

**"ModuleNotFoundError"**:
- Run: `pip install -r requirements.txt`

**"Spreadsheet not found"**:
- Check the spreadsheet name in config/config.json
- Make sure it's shared with the service account

## Need Help?

1. Run `python setup_check.py` to diagnose issues
2. Check the README.md for detailed documentation
3. Verify your Google Sheets API setup

---

**Ready to start managing your inventory!** 🎉