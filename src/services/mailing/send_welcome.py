from services.mailing.send_mail import send_email


async def send_welcome(recipient: str):
    subject = "Welcome to our website"
    plain_content = f"""
        Dear {recipient}, welcome to our website!
        Thank you for registering
        """
    html_content = ""

    await send_email(
        recipient=recipient,
        subject=subject,
        plain_content=plain_content,
        html_content=html_content,
    )
