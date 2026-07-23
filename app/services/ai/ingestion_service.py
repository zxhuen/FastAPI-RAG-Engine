from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile, File
import logging  
from app.core.supabase_bucket import supabase

from app.schemas import DocumentCreate, DocumentResponse
from app.Repository.Subject_Repo import list_subjects, find_subject_name
from app.models import Document, Chunk

from uuid import UUID, uuid4

from app.core.status import DocumentStatus

def save_chunk(id: UUID, index: int, chunk: str, vector: float, db: Session):
    chunk = Chunk(
        document_id = id,
        chunk_index = index,
        content = chunk,
        embedding = vector
    )

    try:
        db.add(chunk)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )