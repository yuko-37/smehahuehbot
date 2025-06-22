import utils as u
import settings as s
import async_ai_requests as aair
import asyncio

u.load_from_env()
print('...')


def test_request_ai_jokes_async():
    templates = "Тапки совсем как собаки, потому что ...", "Бутылки совсем ка люди, когда ..."
    ai_joke_templates = dict()
    ai_joke_templates[s.GPT] = templates
    ai_joke_templates[s.CLAUDE] = templates
    ai_joke_templates[s.GEMINI] = templates
    ai_joke_templates[s.DEEP_SEEK] = templates
    responses = asyncio.run(aair.request_ai_jokes_async(ai_joke_templates))

    for r in responses:
        print(f"{r[0]}:\n{r[1]}")


def test_request_ai_votes_async():
    data = [
        [[0, "Если бы у меня были вялые тапки, я бы стал экспертом по медленной ходьбе.", "player1", 0],
         [9, "Ревущие бегемоты умнее, чем кажутся, особенно когда дело касается выбора места для пикника.","player3", 0]],
        [[1, "Если бы не мечтательные котлеты, мир был бы скучным.", "player4", 0],
         [2, 'Если бы вспыльчивые лоси могли говорить, первое, что они бы сказали "Хватит меня бесить!"', "player2", 0]],
        [[4, "На первом свидании лучше не упоминать про трясущиеся пончики, потому что это может отпугнуть веганов.", "player5", 0],
         [7, "Неуравновешенные фламинго ведут себя идеально дома, но в ветклинике устраивают розовый переполох.", "player2", 0]],
        [[3, "Говорят, что гиперлупные чемоданы появляются там, где забыли зарядить телефон", "player3", 0],
         [8, "Пингвины — лучший способ познакомиться с противоположным полом, если не считать того, что они не умеют танцевать", "player1", 0]]
    ]
    prompt = u.get_user_voting_prompt(data)
    joke_pairs = dict()
    joke_pairs[s.GPT] = prompt
    joke_pairs[s.CLAUDE] = prompt
    joke_pairs[s.GEMINI] = prompt
    joke_pairs[s.DEEP_SEEK] = prompt
    responses = asyncio.run(aair.request_ai_votes_async(joke_pairs))

    for r in responses:
        print(f"{r[0]}:\n{r[1]}")


test_request_ai_votes_async()
