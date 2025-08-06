import os
import utils as u
import logging
from tempfile import NamedTemporaryFile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_extract_word_set_from_file():
    with NamedTemporaryFile("w+", delete=False) as tmp:
        tmp.write("item1, item2, item3, item4, item5, item6")
        tmp_path = tmp.name

    try:
        limit = 3
        result = u.extract_word_set_from_file(tmp_path, limit)
        assert len(result) == limit
    finally:
        os.remove(tmp_path)

