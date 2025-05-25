import time
from random import choice
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import game as game
import settings as s
import votes as v


def ask_users_for_sj_pattern(bot):
    for userdata in s.users.values():
        chat_id = userdata['chat_id']

        sj_patterns = userdata['user_sj_patterns']
        text = f'Выберите один из шаблонов: \n\n\t1. {sj_patterns[0]}\n\t2. {sj_patterns[1]}\n\n'

        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton("Шаблон 1", callback_data="pattern_0")
        button2 = InlineKeyboardButton("Шаблон 2", callback_data="pattern_1")
        markup.add(button1, button2)
        bot.send_message(chat_id, text, reply_markup=markup)


def ask_user_to_finish_joke(call, bot):
    username = call.from_user.username
    sj_patterns = s.users[username]['user_sj_patterns']
    user_subjects = s.users[username]['user_subject_set']
    subject = choice(list(s.subjects - user_subjects))
    index = int(call.data.replace('pattern_', ''))

    if sj_patterns[index].startswith('[]'):
        subject = subject.capitalize()

    sj_chosen = sj_patterns[index].replace('[]', subject)
    s.users[username]['sj_chosen'] = sj_chosen
    text = f'Добейте шутку: \n\n{sj_chosen}'

    sent_msg = bot.send_message(call.message.chat.id, text)
    bot.register_next_step_handler(sent_msg, process_joke_creation, bot=bot)


def process_joke_creation(message, bot):
    username = message.from_user.username
    sj_chosen = s.users[username]['sj_chosen']
    s_joke = sj_chosen.replace('...', f' {message.text}.')
    s.users[username]['s_joke'] = s_joke
    bot.send_message(message.chat.id, 'Ждём других игроков...')

    if username == s.admin:
        waiting_jokes(bot)
        v.ask_users_for_joke_voting(bot)


def waiting_jokes(bot):
    iter = 0
    finished = {}
    while game.is_active() and len(finished) < s.num_users:
        iter += 1
        if iter > s.MAX_WAIT_ITER:
            print('слишком долгое ожидание шуток...')
            game.finish(bot)
            return
        time.sleep(3)
        finished = {u for u in s.users if 's_joke' in s.users[u]}
        log = f'''шутки #{iter}: [{len(finished)}\\{s.num_users}]{'' if (len(finished) == s.num_users) else ' ждём ' + str(s.users.keys()-finished) + '...'}'''
        print(log)

