from sqlalchemy.orm import Session
from uuid import UUID
from app.models.Document import Document

def change_status(id: UUID, db: Session):
    return db.query(Document).filter(Document.id == id).first()
