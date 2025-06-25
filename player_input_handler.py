import settings as s
import utils as u


class PlayerInputHandler:
    def __init__(self, game):
        self.game = game

    def start_collecting_data(self, bot):
        self.game.items = u.extract_word_set_from_file(s.AI_ITEMS_PATH)
        self.game.animals = u.extract_word_set_from_file(s.AI_ANIMALS_PATH)
        self.ask_players_for_items(bot)

    def ask_players_for_items(self, bot):
        for player_data in self.game.players.values():
            text = ('Напишите 2 или более произвольных предмета (бытовые приборы, одежда, мебель, что угодно)'
                    ' во множ.числе, можете украсить свои слова сочными прилагательными, например, весёлые кирпичи): ')
            sent_msg = bot.send_message(player_data['chat_id'], text)
            bot.register_next_step_handler(sent_msg, self.process_items, bot=bot)

    def process_items(self, message, bot):
        game = self.game
        player = message.from_user.username
        player_items = self.extract_data(message, bot)
        game.players[player]['items'] = player_items
        game.items |= player_items
        self.ask_player_for_animals(message, bot)

    def extract_data(self, message, bot):
        if message.text == '/end':
            self.game.finish(bot, message)
            return set()

        return u.extract_word_set(message.text)

    def ask_player_for_animals(self, message, bot):
        player = message.from_user.username
        text = ('А теперь давай добавим 2 или более животных во множ.числе, '
                'как и раньше можешь добавить характеристику, к примеру, розовые слоники): ')
        sent_msg = bot.send_message(self.game.players[player]['chat_id'], text)
        bot.register_next_step_handler(sent_msg, self.process_animals, bot=bot)

    def process_animals(self, message, bot):
        game = self.game
        player = message.from_user.username
        player_animals = self.extract_data(message, bot)
        game.players[player]['animals'] = player_animals
        game.animals |= player_animals

        bot.send_message(message.chat.id, 'Ждём других игроков...')

        if player == game.admin:
            game.waiting_for_players(bot, 'animals', 'data')
            game.joke_handler.offer_it_joke_templates_to_players(bot)

