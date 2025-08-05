from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# from backend.api import fuzzy_search, llm_search  # ✅ Import both routers
from backend.api import fuzzy_search, llm_search, vector_search
import os

app = FastAPI()

# ✅ CORS middleware to allow frontend access from localhost:5173
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or ["*"] during development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Serve static files (e.g., images)
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/images", StaticFiles(directory=static_dir), name="images")

# ✅ Include fuzzy search and LLM search API routers
# app.include_router(fuzzy_search.router, prefix="/api")
# app.include_router(llm_search.router, prefix="/api")  # 👈 Add this line
# app.include_router(vector_search.router, prefix="/api")
