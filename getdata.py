import settings as s


def process_user(message, bot):
    username = message.from_user.username
    if username is None:
        text = f'Пожалуйста, установите username в своём telegram профиле и наберите /{s.game_code} опять.'
    elif username in s.users:
        text = f'{username}, вы уже в игре.'
    else:
        s.users.add(username)
        text = f'{username}, добро пожаловать на борт Смехокорабля!'

    bot.send_message(message.chat.id, text)
    
    text = "Введите через запятую 3 предмета во мн.ч.: "
    sent_msg = bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(sent_msg, process_subjects, bot=bot)

def process_subjects(message, bot):
    s.subjects |= set(message.text.split(','))

    text = "Введите через запятую 3 животных во мн.ч.: "
    sent_msg = bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(sent_msg, process_animals, bot=bot)

def process_animals(message, bot):
    s.animals |= set(message.text.split(','))
    bot.send_message(message.chat.id, 'Спасибо')
    bot.send_message(message.chat.id, str(s.subjects))
    bot.send_message(message.chat.id, str(s.animals))
