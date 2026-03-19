from fastapi import FastAPI
from routes import health, upload, history,users

app = FastAPI(title="Agri AI Platform")

app.include_router(health.router)
app.include_router(upload.router)
app.include_router(history.router)
app.include_router(users.router)

@app.get("/")
def home():
    return {"message": "Agri AI Platform Backend Running"}