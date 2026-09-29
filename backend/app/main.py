from fastapi import FastAPI
from app.services import router as api_router

app = FastAPI(title="Sistem Perpustakaan")

# Health check endpoint untuk automated test
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Router utama aplikasi
app.include_router(api_router)