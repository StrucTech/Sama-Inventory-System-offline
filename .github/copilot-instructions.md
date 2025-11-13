# Inventory Management System - Copilot Instructions

This is a Python desktop application for inventory management that connects to Google Sheets.

## Project Structure
- Main application entry point: `main.py`
- GUI components: `gui/`
- Google Sheets integration: `sheets/`
- Configuration: `config/`
- Requirements: `requirements.txt`

## Technologies Used
- **GUI Framework**: tkinter (built-in Python library)
- **Google Sheets API**: gspread library
- **Authentication**: google-auth library
- **Configuration**: JSON for settings

## Features
- View inventory items from Google Sheets
- Add new items to inventory
- Edit item quantities
- Remove items from inventory
- Real-time synchronization with Google Sheets

## Setup Requirements
1. Google Sheets API credentials (service account JSON file)
2. Python 3.7+ with required packages
3. Google Sheets document set up for inventory data

## Progress Tracking
- [x] Project structure created
- [x] Main application files implemented  
- [x] GUI components created (main window, inventory view, dialogs)
- [x] Google Sheets integration implemented
- [x] Configuration setup and management
- [x] Python packages installed (gspread, google-auth, etc.)
- [x] Setup verification script created
- [x] Documentation completed (README, Getting Started guide)

## Next Steps for Users
1. Set up Google Sheets API credentials
2. Create and share a Google Sheets document
3. Run `python setup_check.py` to verify setup
4. Launch the application with `python main.py`