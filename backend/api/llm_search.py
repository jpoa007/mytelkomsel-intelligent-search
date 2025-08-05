from fastapi import APIRouter, Query
from openai import OpenAI
import chromadb
import os
from backend.utils.filters import apply_filter

router = APIRouter()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

chroma_client = chromadb.PersistentClient(path="backend/vector_store")
collection = chroma_client.get_or_create_collection(
    name="products", metadata={"hnsw:space": "cosine"}
)


@router.get("/llm-search")
def llm_search(
    query: str = Query(..., min_length=1),
    top_n: int = Query(10, ge=1, le=50),
    threshold: float = Query(0.15, ge=0.0, le=1.0),
    sort_by: str = Query("similarity"),  # or "price"
    order: str = Query("desc"),  # or "asc"
):
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small", input=[query]
        )
        query_embedding = response.data[0].embedding
    except Exception as e:
        return {"error": f"Embedding failed: {str(e)}"}

    try:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_n,
            include=["metadatas", "distances"],
        )
    except Exception as e:
        return {"error": f"ChromaDB query failed: {str(e)}"}

    distances = results.get("distances", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    similarities = [1 - d for d in distances]

    enriched = []
    for metadata, sim in zip(metadatas, similarities):
        if sim >= threshold:
            enriched.append({**metadata, "similarity": round(sim, 4)})

    if not enriched:
        return {
            "query": query,
            "response": "Maaf, saya belum bisa menjawab pertanyaan itu dengan informasi produk yang tersedia.",
        }

    # ✅ Apply frontend-friendly sorting
    sorted_filtered = apply_filter(enriched, sort_by=sort_by, order=order)
    return {"query": query, "results": sorted_filtered, "threshold": threshold}
