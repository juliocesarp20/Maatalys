import uuid
from datetime import datetime
from typing import Literal, get_args

from sqlalchemy import UUID, Boolean, DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.db.base import Base
from src.investigation.models import Investigation

tp_status_values = Literal["WAITING", "FINISHED", "PROCESSING", "ERROR", "CANCELLED"]


class Search(Base):
    __tablename__ = "tb_search"

    id_search: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    nm_source: Mapped[str] = mapped_column(String, nullable=False)
    id_investigation: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tb_investigation.id_investigation"),
        nullable=False,
    )

    dt_creation: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    dt_processing: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    dt_finished: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    dt_cancelled: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    tp_status: Mapped[tp_status_values] = mapped_column(
        Enum(
            *get_args(tp_status_values),
            name="tp_status_enum",
            create_constraint=True,
            validate_strings=True,
        ),
        default="WAITING",
        nullable=False,
    )

    investigation: Mapped["Investigation"] = relationship(
        "Investigation", back_populates="searches"
    )
    parameter_searches: Mapped[list["ParameterSearch"]] = relationship(
        "ParameterSearch", back_populates="search"
    )
