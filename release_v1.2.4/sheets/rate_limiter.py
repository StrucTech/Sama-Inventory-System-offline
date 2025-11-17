"""
تحكم في معدل الطلبات لتجنب تجاوز حدود Google Sheets API
"""

import time
import threading
from functools import wraps

class RateLimiter:
    """فئة للتحكم في معدل الطلبات"""
    
    def __init__(self, max_calls=100, time_window=60):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = []
        self.lock = threading.Lock()
    
    def can_make_call(self):
        """التحقق من إمكانية إجراء طلب"""
        with self.lock:
            now = time.time()
            # إزالة الطلبات القديمة
            self.calls = [call_time for call_time in self.calls if now - call_time < self.time_window]
            
            if len(self.calls) < self.max_calls:
                self.calls.append(now)
                return True
            return False
    
    def wait_if_needed(self):
        """انتظار إذا لزم الأمر"""
        while not self.can_make_call():
            time.sleep(1)

# إنشاء محدد معدل عالمي
sheets_rate_limiter = RateLimiter(max_calls=90, time_window=60)

def rate_limited(func):
    """ديكوريتر للتحكم في معدل الطلبات"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        sheets_rate_limiter.wait_if_needed()
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if "429" in str(e) or "Quota exceeded" in str(e):
                print(f"تم تجاوز الحد المسموح - انتظار 60 ثانية...")
                time.sleep(60)
                return func(*args, **kwargs)
            raise e
    return wrapper
