from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv
from qdrant_client.models import Distance, VectorParams
from qdrant_client.models import PointStruct
import json

load_dotenv()

# Initialize the client
qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"), 
    api_key=os.getenv("QDRANT_API_KEY"),
)

collection_name = "test_collection886"

# Create the collection
try:
    qdrant_client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=4, distance=Distance.DOT),
    )
except Exception as e:
    print(e)



# Upsert to the collection
operation_info = qdrant_client.upsert(
    collection_name=collection_name,
    wait=True,
    points=[
        PointStruct(id=1, vector=[0.05, 0.61, 0.76, 0.74], payload={"city": "Berlin"}),
        PointStruct(id=2, vector=[0.19, 0.81, 0.75, 0.11], payload={"city": "London"}),
        PointStruct(id=3, vector=[0.36, 0.55, 0.47, 0.94], payload={"city": "Moscow"}),
        PointStruct(id=4, vector=[0.18, 0.01, 0.85, 0.80], payload={"city": "New York"}),
        PointStruct(id=5, vector=[0.24, 0.18, 0.22, 0.44], payload={"city": "Beijing"}),
        PointStruct(id=6, vector=[0.35, 0.08, 0.11, 0.44], payload={"city": "Mumbai"}),
    ],
)

# Query the collection
search_result = qdrant_client.query_points(
    collection_name=collection_name,
    query=[0.18, 0.01, 0.85, 0.80], # New York
    with_payload=True,
    limit=3
).points

print(f"\n\nSearch result: {json.dumps([point.model_dump() for point in search_result], indent=4)}")

print(f"\n\nCurrent collections: {qdrant_client.get_collections()}")
