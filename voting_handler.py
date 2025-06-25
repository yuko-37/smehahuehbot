import random
import settings as s
import utils as u
import async_ai_requests as aair
import ai_requests as ai
import asyncio

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import get_vote_str
from io import BytesIO


class VotingHandler:
    def __init__(self, game):
        self.game = game

    def create_pairs_of_jokes_for_voting(self):
        game = self.game
        start = 0
        end = game.num_players
        jokes = [[index, data['it_joke'], player, 0] for index, (player, data)
                 in zip(range(start, end), game.players.items())]
        start += game.num_players
        end += game.num_players
        jokes += [[index, data['an_joke'], player, 0] for index, (player, data)
                  in zip(range(start, end), game.players.items())]
        start += game.num_players
        end += len(game.ai_players)
        jokes += [[index, data['it_joke'], player, 0] for index, (player, data)
                  in zip(range(start, end), game.ai_players.items())]
        start += len(game.ai_players)
        end += len(game.ai_players)
        jokes += [[index, data['an_joke'], player, 0] for index, (player, data)
                  in zip(range(start, end), game.ai_players.items())]
        game.jokes = jokes

        sj = jokes[:]
        random.shuffle(sj)
        pairs = [[sj[i], sj[i-1]] for i in range(1, len(sj), 2)]
        game.joke_pairs = pairs

        for player, data in game.players.items():
            data['pairs'] = [ind for ind, p in enumerate(pairs) if p[0][2] != player and p[1][2] != player]
            data['player_pair_index'] = 0

    def ask_players_for_jokes_voting(self, bot):
        for player, data in self.game.players.items():
            self.ask_a_player_for_jokes_voting(player, bot)

        if self.game.ai_is_active:
            self.collect_ai_votes()

    def collect_ai_votes(self):
        game = self.game
        jokes_for_ai_voting = dict()
        for ai_player in game.ai_players:
            joke_pairs = [pair for pair in game.joke_pairs if pair[0][2] != ai_player and pair[1][2] != ai_player]
            jokes_for_ai_voting[ai_player] = u.get_user_voting_prompt(joke_pairs)

        responses = asyncio.run(aair.request_ai_votes_async(jokes_for_ai_voting))
        for r in responses:
            items = r[1].lstrip("[").rstrip("]").split(",")
            for item in items:
                try:
                    joke_ind = int(item)
                    self.update_score(joke_ind)
                    joke = game.jokes[joke_ind]
                    print(f"{r[0]} voted for {joke[2]} #{joke[0]}. {joke[1]}")
                except ValueError as e:
                    print(f'Failed to parse vote [{item}] from [{r[0]}]: {e}')

    def update_score(self, joke_ind):
        game = self.game
        joke = game.jokes[joke_ind]
        joke[3] += 1
        voted_player = joke[2]
        game.score[voted_player] = game.score[voted_player] + 1 if voted_player in game.score else 1

    def ask_a_player_for_jokes_voting(self, player, bot):
        game = self.game
        data = game.players[player]
        chat_id = data['chat_id']
        pair_ind = data['pairs'][data['player_pair_index']]
        joke_pair = game.joke_pairs[pair_ind]

        markup = InlineKeyboardMarkup()
        text = f'Проголосуйте за понравившуюся шутку: \n\n'
        text += f'\t1. {joke_pair[0][1]}\n\n'
        text += f'\t2. {joke_pair[1][1]}\n\n'
        button1 = InlineKeyboardButton(f'Шутка 1', callback_data=f'vote_{joke_pair[0][0]}')
        button2 = InlineKeyboardButton(f'Шутка 2', callback_data=f'vote_{joke_pair[1][0]}')
        markup.row(button1, button2)

        bot.send_message(chat_id, text, reply_markup=markup)

    def process_player_vote(self, call, bot):
        game = self.game
        player = call.from_user.username
        vote = int(call.data.replace('vote_', ''))
        self.update_score(vote)
        data = game.players[player]
        data['player_pair_index'] += 1
        player_pair_index = data['player_pair_index']

        if player_pair_index < len(game.players[player]['pairs']):
            self.ask_a_player_for_jokes_voting(player, bot)
        else:
            data['finish_voting'] = True
            bot.send_message(call.message.chat.id, 'Ждём пока все проголосуют...')

            if player == game.admin:
                game.waiting_for_players(bot, 'finish_voting', 'votes')
                self.process_voting_results(bot)

    def process_voting_results(self, bot):
        game = self.game
        sorted_jokes = sorted(game.jokes, key=lambda x: (-x[3]))
        text = 'Результаты: \n\n'

        sorted_score = dict(sorted(game.score.items(), key=lambda x: (-x[1], x[0])))
        for player, score in sorted_score.items():
            text += f"{player}: {score}\n"

        text += '\nТоповые шутки: \n\n'

        for joke_data in sorted_jokes[:5]:
            if joke_data[3] > 0:
                text += f'{joke_data[3]} {get_vote_str(joke_data[3])}:\n{joke_data[1]}\n\n'

        for player_data in game.players.values():
            bot.send_message(player_data['chat_id'], text)

        if s.GENERATE_MOST_LIKED_JOKE_IMAGE:
            most_liked_joke = sorted_jokes[0][1]
            print(f"generating image for joke: {most_liked_joke}")
            image_data = ai.generate_image_as_bytes(most_liked_joke)

            for player_data in game.players.values():
                image = BytesIO(image_data)
                image.name = 'generate.png'
                bot.send_photo(chat_id=player_data['chat_id'], photo=image, caption=None)

        game.finish(bot, success=True)
