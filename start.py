#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ملف تشغيل سريع لنظام إدارة المخزن
"""

import subprocess
import sys
import os

def main():
    """تشغيل النظام"""
    try:
        # التأكد من وجود البيئة الافتراضية
        venv_python = os.path.join(".venv", "Scripts", "python.exe")
        
        if os.path.exists(venv_python):
            # تشغيل من البيئة الافتراضية
            subprocess.run([venv_python, "main.py"])
        else:
            # تشغيل مباشر من Python
            subprocess.run([sys.executable, "main.py"])
            
    except Exception as e:
        print(f"خطأ في تشغيل النظام: {e}")
        input("اضغط Enter للخروج...")

if __name__ == "__main__":
    main()