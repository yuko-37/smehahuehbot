import settings as s
import random


def process_admin(message, bot):
    username = message.from_user.username

    if s.admin is None:
        s.admin = message.from_user.username

    if username == s.admin:
        text = f'Введите количество игроков (от {s.MIN_USERS}-{s.MAX_USERS}): '
        sent_msg = bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(sent_msg, process_num_user, bot=bot)
    else:
        bot.send_message(message.chat.id, 'Игра в процессе, админ уже назначен.')


def process_num_user(message, bot):
    num_text = message.text
    try:
        num_users = int(num_text)
        if (num_users < s.MIN_USERS or num_users > s.MAX_USERS):
            num_users = None
            raise Exception

        s.start_game(num_users)
        text = f'Получите код игры {s.game_code}'
        bot.send_message(message.chat.id, text)

    except Exception as e:
        print(e)
        text = f'Ошибка ввода. Пожалуйста введите целое число от {s.MIN_USERS} до {s.MAX_USERS}: '
        sent_msg = bot.reply_to(message, text)
        bot.register_next_step_handler(sent_msg, process_num_user, bot=bot)

    
