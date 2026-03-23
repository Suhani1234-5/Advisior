from fastapi import APIRouter
from services.grok_service import generate_grok_answer
from fastapi import APIRouter
from services.grok_service import generate_disease_advice

router = APIRouter()

@router.get("/ask-ai")
def ask_ai(query: str):
    answer = generate_grok_answer(query)
    return {"answer": answer}


@router.post("/ask-disease")
def ask_disease(query: str):
    response = generate_disease_advice(query)
    return {"answer": response}