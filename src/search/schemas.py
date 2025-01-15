from typing import List
from uuid import UUID

from pydantic import BaseModel

from src.parameter_search.schemas import ParameterSearchCreate, ParameterSearchResponse


class SearchBase(BaseModel):
    source: str
    parameters: List[ParameterSearchCreate]


class SearchCreate(SearchBase):
    pass


class SearchResponse(BaseModel):
    id: UUID
    source: str
    parameter_searches: List[ParameterSearchResponse]
