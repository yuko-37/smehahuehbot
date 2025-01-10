import settings as s
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from random import sample
import time

def process_jokes(bot):
    for userdata in s.users.values():
        chat_id = userdata['chat_id']

        sj_patterns = userdata['user_sj_patterns']
        text = f'Выберите один из шаблонов: \n\n\t1. {sj_patterns[0]}\n\t2. {sj_patterns[1]}\n\n'

        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton("Шутка 1", callback_data="joke_0")
        button2 = InlineKeyboardButton("Шутка 2", callback_data="joke_1")
        markup.add(button1, button2)
        bot.send_message(chat_id, text, reply_markup=markup)


def process_joke_creation(message, bot):
    username = message.from_user.username
    sj_chosen = s.users[username]['sj_chosen']
    s_joke = sj_chosen.replace('...', ' ' + message.text)
    s.users[username]['s_joke'] = s_joke
    bot.send_message(message.chat.id, 'Ждём других игроков...')

    if username == s.admin:
        iter = 1
        finished = {}
        while len(finished) < s.num_users:
            print(f'шутки {iter}...{finished}')
            iter += 1
            if iter > 100:
                print('Слишком долгое ожидание')
                s.finish_game()
                return
            time.sleep(3)
            finished = {u for u in s.users if 's_joke' in s.users[u]}
    
        process_joke_voting(bot)


def process_joke_voting(bot):
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
        info = f'{user} - {score}\n'
        info += s.users[user]['s_joke'] + '\n\n'
        text += info
    
    for userdata in s.users.values():
        bot.send_message(userdata['chat_id'], text)

