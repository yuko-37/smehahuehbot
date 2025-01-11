import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import game as game
import settings as s


def ask_users_for_joke_voting(bot):
    for username, userdata in s.users.items():
        chat_id = userdata['chat_id']
        s_jokes = {u:s.users[u]['s_joke'] for u in s.users if u != username}

        markup = InlineKeyboardMarkup()
        text = f'Проголосуйте за понравившуюся шутку: \n\n'
        buttons = list()

        ind = 1
        for user, joke in s_jokes.items():
            text += f'\t{ind}. {joke}\n\n'
            button = InlineKeyboardButton(f'Шутка {ind}', callback_data=f'vote_{user}')
            buttons.append(button)

            if ind % 2 == 0:
                markup.row(buttons[0], buttons[1])
                buttons = list()
            elif ind == len(s_jokes):
                markup.add(button)

            ind += 1

        bot.send_message(chat_id, text, reply_markup=markup)


def process_user_vote(call, bot):
    username = call.from_user.username
    s.users[username]['sj_vote'] = call.data.replace('vote_', '')
    bot.send_message(call.message.chat.id, 'Ждём пока все проголосуют...')

    if username == s.admin:
        waiting_votes(bot)
        process_voting_results(bot)


def waiting_votes(bot):
    iter = 0
    finished = {}
    while game.is_active() and len(finished) < s.num_users:
        iter += 1
        if iter > s.MAX_WAIT_ITER:
            print('cлишком долгое ожидание голосования...')
            game.finish(bot)
            return
        time.sleep(3)
        finished = {u for u in s.users if 'sj_vote' in s.users[u]}
        log = f'''голосование #{iter}: [{len(finished)}\{s.num_users}]{'' if (len(finished) == s.num_users) else ' ждём ' + str(s.users.keys()-finished) + '...'}'''
        print(log)

def process_voting_results(bot):
    res = dict()
    votes = [s.users[u]['sj_vote'] for u in s.users]
    for vote in votes:
        if vote not in res:
            res[vote] = 0
        res[vote] += 1

    text = 'Результаты: \n\n'
    sorted_res = sorted(res.items(), key=lambda item: item[1], reverse=True)
    for user, score in sorted_res:
        info = f'{user} - {score} {get_vote_str(score)}\n'
        info += s.users[user]['s_joke'] + '\n\n'
        text += info
    
    for userdata in s.users.values():
        bot.send_message(userdata['chat_id'], text)
    
    game.finish(bot)


def get_vote_str(num):
    match num:
        case 1:
            return 'голос'
        case 2 | 3 | 4:
            return 'голоса'
        case _:
            return 'голосов'