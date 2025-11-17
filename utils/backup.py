"""
نظام النسخ الاحتياطي البسيط
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path

class BackupManager:
    """مدير النسخ الاحتياطية"""
    
    def __init__(self, backup_dir="backups"):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)
    
    def create_config_backup(self):
        """نسخة احتياطية من ملفات الإعدادات"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = self.backup_dir / f"config_backup_{timestamp}"
            backup_path.mkdir(exist_ok=True)
            
            # نسخ ملفات الإعدادات
            config_files = ['config/config.json', 'config/settings.py']
            for file_path in config_files:
                if os.path.exists(file_path):
                    shutil.copy2(file_path, backup_path / os.path.basename(file_path))
            
            print(f"تم إنشاء نسخة احتياطية: {backup_path}")
            return True
            
        except Exception as e:
            print(f"خطأ في إنشاء النسخة الاحتياطية: {e}")
            return False
    
    def restore_config_backup(self, backup_name):
        """استعادة نسخة احتياطية"""
        try:
            backup_path = self.backup_dir / backup_name
            if not backup_path.exists():
                print(f"النسخة الاحتياطية غير موجودة: {backup_name}")
                return False
            
            # استعادة الملفات
            for file_path in backup_path.glob("*"):
                target_path = f"config/{file_path.name}"
                shutil.copy2(file_path, target_path)
            
            print(f"تم استعادة النسخة الاحتياطية: {backup_name}")
            return True
            
        except Exception as e:
            print(f"خطأ في استعادة النسخة الاحتياطية: {e}")
            return False
    
    def list_backups(self):
        """قائمة النسخ الاحتياطية المتاحة"""
        backups = []
        for backup_path in self.backup_dir.glob("config_backup_*"):
            if backup_path.is_dir():
                backups.append(backup_path.name)
        return sorted(backups, reverse=True)

# إنشاء مدير النسخ الاحتياطية
backup_manager = BackupManager()
