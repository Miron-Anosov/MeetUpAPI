"""Send email to clients."""

from celery import shared_task
from celery.utils import log

from src.core.apps.tasks.email.send_for_match_email import send_email

log.get_task_logger(__name__)


@shared_task(name="send_email", max_retries=10)
def send_mail_background(
    target_email: str, name: str, users_email: str
) -> None:
    """Send email to clients."""
    log.logger.info(
        "email sent to %s <%s> from <%s>", name, target_email, users_email
    )
    send_email(target_email=target_email, name=name, users_email=users_email)
