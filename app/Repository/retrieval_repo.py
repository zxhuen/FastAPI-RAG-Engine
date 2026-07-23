from sqlalchemy.orm import Session
from uuid import UUID
from app.models.Chunk import Chunk
from app.models.Document import Document

def find_similar_chunks(db: Session, embedding: list[float], subject_id: UUID | None = None, limit: int = 5):
    query = db.query(Chunk).join(Document).filter(Document.subject_id == subject_id)
    query_compare = query.order_by(Chunk.embedding.cosine_distance(embedding)).limit(limit)

    return query_compare.all()