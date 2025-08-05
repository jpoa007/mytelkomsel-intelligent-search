import os
import json
from openai import OpenAI
import chromadb

# ✅ Persistent ChromaDB client
chroma_client = chromadb.PersistentClient(path="backend/vector_store")

# ✅ Force cosine similarity
collection = chroma_client.get_or_create_collection(
    name="products", metadata={"hnsw:space": "cosine"}
)

# ✅ Load product data
with open("backend/data/products.json", encoding="utf-8") as f:
    products = json.load(f)

# ✅ Skip if already added
if collection.count() == 0:
    print("⏳ Creating embeddings and storing in ChromaDB...")

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

    print("✅ Embeddings stored in: backend/vector_store")
else:
    print("✅ Embeddings already exist.")
