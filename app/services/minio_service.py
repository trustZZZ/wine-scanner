import os
import boto3
from botocore.exceptions import ClientError

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://minio:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
BUCKET_NAME = os.getenv("BUCKET_NAME", "wine-labels")

s3_client = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
    region_name="us-east-1",
    use_ssl=False,
)

def ensure_bucket():
    """Создаёт бакет, если его нет."""
    try:
        s3_client.head_bucket(Bucket=BUCKET_NAME)
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            s3_client.create_bucket(Bucket=BUCKET_NAME)
        else:
            raise

def upload_image(file_bytes: bytes, object_name: str) -> str:
    """Загружает байты как файл в MinIO и возвращает публичный URL."""
    ensure_bucket()
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=object_name,
        Body=file_bytes,
        ContentType="image/jpeg",
    )
    # Для локальной разработки можно отдавать прямой URL к MinIO
    return f"{MINIO_ENDPOINT}/{BUCKET_NAME}/{object_name}"
