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


# ✅ Register routers
app.include_router(fuzzy_search.router, prefix="/api")
app.include_router(llm_search.router, prefix="/api")
