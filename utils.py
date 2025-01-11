import game as game
import settings as s


def notify_all_except(text, me, bot):
    for username, userdata in s.users.items():
        if game.is_active() and username != me:
            bot.send_message(userdata['chat_id'], text, parse_mode='Markdown')
        else:
            return


def formatted_code():
    return f'*{s.game_code[1:]}*' if s.game_code is not None else None