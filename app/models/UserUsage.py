from datetime import datetime, UTC

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class UserUsage(Base):
    __tablename__ = "user_usage"

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )

    used_today = Column(Integer, default=0, nullable=False)

    last_reset_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="usage",
    )
