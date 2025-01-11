from random import randint
from pathlib import Path

import settings as s


def start(message):
    admin = message.from_user.username
    admin_chat_id = message.chat.id

    s.game_is_active = True
    s.game_code = f'/{randint(1000, 10000)}'
    s.admin = admin
    s.admin_chat_id = admin_chat_id
    s.num_users = None
    s.subjects = set()
    s.users = dict()

    path = Path(s.SJ_PATTERNS_PATH)
    content = path.read_text()
    s.sj_patterns = content.splitlines()
    print(f'\n---------[START] игра {s.game_code} началась\n')


def finish(bot, message=None):
    if message is not None:
        username = message.from_user.username
        print(f'отправлен запрос на окончание игры {s.game_code} [{username}]')
        if s.game_code is not None:
            if username not in s.users:
                bot.send_message(message.chat.id, f'{username}, игра {s.game_code} прервана по вашему запросу')
            if s.admin_chat_id is not None and username != s.admin and s.admin not in s.users:
                bot.send_message(s.admin_chat_id, f'{username}, игра {s.game_code} прервана по запросу {username}')
        else:
            bot.send_message(message.chat.id, f'{username}, нет активной игры для завершения.')

    for username, userdata in s.users.items():
        text = f'Конец игры. {username}, спасибо за участие!'
        bot.send_message(userdata['chat_id'], text)

    if s.game_code is not None:
        print(f'\n---------[END] игра {s.game_code} завершена\n')
    else:
        print(f'сброс данных')

    s.game_is_active = False
    s.game_code = None
    s.admin = None
    s.admin_chat_id = None
    s.num_users = None
    s.subjects = set()
    s.users = dict()
    s.sj_patterns = list()


def is_active(): 
    res = s.game_is_active
    res = res and s.game_code is not None
    res = res and s.admin is not None
    return res