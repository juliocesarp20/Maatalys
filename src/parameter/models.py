import uuid
from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import Mapped, relationship
from src.db.base import Base

class Parameter(Base):
    __tablename__ = "parameter"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    parameter_searches: Mapped[list["ParameterSearch"]] = relationship(
    "ParameterSearch", back_populates="parameter"
    )
