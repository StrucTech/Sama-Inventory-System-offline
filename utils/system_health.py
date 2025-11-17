"""
فاحص صحة النظام
تحقق دوري من حالة جميع مكونات النظام
"""

import os
import json
import time
from datetime import datetime

class SystemHealthChecker:
    """فاحص صحة النظام"""
    
    def __init__(self):
        self.last_check = None
        self.health_status = {}
    
    def run_health_check(self) -> dict:
        """تشغيل فحص الصحة الشامل"""
        self.last_check = datetime.now()
        
        checks = {
            'files': self.check_critical_files(),
            'config': self.check_configuration(),
            'memory': self.check_memory_usage(),
            'logs': self.check_logs(),
            'permissions': self.check_permissions()
        }
        
        # حساب الصحة العامة
        total_checks = len(checks)
        passed_checks = sum(1 for result in checks.values() if result['status'] == 'ok')
        health_percentage = (passed_checks / total_checks) * 100
        
        self.health_status = {
            'timestamp': self.last_check.isoformat(),
            'overall_health': health_percentage,
            'status': 'healthy' if health_percentage >= 80 else 'warning' if health_percentage >= 60 else 'critical',
            'details': checks
        }
        
        return self.health_status
    
    def check_critical_files(self) -> dict:
        """فحص الملفات الحرجة"""
        critical_files = [
            'main_with_auth.py',
            'config/config.json',
            'gui/main_window.py',
            'sheets/manager.py'
        ]
        
        missing_files = [f for f in critical_files if not os.path.exists(f)]
        
        return {
            'status': 'ok' if not missing_files else 'error',
            'message': 'جميع الملفات موجودة' if not missing_files else f'ملفات مفقودة: {missing_files}',
            'missing_count': len(missing_files)
        }
    
    def check_configuration(self) -> dict:
        """فحص الإعدادات"""
        try:
            with open('config/config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            required_keys = ['spreadsheet_name', 'credentials_file']
            missing_keys = [key for key in required_keys if key not in config]
            
            return {
                'status': 'ok' if not missing_keys else 'warning',
                'message': 'الإعدادات سليمة' if not missing_keys else f'إعدادات ناقصة: {missing_keys}'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'خطأ في قراءة الإعدادات: {e}'
            }
    
    def check_memory_usage(self) -> dict:
        """فحص استخدام الذاكرة"""
        try:
            import psutil
            memory_percent = psutil.virtual_memory().percent
            
            if memory_percent > 90:
                status = 'critical'
                message = f'استخدام ذاكرة عالي جداً: {memory_percent}%'
            elif memory_percent > 75:
                status = 'warning'  
                message = f'استخدام ذاكرة مرتفع: {memory_percent}%'
            else:
                status = 'ok'
                message = f'استخدام ذاكرة طبيعي: {memory_percent}%'
            
            return {
                'status': status,
                'message': message,
                'memory_percent': memory_percent
            }
        except:
            return {
                'status': 'warning',
                'message': 'لا يمكن قراءة معلومات الذاكرة'
            }
    
    def check_logs(self) -> dict:
        """فحص ملفات السجلات"""
        log_files = ['system.log', 'error.log']
        log_issues = []
        
        for log_file in log_files:
            if os.path.exists(log_file):
                file_size = os.path.getsize(log_file) / 1024 / 1024  # MB
                if file_size > 50:  # أكبر من 50 ميجا
                    log_issues.append(f'{log_file} كبير جداً ({file_size:.1f}MB)')
        
        return {
            'status': 'ok' if not log_issues else 'warning',
            'message': 'ملفات السجلات بحجم طبيعي' if not log_issues else f'مشاكل: {log_issues}'
        }
    
    def check_permissions(self) -> dict:
        """فحص صلاحيات الملفات"""
        sensitive_files = ['.gitignore', 'config/config.json']
        permission_issues = []
        
        for file_path in sensitive_files:
            if os.path.exists(file_path):
                # فحص بسيط للقراءة والكتابة
                if not os.access(file_path, os.R_OK):
                    permission_issues.append(f'{file_path}: لا يمكن القراءة')
                if not os.access(file_path, os.W_OK):
                    permission_issues.append(f'{file_path}: لا يمكن الكتابة')
        
        return {
            'status': 'ok' if not permission_issues else 'warning',
            'message': 'الصلاحيات سليمة' if not permission_issues else f'مشاكل صلاحيات: {permission_issues}'
        }
    
    def save_health_report(self):
        """حفظ تقرير الصحة"""
        if self.health_status:
            with open('system_health_report.json', 'w', encoding='utf-8') as f:
                json.dump(self.health_status, f, ensure_ascii=False, indent=2)
    
    def get_quick_status(self) -> str:
        """الحصول على حالة سريعة"""
        if not self.health_status:
            return "لم يتم فحص النظام بعد"
        
        overall_health = self.health_status.get('overall_health', 0)
        status = self.health_status.get('status', 'unknown')
        
        if status == 'healthy':
            return f"✅ صحي ({overall_health:.0f}%)"
        elif status == 'warning':
            return f"⚠️ تحذير ({overall_health:.0f}%)"
        else:
            return f"❌ مشاكل ({overall_health:.0f}%)"

# إنشاء فاحص عالمي
system_health = SystemHealthChecker()
