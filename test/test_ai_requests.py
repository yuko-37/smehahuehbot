import utils as u
import settings as s
import ai_requests as air


u.load_from_env()
templates = "Тапки совсем как собаки, потому что ...", "Бутылки совсем ка люди, когда ..."
user_prompt = u.get_user_prompt(templates)

# print('\nGPT: \n' + air.ask_gpt(user_prompt))
# print('\n\nClaude: \n' + air.ask_claude(user_prompt))
# print('\n\nGemini: \n' + air.ask_gemini(user_prompt))
# print('\n\nDeepSeek: \n' + air.ask_deepseek(user_prompt))

for ai_player in s.AI_PLAYERS:
    jokes = air.ask_ai_for_jokes(ai_player, templates)
    print(f'{ai_player}: {jokes}')
