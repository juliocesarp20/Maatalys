import datetime
from typing import List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class ParameterSearchCreate(BaseModel):
    id_parameter: Optional[UUID] = Field(None, alias="parameterId")
    nm_parameter: Optional[str]
    vl_parameter: str

    @model_validator(mode="before")
    @classmethod
    def validate_one_of_required(cls, values):
        if not (values.get("id_parameter") or values.get("nm_parameter")):
            raise ValueError(
                "Either 'id_parameter' or 'nm_parameter' must be provided."
            )
        return values


class SearchCreate(BaseModel):
    nm_source: str
    parameters: List[ParameterSearchCreate]


class InvestigationCreate(BaseModel):
    nm_investigation: str
    searches: List[SearchCreate]


class ParameterSearchResponse(BaseModel):
    id_parameter_search: UUID
    id_parameter: UUID
    vl_parameter_search: str

    class Config:
        from_attributes = True


class SearchResponse(BaseModel):
    id_search: UUID
    nm_source: str
    dt_created: datetime.datetime
    dt_processed: Union[datetime.datetime, None]
    dt_finished: Union[datetime.datetime, None]
    dt_cancelled: Union[datetime.datetime, None]
    parameter_searches: List[ParameterSearchResponse]

    class Config:
        from_attributes = True


class InvestigationResponse(BaseModel):
    id_investigation: UUID
    nm_investigation: str
    searches: List[SearchResponse]

    class Config:
        from_attributes = True
