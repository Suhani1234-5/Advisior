#this will run everything
import json
from embed import build_embedding_text, get_embedding
from db import setup_collection, insert_points, search
from qdrant_client.models import PointStruct

# 1. Load data
with open("../data/chilli_diseases.json", "r") as f:
    data = json.load(f)

# 2. Setup DB
setup_collection()

# 3. Insert data
points = []

for i, item in enumerate(data):
    text = build_embedding_text(item)
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
    )  #Qdrant Python client expects structured objects. Not raw dictionaries 

insert_points(points)

# 4. Test query
query = "chilli plant wilting and dying"
query_vector = get_embedding(query)

results = search(query_vector)

top = results[0].payload
alternatives = [r.payload["disease"] for r in results[1:]]

print("\n--- AI Advisor Response ---\n")

print(f"Based on the symptoms, your chilli crop is likely affected by {top['disease']}.")

print(f"\nCause: {top['pathogen']}")
print(f"Affected parts: {', '.join(top['affected_part'])}")
print(f"Severity: {top['severity_hint']}")

print(f"\nIt can sometimes be confused with: {', '.join(top['confusion_with'])}")

print(f"\nOther possible diseases: {', '.join(alternatives)}")