from fastapi import FastAPI

from app.api.v1 import router as api_v1_router  # это тот самый router из __init__.py

app = FastAPI(title="Wine Scanner API", version="0.1.0")

app.include_router(api_v1_router, prefix="/api/v1")
