#!/usr/bin/env python3
"""
سكريبت إطلاق الإصدار 1.2.4
"""

import os
import json
import zipfile
import shutil
from datetime import datetime
import subprocess

def create_release_package():
    """إنشاء حزمة الإصدار"""
    
    print("📦 إنشاء حزمة الإصدار 1.2.4...")
    
    # إنشاء مجلد الإصدار
    release_dir = "release_v1.2.4"
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    os.makedirs(release_dir)
    
    # قائمة الملفات المطلوبة للإصدار
    files_to_include = [
        # الملفات الرئيسية
        "main_with_auth.py",
        "requirements.txt",
        "README.md",
        "CHANGELOG_v1.2.4.md",
        "update_info.json",
        
        # ملفات النظام
        "auto_updater.py",
        "setup_wizard.py",
        
        # مجلدات النظام
        "gui/",
        "sheets/",
        "config/",
        
        # ملفات الاختبار والتوثيق
        "test_filter_restrictions_simple.py",
        "demo_filter_restrictions.py",
        "UI_UPDATES_SUMMARY.md",
        
        # نظام الفلاتر الجديد
        "new_activity_filter_system.py",
    ]
    
    # نسخ الملفات
    for file_path in files_to_include:
        src_path = file_path
        dest_path = os.path.join(release_dir, file_path)
        
        if os.path.isdir(src_path):
            # نسخ المجلد
            shutil.copytree(src_path, dest_path, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            print(f"📁 تم نسخ المجلد: {file_path}")
        elif os.path.isfile(src_path):
            # نسخ الملف
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy2(src_path, dest_path)
            print(f"📄 تم نسخ الملف: {file_path}")
        else:
            print(f"⚠️ لم يتم العثور على: {file_path}")
    
    # إنشاء ملف معلومات الإصدار
    release_info = {
        "version": "1.2.4",
        "release_date": datetime.now().isoformat(),
        "build_type": "stable",
        "features": [
            "تحسينات واجهة المستخدم",
            "نظام فلاتر محسن",
            "رسائل تشويقية للميزات القادمة",
            "إصلاحات شاملة للفلاتر",
            "تحسينات الأمان والأداء"
        ],
        "requirements": [
            "Python 3.7+",
            "tkinter (مدمج مع Python)",
            "Google Sheets API",
            "اتصال بالإنترنت"
        ]
    }
    
    with open(os.path.join(release_dir, "release_info.json"), 'w', encoding='utf-8') as f:
        json.dump(release_info, f, ensure_ascii=False, indent=2)
    
    print("✅ تم إنشاء ملف معلومات الإصدار")
    
    return release_dir

def create_zip_archive(release_dir):
    """إنشاء ملف مضغوط للإصدار"""
    
    zip_filename = "sama-inventory-v1.2.4.zip"
    
    print(f"🗜️ إنشاء الملف المضغوط: {zip_filename}")
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(release_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, release_dir)
                zipf.write(file_path, arc_name)
                print(f"   ✅ {arc_name}")
    
    # حساب حجم الملف
    size_mb = os.path.getsize(zip_filename) / (1024 * 1024)
    print(f"📊 حجم الملف: {size_mb:.2f} MB")
    
    return zip_filename

def create_release_notes():
    """إنشاء ملاحظات الإصدار لـ GitHub"""
    
    release_notes = """# 🎉 الإصدار 1.2.4 - تحسينات الواجهة والفلاتر

## ✨ الميزات الجديدة:

### 🎯 تحسينات واجهة المستخدم:
- 🔍 **زر "بحث بالفلاتر" محسن**: اسم أوضح وتفعيل ذكي
- 📊 **ميزة "تحليل ورؤى البيانات"**: رسالة تشويقية للإصدارات القادمة
- ⚡ **تحميل ذكي**: الأزرار تتفعل عند اكتمال تحميل البيانات

### 🔒 نظام فلاتر محسن:
- 👥 **قيود وصول للمستخدمين العاديين**: كل مستخدم يرى بيانات مشروعه فقط
- 🎨 **مؤشرات بصرية**: إشارات واضحة للفلاتر المقيدة
- 🛡️ **أمان معزز**: منع تسرب البيانات بين المشاريع

## 🐛 الإصلاحات:
- ✅ **حل مشكلة الفلاتر**: إصلاح شامل لعدم تأثير الفلاتر على البيانات
- 🔧 **تحسين الأداء**: استجابة أسرع وأكثر استقراراً
- 🎯 **دقة العرض**: ضمان عرض البيانات الصحيحة فقط

## 📥 كيفية التحديث:
1. **تلقائياً**: انتظر رسالة التحديث (خلال 24 ساعة)
2. **يدوياً**: حمّل الملف المضغوط أدناه

## 🚀 ما الجديد:
- واجهة أبسط وأوضح
- أمان محسن للبيانات
- رسائل تشويقية للميزات القادمة
- نظام فلاتر أكثر دقة

## 🎯 الميزات القادمة:
- 📊 تحليل ورؤى البيانات متقدمة
- 📈 تقارير تفصيلية قابلة للتخصيص
- 🔔 إشعارات ذكية للمخزون
- 📱 واجهة محسنة للأجهزة المختلفة

---

**📋 متطلبات التشغيل:**
- Python 3.7+
- Google Sheets API
- اتصال بالإنترنت

**🏆 إصدار مستقر جاهز للإنتاج**
"""
    
    with open("github_release_notes.md", 'w', encoding='utf-8') as f:
        f.write(release_notes)
    
    print("📝 تم إنشاء ملاحظات GitHub")
    return "github_release_notes.md"

def generate_git_commands():
    """إنشاء الأوامر المطلوبة لـ Git و GitHub"""
    
    commands = [
        "# أوامر Git لإطلاق الإصدار",
        "",
        "# 1. إضافة جميع التغييرات",
        "git add .",
        "",
        "# 2. إنشاء commit للإصدار",
        'git commit -m "إصدار 1.2.4: تحسينات الواجهة والفلاتر"',
        "",
        "# 3. إنشاء tag للإصدار", 
        "git tag v1.2.4",
        "",
        "# 4. رفع التغييرات",
        "git push origin main",
        "git push origin v1.2.4",
        "",
        "# 5. إنشاء Release على GitHub:",
        "# - اذهب إلى GitHub Repository",
        "# - اضغط 'Releases' ثم 'Create a new release'",
        "# - اختر Tag: v1.2.4",
        "# - العنوان: 'الإصدار 1.2.4 - تحسينات الواجهة والفلاتر'",
        "# - انسخ محتويات github_release_notes.md",
        "# - ارفع ملف sama-inventory-v1.2.4.zip",
        "# - اضغط 'Publish release'",
    ]
    
    with open("git_release_commands.txt", 'w', encoding='utf-8') as f:
        f.write('\n'.join(commands))
    
    print("📋 تم إنشاء ملف أوامر Git")
    return commands

def main():
    """الدالة الرئيسية لإطلاق الإصدار"""
    
    print("🚀 بدء عملية إطلاق الإصدار 1.2.4")
    print("=" * 50)
    
    try:
        # 1. إنشاء حزمة الإصدار
        release_dir = create_release_package()
        print(f"\n✅ تم إنشاء حزمة الإصدار في: {release_dir}")
        
        # 2. إنشاء الملف المضغوط
        zip_file = create_zip_archive(release_dir)
        print(f"\n✅ تم إنشاء الملف المضغوط: {zip_file}")
        
        # 3. إنشاء ملاحظات الإصدار
        notes_file = create_release_notes()
        print(f"\n✅ تم إنشاء ملاحظات الإصدار: {notes_file}")
        
        # 4. إنشاء أوامر Git
        git_commands = generate_git_commands()
        print(f"\n✅ تم إنشاء أوامر Git")
        
        # 5. ملخص الإصدار
        print("\n" + "=" * 50)
        print("🎉 تم الانتهاء من إعداد الإصدار 1.2.4!")
        print("\n📦 الملفات المُنشأة:")
        print(f"   📁 {release_dir}/ - حزمة الإصدار")
        print(f"   🗜️ {zip_file} - الملف المضغوط")
        print(f"   📝 {notes_file} - ملاحظات GitHub")
        print(f"   📋 git_release_commands.txt - أوامر Git")
        
        print("\n🚀 الخطوات التالية:")
        print("   1. راجع الملفات المُنشأة")
        print("   2. شغّل أوامر Git المذكورة في git_release_commands.txt")
        print("   3. أنشئ Release على GitHub")
        print("   4. ارفع الملف المضغوط")
        print("   5. انشر الإعلان!")
        
        print(f"\n✨ الإصدار 1.2.4 جاهز للإطلاق!")
        
    except Exception as e:
        print(f"\n❌ خطأ في إعداد الإصدار: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()