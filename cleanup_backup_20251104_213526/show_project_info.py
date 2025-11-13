"""
سكريبت لعرض ملخص شامل لبيانات المشروع
"""

import sys
import os
import json
import sqlite3
from datetime import datetime

# إضافة مسار المشروع
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sheets.manager import SheetsManager
from config.settings import load_config

def display_project_overview():
    """عرض ملخص شامل للمشروع والبيانات"""
    print("=" * 80)
    print("📋 ملخص شامل لمشروع نظام إدارة المخزون")
    print("=" * 80)
    
    # معلومات أساسية
    print("\n🎯 معلومات المشروع:")
    print("-" * 50)
    print("📂 المسار: D:\\StrucTech Projects\\Inventory System")
    print("⚡ التقنية: Python + tkinter + Google Sheets API")
    print("🌐 قاعدة البيانات: Google Sheets (سحابية)")
    print("💾 نسخة احتياطية: SQLite (محلية)")
    
    # فحص الإعدادات
    print("\n⚙️ إعدادات النظام:")
    print("-" * 50)
    
    try:
        config = load_config()
        if config:
            print(f"📊 اسم الجدول: {config.get('spreadsheet_name', 'غير محدد')}")
            print(f"📄 شيت المخزون: {config.get('worksheet_name', 'غير محدد')}")
            print(f"📋 شيت السجل: {config.get('activity_log_name', 'غير محدد')}")
            print(f"🌍 اللغة: {config.get('language', 'غير محدد')}")
            print(f"🔄 التحديث التلقائي: {config.get('auto_refresh_minutes', 0)} دقيقة")
            print(f"🖥️ أبعاد النافذة: {config.get('window', {}).get('width', 0)}×{config.get('window', {}).get('height', 0)}")
        else:
            print("❌ فشل في تحميل الإعدادات")
    except Exception as e:
        print(f"❌ خطأ في قراءة الإعدادات: {e}")
    
    # فحص Google Sheets
    print("\n🌐 بيانات Google Sheets:")
    print("-" * 50)
    
    try:
        config = load_config()
        if config:
            manager = SheetsManager(
                credentials_file=config.get('credentials_file', ''),
                spreadsheet_name=config.get('spreadsheet_name', ''),
                worksheet_name=config.get('worksheet_name', 'Inventory')
            )
            
            if manager.connect():
                print("✅ الاتصال: نجح")
                
                # معلومات الشيتات
                if manager.spreadsheet:
                    worksheets = manager.spreadsheet.worksheets()
                    print(f"📊 عدد الشيتات: {len(worksheets)}")
                    
                    for i, sheet in enumerate(worksheets, 1):
                        print(f"  {i}. 📄 {sheet.title} ({sheet.row_count}×{sheet.col_count})")
                        
                        # عدد الصفوف التي تحتوي على بيانات
                        try:
                            values = sheet.get_all_values()
                            data_rows = len([row for row in values if any(cell.strip() for cell in row)])
                            print(f"     📊 صفوف البيانات: {data_rows}")
                        except:
                            print(f"     📊 صفوف البيانات: غير متاح")
                    
                    # فحص بيانات المخزون
                    print("\n📦 بيانات المخزون:")
                    print("-" * 30)
                    try:
                        items = manager.get_all_items()
                        if items:
                            print(f"📈 إجمالي العناصر: {len(items)}")
                            total_quantity = sum(item.get('quantity', 0) for item in items)
                            print(f"📊 إجمالي الكميات: {total_quantity}")
                            
                            print("\n🔍 عينة من العناصر:")
                            for i, item in enumerate(items[:3], 1):
                                name = item.get('item_name', 'غير محدد')
                                qty = item.get('quantity', 0)
                                updated = item.get('last_updated', 'غير محدد')
                                print(f"  {i}. {name}: {qty} قطعة (آخر تحديث: {updated})")
                        else:
                            print("📦 لا توجد عناصر في المخزون")
                    except Exception as e:
                        print(f"❌ خطأ في قراءة المخزون: {e}")
                        
                else:
                    print("❌ فشل في الوصول للجدول")
            else:
                print("❌ الاتصال: فشل")
                
    except Exception as e:
        print(f"❌ خطأ في Google Sheets: {e}")
    
    # فحص قاعدة البيانات المحلية
    print("\n💽 قاعدة البيانات المحلية:")
    print("-" * 50)
    
    db_path = "inventory_users.db"
    if os.path.exists(db_path):
        print(f"✅ الملف: موجود ({os.path.getsize(db_path)} بايت)")
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # فحص الجداول
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            if tables:
                print(f"📊 عدد الجداول: {len(tables)}")
                for table in tables:
                    table_name = table[0]
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    count = cursor.fetchone()[0]
                    print(f"  📋 {table_name}: {count} سجل")
            else:
                print("📊 لا توجد جداول")
                
            conn.close()
            
        except Exception as e:
            print(f"❌ خطأ في قراءة قاعدة البيانات: {e}")
    else:
        print("❌ الملف: غير موجود")
    
    # فحص الملفات المهمة
    print("\n📁 الملفات المهمة:")
    print("-" * 50)
    
    important_files = [
        ("main.py", "نقطة البداية الرئيسية"),
        ("main_arabic.py", "النسخة العربية"),
        ("config/config.json", "إعدادات التطبيق"),
        ("config/credentials.json", "بيانات اعتماد Google API"),
        ("requirements.txt", "متطلبات Python"),
        ("tests/test_complete.py", "الاختبارات الشاملة"),
    ]
    
    for file_path, description in important_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {file_path}: {description} ({size} بايت)")
        else:
            print(f"❌ {file_path}: مفقود")
    
    # معلومات إضافية
    print("\n📈 إحصائيات إضافية:")
    print("-" * 50)
    
    # عدد ملفات Python
    py_files = 0
    total_lines = 0
    
    for root, dirs, files in os.walk("."):
        # تجاهل مجلدات معينة
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'venv']]
        
        for file in files:
            if file.endswith('.py'):
                py_files += 1
                try:
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = len(f.readlines())
                        total_lines += lines
                except:
                    pass
    
    print(f"🐍 ملفات Python: {py_files}")
    print(f"📝 أسطر الكود: ~{total_lines}")
    print(f"📅 آخر تعديل: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n" + "=" * 80)
    print("🎉 انتهى الملخص!")
    print("=" * 80)

if __name__ == "__main__":
    display_project_overview()
    input("\nاضغط Enter للخروج...")