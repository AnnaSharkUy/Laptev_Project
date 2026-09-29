@echo off
chcp 65001 >nul
title One-Punch Man: Географический Герой
echo Запуск игры...
python "OnePunch_Geography_Game.py"
if errorlevel 1 (
    echo.
    echo ========================================
    echo  Ошибка: Python не найден!
    echo  Установите Python с python.org
    echo  и поставьте галочку "Add to PATH"
    echo ========================================
    pause
)
