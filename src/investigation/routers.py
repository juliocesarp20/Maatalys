from fastapi import APIRouter, Depends, status
from typing import List
from uuid import UUID
from src.investigation.schemas import (
    InvestigationCreate,
    InvestigationResponse,
)
from src.investigation.services import InvestigationService
from src.db.session import DbSession
from src.auth.services import CurrentUser

router = APIRouter()

investigation_service = InvestigationService()

@router.post("/", response_model=InvestigationResponse, status_code=status.HTTP_201_CREATED)
async def create_new_investigation(
    investigation: InvestigationCreate,
    db: DbSession,
    current_user: CurrentUser,
):
    return await investigation_service.create_investigation(db, investigation, current_user.id)

@router.get("/{investigation_id}", response_model=InvestigationResponse)
async def get_investigation(
    investigation_id: UUID,
    db: DbSession,
):
    return await investigation_service.get_investigation_by_id(db, investigation_id)

@router.get("/", response_model=List[InvestigationResponse])
async def get_user_investigations(
    db: DbSession,
    current_user: CurrentUser,
):
    return await investigation_service.list_investigations(db, current_user.id)

@router.delete("/{investigation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_investigation_by_id(
    investigation_id: UUID,
    db: DbSession,
):
    return await investigation_service.delete_investigation(db, investigation_id)
