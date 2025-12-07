# -*- coding: utf-8 -*-
"""
Build script for creating EXE files using PyInstaller
Builds both applications: main.py and advanced_report_viewer.py
"""

import os
import subprocess
import sys
from pathlib import Path

def build_exe_for_file(python_file, app_name):
    """Build a single EXE file"""
    print(f"\nBuilding {app_name}...")
    
    # Ensure PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print(f"Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyInstaller"])
    
    # Project path
    project_dir = Path(__file__).parent
    main_file = project_dir / python_file
    
    if not main_file.exists():
        print(f"ERROR: {python_file} not found!")
        return False
    
    # Icon (optional)
    icon_path = None
    if (project_dir / "icon.ico").exists():
        icon_path = str(project_dir / "icon.ico")
    
    # PyInstaller command
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        f"--name={app_name}",
        "--onefile",
        f"--distpath={project_dir}/dist",
        f"--workpath={project_dir}/build_{app_name}",
        f"--specpath={project_dir}/specs",
        "--console",
        "--noupx",
        "--hidden-import=PyQt6",
        "--hidden-import=pandas",
        "--hidden-import=openpyxl",
        "--collect-all=PyQt6",
        str(main_file)
    ]
    
    # Add icon if exists
    if icon_path:
        cmd.insert(-1, f"--icon={icon_path}")
    
    # Run build
    try:
        subprocess.run(cmd, check=True)
        print(f"SUCCESS: {app_name}.exe built successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR building {app_name}: {e}")
        return False

def main():
    """Build all applications"""
    print("\n" + "="*60)
    print("Building Sama Inventory System Applications")
    print("="*60)
    
    project_dir = Path(__file__).parent
    
    # Applications to build
    apps = [
        ("main.py", "SamaInventorySystem"),
        ("advanced_report_viewer.py", "SamaReportViewer")
    ]
    
    results = {}
    
    # Build each application
    for py_file, app_name in apps:
        results[app_name] = build_exe_for_file(py_file, app_name)
    
    # Summary
    print("\n" + "="*60)
    print("Build Summary:")
    print("="*60)
    
    for app_name, success in results.items():
        status = "SUCCESS" if success else "FAILED"
        print(f"{app_name}: {status}")
    
    print(f"\nOutput directory: {project_dir}/dist/")
    print("\nBuilt files:")
    for py_file, app_name in apps:
        exe_path = project_dir / "dist" / f"{app_name}.exe"
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"  - {app_name}.exe ({size_mb:.2f} MB)")
    
    # Return exit code
    success = all(results.values())
    print()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
