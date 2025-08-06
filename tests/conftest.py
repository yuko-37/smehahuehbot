import pytest
import utils as u
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture(scope='session', autouse=True)
def setup():
    logger.info('----START----')
    u.load_from_env()
    yield
    logger.info('----END----')
