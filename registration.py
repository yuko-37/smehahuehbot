import settings as s
import utils as u
import time

from random import randrange


class Registration:
    def __init__(self, game):
        self.game = game

    def register_ai_players(self):
        game = self.game
        for ai_player in s.AI_PLAYERS:
            game.ai_players[ai_player] = dict()
            index = randrange(len(game.it_joke_templates))
            game.ai_players[ai_player]['it_joke_template'] = game.it_joke_templates.pop(index)
            index = randrange(len(game.an_joke_templates))
            game.ai_players[ai_player]['an_joke_template'] = game.an_joke_templates.pop(index)
            print(f'register AI player [{ai_player}]')

    def process_player(self, message, bot):
        game = self.game
        player = message.from_user.username

        if player is None:
            text = f'Пожалуйста, установите username в своём telegram профиле и введите /{game.code} опять.'
            bot.send_message(message.chat.id, text)
            return
        elif player not in game.players:
            self.register_player(player, int(message.chat.id))

            if player == game.admin:
                bot.send_message(message.chat.id, f'Вы назначены администратором игры {game.code_formatted()}.',
                                 parse_mode='Markdown')
            else:
                bot.send_message(message.chat.id, f'*{player}*, добро пожаловать на борт Смехокорабля!',
                                 parse_mode='Markdown')

            bot.send_message(message.chat.id, 'Ждём подключения других игроков...')
            game.notify_all_except(f'*{player}* присоединился к игре...', player, bot)

        if player == game.admin:
            self.waiting_for_players(message, bot)

    def register_player(self, player, chat_id):
        game = self.game
        game.players[player] = dict()
        game.players[player]['chat_id'] = int(chat_id)
        game.players[player]['it_joke_templates'] = u.extract_random_two_from(game.it_joke_templates)
        game.players[player]['an_joke_templates'] = u.extract_random_two_from(game.an_joke_templates)
        print(f'register player [{player}]')

    def waiting_for_players(self, message, bot):
        game = self.game
        if game.is_active():

            if message.text == s.NO:
                game.num_players = len(game.players)
                ai_and_players = list(game.players.keys()) + list(game.ai_players.keys())
                log_players: str = f'{len(ai_and_players)}: {", ".join(ai_and_players)}'
                text = f'В игре участвуют {log_players}'

                if game.is_active():
                    bot.send_message(game.admin_chat_id, text)

                print(f'Currently in the game {log_players}')
                game.player_input_handler.start_collecting_data(bot)
                return

            elif message.text == s.YES:
                print((f'waiting for players at the admin\'s request, players[{len(game.players)}] '
                       f'{", ".join(game.players.keys())}...'))
                time.sleep(5)

            elif message.text == '/end':
                game.finish(bot, message)
                return

            iterations = 0
            while game.is_active() and len(game.players) < s.MIN_PLAYERS:
                iterations += 1
                if iterations > s.MAX_CONNECT_ITER:
                    print(f'waiting for players time out...[{len(game.players)}\\{s.MIN_PLAYERS}]')
                    game.finish(bot)
                    return
                time.sleep(3)
                print((f'join attempt #{iterations}: [{len(game.players)}\\{s.MIN_PLAYERS}] '
                       f'{list(game.players.keys())}...'))

            ai_and_players = list(game.players.keys()) + list(game.ai_players.keys())
            players_str = '\n'.join(ai_and_players)
            text = f'Сейчас игроков {len(ai_and_players)}: \n{players_str}\n\nПодождать ещё? {s.YES} {s.NO}'

            if game.is_active():
                sent_msg = bot.send_message(game.admin_chat_id, text)
                bot.register_next_step_handler(sent_msg, self.waiting_for_players, bot=bot)
