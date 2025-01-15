from typing import Optional
from uuid import UUID

from pydantic import BaseModel, model_validator


class ParameterSearchBase(BaseModel):
    search_id: UUID
    parameter_id: UUID
    value: str


class ParameterSearchCreate(BaseModel):
    parameter_id: Optional[UUID] = None
    name: Optional[str] = None
    value: str

    @model_validator(mode="before")
    @classmethod
    def validate_one_of_required(cls, values):
        if not values.get("parameter_id") and not values.get("name"):
            raise ValueError("Either 'parameter_id' or 'name' must be provided.")
        return values


class ParameterSearchResponse(ParameterSearchBase):
    id: UUID
    parameter_id: UUID
    value: str
