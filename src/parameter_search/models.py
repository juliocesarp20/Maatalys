import uuid

from sqlalchemy import UUID, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base
from src.parameter.models import Parameter  # Ensure the Parameter model is imported
from src.search.models import Search  # Ensure the Search model is imported


class ParameterSearch(Base):
    __tablename__ = "tb_parameter_search"

    id_parameter_search: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    id_search: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tb_search.id_search"), nullable=False
    )
    id_parameter: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tb_parameter.id_parameter"), nullable=False
    )
    vl_parameter_search: Mapped[str] = mapped_column(String, nullable=False)

    search: Mapped["Search"] = relationship(
        "Search", back_populates="parameter_searches"
    )
    parameter: Mapped["Parameter"] = relationship(
        "Parameter", back_populates="parameter_searches"
    )
