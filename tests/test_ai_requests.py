import settings as s
import ai_requests as air
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_ask_ai_for_jokes():
    templates = "Тапки совсем как собаки, потому что ...", "Бутылки совсем ка люди, когда ..."

    for ai_player in s.AI_PLAYERS:
        logger.info(f'check {ai_player}')
        jokes = air.ask_ai_for_jokes(ai_player, templates)
        assert len(jokes) == 2
        print(f'{ai_player}: {jokes}')
