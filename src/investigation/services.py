import logging
from typing import Optional
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
        id_user: UUID,
        event_producer: EventProducerService,
    ) -> Investigation:
        logger.info(f"Creating investigation: {investigation_data.nm_investigation}")

        try:
            parameter_names = {
                param.nm_parameter
                for search in investigation_data.searches
                for param in search.parameters
                if param.nm_parameter
            }
            existing_parameters = await db.execute(
                select(Parameter).filter(Parameter.nm_parameter.in_(parameter_names))
            )
            parameter_map = {
                param.nm_parameter: param for param in existing_parameters.scalars()
            }

            missing_parameter_names = parameter_names - parameter_map.keys()
            if missing_parameter_names:
                new_parameters = await parameter_service.create_parameters(
                    db=db,
                    parameter_names=list(missing_parameter_names),
                    auto_commit=False,
                )
                parameter_map.update(
                    {param.nm_parameter: param for param in new_parameters}
                )

            new_investigation = Investigation(
                nm_investigation=investigation_data.nm_investigation,
                id_user=id_user,
                searches=[
                    Search(
                        nm_source=search_data.nm_source,
                        parameter_searches=[
                            ParameterSearch(
                                id_parameter=parameter_map[
                                    param.nm_parameter
                                ].id_parameter,
                                vl_parameter_search=param.vl_parameter,
                            )
                            for param in search_data.parameters
                            if param.nm_parameter in parameter_map
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
                f"Investigation {investigation_data.nm_investigation} created successfully."
            )
            import json

            investigation_response = InvestigationResponse.model_validate(
                new_investigation
            )
            await event_producer.publish(
                "abc",
                json.dumps(
                    {
                        "id": str(investigation_response.id_investigation),
                        "name": investigation_response.nm_investigation,
                    }
                ),
            )
            return investigation_response

        except SQLAlchemyError as e:
            logger.error(f"Database error while creating investigation: {e}")
            await db.rollback()
            raise RuntimeError("Database error: Unable to create investigation.")

    async def get_investigation_by_id(
        self, db: DbSession, id_investigation: UUID
    ) -> Optional[Investigation]:
        """
        Fetch an investigation by its ID with eager loading.
        """
        logger.debug(f"Fetching investigation by ID: {id_investigation}")
        try:
            result = await db.execute(
                select(Investigation)
                .options(
                    selectinload(Investigation.user),
                    selectinload(Investigation.searches).selectinload(
                        Search.parameter_searches
                    ),
                )
                .filter(Investigation.id_investigation == id_investigation)
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"Database error occurred while fetching investigation: {e}")
            raise RuntimeError("Database error: Unable to fetch investigation.")

    async def list_investigations(
        self, db: DbSession, id_user: UUID
    ) -> list[Investigation]:
        """
        list all investigations for a specific user with eager loading.
        """
        logger.debug(f"Listing investigations for user ID: {id_user}")
        try:
            result = await db.execute(
                select(Investigation)
                .options(
                    selectinload(Investigation.user),
                    selectinload(Investigation.searches).selectinload(
                        Search.parameter_searches
                    ),
                )
                .filter(Investigation.id_user == id_user)
            )
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Database error occurred while listing investigations: {e}")
            raise RuntimeError("Database error: Unable to list investigations.")
