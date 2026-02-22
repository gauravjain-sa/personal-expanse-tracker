@echo off
:: Automated Build Script for Expense Tracker
:: This script builds the executable and creates the installer
:: Usage: Just double-click or run from command line

echo ========================================
echo Expense Tracker - Automated Build
echo ========================================
echo.

:: Step 1: Check Python
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo.

:: Step 2: Build executable
echo [2/4] Building executable with PyInstaller...
echo This may take 2-3 minutes...
python build.py
if errorlevel 1 (
    echo ERROR: Build failed!
    echo Check the error messages above.
    pause
    exit /b 1
)
echo Build completed successfully!
echo.

:: Step 3: Pause for testing (optional)
echo [3/4] Build complete! You can now test the application.
echo.
echo The executable is located at: dist\ExpenseTracker\ExpenseTracker.exe
echo.
choice /C YN /M "Do you want to test the application before creating the installer"
if errorlevel 2 goto create_installer
if errorlevel 1 (
    echo.
    echo Launching application for testing...
    echo Close the application when you're done testing.
    echo.
    start "" "dist\ExpenseTracker\ExpenseTracker.exe"
    pause
)

:create_installer
echo.
echo [4/4] Creating installer with Inno Setup...

:: Check if Inno Setup is installed (check both common locations)
set INNO_PATH=
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    set INNO_PATH="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
) else if exist "C:\Program Files\Inno Setup 6\ISCC.exe" (
    set INNO_PATH="C:\Program Files\Inno Setup 6\ISCC.exe"
)

if not defined INNO_PATH (
    echo WARNING: Inno Setup not found!
    echo.
    echo Please install Inno Setup 6 from: https://jrsoftware.org/isdl.php
    echo Then run this script again.
    echo.
    echo You can still distribute the folder: dist\ExpenseTracker\
    pause
    exit /b 0
)

%INNO_PATH% installer.iss
if errorlevel 1 (
    echo ERROR: Installer creation failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo BUILD COMPLETED SUCCESSFULLY!
echo ========================================
echo.
echo Executable: dist\ExpenseTracker\ExpenseTracker.exe
echo Installer:  installer_output\ExpenseTracker_Setup_v1.0.0.exe
echo.
echo The installer is ready to distribute to users!
echo The installer is 100%% self-contained - users need nothing else.
echo.

:: Ask if user wants to open output folder
choice /C YN /M "Do you want to open the output folder"
if errorlevel 2 goto end
if errorlevel 1 (
    if not exist "installer_output" mkdir installer_output
    start "" "installer_output"
)

:end
echo.
echo Done! Press any key to exit.
pause >nul
