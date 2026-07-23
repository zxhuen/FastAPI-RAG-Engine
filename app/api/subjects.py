from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.limiter import limiter

from app.schemas import subjectCreate, subjectResponse
from app.services.subject_service import create_subject, list_all_subject

router = APIRouter(prefix="/Subjects", tags=["Subjects"])

@router.post("/add-subject")
@limiter.limit("0/minute")
def add_subject(request: Request, subject: subjectCreate, db: Session = Depends(get_db)):
    return create_subject(subject, db)

@router.get("/list-suject", response_model=list[subjectResponse])
def list_subject(db: Session = Depends(get_db)):
    return list_all_subject(db)

