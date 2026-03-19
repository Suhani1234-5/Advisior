from fastapi import APIRouter, UploadFile, Query, Depends, HTTPException
from services.minio_service import upload_file
from services.supabase_service import supabase
from services.auth_middleware import get_current_user

router = APIRouter()

@router.post("/upload")
async def upload_media(
    file: UploadFile,
    farm_id: str = Query(default=None),
    is_360: bool = Query(default=False),
    scan_type: str = Query(default="general"),
    current_user=Depends(get_current_user)  # 🔒 auth required
):
    try:
        content_type = file.content_type or "application/octet-stream"
        result = upload_file(file.filename, file.file, content_type, is_360)

        user_id = current_user.id
        bucket = result["bucket"]
        url = result["url"]
        is_video = bucket == "crop-360-videos"

        # Save record to Supabase — tagged with this user's ID
        if is_video or is_360:
            media_type = "video" if is_video else "360_image"
            supabase.table("farm_media").insert({
                "user_id": user_id,
                "farm_id": farm_id,
                "media_url": url,
                "bucket_name": bucket,
                "file_name": file.filename,
                "media_type": media_type,
            }).execute()
        else:
            supabase.table("crop_scans").insert({
                "user_id": user_id,
                "farm_id": farm_id,
                "image_url": url,
                "bucket_name": bucket,
                "file_name": file.filename,
                "scan_type": scan_type,
            }).execute()

        return {
            "message": "File uploaded",
            "url": url,
            "bucket": bucket,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))