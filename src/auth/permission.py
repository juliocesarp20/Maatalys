from abc import ABC, abstractmethod
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.db.session import DbSession
from src.auth.services import CurrentUser

class BasePermission(ABC):
    @abstractmethod
    async def has_permission(
        self, db: Session, current_user: CurrentUser, **kwargs
    ) -> bool:
        """
        Abstract method to check if a user has permission.
        """
        pass

    async def __call__(
        self, db: DbSession, current_user: CurrentUser, **kwargs
    ):
        if not await self.has_permission(db, current_user, **kwargs):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied."
            )
