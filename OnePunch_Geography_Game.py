# -*- coding: utf-8 -*-
"""
One-Punch Man: Географический Герой
Игра для подготовки к ВПР по географии 6 класс
Вопросы на основе РЕШУ ВПР (geo6-vpr.sdamgia.ru)
Авторы: Владимир Лаптев, Дима Пикулин, Ярослав Костюков
Школа № 311, 6А класс

Папки:
  music/      — сюда класть .mp3 / .wav / .ogg
  animation/  — сюда класть .png / .gif / .jpg
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
        # пробуем другие расширения
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
        # простое уменьшение, если слишком большая
        w, h = img.width(), img.height()
        mw, mh = max_size
        if w > mw or h > mh:
            factor = max(w // mw, h // mh, 1)
            img = img.subsample(factor, factor)
        return img
    except Exception:
        return None

# ==================== ДАННЫЕ ИГРЫ ====================
LEVELS = [
    {
        "name": "Уровень 1: Угроза «Волк»",
        "title": "Мировой океан и моря",
        "story": "Монстр «Солёный Кракен» появился в Мировом океане!\nОн запутывает героев ложными знаниями о морях и океанах.\nВыбери правильный ответ в окошке — и победи одним ударом!",
        "hero": "Сайтама",
        "monster_img": "monster_wolf.png",
        "questions": [
            {
                "text": "Мировой океан занимает около 70% поверхности Земли.\nКакой океан является самым большим по площади?",
                "options": ["Атлантический", "Индийский", "Тихий", "Северный Ледовитый"],
                "answer": 2,
                "explain": "Тихий океан — самый большой и глубокий океан Земли."
            },
            {
                "text": "Какое из перечисленных морей относится к морям Северного Ледовитого океана?",
                "options": ["Баренцево", "Средиземное", "Карибское", "Аравийское"],
                "answer": 0,
                "explain": "Баренцево море — окраинное море Северного Ледовитого океана."
            },
            {
                "text": "Какое из перечисленных морей является внутренним?",
                "options": ["Берингово море", "Чёрное море", "Японское море", "Баренцево море"],
                "answer": 1,
                "explain": "Чёрное море — внутреннее море: глубоко вдаётся в сушу и соединяется с океаном через проливы."
            },
            {
                "text": "В каком океане находится Аравийское море?",
                "options": ["Атлантическом", "Тихом", "Индийском", "Северном Ледовитом"],
                "answer": 2,
                "explain": "Аравийское море — часть Индийского океана."
            },
            {
                "text": "Какой пролив соединяет Тихий и Северный Ледовитый океаны?",
                "options": ["Гибралтарский", "Берингов", "Магелланов", "Дрейка"],
                "answer": 1,
                "explain": "Берингов пролив соединяет Тихий и Северный Ледовитый океаны."
            }
        ]
    },
    {
        "name": "Уровень 2: Угроза «Тигр»",
        "title": "Воды суши — реки и озёра",
        "story": "Монстр «Речной Демон» перекрыл все реки и озёра!\nОн требует знания о водах суши.\nВыбери правильный ответ — и он повержен одним ударом!",
        "hero": "Генос",
        "monster_img": "monster_tiger.png",
        "questions": [
            {
                "text": "Какая из перечисленных рек имеет наибольшую длину?",
                "options": ["Обь", "Амазонка", "Конго", "Янцзы"],
                "answer": 1,
                "explain": "Амазонка — одна из самых длинных рек мира."
            },
            {
                "text": "Какая из перечисленных рек относится к бассейну Тихого океана?",
                "options": ["Миссисипи", "Янцзы", "Лена", "Обь"],
                "answer": 1,
                "explain": "Янцзы впадает в Восточно-Китайское море Тихого океана."
            },
            {
                "text": "Какая из перечисленных рек относится к бассейну Атлантического океана?",
                "options": ["Миссисипи", "Янцзы", "Лена", "Обь"],
                "answer": 0,
                "explain": "Миссисипи впадает в Мексиканский залив Атлантического океана."
            },
            {
                "text": "В каком из следующих высказываний содержится информация о режиме реки Оби?",
                "options": [
                    "Обь берёт начало в Алтайском крае при слиянии двух рек",
                    "Половодье на Оби приходится на весну и начало лета",
                    "Направление течения Оби несколько раз меняется",
                    "Обь собирает воды с территории более 2 990 000 км²"
                ],
                "answer": 1,
                "explain": "Режим реки — изменение уровня воды в течение года. Половодье — часть режима."
            },
            {
                "text": "Какое озеро является самым большим по площади в мире?",
                "options": ["Байкал", "Каспийское море", "Верхнее", "Виктория"],
                "answer": 1,
                "explain": "Каспийское море — самое большое озеро (море-озеро) по площади."
            }
        ]
    },
    {
        "name": "Уровень 3: Угроза «Демон»",
        "title": "Атмосфера и погода",
        "story": "Финальный монстр «Атмосферный Титан» искажает погоду по всей планете!\nТолько настоящий герой с знаниями об атмосфере сможет победить его\nОДНИМ УДАРОМ!",
        "hero": "Сайтама",
        "monster_img": "monster_demon.png",
        "questions": [
            {
                "text": "Как называется самый нижний слой атмосферы, в котором формируется погода?",
                "options": ["Стратосфера", "Тропосфера", "Мезосфера", "Термосфера"],
                "answer": 1,
                "explain": "Тропосфера — нижний слой атмосферы. Здесь происходят все погодные явления."
            },
            {
                "text": "Что такое суточная амплитуда температуры воздуха?",
                "options": [
                    "Средняя температура за сутки",
                    "Разница между максимальной и минимальной температурой за сутки",
                    "Самая высокая температура за сутки",
                    "Изменение температуры с высотой"
                ],
                "answer": 1,
                "explain": "Суточная амплитуда = максимальная температура минус минимальная за одни сутки."
            },
            {
                "text": "Максимальная температура была +13,6 °C, минимальная +4,7 °C.\nЧему равна суточная амплитуда?",
                "options": ["8,9 °C", "18,3 °C", "9,1 °C", "4,7 °C"],
                "answer": 0,
                "explain": "13,6 − 4,7 = 8,9 °C"
            },
            {
                "text": "Как называется ветер, который меняет направление два раза в сутки\n(днём с моря на сушу, ночью наоборот)?",
                "options": ["Муссон", "Пассат", "Бриз", "Фён"],
                "answer": 2,
                "explain": "Бриз — местный ветер с суточной сменой направления."
            },
            {
                "text": "С увеличением высоты над уровнем моря температура воздуха в тропосфере...",
                "options": ["Повышается", "Понижается", "Не изменяется", "Сначала повышается, потом понижается"],
                "answer": 1,
                "explain": "В тропосфере температура понижается примерно на 6 °C на каждый километр высоты."
            },
            {
                "text": "Какой газ составляет наибольшую долю в составе атмосферы Земли?",
                "options": ["Кислород", "Углекислый газ", "Азот", "Аргон"],
                "answer": 2,
                "explain": "Азот — около 78% объёма атмосферы, кислород — около 21%."
            }
        ]
    }
]

HERO_PHRASES = {
    "correct": [
        "ONE PUNCH! Монстр уничтожен!",
        "Слишком легко... Как и всегда.",
        "Отличный удар! Знания — это сила.",
        "Монстр даже не успел моргнуть!",
        "Вот что значит настоящий герой!"
    ],
    "wrong": [
        "Ой... Промахнулся.",
        "Монстр оказался хитрее. Не сдавайся!",
        "Нужно лучше готовиться к ВПР...",
        "В следующий раз точно попадёшь!",
        "Герои тоже ошибаются. Главное — учиться."
    ]
}


class OnePunchGeographyGame:
    def __init__(self, root):
        self.root = root
        self.root.title("One-Punch Man: Географический Герой")
        self.root.geometry("920x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a2e")

        self.current_level = 0
        self.current_question = 0
        self.score = 0
        self.lives = 3
        self.correct_in_level = 0
        self.shuffled_questions = []
        self._images = []  # чтобы картинки не удалялись сборщиком мусора

        self.title_font = font.Font(family="Arial", size=22, weight="bold")
        self.header_font = font.Font(family="Arial", size=16, weight="bold")
        self.normal_font = font.Font(family="Arial", size=13)
        self.button_font = font.Font(family="Arial", size=12, weight="bold")
        self.small_font = font.Font(family="Arial", size=11)
        self.option_font = font.Font(family="Arial", size=12)
        self.big_punch_font = font.Font(family="Arial", size=28, weight="bold")

        self.show_main_menu()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self._images.clear()

    def keep_image(self, img):
        if img:
            self._images.append(img)
        return img

    # ---------- анимация текста ----------
    def animate_punch_text(self, label, texts, colors, step=0):
        if step >= len(texts):
            return
        label.config(text=texts[step], fg=colors[step % len(colors)])
        self.root.after(120, lambda: self.animate_punch_text(label, texts, colors, step + 1))

    def flash_bg(self, color1="#e94560", color2="#1a1a2e", times=4, delay=80):
        def _flash(n):
            if n <= 0:
                self.root.configure(bg="#1a1a2e")
                return
            self.root.configure(bg=color1 if n % 2 else color2)
            self.root.after(delay, lambda: _flash(n - 1))
        _flash(times)

    # ---------- экраны ----------
    def show_main_menu(self):
        self.clear_window()
        play_music("menu.mp3")

        frame = tk.Frame(self.root, bg="#1a1a2e")
        frame.pack(expand=True, fill="both")

        # логотип из animation/logo.png если есть
        logo = self.keep_image(load_image("logo.png", (350, 200)))
        if logo:
            tk.Label(frame, image=logo, bg="#1a1a2e").pack(pady=(20, 5))
        else:
            tk.Label(frame, text="ONE-PUNCH MAN", font=self.title_font,
                     fg="#e94560", bg="#1a1a2e").pack(pady=(35, 5))

        tk.Label(frame, text="ГЕОГРАФИЧЕСКИЙ ГЕРОЙ", font=self.header_font,
                 fg="#ffffff", bg="#1a1a2e").pack(pady=(0, 8))
        tk.Label(frame, text="Подготовка к ВПР по географии • 6 класс",
                 font=self.small_font, fg="#aaaaaa", bg="#1a1a2e").pack(pady=(0, 20))

        desc = ("Ты — герой Геройской Ассоциации!\n"
                "Монстры искажают знания о Земле.\n"
                "Выбирай правильный ответ в окошке —\n"
                "и побеждай их ОДНИМ УДАРОМ!")
        tk.Label(frame, text=desc, font=self.normal_font, fg="#dddddd",
                 bg="#1a1a2e", justify="center").pack(pady=6)

        btn_style = {"font": self.button_font, "width": 25, "height": 2,
                     "bd": 0, "cursor": "hand2"}

        tk.Button(frame, text="НАЧАТЬ ИГРУ", bg="#e94560", fg="white",
                  activebackground="#c73a52", command=self.start_game,
                  **btn_style).pack(pady=8)

        tk.Button(frame, text="ПРАВИЛА", bg="#0f3460", fg="white",
                  activebackground="#16213e", command=self.show_rules,
                  **btn_style).pack(pady=5)

        tk.Button(frame, text="ОБ АВТОРАХ", bg="#0f3460", fg="white",
                  activebackground="#16213e", command=self.show_authors,
                  **btn_style).pack(pady=5)

        tk.Button(frame, text="ВЫХОД", bg="#333333", fg="white",
                  activebackground="#555555", command=self.root.quit,
                  **btn_style).pack(pady=5)

        sound_status = "🔊 Звук: включён" if SOUND_AVAILABLE else "🔇 Звук: pygame не установлен (игра без музыки)"
        tk.Label(frame, text=sound_status, font=self.small_font,
                 fg="#666666", bg="#1a1a2e").pack(pady=8)

        tk.Label(frame, text="Школа № 311  •  6А класс  •  2026",
                 font=self.small_font, fg="#666666", bg="#1a1a2e").pack(side="bottom", pady=10)

    def show_rules(self):
        self.clear_window()
        frame = tk.Frame(self.root, bg="#1a1a2e")
        frame.pack(expand=True, fill="both", padx=40, pady=20)

        tk.Label(frame, text="ПРАВИЛА ИГРЫ", font=self.header_font,
                 fg="#e94560", bg="#1a1a2e").pack(pady=(5, 12))

        rules = (
            "• 3 уровня (Волк → Тигр → Демон).\n\n"
            "• Вопросы в формате ВПР по географии 6 класса\n"
            "  (источник: РЕШУ ВПР / ФИОКО).\n\n"
            "• Варианты ответов — большие кнопки-окошки.\n"
            "  Нажми на одно окошко — это твой выбор.\n\n"
            "• Правильный ответ = ONE PUNCH! + анимация + звук.\n"
            "  Герой комментирует и показывает пояснение.\n\n"
            "• Неправильный ответ = потеря жизни.\n"
            "  Всё равно показывается правильный ответ.\n\n"
            "• Папки music/ и animation/ — туда можно класть\n"
            "  свои файлы (см. README внутри папок)."
        )
        tk.Label(frame, text=rules, font=self.normal_font, fg="#eeeeee",
                 bg="#1a1a2e", justify="left").pack(anchor="w")

        tk.Button(frame, text="← НАЗАД В МЕНЮ", font=self.button_font,
                  bg="#0f3460", fg="white", width=20,
                  command=self.show_main_menu).pack(pady=20)

    def show_authors(self):
        self.clear_window()
        frame = tk.Frame(self.root, bg="#1a1a2e")
        frame.pack(expand=True, fill="both", padx=40, pady=20)

        tk.Label(frame, text="АВТОРЫ ПРОЕКТА", font=self.header_font,
                 fg="#e94560", bg="#1a1a2e").pack(pady=(5, 12))

        authors = (
            "Владимир Лаптев\n"
            "Дима Пикулин\n"
            "Ярослав Костюков\n\n"
            "Учащиеся 6А класса\n"
            "ГБОУ СОШ № 311\n"
            "с углублённым изучением физики\n"
            "Фрунзенского района г. Санкт-Петербурга\n\n"
            "Учебный год: 2026\n"
            "Предмет: География + Информатика\n"
            "Тип проекта: практико-ориентированный\n\n"
            "Продукт: обучающая игра для подготовки к ВПР"
        )
        tk.Label(frame, text=authors, font=self.normal_font, fg="#eeeeee",
                 bg="#1a1a2e", justify="center").pack()

        tk.Button(frame, text="← НАЗАД В МЕНЮ", font=self.button_font,
                  bg="#0f3460", fg="white", width=20,
                  command=self.show_main_menu).pack(pady=20)

    def start_game(self):
        stop_music()
        self.current_level = 0
        self.score = 0
        self.lives = 3
        self.show_level_intro()

    def show_level_intro(self):
        self.clear_window()
        play_music("battle.mp3")
        level = LEVELS[self.current_level]

        frame = tk.Frame(self.root, bg="#1a1a2e")
        frame.pack(expand=True, fill="both", padx=25, pady=15)

        tk.Label(frame, text=level["name"], font=self.header_font,
                 fg="#e94560", bg="#1a1a2e").pack(pady=(10, 4))
        tk.Label(frame, text=level["title"], font=self.normal_font,
                 fg="#ffffff", bg="#1a1a2e").pack(pady=(0, 10))

        # картинка монстра
        monster = self.keep_image(load_image(level["monster_img"], (220, 220)))
        if monster:
            tk.Label(frame, image=monster, bg="#1a1a2e").pack(pady=5)

        story_frame = tk.Frame(frame, bg="#16213e", bd=2, relief="ridge")
        story_frame.pack(fill="x", pady=8, padx=10)
        tk.Label(story_frame, text=level["story"], font=self.normal_font,
                 fg="#eeeeee", bg="#16213e", justify="center",
                 wraplength=780, pady=14, padx=12).pack()

        hero_name = level["hero"]
        hero_file = "saitama.png" if hero_name == "Сайтама" else "genos.png"
        hero_img = self.keep_image(load_image(hero_file, (120, 120)))
        if hero_img:
            hf = tk.Frame(frame, bg="#1a1a2e")
            hf.pack(pady=5)
            tk.Label(hf, image=hero_img, bg="#1a1a2e").pack(side="left", padx=8)
            tk.Label(hf, text=f"Напарник: {hero_name}", font=self.small_font,
                     fg="#f0a500", bg="#1a1a2e").pack(side="left")
        else:
            tk.Label(frame, text=f"Напарник: {hero_name}", font=self.small_font,
                     fg="#f0a500", bg="#1a1a2e").pack(pady=4)

        status = f"Жизни: {'❤️' * self.lives}{'🖤' * (3 - self.lives)}    |    Очки: {self.score}"
        tk.Label(frame, text=status, font=self.normal_font,
                 fg="#f0a500", bg="#1a1a2e").pack(pady=6)

        tk.Button(frame, text="В БОЙ!  →", font=self.button_font,
                  bg="#e94560", fg="white", width=20, height=2,
                  command=self.start_level).pack(pady=12)

    def start_level(self):
        self.current_question = 0
        self.correct_in_level = 0
        level = LEVELS[self.current_level]
        self.shuffled_questions = level["questions"][:]
        random.shuffle(self.shuffled_questions)
        self.show_question()

    def show_question(self):
        self.clear_window()
        level = LEVELS[self.current_level]
        q = self.shuffled_questions[self.current_question]
        total_q = len(self.shuffled_questions)

        frame = tk.Frame(self.root, bg="#1a1a2e")
        frame.pack(expand=True, fill="both", padx=18, pady=10)

        top = tk.Frame(frame, bg="#1a1a2e")
        top.pack(fill="x")
        tk.Label(top, text=f"{level['name']}  •  Вопрос {self.current_question + 1}/{total_q}",
                 font=self.small_font, fg="#aaaaaa", bg="#1a1a2e").pack(side="left")
        status = f"❤️ {self.lives}   |   ⭐ {self.score}   |   {level['hero']}"
        tk.Label(top, text=status, font=self.small_font,
                 fg="#f0a500", bg="#1a1a2e").pack(side="right")

        q_frame = tk.Frame(frame, bg="#16213e", bd=2, relief="ridge")
        q_frame.pack(fill="x", pady=10)
        tk.Label(q_frame, text=q["text"], font=self.normal_font,
                 fg="#ffffff", bg="#16213e", justify="left",
                 wraplength=840, pady=14, padx=16).pack()

        tk.Label(frame, text="Выбери ОДИН правильный ответ (нажми на окошко):",
                 font=self.small_font, fg="#aaaaaa", bg="#1a1a2e").pack(pady=(4, 6))

        options_frame = tk.Frame(frame, bg="#1a1a2e")
        options_frame.pack(fill="both", expand=True)

        colors = ["#0f3460", "#16213e", "#0f3460", "#16213e"]
        for i, opt in enumerate(q["options"]):
            btn = tk.Button(
                options_frame,
                text=f"  {chr(65 + i)}.  {opt}",
                font=self.option_font,
                bg=colors[i % 4],
                fg="#ffffff",
                activebackground="#e94560",
                activeforeground="#ffffff",
                bd=2,
                relief="raised",
                anchor="w",
                padx=14,
                pady=11,
                cursor="hand2",
                wraplength=820,
                justify="left",
                command=lambda idx=i: self.check_answer(idx)
            )
            btn.pack(fill="x", padx=22, pady=4)

    def check_answer(self, chosen_index):
        q = self.shuffled_questions[self.current_question]
        is_correct = chosen_index == q["answer"]
        level = LEVELS[self.current_level]
        hero = level["hero"]

        self.clear_window()
        frame = tk.Frame(self.root, bg="#1a1a2e")
        frame.pack(expand=True, fill="both", padx=25, pady=20)

        punch_label = tk.Label(frame, text="", font=self.big_punch_font, bg="#1a1a2e")
        punch_label.pack(pady=(8, 4))

        if is_correct:
            self.score += 10
            self.correct_in_level += 1
            play_sound("punch.wav")
            self.flash_bg("#00ff88", "#1a1a2e", times=5, delay=70)
            self.animate_punch_text(
                punch_label,
                ["💥", "ONE", "PUNCH!", "💥 ONE PUNCH! 💥"],
                ["#ffffff", "#00ff88", "#00ff88", "#00ff88"]
            )
            phrase = random.choice(HERO_PHRASES["correct"])
            # картинка удара
            punch_img = self.keep_image(load_image("punch.gif", (180, 180)) or load_image("punch.png", (180, 180)))
            if punch_img:
                tk.Label(frame, image=punch_img, bg="#1a1a2e").pack(pady=4)
        else:
            self.lives -= 1
            self.flash_bg("#e94560", "#1a1a2e", times=4, delay=90)
            punch_label.config(text="МОНСТР АТАКУЕТ!", fg="#e94560")
            phrase = random.choice(HERO_PHRASES["wrong"])

        tk.Label(frame, text=f"{hero}: «{phrase}»",
                 font=self.header_font, fg="#ffffff", bg="#1a1a2e").pack(pady=6)

        # правильный ответ + пояснение
        result_frame = tk.Frame(frame, bg="#16213e", bd=2, relief="ridge")
        result_frame.pack(fill="x", pady=16, padx=8)

        correct_text = q["options"][q["answer"]]
        tk.Label(result_frame, text=f"Правильный ответ: {correct_text}",
                 font=self.button_font, fg="#00ff88", bg="#16213e",
                 pady=6).pack()
        tk.Label(result_frame, text="Пояснение:", font=self.small_font,
                 fg="#f0a500", bg="#16213e").pack(anchor="w", padx=14, pady=(4, 0))
        tk.Label(result_frame, text=q["explain"], font=self.normal_font,
                 fg="#eeeeee", bg="#16213e", wraplength=780,
                 justify="left", padx=14, pady=6).pack(anchor="w")

        status = f"Жизни: {'❤️' * max(0, self.lives)}{'🖤' * (3 - max(0, self.lives))}    |    Очки: {self.score}"
        tk.Label(frame, text=status, font=self.normal_font,
                 fg="#f0a500", bg="#1a1a2e").pack(pady=6)

        if self.lives <= 0:
            tk.Button(frame, text="ИГРА ОКОНЧЕНА", font=self.button_font,
                      bg="#e94560", fg="white", width=20,
                      command=self.game_over).pack(pady=12)
        else:
            tk.Button(frame, text="ДАЛЬШЕ →", font=self.button_font,
                      bg="#0f3460", fg="white", width=20,
                      command=self.next_question).pack(pady=12)

    def next_question(self):
        self.current_question += 1
        if self.current_question >= len(self.shuffled_questions):
            self.finish_level()
        else:
            self.show_question()

    def finish_level(self):
        self.clear_window()
        needed = 3
        frame = tk.Frame(self.root, bg="#1a1a2e")
        frame.pack(expand=True, fill="both", padx=30, pady=25)

        if self.correct_in_level >= needed:
            tk.Label(frame, text="УРОВЕНЬ ПРОЙДЕН!", font=self.title_font,
                     fg="#00ff88", bg="#1a1a2e").pack(pady=12)
            msg = f"Правильных ответов: {self.correct_in_level} из {len(self.shuffled_questions)}\nМонстр побеждён одним ударом!"
            tk.Label(frame, text=msg, font=self.normal_font,
                     fg="#ffffff", bg="#1a1a2e", justify="center").pack()

            self.current_level += 1
            if self.current_level >= len(LEVELS):
                tk.Button(frame, text="К ФИНАЛУ!", font=self.button_font,
                          bg="#e94560", fg="white", width=20, height=2,
                          command=self.victory).pack(pady=22)
            else:
                tk.Button(frame, text="СЛЕДУЮЩИЙ УРОВЕНЬ →", font=self.button_font,
                          bg="#e94560", fg="white", width=25, height=2,
                          command=self.show_level_intro).pack(pady=22)
        else:
            tk.Label(frame, text="УРОВЕНЬ НЕ ПРОЙДЕН", font=self.title_font,
                     fg="#e94560", bg="#1a1a2e").pack(pady=12)
            msg = (f"Правильных ответов: {self.correct_in_level} из {len(self.shuffled_questions)}\n"
                   f"Нужно минимум {needed}.\nПопробуй ещё раз!")
            tk.Label(frame, text=msg, font=self.normal_font,
                     fg="#ffffff", bg="#1a1a2e", justify="center").pack()
            tk.Button(frame, text="ПОВТОРИТЬ УРОВЕНЬ", font=self.button_font,
                      bg="#0f3460", fg="white", width=22,
                      command=self.show_level_intro).pack(pady=10)
            tk.Button(frame, text="В ГЛАВНОЕ МЕНЮ", font=self.button_font,
                      bg="#333333", fg="white", width=22,
                      command=self.show_main_menu).pack(pady=5)

    def victory(self):
        self.clear_window()
        stop_music()
        play_music("victory.mp3", loop=False)

        frame = tk.Frame(self.root, bg="#1a1a2e")
        frame.pack(expand=True, fill="both", padx=30, pady=25)

        win_img = self.keep_image(load_image("victory.png", (280, 200)))
        if win_img:
            tk.Label(frame, image=win_img, bg="#1a1a2e").pack(pady=8)

        tk.Label(frame, text="🏆 ПОБЕДА! 🏆", font=self.title_font,
                 fg="#ffd700", bg="#1a1a2e").pack(pady=8)
        tk.Label(frame, text="Ты стал Героем S-класса!",
                 font=self.header_font, fg="#00ff88", bg="#1a1a2e").pack()
        tk.Label(frame, text="Сайтама: «Неплохо... Для новичка.»",
                 font=self.normal_font, fg="#dddddd", bg="#1a1a2e").pack(pady=6)

        final = (f"Все монстры побеждены одним ударом!\n\n"
                 f"Итоговые очки: {self.score}\n"
                 f"Оставшиеся жизни: {self.lives}\n\n"
                 f"Ты отлично подготовился к ВПР по географии!")
        tk.Label(frame, text=final, font=self.normal_font,
                 fg="#eeeeee", bg="#1a1a2e", justify="center").pack(pady=12)

        tk.Button(frame, text="ИГРАТЬ СНОВА", font=self.button_font,
                  bg="#e94560", fg="white", width=20,
                  command=self.start_game).pack(pady=6)
        tk.Button(frame, text="В ГЛАВНОЕ МЕНЮ", font=self.button_font,
                  bg="#0f3460", fg="white", width=20,
                  command=self.show_main_menu).pack(pady=4)

    def game_over(self):
        self.clear_window()
        stop_music()
        frame = tk.Frame(self.root, bg="#1a1a2e")
        frame.pack(expand=True, fill="both", padx=30, pady=25)

        tk.Label(frame, text="ИГРА ОКОНЧЕНА", font=self.title_font,
                 fg="#e94560", bg="#1a1a2e").pack(pady=12)
        tk.Label(frame, text="Монстры оказались сильнее...\nНо герои не сдаются!",
                 font=self.normal_font, fg="#ffffff", bg="#1a1a2e",
                 justify="center").pack(pady=6)
        tk.Label(frame, text=f"Набрано очков: {self.score}",
                 font=self.header_font, fg="#f0a500", bg="#1a1a2e").pack(pady=10)

        tk.Button(frame, text="ПОПРОБОВАТЬ СНОВА", font=self.button_font,
                  bg="#e94560", fg="white", width=22,
                  command=self.start_game).pack(pady=6)
        tk.Button(frame, text="В ГЛАВНОЕ МЕНЮ", font=self.button_font,
                  bg="#0f3460", fg="white", width=22,
                  command=self.show_main_menu).pack(pady=4)


if __name__ == "__main__":
    root = tk.Tk()
    app = OnePunchGeographyGame(root)
    root.mainloop()
