import time

import game as game
import settings as s
import jokes as j


def ask_users_for_subjects(bot):
    for userdata in s.users.values():
        text = 'Введите через запятую 3 предмета во множ.числе: '
        sent_msg = bot.send_message(userdata['chat_id'], text)
        bot.register_next_step_handler(sent_msg, process_subjects, bot=bot)


def process_subjects(message, bot):
    username = message.from_user.username
    user_subject_set = extract_wordset(message)
    s.users[username]['user_subject_set'] = user_subject_set
    s.subjects |= user_subject_set

    bot.send_message(message.chat.id, 'Ждём других игроков...')

    if username == s.admin:
        waiting_subjects(bot)
        j.ask_users_for_sj_pattern(bot)


def extract_wordset(message):
    wordset = {sub.strip() for sub in message.text.split(',')}
    wordset.discard('')
    return wordset


def waiting_subjects(bot):
    finished = {}
    iter = 0
    while game.is_active() and len(finished) < s.num_users:
        iter += 1
        if iter > s.MAX_WAIT_ITER:
            print('cлишком долгое ожидание предметов...')
            game.finish(bot)
            return
        time.sleep(3)
        finished = {u for u in s.users if 'user_subject_set' in s.users[u]}
        log = f'''предметы #{iter}: [{len(finished)}\{s.num_users}]{'' if (len(finished) == s.num_users) else ' ждём ' + str(s.users.keys()-finished) + '...'}'''
        print(log)