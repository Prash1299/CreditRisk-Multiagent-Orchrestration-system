from celery import Celery

from core.config import get_settings

settings = get_settings()
celery_app = Celery(
    "creditrisk",
    broker=settings.broker,
    backend=settings.result_backend,
    include=["worker.tasks"],
)
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_track_started=True,
)
