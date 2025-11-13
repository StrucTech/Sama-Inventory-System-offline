# Sama Inventory Management System 📦

نظام إدارة المخزون المتقدم - تطبيق سطح مكتب مطور بـ Python يتصل مع Google Sheets لتخزين ومزامنة البيانات.

[![GitHub release](https://img.shields.io/github/release/StrucTech/Sama-Inventory-System.svg)](https://github.com/StrucTech/Sama-Inventory-System/releases)
[![GitHub downloads](https://img.shields.io/github/downloads/StrucTech/Sama-Inventory-System/total.svg)](https://github.com/StrucTech/Sama-Inventory-System/releases)
[![Build Status](https://github.com/StrucTech/Sama-Inventory-System/workflows/Build%20and%20Release%20Sama%20Inventory%20System/badge.svg)](https://github.com/StrucTech/Sama-Inventory-System/actions)

A Python desktop application for managing inventory that connects to Google Sheets for data storage and synchronization.

## Features

- **View Inventory**: Display all inventory items in a clean table format
- **Add Items**: Add new items with name, category, and quantity ✨
- **Item Categories**: Organize items by categories for better management ✨
- **Edit Quantities**: Update the quantity of existing items
- **Remove Items**: Delete items from the inventory
- **User Management**: Multi-user system with role-based access control ✨
- **Project Management**: Assign items to specific projects ✨
- **Real-time Sync**: All changes are synchronized with Google Sheets
- **Activity Logging**: Track all inventory changes with detailed logs ✨

## Requirements

- Python 3.7 or higher
- Google Sheets API credentials
- Internet connection for Google Sheets synchronization

## 📥 التحميل والاستخدام السريع

### للمستخدمين العاديين (نسخة مستقلة)

1. **تحميل النسخة المستقلة:**
   - اذهب إلى [صفحة الإصدارات](https://github.com/StrucTech/Sama-Inventory-System/releases)
   - حمل أحدث إصدار `Sama-Inventory-System-vX.X.X.zip`
   - استخرج المحتويات

2. **تشغيل البرنامج:**
   - شغل `نظام إدارة المخزون.exe`
   - اتبع معالج الإعداد الأولي
   - **لا حاجة لتثبيت Python أو أي متطلبات إضافية!**

### للمطورين (من الكود المصدري)

## Installation

1. **Clone or download this repository**
   ```bash
   git clone https://github.com/StrucTech/Sama-Inventory-System.git
   cd Sama-Inventory-System
   ```

2. **Install required Python packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google Sheets API credentials:**
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Google Sheets API
   - Create a service account and download the JSON credentials file
   - Place the credentials file at `config/credentials.json`
   - Share your Google Sheets document with the service account email

4. **Configure the application:**
   - Edit `config/config.json` to match your Google Sheets document name
   - Ensure the worksheet name matches your setup

## Usage

1. **Run the application:**
   ```bash
   python main.py
   ```

2. **Using the interface:**
   - **Refresh**: Reload data from Google Sheets
   - **Add Item**: Click to add a new inventory item
   - **Edit Quantity**: Select an item and click to edit its quantity
   - **Remove Item**: Select an item and click to remove it
   - **Settings**: Access configuration options

## Google Sheets Setup

Your Google Sheets document should have the following columns:
- **A**: Item Name
- **B**: Quantity
- **C**: Unit Price
- **D**: Total Value (calculated automatically)
- **E**: Last Updated (updated automatically)

The application will create the headers automatically if they don't exist.

## Configuration

Edit `config/config.json` to customize:

```json
{
    "credentials_file": "config/credentials.json",
    "spreadsheet_name": "Your Spreadsheet Name",
    "worksheet_name": "Your Worksheet Name",
    "window": {
        "width": 800,
        "height": 600
    }
}
```

## File Structure

```
inventory-system/
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── config/
│   ├── __init__.py
│   ├── settings.py           # Configuration management
│   ├── config.json           # Application settings
│   └── credentials.json      # Google Sheets API credentials (you create this)
├── gui/
│   ├── __init__.py
│   ├── main_window.py        # Main application window
│   ├── inventory_view.py     # Inventory table display (with categories) ✨
│   ├── add_item_dialog.py    # Add item dialog (with category field) ✨
│   ├── edit_quantity_dialog.py # Edit quantity dialog
│   ├── login_window.py       # User login interface ✨
│   ├── register_window.py    # User registration ✨
│   ├── admin_projects_window.py # Project management ✨
│   └── outbound_dialog.py    # Item outbound processing ✨
├── sheets/
│   ├── __init__.py
│   └── manager.py            # Google Sheets integration
└── .github/
    └── copilot-instructions.md
```

## Troubleshooting

**Connection Issues:**
- Verify your `credentials.json` file is valid and in the correct location
- Ensure the service account has access to your Google Sheets document
- Check your internet connection

**Import Errors:**
- Make sure all required packages are installed: `pip install -r requirements.txt`
- Verify you're using Python 3.7 or higher

**Permission Errors:**
- Share your Google Sheets document with the service account email address
- Grant "Editor" permissions to the service account

## 🛠️ البناء والتطوير

### بناء النسخة المستقلة

```bash
# تثبيت متطلبات البناء
pip install -r requirements_build.txt

# بناء النسخة المستقلة
python build_setup.py
# أو استخدم
build.bat
```

### إنشاء إصدار جديد

```bash
# إنشاء إصدار جديد تلقائياً
create_release.bat

# أو يدوياً
git tag v1.0.0
git push origin v1.0.0
```

### نظام التحديث التلقائي

- البرنامج يتحقق من التحديثات تلقائياً
- التحديثات تُحمل من [GitHub Releases](https://github.com/StrucTech/Sama-Inventory-System/releases)
- نسخة احتياطية تلقائية قبل كل تحديث

## 🤝 المساهمة

نرحب بالمساهمات! يرجى:

1. Fork المشروع
2. إنشاء branch للميزة الجديدة (`git checkout -b feature/AmazingFeature`)
3. Commit التغييرات (`git commit -m 'Add some AmazingFeature'`)
4. Push للـ branch (`git push origin feature/AmazingFeature`)
5. فتح Pull Request

## 📧 التواصل

- **مشروع**: [Sama Inventory System](https://github.com/StrucTech/Sama-Inventory-System)
- **Issues**: [تقرير مشكلة](https://github.com/StrucTech/Sama-Inventory-System/issues)
- **Releases**: [التحميلات](https://github.com/StrucTech/Sama-Inventory-System/releases)

## 📜 License

This project is open source and available under the MIT License.

---

<div align="center">
  <b>🚀 Developed by StrucTech Solutions</b><br>
  <i>نحو حلول تقنية متقدمة</i>
</div>