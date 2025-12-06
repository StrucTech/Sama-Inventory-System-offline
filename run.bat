@echo off
echo ================================================
echo        نظام إدارة المخزن الأوفلاين
echo        StrucTech Inventory Management System
echo ================================================
echo.

REM التحقق من وجود Python
python --version >nul 2>&1
if errorlevel 1 (
    echo خطأ: Python غير مثبت على النظام
    echo يرجى تثبيت Python 3.8 أو أحدث من python.org
    pause
    exit /b 1
)

REM التحقق من وجود البيئة الافتراضية
if not exist ".venv\" (
    echo إنشاء بيئة افتراضية...
    python -m venv .venv
    if errorlevel 1 (
        echo خطأ في إنشاء البيئة الافتراضية
        pause
        exit /b 1
    )
)

REM تفعيل البيئة الافتراضية
echo تفعيل البيئة الافتراضية...
call .venv\Scripts\activate.bat

REM تثبيت المتطلبات
echo تثبيت المكتبات المطلوبة...
pip install -r requirements.txt --quiet

REM تشغيل النظام
echo تشغيل نظام إدارة المخزن...
echo.
python main.py

REM إذا حدث خطأ
if errorlevel 1 (
    echo.
    echo حدث خطأ في تشغيل النظام
    echo يرجى التحقق من رسائل الخطأ أعلاه
    pause
)

echo.
echo شكراً لاستخدام نظام إدارة المخزن
pause