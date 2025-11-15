"""
Build script for Sama Inventory Management System
Creates standalone .exe executable for Windows
"""

import os
import sys
import shutil
from pathlib import Path
import PyInstaller.__main__

# معلومات البرنامج
APP_NAME = "SamaInventorySystem"
APP_DISPLAY_NAME = "نظام إدارة المخزون"  # للعرض فقط
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "نظام متقدم لإدارة المخزون والمواد"
MAIN_SCRIPT = "main_with_auth.py"

def clean_build_dirs():
    """تنظيف مجلدات البناء السابقة"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"[INFO] Removed {dir_name}")

def create_spec_file():
    """إنشاء ملف .spec مخصص لـ PyInstaller"""
    spec_content = f'''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['{MAIN_SCRIPT}'],
    pathex=[],
    binaries=[],
    datas=[
        ('gui', 'gui'),
        ('sheets', 'sheets'),
        ('config', 'config'),
        ('localization', 'localization'),
        ('docs', 'docs'),
        ('requirements.txt', '.'),
        ('README.md', '.'),
        ('*.py', '.'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'gspread',
        'google.auth',
        'google.oauth2',
        'matplotlib',
        'seaborn',
        'numpy',
        'pandas',
        'arabic_reshaper',
        'python_bidi',
        'requests',
        'urllib3',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyd_list = []
a.binaries = [x for x in a.binaries if not x[0].endswith('.pyd')]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{APP_NAME}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # إخفاء نافذة الكونسول
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version_info.txt',
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)
'''
    
    with open('inventory_system.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("[INFO] Spec file created")

def create_version_info():
    """إنشاء ملف معلومات الإصدار"""
    version_info = f'''
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({APP_VERSION.replace('.', ', ')}, 0),
    prodvers=({APP_VERSION.replace('.', ', ')}, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          u'040904B0',
          [StringStruct(u'CompanyName', u'StrucTech Solutions'),
          StringStruct(u'FileDescription', u'{APP_DESCRIPTION}'),
          StringStruct(u'FileVersion', u'{APP_VERSION}'),
          StringStruct(u'InternalName', u'{APP_NAME}'),
          StringStruct(u'LegalCopyright', u'© 2025 StrucTech Solutions'),
          StringStruct(u'OriginalFilename', u'{APP_NAME}.exe'),
          StringStruct(u'ProductName', u'{APP_NAME}'),
          StringStruct(u'ProductVersion', u'{APP_VERSION}')])
      ]
    ),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
    
    with open('version_info.txt', 'w', encoding='utf-8') as f:
        f.write(version_info)
    
    print("[INFO] Version info file created")

def build_executable():
    """بناء الملف التنفيذي"""
    print("[INFO] Starting build process...")
    
    # تنظيف المجلدات السابقة
    clean_build_dirs()
    
    # إنشاء الملفات المطلوبة
    create_spec_file()
    create_version_info()
    
    # بناء التطبيق باستخدام PyInstaller
    PyInstaller.__main__.run([
        'inventory_system.spec',
        '--clean',
        '--noconfirm',
    ])
    
    print("[SUCCESS] Executable built successfully!")
    
    # نسخ الملفات الإضافية
    copy_additional_files()

def copy_additional_files():
    """نسخ الملفات الإضافية المطلوبة"""
    dist_dir = Path('dist') / APP_NAME
    
    if dist_dir.exists():
        # نسخ ملف الإعدادات النموذجي
        if os.path.exists('config/config_template.json'):
            shutil.copy('config/config_template.json', dist_dir / 'config.json')
        
        # إنشاء ملف README للمستخدم النهائي
        create_user_readme(dist_dir)
        
        # إنشاء ملف التحديث
        create_update_info(dist_dir)
        
        print(f"[INFO] Files ready in: {dist_dir}")

def create_user_readme(dist_dir):
    """إنشاء ملف README للمستخدم النهائي"""
    readme_content = f'''
# {APP_DISPLAY_NAME} - النسخة المستقلة

## متطلبات التشغيل:
- نظام تشغيل Windows 10 أو أحدث
- اتصال بالإنترنت
- حساب Google مع صلاحية الوصول لـ Google Sheets

## طريقة التشغيل:
1. قم بتشغيل "{APP_NAME}.exe"
2. في المرة الأولى، ستحتاج لإعداد:
   - ملف اعتماد Google Sheets
   - اسم ملف Google Sheets
   - بيانات المدير

## الإعدادات:
- ملف الإعدادات: config.json
- يمكنك تعديل الإعدادات من خلال البرنامج

## التحديثات:
- البرنامج يتحقق من التحديثات تلقائياً عند بدء التشغيل
- التحديثات تُحمل وتُثبت تلقائياً

## الدعم الفني:
للدعم الفني، يرجى التواصل مع فريق StrucTech Solutions

الإصدار: {APP_VERSION}
تاريخ البناء: {Path(__file__).stat().st_mtime}
'''
    
    with open(dist_dir / 'README.txt', 'w', encoding='utf-8') as f:
        f.write(readme_content)

def create_update_info(dist_dir):
    """إنشاء ملف معلومات التحديث"""
    update_info = {
        "current_version": APP_VERSION,
        "update_url": "https://api.github.com/repos/StrucTech/Sama-Inventory-System/releases/latest",
        "check_interval": 24,  # التحقق كل 24 ساعة
        "auto_update": True
    }
    
    import json
    with open(dist_dir / 'update_info.json', 'w', encoding='utf-8') as f:
        json.dump(update_info, f, ensure_ascii=False, indent=2)

def main():
    """Main function for building the application"""
    print(f"Building {APP_NAME} - Version {APP_VERSION}")
    print("=" * 50)
    
    try:
        # Check if PyInstaller is available
        import PyInstaller
        print(f"[OK] PyInstaller version: {PyInstaller.__version__}")
    except ImportError:
        print("[ERROR] PyInstaller not installed!")
        print("Install it with: pip install pyinstaller")
        return
    
    # Check if main script exists
    if not os.path.exists(MAIN_SCRIPT):
        print(f"[ERROR] Main script not found: {MAIN_SCRIPT}")
        return
    
    # Build the application
    build_executable()
    
    print("=" * 50)
    print("[SUCCESS] Build completed successfully!")
    print(f"[INFO] Executable location: dist/{APP_NAME}/")
    print(f"[INFO] Run the file: dist/{APP_NAME}/{APP_NAME}.exe")

if __name__ == "__main__":
    main()