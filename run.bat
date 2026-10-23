@echo off
REM Korotkiy zapusk bez proverok (esli Python i pygame uzhe est)
cd /d "%~dp0"
py -3 main.py 2>nul || python main.py 2>nul || python3 main.py
if errorlevel 1 (
    echo.
    echo Ne udalos' zapustit'. Ispol'zuyte start.bat
    pause
)
