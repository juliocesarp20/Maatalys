from typing import Dict
from uuid import UUID

from pydantic import BaseModel


class SearchBase(BaseModel):
    source: str
    parameters: Dict[str, str]


class SearchCreate(SearchBase):
    investigation_id: UUID


class SearchResponse(SearchBase):
    id: UUID

    class Config:
        from_attributes = True
