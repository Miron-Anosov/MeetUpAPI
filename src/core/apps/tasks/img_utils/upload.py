"""Upload file."""

from src.core.apps.s3client import s3_client


async def upload_file_to_s3(file_path: str, filename: str) -> str:
    """Upload to S3 storage."""
    file_path = await s3_client.upload_object(
        file_path=file_path, object_name=filename
    )
    return file_path
