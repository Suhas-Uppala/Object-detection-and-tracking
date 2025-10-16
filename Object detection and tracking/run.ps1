# Quick Start Script for Object Detection and Tracking (PowerShell)
# This script helps you run the application easily

function Show-Menu {
    Clear-Host
    Write-Host ""
    Write-Host "========================================"
    Write-Host "  Object Detection and Tracking"
    Write-Host "========================================"
    Write-Host ""
    Write-Host "[1] Run with video file (los_angeles.mp4)"
    Write-Host "[2] Run with webcam"
    Write-Host "[3] Test setup"
    Write-Host "[4] Download model files"
    Write-Host "[5] View usage guide"
    Write-Host "[6] Exit"
    Write-Host ""
}

function Start-WithVideo {
    Write-Host ""
    Write-Host "Starting with video file..." -ForegroundColor Green
    Write-Host ""
    python object_tracking.py
}

function Start-WithWebcam {
    Write-Host ""
    Write-Host "Starting with webcam..." -ForegroundColor Green
    Write-Host "NOTE: This will temporarily modify object_tracking.py to use webcam" -ForegroundColor Yellow
    Write-Host ""
    $confirm = Read-Host "Continue? (y/n)"
    
    if ($confirm -eq 'y' -or $confirm -eq 'Y') {
        # Backup original file
        Copy-Item "object_tracking.py" "object_tracking.py.backup"
        
        # Modify to use webcam
        $content = Get-Content "object_tracking.py" -Raw
        $content = $content -replace 'VIDEO_SOURCE = "[^"]*"', 'VIDEO_SOURCE = 0'
        Set-Content "object_tracking.py" $content
        
        # Run
        python object_tracking.py
        
        # Restore original
        Move-Item "object_tracking.py.backup" "object_tracking.py" -Force
        Write-Host ""
        Write-Host "Original file restored" -ForegroundColor Green
    }
}

function Test-Setup {
    Write-Host ""
    Write-Host "Running setup verification..." -ForegroundColor Green
    Write-Host ""
    python test_setup.py
    Write-Host ""
    Read-Host "Press Enter to continue"
}

function Download-Models {
    Write-Host ""
    Write-Host "Downloading model files..." -ForegroundColor Green
    Write-Host "This may take several minutes..." -ForegroundColor Yellow
    Write-Host ""
    python download_models.py
    Write-Host ""
    Read-Host "Press Enter to continue"
}

function Show-UsageGuide {
    Write-Host ""
    Write-Host "Opening usage guide..." -ForegroundColor Green
    
    if (Test-Path "USAGE_GUIDE.md") {
        notepad "USAGE_GUIDE.md"
    } else {
        Write-Host "Usage guide not found!" -ForegroundColor Red
    }
}

# Main loop
do {
    Show-Menu
    $choice = Read-Host "Enter your choice (1-6)"
    
    switch ($choice) {
        '1' { Start-WithVideo }
        '2' { Start-WithWebcam }
        '3' { Test-Setup }
        '4' { Download-Models }
        '5' { Show-UsageGuide }
        '6' { 
            Write-Host ""
            Write-Host "Thank you for using Object Detection and Tracking!" -ForegroundColor Green
            Write-Host ""
            exit 
        }
        default {
            Write-Host ""
            Write-Host "Invalid choice. Please try again." -ForegroundColor Red
            Start-Sleep -Seconds 2
        }
    }
} while ($true)
