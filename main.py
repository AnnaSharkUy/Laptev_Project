# -*- coding: utf-8 -*-
"""
LuffyGame — десктопная игра для подготовки к ВПР по географии 5 класса.
Сюжет: команда пиратов One Piece плывёт по четырём морям и Гранд-Лайн,
изучая географию Земли.

Авторы: Владимир Лаптев, Дмитрий Пикулин, Ярослав Костюков
Куратор проекта: Воронцов Николай Витальевич
"""

import sys
import os
import random
import math

# Добавляем папку скрипта в путь
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

try:
    import pygame
except ImportError:
    print("=" * 50)
    print("Pygame не установлен!")
    print("Выполните: pip install pygame")
    print("Или запустите start.bat — он попробует установить сам.")
    print("=" * 50)
    input("Нажмите Enter для выхода...")
    sys.exit(1)

from questions import QUESTIONS, SEAS_ORDER, SEA_DESCRIPTIONS

# ==================== НАСТРОЙКИ ====================
WIDTH, HEIGHT = 1024, 640
FPS = 60
TITLE = "LuffyGame — География с Луффи | ВПР 5 класс"

# Цвета
SEA_BLUE = (30, 100, 180)
SEA_DARK = (15, 50, 100)
SKY = (135, 206, 250)
GOLD = (255, 215, 0)
WHITE = (255, 255, 255)
BLACK = (20, 20, 30)
RED = (220, 50, 50)
GREEN = (50, 180, 80)
ORANGE = (255, 140, 0)
CREAM = (255, 248, 220)
PANEL = (40, 60, 100, 220)

# ==================== ИНИЦИАЛИЗАЦИЯ ====================
# Безопасный старт: звук не обязателен (на некоторых ПК mixer падает)
os.environ.setdefault("SDL_VIDEODRIVER", "")  # пусть SDL сам выберет
SOUND_OK = False

try:
    pygame.init()
except Exception as e:
    print("Ошибка pygame.init():", e)
    input("Нажмите Enter...")
    sys.exit(1)

try:
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    SOUND_OK = True
except Exception:
    # Без звука игра всё равно работает
    SOUND_OK = False
    try:
        pygame.mixer.quit()
    except Exception:
        pass

try:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
except Exception as e:
    print("Не удалось открыть окно игры:", e)
    print("Попробуйте обновить драйверы видеокарты / перезапустить ПК.")
    input("Нажмите Enter...")
    sys.exit(1)

clock = pygame.time.Clock()

# Шрифты (на Windows Segoe UI обычно есть; иначе — стандартный)
def get_font(size, bold=False):
    for name in ("segoeui", "Segoe UI", "arial", "Arial", "tahoma", "Tahoma", "dejavusans"):
        try:
            f = pygame.font.SysFont(name, size, bold=bold)
            if f:
                return f
        except Exception:
            continue
    return pygame.font.Font(None, size)

font_title = get_font(48, True)
font_large = get_font(32, True)
font_med = get_font(24)
font_small = get_font(18)
font_tiny = get_font(14)

# ==================== ЗВУКИ (простые генераторы, если нет файлов) ====================
def make_beep(freq=440, duration=0.1, volume=0.3):
    """Генерирует простой звук без внешних файлов."""
    if not SOUND_OK:
        return None
    sample_rate = 22050
    n_samples = int(sample_rate * duration)
    buf = bytearray()
    for i in range(n_samples):
        t = float(i) / sample_rate
        val = int(32767 * volume * math.sin(2 * math.pi * freq * t) * (1 - t / duration))
        buf += val.to_bytes(2, "little", signed=True)
    try:
        return pygame.mixer.Sound(buffer=bytes(buf))
    except Exception:
        return None

sound_correct = make_beep(660, 0.15, 0.25)
sound_wrong = make_beep(220, 0.25, 0.3)
sound_click = make_beep(440, 0.05, 0.15)
sound_win = make_beep(880, 0.4, 0.3)

def play(s):
    if s and SOUND_OK:
        try:
            s.play()
        except Exception:
            pass

# ==================== ЗАГРУЗКА МУЗЫКИ / АНИМАЦИИ (опционально) ====================
MUSIC_DIR = os.path.join(BASE_DIR, "music")
ANIM_DIR = os.path.join(BASE_DIR, "animation")

def try_load_music():
    if not SOUND_OK or not os.path.isdir(MUSIC_DIR):
        return
    for f in os.listdir(MUSIC_DIR):
        if f.lower().endswith((".mp3", ".ogg", ".wav")):
            try:
                pygame.mixer.music.load(os.path.join(MUSIC_DIR, f))
                pygame.mixer.music.set_volume(0.35)
                pygame.mixer.music.play(-1)
                return
            except Exception:
                pass

# ==================== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ====================
def draw_text(surf, text, font, color, x, y, center=False, max_width=None):
    """Рисует текст, при необходимости переносит строки."""
    if max_width:
        words = text.split()
        lines = []
        current = ""
        for w in words:
            test = current + " " + w if current else w
            if font.size(test)[0] <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = w
        if current:
            lines.append(current)
    else:
        lines = [text]

    for i, line in enumerate(lines):
        img = font.render(line, True, color)
        rect = img.get_rect()
        if center:
            rect.centerx = x
            rect.y = y + i * (font.get_height() + 4)
        else:
            rect.x = x
            rect.y = y + i * (font.get_height() + 4)
        surf.blit(img, rect)
    return len(lines) * (font.get_height() + 4)

def draw_rounded_rect(surf, color, rect, radius=12, border=0, border_color=None):
    pygame.draw.rect(surf, color, rect, border_radius=radius)
    if border and border_color:
        pygame.draw.rect(surf, border_color, rect, border, border_radius=radius)

def button_rect(x, y, w, h):
    return pygame.Rect(x, y, w, h)

# ==================== КЛАССЫ СОСТОЯНИЙ ====================
class GameState:
    MENU = 0
    SEA_SELECT = 1
    QUIZ = 2
    RESULT = 3
    FINAL = 4
    ABOUT = 5

class Game:
    def __init__(self):
        self.state = GameState.MENU
        self.score = 0
        self.total_answered = 0
        self.current_sea_idx = 0
        self.questions_pool = []
        self.current_q = None
        self.selected_option = -1
        self.show_explanation = False
        self.answered = False
        self.correct_count_in_sea = 0
        self.questions_in_sea = 0
        self.ship_x = 100
        self.wave_offset = 0
        self.stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT // 2)) for _ in range(40)]
        self.particles = []
        self.menu_anim = 0
        try_load_music()

    def reset_quiz(self, sea_name=None):
        if sea_name is None:
            sea_name = SEAS_ORDER[self.current_sea_idx]
        self.questions_pool = [q for q in QUESTIONS if q["sea"] == sea_name]
        random.shuffle(self.questions_pool)
        self.questions_in_sea = len(self.questions_pool)
        self.correct_count_in_sea = 0
        self.current_q = None
        self.next_question()
        self.show_explanation = False
        self.answered = False
        self.selected_option = -1

    def next_question(self):
        if self.questions_pool:
            self.current_q = self.questions_pool.pop(0)
            self.answered = False
            self.show_explanation = False
            self.selected_option = -1
            return True
        return False

    def answer(self, idx):
        if self.answered or self.current_q is None:
            return
        self.selected_option = idx
        self.answered = True
        self.total_answered += 1
        if idx == self.current_q["correct"]:
            self.score += 1
            self.correct_count_in_sea += 1
            play(sound_correct)
            self.spawn_particles(GREEN)
        else:
            play(sound_wrong)
            self.spawn_particles(RED)
        self.show_explanation = True

    def spawn_particles(self, color):
        for _ in range(18):
            self.particles.append({
                "x": WIDTH // 2 + random.randint(-80, 80),
                "y": HEIGHT // 2,
                "vx": random.uniform(-4, 4),
                "vy": random.uniform(-6, -1),
                "life": 40,
                "color": color
            })

    def update_particles(self):
        for p in self.particles[:]:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vy"] += 0.15
            p["life"] -= 1
            if p["life"] <= 0:
                self.particles.remove(p)

    # ---------- ОТРИСОВКА ----------
    def draw_background(self, sea=True):
        # Небо
        screen.fill(SKY)
        # Звёзды / облака
        for sx, sy in self.stars:
            pygame.draw.circle(screen, WHITE, (int(sx), int(sy)), 1)

        if sea:
            # Волны
            self.wave_offset = (self.wave_offset + 1.2) % 40
            for i in range(8):
                y = HEIGHT - 180 + i * 22
                points = []
                for x in range(0, WIDTH + 20, 20):
                    dy = math.sin((x + self.wave_offset + i * 15) * 0.04) * 8
                    points.append((x, y + dy))
                if len(points) > 1:
                    pygame.draw.lines(screen, SEA_BLUE if i % 2 == 0 else SEA_DARK, False, points, 3)
            # Море снизу
            pygame.draw.rect(screen, SEA_DARK, (0, HEIGHT - 120, WIDTH, 120))
            # Корабль (простой)
            self.draw_ship(self.ship_x, HEIGHT - 160)

    def draw_ship(self, x, y):
        # Корпус
        hull = [(x - 40, y), (x + 50, y), (x + 35, y + 25), (x - 25, y + 25)]
        pygame.draw.polygon(screen, (139, 90, 43), hull)
        pygame.draw.polygon(screen, (100, 60, 30), hull, 2)
        # Мачта
        pygame.draw.line(screen, (80, 50, 20), (x + 5, y), (x + 5, y - 55), 4)
        # Парус
        sail = [(x + 8, y - 50), (x + 45, y - 25), (x + 8, y - 5)]
        pygame.draw.polygon(screen, (255, 250, 240), sail)
        pygame.draw.polygon(screen, (200, 180, 150), sail, 2)
        # Флаг соломенной шляпы (простой)
        pygame.draw.circle(screen, GOLD, (x + 5, y - 60), 8)
        pygame.draw.arc(screen, (180, 120, 40), (x - 3, y - 68, 16, 12), 0.3, 2.8, 2)

    def draw_menu(self):
        self.draw_background()
        self.menu_anim += 0.03

        # Заголовок
        title_y = 80 + math.sin(self.menu_anim) * 6
        draw_text(screen, "LUFFY GAME", font_title, GOLD, WIDTH // 2, title_y, center=True)
        draw_text(screen, "Подготовка к ВПР по географии · 5 класс", font_med, WHITE, WIDTH // 2, title_y + 55, center=True)
        draw_text(screen, "Команда пиратов плывёт по морям One Piece и изучает Землю!", font_small, CREAM, WIDTH // 2, title_y + 90, center=True)

        # Кнопки
        btn_w, btn_h = 280, 55
        bx = WIDTH // 2 - btn_w // 2

        buttons = [
            ("Начать плавание!", GameState.SEA_SELECT, 220),
            ("Об игре", GameState.ABOUT, 290),
            ("Выход", None, 360),
        ]

        mouse = pygame.mouse.get_pos()
        for text, state, by in buttons:
            rect = button_rect(bx, by, btn_w, btn_h)
            hover = rect.collidepoint(mouse)
            color = ORANGE if hover else (70, 120, 180)
            draw_rounded_rect(screen, color, rect, 14)
            draw_text(screen, text, font_med, WHITE, WIDTH // 2, by + 12, center=True)

        # Авторы
        draw_text(screen, "Авторы: Владимир Лаптев, Дмитрий Пикулин, Ярослав Костюков", font_tiny, CREAM, WIDTH // 2, HEIGHT - 50, center=True)
        draw_text(screen, "Куратор: Воронцов Николай Витальевич", font_tiny, CREAM, WIDTH // 2, HEIGHT - 30, center=True)

    def draw_sea_select(self):
        self.draw_background()
        draw_text(screen, "Выбери море для плавания", font_large, GOLD, WIDTH // 2, 40, center=True)
        draw_text(screen, "Каждое море — свой набор вопросов по темам ВПР", font_small, WHITE, WIDTH // 2, 80, center=True)

        mouse = pygame.mouse.get_pos()
        btn_w, btn_h = 420, 58
        start_y = 130

        for i, sea in enumerate(SEAS_ORDER):
            rect = button_rect(WIDTH // 2 - btn_w // 2, start_y + i * 70, btn_w, btn_h)
            hover = rect.collidepoint(mouse)
            color = (255, 160, 50) if hover else (50, 100, 160)
            draw_rounded_rect(screen, color, rect, 12)
            draw_text(screen, f"{i + 1}. {sea}", font_med, WHITE, WIDTH // 2, start_y + i * 70 + 8, center=True)
            # Короткое описание
            desc = SEA_DESCRIPTIONS.get(sea, "")[:55] + "..."
            draw_text(screen, desc, font_tiny, CREAM, WIDTH // 2, start_y + i * 70 + 34, center=True)

        # Назад
        back = button_rect(30, HEIGHT - 60, 120, 40)
        hover = back.collidepoint(mouse)
        draw_rounded_rect(screen, ORANGE if hover else (80, 80, 100), back, 10)
        draw_text(screen, "← Меню", font_small, WHITE, 90, HEIGHT - 50, center=True)

        # Счёт
        draw_text(screen, f"Всего правильных: {self.score}", font_small, GOLD, WIDTH - 30, HEIGHT - 45, center=False)

    def draw_quiz(self):
        self.draw_background()
        if not self.current_q:
            return

        q = self.current_q
        sea = SEAS_ORDER[self.current_sea_idx]

        # Верхняя панель
        draw_rounded_rect(screen, (20, 40, 80), (20, 15, WIDTH - 40, 50), 10)
        draw_text(screen, f"{sea}  ·  {q['theme']}", font_small, GOLD, 40, 28)
        progress = f"Вопрос {self.questions_in_sea - len(self.questions_pool)} / {self.questions_in_sea}   |   Верно: {self.correct_count_in_sea}"
        draw_text(screen, progress, font_small, WHITE, WIDTH - 40, 28)

        # Текст вопроса
        panel = pygame.Rect(40, 90, WIDTH - 80, 130)
        draw_rounded_rect(screen, (25, 50, 90), panel, 14)
        draw_text(screen, q["text"], font_med, WHITE, WIDTH // 2, 110, center=True, max_width=WIDTH - 120)

        # Варианты ответов
        mouse = pygame.mouse.get_pos()
        opt_h = 55
        start_y = 250
        for i, opt in enumerate(q["options"]):
            rect = button_rect(80, start_y + i * (opt_h + 12), WIDTH - 160, opt_h)
            hover = rect.collidepoint(mouse) and not self.answered

            if self.answered:
                if i == q["correct"]:
                    color = GREEN
                elif i == self.selected_option:
                    color = RED
                else:
                    color = (60, 70, 90)
            else:
                color = (255, 150, 40) if hover else (55, 100, 150)

            draw_rounded_rect(screen, color, rect, 12)
            letter = chr(65 + i)  # A B C D
            draw_text(screen, f"{letter}.  {opt}", font_med, WHITE, 110, start_y + i * (opt_h + 12) + 12)

        # Пояснение
        if self.show_explanation:
            exp_panel = pygame.Rect(40, HEIGHT - 140, WIDTH - 80, 90)
            draw_rounded_rect(screen, (30, 60, 50) if self.selected_option == q["correct"] else (80, 40, 40), exp_panel, 12)
            title = "Верно! 🎉" if self.selected_option == q["correct"] else "Неверно..."
            draw_text(screen, title, font_med, GOLD if self.selected_option == q["correct"] else ORANGE, 60, HEIGHT - 130)
            draw_text(screen, q["explanation"], font_small, WHITE, 60, HEIGHT - 95, max_width=WIDTH - 140)

            # Кнопка далее
            next_rect = button_rect(WIDTH - 200, HEIGHT - 55, 160, 40)
            hover = next_rect.collidepoint(mouse)
            draw_rounded_rect(screen, ORANGE if hover else (70, 130, 70), next_rect, 10)
            label = "Следующий →" if self.questions_pool else "К итогам →"
            draw_text(screen, label, font_small, WHITE, WIDTH - 120, HEIGHT - 45, center=True)

        self.update_particles()
        for p in self.particles:
            alpha = max(0, p["life"] * 6)
            s = pygame.Surface((8, 8), pygame.SRCALPHA)
            pygame.draw.circle(s, (*p["color"][:3], min(255, alpha)), (4, 4), 4)
            screen.blit(s, (p["x"], p["y"]))

    def draw_result(self):
        self.draw_background()
        sea = SEAS_ORDER[self.current_sea_idx]
        draw_text(screen, f"Море «{sea}» пройдено!", font_large, GOLD, WIDTH // 2, 100, center=True)

        pct = int(100 * self.correct_count_in_sea / max(1, self.questions_in_sea))
        draw_text(screen, f"Правильных ответов: {self.correct_count_in_sea} из {self.questions_in_sea}  ({pct}%)", font_med, WHITE, WIDTH // 2, 170, center=True)

        if pct >= 80:
            msg = "Отлично! Ты настоящий навигатор Соломенной Шляпы!"
            color = GREEN
        elif pct >= 50:
            msg = "Хорошо! Продолжай путь — Гранд-Лайн ждёт!"
            color = ORANGE
        else:
            msg = "Нужно ещё потренироваться. Попробуй это море снова!"
            color = RED
        draw_text(screen, msg, font_med, color, WIDTH // 2, 230, center=True)

        mouse = pygame.mouse.get_pos()
        # Кнопки
        btns = [
            ("Следующее море", "next", 320),
            ("Повторить это море", "retry", 400),
            ("Выбор моря", "seas", 480),
        ]
        for text, action, by in btns:
            rect = button_rect(WIDTH // 2 - 160, by, 320, 55)
            hover = rect.collidepoint(mouse)
            draw_rounded_rect(screen, ORANGE if hover else (60, 110, 170), rect, 12)
            draw_text(screen, text, font_med, WHITE, WIDTH // 2, by + 12, center=True)

    def draw_final(self):
        self.draw_background()
        draw_text(screen, "Путешествие завершено!", font_title, GOLD, WIDTH // 2, 120, center=True)
        draw_text(screen, f"Всего правильных ответов: {self.score} из {self.total_answered}", font_large, WHITE, WIDTH // 2, 200, center=True)
        pct = int(100 * self.score / max(1, self.total_answered))
        draw_text(screen, f"Результат: {pct}%", font_large, GREEN if pct >= 70 else ORANGE, WIDTH // 2, 260, center=True)
        draw_text(screen, "Ты готов к ВПР по географии!", font_med, CREAM, WIDTH // 2, 330, center=True)
        draw_text(screen, "«Я стану Королём Пиратов!» — Монки Д. Луффи", font_small, GOLD, WIDTH // 2, 380, center=True)

        mouse = pygame.mouse.get_pos()
        rect = button_rect(WIDTH // 2 - 140, 450, 280, 55)
        hover = rect.collidepoint(mouse)
        draw_rounded_rect(screen, ORANGE if hover else (70, 120, 180), rect, 12)
        draw_text(screen, "В главное меню", font_med, WHITE, WIDTH // 2, 462, center=True)

    def draw_about(self):
        self.draw_background(sea=False)
        screen.fill((20, 35, 60))
        draw_text(screen, "Об игре LuffyGame", font_large, GOLD, WIDTH // 2, 40, center=True)

        lines = [
            "Игра для подготовки к Всероссийской проверочной работе",
            "по географии для 5 классов.",
            "",
            "Сюжет: команда пиратов из манги One Piece плывёт",
            "по четырём морям и Гранд-Лайн, изучая географию Земли",
            "через приключения в вымышленном мире.",
            "",
            "Источник вопросов: РЕШУ ВПР / демоверсии ФИОКО",
            "(география 5 класс).",
            "",
            "Авторы: Владимир Лаптев, Дмитрий Пикулин, Ярослав Костюков",
            "Куратор проекта: Воронцов Николай Витальевич",
            "",
            "Папки music/ и animation/ — положите туда свои",
            "звуки (.mp3/.ogg) и картинки, они подхватятся автоматически.",
            "",
            "Управление: мышь. Выбирайте ответы кликом."
        ]
        y = 100
        for line in lines:
            draw_text(screen, line, font_small, WHITE, WIDTH // 2, y, center=True)
            y += 26

        mouse = pygame.mouse.get_pos()
        back = button_rect(WIDTH // 2 - 100, HEIGHT - 70, 200, 45)
        hover = back.collidepoint(mouse)
        draw_rounded_rect(screen, ORANGE if hover else (70, 100, 150), back, 10)
        draw_text(screen, "← Назад", font_med, WHITE, WIDTH // 2, HEIGHT - 58, center=True)

    # ---------- СОБЫТИЯ ----------
    def handle_click(self, pos):
        play(sound_click)
        if self.state == GameState.MENU:
            btn_w, btn_h = 280, 55
            bx = WIDTH // 2 - btn_w // 2
            if button_rect(bx, 220, btn_w, btn_h).collidepoint(pos):
                self.state = GameState.SEA_SELECT
            elif button_rect(bx, 290, btn_w, btn_h).collidepoint(pos):
                self.state = GameState.ABOUT
            elif button_rect(bx, 360, btn_w, btn_h).collidepoint(pos):
                pygame.quit()
                sys.exit()

        elif self.state == GameState.SEA_SELECT:
            btn_w, btn_h = 420, 58
            start_y = 130
            for i, sea in enumerate(SEAS_ORDER):
                if button_rect(WIDTH // 2 - btn_w // 2, start_y + i * 70, btn_w, btn_h).collidepoint(pos):
                    self.current_sea_idx = i
                    self.reset_quiz(sea)
                    self.state = GameState.QUIZ
                    return
            if button_rect(30, HEIGHT - 60, 120, 40).collidepoint(pos):
                self.state = GameState.MENU

        elif self.state == GameState.QUIZ:
            if not self.answered and self.current_q:
                opt_h = 55
                start_y = 250
                for i in range(len(self.current_q["options"])):
                    if button_rect(80, start_y + i * (opt_h + 12), WIDTH - 160, opt_h).collidepoint(pos):
                        self.answer(i)
                        return
            if self.show_explanation:
                if button_rect(WIDTH - 200, HEIGHT - 55, 160, 40).collidepoint(pos):
                    if self.next_question():
                        pass
                    else:
                        self.state = GameState.RESULT
                        play(sound_win)

        elif self.state == GameState.RESULT:
            if button_rect(WIDTH // 2 - 160, 320, 320, 55).collidepoint(pos):  # next
                self.current_sea_idx += 1
                if self.current_sea_idx >= len(SEAS_ORDER):
                    self.state = GameState.FINAL
                else:
                    self.reset_quiz()
                    self.state = GameState.QUIZ
            elif button_rect(WIDTH // 2 - 160, 400, 320, 55).collidepoint(pos):  # retry
                self.reset_quiz()
                self.state = GameState.QUIZ
            elif button_rect(WIDTH // 2 - 160, 480, 320, 55).collidepoint(pos):  # seas
                self.state = GameState.SEA_SELECT

        elif self.state == GameState.FINAL:
            if button_rect(WIDTH // 2 - 140, 450, 280, 55).collidepoint(pos):
                self.score = 0
                self.total_answered = 0
                self.current_sea_idx = 0
                self.state = GameState.MENU

        elif self.state == GameState.ABOUT:
            if button_rect(WIDTH // 2 - 100, HEIGHT - 70, 200, 45).collidepoint(pos):
                self.state = GameState.MENU

    def run(self):
        running = True
        while running:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.state == GameState.MENU:
                            running = False
                        else:
                            self.state = GameState.MENU

            # Отрисовка
            if self.state == GameState.MENU:
                self.draw_menu()
            elif self.state == GameState.SEA_SELECT:
                self.draw_sea_select()
            elif self.state == GameState.QUIZ:
                self.draw_quiz()
            elif self.state == GameState.RESULT:
                self.draw_result()
            elif self.state == GameState.FINAL:
                self.draw_final()
            elif self.state == GameState.ABOUT:
                self.draw_about()

            # Движение корабля
            self.ship_x = 80 + math.sin(pygame.time.get_ticks() * 0.001) * 30

            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
