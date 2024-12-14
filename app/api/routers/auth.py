from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.schemas import UserCreate, UserResponse, Token
from app.config import Config
from app.repository import users
from app.repository.database import get_db
from app.repository.models import User
from app.services.user_service import get_current_user
from app.utils.jwt import create_access_token, create_email_verification_token, verify_email_verification_token
from app.utils.mail import send_verification_email

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=201)
async def register_user(
    user_data: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    existing_user = users.get_user_by_email(db, email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    new_user = users.create_user(db, user_data.email, user_data.password)

    token = create_email_verification_token(new_user.email)
    new_user.verification_token = token
    db.commit()

    await send_verification_email(new_user.email, token, background_tasks)
    return new_user


@router.post("/login", response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = users.get_user_by_email(db, form_data.username)
    if not user or not users.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/send-verification-email", status_code=200)
async def send_verification(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    token = create_email_verification_token(current_user.email)
    current_user.verification_token = token
    db.commit()
    await send_verification_email(current_user.email, token)
    return {"detail": "Verification email sent"}


@router.get("/verify-email", status_code=200)
def verify_email(token: str, db: Session = Depends(get_db)):
    email = verify_email_verification_token(token)
    user = users.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_verified = True
    user.verification_token = None
    db.commit()
    return {"detail": "Email verified successfully"}
