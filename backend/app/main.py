from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services import router as api_router
from . import models
from .database import engine

# Inisialisasi aplikasi FastAPI
app = FastAPI(title="Sistem Perpustakaan")

# CORS Middleware agar frontend bisa mengakses backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Otomatis membuat tabel database SQLite saat server dijalankan
models.Base.metadata.create_all(bind=engine)

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(api_router)
