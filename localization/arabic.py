"""
Arabic language strings for the Inventory Management System
"""

ARABIC_STRINGS = {
    # Main Window
    "app_title": "نظام إدارة المخزون",
    "connecting": "جاري الاتصال بجداول جوجل...",
    "connected": "متصل بجداول جوجل",
    "connection_failed": "فشل الاتصال",
    "loading_data": "جاري تحميل البيانات...",
    "loaded_items": "تم تحميل {} عنصر",
    "failed_to_load": "فشل في تحميل البيانات",
    
    # Buttons
    "refresh": "تحديث",
    "add_item": "إضافة عنصر",
    "edit_quantity": "تعديل الكمية",
    "outbound_item": "إخراج بضاعة",
    "remove_item": "حذف العنصر",
    "cancel": "إلغاء",
    "add": "إضافة",
    "update": "تحديث",
    "outbound": "إخراج",
    "yes": "نعم",
    "no": "لا",
    
    # Table Headers
    "item_name": "اسم العنصر",
    "quantity": "الكمية المتاحة",
    "last_updated": "آخر تحديث",
    
    # Add Item Dialog
    "add_new_item": "إضافة عنصر جديد",
    "add_new_inventory_item": "إضافة عنصر جديد للمخزون",
    "item_name_label": "اسم العنصر:",
    "quantity_label": "الكمية:",
    "preview": "معاينة",
    "quantity_preview": "الكمية: {}",
    
    # Edit Quantity Dialog
    "edit_quantity_title": "تعديل الكمية",
    "edit_item_quantity": "تعديل كمية العنصر",
    "item_info": "معلومات العنصر",
    "item_label": "العنصر: {}",
    "current_quantity": "الكمية الحالية: {}",
    "new_quantity": "الكمية الجديدة:",
    
    # Outbound Dialog
    "outbound_title": "إخراج بضاعة",
    "outbound_item_title": "إخراج بضاعة من المخزون",
    "outbound_quantity_label": "الكمية المطلوب إخراجها:",
    "recipient_name_label": "اسم المستلم:",
    "available_quantity": "الكمية المتاحة: {}",
    "remaining_quantity": "الكمية المتبقية: {}",
    
    # Status Messages
    "adding_item": "جاري إضافة العنصر...",
    "item_added": "تم إضافة العنصر بنجاح",
    "updating_quantity": "جاري تحديث الكمية...",
    "quantity_updated": "تم تحديث الكمية بنجاح",
    "processing_outbound": "جاري إخراج البضاعة...",
    "outbound_processed": "تم إخراج البضاعة بنجاح",
    "removing_item": "جاري حذف العنصر...",
    "item_removed": "تم حذف العنصر بنجاح",
    "operation_failed": "فشلت العملية",
    
    # Error Messages
    "error": "خطأ",
    "connection_error": "خطأ في الاتصال",
    "data_error": "خطأ في البيانات",
    "operation_error": "خطأ في العملية",
    "enter_item_name": "يرجى إدخال اسم العنصر.",
    "enter_valid_quantity": "يرجى إدخال كمية صحيحة (رقم غير سالب).",
    "enter_recipient_name": "يرجى إدخال اسم المستلم.",
    "insufficient_quantity": "الكمية المطلوبة أكبر من الكمية المتاحة.",
    "enter_outbound_quantity": "يرجى إدخال كمية الإخراج.",
    "no_change": "لا توجد تغييرات",
    "quantity_same": "الكمية هي نفس القيمة الحالية.",
    "confirm_removal": "تأكيد الحذف",
    "confirm_remove_item": "هل أنت متأكد من حذف '{}'؟",
    
    # Connection Error Details
    "connection_error_details": "فشل في الاتصال بجداول جوجل:\\n{}\\n\\nيرجى التحقق من ملف بيانات الاعتماد واتصال الإنترنت.",
    "data_error_details": "فشل في تحميل بيانات المخزون:\\n{}",
    "operation_error_details": "فشلت العملية:\\n{}"
}

def get_text(key: str, *args) -> str:
    """
    Get localized text with formatting support.
    
    Args:
        key: Text key
        *args: Format arguments
        
    Returns:
        Formatted localized text
    """
    text = ARABIC_STRINGS.get(key, key)
    if args:
        try:
            return text.format(*args)
        except:
            return text
    return text