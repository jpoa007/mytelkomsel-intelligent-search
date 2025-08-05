from fastapi import APIRouter
from rapidfuzz import process
import json
import os

router = APIRouter()

# ✅ Load product data
current_dir = os.path.dirname(__file__)
product_path = os.path.join(current_dir, "../data/products.json")

with open(product_path, "r", encoding="utf-8") as f:
    products = json.load(f)


@router.get("/fuzzy")
def fuzzy_search(q: str):
    query = q.lower()

    # ✅ Combine searchable text (name + description)
    searchable_map = {
        f"{p['name'].lower()} {p['description'].lower()}": p for p in products
    }

    # ✅ Perform fuzzy matching
    matches = process.extract(
        query,
        searchable_map.keys(),
        limit=10,  # check top 10 matches
        score_cutoff=40,  # more tolerant for typos
    )

    # ✅ Extract matched product objects
    results = [searchable_map[match[0]] for match in matches]

    return {"query": q, "results": results}
