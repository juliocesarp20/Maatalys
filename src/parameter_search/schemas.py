from uuid import UUID

from pydantic import BaseModel


class ParameterSearchBase(BaseModel):
    search_id: UUID
    parameter_id: UUID
    value: str


class ParameterSearchCreate(ParameterSearchBase):
    pass


class ParameterSearchResponse(ParameterSearchBase):
    id: UUID

    class Config:
        from_attributes = True
