@echo off
chcp 65001 > nul
echo 🚀 بناء النسخة المستقلة من نظام إدارة المخزون
echo ================================================

:: التحقق من وجود Python
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ Python غير مثبت! يرجى تثبيت Python أولاً
    pause
    exit /b 1
)

echo ✅ Python متاح

:: التحقق من وجود PyInstaller
pip show pyinstaller > nul 2>&1
if errorlevel 1 (
    echo 📦 تثبيت PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo ❌ فشل في تثبيت PyInstaller
        pause
        exit /b 1
    )
)

echo ✅ PyInstaller متاح

:: تنظيف المجلدات السابقة
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
echo 🗑️ تم تنظيف المجلدات السابقة

:: بناء التطبيق
echo 🔨 بدء بناء التطبيق...
python build_setup.py

if errorlevel 1 (
    echo ❌ فشل في بناء التطبيق
    pause
    exit /b 1
)

echo ✅ تم بناء التطبيق بنجاح!

:: فتح مجلد النتيجة
if exist "dist\نظام إدارة المخزون" (
    echo 📂 فتح مجلد النتيجة...
    explorer "dist\نظام إدارة المخزون"
) else (
    echo 📂 ابحث عن النتيجة في مجلد dist
    explorer "dist"
)

echo.
echo 🎉 اكتمل البناء بنجاح!
echo 📁 ستجد الملف التنفيذي في مجلد dist
echo.
pause