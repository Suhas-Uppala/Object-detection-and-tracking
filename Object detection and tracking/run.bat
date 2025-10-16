@echo off
REM Quick Start Script for Object Detection and Tracking
REM This script helps you run the application easily

echo.
echo ========================================
echo   Object Detection and Tracking
echo ========================================
echo.

:menu
echo Choose an option:
echo.
echo [1] Run with video file (los_angeles.mp4)
echo [2] Run with webcam
echo [3] Test setup
echo [4] Download model files
echo [5] Exit
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto video
if "%choice%"=="2" goto webcam
if "%choice%"=="3" goto test
if "%choice%"=="4" goto download
if "%choice%"=="5" goto end

echo Invalid choice. Please try again.
echo.
goto menu

:video
echo.
echo Starting with video file...
echo.
python object_tracking.py
goto end

:webcam
echo.
echo Starting with webcam...
echo NOTE: This will modify object_tracking.py to use webcam
echo.
set /p confirm="Continue? (y/n): "
if /i not "%confirm%"=="y" goto menu

REM Create temporary script to use webcam
python -c "import re; content = open('object_tracking.py', 'r').read(); content = re.sub(r'VIDEO_SOURCE = \"[^\"]*\"', 'VIDEO_SOURCE = 0', content); open('object_tracking.py', 'w').write(content)"
python object_tracking.py
goto end

:test
echo.
echo Running setup verification...
echo.
python test_setup.py
pause
goto menu

:download
echo.
echo Downloading model files...
echo This may take several minutes...
echo.
python download_models.py
pause
goto menu

:end
echo.
echo Thank you for using Object Detection and Tracking!
echo.
pause
