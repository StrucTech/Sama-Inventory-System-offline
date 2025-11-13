@echo off
chcp 65001 > nul
echo 🏷️ إنشاء إصدار جديد - نظام Sama لإدارة المخزون
echo =====================================================

:: التحقق من وجود Git
git --version > nul 2>&1
if errorlevel 1 (
    echo ❌ Git غير مثبت! يرجى تثبيت Git أولاً
    pause
    exit /b 1
)

echo ✅ Git متاح

:: عرض الإصدار الحالي
echo.
echo 📋 معلومات المشروع الحالية:
echo Repository: https://github.com/StrucTech/Sama-Inventory-System

:: الحصول على آخر tag
for /f "tokens=*" %%i in ('git describe --tags --abbrev=0 2^>nul') do (
    set LAST_TAG=%%i
)

if defined LAST_TAG (
    echo آخر إصدار: %LAST_TAG%
) else (
    echo آخر إصدار: لا يوجد
    set LAST_TAG=v0.0.0
)

echo.
echo 🔢 إدخال رقم الإصدار الجديد:
echo تنسيق الإصدار: v1.0.0, v1.1.0, v2.0.0, إلخ...
echo.
set /p NEW_VERSION="أدخل رقم الإصدار الجديد (مثال: v1.0.1): "

if "%NEW_VERSION%"=="" (
    echo ❌ يجب إدخال رقم إصدار!
    pause
    exit /b 1
)

:: التحقق من تنسيق الإصدار
echo %NEW_VERSION% | findstr /r "^v[0-9]*\.[0-9]*\.[0-9]*$" > nul
if errorlevel 1 (
    echo ❌ تنسيق الإصدار غير صحيح! استخدم v1.0.0
    pause
    exit /b 1
)

echo.
echo 📝 إدخال وصف الإصدار:
set /p RELEASE_NOTES="وصف التحديثات (اختياري): "

echo.
echo 📋 ملخص الإصدار الجديد:
echo ========================
echo الإصدار: %NEW_VERSION%
echo الوصف: %RELEASE_NOTES%
echo Repository: https://github.com/StrucTech/Sama-Inventory-System
echo.

set /p CONFIRM="هل تريد المتابعة؟ (y/n): "
if /i not "%CONFIRM%"=="y" (
    echo ❌ تم الإلغاء
    pause
    exit /b 1
)

echo.
echo 🔄 جاري إنشاء الإصدار...

:: تحديث رقم الإصدار في build_setup.py
echo 📝 تحديث رقم الإصدار في الكود...
set VERSION_NUMBER=%NEW_VERSION:v=%
powershell -Command "(Get-Content 'build_setup.py') -replace 'APP_VERSION = \"[^\"]*\"', 'APP_VERSION = \"%VERSION_NUMBER%\"' | Set-Content 'build_setup.py'"

:: إضافة جميع التغييرات
echo ➕ إضافة التغييرات...
git add .

:: إنشاء commit
if "%RELEASE_NOTES%"=="" (
    git commit -m "Release %NEW_VERSION%"
) else (
    git commit -m "Release %NEW_VERSION%: %RELEASE_NOTES%"
)

if errorlevel 1 (
    echo ❌ فشل في إنشاء commit
    pause
    exit /b 1
)

:: push التغييرات
echo 🚀 رفع التغييرات للمستودع...
git push origin main

if errorlevel 1 (
    echo ❌ فشل في رفع التغييرات
    pause
    exit /b 1
)

:: إنشاء tag
echo 🏷️ إنشاء tag للإصدار...
if "%RELEASE_NOTES%"=="" (
    git tag -a %NEW_VERSION% -m "Release %NEW_VERSION%"
) else (
    git tag -a %NEW_VERSION% -m "Release %NEW_VERSION%: %RELEASE_NOTES%"
)

if errorlevel 1 (
    echo ❌ فشل في إنشاء tag
    pause
    exit /b 1
)

:: push التags
echo 🚀 رفع tag للمستودع...
git push origin %NEW_VERSION%

if errorlevel 1 (
    echo ❌ فشل في رفع tag
    pause
    exit /b 1
)

echo.
echo 🎉 تم إنشاء الإصدار بنجاح!
echo ================================
echo الإصدار: %NEW_VERSION%
echo.
echo 🔗 الروابط المفيدة:
echo Repository: https://github.com/StrucTech/Sama-Inventory-System
echo Releases: https://github.com/StrucTech/Sama-Inventory-System/releases
echo Actions: https://github.com/StrucTech/Sama-Inventory-System/actions
echo.
echo ⏱️ البناء التلقائي سيبدأ خلال دقائق...
echo تابع التقدم في: https://github.com/StrucTech/Sama-Inventory-System/actions
echo.
echo 📦 بعد اكتمال البناء، ستجد النسخة المستقلة في:
echo https://github.com/StrucTech/Sama-Inventory-System/releases/tag/%NEW_VERSION%
echo.

:: فتح صفحة Actions في المتصفح (اختياري)
set /p OPEN_BROWSER="فتح صفحة GitHub Actions في المتصفح؟ (y/n): "
if /i "%OPEN_BROWSER%"=="y" (
    start https://github.com/StrucTech/Sama-Inventory-System/actions
)

echo.
echo ✅ تم! انتظر اكتمال البناء التلقائي على GitHub
pause