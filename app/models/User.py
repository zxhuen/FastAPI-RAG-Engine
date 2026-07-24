from datetime import datetime

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

class User(Base):
    __tablename__ = "users"

    # Supabase Auth UUID
    id = Column(UUID(as_uuid=True), primary_key=True)

    email = Column(String(255), nullable=False, unique=True)
    display_name = Column(String(255), nullable=False)
    avatar_url = Column(String, nullable=True)

    premium_type_id = Column(
        Integer,
        ForeignKey("premium_types.id"),
        nullable=False,
    )

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    premium_type = relationship(
        "PremiumType",
        back_populates="users",
    )

    usage = relationship(
        "UserUsage",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
