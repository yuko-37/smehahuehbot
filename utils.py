import os

from pathlib import Path
from random import sample, choice
from dotenv import load_dotenv


def prepare_joke_template(template, from_items, except_items=None):
    items = (from_items - except_items) if except_items is not None else from_items
    random_item = choice(list(items))
    from_items.remove(random_item)

    if template.startswith('[]'):
        random_item = random_item.capitalize()

    return template.replace('[]', random_item)


def get_user_prompt(*templates):
    prompt = "Создай шутку на основе шаблонов: "
    for template in templates:
        prompt += f'\n{template}'
    return prompt


def get_user_voting_prompt(joke_pairs):
    prompt = [f"({pair[0][0]}. {pair[0][1]}; {pair[1][0]}. {pair[1][1]})" for pair in joke_pairs]
    return str(prompt)


def extract_random_two_from(item_list):
    sublist = sample(item_list, 2)
    for item in sublist:
        item_list.remove(item)
    return sublist


def extract_word_set_from_file(file_path):
    path = Path(file_path)
    content = path.read_text()
    return extract_word_set(content)


def extract_word_set(text: str):
    word_set = {sub.strip() for sub in text.split(',')}
    word_set.discard('')
    return word_set


def load_from_file(file_path):
    path = Path(file_path)
    content = path.read_text()
    return content.splitlines()


def load_from_env():
    load_dotenv(override=True)
    bot_api_token = os.getenv('BOT_API_TOKEN')
    openai_api_key = os.getenv('OPENAI_API_KEY')
    anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
    google_api_key = os.getenv('GOOGLE_API_KEY')
    deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
    end_ind = 5

    if bot_api_token:
        print(f"Bot API Token exists and begins {bot_api_token[:end_ind]}")

    if openai_api_key:
        print(f"OpenAI API Key exists and begins {openai_api_key[:end_ind]}")
    else:
        print("OpenAI API Key not set")

    if anthropic_api_key:
        print(f"Anthropic API Key exists and begins {anthropic_api_key[:end_ind]}")
    else:
        print("Anthropic API Key not set")

    if google_api_key:
        print(f"Google API Key exists and begins {google_api_key[:end_ind]}")
    else:
        print("Google API Key not set")

    if deepseek_api_key:
        print(f"Deepseek API Key exists and begins {deepseek_api_key[:end_ind]}")
    else:
        print("DeepSeek API Key not set")


def get_vote_str(num):
    match num:
        case 1:
            return 'голос'
        case 2 | 3 | 4:
            return 'голоса'
        case _:
            return 'голосов'


