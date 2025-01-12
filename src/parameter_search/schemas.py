from pydantic import BaseModel
from uuid import UUID

class ParameterSearchBase(BaseModel):
    search_id: UUID
    parameter_id: UUID
    value: str

class ParameterSearchCreate(ParameterSearchBase):
    pass

class ParameterSearchResponse(ParameterSearchBase):
    id: UUID
