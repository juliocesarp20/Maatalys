import uuid
from sqlalchemy import String, ForeignKey, UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.db.base import Base
from src.investigation.models import Investigation

class Search(Base):
    __tablename__ = "search"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    source: Mapped[str] = mapped_column(String, nullable=False)
    investigation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("investigation.id"), nullable=False
    )

    investigation: Mapped["Investigation"] = relationship(
        "Investigation", back_populates="searches"
    )
    parameter_searches: Mapped[list["ParameterSearch"]] = relationship(
        "ParameterSearch", back_populates="search"
    )
