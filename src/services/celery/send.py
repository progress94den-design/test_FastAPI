from services.celery.tasks import send_email_on_after_register


def send_welcomes(
    email: str,
):
    send_email_on_after_register.delay(
        emails=email,
    )


if __name__ == "__main__":
    for i in range(5):
        send_welcomes(f"den{i}@gmail.com")
