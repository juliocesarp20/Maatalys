from pydantic import BaseModel
from uuid import UUID
from typing import Dict

class SearchBase(BaseModel):
    source: str
    parameters: Dict[str, str]

class SearchCreate(SearchBase):
    investigation_id: UUID

class SearchResponse(SearchBase):
    id: UUID
