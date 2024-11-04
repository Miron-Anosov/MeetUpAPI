"""Picture tasks celery."""

import asyncio

from src.core.apps.tasks.email.celery_postman import send_mail_background
from src.core.apps.tasks.img_utils.db_update_user import add_path_to_user
from src.core.apps.tasks.img_utils.del_file import del_temp_file
from src.core.apps.tasks.img_utils.download import download_file
from src.core.apps.tasks.img_utils.upload import upload_file_to_s3
from src.core.apps.tasks.img_utils.watermark import add_watermark
from src.core.settings.constants import IntKeys


async def watermark_proc(
    receiver_id: str,
    file: bytes,
    filename: str,
) -> None:
    """Create image watermark task."""
    file_path: str = await download_file(
        file=file, receiver_id=receiver_id, filename=filename
    )

    watermark_image_path = add_watermark(file_path=file_path)

    s3_path = await upload_file_to_s3(
        file_path=watermark_image_path, filename=filename
    )

    # TODO Add logger + try/except

    await asyncio.gather(
        del_temp_file(file_path=file_path),
        del_temp_file(file_path=watermark_image_path),
        add_path_to_user(file_path=s3_path, user_id=receiver_id),
    )


def background_task_send_email(
    emails: tuple[str, str], names: tuple[str, str]
) -> None:
    """Send email task."""
    send_mail_background.delay(
        target_email=emails[IntKeys.TARGET_USER_FOR_EMAIL],
        name=names[IntKeys.AUTH_USER_FOR_EMAIL],
        users_email=emails[IntKeys.AUTH_USER_FOR_EMAIL],
    )
    send_mail_background.delay(
        target_email=emails[IntKeys.AUTH_USER_FOR_EMAIL],
        name=names[IntKeys.TARGET_USER_FOR_EMAIL],
        users_email=emails[IntKeys.TARGET_USER_FOR_EMAIL],
    )
