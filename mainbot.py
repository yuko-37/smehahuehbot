import telebot as tlb
from pathlib import Path

import settings as s
import admin as a
import getdata as gt

bot = tlb.TeleBot('7789037765:AAFzNMCVoyG6Of0MBtOPZ4p50hmybM7QUMA')


@bot.message_handler(commands=['admin', 'админ'])
def admin_command_handler(message):
    a.process_admin(message, bot)


@bot.message_handler(commands=['start', 'старт'])
def admin_command_handler(message):
    if s.game_code is None:
        text = 'Игра ещё не началась.'
    else:
        text = f'Получите код игры {s.game_code}'
    bot.send_message(message.chat.id, text)


@bot.message_handler(func=lambda message: message.text.startswith('/'))
def start_game_handler(message):
    if message.text == s.game_code:
        gt.process_user(message, bot)

bot.infinity_polling()