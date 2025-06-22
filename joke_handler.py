import utils as u
import settings as s
import async_ai_requests as aair
import asyncio
import time

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class JokeHandler:
    def __init__(self, game):
        self.game = game

    def offer_it_joke_templates_to_players(self, bot):
        for player_data in self.game.players.values():
            chat_id = player_data['chat_id']

            it_joke_templates = player_data['it_joke_templates']
            text = f'Выберите один из шаблонов: \n\n\t1. {it_joke_templates[0]}\n\t2. {it_joke_templates[1]}\n\n'

            markup = InlineKeyboardMarkup()
            button1 = InlineKeyboardButton("Шаблон 1", callback_data="it_template_0")
            button2 = InlineKeyboardButton("Шаблон 2", callback_data="it_template_1")
            markup.add(button1, button2)
            bot.send_message(chat_id, text, reply_markup=markup)

    def ask_player_to_finish_it_joke(self, call, bot):
        game = self.game
        player = call.from_user.username
        player_data = game.players[player]
        index = int(call.data.replace('it_template_', ''))
        prepared_it_joke_template = u.prepare_joke_template(player_data['it_joke_templates'][index],
                                                            game.items,
                                                            player_data['items'])
        player_data['prepared_it_joke_template'] = prepared_it_joke_template
        text = f'Добейте шутку: \n\n{prepared_it_joke_template}'

        sent_msg = bot.send_message(call.message.chat.id, text)
        bot.register_next_step_handler(sent_msg, self.process_it_joke, bot=bot)

    def process_it_joke(self, message, bot):
        game = self.game
        player = message.from_user.username
        prepared_it_joke_template = game.players[player]['prepared_it_joke_template']
        it_joke = prepared_it_joke_template.replace('...', f' {message.text}.')
        game.players[player]['it_joke'] = it_joke
        if player == game.admin:
            if game.ai_is_active:
                self.collect_ai_jokes()
        self.offer_an_joke_templates_to_a_player(message, bot)

    def offer_an_joke_templates_to_a_player(self, message, bot):
        game = self.game
        player = message.from_user.username
        an_joke_templates = game.players[player]['an_joke_templates']
        text = f'Выберите один из шаблонов: \n\n\t1. {an_joke_templates[0]}\n\t2. {an_joke_templates[1]}\n\n'

        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton("Шаблон 1", callback_data="an_template_0")
        button2 = InlineKeyboardButton("Шаблон 2", callback_data="an_template_1")
        markup.add(button1, button2)
        bot.send_message(game.players[player]['chat_id'], text, reply_markup=markup)

    def collect_ai_jokes(self):
        game = self.game
        ai_joke_templates = dict()
        for ai_player in s.AI_PLAYERS:
            it_joke_template = u.prepare_joke_template(game.ai_players[ai_player]['it_joke_template'], game.items)
            an_joke_template = u.prepare_joke_template(game.ai_players[ai_player]['an_joke_template'], game.animals)
            ai_joke_templates[ai_player] = [it_joke_template, an_joke_template]

        responses = asyncio.run(aair.request_ai_jokes_async(ai_joke_templates))
        for r in responses:
            print(f'ai jokes [{r[0]}]: {r[1]}\n')
            if r[1] is not None:
                jokes = r[1].split('\n')
                if len(jokes) == 2:
                    game.ai_players[r[0]]['it_joke'] = jokes[0]
                    game.ai_players[r[0]]['an_joke'] = jokes[1]

    def ask_player_to_finish_an_joke(self, call, bot):
        game = self.game
        player = call.from_user.username
        player_data = game.players[player]
        index = int(call.data.replace('an_template_', ''))
        prepared_an_joke_template = u.prepare_joke_template(player_data['an_joke_templates'][index],
                                                            game.items,
                                                            player_data['items'])
        player_data['prepared_an_joke_template'] = prepared_an_joke_template
        text = f'Добейте шутку: \n\n{prepared_an_joke_template}'

        sent_msg = bot.send_message(call.message.chat.id, text)
        bot.register_next_step_handler(sent_msg, self.process_an_joke, bot=bot)

    def process_an_joke(self, message, bot):
        game = self.game
        player = message.from_user.username
        prepared_an_joke_template = game.players[player]['prepared_an_joke_template']
        an_joke = prepared_an_joke_template.replace('...', f' {message.text}.')
        game.players[player]['an_joke'] = an_joke

        bot.send_message(message.chat.id, 'Ждём других игроков...')

        if player == game.admin:
            self.waiting_for_players_jokes(bot)
            game.voting_handler.create_pairs_of_jokes_for_voting()
            game.voting_handler.ask_players_for_jokes_voting(bot)

    def waiting_for_players_jokes(self, bot):
        game = self.game
        finished = {}
        iterations = 0
        while game.is_active() and len(finished) < game.num_players:
            iterations += 1
            if iterations > s.MAX_WAIT_ITER:
                print('waiting for players jokes time out...')
                game.finish(bot)
                return
            time.sleep(3)
            finished = {p for p in game.players if 'an_joke' in game.players[p]}
            players_waiting = str(game.players.keys() - finished)
            log = (f"jokes #{iterations}: [{len(finished)}\\{game.num_players}]"
                   f"{'' if (len(finished) == game.num_players) else f' ждём ' + players_waiting + '...'}")
            print(log)
