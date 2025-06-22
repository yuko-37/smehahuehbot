import os
import settings as s
import utils as u
import asyncio
import aiohttp


SYSTEM_MSG = ('Ты участвуешь в игре по созданию шуток на основе шаблонов. '
              'В каждом шаблоне нужно заменить многоточие ... на текст, '
              'чтобы получилась шутка = шаблон - ... + текст. '
              'В итоге вывести только список шуток разделённых новой строкой. Без дополнительных слов.')


SYSTEM_VOTING_MSG = ('Ты жюри в соревнованиях по шуткам, тебе дан список пар шуток, '
                     'из каждой пары шуток выбери наиболее удачную шутку '
                     'и в ответе укажи только номер-идентификатор шутки победителя. '
                     'Например, пришёл запрос:\n'
                     '[ (32.Тут шутка такая; 5.А тут ещё одна шутка.),  (1.Ещё одна смешная шутка; 43.Весёлая шутка)'
                     'В ответе только номер-идентификатор шутки победителя для каждой пары в виде списка, '
                     'например, [32, 1].')

TEST_MODE_JOKES_RESPONSES = [(s.GPT, ("Грустные пончики похожи на людей: они тоже могут быть с начинкой.\n"
                                     "Подозрительные страусы в квартире — это мило, пока они не начинают делать "
                                     "покупки в интернет-магазинах.")),
                     (s.CLAUDE, ("Страдающие брокколи не зависят от времени года, но почему-то всегда "
                                 "жалуются на погоду.\n"
                                 "Если вялые черепахи молчат слишком долго, значит они обдумывают план побега.")),
                     (s.GEMINI, ("На первом свидании лучше не упоминать про сочные тролли, "
                                 "потому что это может отпугнуть партнера, если он не разделяет твои интересы "
                                 "в фэнтези.\n"
                                 "Нежные пумы понимают человеческую речь, но притворяются глупыми, когда их просят "
                                 "принести тапочки.")),
                     (s.DEEP_SEEK, ("Липкие тапочки нарушают все законы физики, потому что они прилипают даже "
                                    "к потолку\n"
                                    "Прилипчивые осьминоги — лучший способ познакомиться с противоположным полом, "
                                    "если не считать того, что они не отпускают"))
                     ]


TEST_MODE_VOTES_RESPONSES = [(s.GPT, "1, 0, 5, 7, 3"),
                             (s.CLAUDE, "2, 3, 4, 0, 1"),
                             (s.GEMINI, "2, 3, 4, 7, 0"),
                             (s.DEEP_SEEK, "1, 3, 5, 7, 2")
                             ]


async def request_ai_jokes_async(ai_joke_templates):
    if s.TEST_MODE:
        return TEST_MODE_JOKES_RESPONSES
    else:
        print('start requesting AI API for jokes...')
        tasks = list()
        async with aiohttp.ClientSession() as session:
            if s.GPT in ai_joke_templates:
                user_prompt = u.get_user_prompt(ai_joke_templates[s.GPT])
                tasks.append(ask_gpt_async(session, user_prompt, SYSTEM_MSG))
            if s.CLAUDE in ai_joke_templates:
                user_prompt = u.get_user_prompt(ai_joke_templates[s.CLAUDE])
                tasks.append(ask_claude_async(session, user_prompt, SYSTEM_MSG))
            if s.GEMINI in ai_joke_templates:
                user_prompt = u.get_user_prompt(ai_joke_templates[s.GEMINI])
                tasks.append(ask_gemini_async(session, user_prompt, SYSTEM_MSG))
            if s.DEEP_SEEK in ai_joke_templates:
                user_prompt = u.get_user_prompt(ai_joke_templates[s.DEEP_SEEK])
                tasks.append(ask_deepseek_async(session, user_prompt, SYSTEM_MSG))
            responses = await asyncio.gather(*tasks)
            return responses


async def request_ai_votes_async(joke_pairs):
    if s.TEST_MODE:
        return TEST_MODE_VOTES_RESPONSES
    else:
        print('start requesting AI API for votes...')
        tasks = list()
        async with aiohttp.ClientSession() as session:
            if s.GPT in joke_pairs:
                tasks.append(ask_gpt_async(session, joke_pairs[s.GPT], SYSTEM_VOTING_MSG))
            if s.CLAUDE in joke_pairs:
                tasks.append(ask_claude_async(session, joke_pairs[s.CLAUDE], SYSTEM_VOTING_MSG))
            if s.GEMINI in joke_pairs:
                tasks.append(ask_gemini_async(session, joke_pairs[s.GEMINI], SYSTEM_VOTING_MSG))
            if s.DEEP_SEEK in joke_pairs:
                tasks.append(ask_deepseek_async(session, joke_pairs[s.DEEP_SEEK], SYSTEM_VOTING_MSG))
            responses = await asyncio.gather(*tasks)
            return responses


async def ask_gpt_async(session, user_prompt, system_prompt):
    api_url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json"
    }

    data = {
        "model": s.GPT_MODEL,
        "messages": [
            {"role": "system", "content": f"{system_prompt}"},
            {"role": "user", "content": f"{user_prompt}"}
        ],
        "temperature": 0.7
    }

    async with session.post(api_url, headers=headers, json=data) as response:
        res = await response.json()
        try:
            res = res["choices"][0]["message"]["content"].strip()
        except KeyError:
            print(res)
            res = None

        return s.GPT, res


async def ask_claude_async(session, user_prompt, system_prompt):
    api_url = "https://api.anthropic.com/v1/messages"

    headers = {
        "x-api-key": f"{os.getenv('ANTHROPIC_API_KEY')}",
        "anthropic-version": s.ANTHROPIC_VERSION_HEADER,
        "Content-Type": "application/json"
    }

    data = {
        "model": s.ANTHROPIC_MODEL,
        "max_tokens": 300,
        "system": system_prompt,
        "messages": [
            {"role": "user", "content": f"{user_prompt}"}
        ],
        "temperature": 0.7
    }

    async with session.post(api_url, headers=headers, json=data) as response:
        res = await response.json()
        try:
            res = res["content"][0]["text"].strip()
        except KeyError:
            print(res)
            res = None

        return s.CLAUDE, res


async def ask_gemini_async(session, user_prompt, system_prompt):
    api_url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
               f"{s.GOOGLE_MODEL}:generateContent?key={os.getenv('GOOGLE_API_KEY')}")

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [
            {"role": "user", "parts": [{"text": user_prompt}]}
        ],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 300
        }
    }

    async with session.post(api_url, headers=headers, json=data) as response:
        res = await response.json()
        try:
            res = res["candidates"][0]["content"]["parts"][0]["text"].strip()
        except KeyError:
            print(res)
            res = None

        return s.GEMINI, res


async def ask_deepseek_async(session, user_prompt, system_prompt):
    api_url = "https://api.deepseek.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}",
        "Content-Type": "application/json"
    }

    data = {
        "model": s.DEEPSEEK_MODEL,
        "messages": [
            {"role": "system", "content": f"{system_prompt}"},
            {"role": "user", "content": f"{user_prompt}"}
        ],
        "temperature": 0.7
    }

    async with session.post(api_url, headers=headers, json=data) as response:
        res = await response.json()
        try:
            res = res["choices"][0]["message"]["content"].strip()
        except KeyError:
            print(res)
            res = None

        return s.DEEP_SEEK, res
