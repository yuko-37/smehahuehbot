import time

import game as game
import settings as s
import jokes as j


def ask_users_for_animals(bot):
    for userdata in s.users.values():
        text = ('Давай теперь добавим через запятую 3 или более животных во множ.числе: ')
        sent_msg = bot.send_message(userdata['chat_id'], text)
        bot.register_next_step_handler(sent_msg, process_animals, bot=bot)


def process_animals(message, bot):
    if message.text == '/end':
        game.finish(bot, message)
        return

    username = message.from_user.username
    user_animal_set = extract_wordset(message)
    s.users[username]['user_animal_set'] = user_animal_set
    s.animals |= user_animal_set

    bot.send_message(message.chat.id, 'Ждём других игроков...')

    if username == s.admin:
        waiting_animals(bot)
        j.ask_users_for_sj_pattern(bot)


def extract_wordset(message):
    wordset = {sub.strip() for sub in message.text.split(',')}
    wordset.discard('')
    return wordset


def waiting_animals(bot):
    finished = {}
    iter = 0
    while game.is_active() and len(finished) < s.num_users:
        iter += 1
        if iter > s.MAX_WAIT_ITER:
            print('cлишком долгое ожидание предметов...')
            game.finish(bot)
            return
        time.sleep(3)
        finished = {u for u in s.users if 'user_animal_set' in s.users[u]}
        log = f'''животные #{iter}: [{len(finished)}\{s.num_users}]{'' if (len(finished) == s.num_users) else ' ждём ' + str(s.users.keys()-finished) + '...'}'''
        print(log)