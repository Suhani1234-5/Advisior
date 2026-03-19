# routes/users.py
from fastapi import APIRouter, Depends
from services.auth_middleware import get_current_user
from services.supabase_service import supabase

router = APIRouter()

@router.get("/me")
def get_profile(current_user=Depends(get_current_user)):
    result = supabase.table("profiles") \
        .select("*") \
        .eq("id", current_user.id) \
        .single() \
        .execute()
    return {
        "user_id": current_user.id,
        "email": current_user.email,
        "profile": result.data
    }