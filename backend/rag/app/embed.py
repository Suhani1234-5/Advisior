#this will build embeddings for the documents and store them in a vector database
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def build_embedding_text(item):
    return f"""
    Crop: {item['crop']}
    Disease: {item['disease']}
    Symptoms: {', '.join(item['symptoms'])}
    Description: {item['symptom_text']}
    Keywords: {', '.join(item['search_keywords'])}
    """

def get_embedding(text):
    return model.encode(text).tolist()