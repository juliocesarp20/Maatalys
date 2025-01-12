from pydantic import BaseModel, Field, model_validator
from typing import Optional, List
from uuid import UUID

class ParameterSearchCreate(BaseModel):
    parameter_id: Optional[UUID] = Field(None, alias="parameterId")
    name: Optional[str]
    value: str

    @model_validator(mode="before")
    @classmethod
    def validate_one_of_required(cls, values):
        if not (values.get("parameter_id") or values.get("name")):
            raise ValueError("Either 'parameter_id' or 'name' must be provided.")
        return values

class SearchCreate(BaseModel):
    source: str
    parameters: List[ParameterSearchCreate]

class InvestigationCreate(BaseModel):
    name: str
    searches: List[SearchCreate]

class ParameterSearchResponse(BaseModel):
    id: UUID
    parameter_id: UUID
    value: str


class SearchResponse(BaseModel):
    id: UUID
    source: str
    parameters: List[ParameterSearchResponse]


class InvestigationResponse(BaseModel):
    id: UUID
    name: str
    searches: List[SearchResponse]

