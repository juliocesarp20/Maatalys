from fastapi import APIRouter, HTTPException, Depends
from src.user.schemas import UserCreate, UserResponse
from src.user.services import UserService
from src.db.session import DbSession

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register_user(
    user: UserCreate,
    db: DbSession,
    user_service: UserService = Depends()
):
    existing_user = await user_service.get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    return await user_service.create_user(db, user)