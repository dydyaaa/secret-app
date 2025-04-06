import logging
import aiohttp
import re
from logging import Filter
from src.config import settings


class WerkzeugFilter(Filter):
    """Фильтр для очистки логов uvicorn (аналог werkzeug)."""
    def filter(self, record):
        record.msg = re.sub(r'^\d+\.\d+\.\d+\.\d+ - - \[\d+\/\w+\/\d+[:\d+ ]+\] ', '', record.msg)
        record.msg = record.msg.rstrip('- ')
        return True


class LokiHandler(logging.Handler):
    """Асинхронный handler для отправки логов в Loki."""
    def __init__(self, url=settings.LOKI_URL, labels=None):
        super().__init__()
        self.url = url
        self.labels = labels or {"job": "fastapi_app"}

    async def emit_async(self, record):
        """Асинхронная отправка логов в Loki."""
        try:
            log_entry = self.format(record)
            timestamp = int(record.created * 1e9)

            payload = {
                "streams": [{
                    "stream": self.labels,
                    "values": [[str(timestamp), log_entry]]
                }]
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(self.url, json=payload, headers={"Content-Type": "application/json"}) as response:
                    if response.status != 204:
                        logging.error(f"Failed to send log to Loki: {response.status}")
        except Exception as e:
            self.handleError(record)

    def emit(self, record):
        """Синхронный вызов для совместимости, запускает асинхронный код."""
        import asyncio
        loop = asyncio.get_event_loop()
        if loop.is_running():
            loop.create_task(self.emit_async(record))
        else:
            asyncio.run(self.emit_async(record))


def setup_logging(test_mode: bool):
    """Инициализация логирования."""
    logging.getLogger('').addHandler(LokiHandler())