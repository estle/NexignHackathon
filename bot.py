import telebot
from telebot import types
import videoediting
from videoediting import render

bot = telebot.TeleBot('5648080215:AAG62dzCqEvT9NrWTWn-I-IhefRX4_iACBw')


def men():
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    run = types.KeyboardButton('Поехали!')
    info = types.KeyboardButton('ℹ️ Обо мне')
    menu.add(run, info)
    return menu


def go(message):

    bot.send_message(message.from_user.id, "Окей, теперь ждём пару секунд)", reply_markup=men())
    render(message.text)
    vid = open("output_video.mp4", 'rb')

    bot.send_video_note(message.from_user.id, vid)


@bot.message_handler(content_types=['video'])
def handle_docs_photo(message):
    try:
        chat_id = message.chat.id

        file_info = bot.get_file(message.video.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = 'wow' + ".mp4"
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        msk1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        stich = types.KeyboardButton('Мани реин')
        stars = types.KeyboardButton('Звёздочки')
        cat = types.KeyboardButton('Котик')
        mob = types.KeyboardButton('Монстрик')
        msk1.add(stich, stars, mob, cat)

        bot.send_message(message.chat.id, "Отлично! Теперь выберите эмоцию))", reply_markup=msk1)
    except Exception as e:
        bot.reply_to(message.chat.id, e)


@bot.message_handler(content_types=['video_note'])
def handle_docs_photo(message):
    try:
        chat_id = message.chat.id

        file_info = bot.get_file(message.video_note.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = 'wow' + ".mp4"
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        msk1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        hat = types.KeyboardButton('Мани реин')
        stars = types.KeyboardButton('Звёздочки')
        cat = types.KeyboardButton('Котик')
        mob = types.KeyboardButton('Монстрик')
        msk1.add(hat, stars, mob, cat)

        bot.send_message(message.from_user.id, "Отлично! Теперь выберите маску 👺", reply_markup=msk1)
    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":

        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?", reply_markup=men())

    elif message.text == "Поехали!":
        bot.send_message(message.from_user.id, "Загрузи видео или кружочек", reply_markup=men())

    elif message.text == "/start":

        bot.send_message(message.from_user.id, "Ой, кто здесь?", reply_markup=men())

    elif message.text == "ℹ️ Обо мне":
        bot.send_message(message.from_user.id, "Хочешь примерить маску или шапку, которой нет в популярных соц сетях?")
        bot.send_message(message.from_user.id,
                         "Тогда тебе к нам, загрузи видео с собой или другом, выбери маску и наслаждайся✌️",
                         reply_markup=men())

    elif message.text == "Кто ты?":
        bot.send_message(message.from_user.id, "Меня зовут страж и я охраняю твой vайб", reply_markup=men())

    elif message.text == "Стич" or 'Звёздочки' or 'Котик' or 'Монстрик':
        go(message)
    else:
        bot.send_message(message.from_user.id, "Моя твоя не понимайт. Напиши /help.", reply_markup=men())


bot.polling(none_stop=True, interval=0)
