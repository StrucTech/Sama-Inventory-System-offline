@echo off
echo 🧪 تشغيل الاختبارات الشاملة لنظام إدارة المخزون
echo ============================================

cd /d "%~dp0"

echo.
echo 📋 فحص متطلبات البيئة...
python -c "import sys; print(f'Python: {sys.version}')"
python -c "import tkinter; print('✅ Tkinter متاح')" 2>nul || echo "❌ Tkinter غير متاح"

echo.
echo 🚀 بدء تشغيل جميع الاختبارات...
echo.

python run_all_tests.py

echo.
echo ✨ انتهت الاختبارات!
echo 📄 تحقق من ملف test_report.html للحصول على التقرير المفصل

pause