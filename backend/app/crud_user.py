from sqlalchemy.orm import Session
from . import models

# Ambil user berdasarkan username (dipakai A1 saat Login)
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

# Ambil user berdasarkan ID
def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# Tambah user baru (Create Account / Register)
def create_user(db: Session, username: str, hashed_password: str, role: str = "user"):
    db_user = models.User(
        username=username, 
        hashed_password=hashed_password, 
        role=role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Update Role user (misal ubah jadi admin)
def update_user_role(db: Session, user_id: int, new_role: str):
    db_user = get_user_by_id(db, user_id)
    if db_user:
        db_user.role = new_role
        db.commit()
        db.refresh(db_user)
    return db_user