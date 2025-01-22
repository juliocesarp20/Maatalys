import logging
import uuid
from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select

from src.db.session import DbSession
from src.parameter_search.models import ParameterSearch
from src.parameter_search.schemas import ParameterSearchCreate

logger = logging.getLogger(__name__)


async def create_parameter_search(
    db: DbSession, parameter_search_data: ParameterSearchCreate
) -> Optional[ParameterSearch]:
    logger.info(
        f"Creating parameter_search with id_search: {parameter_search_data.id_search} and value: {parameter_search_data.vl_parameter_search}"
    )
    new_parameter_search = ParameterSearch(
        id_search=parameter_search_data.id_search,
        id_parameter=parameter_search_data.id_parameter,
        vl_parameter_search=parameter_search_data.vl_parameter_search,
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


async def get_parameter_search_by_id(
    db: DbSession, id_parameter_search: uuid.UUID
) -> Optional[ParameterSearch]:
    logger.debug(f"Fetching parameter_search by ID: {id_parameter_search}")
    try:
        result = await db.execute(
            select(ParameterSearch).filter(
                ParameterSearch.id_parameter_search == id_parameter_search
            )
        )
        return result.scalar_one_or_none()
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred while fetching ParameterSearch: {e}")
        raise RuntimeError("Database error: Unable to fetch ParameterSearch.")


async def list_parameter_searches_for_search(
    db: DbSession, id_search: uuid.UUID
) -> List[ParameterSearch]:
    logger.debug(f"Listing parameter_searches for id_search: {id_search}")
    try:
        result = await db.execute(
            select(ParameterSearch).filter(ParameterSearch.id_search == id_search)
        )
        return result.scalars().all()
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred while listing ParameterSearches: {e}")
        raise RuntimeError("Database error: Unable to list ParameterSearches.")


async def delete_parameter_search(
    db: DbSession, id_parameter_search: uuid.UUID
) -> bool:
    logger.info(f"Deleting parameter_search ID: {id_parameter_search}")
    try:
        result = await db.execute(
            select(ParameterSearch).filter(
                ParameterSearch.id_parameter_search == id_parameter_search
            )
        )
        parameter_search = result.scalar_one_or_none()
        if parameter_search:
            await db.delete(parameter_search)
            await db.commit()
            logger.info(
                f"ParameterSearch ID {id_parameter_search} deleted successfully."
            )
            return True
        else:
            logger.warning(f"ParameterSearch ID {id_parameter_search} not found.")
            return False
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred while deleting ParameterSearch: {e}")
        await db.rollback()
        raise RuntimeError("Database error: Unable to delete ParameterSearch.")
