from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile, File
import logging  
from app.core.supabase_bucket import supabase

from app.schemas import subjectResponse, subjectCreate
from app.models import Subject

logger = logging.getLogger(__name__)

def create_subject(subject: subjectCreate, db: Session):
    new_subject = Subject(
        name = subject.name,
        term = subject.term
    )

    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)

    return new_subject



