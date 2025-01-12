from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.auth.schemas import Token
from src.auth.services import AuthService, CurrentUser
from src.db.session import DbSession
from src.user.schemas import UserResponse

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/login", response_model=Token)
async def login_for_access_token(
    db: DbSession,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[AuthService, Depends(AuthService)],
):
    user = await auth_service.authenticate_user(
        db, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = auth_service.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def get_user_info(current_user: CurrentUser):
    return current_user
