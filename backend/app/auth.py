
import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from . import crud_user, models
from .database import get_db
from .schemas import RegisterRequest, UserUpdate, UserOut
from .security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)

router = APIRouter(tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# =========================
# CREATE ACCOUNT / REGISTER
# =========================
@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db),
):
    username = data.username.strip()

    if not username:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Username tidak boleh kosong",
        )

    existing_user = crud_user.get_user_by_username(db, username)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username sudah digunakan",
        )

    try:
        user = crud_user.create_user(
            db=db,
            username=username,
            hashed_password=hash_password(data.password),
            role="user",
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username sudah digunakan",
        )

    return user


# =========================
# LOGIN
# =========================
@router.post("/login")
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = crud_user.get_user_by_username(db, form.username)

    if not user or not verify_password(
        form.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username atau password salah",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(
        subject=str(user.id),
        role=user.role,
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }


# =========================
# MENDAPATKAN USER LOGIN
# =========================
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> models.User:
    cred_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token tidak valid atau kedaluwarsa",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        user_id = int(payload["sub"])
    except (jwt.PyJWTError, KeyError, ValueError, TypeError):
        raise cred_exc

    user = crud_user.get_user_by_id(db, user_id)

    if user is None:
        raise cred_exc

    return user


# =========================
# MELIHAT DATA USER LOGIN
# =========================
@router.get("/me", response_model=UserOut)
def read_me(
    user: models.User = Depends(get_current_user),
):
    return user


# =========================
# UPDATE DATA USER LOGIN
# =========================
@router.patch("/me", response_model=UserOut)
def update_me(
    data: UserUpdate,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    username = data.username.strip()

    if not username:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Username tidak boleh kosong",
        )

    existing_user = crud_user.get_user_by_username(db, username)

    if existing_user and existing_user.id != user.id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username sudah digunakan",
        )

    user.username = username

    # Password diganti hanya jika password baru diisi.
    if data.password:
        user.hashed_password = hash_password(data.password)

    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username sudah digunakan",
        )

    return user


# =========================
# PEMBATASAN AKSES BERDASARKAN ROLE
# =========================
def require_role(*allowed_roles: str):
    """Memastikan user memiliki salah satu role yang diizinkan."""

    def checker(
        user: models.User = Depends(get_current_user),
    ) -> models.User:
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Anda tidak punya akses ke resource ini",
            )

        return user

    return checker
