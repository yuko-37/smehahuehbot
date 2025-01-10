from telebot import TeleBot
from config import BOT_TOKEN
from pathlib import Path
from random import choice

import time
import settings as s
import admin as a
import getdata as gt
import jokes as j

bot = TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['admin', 'админ'])
def admin_command_handler(message):
    a.process_admin(message, bot)


@bot.message_handler(commands=['end'])
def end_command_handler(message):
    s.finish_game(bot)


@bot.message_handler(content_types=['text'])
def start_game_handler(message):
    username = message.from_user.username
    print(f'{username}: {message.text}')
    if s.game_active():
        username = message.from_user.username

        if username not in s.users:
            if message.text == s.game_code:
                gt.process_user(message, bot)
            else:
                bot.send_message(message.chat.id, f'Получите код игры {s.game_code}')
    else:
        text = 'Игра ещё не началась. Подождите, пока админ запустит игру.'
        bot.send_message(message.chat.id, text)


@bot.callback_query_handler(func=lambda call: call.data.startswith('joke_'))
def callback_handler(call):
    if s.game_active():
        username = call.from_user.username
        sj_patterns = s.users[username]['user_sj_patterns']
        user_subjects = s.users[username]['user_subject_set']
        subject = choice(list(s.subjects - user_subjects))
        index = int(call.data.replace('joke_', ''))
        sj_chosen = sj_patterns[index].replace('[]', subject)
        s.users[username]['sj_chosen'] = sj_chosen
        text = f'Добейте шутку: \n\n{sj_chosen}'

        sent_msg = bot.send_message(call.message.chat.id, text)
        bot.register_next_step_handler(sent_msg, j.process_joke_creation, bot=bot)

        bot.delete_message(chat_id=call.message.chat.id, 
                                message_id=call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('vote_'))
def callback_handler(call):
    if s.game_active():
        username = call.from_user.username
        s.users[username]['sj_vote'] = call.data.replace('vote_', '')

        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        sent_msg = bot.send_message(call.message.chat.id, 'Ждём пока все проголосуют...')

        if username == s.admin:
            iter = 1
            finished = {}
            while len(finished) < s.num_users:
                print(f'голосование {iter}...{finished}')
                iter += 1
                if iter > 100:
                    print('Слишком долгое ожидание')
                    s.finish_game()
                    return
                time.sleep(3)
                finished = {u for u in s.users if 'sj_vote' in s.users[u]}

            j.process_voting_results(bot)
            s.finish_game(bot)





bot.infinity_polling()