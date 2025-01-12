import uuid
from sqlalchemy import String, ForeignKey, UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.db.base import Base
from src.user.models import User

class Investigation(Base):
    __tablename__ = "investigation"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="investigations")
    searches: Mapped[list["Search"]] = relationship(
        "Search", back_populates="investigation"
    )
