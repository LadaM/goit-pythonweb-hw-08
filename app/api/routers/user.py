from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.api.schemas import UserResponse
from app.repository.models import User
from app.services.authentication import get_current_user, get_current_admin_user
from app.services.user_service import UserService

router = APIRouter(prefix="/user", tags=["User"])
limiter = Limiter(key_func=get_remote_address)


@router.get(
    "/me", response_model=UserResponse, description="No more than 10 requests per minute"
)
@limiter.limit("10/minute")
async def get_current_user(request: Request, user: User = Depends(get_current_user)):
    return user


@router.put("/avatar", response_model=UserResponse)
def update_avatar(
        avatar: UploadFile = File(...),
        current_user: User = Depends(get_current_admin_user),
        user_service: UserService = Depends()
):
    try:
        updated_user = user_service.update_avatar(current_user, avatar, avatar.filename)
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
