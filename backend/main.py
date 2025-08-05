from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from backend.api import fuzzy_search, llm_search

app = FastAPI()

# ✅ Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Local development
        "https://mytelkomsel-frontend-production.up.railway.app",  # Your frontend
        "https://mytelkomsel-backend-production.up.railway.app",  # Your backend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Mount static image files
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/images", StaticFiles(directory=static_dir), name="images")


@app.get("/")
def health_check():
    return {"status": "OK"}


@app.post("/admin/create-embeddings")
def create_embeddings():
    """Manual endpoint to populate ChromaDB - call only when needed"""
    import json
    from openai import OpenAI
    import chromadb

    try:
        chroma_client = chromadb.PersistentClient(path="backend/vector_store")
        collection = chroma_client.get_or_create_collection(
            name="products", metadata={"hnsw:space": "cosine"}
        )

        current_count = collection.count()

        # Load product data
        with open("backend/data/products.json", encoding="utf-8") as f:
            products = json.load(f)

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Clear existing and add new
        if current_count > 0:
            collection.delete(ids=[str(p["id"]) for p in products])

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

        return {
            "message": "✅ Embeddings created successfully!",
            "previous_count": current_count,
            "new_count": len(products),
        }

    except Exception as e:
        return {"error": str(e)}


@app.get("/admin/embedding-status")
def embedding_status():
    """Check if embeddings exist"""
    try:
        chroma_client = chromadb.PersistentClient(path="backend/vector_store")
        collection = chroma_client.get_or_create_collection(name="products")
        return {
            "count": collection.count(),
            "status": "ready" if collection.count() > 0 else "empty",
        }
    except Exception as e:
        return {"error": str(e)}


# ✅ Register routers
app.include_router(fuzzy_search.router, prefix="/api")
app.include_router(llm_search.router, prefix="/api")
