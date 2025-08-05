import json
import os
from difflib import get_close_matches

# Locate your products.json file
DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/products.json")

# Load product list
def load_products():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# Fuzzy search using product name
def fuzzy_search(query: str):
    products = load_products()
    names = [p["name"] for p in products]
    matches = get_close_matches(query, names, n=10, cutoff=0.3)
    return [p for p in products if p["name"] in matches]
