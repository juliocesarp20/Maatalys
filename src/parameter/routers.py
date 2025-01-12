from fastapi import APIRouter, HTTPException, status, Depends
from src.parameter.schemas import ParameterCreate, ParameterResponse
from src.parameter.services import ParameterService
from src.db.session import DbSession
from typing import List
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=ParameterResponse, status_code=status.HTTP_201_CREATED)
async def create_new_parameter(
    parameter: ParameterCreate,
    db: DbSession,
    parameter_service: ParameterService = Depends()
):
    try:
        return await parameter_service.create_parameter(db, parameter)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=List[ParameterResponse])
async def get_all_parameters(
    db: DbSession,
    parameter_service: ParameterService = Depends()
):
    return await parameter_service.list_parameters(db)

@router.get("/{parameter_id}", response_model=ParameterResponse)
async def get_parameter(
    parameter_id: UUID,
    db: DbSession,
    parameter_service: ParameterService = Depends()
):
    parameter = await parameter_service.get_parameter_by_id(db, parameter_id)
    if not parameter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parameter not found.")
    return parameter

@router.delete("/{parameter_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_parameter_by_id(
    parameter_id: UUID,
    db: DbSession,
    parameter_service: ParameterService = Depends()
):
    success = await parameter_service.delete_parameter(db, parameter_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parameter not found.")
