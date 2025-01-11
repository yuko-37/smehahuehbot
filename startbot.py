from telebot import TeleBot
from config import BOT_TOKEN

import game as game
import settings as s
import utils as u
import registration as r
import jokes as j
import votes as v


bot = TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['admin', 'админ'])
def admin_command_handler(message):
    username = message.from_user.username

    if s.admin is None:
        game.start(message)
        print(f'назначение админа [{s.admin}]')
        r.process_user(message, bot)
    elif username == s.admin:
        bot.send_message(message.chat.id, f'Вы назначены администратором игры *{u.game_code_as_num()}*.',
                             parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, f'Админ *{s.admin}* уже назначен. Получите код игры {s.game_code}', 
                         parse_mode='Markdown')


@bot.message_handler(commands=['end'])
def end_command_handler(message):
    game.finish(bot, message)


@bot.message_handler(content_types=['text'])
def start_game_handler(message):
    if game.is_active():
        username = message.from_user.username

        if username not in s.users:
            if len(s.users) < s.MAX_USERS:
                if message.text == s.game_code:
                    r.process_user(message, bot)
                else:
                    bot.send_message(message.chat.id, f'Получите код игры {s.game_code}')
            else:
                bot.send_message(message.chat.id, 'Нет свободных мест. Подождите окончания текущей игры.')

    else:
        bot.send_message(message.chat.id, f'Для начала игры, введите {s.ADMIN}.')


@bot.callback_query_handler(func=lambda call: call.data.startswith('pattern_'))
def callback_handler(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    if game.is_active():
        j.ask_user_to_finish_joke(call, bot)


@bot.callback_query_handler(func=lambda call: call.data.startswith('vote_'))
def callback_handler(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    if game.is_active():
        v.process_user_vote(call, bot)


bot.infinity_polling()