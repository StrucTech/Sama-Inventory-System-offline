# -*- coding: utf-8 -*-
"""
سكريبت بناء ملفات EXE باستخدام PyInstaller
يبني البرنامجين: main.py و advanced_report_viewer.py
"""

import os
import subprocess
import sys
from pathlib import Path

def build_exe_for_file(python_file, app_name):
    """بناء ملف EXE واحد"""
    print(f"\n🔨 جاري بناء ملف {app_name}...")
    
    # التأكد من تثبيت PyInstaller
    try:
        import PyInstaller
    except ImportError:
        print("📦 تثبيت PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyInstaller"])
    
    # مسار المشروع
    project_dir = Path(__file__).parent
    main_file = project_dir / python_file
    
    if not main_file.exists():
        print(f"❌ الملف {python_file} غير موجود!")
        return False
    
    # الأيقونة (اختياري)
    icon_path = None
    if (project_dir / "icon.ico").exists():
        icon_path = str(project_dir / "icon.ico")
    
    # أوامر PyInstaller
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        f"--name={app_name}",
        "--onefile",  # ملف واحد
        f"--distpath={project_dir}/dist",
        f"--buildpath={project_dir}/build_{app_name}",
        f"--specpath={project_dir}/specs",
        "--console",  # إظهار console
        "--noupx",
        "--hidden-import=PyQt6",
        "--hidden-import=pandas",
        "--hidden-import=openpyxl",
        "--collect-all=PyQt6",
        str(main_file)
    ]
    
    # إضافة الأيقونة إذا كانت موجودة
    if icon_path:
        cmd.insert(-1, f"--icon={icon_path}")
    
    # تشغيل البناء
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ تم بناء {app_name}.exe بنجاح!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ خطأ في بناء {app_name}: {e}")
        return False

def main():
    """بناء جميع البرامج"""
    print("\n" + "="*50)
    print("🚀 بناء تطبيقات Sama Inventory System")
    print("="*50)
    
    project_dir = Path(__file__).parent
    
    # البرامج المراد بناؤها
    apps = [
        ("main.py", "SamaInventorySystem"),
        ("advanced_report_viewer.py", "SamaReportViewer")
    ]
    
    results = {}
    
    # بناء كل برنامج
    for py_file, app_name in apps:
        results[app_name] = build_exe_for_file(py_file, app_name)
    
    # ملخص النتائج
    print("\n" + "="*50)
    print("📊 ملخص البناء:")
    print("="*50)
    
    for app_name, success in results.items():
        status = "✅ نجح" if success else "❌ فشل"
        print(f"{app_name}: {status}")
    
    print(f"\n📁 الملفات موجودة في: {project_dir}/dist/")
    print("\nملفات البناء:")
    for py_file, app_name in apps:
        exe_path = project_dir / "dist" / f"{app_name}.exe"
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"  • {app_name}.exe ({size_mb:.2f} MB)")
    
    # العودة بكود الخروج
    success = all(results.values())
    print()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
