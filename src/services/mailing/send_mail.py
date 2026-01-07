import aiosmtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from core.config import settings


async def send_email(
    recipient: str,
    subject: str,
    plain_content: str,
    html_content: str = "",
):
    admin_email = settings.email.admin_email

    message = MIMEMultipart("alternative")
    message["From"] = admin_email
    message["To"] = recipient
    message["Subject"] = subject

    plain_text_message = MIMEText(
        plain_content,
        "plain",
        "utf-8",
    )
    message.attach(plain_text_message)

    if html_content:
        html_message = MIMEText(
            html_content,
            "html",
            "utf-8",
        )
        message.attach(html_message)

    await aiosmtplib.send(
        message,
        hostname=settings.email.host,
        port=settings.email.port,
    )
