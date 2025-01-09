import settings as s
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from random import sample

def process_jokes(message, bot):
    username = message.from_user.username
    jokes = sample(s.subject_jokes, 2)
    s.users[username]['joke_patterns'] = jokes
    text = f'Выберите: \n1. {jokes[0]}\n2. {jokes[1]}\n'

    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton("Шутка 1", callback_data="joke_1")
    button2 = InlineKeyboardButton("Шутка 2", callback_data="joke_2")
    markup.add(button1, button2)
    bot.send_message(message.chat.id, text, reply_markup=markup)



def process_joke_choice(message, bot):
    username = message.from_user.username
    joke = s.users[username]['joke']
    answer = f'Получилось в итоге: \n{joke}{message.text}\n'
    bot.send_message(message.chat.id, answer)