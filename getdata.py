import settings as s
import jokes as j
import time


def process_user(message, bot):
    username = message.from_user.username

    if username is None:
        text = f'Пожалуйста, установите username в своём telegram профиле и наберите /{s.game_code} опять.'
        bot.send_message(message.chat.id, text)
        return
    elif username not in s.users:
        s.register_user(username, int(message.chat.id))
        text = f'{username}, добро пожаловать на борт Смехокорабля!'
        bot.send_message(message.chat.id, text)
        bot.send_message(message.chat.id, 'Ждём подключения других игроков...')

    if username == s.admin:
        iter = 1
        while len(s.users) < s.num_users:
            print(f'подключение {iter}...{list(s.users.keys())}')
            iter += 1
            if iter > 100:
                print('Слишком долгое ожидание')
                s.finish_game()
                return
            time.sleep(3)

        for userdata in s.users.values():
            text = 'Введите через запятую 3 предмета во мн.ч.: '
            sent_msg = bot.send_message(userdata['chat_id'], text)
            bot.register_next_step_handler(sent_msg, process_subjects, bot=bot)


def process_subjects(message, bot):
    if (message.text == '/end'):
        s.finish_game(bot)
        return
    
    username = message.from_user.username
    user_subject_set = extract_wordset(message)
    s.register_user_subject_set(username, user_subject_set)
    bot.send_message(message.chat.id, 'Ждём других игроков...')

    if username == s.admin:
        iter = 1
        finished = {}
        while len(finished) < s.num_users:
            print(f'предметы {iter}...{finished}')
            iter += 1
            if iter > 100:
                print('Слишком долгое ожидание')
                s.finish_game()
                return
            time.sleep(3)
            finished = {u for u in s.users if 'user_subject_set' in s.users[u]}

        j.process_jokes(bot)


def extract_wordset(message):
    wordset = {sub.strip() for sub in message.text.split(',')}
    wordset.discard('')
    return wordset
