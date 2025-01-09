import settings as s
import jokes as j


def process_user(message, bot):
    username = message.from_user.username
    if username is None:
        text = f'Пожалуйста, установите username в своём telegram профиле и наберите /{s.game_code} опять.'
    elif username in s.users:
        text = f'{username}, вы уже в игре.'
    else:
        s.users[username] = {}
        text = f'{username}, добро пожаловать на борт Смехокорабля!'

    bot.send_message(message.chat.id, text)

    # # CHEAT
    # j.process_jokes(message, bot)
    # print('cheat')
    # # END CHEAT

    # if False: 
    
    text = "Введите через запятую 3 предмета во мн.ч.: "
    sent_msg = bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(sent_msg, process_subjects, bot=bot)

def process_subjects(message, bot):
    add_data_from_msg_to_set(message, s.subjects)

    text = "Введите через запятую 3 животных во мн.ч.: "
    sent_msg = bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(sent_msg, process_animals, bot=bot)

def process_animals(message, bot):
    add_data_from_msg_to_set(message, s.animals)

    print(s.subjects)
    print(s.animals)
    
    j.process_jokes(message, bot)


def add_data_from_msg_to_set(message, dataset):
    dataset |= set(message.text.split(','))
    dataset.discard('')
