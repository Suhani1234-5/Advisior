from fastapi import FastAPI
from routes import health, upload, history,users
from services.qdrant_service import create_collection
from routes.qdrant_routes import router as qdrant_router
from routes.pdf_routes import router as pdf_router
from routes.ai_routes import router as ai_router

from dotenv import load_dotenv
load_dotenv()  # ✅ MUST be first, before any other imports


app = FastAPI(title="Agri AI Platform")
create_collection()
app.include_router(health.router)
app.include_router(upload.router)
app.include_router(history.router)
app.include_router(users.router)
#app.include_router(qdrant_router)
app.include_router(pdf_router)
app.include_router(ai_router, prefix="/ai")


@app.get("/")
def home():
    return {"message": "Agri AI Platform Backend Running"}

@app.get("/debug")
def debug():
    from services.qdrant_service import client, COLLECTION_NAME
    return client.count(collection_name=COLLECTION_NAME)

