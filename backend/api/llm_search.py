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


def generate_polite_refusal(query: str) -> str:
    """Generate polite refusal in the same language as the query"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a Telkomsel product search assistant. When you cannot find relevant products for a user's query, politely decline and suggest they search for specific Telkomsel products like data packages, phone plans, etc. Respond in the same language as the user's query.",
                },
                {
                    "role": "user",
                    "content": f"User searched for: '{query}' - No relevant products found. Please politely decline and suggest searching for Telkomsel products.",
                },
            ],
            max_tokens=100,
            temperature=0.3,
        )

        return response.choices[0].message.content.strip()
    except:
        return "Sorry, I can only help you find Telkomsel products. Please search for data packages, phone plans, or other Telkomsel services."


@router.get("/llm-search")
def llm_search(
    query: str = Query(..., min_length=1),
    top_n: int = Query(10, ge=1, le=50),
    threshold: float = Query(0.15, ge=0.0, le=1.0),
    sort_by: str = Query("similarity"),
    order: str = Query("desc"),
):
    # ✅ Debug: Print collection info
    print(f"🔍 Query: '{query}', Threshold: {threshold}")
    print(f"📊 Collection count: {collection.count()}")

    try:
        response = client.embeddings.create(
            model="text-embedding-3-small", input=[query]
        )
        query_embedding = response.data[0].embedding
        print(f"✅ Embedding created successfully")
    except Exception as e:
        print(f"❌ Embedding failed: {str(e)}")
        return {"error": f"Embedding failed: {str(e)}"}

    try:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_n,
            include=["metadatas", "distances"],
        )
        print(f"✅ ChromaDB query successful")
    except Exception as e:
        print(f"❌ ChromaDB query failed: {str(e)}")
        return {"error": f"ChromaDB query failed: {str(e)}"}

    distances = results.get("distances", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    similarities = [1 - d for d in distances]

    # ✅ Debug: Print similarity scores
    print(f"📈 Top 3 similarities: {similarities[:3]}")
    print(f"📈 Top 3 distances: {distances[:3]}")

    enriched = []
    for metadata, sim in zip(metadatas, similarities):
        if sim >= threshold:
            enriched.append({**metadata, "similarity": round(sim, 4)})

    # ✅ Debug: Print results
    print(f"🎯 Items above threshold ({threshold}): {len(enriched)}")

    # ✅ If no products found, politely refuse
    if not enriched:
        print(f"❌ No results found for query: '{query}'")
        return {
            "query": query,
            "response": generate_polite_refusal(query),
            "results": [],
        }

    sorted_filtered = apply_filter(enriched, sort_by=sort_by, order=order)
    print(f"✅ Returning {len(sorted_filtered)} results")
    return {"query": query, "results": sorted_filtered, "threshold": threshold}
