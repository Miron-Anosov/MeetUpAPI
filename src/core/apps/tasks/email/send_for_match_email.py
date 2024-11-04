"""Email client."""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template

from src.core.settings.env import settings

template = Template("«Вы понравились $name! Почта участника: $email»")


def send_email(target_email: str, name: str, users_email: str):
    """Send email to somebody."""
    with smtplib.SMTP(
        settings.email.SMTP_HOST, settings.email.SMTP_PORT
    ) as server:
        server.starttls()
        server.login(settings.email.SMTP_USER, settings.email.SMTP_PASSWORD)

        email = MIMEMultipart()
        email["Subject"] = "«Возникла взаимная симпатия»"
        email["From"] = settings.email.SMTP_USER
        email["To"] = target_email

        message = template.substitute(name=name, email=users_email)
        email.attach(MIMEText(message, "plain"))
        text = email.as_string()

        server.sendmail(settings.email.SMTP_USER, target_email, text)
