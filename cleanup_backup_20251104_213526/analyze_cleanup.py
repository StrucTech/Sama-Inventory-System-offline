#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تحليل الملفات المطلوبة لـ main_with_auth.py
"""

import os
import ast
import sys

def analyze_imports(file_path):
    """تحليل imports في ملف"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
        
        return imports
    except:
        return []

def find_required_files():
    """العثور على الملفات المطلوبة لـ main_with_auth.py"""
    print("🔍 تحليل الملفات المطلوبة لـ main_with_auth.py...")
    print("=" * 60)
    
    required_files = set()
    required_dirs = set()
    
    # ملفات أساسية
    core_files = [
        "main_with_auth.py",
        "requirements.txt",
        "README.md",
        "README_Arabic.md"
    ]
    
    for file in core_files:
        if os.path.exists(file):
            required_files.add(file)
    
    # تحليل main_with_auth.py
    main_imports = analyze_imports("main_with_auth.py")
    print("📋 Imports في main_with_auth.py:")
    for imp in main_imports:
        print(f"   - {imp}")
    
    # مجلدات مطلوبة
    required_dirs.update(["gui", "config", "sheets", "auth", "localization"])
    
    # ملفات مطلوبة
    essential_files = [
        # Core files
        "main_with_auth.py",
        "enhanced_sheets_manager.py", 
        "new_filter_window.py",
        
        # Configuration
        "requirements.txt",
        "credentials.json",  # إذا كان موجوداً
        
        # Documentation
        "README.md",
        "README_Arabic.md",
        "حل_مشكلة_الفلاتر.md",
        "نظام_الفلاتر_الجديد.md"
    ]
    
    print(f"\n📂 المجلدات المطلوبة:")
    for dir_name in sorted(required_dirs):
        if os.path.isdir(dir_name):
            print(f"   ✅ {dir_name}/")
            required_files.add(dir_name + "/")
        else:
            print(f"   ❌ {dir_name}/ (غير موجود)")
    
    print(f"\n📄 الملفات الأساسية:")
    for file in essential_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
            required_files.add(file)
        else:
            print(f"   ❌ {file} (غير موجود)")
    
    # تحليل الملفات في gui/
    gui_files = []
    if os.path.isdir("gui"):
        for file in os.listdir("gui"):
            if file.endswith(".py"):
                gui_files.append(f"gui/{file}")
                required_files.add(f"gui/{file}")
    
    print(f"\n🖥️ ملفات GUI المطلوبة:")
    for file in sorted(gui_files):
        print(f"   ✅ {file}")
    
    # باقي المجلدات
    other_dirs = ["config", "sheets", "auth", "localization"]
    for dir_name in other_dirs:
        if os.path.isdir(dir_name):
            for root, dirs, files in os.walk(dir_name):
                for file in files:
                    file_path = os.path.join(root, file).replace("\\", "/")
                    required_files.add(file_path)
    
    return required_files

def get_unnecessary_files():
    """العثور على الملفات غير المطلوبة"""
    print("\n🗑️ تحليل الملفات غير المطلوبة...")
    print("=" * 60)
    
    required = find_required_files()
    all_files = set()
    
    # جمع جميع الملفات
    for root, dirs, files in os.walk("."):
        # تجاهل مجلدات معينة
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', '.github', 'backups']]
        
        for file in files:
            file_path = os.path.join(root, file).replace("\\", "/")
            if file_path.startswith("./"):
                file_path = file_path[2:]
            all_files.add(file_path)
    
    # الملفات غير المطلوبة
    unnecessary = all_files - required
    
    # تصنيف الملفات غير المطلوبة
    test_files = [f for f in unnecessary if f.startswith("test_")]
    old_files = [f for f in unnecessary if any(keyword in f.lower() for keyword in ["old", "backup", "temp", "debug"])]
    docs = [f for f in unnecessary if f.endswith(".md") and f not in required]
    other = [f for f in unnecessary if f not in test_files and f not in old_files and f not in docs]
    
    print(f"📊 ملخص التحليل:")
    print(f"   ✅ ملفات مطلوبة: {len(required)}")
    print(f"   🗑️ ملفات غير مطلوبة: {len(unnecessary)}")
    print(f"      - ملفات اختبار: {len(test_files)}")
    print(f"      - ملفات قديمة: {len(old_files)}")
    print(f"      - وثائق إضافية: {len(docs)}")
    print(f"      - أخرى: {len(other)}")
    
    return {
        "test_files": test_files,
        "old_files": old_files,
        "docs": docs,
        "other": other
    }

if __name__ == "__main__":
    os.chdir(r"D:\StrucTech Projects\Inventory System")
    
    print("🧹 تحليل تنظيف الملفات")
    print("=" * 60)
    
    unnecessary = get_unnecessary_files()
    
    print(f"\n🗑️ ملفات الاختبار ({len(unnecessary['test_files'])}):")
    for file in sorted(unnecessary['test_files'])[:10]:  # أول 10
        print(f"   - {file}")
    if len(unnecessary['test_files']) > 10:
        print(f"   ... و {len(unnecessary['test_files']) - 10} ملف آخر")
    
    print(f"\n📄 وثائق إضافية ({len(unnecessary['docs'])}):")
    for file in sorted(unnecessary['docs']):
        print(f"   - {file}")
    
    print(f"\n📁 ملفات أخرى ({len(unnecessary['other'])}):")
    for file in sorted(unnecessary['other'])[:10]:  # أول 10
        print(f"   - {file}")
    if len(unnecessary['other']) > 10:
        print(f"   ... و {len(unnecessary['other']) - 10} ملف آخر")
    
    print(f"\n💡 توصيات:")
    print(f"   1. يمكن حذف جميع ملفات test_*.py")
    print(f"   2. يمكن نقل الوثائق الإضافية لمجلد docs/")
    print(f"   3. يمكن حذف الملفات القديمة والمؤقتة")
    print(f"   4. الاحتفاظ بالملفات الأساسية المطلوبة فقط")