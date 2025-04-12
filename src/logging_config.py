import re
from logging import Filter
from src.config import settings


class WerkzeugFilter(Filter):
    """Фильтр для очистки логов uvicorn (аналог werkzeug)."""
    def filter(self, record):
        record.msg = re.sub(r'^\d+\.\d+\.\d+\.\d+ - - \[\d+\/\w+\/\d+[:\d+ ]+\] ', '', record.msg)
        record.msg = record.msg.rstrip('- ')
        return True

def setup_logging(test_mode: bool):
    """Инициализация логирования (возможно, добавь другие настройки при test_mode=True)."""
    pass  # пока ничего не делаем, всё берётся из logging.ini
