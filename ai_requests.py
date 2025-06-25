import openai
import anthropic
import os
import settings as s
import utils as u
import base64

from google import genai
from google.genai import types


SYSTEM_MSG = ('Ты участвуешь в игре по созданию шуток на основе шаблонов. '
              'В каждом шаблоне нужно заменить многоточие ... на текст, '
              'чтобы получилась шутка = шаблон - ... + текст. '
              'В итоге вывести только список шуток разделённых новой строкой. Без дополнительных слов.')


def generate_image_as_bytes(joke):
    response = openai.images.generate(
        model="dall-e-3",
        prompt=f"Сгенерируй забавную картинку в стиле мема под шутку: {joke}",
        size="1024x1024",
        n=1,
        response_format="b64_json"
    )

    image_base64 = response.data[0].b64_json
    image_data = base64.b64decode(image_base64)
    return image_data


def ask_ai_for_jokes(ai_player, *joke_templates):
    prompts = u.get_user_prompt(joke_templates)
    jokes_str = None
    if ai_player == 'gpt':
        jokes_str = ask_gpt(prompts)
    elif ai_player == 'Claude':
        jokes_str = ask_claude(prompts)
    elif ai_player == 'Gemini':
        jokes_str = ask_gemini(prompts)
    elif ai_player == 'DeepSeek':
        jokes_str = ask_deepseek(prompts)
    else:
        print(f'ERROR: unknown ai_player {ai_player}.')

    if jokes_str is not None:
        jokes = jokes_str.splitlines()
        if len(jokes) == 2:
            return jokes

    return None


def ask_gpt(user_prompt):
    prompts = [
        {'role': 'system', 'content': SYSTEM_MSG},
        {'role': 'user', 'content': user_prompt}
    ]

    try:
        completion = openai.chat.completions.create(
            model=s.GPT_MODEL,
            messages=prompts,
            temperature=0.4
        )
        result = completion.choices[0].message.content
        return result

    except Exception as ex:
        print(ex)
        return None


def ask_claude(user_prompt):
    try:
        response = anthropic.Anthropic().messages.create(
            model=s.ANTHROPIC_MODEL,
            max_tokens=100,
            system=SYSTEM_MSG,
            messages=[
                {'role': 'user', 'content': user_prompt}
            ]
        )
        return response.content[0].text

    except Exception as ex:
        print(ex)
        return None


def ask_gemini(user_prompt):
    try:
        gemini = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))
        response = gemini.models.generate_content(
            model=s.GOOGLE_MODEL,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_MSG,
                temperature=0.4
            ),
            contents=user_prompt
        )
        return response.text

    except Exception as ex:
        print(ex)
        return None


def ask_deepseek(user_prompt):
    try:
        client = openai.OpenAI(api_key=os.getenv('DEEPSEEK_API_KEY'), base_url="https://api.deepseek.com")

        response = client.chat.completions.create(
            model=s.DEEPSEEK_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_MSG},
                {"role": "user", "content": user_prompt},
            ],
            stream=False
        )

        return response.choices[0].message.content

    except Exception as ex:
        print(ex)
        return None
