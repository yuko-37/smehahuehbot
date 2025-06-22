import settings as s
import utils as u

from random import randint
from registration import Registration
from player_input_handler import PlayerInputHandler
from joke_handler import JokeHandler
from voting_handler import VotingHandler


class Game:
    def __init__(self):
        self.registration = Registration(self)
        self.player_input_handler = PlayerInputHandler(self)
        self.joke_handler = JokeHandler(self)
        self.voting_handler = VotingHandler(self)

        self.active = False
        self.code = None
        self.admin = None
        self.admin_chat_id = None
        self.num_players = None
        self.players = dict()
        self.ai_is_active = True
        self.ai_players = dict()
        self.items = set()
        self.animals = set()
        self.it_joke_templates = list()
        self.an_joke_templates = list()
        self.jokes = list()
        self.joke_pairs = list()
        self.score = dict()

    def start(self, message):
        admin = message.from_user.username
        admin_chat_id = message.chat.id

        self.active = True
        self.code = f'/{randint(1000, 10000)}'
        self.admin = admin
        self.admin_chat_id = admin_chat_id

        self.it_joke_templates = u.load_from_file(s.IT_JOKE_TEMPLATES_PATH)
        self.an_joke_templates = u.load_from_file(s.AN_JOKE_TEMPLATES_PATH)

        print(f'\n---------[START] game {self.code} started\n')

    def is_active(self):
        res = self.active
        res = res and self.code is not None
        res = res and self.admin is not None
        res = res and self.admin_chat_id is not None
        return res

    def code_formatted(self):
        return f'*{self.code[1:]}*' if self.code is not None else None

    def notify_all_except(self, text, me, bot):
        for player, player_data in self.players.items():
            if self.is_active() and player != me:
                bot.send_message(player_data['chat_id'], text, parse_mode='Markdown')
            else:
                return

    def finish(self, bot, message=None, success=False):
        if success:
            for player, data in self.players.items():
                text = f'Конец игры. {player}, спасибо за участие!'
                bot.send_message(data['chat_id'], text)

        else:
            code_f = self.code_formatted()
            if message is not None:
                player = message.from_user.username
                print(f'request to end the game {self.code} has been sent by [{player}]')
                text = f'игра {code_f} прервана по запросу *{player}*'
            else:
                print(f'game {self.code} was interrupted due to timeout')
                text = f'игра {code_f} прервана из-за таймаута'

            for player, data in self.players.items():
                bot.send_message(data['chat_id'], text, parse_mode='Markdown')

        print(f'\n---------[END] game {self.code} is over\n')
        self.reset()

    def reset(self):
        self.active = False
        self.code = None
        self.admin = None
        self.admin_chat_id = None
        self.num_players = None
        self.players = dict()
        self.ai_is_active = True
        self.ai_players = dict()
        self.items = set()
        self.animals = set()
        self.it_joke_templates = list()
        self.an_joke_templates = list()
        self.jokes = list()
        self.joke_pairs = list()
        self.score = dict()

