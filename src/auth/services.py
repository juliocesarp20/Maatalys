import logging
from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

import jwt
from fastapi import Depends, HTTPException

from src.auth.auth import auth_settings, oauth2_scheme
from src.db.session import DbSession
from src.user.models import User
from src.user.schemas import UserResponse
from src.user.services import UserService
from src.utils.password_manager import PasswordManager

logger = logging.getLogger(__name__)

user_service = UserService()


class AuthService:
    async def authenticate_user(
        self,
        db: DbSession,
        username: str,
        password: str,
    ) -> Optional[User]:
        """
        Authenticate the user by validating the username and password.
        """
        logger.debug(f"Authenticating user: {username}")
        user = await user_service.get_user_by_username(db, username)
        if not user:
            logger.warning(f"Authentication failed: User {username} not found.")
            return None
        if not PasswordManager.verify_password(password, user.hashed_password):
            logger.warning(
                f"Authentication failed: Invalid password for user {username}."
            )
            return None
        logger.info(f"User {username} authenticated successfully.")
        return user

    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create a new JWT token with the specified expiration delta.
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (
            expires_delta
            or timedelta(minutes=auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode, auth_settings.SECRET_KEY, algorithm=auth_settings.ALGORITHM
        )

    @staticmethod
    async def get_current_user(
        db: DbSession,
        token: str = Depends(oauth2_scheme),
        user_service: UserService = Depends(UserService),
    ) -> UserResponse:
        """
        Retrieve the current user based on the JWT token.
        """
        credentials_exception = HTTPException(
            status_code=401, detail="Invalid credentials"
        )
        try:
            payload = jwt.decode(
                token, auth_settings.SECRET_KEY, algorithms=[auth_settings.ALGORITHM]
            )
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise credentials_exception

        user = await user_service.get_user_by_username(db, username)
        if user is None:
            raise credentials_exception

        return user


CurrentUser = Annotated[UserResponse, Depends(AuthService.get_current_user)]
