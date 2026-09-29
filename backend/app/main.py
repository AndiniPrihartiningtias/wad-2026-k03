from fastapi import FastAPI
from app.services import router as api_router

app = FastAPI(title="Sistem Perpustakaan")

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(api_router)