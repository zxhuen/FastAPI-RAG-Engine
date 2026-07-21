from sqlalchemy import Column, Text, Integer, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from pgvector.sqlalchemy import Vector

from app.core.database import Base


class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    document_id = Column(
        UUID(as_uuid=True),
        ForeignKey("documents.id"),
        nullable=False
    )

    page_number = Column(Integer, nullable=True)
    chunk_index = Column(Integer, nullable=False)

    content = Column(Text, nullable=False)
    embedding = Column(Vector(768))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    document = relationship("Document", back_populates="chunks")