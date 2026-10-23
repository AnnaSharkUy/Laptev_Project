@echo off
setlocal EnableExtensions
chcp 65001 >nul 2>&1
title LuffyGame - Zapusk
cd /d "%~dp0"

echo ============================================
echo   LuffyGame - Geografiya s Luffy
echo   Podgotovka k VPR 5 klass
echo ============================================
echo.

REM --- Ищем рабочий Python: py, python, python3 ---
set "PY="
where py >nul 2>&1
if %errorlevel% equ 0 (
    py -3 -c "import sys; print(sys.version)" >nul 2>&1
    if %errorlevel% equ 0 set "PY=py -3"
)
if not defined PY (
    where python >nul 2>&1
    if %errorlevel% equ 0 (
        python -c "import sys; print(sys.version)" >nul 2>&1
        if %errorlevel% equ 0 set "PY=python"
    )
)
if not defined PY (
    where python3 >nul 2>&1
    if %errorlevel% equ 0 (
        python3 -c "import sys; print(sys.version)" >nul 2>&1
        if %errorlevel% equ 0 set "PY=python3"
    )
)

if not defined PY (
    echo [OSHIBKA] Python 3 ne nayden!
    echo.
    echo 1. Skachayte Python 3: https://www.python.org/downloads/
    echo 2. Pri ustanovke OB'YAZATEL'NO postav'te galochku:
    echo    "Add python.exe to PATH"
    echo 3. Posle ustanovki PEREZAGRUZITE komp'yuter ili otkroyte
    echo    novoe okno komandnoy stroki.
    echo 4. Zapustite start.bat snova.
    echo.
    echo Esli Python uzhe ustanovlen, poprobuyte v komandnoy stroke:
    echo    py -3 main.py
    echo.
    pause
    exit /b 1
)

echo Nayden Python: %PY%
%PY% -c "import sys; print('  Versiya:', sys.version.split()[0])"
echo.

REM --- Проверка / установка pygame ---
echo Proveryayu pygame...
%PY% -c "import pygame" >nul 2>&1
if %errorlevel% neq 0 (
    echo pygame ne ustanovlen. Ustanavlivayu...
    echo.
    %PY% -m pip install --upgrade pip
    %PY% -m pip install pygame
    if %errorlevel% neq 0 (
        echo.
        echo [OSHIBKA] Ne udalos' ustanovit' pygame.
        echo Poprobuyte vruchnuyu v komandnoy stroke:
        echo    %PY% -m pip install pygame
        echo.
        pause
        exit /b 1
    )
    echo.
    echo pygame uspeshno ustanovlen.
) else (
    echo pygame OK.
)

echo.
echo Zapuskayu igru...
echo --------------------------------------------
%PY% main.py
set ERR=%errorlevel%
echo --------------------------------------------

if %ERR% neq 0 (
    echo.
    echo [OSHIBKA] Igra zavershilas' s kodom %ERR%.
    echo.
    echo Chasto byvaet:
    echo  - net pygame  -^>  %PY% -m pip install pygame
    echo  - oshibka v kode / shriftakh
    echo  - problema so zvukom  (v main.py zvuk otklyuchaetsya sam)
    echo.
    echo Zapustite iz komandnoy stroki, chtoby uvidet' polnyy tekst oshibki:
    echo    cd /d "%~dp0"
    echo    %PY% main.py
    echo.
)

echo.
pause
endlocal
