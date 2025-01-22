import uuid

from sqlalchemy import UUID, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base
from src.user.models import User


class Investigation(Base):
    __tablename__ = "investigation"

    id_investigation: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    nm_investigation: Mapped[str] = mapped_column(String, nullable=False)
    id_user: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id_user"), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="investigations")
    searches: Mapped[list["Search"]] = relationship(
        "Search", back_populates="investigation"
    )
