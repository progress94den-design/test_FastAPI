from services.mailing.send_welcome import send_welcome
from services.taskiq.taskiq_broker import broker


@broker.task
async def send_welcome_email(email: str):
    await send_welcome(email)
