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


def finish(bot, message=None, success=False):
    code = s.game_code
    items = s.users
    reset()

    if success:
        for name, data in items.items():
            text = f'Конец игры. {name}, спасибо за участие!'
            bot.send_message(data['chat_id'], text)

    else:
        if message is not None:
            username = message.from_user.username
            print(f'отправлен запрос на окончание игры {code} [{username}]')
            text = f'игра {code} прервана по запросу {username}'
        else:
            print(f'игра {code} прервана из-за таймаута')
            text = f'игра {code} прервана из-за таймаута'

        for name, data in items.items():
            bot.send_message(data['chat_id'], text)

    print(f'\n---------[END] игра {code} завершена\n')


def is_active(): 
    res = s.game_is_active
    res = res and s.game_code is not None
    res = res and s.admin is not None
    res = res and s.admin_chat_id is not None
    return res


def reset():
    s.game_is_active = False
    s.game_code = None
    s.admin = None
    s.admin_chat_id = None
    s.num_users = None
    s.subjects = set()
    s.users = dict()
    s.sj_patterns = list()