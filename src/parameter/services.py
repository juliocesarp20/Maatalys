import logging
import uuid
from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select

from src.db.session import DbSession
from src.parameter.models import Parameter
from src.parameter.schemas import ParameterCreate

logger = logging.getLogger(__name__)


class ParameterService:
    async def create_parameter(
        self, db: DbSession, parameter_data: ParameterCreate
    ) -> Optional[Parameter]:
        """
        Create a new parameter and persist it to the database.
        """
        logger.info(f"Creating parameter: {parameter_data.nm_parameter}")
        new_parameter = Parameter(
            nm_parameter=parameter_data.nm_parameter,
            ds_parameter=parameter_data.ds_parameter,
        )
        try:
            db.add(new_parameter)
            await db.commit()
            await db.refresh(new_parameter)
            logger.info(f"Parameter {parameter_data.name} created successfully.")
            return new_parameter
        except SQLAlchemyError as e:
            logger.error(f"Database error occurred while creating parameter: {e}")
            await db.rollback()
            raise RuntimeError("Database error: Unable to create parameter.")

    async def create_parameters(
        self, db: DbSession, parameter_names: list[str], auto_commit: bool = True
    ) -> list[Parameter]:
        """
        Create multiple parameters in bulk.

        Args:
            db: Database session
            parameter_names: list of parameter names to create
            auto_commit: If True, commits immediately. If False, just adds to session
        """
        logger.info(f"Creating parameters: {parameter_names}")
        try:
            new_parameters = [Parameter(nm_parameter=name) for name in parameter_names]
            db.add_all(new_parameters)

            if auto_commit:
                await db.commit()
                for param in new_parameters:
                    await db.refresh(param)
            else:
                await db.flush()

            return new_parameters
        except SQLAlchemyError as e:
            logger.error(f"Database error occurred while creating parameters: {e}")
            if auto_commit:
                await db.rollback()
            raise RuntimeError("Database error: Unable to create parameters.")

    async def get_parameter_by_id(
        self, db: DbSession, id_parameter: uuid.UUID
    ) -> Optional[Parameter]:
        """
        Fetch a parameter by its ID.
        """
        logger.debug(f"Fetching parameter by ID: {id_parameter}")
        try:
            result = await db.execute(
                select(Parameter).filter(Parameter.id_parameter == id_parameter)
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"Database error occurred while fetching parameter: {e}")
            raise RuntimeError("Database error: Unable to fetch parameter.")

    async def list_parameters(self, db: DbSession) -> list[Parameter]:
        """
        list all parameters.
        """
        logger.debug("Listing all parameters.")
        try:
            result = await db.execute(select(Parameter))
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Database error occurred while listing parameters: {e}")
            raise RuntimeError("Database error: Unable to list parameters.")

    async def delete_parameter(self, db: DbSession, id_parameter: uuid.UUID) -> bool:
        """
        Delete a parameter by its ID.
        """
        logger.info(f"Deleting parameter ID: {id_parameter}")
        try:
            result = await db.execute(
                select(Parameter).filter(Parameter.id_parameter == id_parameter)
            )
            parameter = result.scalar_one_or_none()
            if parameter:
                await db.delete(parameter)
                await db.commit()
                logger.info(f"Parameter ID {id_parameter} deleted successfully.")
                return True
            else:
                logger.warning(f"Parameter ID {id_parameter} not found.")
                return False
        except SQLAlchemyError as e:
            logger.error(f"Database error occurred while deleting parameter: {e}")
            await db.rollback()
            raise RuntimeError("Database error: Unable to delete parameter.")
