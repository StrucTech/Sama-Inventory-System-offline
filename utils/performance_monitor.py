"""
مراقب الأداء والاستخدام
تتبع استخدام الذاكرة وسرعة الاستجابة
"""

import psutil
import time
from datetime import datetime

class PerformanceMonitor:
    """مراقب الأداء"""
    
    def __init__(self):
        self.start_time = time.time()
        self.memory_usage = []
        self.operation_times = {}
    
    def start_operation(self, operation_name: str):
        """بدء مراقبة عملية"""
        self.operation_times[operation_name] = time.time()
    
    def end_operation(self, operation_name: str):
        """إنهاء مراقبة عملية"""
        if operation_name in self.operation_times:
            duration = time.time() - self.operation_times[operation_name]
            print(f"⏱️ {operation_name}: {duration:.2f} ثانية")
            return duration
        return 0
    
    def check_memory(self):
        """فحص استخدام الذاكرة"""
        process = psutil.Process()
        memory_mb = process.memory_info().rss / 1024 / 1024
        self.memory_usage.append(memory_mb)
        return memory_mb
    
    def get_system_info(self):
        """معلومات النظام"""
        return {
            'memory_mb': self.check_memory(),
            'cpu_percent': psutil.cpu_percent(),
            'uptime_seconds': time.time() - self.start_time
        }
    
    def generate_report(self):
        """تقرير الأداء"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'peak_memory_mb': max(self.memory_usage) if self.memory_usage else 0,
            'average_memory_mb': sum(self.memory_usage) / len(self.memory_usage) if self.memory_usage else 0,
            'total_uptime': time.time() - self.start_time,
            'operation_count': len(self.operation_times)
        }
        return report

# مراقب عالمي
performance_monitor = PerformanceMonitor()
