# 🔧 دليل التطوير - نظام إدارة المخزون

## 🏗️ **البنية التقنية**

### **معمارية المشروع:**
```
📦 نظام إدارة المخزون
├── 🎨 Presentation Layer (GUI)
│   ├── main_window.py      - النافذة الرئيسية
│   ├── inventory_view.py   - عرض المخزون
│   └── *_dialog.py         - النوافذ المنبثقة
├── 🔧 Business Layer (Logic)
│   ├── sheets/manager.py   - منطق الأعمال
│   └── config/settings.py  - إدارة الإعدادات
└── 💾 Data Layer (Google Sheets)
    ├── Inventory Sheet     - بيانات المخزون
    └── Activity Log Sheet  - سجل الأنشطة
```

---

## 📊 **نموذج البيانات**

### **جدول المخزون الرئيسي:**
```sql
CREATE TABLE Inventory (
    item_name VARCHAR(255) PRIMARY KEY,
    quantity INTEGER NOT NULL,
    last_updated DATETIME NOT NULL
);
```

### **جدول سجل الأنشطة:**
```sql
CREATE TABLE ActivityLog (
    timestamp DATETIME NOT NULL,
    operation VARCHAR(50) NOT NULL,
    item_name VARCHAR(255) NOT NULL,
    quantity_change INTEGER,
    new_quantity INTEGER,
    recipient VARCHAR(255),
    details TEXT
);
```

---

## 🔌 **واجهات برمجة التطبيقات**

### **SheetsManager Class:**
```python
class SheetsManager:
    def connect() -> bool
    def get_all_items() -> List[Dict]
    def add_item(name: str, quantity: int) -> bool
    def update_quantity(name: str, new_quantity: int) -> bool
    def outbound_item(name: str, quantity: int, recipient: str) -> bool
    def remove_item(name: str) -> bool
    def get_activity_log() -> List[Dict]
```

### **Dialog Classes:**
```python
class AddItemDialog:
    def __init__(parent)
    def show() -> Optional[Tuple[str, int]]

class EditQuantityDialog:
    def __init__(parent, item: Dict)
    def show() -> Optional[int]

class OutboundDialog:
    def __init__(parent, item: Dict)
    def show() -> Optional[Tuple[int, str]]
```

---

## 🎨 **نظام التعريب**

### **هيكل الترجمة:**
```python
# localization/arabic.py
ARABIC_STRINGS = {
    "key": "القيمة العربية",
    "formatted_key": "نص مع متغير: {}",
    # ... المزيد
}

def get_text(key: str, *args) -> str:
    """استرجاع النص المترجم مع التنسيق"""
    text = ARABIC_STRINGS.get(key, key)
    return text.format(*args) if args else text
```

### **استخدام النظام:**
```python
# في أي ملف GUI
from localization import get_text

# نص بسيط
title = get_text("app_title")

# نص مع متغيرات
message = get_text("loaded_items", count)
```

---

## 🔄 **إدارة العمليات اللاتزامنية**

### **نمط Threading:**
```python
def perform_background_operation(self, operation_func, *args):
    """تنفيذ عملية في الخلفية"""
    def worker():
        try:
            # تحديث واجهة المستخدم
            self.root.after(0, lambda: self.show_loading())
            
            # تنفيذ العملية
            result = operation_func(*args)
            
            # تحديث الواجهة بالنتيجة
            self.root.after(0, lambda: self.handle_success(result))
        except Exception as e:
            # معالجة الأخطاء
            self.root.after(0, lambda: self.handle_error(e))
    
    thread = threading.Thread(target=worker)
    thread.daemon = True
    thread.start()
```

---

## 🛡️ **نظام معالجة الأخطاء**

### **مستويات الأخطاء:**
```python
# أخطاء الاتصال
class ConnectionError(Exception):
    """خطأ في الاتصال بـ Google Sheets"""

# أخطاء البيانات
class DataValidationError(Exception):
    """خطأ في صحة البيانات"""

# أخطاء العمليات
class OperationError(Exception):
    """خطأ في تنفيذ العملية"""
```

### **معالجة موحدة:**
```python
def handle_error(self, error: Exception):
    """معالجة موحدة للأخطاء"""
    if isinstance(error, ConnectionError):
        self.show_connection_error(error)
    elif isinstance(error, DataValidationError):
        self.show_validation_error(error)
    else:
        self.show_general_error(error)
```

---

## 📝 **إضافة ميزات جديدة**

### **1. إضافة dialog جديد:**
```python
# gui/new_dialog.py
class NewDialog:
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.result = None
        
    def show(self):
        self.dialog = tk.Toplevel(self.parent)
        self.setup_ui()
        self.dialog.wait_window()
        return self.result
        
    def setup_ui(self):
        # إعداد الواجهة
        pass
```

### **2. إضافة عملية جديدة:**
```python
# sheets/manager.py
def new_operation(self, param1, param2):
    """عملية جديدة"""
    try:
        # تنفيذ العملية
        result = self.worksheet.update_cells(...)
        
        # تسجيل النشاط
        self._log_activity("NEW_OPERATION", param1, details=param2)
        
        return True
    except Exception as e:
        raise OperationError(f"فشل في العملية الجديدة: {e}")
```

### **3. إضافة نصوص جديدة:**
```python
# localization/arabic.py
ARABIC_STRINGS.update({
    "new_feature": "الميزة الجديدة",
    "new_button": "زر جديد",
    "new_dialog_title": "عنوان النافذة الجديدة"
})
```

---

## 🧪 **الاختبار والتجريب**

### **اختبارات الوحدة:**
```python
# tests/test_sheets_manager.py
import unittest
from sheets.manager import SheetsManager

class TestSheetsManager(unittest.TestCase):
    def setUp(self):
        self.manager = SheetsManager(test_mode=True)
        
    def test_add_item(self):
        result = self.manager.add_item("اختبار", 10)
        self.assertTrue(result)
        
    def test_invalid_quantity(self):
        with self.assertRaises(DataValidationError):
            self.manager.add_item("اختبار", -5)
```

### **اختبار الواجهة:**
```python
# tests/test_gui.py
import tkinter as tk
from gui.main_window import MainWindow

def test_main_window():
    root = tk.Tk()
    app = MainWindow(root, test_config)
    
    # اختبار إنشاء الواجهة
    assert app.inventory_view is not None
    assert len(app.root.winfo_children()) > 0
    
    root.destroy()
```

---

## 📚 **أفضل الممارسات**

### **كتابة الكود:**
```python
# ✅ جيد
def add_item(self, name: str, quantity: int) -> bool:
    """
    إضافة عنصر جديد للمخزون.
    
    Args:
        name: اسم العنصر
        quantity: الكمية الأولية
        
    Returns:
        True إذا نجحت العملية، False إذا فشلت
        
    Raises:
        DataValidationError: إذا كانت البيانات غير صحيحة
    """
    if not name or quantity < 0:
        raise DataValidationError("بيانات غير صحيحة")
    
    # باقي الكود...
```

### **إدارة الموارد:**
```python
# ✅ استخدام context managers
with self.lock:
    # عمليات حساسة
    pass

# ✅ تنظيف الموارد
try:
    # عمليات
    pass
finally:
    # تنظيف
    pass
```

### **التعامل مع الواجهة:**
```python
# ✅ استخدام after() للعمليات اللاتزامنية
self.root.after(0, lambda: self.update_ui(data))

# ✅ تجميد الأزرار أثناء المعالجة
self.button.config(state="disabled")
# ... معالجة ...
self.button.config(state="normal")
```

---

## 🚀 **نشر التطبيق**

### **إنشاء ملف تنفيذي:**
```bash
# تثبيت PyInstaller
pip install pyinstaller

# إنشاء ملف exe
pyinstaller --onefile --windowed --name="نظام المخزون" main_arabic.py
```

### **إعداد التثبيت:**
```bash
# استخدام cx_Freeze
pip install cx_Freeze

# إنشاء setup.py
python setup.py build
```

---

## 📈 **مقاييس الأداء**

### **معايير القياس:**
- ⏱️ **وقت بدء التطبيق**: < 3 ثواني
- 🔄 **وقت تحديث البيانات**: < 5 ثواني
- 💾 **استهلاك الذاكرة**: < 100 ميجابايت
- 🌐 **timeout الشبكة**: 30 ثانية

### **تحسين الأداء:**
```python
# تخزين مؤقت للبيانات
@lru_cache(maxsize=100)
def get_cached_data(self, key):
    return self.expensive_operation(key)

# تحميل تدريجي
def load_data_incrementally(self):
    for chunk in data_chunks:
        self.process_chunk(chunk)
        self.root.update()  # تحديث الواجهة
```

---

*🔧 دليل شامل لتطوير وصيانة النظام!*