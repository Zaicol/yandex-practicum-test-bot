from telebot.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


def build_menu(buttons, n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


def make_kb(btns):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for btn in btns:
        if isinstance(btn, list):
            kb.add(*[KeyboardButton(b) for b in btn])
        else:
            kb.add(KeyboardButton(btn))
    return kb


def make_inline(p):
    kb = InlineKeyboardMarkup()
    for i in range(len(p)):
        kb.add(InlineKeyboardButton(i + 1, callback_data=str(i)))
    return kb


markup_main = make_kb([['Фото', 'Голосовые']])
markup_img = make_kb([['Последнее селфи', 'Фото из старшей школы'], ['Назад']])

hobby_text = """
Моё хобби - коллекционирование книг.
Lorem ipsum dolor sit amet, consectetur adipiscing elit. \
Etiam fermentum tempus cursus. In facilisis vulputate varius. \
Vestibulum nibh elit, tempus eu nibh non, hendrerit fringilla sem. Mauris lectus. \
Lorem ipsum dolor sit amet, consectetur adipiscing elit. \
Etiam fermentum tempus cursus. In facilisis vulputate varius. \
Vestibulum nibh elit, tempus eu nibh non, hendrerit fringilla sem. Mauris lectus. \
Lorem ipsum dolor sit amet, consectetur adipiscing elit. \
Etiam fermentum tempus cursus. In facilisis vulputate varius. \
Vestibulum nibh elit, tempus eu nibh non, hendrerit fringilla sem. Mauris lectus. \
"""
