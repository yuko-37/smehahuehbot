import settings as s
import utils as u
import os

from telebot import TeleBot
from game import Game

u.load_from_env()
bot = TeleBot(os.getenv('BOT_API_TOKEN'))
game = Game()
print('start listening...')


@bot.message_handler(commands=['admin', 'админ'])
def admin_command_handler(message):
    player = message.from_user.username

    if game.admin is None:
        game.start(message)
        print(f'admin assignment [{game.admin}]')
        game.registration.register_ai_players()
        game.registration.process_player(message, bot)

    elif player == game.admin:
        bot.send_message(message.chat.id, f'Вы назначены администратором игры {game.code_formatted()}.',
                         parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, f'Админ *{game.admin}* уже назначен. Получите код игры {game.code}',
                         parse_mode='Markdown')


@bot.message_handler(commands=['end'])
def end_command_handler(message):
    if game.is_active():
        player = message.from_user.username
        if player == game.admin or player in game.players:
            game.finish(bot, message)
        else:
            bot.send_message(message.chat.id, 'Вы не можете прервать текущую игру, вы не являетесь участником.')
    else:
        game.reset()
        print('reset settings')


@bot.message_handler(content_types=['text'])
def start_game_handler(message):
    if game.is_active():
        player = message.from_user.username

        if player not in game.players:
            if len(game.players) < s.MAX_PLAYERS:
                if message.text == game.code:
                    game.registration.process_player(message, bot)
                else:
                    bot.send_message(message.chat.id, f'Получите код игры {game.code}')
            else:
                bot.send_message(message.chat.id, 'Нет свободных мест. Подождите окончания текущей игры.')

    else:
        bot.send_message(message.chat.id, f'Для начала игры, введите /admin.')


@bot.callback_query_handler(func=lambda call: call.data.startswith('it_template_'))
def callback_handler(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    if game.is_active():
        game.joke_handler.ask_player_to_finish_it_joke(call, bot)


@bot.callback_query_handler(func=lambda call: call.data.startswith('an_template_'))
def callback_handler(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    if game.is_active():
        game.joke_handler.ask_player_to_finish_an_joke(call, bot)


@bot.callback_query_handler(func=lambda call: call.data.startswith('vote_'))
def callback_handler(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    if game.is_active():
        game.voting_handler.process_player_vote(call, bot)


bot.infinity_polling()
