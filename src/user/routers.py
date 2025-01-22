from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.db.session import DbSession
from src.user.schemas import UserCreate, UserResponse
from src.user.services import UserService

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register_user(
    user: UserCreate,
    db: DbSession,
    user_service: Annotated[UserService, Depends(UserService)],
):
    existing_user = await user_service.get_user_by_username(db, user.nm_user)
    if existing_user:
        raise HTTPException(status_code=400, detail="nm_user already taken")
    return await user_service.create_user(db, user)
