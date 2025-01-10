from pathlib import Path
from random import sample, randint

MIN_USERS = 2
MAX_USERS = 8
MAX_CONNECT_ITER = 100

game_is_active = False
game_code = None
admin = None
num_users = 0
subjects = set()
users = dict()
subject_joke_patterns = list()

def game_active(): 
    res = game_is_active
    res = res and game_code is not None
    res = res and admin is not None
    return res

def register_user(username, chat_id):
    global users

    users[username] = dict()
    users[username]['chat_id'] = int(chat_id)
    sj_patterns = sample(subject_joke_patterns, 2)
    users[username]['user_sj_patterns'] = sj_patterns

    print(f'register {username}')


def register_user_subject_set(username, user_subject_set):
    global users
    global subjects

    users[username]['user_subject_set'] = user_subject_set
    subjects |= user_subject_set


def start_game(num_of_users):
    global game_is_active
    global game_code
    global admin
    global num_users
    global subjects
    global users
    global subject_joke_patterns

    game_is_active = True
    game_code = f'/{randint(1000, 10000)}'
    num_users = num_of_users
    subjects = set()
    users = dict()

    path = Path('smehahuehbot/text/joke-subjects.txt')
    content = path.read_text()
    subject_joke_patterns = content.splitlines()
    print(f'\n---------[START] игра {game_code} началась\n')


def finish_game(bot):
    global game_is_active
    global game_code
    global admin
    global num_users
    global subjects
    global subject_joke_patterns
    global users
    
    log = f'\n---------[END] игра {game_code} завершена\n'
    game_is_active = False
    game_code = None
    admin = None
    num_users = 0
    subjects = set()
    subject_joke_patterns = list()

    for username, userdata in users.items():
        text = f'Конец игры. {username}, спасибо за участие!'
        bot.send_message(userdata['chat_id'], text)
    
    print(log)
    users = dict()

