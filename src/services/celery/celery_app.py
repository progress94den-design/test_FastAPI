from celery import Celery

from core.config import settings


celery_app = Celery(
    "services.celery.celery",
    broker=str(settings.rabbitmq.url),
    backend="rpc://",
    include=["services.celery.tasks"],
)
# celery --app services.celery.celery_app  worker --pool=solo --loglevel INFO
