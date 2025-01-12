from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from src.parameter_search.models import ParameterSearch
from src.parameter_search.schemas import ParameterSearchCreate
from src.db.session import DbSession
from typing import List, Optional
import logging
import uuid

logger = logging.getLogger(__name__)

async def create_parameter_search(db: DbSession, parameter_search_data: ParameterSearchCreate) -> Optional[ParameterSearch]:
    logger.info(f"Creating parameter_search with search_id: {parameter_search_data.search_id} and value: {parameter_search_data.value}")
    new_parameter_search = ParameterSearch(
        search_id=parameter_search_data.search_id,
        parameter_id=parameter_search_data.parameter_id,
        value=parameter_search_data.value,
    )
    try:
        db.add(new_parameter_search)
        await db.commit()
        await db.refresh(new_parameter_search)
        logger.info("ParameterSearch created successfully.")
        return new_parameter_search
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred while creating ParameterSearch: {e}")
        await db.rollback()
        raise RuntimeError("Database error: Unable to create ParameterSearch.")

async def get_parameter_search_by_id(db: DbSession, parameter_search_id: uuid.UUID) -> Optional[ParameterSearch]:
    logger.debug(f"Fetching parameter_search by ID: {parameter_search_id}")
    try:
        result = await db.execute(
            select(ParameterSearch).filter(ParameterSearch.id == parameter_search_id)
        )
        return result.scalar_one_or_none()
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred while fetching ParameterSearch: {e}")
        raise RuntimeError("Database error: Unable to fetch ParameterSearch.")

async def list_parameter_searches_for_search(db: DbSession, search_id: uuid.UUID) -> List[ParameterSearch]:
    logger.debug(f"Listing parameter_searches for search_id: {search_id}")
    try:
        result = await db.execute(
            select(ParameterSearch).filter(ParameterSearch.search_id == search_id)
        )
        return result.scalars().all()
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred while listing ParameterSearches: {e}")
        raise RuntimeError("Database error: Unable to list ParameterSearches.")

async def delete_parameter_search(db: DbSession, parameter_search_id: uuid.UUID) -> bool:
    logger.info(f"Deleting parameter_search ID: {parameter_search_id}")
    try:
        result = await db.execute(
            select(ParameterSearch).filter(ParameterSearch.id == parameter_search_id)
        )
        parameter_search = result.scalar_one_or_none()
        if parameter_search:
            await db.delete(parameter_search)
            await db.commit()
            logger.info(f"ParameterSearch ID {parameter_search_id} deleted successfully.")
            return True
        else:
            logger.warning(f"ParameterSearch ID {parameter_search_id} not found.")
            return False
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred while deleting ParameterSearch: {e}")
        await db.rollback()
        raise RuntimeError("Database error: Unable to delete ParameterSearch.")
