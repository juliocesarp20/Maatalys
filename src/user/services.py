from sqlalchemy.future import select
from src.user.models import User
from src.user.schemas import UserCreate
from src.utils.password_manager import PasswordManager
from src.db.session import DbSession
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class UserService:
    async def create_user(self, db: DbSession, user_data: UserCreate) -> User:
        """
        Create a new user and persist it to the database.
        """
        logger.info(f"Creating new user with username: {user_data.username}")
        hashed_password = PasswordManager.hash_password(user_data.password)  # Static method
        new_user = User(
            username=user_data.username,
            hashed_password=hashed_password,
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        logger.info(f"User {user_data.username} created successfully.")
        return new_user

    async def get_user_by_username(self, db: DbSession, username: str) -> Optional[User]:
        """
        Fetch a user by their username.
        """
        logger.debug(f"Fetching user by username: {username}")
        result = await db.execute(
            select(User).filter(User.username == username)
        )
        return result.scalar_one_or_none()
