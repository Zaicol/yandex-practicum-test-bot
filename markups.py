from telebot.types import KeyboardButton, ReplyKeyboardMarkup
from models import *


def make_kb(btns):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for btn in btns:
        if isinstance(btn, list):
            kb.add(*[KeyboardButton(b) for b in btn])
        else:
            kb.add(KeyboardButton(btn))
    return kb


def make_markup_voice():
    ses = Session()
    voices = ses.query(Media).filter(Media.type == 'voice').all()
    voices = [x.name for x in voices] + ['Назад']
    ses.close()
    return make_kb(voices)


markup_main = make_kb([['Фото', 'Голосовые']])
markup_img = make_kb([['Последнее селфи', 'Фото из старшей школы'], ['Назад']])
