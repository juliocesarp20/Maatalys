from uuid import UUID

from pydantic import BaseModel


class UserBase(BaseModel):
    nm_user: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id_user: UUID

    class Config:
        from_attributes = True
