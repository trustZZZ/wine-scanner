import os
from celery import Celery

celery_app = Celery(
    "wine_scanner",
    broker_connection_retry_on_startup=True,
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/1"),
    include=["app.tasks.tasks"],
)


celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Moscow",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,        # 5 минут максимум на задачу
    task_soft_time_limit=240,   # мягкий лимит — 4 минуты
)
