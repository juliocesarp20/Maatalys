import uuid

from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base


class Parameter(Base):
    __tablename__ = "parameter"

    id_parameter: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    nm_parameter: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    ds_parameter: Mapped[str] = mapped_column(Text, nullable=True)
    parameter_searches: Mapped[list["ParameterSearch"]] = relationship(
        "ParameterSearch", back_populates="parameter"
    )
