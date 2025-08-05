from fastapi import APIRouter
from openai import OpenAI
import chromadb
import os
import json

router = APIRouter()

# Load products
with open(
    os.path.join(os.path.dirname(__file__), "../data/products.json"), encoding="utf-8"
) as f:
    products = json.load(f)

# Initialize OpenAI and Chroma
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="products")

# Step 1: Add product embeddings to ChromaDB (only if not already present)
if not collection.count():
    for product in products:
        text = f"{product['name']} - {product['description']}"
        response = client.embeddings.create(
            model="text-embedding-3-small", input=[text]
        )
        embedding = response.data[0].embedding
        collection.add(
            documents=[text],
            metadatas=[product],
            ids=[str(product["id"])],
            embeddings=[embedding],
        )


# Step 2: Search endpoint
@router.get("/vector-search")
def vector_search(q: str):
    response = client.embeddings.create(model="text-embedding-3-small", input=[q])
    query_embedding = response.data[0].embedding

    results = collection.query(query_embeddings=[query_embedding], n_results=10)

    return {
        "query": q,
        "results": results["metadatas"][0],  # returns list of top matching products
    }
