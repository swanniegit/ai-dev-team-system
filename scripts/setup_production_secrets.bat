@echo off
REM Generate secure secrets for Agentic Agile System production deployment
REM This script creates secure secrets using PowerShell

echo 🔐 Agentic Agile System - Security Keys Generator
echo ==================================================
echo.

REM Generate secrets using PowerShell
powershell -Command "
$jwt_secret = [System.Web.Security.Membership]::GeneratePassword(64, 16)
$db_password = [System.Web.Security.Membership]::GeneratePassword(20, 5)
$github_secret = [System.Web.Security.Membership]::GeneratePassword(40, 10)
$gitlab_secret = [System.Web.Security.Membership]::GeneratePassword(40, 10)
$api_key = [System.Web.Security.Membership]::GeneratePassword(32, 8)

Write-Host '🔑 Generated Secrets (store these securely!):' -ForegroundColor Green
Write-Host '------------------------------------------------' -ForegroundColor Yellow
Write-Host 'SECRET_KEY=' -NoNewline; Write-Host $jwt_secret -ForegroundColor Cyan
Write-Host 'DATABASE_PASSWORD=' -NoNewline; Write-Host $db_password -ForegroundColor Cyan
Write-Host 'GITHUB_WEBHOOK_SECRET=' -NoNewline; Write-Host $github_secret -ForegroundColor Cyan
Write-Host 'GITLAB_WEBHOOK_TOKEN=' -NoNewline; Write-Host $gitlab_secret -ForegroundColor Cyan
Write-Host 'API_ENCRYPTION_KEY=' -NoNewline; Write-Host $api_key -ForegroundColor Cyan
Write-Host ''

$env_content = @'
# Agentic Agile System - Production Secrets
# CRITICAL: Keep these secrets secure and never commit to version control!

SECRET_KEY=' + $jwt_secret + '
DATABASE_PASSWORD=' + $db_password + '
GITHUB_WEBHOOK_SECRET=' + $github_secret + '
GITLAB_WEBHOOK_TOKEN=' + $gitlab_secret + '
API_ENCRYPTION_KEY=' + $api_key + '
'@

$env_content | Out-File -FilePath '.env.secrets' -Encoding UTF8

Write-Host '💾 Secrets saved to: .env.secrets' -ForegroundColor Green
Write-Host ''
Write-Host '⚠️  SECURITY WARNINGS:' -ForegroundColor Red
Write-Host '   1. Copy these secrets to your secure environment'
Write-Host '   2. Delete the .env.secrets file after copying'
Write-Host '   3. Never commit these secrets to version control'
Write-Host '   4. Rotate these secrets regularly'
"

echo.
echo 🚀 Next steps:
echo    1. Update your production environment variables
echo    2. Restart your services  
echo    3. Test authentication and webhooks

pause