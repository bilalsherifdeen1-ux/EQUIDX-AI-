"""S3-compatible object storage client wrapper (works with MinIO locally,
AWS S3 / any S3-compatible provider in production)."""
import boto3
from botocore.client import Config

from app.core.config import get_settings

settings = get_settings()


def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=settings.S3_ENDPOINT_URL,
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
        region_name=settings.S3_REGION,
        config=Config(signature_version="s3v4"),
    )


def ensure_bucket_exists(bucket: str = settings.S3_BUCKET_NAME) -> None:
    client = get_s3_client()
    existing = [b["Name"] for b in client.list_buckets().get("Buckets", [])]
    if bucket not in existing:
        client.create_bucket(Bucket=bucket)


def upload_file(file_obj, key: str, bucket: str = settings.S3_BUCKET_NAME, content_type: str | None = None) -> str:
    extra_args = {"ContentType": content_type} if content_type else {}
    get_s3_client().upload_fileobj(file_obj, bucket, key, ExtraArgs=extra_args)
    return key


def generate_presigned_url(key: str, bucket: str = settings.S3_BUCKET_NAME, expires_in: int = 3600) -> str:
    return get_s3_client().generate_presigned_url(
        "get_object", Params={"Bucket": bucket, "Key": key}, ExpiresIn=expires_in
    )


def delete_file(key: str, bucket: str = settings.S3_BUCKET_NAME) -> None:
    get_s3_client().delete_object(Bucket=bucket, Key=key)
