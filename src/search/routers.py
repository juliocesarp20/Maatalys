from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.db.session import DbSession
from src.search.schemas import SearchCreate, SearchResponse
from src.search.services import SearchService

router = APIRouter()


@router.post("/", response_model=SearchResponse, status_code=status.HTTP_201_CREATED)
async def create_new_search(
    search: SearchCreate,
    db: DbSession,
    search_service: Annotated[SearchService, Depends(SearchService)],
):
    try:
        return await search_service.create_search(db, search)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{search_id}", response_model=SearchResponse)
async def get_search(
    search_id: UUID,
    db: DbSession,
    search_service: Annotated[SearchService, Depends(SearchService)],
):
    search = await search_service.get_search_by_id(db, search_id)
    if not search:
        raise HTTPException(status_code=404, detail="Search not found.")
    return search


@router.get("/investigation/{investigation_id}", response_model=List[SearchResponse])
async def get_searches_for_investigation(
    investigation_id: UUID,
    db: DbSession,
    search_service: Annotated[SearchService, Depends(SearchService)],
):
    try:
        return await search_service.list_searches_by_investigation(db, investigation_id)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{search_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_search_by_id(
    search_id: UUID,
    db: DbSession,
    search_service: Annotated[SearchService, Depends(SearchService)],
):
    success = await search_service.delete_search(db, search_id)
    if not success:
        raise HTTPException(status_code=404, detail="Search not found.")
