@echo off
REM Setup scheduled updates for Agentic Agile System
REM Run this script as Administrator

echo ========================================
echo Agentic Agile System - Scheduled Updates
echo ========================================
echo.

REM Get the current directory
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."
set "UPDATE_SCRIPT=%SCRIPT_DIR%update_system.py"

echo Project Root: %PROJECT_ROOT%
echo Update Script: %UPDATE_SCRIPT%
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script must be run as Administrator
    echo Right-click and select "Run as administrator"
    pause
    exit /b 1
)

echo Creating scheduled tasks...
echo.

REM Create weekly system health check (Sundays at 2 AM)
echo Creating weekly system health check...
schtasks /create /tn "AgenticAgileSystem-WeeklyHealthCheck" /tr "python %UPDATE_SCRIPT%" /sc weekly /d SUN /st 02:00 /ru SYSTEM /f

REM Create daily memory backup check (Daily at 3 AM)
echo Creating daily memory backup check...
schtasks /create /tn "AgenticAgileSystem-DailyBackupCheck" /tr "python %SCRIPT_DIR%backup_memory.py" /sc daily /st 03:00 /ru SYSTEM /f

REM Create monthly dependency update check (1st of month at 4 AM)
echo Creating monthly dependency update check...
schtasks /create /tn "AgenticAgileSystem-MonthlyDependencyCheck" /tr "python %UPDATE_SCRIPT% --dependencies-only" /sc monthly /mo 1 /st 04:00 /ru SYSTEM /f

echo.
echo ========================================
echo Scheduled Tasks Created Successfully!
echo ========================================
echo.
echo Tasks created:
echo - Weekly Health Check: Sundays at 2:00 AM
echo - Daily Backup Check: Daily at 3:00 AM  
echo - Monthly Dependency Check: 1st of month at 4:00 AM
echo.
echo To view tasks: schtasks /query /tn "AgenticAgileSystem*"
echo To delete tasks: schtasks /delete /tn "AgenticAgileSystem-*" /f
echo.
pause 