from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ParameterBase(BaseModel):
    name: str
    description: Optional[str]


class ParameterCreate(ParameterBase):
    pass


class ParameterResponse(ParameterBase):
    id: UUID

    class Config:
        from_attributes = True
