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


@router.get("/{id_search}", response_model=SearchResponse)
async def get_search(
    id_search: UUID,
    db: DbSession,
    search_service: Annotated[SearchService, Depends(SearchService)],
):
    search = await search_service.get_search_by_id(db, id_search)
    if not search:
        raise HTTPException(status_code=404, detail="Search not found.")
    return search


@router.get("/investigation/{id_investigation}", response_model=List[SearchResponse])
async def get_searches_for_investigation(
    id_investigation: UUID,
    db: DbSession,
    search_service: Annotated[SearchService, Depends(SearchService)],
):
    try:
        return await search_service.list_searches_by_investigation(db, id_investigation)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{id_search}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_search_by_id(
    id_search: UUID,
    db: DbSession,
    search_service: Annotated[SearchService, Depends(SearchService)],
):
    success = await search_service.delete_search(db, id_search)
    if not success:
        raise HTTPException(status_code=404, detail="Search not found.")
