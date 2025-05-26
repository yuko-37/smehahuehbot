import time
from random import sample

import game as game
import settings as s
import utils as u
import subjects as sb


def process_user(message, bot):
    username = message.from_user.username

    if username is None:
        text = f'Пожалуйста, установите username в своём telegram профиле и введите /{s.game_code} опять.'
        bot.send_message(message.chat.id, text)
        return
    elif username not in s.users:
        register_user(username, int(message.chat.id))

        if username == s.admin:
            bot.send_message(message.chat.id, f'Вы назначены администратором игры {u.formatted_code()}.',
                             parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, f'*{username}*, добро пожаловать на борт Смехокорабля!', parse_mode='Markdown')

        bot.send_message(message.chat.id, 'Ждём подключения других игроков...')
        u.notify_all_except(f'*{username}* присоединился к игре...', username, bot)

    if username == s.admin:
        waiting_users(message, bot)


def register_user(username, chat_id):
    s.users[username] = dict()
    s.users[username]['chat_id'] = int(chat_id)
    sj_patterns = sample(s.sj_patterns, 2)
    s.users[username]['user_sj_patterns'] = sj_patterns

    print(f'регистрация пользователя [{username}]')


def register_ai_user(ainame):
    s.ai_users[ainame] = dict()
    s.ai_users[ainame]['ai_sj_pattern'] = sample(s.sj_patterns, 1)[0]

    print(f'регистрация ИИ [{ainame}]')

def waiting_users(message, bot):
    if game.is_active():

        if message.text == s.NO:
            s.num_users = len(s.users)
            ai_and_users = list(s.users.keys()) + list(s.ai_users.keys())
            text = f'В игре участвуют {len(ai_and_users)}: {", ".join(ai_and_users)}'

            if s.admin_chat_id is not None:
                bot.send_message(s.admin_chat_id, text)

            print(text)
            sb.ask_users_for_subjects(bot)
            return
        
        elif message.text == s.YES:
            print(f'ожидание игроков по желанию админа, игроки[{len(s.users)}] {", ".join(s.users.keys())}...')
            time.sleep(5)
        
        elif message.text == '/end':
            game.finish(bot, message)
            return

        iter = 0
        while game.is_active() and len(s.users) < s.MIN_USERS:
            iter += 1
            if iter > s.MAX_CONNECT_ITER:
                print(f'cлишком долгое ожидание игроков...[{len(s.users)}\{s.MIN_USERS}]')
                game.finish(bot)
                return
            time.sleep(3)
            print(f'подключение #{iter}: [{len(s.users)}\{s.MIN_USERS}] {list(s.users.keys())}...')

        ai_and_users = list(s.users.keys()) + list(s.ai_users.keys())
        users_str = '\n'.join(ai_and_users)
        text = f'Сейчас игроков {len(ai_and_users)}: \n{users_str}\n\nПодождать ещё? {s.YES} {s.NO}'
        
        if s.admin_chat_id is not None:
            sent_msg = bot.send_message(s.admin_chat_id, text)
            bot.register_next_step_handler(sent_msg, waiting_users, bot=bot)
