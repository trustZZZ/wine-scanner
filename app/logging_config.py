# app/logging_config.py
import logging
import sys
from app.core.config import settings

def setup_logging():
    """
    Настраивает корневой logger.
    Формат: [LEVEL] [TIMESTAMP] [MODULE] MESSAGE
    """
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    formatter = logging.Formatter(
        fmt="[%(levelname)s] [%(asctime)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.handlers.clear()  # убираем дефолтные хендлеры, если есть
    root_logger.addHandler(handler)

    # Отключаем propagation для библиотек, чтобы не дублировать логи (опционально)
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    logging.getLogger("alembic").setLevel(logging.INFO)

    return root_logger
