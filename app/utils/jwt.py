"""
JWT Utilities.
"""
from datetime import datetime, timedelta
from typing import Union

from fastapi import HTTPException
from jose import JWTError, jwt

from app.config import Config


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        return email
    except JWTError:
        return None


def create_email_verification_token(email: str):
    data = {"sub": email}
    return create_access_token(data, expires_delta=timedelta(hours=24))


def verify_email_verification_token(token: str):
    """
    Decode and verify an email verification token.
    Raise an exception if the token is invalid.
    """
    email = verify_access_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    return email
