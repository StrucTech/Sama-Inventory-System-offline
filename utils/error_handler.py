"""
معالج الأخطاء المحسن
"""

import logging
import traceback
from functools import wraps
from datetime import datetime

# إعداد نظام التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('system.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('SamaInventory')

class ErrorHandler:
    """معالج الأخطاء المتقدم"""
    
    @staticmethod
    def handle_sheets_error(error):
        """معالجة أخطاء Google Sheets"""
        error_str = str(error)
        
        if "429" in error_str or "Quota exceeded" in error_str:
            logger.warning("تم تجاوز حد الطلبات - يُنصح بالانتظار")
            return "quota_exceeded"
        elif "403" in error_str:
            logger.error("خطأ في صلاحيات الوصول")
            return "permission_denied"
        elif "404" in error_str:
            logger.error("لم يتم العثور على الجدول")
            return "sheet_not_found"
        else:
            logger.error(f"خطأ غير متوقع في Google Sheets: {error}")
            return "unknown_error"
    
    @staticmethod
    def handle_network_error(error):
        """معالجة أخطاء الشبكة"""
        logger.error(f"خطأ في الشبكة: {error}")
        return "network_error"
    
    @staticmethod
    def log_error(error, context=""):
        """تسجيل الأخطاء"""
        logger.error(f"خطأ في {context}: {error}")
        logger.debug(traceback.format_exc())

def safe_execute(func):
    """ديكوريتر لتنفيذ آمن للدوال"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            ErrorHandler.log_error(e, func.__name__)
            return None
    return wrapper

# معالج الأخطاء العالمي
error_handler = ErrorHandler()
