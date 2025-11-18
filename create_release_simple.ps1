# GitHub Release Creator Script v1.2.4
# Creates GitHub Release for Sama Inventory System

param(
    [string]$Token = $env:GITHUB_TOKEN
)

# Release settings
$repo = "StrucTech/Sama-Inventory-System"
$tag = "v1.2.4"
$name = "Release 1.2.4 - UI and Filter Improvements"
$zipFile = "sama-inventory-v1.2.4.zip"

# Read release notes
$releaseNotesFile = "github_release_notes.md"
if (Test-Path $releaseNotesFile) {
    $body = Get-Content $releaseNotesFile -Raw -Encoding UTF8
    Write-Host "Release notes loaded from $releaseNotesFile" -ForegroundColor Green
} else {
    Write-Host "Release notes file not found" -ForegroundColor Red
    exit 1
}

# Check zip file exists
if (!(Test-Path $zipFile)) {
    Write-Host "Zip file not found: $zipFile" -ForegroundColor Red
    exit 1
}

Write-Host "Creating GitHub Release..." -ForegroundColor Cyan
Write-Host "Repository: $repo" -ForegroundColor White
Write-Host "Tag: $tag" -ForegroundColor White
Write-Host "Name: $name" -ForegroundColor White

# Create API data
$releaseData = @{
    tag_name = $tag
    target_commitish = "main"
    name = $name
    body = $body
    draft = $false
    prerelease = $false
} | ConvertTo-Json -Depth 3

Write-Host "Sending API request..." -ForegroundColor Yellow

try {
    if ($Token) {
        $headers = @{
            "Authorization" = "Bearer $Token"
            "Accept" = "application/vnd.github.v3+json"
            "User-Agent" = "PowerShell-Release-Creator"
        }
        
        $uri = "https://api.github.com/repos/$repo/releases"
        
        $response = Invoke-RestMethod -Uri $uri -Method Post -Headers $headers -Body $releaseData -ContentType "application/json"
        
        Write-Host "Release created successfully!" -ForegroundColor Green
        Write-Host "Release URL: $($response.html_url)" -ForegroundColor Cyan
        
        # Upload zip file
        Write-Host "Uploading zip file..." -ForegroundColor Yellow
        
        $uploadUrl = $response.upload_url -replace '\{\?name,label\}', "?name=$zipFile"
        $fileBytes = [System.IO.File]::ReadAllBytes((Resolve-Path $zipFile))
        
        $uploadHeaders = @{
            "Authorization" = "Bearer $Token"
            "Content-Type" = "application/zip"
            "Accept" = "application/vnd.github.v3+json"
        }
        
        $uploadResponse = Invoke-RestMethod -Uri $uploadUrl -Method Post -Headers $uploadHeaders -Body $fileBytes
        
        Write-Host "Zip file uploaded successfully!" -ForegroundColor Green
        Write-Host "Download URL: $($uploadResponse.browser_download_url)" -ForegroundColor Cyan
        
        Write-Host ""
        Write-Host "Release 1.2.4 published successfully!" -ForegroundColor Green
        Write-Host "Visit: $($response.html_url)" -ForegroundColor White
        
    } else {
        Write-Host "No GitHub Token provided" -ForegroundColor Red
        Write-Host "Use: `$env:GITHUB_TOKEN = 'your_token'" -ForegroundColor Yellow
        Write-Host "Or: .\create_github_release.ps1 -Token 'your_token'" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Manual release creation:" -ForegroundColor Cyan
        Write-Host "https://github.com/$repo/releases/new" -ForegroundColor White
        Write-Host ""
        Write-Host "Release info:" -ForegroundColor Yellow
        Write-Host "Tag: $tag" -ForegroundColor White
        Write-Host "Title: $name" -ForegroundColor White
        Write-Host "File: $zipFile" -ForegroundColor White
    }
    
} catch {
    Write-Host "Error creating release: $($_.Exception.Message)" -ForegroundColor Red
    
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "Error details: $responseBody" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "Create release manually at:" -ForegroundColor Cyan
    Write-Host "https://github.com/$repo/releases/new" -ForegroundColor White
}

Write-Host ""
Write-Host "Release Summary:" -ForegroundColor Cyan
Write-Host "- Version: v1.2.4" -ForegroundColor White
Write-Host "- Size: 0.16 MB" -ForegroundColor White
Write-Host "- Files: 195 updated" -ForegroundColor White
Write-Host "- Type: Stable Release" -ForegroundColor White