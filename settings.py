from pathlib import Path

admin = None
num_users = None

animals = {'бегемоты', 'жирафы'}
subjects = {'туфли', 'тапки', 'часы'}
users = {}

game_code = None


path = Path('smehahuehbot/text/joke-subjects.txt')
content = path.read_text()

subject_jokes = content.splitlines()
