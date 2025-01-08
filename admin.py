import settings as s
import random


def process_admin(message, bot):
    username = message.from_user.username

    if s.admin is None:
        s.admin = message.from_user.username
    
    if username == s.admin:
        text = 'Введите количество игроков (от 2-8): '
        sent_msg = bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(sent_msg, process_num_user, bot=bot)
    else:
        bot.send_message(message.chat.id, 'Админ уже есть.')


def process_num_user(message, bot):
    num_text = message.text
    print('here ' + num_text)
    try:
        num_users = int(num_text)
        if (num_users < 2 or num_users > 8):
            num_users = None
            raise Exception
        s.num_users = num_users
        s.game_code = f'/{random.randint(1000, 10000)}'
        text = f'Получите код игры {s.game_code}'
        bot.send_message(message.chat.id, text)

    except Exception as e:
        print(e)
        text = 'Ошибка ввода. Пожалуйста введите целое число от 2 до 8: '
        sent_msg = bot.reply_to(message, text)
        bot.register_next_step_handler(sent_msg, process_num_user, bot=bot)

    print(s.num_users)
