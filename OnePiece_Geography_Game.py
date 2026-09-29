# -*- coding: utf-8 -*-
# One Piece: География Великого Моря
# Игра для подготовки к ВПР по географии 6 класс
# Авторы: Владимир Лаптев, Дмитрий Пикулин, Ярослав Костюков
# Куратор проекта: Воронцов Николай Витальевич
import zlib, base64, pathlib
_b64 = pathlib.Path(__file__).with_name("game.b64").read_text(encoding="ascii").strip()
exec(zlib.decompress(base64.b64decode(_b64)).decode("utf-8"))
