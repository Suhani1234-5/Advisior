from fastapi import APIRouter, UploadFile, File
from services.qdrant_service import insert_data_from_text

router = APIRouter()

@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    from PyPDF2 import PdfReader
    reader = PdfReader(file.file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    # Send to Qdrant
    insert_data_from_text(text)

    return {"message": "PDF ingested into Qdrant successfully"}