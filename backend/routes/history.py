from fastapi import APIRouter, Query, Depends
from services.supabase_service import supabase
from services.auth_middleware import get_current_user
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/history/scans")
def get_scan_history(
    days: int = Query(default=30),
    current_user=Depends(get_current_user)
):
    """Returns this user's crop scans. RLS in Supabase also enforces this."""
    since = (datetime.utcnow() - timedelta(days=days)).isoformat()
    result = supabase.table("crop_scans") \
        .select("*") \
        .eq("user_id", current_user.id) \
        .gte("captured_at", since) \
        .order("captured_at", desc=True) \
        .execute()
    return result.data

@router.get("/history/media")
def get_media_history(
    days: int = Query(default=30),
    current_user=Depends(get_current_user)
):
    """Returns this user's 360 images and videos."""
    since = (datetime.utcnow() - timedelta(days=days)).isoformat()
    result = supabase.table("farm_media") \
        .select("*") \
        .eq("user_id", current_user.id) \
        .gte("captured_at", since) \
        .order("captured_at", desc=True) \
        .execute()
    return result.data