import logging
from typing import List, Optional
from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.db.session import DbSession
from src.investigation.models import Investigation
from src.investigation.schemas import InvestigationCreate, InvestigationResponse
from src.parameter.models import Parameter
from src.parameter_search.models import ParameterSearch
from src.search.models import Search
from src.streaming.event_producer_service import EventProducerService

logger = logging.getLogger(__name__)

from src.parameter.services import ParameterService

parameter_service = ParameterService()


class InvestigationService:
    async def create_investigation(
        self,
        db: DbSession,
        investigation_data: InvestigationCreate,
        user_id: UUID,
        event_producer: EventProducerService,
    ) -> Investigation:
        logger.info(f"Creating investigation: {investigation_data.name}")

        try:
            parameter_names = {
                param.name
                for search in investigation_data.searches
                for param in search.parameters
                if param.name
            }
            existing_parameters = await db.execute(
                select(Parameter).filter(Parameter.name.in_(parameter_names))
            )
            parameter_map = {
                param.name: param for param in existing_parameters.scalars()
            }

            missing_parameter_names = parameter_names - parameter_map.keys()
            if missing_parameter_names:
                new_parameters = await parameter_service.create_parameters(
                    list(missing_parameter_names), auto_commit=False
                )
                parameter_map.update({param.name: param for param in new_parameters})

            new_investigation = Investigation(
                name=investigation_data.name,
                user_id=user_id,
                searches=[
                    Search(
                        source=search_data.source,
                        parameter_searches=[
                            ParameterSearch(
                                parameter_id=parameter_map[param.name].id,
                                value=param.value,
                            )
                            for param in search_data.parameters
                            if param.name in parameter_map
                        ],
                    )
                    for search_data in investigation_data.searches
                ],
            )
            db.add(new_investigation)

            await db.commit()

            await db.refresh(new_investigation, ["user", "searches"])
            for search in new_investigation.searches:
                await db.refresh(search, ["parameter_searches"])

            logger.info(
                f"Investigation {investigation_data.name} created successfully."
            )
            import json

            investigation_response = InvestigationResponse.model_validate(
                new_investigation
            )
            await event_producer.publish(
                "abc",
                json.dumps(
                    {
                        "id": str(investigation_response.id),
                        "name": investigation_response.name,
                    }
                ),
            )
            return investigation_response

        except SQLAlchemyError as e:
            logger.error(f"Database error while creating investigation: {e}")
            await db.rollback()
            raise RuntimeError("Database error: Unable to create investigation.")

    async def get_investigation_by_id(
        self, db: DbSession, investigation_id: UUID
    ) -> Optional[Investigation]:
        """
        Fetch an investigation by its ID with eager loading.
        """
        logger.debug(f"Fetching investigation by ID: {investigation_id}")
        try:
            result = await db.execute(
                select(Investigation)
                .options(
                    selectinload(Investigation.user),
                    selectinload(Investigation.searches).selectinload(
                        Search.parameter_searches
                    ),
                )
                .filter(Investigation.id == investigation_id)
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"Database error occurred while fetching investigation: {e}")
            raise RuntimeError("Database error: Unable to fetch investigation.")

    async def list_investigations(
        self, db: DbSession, user_id: UUID
    ) -> List[Investigation]:
        """
        List all investigations for a specific user with eager loading.
        """
        logger.debug(f"Listing investigations for user ID: {user_id}")
        try:
            result = await db.execute(
                select(Investigation)
                .options(
                    selectinload(Investigation.user),
                    selectinload(Investigation.searches).selectinload(
                        Search.parameter_searches
                    ),
                )
                .filter(Investigation.user_id == user_id)
            )
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Database error occurred while listing investigations: {e}")
            raise RuntimeError("Database error: Unable to list investigations.")
