import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
from services.qdrant_service import insert_disease_data, create_collection

create_collection()

with open("rag/data/chilli_diseases.json") as f:
    data = json.load(f)

insert_disease_data(data)

print("✅ Data inserted successfully!")