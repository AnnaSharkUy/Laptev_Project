# -*- coding: utf-8 -*-
"""
One-Punch Man: Географический Герой
Игра для подготовки к ВПР по географии 6 класс
Авторы: Владимир Лаптев, Дима Пикулин, Ярослав Костюков
Куратор проекта: Воронцов Николай Витальевич
"""

import tkinter as tk
from tkinter import messagebox, font
import random
import os
import sys

# ==================== ПУТИ К ПАПКАМ ====================
def get_base_dir():
    """Папка, где лежит программа (работает и из .py, и из .exe)"""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_base_dir()
MUSIC_DIR = os.path.join(BASE_DIR, "music")
ANIM_DIR = os.path.join(BASE_DIR, "animation")

# ==================== ЗВУК (опционально) ====================
SOUND_AVAILABLE = False
try:
    import pygame
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    SOUND_AVAILABLE = True
except Exception:
    SOUND_AVAILABLE = False

def play_music(filename, loop=True):
    """Играет музыку из папки music/. Если файла нет — тихо."""
    if not SOUND_AVAILABLE:
        return
    path = os.path.join(MUSIC_DIR, filename)
    if not os.path.isfile(path):
        for ext in (".mp3", ".wav", ".ogg"):
            alt = os.path.join(MUSIC_DIR, os.path.splitext(filename)[0] + ext)
            if os.path.isfile(alt):
                path = alt
                break
        else:
            return
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1 if loop else 0)
    except Exception:
        pass

def stop_music():
    if SOUND_AVAILABLE:
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass

def play_sound(filename):
    """Короткий звук (удар и т.п.)"""
    if not SOUND_AVAILABLE:
        return
    path = os.path.join(MUSIC_DIR, filename)
    if not os.path.isfile(path):
        for ext in (".wav", ".ogg", ".mp3"):
            alt = os.path.join(MUSIC_DIR, os.path.splitext(filename)[0] + ext)
            if os.path.isfile(alt):
                path = alt
                break
        else:
            return
    try:
        sound = pygame.mixer.Sound(path)
        sound.set_volume(0.7)
        sound.play()
    except Exception:
        pass

# ==================== КАРТИНКИ (опционально) ====================
def load_image(filename, max_size=(300, 300)):
    """Загружает картинку из animation/. Возвращает PhotoImage или None."""
    path = os.path.join(ANIM_DIR, filename)
    if not os.path.isfile(path):
        for ext in (".png", ".gif", ".jpg", ".jpeg"):
            alt = os.path.join(ANIM_DIR, os.path.splitext(filename)[0] + ext)
            if os.path.isfile(alt):
                path = alt
                break
        else:
            return None
    try:
        img = tk.PhotoImage(file=path)
        w, h = img.width(), img.height()
        mw, mh = max_size
        if w > mw or h > mh:
            factor = max(w // mw, h // mh, 1)
            img = img.subsample(factor, factor)
        return img
    except Exception:
        return None
