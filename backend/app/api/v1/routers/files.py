"""File upload / object-storage endpoints (biosensor raw signal files,
attachments). Files are streamed to the S3-compatible bucket; a presigned
URL is returned rather than the raw file so access can expire."""
import uuid

from fastapi import APIRouter, Depends, UploadFile, status

from app.core.deps import CurrentUser, get_current_user
from app.infrastructure.storage.s3_client import ensure_bucket_exists, generate_presigned_url, upload_file

router = APIRouter(prefix="/files", tags=["File Storage"])


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload(file: UploadFile, current_user: CurrentUser = Depends(get_current_user)):
    ensure_bucket_exists()
    key = f"uploads/{current_user.id}/{uuid.uuid4()}-{file.filename}"
    upload_file(file.file, key, content_type=file.content_type)
    return {"key": key, "url": generate_presigned_url(key)}


@router.get("/{key:path}/url")
async def get_download_url(key: str, current_user: CurrentUser = Depends(get_current_user)):
    return {"url": generate_presigned_url(key)}
