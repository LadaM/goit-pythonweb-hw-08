from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.repository import users
from app.repository.database import get_db
from app.utils.jwt import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    email = verify_access_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = users.get_user_by_email(db, email=email)
    if not user or not user.is_verified:
        raise HTTPException(status_code=403, detail="User is not verified")
    return user
