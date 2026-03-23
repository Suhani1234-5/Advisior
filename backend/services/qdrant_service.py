from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.models import PointStruct
from services.embedding_service import get_embedding
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client.models import Filter, FieldCondition, MatchValue

from openai import OpenAI
import os  # ✅ ADD THIS

# Connect to Qdrant (Docker running locally)
client = QdrantClient(url="http://localhost:6333")

COLLECTION_NAME = "agri_knowledge"

def create_collection():
    collections = client.get_collections().collections
    exists = any(col.name == COLLECTION_NAME for col in collections)
    if not exists:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )

def insert_disease_data(data):
    points = []

    for i, item in enumerate(data):
        # Build embedding text (IMPORTANT)
        text = f"""
        Crop: {item['crop']}
        Disease: {item['disease']}
        Symptoms: {', '.join(item['symptoms'])}
        Description: {item['symptom_text']}
        Keywords: {', '.join(item['search_keywords'])}
        """

        vector = get_embedding(text)

        payload = {
            "crop": item["crop"],
            "disease": item["disease"],
            "pathogen": item["pathogen"],
            "affected_part": item["affected_part"],
            "severity_hint": item["severity_hint"],
            "confusion_with": item["confusion_with"]
        }

        points.append(
            PointStruct(
                id=i,
                vector=vector,
                payload=payload
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

def search_data(query: str):
    query_vector = get_embedding(query)
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=3
    )
    return [point.payload for point in results.points]

from qdrant_client.models import Filter, FieldCondition, MatchValue

def search_diseases(query: str):
    query_vector = get_embedding(query)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=3,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="crop",
                    match=MatchValue(value="chilli")
                )
            ]
        )
    )

    return [point.payload for point in results.points]
# Initialize embedding client - lazy init to avoid crash on missing key
def get_embedding_client():
    api_key = os.getenv("GROK_API_KEY") or os.getenv("XAI_API_KEY")
    if not api_key:
        raise ValueError("GROK_API_KEY or XAI_API_KEY environment variable not set")
    return OpenAI(
        api_key=api_key,
        base_url="https://api.x.ai/v1"  # Grok's API endpoint
    )

# ✅ REMOVED duplicate PointStruct import that was here

def insert_data_from_text(text: str):
    embedding_client = get_embedding_client()  # ✅ get client here, not at module level
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_text(text)

    points = []
    for i, chunk in enumerate(chunks):
        emb = embedding_client.embeddings.create(
            model="text-embedding-3-large",
            input=chunk
        ).data[0].embedding
        points.append(PointStruct(id=i, vector=emb, payload={"text": chunk}))

    client.upsert(collection_name=COLLECTION_NAME, points=points)
