# سكريبت إنشاء GitHub Release للإصدار 1.2.4
# GitHub Release Creator Script v1.2.4

param(
    [string]$Token = $env:GITHUB_TOKEN
)

# إعدادات الإصدار
$repo = "StrucTech/Sama-Inventory-System"
$tag = "v1.2.4"
$name = "الإصدار 1.2.4 - تحسينات الواجهة والفلاتر"
$zipFile = "sama-inventory-v1.2.4.zip"

# قراءة ملاحظات الإصدار
$releaseNotesFile = "github_release_notes.md"
if (Test-Path $releaseNotesFile) {
    $body = Get-Content $releaseNotesFile -Raw -Encoding UTF8
    Write-Host "✅ تم تحميل ملاحظات الإصدار من $releaseNotesFile" -ForegroundColor Green
} else {
    Write-Host "❌ لم يتم العثور على ملف ملاحظات الإصدار" -ForegroundColor Red
    exit 1
}

# التحقق من وجود الملف المضغوط
if (!(Test-Path $zipFile)) {
    Write-Host "❌ لم يتم العثور على الملف المضغوط: $zipFile" -ForegroundColor Red
    exit 1
}

Write-Host "🚀 بدء إنشاء GitHub Release..." -ForegroundColor Cyan
Write-Host "📦 Repository: $repo" -ForegroundColor White
Write-Host "🏷️ Tag: $tag" -ForegroundColor White
Write-Host "📝 Name: $name" -ForegroundColor White

# إنشاء البيانات للـ API
$releaseData = @{
    tag_name = $tag
    target_commitish = "main"
    name = $name
    body = $body
    draft = $false
    prerelease = $false
} | ConvertTo-Json -Depth 3

Write-Host "📡 إرسال طلب إنشاء Release..." -ForegroundColor Yellow

try {
    # إنشاء Release
    if ($Token) {
        $headers = @{
            "Authorization" = "Bearer $Token"
            "Accept" = "application/vnd.github.v3+json"
            "User-Agent" = "PowerShell-Release-Creator"
        }
        
        $uri = "https://api.github.com/repos/$repo/releases"
        
        $response = Invoke-RestMethod -Uri $uri -Method Post -Headers $headers -Body $releaseData -ContentType "application/json"
        
        Write-Host "✅ تم إنشاء Release بنجاح!" -ForegroundColor Green
        Write-Host "🔗 رابط الإصدار: $($response.html_url)" -ForegroundColor Cyan
        
        # رفع الملف المضغوط
        Write-Host "📤 رفع الملف المضغوط..." -ForegroundColor Yellow
        
        $uploadUrl = $response.upload_url -replace '\{\?name,label\}', "?name=$zipFile"
        $fileBytes = [System.IO.File]::ReadAllBytes((Resolve-Path $zipFile))
        
        $uploadHeaders = @{
            "Authorization" = "Bearer $Token"
            "Content-Type" = "application/zip"
            "Accept" = "application/vnd.github.v3+json"
        }
        
        $uploadResponse = Invoke-RestMethod -Uri $uploadUrl -Method Post -Headers $uploadHeaders -Body $fileBytes
        
        Write-Host "✅ تم رفع الملف المضغوط بنجاح!" -ForegroundColor Green
        Write-Host "📎 رابط التحميل: $($uploadResponse.browser_download_url)" -ForegroundColor Cyan
        
        Write-Host "`n🎉 تم إطلاق الإصدار 1.2.4 بنجاح!" -ForegroundColor Green
        Write-Host "🔗 زيارة الإصدار: $($response.html_url)" -ForegroundColor White
        
    } else {
        Write-Host "❌ لم يتم توفير GitHub Token" -ForegroundColor Red
        Write-Host "💡 استخدم: `$env:GITHUB_TOKEN = 'your_token'" -ForegroundColor Yellow
        Write-Host "💡 أو: .\create_github_release.ps1 -Token 'your_token'" -ForegroundColor Yellow
        Write-Host "`n🌐 أو قم بإنشاء Release يدوياً على:" -ForegroundColor Cyan
        Write-Host "https://github.com/$repo/releases/new" -ForegroundColor White
        Write-Host "`n📋 معلومات الإصدار:" -ForegroundColor Yellow
        Write-Host "Tag: $tag" -ForegroundColor White
        Write-Host "Title: $name" -ForegroundColor White
        Write-Host "File: $zipFile" -ForegroundColor White
    }
    
} catch {
    Write-Host "❌ خطأ في إنشاء Release: $($_.Exception.Message)" -ForegroundColor Red
    
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "📄 تفاصيل الخطأ: $responseBody" -ForegroundColor Red
    }
    
    Write-Host "`n🌐 قم بإنشاء Release يدوياً على:" -ForegroundColor Cyan
    Write-Host "https://github.com/$repo/releases/new" -ForegroundColor White
}

Write-Host "`n📊 ملخص الإصدار:" -ForegroundColor Cyan
Write-Host "- الإصدار: v1.2.4" -ForegroundColor White
Write-Host "- الحجم: 0.16 MB" -ForegroundColor White
Write-Host "- الملفات: 195 ملف محدث" -ForegroundColor White
Write-Host "- النوع: إصدار مستقر" -ForegroundColor White