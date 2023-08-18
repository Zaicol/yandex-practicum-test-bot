from telebot import *
from markups import *
from time import sleep


print('Старт')

current_version = '0.1.0 (альфа)'
restart_message = f'Бот перезапущен.\n\n`Версия {current_version}`'


with open('token.txt') as f:
    url = f.readline()
bot = TeleBot(url)
bot.send_message(289208255, restart_message, parse_mode='markdown')


@bot.message_handler(commands=['myid'])
def id_handler(message):
    bot.register_next_step_handler(message, main_handler)
    bot.send_message(message.from_user.id, message.from_user.id, reply_markup=markup_main)


@bot.message_handler(commands=['test'])
def test_handler(message):
    bot.send_message(message.from_user.id, "Тест", reply_markup=markup_main)


@bot.message_handler(commands=['hobby'])
def hobby_handler(message):
    bot.register_next_step_handler(message, main_handler)
    ses = Session()
    hobby_text = ses.query(Media).filter(Media.type == 'text').order_by(Media.id.asc()).all()
    hobby_text = hobby_text[0].data + '\n' + hobby_text[1].data
    bot.send_message(message.from_user.id, hobby_text, reply_markup=markup_main)


def voice_prompt(message):
    uid = message.from_user.id
    rep = "Неправильный ввод, попробуйте снова"
    markup = make_markup_voice()
    next_step = voice_prompt

    ses = Session()
    vc = ses.query(Media).where(Media.name == message.text).first()
    ses.close()
    if vc:
        bot.send_voice(uid, vc.data, caption=vc.name, reply_markup=markup)
    else:
        if message.text == "Назад":
            rep = "Возврат в главное меню"
            next_step = main_handler
            markup = markup_main
        bot.send_message(uid, rep, reply_markup=markup)
    bot.register_next_step_handler(message, next_step)


def image_prompt(message):
    uid = message.from_user.id
    rep = "Неправильный ввод, попробуйте снова"
    markup = markup_img
    next_step = image_prompt

    ses = Session()
    photo = ses.query(Media).where(Media.name == message.text).first()
    ses.close()
    if photo:
        bot.send_photo(uid, photo.data, caption=photo.name, reply_markup=markup_img)
    else:
        if message.text == "Назад":
            rep = "Возврат в главное меню"
            next_step = main_handler
            markup = markup_main
        bot.send_message(uid, rep, reply_markup=markup)
    bot.register_next_step_handler(message, next_step)


@bot.message_handler(commands=['start'])
def main_handler(message):
    rep = "Выберите команду"
    markup = markup_main
    next_step = main_handler
    uid = message.from_user.id
    if message.text == "Фото":
        rep = "Выберите фото"
        markup = markup_img
        next_step = image_prompt
    elif message.text == "Голосовые":
        rep = "Выберите войс"
        markup = make_markup_voice()
        next_step = voice_prompt

    bot.send_message(uid, rep, reply_markup=markup, parse_mode='markdown')
    bot.register_next_step_handler(message, next_step)


startbot = 1
if startbot:
    while True:
        try:
            bot.polling(none_stop=True, timeout=60)
        except Exception as ex:
            print(ex)
            bot.send_message(289208255, "Произошла ошибка")
            bot.send_message(289208255, str(ex))
            sleep(2)
