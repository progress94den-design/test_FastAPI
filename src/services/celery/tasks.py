import asyncio

from services.celery.celery_app import celery_app
from services.mailing.send_welcome import send_welcome


@celery_app.task
def send_email_on_after_register(emails: list[str]):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(send_welcome(recipient=emails))
    except Exception:
        print("Failed to send email")
    finally:
        loop.close()
