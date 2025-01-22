from typing import List
from uuid import UUID

from pydantic import BaseModel

from src.parameter_search.schemas import ParameterSearchCreate, ParameterSearchResponse


class SearchBase(BaseModel):
    nm_source: str
    parameters: List[ParameterSearchCreate]


class SearchCreate(SearchBase):
    id_investigation: str
    pass


class SearchResponse(BaseModel):
    id: UUID
    nm_source: str
    parameter_searches: List[ParameterSearchResponse]
