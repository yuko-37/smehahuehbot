TEST_MODE = False

MIN_PLAYERS = 1
MAX_PLAYERS = 8
MAX_CONNECT_ITER = 100
MAX_WAIT_ITER = 100
GPT = 'gpt'
CLAUDE = 'Claude'
GEMINI = 'Gemini'
DEEP_SEEK = 'DeepSeek'

AI_PLAYERS = [GPT, CLAUDE, GEMINI, DEEP_SEEK]
# AI_PLAYERS = [GPT, GEMINI]
LIMIT_ITEMS = 3 * len(AI_PLAYERS)
GENERATE_MOST_LIKED_JOKE_IMAGE = True

GPT_MODEL = 'gpt-4o-mini'
ANTHROPIC_MODEL = 'claude-3-haiku-20240307'
ANTHROPIC_VERSION_HEADER = '2023-06-01'
GOOGLE_MODEL = 'gemini-2.0-flash'
DEEPSEEK_MODEL = 'deepseek-chat'

IT_JOKE_TEMPLATES_PATH = 'data/it_joke_templates.txt'
AN_JOKE_TEMPLATES_PATH = 'data/an_joke_templates.txt'
AI_ITEMS_PATH = 'data/ai_items.txt'
AI_ANIMALS_PATH = 'data/ai_animals.txt'

YES = '/yes'
NO = '/no'



