#this will handle Qdrant
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from qdrant_client.models import PointStruct
from qdrant_client.models import Filter, FieldCondition, MatchValue

client = QdrantClient(":memory:")  # later we’ll switch to real DB

COLLECTION_NAME = "crop_diseases"

def setup_collection():
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )

def insert_points(points):
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

def search(query_vector):
    return client.query_points(
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
    ).points   #this prevents model from mixing results about chilli and other crops, tomato, for example