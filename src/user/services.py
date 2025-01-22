import logging
from typing import Optional

from sqlalchemy.future import select

from src.db.session import DbSession
from src.user.models import User
from src.user.schemas import UserCreate
from src.utils.password_manager import PasswordManager

logger = logging.getLogger(__name__)


class UserService:
    async def create_user(self, db: DbSession, user_data: UserCreate) -> User:
        """
        Create a new user and persist it to the database.
        """
        logger.info(f"Creating new user with nm_user: {user_data.nm_user}")
        hashed_password = PasswordManager.hash_password(user_data.password)
        new_user = User(
            nm_user=user_data.nm_user,
            hashed_password=hashed_password,
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        logger.info(f"User {user_data.nm_user} created successfully.")
        return new_user

    async def get_user_by_username(self, db: DbSession, nm_user: str) -> Optional[User]:
        """
        Fetch a user by their nm_user.
        """
        logger.debug(f"Fetching user by nm_user: {nm_user}")
        result = await db.execute(select(User).filter(User.nm_user == nm_user))
        return result.scalar_one_or_none()
