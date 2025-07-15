@echo off
echo 🔑 Setting up SSH keys for GitHub...
echo.

REM Run the PowerShell script
powershell -ExecutionPolicy Bypass -File "%~dp0setup_ssh_keys.ps1"

echo.
echo Press any key to exit...
pause >nul 