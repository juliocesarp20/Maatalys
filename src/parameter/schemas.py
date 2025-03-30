from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ParameterBase(BaseModel):
    nm_parameter: str
    ds_parameter: Optional[str]


class ParameterCreate(ParameterBase):
    pass


class ParameterResponse(ParameterBase):
    id: UUID

    class Config:
        from_attributes = True
