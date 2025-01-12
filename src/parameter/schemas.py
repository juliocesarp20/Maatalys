from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional

class ParameterBase(BaseModel):
    name: str
    description: Optional[str]

class ParameterCreate(ParameterBase):
    pass

class ParameterResponse(ParameterBase):
    id: UUID
