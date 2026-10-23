@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0"
echo === Diagnostika LuffyGame ===
echo.
echo [1] Gde Python?
where py 2>nul
where python 2>nul
where python3 2>nul
echo.
echo [2] Versiya:
py -3 -c "import sys; print(sys.version)" 2>nul || python -c "import sys; print(sys.version)" 2>nul || echo Python ne nayden
echo.
echo [3] pygame:
py -3 -c "import pygame; print('pygame', pygame.version.ver)" 2>nul || python -c "import pygame; print('pygame', pygame.version.ver)" 2>nul || echo pygame NE ustanovlen
echo.
echo [4] Fajly:
dir /b main.py questions.py 2>nul
echo.
echo Esli pygame ne ustanovlen:
echo   py -3 -m pip install pygame
echo   ili
echo   python -m pip install pygame
echo.
pause
