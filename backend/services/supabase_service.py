import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")  # service key for backend operations
)

def get_user_from_token(token: str) -> dict:
    """Verify JWT and return user. Raises if invalid."""
    response = supabase.auth.get_user(token)
    if not response.user:
        raise ValueError("Invalid token")
    return response.user