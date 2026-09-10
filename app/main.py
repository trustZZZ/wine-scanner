import logging
from fastapi import FastAPI
from app.logging_config import setup_logging
from app.core.config import settings

from app.api.v1 import router as api_v1_router  # это тот самый router из __init__.py

# Сначала настраиваем логирование
logger = setup_logging()
logger.info("Starting application...")
logger.info(f"Environment: {settings.APP_ENV}, Log Level: {settings.LOG_LEVEL}")

app = FastAPI(title="Wine Scanner API", version="0.1.0")

app.include_router(api_v1_router, prefix="/api/v1")
