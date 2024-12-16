"""
Authentication Utilities.

This module provides authentication functionality, including user authentication and role validation.
"""
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.repository.models import UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
import logging
from app.main import redis_client
from app.services.user_service import UserService
from app.utils.jwt import verify_access_token
from app.repository.models import User
import json

# Configure logging
logger = logging.getLogger(__name__)

def get_current_user(token: str = Depends(oauth2_scheme), user_service: UserService = Depends()):
    """
    Get the current user from the token.

    Args:
        token (str, optional): The authentication token. Defaults to Depends(oauth2_scheme).
        user_service (UserService, optional): The user service. Defaults to Depends().

    Raises:
        HTTPException: If the token is invalid or expired.

    Returns:
        User: The current user.
    """
    email = verify_access_token(token)
    if not email:
        logger.error("Invalid or expired token")
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    cache_key = f"user:{email}"

    # Check Redis cache
    user_data = None
    try:
        cached_user = redis_client.get(cache_key)
        if cached_user:
            logger.info(f"Cache hit for user: {email}")
            user_data = json.loads(cached_user)
        else:
            logger.info(f"Cache miss for user: {email}")
    except Exception as e:
        logger.error(f"Redis connection error: {str(e)}")

    # Fetch user from database if not in cache
    if not user_data:
        user = user_service.get_user_by_email(email=email)
        if not user or not user.is_verified:
            logger.warning(f"User not verified or does not exist: {email}")
            raise HTTPException(status_code=403, detail="User is not verified")

        # Cache user data in Redis
        user_data = {
            "id": user.id,
            "email": user.email,
            "is_verified": user.is_verified,
            "is_active": user.is_active,
            "avatar": user.avatar,
            "role": user.role
        }
        try:
            redis_client.set(cache_key, json.dumps(user_data), ex=3600)  # Cache for 1 hour
            logger.info(f"User data cached for {email}")
        except Exception as e:
            logger.error(f"Failed to cache user data for {email}: {str(e)}")

    return user_data

def get_current_admin_user(current_user: User = Depends(get_current_user)):
    """
    Get the current admin user.

    Args:
        current_user (User, optional): The current user. Defaults to Depends(get_current_user).

    Raises:
        HTTPException: If the current user is not an admin.

    Returns:
        User: The current admin user.
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Access denied: Admins only")
    return current_user
