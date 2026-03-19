from minio import Minio
import mimetypes

client = Minio(
    "localhost:9000",
    access_key="",
    secret_key="",
    secure=False
)

BUCKET_IMAGES     = "crop-images"
BUCKET_360_IMAGES = "crop-360-images"
BUCKET_360_VIDEOS = "crop-360-videos"

VIDEO_TYPES = {"video/mp4", "video/quicktime", "video/webm", "video/x-msvideo"}
IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}

def resolve_bucket(filename: str, content_type: str, is_360: bool = False) -> str:
    if content_type in VIDEO_TYPES:
        return BUCKET_360_VIDEOS
    if content_type in IMAGE_TYPES:
        return BUCKET_360_IMAGES if is_360 else BUCKET_IMAGES
    # Fallback: guess from extension
    guessed, _ = mimetypes.guess_type(filename)
    if guessed in VIDEO_TYPES:
        return BUCKET_360_VIDEOS
    return BUCKET_IMAGES

def upload_file(file_name: str, file_data, content_type: str, is_360: bool = False) -> dict:
    bucket = resolve_bucket(file_name, content_type, is_360)

    client.put_object(
        bucket,
        file_name,
        file_data,
        length=-1,
        part_size=10 * 1024 * 1024,
        content_type=content_type,
    )

    return {
        "url": f"http://localhost:9000/{bucket}/{file_name}",
        "bucket": bucket,
    }