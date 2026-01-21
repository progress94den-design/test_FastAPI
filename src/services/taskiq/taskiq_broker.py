from taskiq_aio_pika import AioPikaBroker

from core.config import settings


broker = AioPikaBroker(
    url=str(settings.taskiq.url),
)

# taskiq worker services:broker --fs-discover --tasks-pattern "**/tasks"
