# -*- coding: utf-8 -*-
# سكريبت الإطلاق السريع - PowerShell Version

Write-Host ""
Write-Host "╔════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  Sama Inventory System - Release Script        ║" -ForegroundColor Cyan
Write-Host "║  سكريبت الإطلاق السريع                        ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# الحصول على مسار السكريبت
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

Write-Host "📁 المجلد: $scriptDir" -ForegroundColor Blue
Write-Host ""

# 1. فحص Python
Write-Host "1️⃣  فحص Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python مثبت: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python غير مثبت!" -ForegroundColor Red
    exit 1
}
Write-Host ""

# 2. اختبار التطبيق (اختياري)
Write-Host "2️⃣  اختبار التطبيق..." -ForegroundColor Yellow
$testApp = Read-Host "هل تريد تشغيل البرنامج؟ (y/n)"
if ($testApp -eq "y") {
    Write-Host "🚀 تشغيل البرنامج..." -ForegroundColor Green
    Start-Process python -ArgumentList "main.py" -NoNewWindow
    Start-Sleep -Seconds 2
}
Write-Host ""

# 3. تحديث VERSION
Write-Host "3️⃣  تحديث رقم الإصدار..." -ForegroundColor Yellow
$currentVersion = Get-Content VERSION.txt
Write-Host "الإصدار الحالي: $currentVersion" -ForegroundColor Cyan
$newVersion = Read-Host "أدخل الإصدار الجديد (مثال: 1.0.1)"

if ([string]::IsNullOrWhiteSpace($newVersion)) {
    $newVersion = $currentVersion
}

$newVersion | Set-Content VERSION.txt
Write-Host "✅ تم تحديث الإصدار إلى: $newVersion" -ForegroundColor Green
Write-Host ""

# 4. Commit
Write-Host "4️⃣  حفظ التغييرات في Git..." -ForegroundColor Yellow
try {
    git add .
    git commit -m "Release v$newVersion"
    Write-Host "✅ تم حفظ التغييرات" -ForegroundColor Green
} catch {
    Write-Host "⚠️ تحذير: $_" -ForegroundColor Yellow
}
Write-Host ""

# 5. Tag
Write-Host "5️⃣  إنشاء Release Tag..." -ForegroundColor Yellow
try {
    git tag -a "v$newVersion" -m "Release Version $newVersion"
    Write-Host "✅ تم إنشاء Tag: v$newVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ خطأ في إنشاء Tag: $_" -ForegroundColor Red
}
Write-Host ""

# 6. Push
Write-Host "6️⃣  رفع التغييرات إلى GitHub..." -ForegroundColor Yellow
try {
    Write-Host "  → رفع main branch..." -ForegroundColor Cyan
    git push origin main
    
    Write-Host "  → رفع Release tag..." -ForegroundColor Cyan
    git push origin "v$newVersion"
    
    Write-Host "✅ تم الرفع بنجاح" -ForegroundColor Green
} catch {
    Write-Host "❌ خطأ في الرفع: $_" -ForegroundColor Red
    exit 1
}
Write-Host ""

# الخطوات التالية
Write-Host "╔════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                ✅ تم بنجاح!                     ║" -ForegroundColor Green
Write-Host "╠════════════════════════════════════════════════╣" -ForegroundColor Green
Write-Host "║  الخطوات التالية:                            ║" -ForegroundColor Green
Write-Host "║                                                ║" -ForegroundColor Green
Write-Host "║  1. اذهب إلى GitHub Actions:                  ║" -ForegroundColor Green
Write-Host "║     github.com/StrucTech/Sama-Inventory...  ║" -ForegroundColor Green
Write-Host "║     /actions                                  ║" -ForegroundColor Green
Write-Host "║                                                ║" -ForegroundColor Green
Write-Host "║  2. انتظر البناء (5-10 دقائق)                 ║" -ForegroundColor Green
Write-Host "║                                                ║" -ForegroundColor Green
Write-Host "║  3. اذهب إلى Releases:                         ║" -ForegroundColor Green
Write-Host "║     github.com/StrucTech/Sama-Inventory...  ║" -ForegroundColor Green
Write-Host "║     /releases                                  ║" -ForegroundColor Green
Write-Host "║                                                ║" -ForegroundColor Green
Write-Host "║  4. احتفل! 🎉                                  ║" -ForegroundColor Green
Write-Host "║                                                ║" -ForegroundColor Green
Write-Host "║  رقم الإصدار: v$newVersion" -ForegroundColor Yellow
Write-Host "╚════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Read-Host "اضغط أي مفتاح للخروج"
