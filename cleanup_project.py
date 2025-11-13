#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تنظيف الملفات غير المطلوبة والاحتفاظ بالملفات الأساسية فقط
"""

import os
import shutil
from datetime import datetime

def cleanup_project():
    """تنظيف المشروع من الملفات غير المطلوبة"""
    print("🧹 بدء تنظيف المشروع...")
    print("=" * 60)
    
    # إنشاء مجلد النسخ الاحتياطية
    backup_dir = f"cleanup_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"📁 تم إنشاء مجلد النسخ الاحتياطية: {backup_dir}")
    
    # الملفات والمجلدات الأساسية المطلوبة
    essential_files = {
        # ملفات Python أساسية
        "main_with_auth.py",
        "enhanced_sheets_manager.py", 
        "new_filter_window.py",
        
        # ملفات التكوين
        "requirements.txt",
        
        # الوثائق المهمة
        "README.md",
        "README_Arabic.md",
        "حل_مشكلة_الفلاتر.md",
        "نظام_الفلاتر_الجديد.md",
        
        # قاعدة البيانات
        "inventory_users.db"
    }
    
    essential_dirs = {
        "gui", "config", "sheets", "auth", "localization"
    }
    
    # ملفات للحذف
    files_to_delete = []
    
    # جمع ملفات الاختبار
    test_files = [f for f in os.listdir(".") if f.startswith("test_") and f.endswith(".py")]
    files_to_delete.extend(test_files)
    
    # جمع الوثائق الإضافية
    additional_docs = [
        "ACTIVITY_LOG_GUIDE.md", "CATEGORY_UPDATE.md", "DEVELOPER_GUIDE.md",
        "DROPDOWN_FEATURE.md", "DROPDOWN_FIX.md", "ENHANCED_FILTER_SUMMARY.md",
        "FINAL_DIALOG_FIXES.md", "FINAL_DROPDOWN_FIX.md", "GETTING_STARTED.md",
        "GETTING_STARTED_Arabic.md", "LOGIN_SYSTEM_GUIDE.md", "NEW_CATEGORY_SOLUTION.md",
        "PROJECT_COMPLETION_REPORT.md", "PROJECT_COMPLETION_SUMMARY.md", "PROJECT_OVERVIEW.md",
        "PROJECT_SUMMARY.md", "PROJECT_SYSTEM_OVERVIEW.md", "SECURITY_UPDATE_SUMMARY.md",
        "ULTIMATE_DROPDOWN_FIX.md", "USER_GUIDE.md", "USER_PERMISSIONS_GUIDE.md",
        "activity_log_restructure_proposal.md", "filter_fix_report.md",
        "filter_search_completion_report.md", "filter_usage_guide.md",
        "final_complete_solution.md", "final_filter_complete_report.md",
        "final_filter_updates_report.md", "final_fixes_report.md",
        "new_activity_log_structure.md"
    ]
    files_to_delete.extend([f for f in additional_docs if os.path.exists(f)])
    
    # جمع الملفات الأخرى غير المطلوبة
    other_files = [
        "add_sample_data.py", "add_sample_items.py", "analyze_activity_log.py",
        "analyze_cleanup.py", "check_worksheets.py", "convert_activity_log.py",
        "create_users_sheet.py", "demo_dropdown.py", "enhanced_filter_app.py",
        "explore_sheets.py", "filter_usage_guide.py", "final_test_dropdown.py",
        "find_spreadsheet.py", "fixed_add_item_dialog.py", "fix_sheets_structure.py",
        "fix_table_display.py", "main.py", "main_arabic.py", "main_with_login.py",
        "quick_filter_test.py", "rebuild_inventory_sheet.py", "reset_sheets.py",
        "reset_sheets_with_data.py", "restructure_activity_log.py", "setup_check.py",
        "setup_users.py", "show_project_info.py", "simple_test_dialog.py",
        "solution_summary.py", "updates_summary.py", "view_activity_log.py"
    ]
    files_to_delete.extend([f for f in other_files if os.path.exists(f)])
    
    # نقل الملفات للنسخ الاحتياطية وحذفها
    deleted_count = 0
    
    print(f"\n🗑️ حذف الملفات غير المطلوبة:")
    for file in files_to_delete:
        if os.path.exists(file):
            try:
                # نسخ للباك اب
                shutil.copy2(file, backup_dir)
                # حذف الملف الأصلي
                os.remove(file)
                print(f"   ✅ تم حذف: {file}")
                deleted_count += 1
            except Exception as e:
                print(f"   ❌ فشل حذف {file}: {e}")
    
    # حذف مجلدات غير مطلوبة
    dirs_to_delete = ["tests", "backups"]
    for dir_name in dirs_to_delete:
        if os.path.exists(dir_name) and os.path.isdir(dir_name):
            try:
                shutil.copytree(dir_name, os.path.join(backup_dir, dir_name))
                shutil.rmtree(dir_name)
                print(f"   ✅ تم حذف المجلد: {dir_name}/")
                deleted_count += 1
            except Exception as e:
                print(f"   ❌ فشل حذف المجلد {dir_name}: {e}")
    
    # إنشاء مجلد docs ونقل الوثائق المتبقية
    docs_dir = "docs"
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)
        print(f"📁 تم إنشاء مجلد: {docs_dir}/")
    
    # عرض الملفات المتبقية
    print(f"\n📊 ملخص التنظيف:")
    print(f"   🗑️ تم حذف: {deleted_count} ملف/مجلد")
    print(f"   💾 نسخ احتياطية في: {backup_dir}/")
    
    print(f"\n✅ الملفات الأساسية المتبقية:")
    remaining_files = []
    for item in os.listdir("."):
        if os.path.isfile(item):
            remaining_files.append(item)
        elif os.path.isdir(item) and item not in [backup_dir, "__pycache__", ".git"]:
            remaining_files.append(f"{item}/")
    
    for item in sorted(remaining_files):
        print(f"   📄 {item}")
    
    print(f"\n🎯 المشروع النظيف جاهز!")
    print(f"   - الملف الرئيسي: main_with_auth.py")
    print(f"   - نظام الفلاتر: new_filter_window.py")
    print(f"   - إدارة البيانات: enhanced_sheets_manager.py")
    print(f"   - المجلدات: {', '.join(essential_dirs)}")

def create_project_structure_summary():
    """إنشاء ملخص هيكل المشروع النهائي"""
    summary = """# 🎯 هيكل المشروع النهائي - نظام إدارة المخزون

## 📁 الملفات الأساسية

### 🔧 ملفات Python الرئيسية
- `main_with_auth.py` - نقطة البداية الرئيسية مع نظام تسجيل الدخول
- `enhanced_sheets_manager.py` - إدارة Google Sheets المحسنة
- `new_filter_window.py` - نافذة الفلاتر المحسنة

### ⚙️ ملفات التكوين
- `requirements.txt` - متطلبات Python
- `inventory_users.db` - قاعدة بيانات المستخدمين

### 📚 الوثائق
- `README.md` - دليل المشروع (English)
- `README_Arabic.md` - دليل المشروع (العربية)
- `حل_مشكلة_الفلاتر.md` - دليل حل مشاكل الفلاتر
- `نظام_الفلاتر_الجديد.md` - دليل نظام الفلاتر الجديد

## 📂 المجلدات

### 🖥️ gui/
واجهات المستخدم الرسومية
- `main_window.py` - النافذة الرئيسية
- `login_window.py` - نافذة تسجيل الدخول
- `inventory_view.py` - عرض المخزون
- `add_item_dialog.py` - حوار إضافة عنصر
- `edit_quantity_dialog.py` - حوار تعديل الكمية
- `outbound_dialog.py` - حوار الإخراج
- `admin_projects_window.py` - نافذة إدارة المشاريع
- `reports_window.py` - نافذة التقارير

### ⚙️ config/
إعدادات التطبيق
- `settings.py` - إدارة الإعدادات
- `config.json` - ملف الإعدادات

### 📊 sheets/
إدارة Google Sheets
- `manager.py` - مدير الشيتس الأساسي
- `auth.py` - المصادقة

### 🔐 auth/
نظام المصادقة
- `user_manager.py` - إدارة المستخدمين
- `permissions.py` - صلاحيات المستخدمين

### 🌐 localization/
الترجمة والتعريب
- `ar.py` - النصوص العربية
- `en.py` - النصوص الإنجليزية

## 🚀 كيفية التشغيل

```bash
# تثبيت المتطلبات
pip install -r requirements.txt

# تشغيل التطبيق
python main_with_auth.py
```

## 🔑 تسجيل الدخول الافتراضي
- المستخدم: `admin`
- كلمة المرور: `admin`

## ✨ المميزات الرئيسية
- ✅ نظام تسجيل دخول آمن
- ✅ واجهة عربية/إنجليزية
- ✅ إدارة المخزون مع Google Sheets
- ✅ نظام فلاتر متقدم (7 أنواع)
- ✅ تقارير وإحصائيات
- ✅ إدارة المشاريع والمستخدمين
- ✅ نظام صلاحيات

---
**تم التنظيف والإعداد:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    with open("PROJECT_STRUCTURE.md", "w", encoding="utf-8") as f:
        f.write(summary)
    
    print("📄 تم إنشاء ملف PROJECT_STRUCTURE.md")

if __name__ == "__main__":
    try:
        print("⚠️  تحذير: سيتم حذف الملفات غير المطلوبة!")
        print("💾 سيتم حفظ نسخ احتياطية قبل الحذف")
        
        response = input("\n❓ هل تريد المتابعة؟ (y/n): ")
        
        if response.lower() in ['y', 'yes', 'نعم']:
            cleanup_project()
            create_project_structure_summary()
            print("\n🎉 تم تنظيف المشروع بنجاح!")
        else:
            print("❌ تم إلغاء العملية")
            
    except KeyboardInterrupt:
        print("\n❌ تم إيقاف العملية بواسطة المستخدم")
    except Exception as e:
        print(f"\n❌ خطأ: {e}")