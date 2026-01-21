import uuid

from miniopy_async import Minio
from fastapi import UploadFile

from core.config import settings


class MinioService:
    def __init__(
        self,
        endpoint: str,
        access_key: str,
        secret_key: str,
        secure: bool = False,
    ):
        self.client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
        )

    async def ensure_bucket(self, bucket_name) -> None:
        exists = await self.client.bucket_exists(bucket_name)
        if not exists:
            await self.client.make_bucket(bucket_name)

    async def upload_file(
        self,
        bucket_name: str,
        file: UploadFile,
        user_id: uuid.UUID,
        obj_id: uuid.UUID,
    ) -> str:
        await self.ensure_bucket(bucket_name)

        object_name = f"{user_id}/{obj_id}/{uuid.uuid4()}-{file.filename}"

        await self.client.put_object(
            bucket_name=bucket_name,
            object_name=object_name,
            data=file.file,
            length=file.size,
            content_type=file.content_type,
        )

        return f"{bucket_name}/{object_name}"


minio_service: MinioService = MinioService(
    endpoint=settings.minio.endpoint,
    access_key=settings.minio.access_key,
    secret_key=settings.minio.secret_key,
)
