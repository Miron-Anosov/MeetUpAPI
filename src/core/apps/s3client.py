"""S3 client."""

from contextlib import asynccontextmanager

import aiofiles
from aiobotocore.session import get_session

from src.core.settings.env import settings


class S3Client:
    """S3 client."""

    def __init__(
        self,
        aws_access_key_id: str,
        secret_key: str,
        endpoint_url: str,
        bucket_name: str,
    ) -> None:
        """Initialize the S3 client."""
        self.conf = {
            "aws_access_key_id": aws_access_key_id,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(
        self,
    ):
        """Return a S3 client."""
        async with self.session.create_client(
            "s3",
            **self.conf,
            verify=False,
        ) as client:
            yield client

    async def upload_object(
        self,
        file_path: str,
        object_name: str,
    ):
        """Upload a file to the S3 bucket."""
        async with self.get_client() as client:
            async with aiofiles.open(file=file_path, mode="rb") as fp:
                file_body = await fp.read()
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=object_name,
                    Body=file_body,
                )

                return f"{settings.s3.DOMAIN_URL}/{object_name}"


s3_client = S3Client(
    aws_access_key_id=settings.s3.AWS_ACCESS_KEY_ID,
    secret_key=settings.s3.AWS_SECRET_ACCESS_KEY,
    endpoint_url=settings.s3.ENDPOINT_URL,
    bucket_name=settings.s3.S3_BUCKET,
)
