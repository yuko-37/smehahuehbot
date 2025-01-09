import telebot as tlb
from telebot import types
from pathlib import Path
from random import choice

import settings as s
import admin as a
import getdata as gt
import jokes as j

bot = tlb.TeleBot('Token')


@bot.message_handler(commands=['admin', 'админ'])
def admin_command_handler(message):
    a.process_admin(message, bot)


@bot.message_handler(func=lambda message: message.text.startswith('/'))
def start_game_handler(message):
    if message.text == s.game_code:
        gt.process_user(message, bot)
    elif s.game_code is None:
        bot.send_message(message.chat.id, 'Игра ещё не началась.')
    else:
        bot.send_message(message.chat.id, f'Получите код игры {s.game_code}')


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    username = call.from_user.username
    joke_patterns = s.users[username]['joke_patterns']
    subject = choice(list(s.subjects))
    ind = 0

    if call.data == "joke_1":
        ind = 0
    elif call.data == "joke_2":
        ind = 1
    
    joke = joke_patterns[ind].replace('[]', subject)
    s.users[username]['joke'] = joke
    text = f'Добейте шутку: \n{joke}'

    sent_msg = bot.send_message(call.message.chat.id, text)
    bot.register_next_step_handler(sent_msg, j.process_joke_choice, bot=bot)

    bot.delete_message(chat_id=call.message.chat.id, 
                            message_id=call.message.message_id)


bot.infinity_polling()