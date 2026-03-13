from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.deps import get_current_active_admin
from app.db import get_db
from app.models import User
from app.schemas import Token, UserCreate, UserRead
from app.services import auth_service


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> Token:
    user = auth_service.authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    return auth_service.create_user_tokens(user)


@router.post("/register", response_model=UserRead)
def register(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_admin),
) -> UserRead:
    existing = auth_service.get_user_by_email(db, email=user_in.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = auth_service.create_user(db, user_in=user_in)
    return user

