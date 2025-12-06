# إصلاح التصنيف عند التعديل

## المشكلة
عند تعديل معاملة حديثة، كان النظام لا يحافظ على التصنيف الأصلي للعنصر في المعاملة الجديدة المُحدثة.

## الحل المطبق

### 1. تحديث دالة record_transaction في excel_manager.py
- إضافة معامل اختياري `category` للسماح بتمرير التصنيف
- استخدام التصنيف المُمرر كمعامل أو الرجوع للتصنيف من معلومات العنصر

```python
def record_transaction(self, project_name, item_name, quantity, operation_type, notes="", custom_date=None, reference_id=None, category=None):
    # استخدام التصنيف الممرر كمعامل أو التصنيف من معلومات العنصر
    item_category = category if category is not None else item_info.get('التصنيف', 'غير محدد')
```

### 2. تحديث دالة add_corrected_individual_transaction
- تمرير التصنيف الأصلي من المعاملة عند إنشاء المعاملة الجديدة

```python
excel_manager.record_transaction(
    self.project_name,
    original_transaction['اسم_العنصر'],
    new_quantity,
    original_transaction['نوع_العملية'],
    f'معاملة محدثة - {self.reason_combo.currentText()} (من {original_transaction["الكمية"]} إلى {new_quantity})',
    reference_id=reference_id,
    category=original_transaction['التصنيف']  # إضافة التصنيف الأصلي
)
```

### 3. تحديث دالة cancel_individual_transaction
- تمرير التصنيف الأصلي عند إنشاء المعاملة العكسية للإلغاء

```python
excel_manager.record_transaction(
    self.project_name,
    original_transaction['اسم_العنصر'],
    original_transaction['الكمية'],
    cancel_operation,
    f'إلغاء معاملة رقم {reference_id} - {self.reason_combo.currentText()}',
    reference_id=reference_id,
    category=original_transaction['التصنيف']  # إضافة التصنيف الأصلي
)
```

## النتيجة
- عند تعديل معاملة، تحتفظ المعاملة الجديدة بنفس التصنيف الأصلي
- يظهر التصنيف بشكل صحيح في جدول المعاملات الحديثة
- تحافظ المعاملات العكسية أيضاً على التصنيف الأصلي للدقة

## التوافق
- الدالة المحدثة متوافقة مع الاستدعاءات الحالية (المعامل الجديد اختياري)
- دالة `add_transaction` الموجودة تحافظ بالفعل على التصنيف بشكل صحيح
- لا تحتاج أي ملفات أخرى لتعديل

## ملاحظات
- تم التحقق من جميع استدعاءات `record_transaction` في النظام
- جميع التعديلات متوافقة مع النظام الحالي
- الإصلاح يعمل للمعاملات الجديدة والمعاملات الموجودة