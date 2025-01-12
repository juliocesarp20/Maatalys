from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from src.parameter_search.models import ParameterSearch
from src.search.models import Search
from src.parameter.models import Parameter
from src.investigation.models import Investigation
from src.investigation.schemas import InvestigationCreate
from src.db.session import DbSession
from uuid import UUID
from typing import Optional, List
import logging
from fastapi import Depends
logger = logging.getLogger(__name__)

import logging

logger = logging.getLogger(__name__)

from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from src.parameter.services import ParameterService

class InvestigationService:
    async def create_investigation(
        self,
        db: DbSession,
        investigation_data: InvestigationCreate,
        user_id: UUID,
        parameter_service: ParameterService = Depends(),
    ) -> Investigation:
        logger.info(f"Creating investigation: {investigation_data.name}")

        pass

    async def get_investigation_by_id(
        self, db: DbSession, investigation_id: UUID
    ) -> Optional[Investigation]:
        """
        Fetch an investigation by its ID.
        """
        logger.debug(f"Fetching investigation by ID: {investigation_id}")
        try:
            result = await db.execute(
                select(Investigation).filter(Investigation.id == investigation_id)
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"Database error occurred while fetching investigation: {e}")
            raise RuntimeError("Database error: Unable to fetch investigation.")

    async def list_investigations(
        self, db: DbSession, user_id: UUID
    ) -> List[Investigation]:
        """
        List all investigations for a specific user.
        """
        logger.debug(f"Listing investigations for user ID: {user_id}")
        try:
            result = await db.execute(
                select(Investigation).filter(Investigation.user_id == user_id)
            )
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Database error occurred while listing investigations: {e}")
            raise RuntimeError("Database error: Unable to list investigations.")

    async def delete_investigation(self, db: DbSession, investigation_id: UUID) -> bool:
        """
        Delete an investigation by its ID.
        """
        logger.info(f"Deleting investigation ID: {investigation_id}")
        try:
            result = await db.execute(
                select(Investigation).filter(Investigation.id == investigation_id)
            )
            investigation = result.scalar_one_or_none()
            if investigation:
                await db.delete(investigation)
                await db.commit()
                logger.info(f"Investigation ID {investigation_id} deleted successfully.")
                return True
            else:
                logger.warning(f"Investigation ID {investigation_id} not found.")
                return False
        except SQLAlchemyError as e:
            logger.error(f"Database error occurred while deleting investigation: {e}")
            await db.rollback()
            raise RuntimeError("Database error: Unable to delete investigation.")
