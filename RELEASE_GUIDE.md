# 🚀 دليل إطلاق Release على GitHub

## الخطوات لإطلاق Release جديد

### 1️⃣ التحضير المحلي

```bash
# تحديث requirements.txt
pip install -r requirements.txt

# اختبار التطبيق
python main.py
```

### 2️⃣ بناء ملف EXE محلياً (اختياري للاختبار)

```bash
python build_exe.py
```

سيتم إنشاء الملف في: `dist/SamaInventorySystem.exe`

### 3️⃣ إنشاء Release على GitHub

#### الطريقة الأولى: عبر Git Commands

```bash
# 1. Commit التغييرات
git add .
git commit -m "Release v1.0.0"

# 2. إنشاء Tag
git tag -a v1.0.0 -m "Release Version 1.0.0"

# 3. Push إلى GitHub
git push origin main
git push origin v1.0.0
```

#### الطريقة الثانية: عبر GitHub Web Interface

1. اذهب إلى: https://github.com/StrucTech/Sama-Inventory-System/releases
2. اضغط على "Create a new release"
3. اختر tag جديد (مثل v1.0.0)
4. أدخل عنوان Release
5. أضف وصف Release
6. اضغط "Publish release"

### 4️⃣ الـ Automated Build (GitHub Actions)

عند إنشاء tag جديد:
- GitHub Actions سيبني ملف EXE تلقائياً
- سيرفعه إلى Release

**ملاحظة:** تأكد من أن `.github/workflows/build-release.yml` موجود

### 📋 نسخة Naming Convention

```
v1.0.0    → Release الأول
v1.0.1    → Bug fix
v1.1.0    → Feature جديد
v2.0.0    → Major update
```

## 🔍 التحقق من Release

1. اذهب إلى: https://github.com/StrucTech/Sama-Inventory-System/releases
2. تحقق من وجود `SamaInventorySystem.exe`
3. المستخدمون يمكنهم تحميل الملف مباشرة

## 📝 Release Notes Template

```markdown
# Sama Inventory System v1.0.0

## ✨ المميزات الجديدة
- [ ] ميزة 1
- [ ] ميزة 2

## 🐛 إصلاحات الأخطاء
- [ ] إصلاح الخطأ 1
- [ ] إصلاح الخطأ 2

## 🔄 التحديثات
- تم تحديث ...

## ⚠️ ملاحظات
- ...

## 📥 التحميل
قم بتحميل `SamaInventorySystem.exe` وتشغيله مباشرة!
```

## 🛠️ المتطلبات

- Git مثبت على النظام
- حساب GitHub مع إذونات Push و Release
- Python 3.11+ (للبناء المحلي)

## ✅ Checklist قبل Release

- [ ] تم اختبار التطبيق
- [ ] تم تحديث VERSION في الكود
- [ ] تم إضافة Release Notes
- [ ] تم Commit جميع التغييرات
- [ ] تم إنشاء Git Tag
- [ ] تم Push إلى GitHub

## 🆘 استكشاف الأخطاء

### خطأ: "workflow not found"
- تأكد من وجود `.github/workflows/build-release.yml`
- تأكد من أن Path صحيح

### خطأ: "PyInstaller failed"
- تأكد من تثبيت جميع المتطلبات
- تجربة: `pip install -r requirements.txt --force-reinstall`

### EXE لا يعمل
- قد تحتاج لتثبيت: Microsoft Visual C++ Redistributable
