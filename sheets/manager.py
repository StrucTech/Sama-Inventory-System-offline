"""
Google Sheets integration for the Inventory Management System.
Handles all interactions with Google Sheets API using gspread.
"""

import gspread
from google.auth.exceptions import DefaultCredentialsError
from typing import List, Dict, Optional, Any
import datetime
import os

class SheetsManager:
    """Manages connections and operations with Google Sheets."""
    
    def __init__(self, credentials_file: str, spreadsheet_name: str, worksheet_name: str = "Inventory"):
        """
        Initialize the SheetsManager.
        
        Args:
            credentials_file: Path to Google Sheets API credentials JSON file
            spreadsheet_name: Name of the Google Sheets spreadsheet
            worksheet_name: Name of the worksheet within the spreadsheet
        """
        self.credentials_file = credentials_file
        self.spreadsheet_name = spreadsheet_name
        self.worksheet_name = worksheet_name
        self.activity_log_name = "Activity_Log"
        self.client = None
        self.spreadsheet = None
        self.worksheet = None
        self.current_user = ""  # المستخدم الحالي
        self.activity_log = None
        
    def set_current_user(self, username: str):
        """Set the current user for activity logging."""
        self.current_user = username
        
    def connect(self) -> bool:
        """
        Establish connection to Google Sheets.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            if not os.path.exists(self.credentials_file):
                raise FileNotFoundError(f"Credentials file not found: {self.credentials_file}")
                
            # Authenticate and create client
            self.client = gspread.service_account(filename=self.credentials_file)
            
            # Open the spreadsheet
            try:
                self.spreadsheet = self.client.open(self.spreadsheet_name)
            except gspread.SpreadsheetNotFound:
                # Create new spreadsheet if it doesn't exist
                self.spreadsheet = self.client.create(self.spreadsheet_name)
                
            # Get or create the worksheet
            try:
                self.worksheet = self.spreadsheet.worksheet(self.worksheet_name)
            except gspread.WorksheetNotFound:
                self.worksheet = self.spreadsheet.add_worksheet(
                    title=self.worksheet_name, 
                    rows=1000, 
                    cols=10
                )
                # Add headers
                self._setup_headers()
                
            # Get or create the activity log worksheet
            try:
                self.activity_log = self.spreadsheet.worksheet(self.activity_log_name)
            except gspread.WorksheetNotFound:
                self.activity_log = self.spreadsheet.add_worksheet(
                    title=self.activity_log_name, 
                    rows=1000, 
                    cols=6
                )
                # Add activity log headers
                self._setup_activity_log_headers()
                
            return True
            
        except (DefaultCredentialsError, FileNotFoundError, Exception) as e:
            print(f"Error connecting to Google Sheets: {e}")
            return False
            
    def _setup_headers(self):
        """Set up the initial headers for the inventory worksheet."""
        headers = ["اسم العنصر", "التصنيف", "الكمية المتاحة", "رقم المشروع", "آخر تحديث"]
        self.worksheet.update("A1:E1", [headers])
        
    def _setup_activity_log_headers(self):
        """Set up the headers for the activity log worksheet."""
        headers = ["التاريخ والوقت", "نوع العملية", "اسم العنصر", "الكمية", "اسم المستلم", "التفاصيل"]
        self.activity_log.update("A1:F1", [headers])
        
    def _log_activity(self, operation_type: str, item_name: str, quantity: str, recipient_name: str = "", details: str = "", category: str = "", current_user: str = ""):
        """
        Log an activity to the new enhanced activity log worksheet.
        
        Args:
            operation_type: Type of operation (إضافة/تعديل/إخراج/حذف)
            item_name: Name of the item
            quantity: Quantity involved in the operation
            recipient_name: Name of the person receiving items (for outbound operations)
            details: Additional details of the operation
            category: Category of the item (optional)
            current_user: Current user performing the operation
        """
        try:
            # استخدام SheetsManager للكتابة في الشيت الجديد
            # Using current manager instance
            enhanced_manager = self
            
            if enhanced_manager.connect():
                # تحديد الكميات حسب نوع العملية
                quantity_added = 0
                quantity_removed = 0
                previous_quantity = 0
                current_quantity = 0
                
                try:
                    quantity_float = float(quantity) if quantity else 0
                    if operation_type == "إضافة":
                        quantity_added = quantity_float
                        current_quantity = quantity_float
                    elif operation_type == "إخراج":
                        quantity_removed = quantity_float
                    elif operation_type == "تحديث":
                        # استخراج الكميات من التفاصيل إذا أمكن
                        if "من" in details and "إلى" in details:
                            import re
                            numbers = re.findall(r'\d+(?:\.\d+)?', details)
                            if len(numbers) >= 2:
                                previous_quantity = float(numbers[0])
                                current_quantity = float(numbers[1])
                                if current_quantity > previous_quantity:
                                    quantity_added = current_quantity - previous_quantity
                                else:
                                    quantity_removed = previous_quantity - current_quantity
                except (ValueError, AttributeError):
                    pass
                
                # إضافة السجل للشيت الجديد
                # استخدام current_user إذا كان متاحاً، وإلا recipient_name
                user_to_log = current_user if current_user else recipient_name
                
                enhanced_manager.add_activity_log_entry_new(
                    operation_type=operation_type,
                    item_name=item_name,
                    quantity_added=quantity_added,
                    quantity_removed=quantity_removed,
                    previous_quantity=previous_quantity,
                    current_quantity=current_quantity,
                    recipient_name=user_to_log,
                    details=details,
                    category=category
                )
            
        except Exception as e:
            print(f"Error logging activity: {e}")
        
    def get_all_items(self) -> List[Dict[str, Any]]:
        """
        Get all inventory items from the spreadsheet.
        
        Returns:
            List of dictionaries containing item data
        """
        try:
            if not self.worksheet:
                return []
                
            # Get all records (excluding header row)
            records = self.worksheet.get_all_records()
            
            # Convert to our format
            items = []
            for i, record in enumerate(records, start=2):  # Start at row 2
                if record.get("اسم العنصر"):  # Only include rows with item names
                    item = {
                        "row": i,
                        "item_name": record.get("اسم العنصر", ""),
                        "category": record.get("التصنيف", ""),
                        "quantity": self._parse_number(record.get("الكمية المتاحة", 0)),
                        "project_id": record.get("رقم المشروع", ""),
                        "last_updated": record.get("آخر تحديث", "")
                    }
                    items.append(item)
                    
            return items
            
        except Exception as e:
            print(f"Error getting items: {e}")
            return []
            
    def get_items_by_project(self, project_id: str) -> List[Dict[str, Any]]:
        """
        Get inventory items for a specific project.
        
        Args:
            project_id: Project ID to filter by
            
        Returns:
            List of dictionaries containing item data for the project
        """
        try:
            all_items = self.get_all_items()
            
            # Filter items by project ID
            project_items = []
            for item in all_items:
                if item.get("project_id", "") == project_id:
                    project_items.append(item)
            
            return project_items
            
        except Exception as e:
            print(f"Error getting items by project: {e}")
            return []
            
    def add_item(self, item_name: str, category: str, quantity: int, project_id: str = "") -> bool:
        """
        Add a new item to the inventory or update existing quantity.
        If the same item exists in the same project, quantities will be combined.
        
        Args:
            item_name: Name of the item
            category: Category of the item
            quantity: Quantity in stock
            project_id: Project ID this item belongs to
            
        Returns:
            True if successful, False otherwise
            
        Raises:
            ValueError: If input parameters are invalid
        """
        # Validate input parameters
        if not item_name or not isinstance(item_name, str) or len(item_name.strip()) == 0:
            raise ValueError("Item name cannot be empty or None")
        
        if not category or not isinstance(category, str) or len(category.strip()) == 0:
            raise ValueError("Category cannot be empty or None")
        
        if not isinstance(quantity, (int, float)) or quantity < 0:
            raise ValueError("Quantity must be a non-negative number")
            
        try:
            if not self.worksheet:
                return False
                
            # Get all current data
            all_data = self.worksheet.get_all_values()
            if not all_data:
                return False
            
            # Clean the inputs
            item_name = item_name.strip()
            category = category.strip()
            project_id = project_id.strip()
            
            # Search for existing item with same name and project
            existing_row = None
            for i, row in enumerate(all_data[1:], start=2):  # Skip header row
                if len(row) >= 4:  # Ensure we have enough columns
                    row_item = row[0].strip() if row[0] else ""
                    row_project = row[3].strip() if len(row) > 3 and row[3] else ""
                    
                    # Check if same item and same project
                    if row_item.lower() == item_name.lower() and row_project == project_id:
                        existing_row = i
                        break
            
            last_updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if existing_row:
                # Update existing item - combine quantities
                current_quantity = 0
                try:
                    current_quantity = float(all_data[existing_row - 1][2]) if all_data[existing_row - 1][2] else 0
                except (ValueError, IndexError):
                    current_quantity = 0
                
                new_quantity = current_quantity + quantity
                
                # Update the existing row
                row_data = [item_name, category, new_quantity, project_id, last_updated]
                self.worksheet.update(f"A{existing_row}:E{existing_row}", [row_data])
                
                # Log the activity
                details = f"تحديث كمية العنصر من {current_quantity} إلى {new_quantity} (إضافة {quantity})"
                if project_id:
                    details += f" للمشروع {project_id}"
                self._log_activity("تحديث", item_name, str(new_quantity), str(current_quantity), details, category, self.current_user)
                
                print(f"✅ تم تحديث العنصر '{item_name}': الكمية الجديدة {new_quantity} (أضيف {quantity})")
                
            else:
                # Add new item
                next_row = len(all_data) + 1
                row_data = [item_name, category, quantity, project_id, last_updated]
                self.worksheet.update(f"A{next_row}:E{next_row}", [row_data])
                
                # Log the activity
                details = f"إضافة عنصر جديد بكمية {quantity}"
                if project_id:
                    details += f" للمشروع {project_id}"
                self._log_activity("إضافة", item_name, str(quantity), "", details, category, self.current_user)
                
                print(f"✅ تم إضافة عنصر جديد '{item_name}' بكمية {quantity}")
            
            return True
            
        except ValueError:
            # Re-raise validation errors
            raise
        except Exception as e:
            print(f"❌ خطأ في إضافة/تحديث العنصر: {e}")
            return False
            
    def update_quantity(self, row: int, new_quantity) -> bool:
        """
        Update the quantity of an item.
        
        Args:
            row: Row number of the item in the spreadsheet
            new_quantity: New quantity value (int or float)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.worksheet:
                return False
                
            last_updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Get item name, category and old quantity for logging
            item_name = self.worksheet.cell(row, 1).value
            category = self.worksheet.cell(row, 2).value or "متنوع"
            old_quantity = self._parse_number(self.worksheet.cell(row, 3).value)
            
            # Update quantity and last updated (quantity now in column C, date in column E)
            # تحديث الكمية والتاريخ
            print(f"DEBUG: تحديث الكمية في الشيت - الصف {row}: {old_quantity} -> {new_quantity}")
            self.worksheet.update(f"C{row}", [[float(new_quantity)]])
            self.worksheet.update(f"E{row}", [[last_updated]])
            
            # Log the activity
            details = f"تعديل الكمية من {old_quantity} إلى {new_quantity}"
            self._log_activity("تعديل", item_name, str(float(new_quantity)), "", details, category, self.current_user)
            
            return True
            
        except Exception as e:
            print(f"Error updating quantity: {e}")
            return False
            
    def outbound_item(self, row: int, outbound_quantity: int, recipient_name: str) -> bool:
        """
        Process outbound items (إخراج بضاعة).
        
        Args:
            row: Row number of the item in the spreadsheet
            outbound_quantity: Quantity to be taken out
            recipient_name: Name of the person receiving the items
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.worksheet:
                return False
                
            # Get current item details
            item_name = self.worksheet.cell(row, 1).value
            category = self.worksheet.cell(row, 2).value or "متنوع"
            current_quantity = self._parse_number(self.worksheet.cell(row, 3).value)
            
            # Check if there's enough quantity
            if current_quantity < outbound_quantity:
                return False  # Not enough quantity
                
            # Calculate new quantity
            new_quantity = current_quantity - outbound_quantity
            last_updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Update quantity and last updated
            updates = [
                {"range": f"C{row}", "values": [[new_quantity]]},
                {"range": f"E{row}", "values": [[last_updated]]}
            ]
            
            self.worksheet.batch_update(updates)
            
            # Log the activity
            details = f"إخراج بضاعة - الكمية المخرجة: {outbound_quantity}, الكمية المتبقية: {new_quantity}"
            self._log_activity("إخراج", item_name, str(outbound_quantity), recipient_name, details, category, self.current_user)
            
            return True
            
        except Exception as e:
            print(f"Error processing outbound: {e}")
            return False
            
    def remove_item(self, row: int) -> bool:
        """
        Remove an item from the inventory.
        
        Args:
            row: Row number of the item to remove
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.worksheet:
                return False
                
            # Get item details for logging before deletion
            item_name = self.worksheet.cell(row, 1).value
            category = self.worksheet.cell(row, 2).value or "متنوع"
            quantity = self.worksheet.cell(row, 3).value  # الكمية في العمود الثالث
            
            # Log the activity before deletion
            details = f"حذف العنصر - الكمية كانت: {quantity}"
            self._log_activity("حذف", item_name, str(quantity), "", details, category, self.current_user)
                
            self.worksheet.delete_rows(row)
            return True
            
        except Exception as e:
            print(f"Error removing item: {e}")
            return False
            
    def _parse_number(self, value: Any) -> float:
        """
        Parse a value as a number, returning 0 if not possible.
        
        Args:
            value: Value to parse
            
        Returns:
            Parsed number or 0
        """
        try:
            if isinstance(value, (int, float)):
                return float(value)
            if isinstance(value, str):
                # Remove currency symbols and commas
                cleaned = value.replace("$", "").replace(",", "").strip()
                return float(cleaned) if cleaned else 0
            return 0
        except (ValueError, TypeError):
            return 0
    
    def get_activity_log(self) -> List[List[str]]:
        """
        Get all activity log entries.
        
        Returns:
            List of activity log entries
        """
        try:
            if not self.activity_log:
                return []
                
            # Get all values from activity log
            all_values = self.activity_log.get_all_values()
            
            # Return all rows except header
            return all_values[1:] if len(all_values) > 1 else []
            
        except Exception as e:
            print(f"Error getting activity log: {e}")
            return []
    
    def get_all_items_raw(self) -> List[List[str]]:
        """
        Get all items as raw list data (for reports).
        
        Returns:
            List of lists containing item data
        """
        try:
            if not self.worksheet:
                return []
                
            # Get all values from worksheet
            all_values = self.worksheet.get_all_values()
            
            # Return all rows except header
            return all_values[1:] if len(all_values) > 1 else []
            
        except Exception as e:
            print(f"Error getting raw items: {e}")
            return []