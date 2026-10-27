from fastapi import Depends, FastAPI                                  
from fastapi.middleware.cors import CORSMiddleware
from app.services import router as api_router
from . import models
from .auth import router as auth_router, get_current_user, require_role   
from .database import engine

app = FastAPI(title="Sistem Perpustakaan")

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
app.include_router(auth_router)


@app.get("/me")
def read_me(user: models.User = Depends(get_current_user)):
    return {"id": user.id, "username": user.username, "role": user.role}


@app.get("/admin/ping")
def admin_ping(user: models.User = Depends(require_role("admin"))):
    return {"message": f"Halo admin {user.username}"}