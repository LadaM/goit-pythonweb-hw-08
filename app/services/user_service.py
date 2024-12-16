"""
User Service.

This module contains the `UserService` class, which provides functionality for user management.
"""
import os
import shutil
from datetime import timedelta

from fastapi import BackgroundTasks, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.config import Config
from app.repository.database import get_db
from app.repository.models import User
from app.utils.jwt import create_access_token, create_email_verification_token
from app.utils.mail import send_verification_email

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class UserService:
    """
    A service class for managing users.

    Attributes:
        db (Session): Database session for queries.
    """
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_user_by_email(self, email: str) -> User | None:
        """Fetch a user by their email."""
        return self.db.query(User).filter(User.email == email).first()

    def create_user(self, email: str, password: str) -> User:
        """Create a new user with a hashed password."""
        hashed_password = pwd_context.hash(password)
        user = User(email=email, hashed_password=hashed_password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    async def create_user_with_verification(self, email: str, password: str, background_tasks: BackgroundTasks) -> User:
        """Create a new user and send a verification email."""
        user = self.create_user(email, password)

        verification_token = create_email_verification_token(user.email)
        self.add_verification_token(user, verification_token)
        await send_verification_email(user.email, verification_token, background_tasks)
        return user

    def add_verification_token(self, user: User, token: str) -> None:
        """Assign a verification token to the user and commit to the database."""
        user.verification_token = token
        self.db.commit()

    async def resend_verification_email(self, user: User, background_tasks: BackgroundTasks) -> None:
        """Send a verification email to the user."""
        verification_token = create_email_verification_token(user.email)
        self.add_verification_token(user, verification_token)
        await send_verification_email(user.email, verification_token, background_tasks)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify if a plaintext password matches a hashed password."""
        return pwd_context.verify(plain_password, hashed_password)

    def generate_access_token(self, email: str) -> str:
        """Generate a JWT access token for the user."""
        return create_access_token(
            data={"sub": email},
            expires_delta=timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES),
        )

    def verify_user_email(self, user):
        """Mark the user's email as verified."""
        user.is_verified = True
        user.verification_token = None
        self.db.commit()

    def update_avatar(self, user: User, avatar_file, avatar_filename: str) -> User:
        if avatar_file.content_type not in ["image/jpeg", "image/png"]:
            raise ValueError("Invalid file type. Only JPEG and PNG allowed.")

        avatar_path = f"avatars/{user.id}_{avatar_filename}"
        os.makedirs("avatars", exist_ok=True)

        with open(avatar_path, "wb") as buffer:
            shutil.copyfileobj(avatar_file.file, buffer)

        user.avatar = avatar_path
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user