import telebot
from telebot import types

bot = telebot.TeleBot('7789037765:AAFzNMCVoyG6Of0MBtOPZ4p50hmybM7QUMA')

menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
words = types.KeyboardButton("Добавить слова")
jokes = types.KeyboardButton("Шутки")
menu.add(words, jokes)

back = types.ReplyKeyboardMarkup(resize_keyboard=True)
back_button = types.KeyboardButton("Назад")
back.add(back_button)

@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    bot.send_message(message.chat.id, "VERSION     7", reply_markup = menu)

@bot.message_handler(content_types=['text'])
def text_message(message):
    if message.text == 'Назад':
        bot.send_message(message.chat.id, 'Снова в меню', reply_markup = menu)
    elif message.text == 'Добавить слова':
        bot.send_message(message.chat.id, 'Добавьте слова через запятую', 
                         reply_markup = types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, add_words)
    elif message.text == 'Шутки':
        bot.send_message(message.chat.id, 'Вы нажали Шутки', reply_markup = back)
    else:
        bot.send_message(message.chat.id, 'не знаю что это', reply_markup = menu)

def add_words(message):
    print(message.text)

bot.infinity_polling()