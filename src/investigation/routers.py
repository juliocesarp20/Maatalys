from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.auth.services import CurrentUser
from src.db.session import DbSession
from src.investigation.schemas import InvestigationCreate, InvestigationResponse
from src.investigation.services import InvestigationService
from src.streaming.event_producer_service import EventProducerService
from src.streaming.kafka_producer_service import get_kafka_producer

router = APIRouter()


@router.post(
    "/", response_model=InvestigationResponse, status_code=status.HTTP_201_CREATED
)
async def create_new_investigation(
    investigation: InvestigationCreate,
    db: DbSession,
    current_user: CurrentUser,
    investigation_service: Annotated[
        InvestigationService, Depends(InvestigationService)
    ],
    kafka_producer: Annotated[EventProducerService, Depends(get_kafka_producer)],
):
    investigation = await investigation_service.create_investigation(
        db, investigation, current_user.id, kafka_producer
    )
    return investigation


@router.get("/{investigation_id}", response_model=InvestigationResponse)
async def get_investigation(
    investigation_id: UUID,
    db: DbSession,
    investigation_service: Annotated[
        InvestigationService, Depends(InvestigationService)
    ],
):
    return await investigation_service.get_investigation_by_id(db, investigation_id)


@router.get("/", response_model=List[InvestigationResponse])
async def get_user_investigations(
    db: DbSession,
    current_user: CurrentUser,
    investigation_service: Annotated[
        InvestigationService, Depends(InvestigationService)
    ],
):
    return await investigation_service.list_investigations(db, current_user.id)
