from telebot import *
from models import *
from markups import *
from time import sleep


print('Начало')

current_version = '0.1.0 (альфа)'
restart_message = f'Бот перезапущен.\n\n`Версия {current_version}`'


with open('token.txt') as f:
    url = f.readline()
bot = TeleBot(url)
bot.send_message(289208255, restart_message, parse_mode='markdown')


def do_log(user, place, other=''):
    if hasattr(user, 'id'):
        uid = str(user.id)
    else:
        try:
            uid = str(user)
        except Exception:
            uid = 'Неизвестный пользователь'
    if hasattr(user, 'username') and user.username:
        try:
            uid += ' ' + user.username
        except Exception as e:
            print('Username log error:', e)
            print(user.username)
    elif hasattr(user, 'first_name') and user.first_name:
        uid += ' ' + user.first_name

    print(dtm.now(), uid, place, other, sep='\t')


@bot.message_handler(commands=['myid'])
def id_handler(message):
    do_log(message.from_user, 'ID')
    bot.register_next_step_handler(message, main_handler)
    bot.send_message(message.from_user.id, message.from_user.id, reply_markup=markup_main)


@bot.message_handler(commands=['test'])
def test_handler(message):
    bot.send_message(message.from_user.id, "Тест", reply_markup=markup_main)


@bot.message_handler(commands=['stop'])
def stop_handler(message):
    if message.from_user.id == 289208255:
        bot.send_message(message.from_user.id, "Бот выключен", reply_markup=markup_main)
        do_log(message.from_user.id, "ManualStop")
        bot.stop_polling()
        sys.exit("Stop")
    do_log(message.from_user.id, "ManualStop", "NotAdmin")
    bot.send_message(message.from_user.id, "Неизвестная команда", reply_markup=markup_main)
    bot.register_next_step_handler(message, main_handler)


@bot.message_handler(commands=['hobby'])
def hobby_handler(message):
    do_log(message.from_user, 'hobby')
    bot.register_next_step_handler(message, main_handler)
    bot.send_message(message.from_user.id, hobby_text, reply_markup=markup_main)


def image_add_handler(message):
    ses = Session()
    uid = message.from_user.id
    rep = "Место не найдено. Попробуйте снова"
    markup = markup_main
    next_step = main_handler
    if message.content_type == "photo":
        try:
            fid = message.photo[-1].file_id
            inp = message.caption
            do_log(message.from_user, "ImageAdd", inp)
            new_image = Media(name=inp, data=fid)
            ses.add(new_image)
            ses.commit()
            rep = "Изображение успешно добавлено"
        except TypeError as e:
            rep = "Type Error"
            do_log(message.from_user, 'Error', str(e))
        except Exception as e:
            rep = "Ошибка:" + str(e)
            do_log(message.from_user, 'Error', str(e))
    elif message.text == "Назад":
        do_log(message.from_user, "ImageAdd", "Back")
        rep = "Отмена добавления изображения"
    else:
        do_log(message.from_user, "ImageAdd", "WrongInput")
        rep = "Необходимо отправить изображение с подписью. Попробуйте снова"
    ses.close()
    bot.register_next_step_handler(message, next_step)
    bot.send_message(uid, rep)


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
            do_log(message.from_user, "ImageSee", "Back")
            rep = "Возврат в главное меню"
            next_step = main_handler
            markup = markup_main
        bot.send_message(uid, rep, reply_markup=markup)
    bot.register_next_step_handler(message, next_step)


@bot.message_handler(commands=['start'])
@bot.message_handler(content_types=['text'])
def main_handler(message):
    to_log = ""
    rep = "123"
    markup = markup_main
    next_step = main_handler
    uid = message.from_user.id
    if message.text == "Фото":
        do_log(message.from_user, "ImageSee", "To")
        rep = "Выберите фото"
        markup = markup_img
        next_step = image_prompt
    elif message.text == "Голосовые":
        ses = Session()
        vc = ses.query(Media).filter(Media.name == "Проверка").first()
        ses.close()
        if vc:
            bot.send_voice(uid, vc.data, "Проверка отправки голоса")

    do_log(message.from_user, 'Main', to_log)
    bot.send_message(uid, rep, reply_markup=markup, parse_mode='markdown')
    bot.register_next_step_handler(message, next_step)


startb = 1
if startb:
    while True:
        try:
            bot.polling(none_stop=True, timeout=60)
        except Exception as ex:
            print(ex)
            bot.send_message(289208255, "Произошла ошибка")
            bot.send_message(289208255, str(ex))
            sleep(2)
