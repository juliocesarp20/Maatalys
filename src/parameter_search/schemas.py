from typing import Optional
from uuid import UUID

from pydantic import BaseModel, model_validator


class ParameterSearchBase(BaseModel):
    id_search: UUID
    id_parameter: UUID
    vl_parameter_search: str


class ParameterSearchCreate(BaseModel):
    id_parameter: Optional[UUID] = None
    id_search: Optional[str] = None
    vl_parameter_search: str

    @model_validator(mode="before")
    @classmethod
    def validate_one_of_required(cls, values):
        if not values.get("id_parameter") and not values.get("name"):
            raise ValueError("Either 'id_parameter' or 'name' must be provided.")
        return values


class ParameterSearchResponse(ParameterSearchBase):
    id: UUID
    id_parameter: UUID
    value: str
