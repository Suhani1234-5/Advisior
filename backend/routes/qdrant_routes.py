from fastapi import APIRouter
from services.qdrant_service import insert_disease_data, search_data

router = APIRouter()

@router.post("/add-knowledge")
def add_knowledge():
    data = [
        {"text": "Yellow leaves in wheat indicate nitrogen deficiency"},
        {"text": "High humidity increases pest risk"},
        {"text": "Tomato early blight causes brown spots"}
    ]

    insert_data(data)
    return {"message": "Data inserted"}

@router.get("/search")
def search(query: str):
    results = search_data(query)
    return {"results": results}