import telebot as tlb

bot = tlb.TeleBot('7789037765:AAFzNMCVoyG6Of0MBtOPZ4p50hmybM7QUMA')
animals = []


@bot.message_handler(commands=['start'])
def start_handler(message):
    text = "Введите через запятую 5 животных: "
    sent_msg = bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(sent_msg, animals_handler)

def animals_handler(message):
    global animals
    animals += message.text.split(',')
    bot.send_message(message.chat.id, 'Спасибо\n' + str(animals))

def choose_joke_handler(message):
    text = "You've entered:\n " + message.text + "\n"
    text += "Choose a joke:\n *Joke 1*, *Joke 2*"
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, make_joke_handler)

def make_joke_handler(message):
    text = "Now you will make a joke from: " + message.text
    bot.reply_to(message, text)

bot.infinity_polling()
