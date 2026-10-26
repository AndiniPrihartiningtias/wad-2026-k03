from fastapi import FastAPI
from . import models
from .database import engine

# Inisialisasi aplikasi FastAPI
app = FastAPI(title="Sistem Perpustakaan")

# Otomatis membuat tabel database SQLite saat server dijalankan
models.Base.metadata.create_all(bind=engine)

@app.get("/health")
def health_check():
    return {"status": "ok"}