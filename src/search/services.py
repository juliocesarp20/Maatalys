import logging
import uuid
from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select

from src.db.session import DbSession
from src.search.models import Search
from src.search.schemas import SearchCreate

logger = logging.getLogger(__name__)


class SearchService:
    async def create_search(
        self, db: DbSession, search_data: SearchCreate
    ) -> Optional[Search]:
        """
        Create a new search and persist it to the database.
        """
        logger.info(f"Creating search with source: {search_data.source}")
        new_search = Search(
            investigation_id=search_data.investigation_id,
            source=search_data.source,
            parameters=search_data.parameters,
        )
        try:
            db.add(new_search)
            await db.commit()
            await db.refresh(new_search)
            logger.info(f"Search for source {search_data.source} created successfully.")
            return new_search
        except SQLAlchemyError as e:
            logger.error(f"Database error occurred while creating search: {e}")
            await db.rollback()
            raise RuntimeError("Database error: Unable to create search.")

    async def get_search_by_id(
        self, db: DbSession, search_id: uuid.UUID
    ) -> Optional[Search]:
        """
        Fetch a search by its ID.
        """
        logger.debug(f"Fetching search by ID: {search_id}")
        try:
            result = await db.execute(select(Search).filter(Search.id == search_id))
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"Database error occurred while fetching search: {e}")
            raise RuntimeError("Database error: Unable to fetch search.")

    async def list_searches_by_investigation(
        self, db: DbSession, investigation_id: uuid.UUID
    ) -> List[Search]:
        """
        List all searches for a specific investigation.
        """
        logger.debug(f"Listing searches for investigation ID: {investigation_id}")
        try:
            result = await db.execute(
                select(Search).filter(Search.investigation_id == investigation_id)
            )
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Database error occurred while listing searches: {e}")
            raise RuntimeError("Database error: Unable to list searches.")

    async def delete_search(self, db: DbSession, search_id: uuid.UUID) -> bool:
        """
        Delete a search by its ID.
        """
        logger.info(f"Deleting search ID: {search_id}")
        try:
            result = await db.execute(select(Search).filter(Search.id == search_id))
            search = result.scalar_one_or_none()
            if search:
                await db.delete(search)
                await db.commit()
                logger.info(f"Search ID {search_id} deleted successfully.")
                return True
            else:
                logger.warning(f"Search ID {search_id} not found.")
                return False
        except SQLAlchemyError as e:
            logger.error(f"Database error occurred while deleting search: {e}")
            await db.rollback()
            raise RuntimeError("Database error: Unable to delete search.")
